"""Explicitly save and run an RFPro analysis with configurable result reuse.

This script is intentionally separate from the CSV importer. Importing sweep
cases never launches a simulation. Run this file inside RFPro only when the
analysis is ready to be queued. The active project is saved immediately before
the public ``runAnalysis`` API is called. Existing-result reuse is controlled
by editable global options. The safe default preserves RFPro's native
Auto/reuse launch policy instead of silently authorizing overwrite behavior.
Required private FEM environment overrides are applied to the RFPro process
before submission and remain set for the rest of the current RFPro session so
asynchronously launched solvers inherit them. Simulations selected by RFPro
are staged under a native queue hold and released through a configurable
bounded window so SiteCluster does not receive the entire sweep at once.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_REUSE_EXISTING_RESULTS = True
# Keep this True to follow the same native RFPro reuse/confirmation path used
# when starting an analysis from the GUI with its reuse policy set to Auto.
DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY = True
# SiteCluster/RFPro job throttle. A value of 1 submits exactly one simulation
# and waits for it to finish before submitting the next. Larger values maintain
# that many active simulations with a sliding window.
DEFAULT_MAX_CONCURRENT_SIMULATIONS = 1
DEFAULT_STOP_SUBMITTING_ON_ERROR = True
DEFAULT_BATCH_POLL_SECONDS = 0.5
DEFAULT_RUN_ENVIRONMENT = {
    "FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR": "0.5",
    "FEMIZER_WAVEGUIDE_VERTICAL_FACTOR": "2.0",
    "FEM_ALWAYS_SOLVE_ON_FINEST_MESH": "on",
}

_ONGOING_SIMULATION_STATUSES = frozenset(
    {"Queued", "Running", "PostProcessing", "Interrupting", "Killing"}
)


@dataclass(frozen=True)
class QtRuntime:
    application: Any
    pyside_file: Path
    plugin_file: Path | None
    application_was_created: bool
    environment_was_restored: bool


@dataclass(frozen=True)
class BatchRunResult:
    """Outcome of a bounded-concurrency RFPro queue run."""

    staged_count: int
    submitted_ids: tuple[str, ...]
    completed_ids: tuple[str, ...]
    failed: tuple[tuple[str, str], ...]
    remaining_ids: tuple[str, ...]

    @property
    def submitted_count(self) -> int:
        return len(self.submitted_ids)


def _expected_qt_platform_plugin() -> str:
    if sys.platform.startswith("linux"):
        return "libqxcb.so"
    if sys.platform == "win32":
        return "qwindows.dll"
    if sys.platform == "darwin":
        return "libqcocoa.dylib"
    raise RuntimeError(f"Unsupported Qt platform: {sys.platform}")


def _locate_qt_platform_plugin(pyside_file: Path) -> Path:
    """Ask Qt for plugin roots, then search the active ADS/EMPro roots."""

    from PySide6.QtCore import QCoreApplication, QLibraryInfo

    plugin_name = _expected_qt_platform_plugin()
    directories: list[Path] = []

    def add_directory(path: Path) -> None:
        try:
            resolved = path.expanduser().resolve()
        except OSError:
            return
        if resolved not in directories:
            directories.append(resolved)

    def add_plugin_root(path: Path) -> None:
        add_directory(path)
        if path.name != "platforms":
            add_directory(path / "platforms")

    qt_plugins_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath)
    if qt_plugins_path:
        add_plugin_root(Path(qt_plugins_path))
    for library_path in QCoreApplication.libraryPaths():
        if library_path:
            add_plugin_root(Path(library_path))

    pyside_root = pyside_file.parent
    add_directory(pyside_root / "plugins" / "platforms")
    add_directory(pyside_root / "Qt" / "plugins" / "platforms")
    for environment_name in ("QT_QPA_PLATFORM_PLUGIN_PATH", "QT_PLUGIN_PATH"):
        for entry in os.environ.get(environment_name, "").split(os.pathsep):
            if entry:
                add_plugin_root(Path(entry))

    for directory in directories:
        plugin_file = directory / plugin_name
        if plugin_file.is_file():
            return plugin_file

    fallback_roots = [pyside_root, Path(sys.prefix)]
    executable = Path(sys.executable).resolve()
    for ancestor in executable.parents:
        if ancestor.name.lower() == "tools":
            fallback_roots.append(ancestor.parent)
            break
    hpeesof_dir = os.environ.get("HPEESOF_DIR")
    if hpeesof_dir:
        fallback_roots.append(Path(hpeesof_dir))
    empro_home = os.environ.get("EMPROHOME")
    if empro_home:
        fallback_roots.append(Path(empro_home))

    searched_roots: list[Path] = []
    for root in fallback_roots:
        try:
            resolved_root = root.expanduser().resolve()
        except OSError:
            continue
        if not resolved_root.is_dir() or resolved_root in searched_roots:
            continue
        searched_roots.append(resolved_root)
        try:
            for match in resolved_root.rglob(plugin_name):
                if match.is_file():
                    return match
        except OSError:
            continue

    checked = [str(path / plugin_name) for path in directories]
    checked.extend(f"recursive: {root}" for root in searched_roots)
    details = "\n  ".join(checked) if checked else "(no valid search roots)"
    raise RuntimeError(
        f"Qt platform plugin {plugin_name!r} was not found automatically.\n"
        f"PySide6: {pyside_file}\nSearched:\n  {details}\n"
        "Run scripts/diagnose_qt.py with the exact RFPro interpreter."
    )


def _validate_linux_plugin(plugin_file: Path) -> None:
    if not sys.platform.startswith("linux"):
        return
    try:
        result = subprocess.run(
            ["ldd", str(plugin_file)],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise RuntimeError(f"Could not inspect Qt plugin {plugin_file}: {error}") from error
    unresolved = [
        line.strip()
        for line in (result.stdout + result.stderr).splitlines()
        if "not found" in line
    ]
    if unresolved:
        details = "\n  ".join(unresolved)
        raise RuntimeError(
            f"Qt found {plugin_file}, but required libraries are missing:\n  {details}"
        )


def create_or_reuse_qapplication() -> QtRuntime:
    """Reuse RFPro-owned Qt, or create script-owned Qt with a scoped redirect."""

    try:
        import PySide6
    except Exception as error:
        raise RuntimeError(
            "PySide6 could not be imported. Run this script directly in RFPro "
            f"or with its bundled Python interpreter, not {sys.executable!r}."
        ) from error

    from PySide6.QtWidgets import QApplication

    pyside_file = Path(PySide6.__file__).resolve()
    application = QApplication.instance()
    if application is not None:
        return QtRuntime(application, pyside_file, None, False, True)

    plugin_file = _locate_qt_platform_plugin(pyside_file)
    _validate_linux_plugin(plugin_file)
    if sys.platform.startswith("linux"):
        selected_platform = os.environ.get("QT_QPA_PLATFORM", "").lower()
        has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
        if not has_display and selected_platform not in {"offscreen", "minimal"}:
            raise RuntimeError(
                "No DISPLAY or WAYLAND_DISPLAY is available for graphical RFPro. "
                "Launch from a graphical session; this script does not force offscreen mode."
            )

    variable = "QT_QPA_PLATFORM_PLUGIN_PATH"
    was_set = variable in os.environ
    previous = os.environ.get(variable)
    os.environ[variable] = str(plugin_file.parent)
    try:
        application = QApplication([])
    finally:
        if was_set:
            os.environ[variable] = previous if previous is not None else ""
        else:
            os.environ.pop(variable, None)

    restored = (
        os.environ.get(variable) == previous if was_set else variable not in os.environ
    )
    return QtRuntime(application, pyside_file, plugin_file, True, restored)


def analysis_names(project: Any) -> list[str]:
    return [str(name) for name in project.analyses.names()]


def find_analysis(project: Any, name: str) -> Any:
    names = analysis_names(project)
    if not names:
        raise RuntimeError("The active RFPro project contains no analyses.")
    if name:
        if name not in names:
            raise ValueError(
                f"Analysis {name!r} does not exist. Available analyses: {', '.join(names)}"
            )
        return project.analyses[project.analyses.index(name)]
    if len(names) == 1:
        return project.analyses[0]
    raise ValueError("An analysis name is required when the project has multiple analyses.")


def _choose_analysis(project: Any, requested_name: str) -> Any:
    names = analysis_names(project)
    if requested_name or len(names) <= 1:
        return find_analysis(project, requested_name)

    from PySide6.QtWidgets import QInputDialog

    selected, accepted = QInputDialog.getItem(
        None,
        "Run RFPro Analysis with Result Reuse",
        "Analysis:",
        names,
        0,
        False,
    )
    if not accepted:
        raise RuntimeError("Analysis selection was cancelled.")
    return find_analysis(project, str(selected))


def _configured_instance_count(analysis: Any) -> int:
    return int(analysis.simulationSettings.numberOfParameterInstances)


def _available_result_ids(empro_module: Any, analysis: Any) -> list[Any]:
    output = empro_module.output.AnalysisOutput(analysis)
    return list(output.getAvailableSimulationIds())


def apply_session_environment(overrides: Mapping[str, str]) -> None:
    """Set persistent process values inherited by later RFPro solver launches."""

    for name, value in overrides.items():
        os.environ[name] = value
    mismatches = {
        name: os.environ.get(name)
        for name, expected in overrides.items()
        if os.environ.get(name) != expected
    }
    if mismatches:
        raise RuntimeError(
            "Could not apply the required RFPro session environment: "
            + ", ".join(f"{name}={value!r}" for name, value in mismatches.items())
        )
    print("Persistent RFPro session environment applied:")
    for name, value in overrides.items():
        print(f"  {name}={value}")


def validate_reuse_supported(empro_module: Any, analysis: Any) -> None:
    """Reject analysis types for which the public reuse flag is not defined."""

    analysis_class = empro_module.analysis.Analysis
    supported_types = {
        analysis_class.EMFUAnalysisType,
        analysis_class.EMUDAnalysisType,
        analysis_class.EMFUPEAnalysisType,
        analysis_class.EMUDPEAnalysisType,
    }
    if analysis.analysisType not in supported_types:
        raise ValueError(
            f"Analysis {analysis.name!r} has type {analysis.analysisType!r}. "
            "The public RFPro existing-result reuse option is supported only "
            "for EMFU, EMUD, EMFUPE, and EMUDPE analyses. Nothing was started."
        )


def build_run_preview(
    analysis: Any,
    configured_count: int,
    result_count: int,
    reuse_existing: bool,
    use_native_reuse_policy: bool = DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY,
    max_concurrent_simulations: int = DEFAULT_MAX_CONCURRENT_SIMULATIONS,
    stop_submitting_on_error: bool = DEFAULT_STOP_SUBMITTING_ON_ERROR,
) -> str:
    environment_preview = "\n".join(
        f"  {name}={value}" for name, value in DEFAULT_RUN_ENVIRONMENT.items()
    )
    if use_native_reuse_policy:
        reuse_preview = (
            "Existing-result policy: RFPro native Auto/dialog",
            "RFPro's native analysis launch path will make the final reuse decision.",
            "An additional native RFPro confirmation may appear; do not approve "
            "an overwrite unless a full rerun is intended.",
        )
    elif reuse_existing:
        reuse_preview = (
            "Existing-result policy: scripted reuse",
            "RFPro will be asked to reuse valid existing results.",
            "Missing or invalidated instances may be queued for simulation.",
        )
    else:
        reuse_preview = (
            "Existing-result policy: scripted overwrite",
            "RFPro will be asked to run regardless of existing results.",
            "All configured instances may be queued for simulation.",
        )
    return "\n".join(
        (
            f"Analysis: {analysis.name}",
            f"Configured parameter instances: {configured_count}",
            f"Existing result sets: {result_count}",
            f"Potentially missing instances: {max(configured_count - result_count, 0)}",
            reuse_preview[0],
            f"Submission option: waitForConfirmation={bool(use_native_reuse_policy)}",
            f"Submission option: reuseExistingIfPossible={bool(reuse_existing)}",
            f"Maximum active simulations: {max_concurrent_simulations}",
            (
                "Failure policy: stop submitting new jobs after the first error"
                if stop_submitting_on_error
                else "Failure policy: continue submitting remaining jobs after errors"
            ),
            "",
            "FEM run environment:",
            environment_preview,
            "",
            reuse_preview[1],
            reuse_preview[2],
            "The active RFPro project will be saved before submission.",
            "The RFPro queue must be idle. Jobs selected by RFPro will be staged "
            "under queue hold, then released through the configured sliding window.",
            "The FEM environment will remain set for the current RFPro session.",
            "This script stays open until every submitted simulation finishes.",
        )
    )


def _confirm_run(preview: str) -> bool:
    from PySide6.QtWidgets import QMessageBox

    answer = QMessageBox.question(
        None,
        "Save and start RFPro analysis?",
        preview,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return answer == QMessageBox.StandardButton.Yes


def run_analysis_reusing_results(
    run_analysis: Callable[..., Any],
    analysis: Any,
    reuse_existing: bool,
    use_native_reuse_policy: bool = DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY,
) -> Any:
    """Apply persistent FEM settings and submit with the requested reuse mode."""

    apply_session_environment(DEFAULT_RUN_ENVIRONMENT)
    return _submit_analysis(
        run_analysis, analysis, reuse_existing, use_native_reuse_policy
    )


def _submit_analysis(
    run_analysis: Callable[..., Any],
    analysis: Any,
    reuse_existing: bool,
    use_native_reuse_policy: bool,
) -> Any:
    """Submit an already prepared analysis through the public RFPro API."""

    return run_analysis(
        analysis,
        waitForConfirmation=use_native_reuse_policy,
        saveProject=True,
        reuseExistingIfPossible=reuse_existing,
    )


def save_and_run_analysis(
    project: Any,
    run_analysis: Callable[..., Any],
    analysis: Any,
    reuse_existing: bool,
    use_native_reuse_policy: bool = DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY,
) -> Any:
    """Prepare and save synchronously, then submit the requested reuse mode."""

    apply_session_environment(DEFAULT_RUN_ENVIRONMENT)
    project.saveActiveProject()
    return _submit_analysis(
        run_analysis, analysis, reuse_existing, use_native_reuse_policy
    )


def _simulation_status(simulation: Any) -> str:
    return str(simulation.status)


def _simulation_label(simulation: Any) -> str:
    """Return a stable, readable simulation identifier without assuming bindings."""

    for attribute_name in ("id", "simulationPath"):
        value = getattr(simulation, attribute_name, None)
        try:
            value = value() if callable(value) else value
        except Exception:
            continue
        if value in (None, ""):
            continue
        text = str(value)
        if attribute_name == "simulationPath":
            leaf = Path(text).name
            if leaf:
                return leaf
        return text
    return f"simulation@{id(simulation):x}"


def _pump_simulation_events(
    _simulations: Any,
    process_events: Callable[[], None],
) -> None:
    # Match empro.toolkit.simulation.wait(): Qt event processing updates each
    # live Simulation.status. SimulationList.refresh() is intentionally avoided
    # because the public wait implementation does not require it.
    process_events()


def _ongoing_simulations(simulations: Any) -> list[Any]:
    return [
        simulation
        for simulation in list(simulations)
        if _simulation_status(simulation) in _ONGOING_SIMULATION_STATUSES
    ]


def _format_simulation_list(simulations: Sequence[Any]) -> str:
    labels = [_simulation_label(simulation) for simulation in simulations]
    return ", ".join(labels[:10]) + (" ..." if len(labels) > 10 else "")


def stage_analysis_simulations(
    simulations: Any,
    submit_analysis: Callable[[], Any],
    process_events: Callable[[], None],
) -> list[Any]:
    """Create RFPro-selected jobs under queue hold, then safely unqueue them.

    This requires exclusive ownership of an idle RFPro queue. If RFPro cannot
    be proven to have unqueued every staged job, the queue is deliberately left
    held so SiteCluster cannot receive the full sweep simultaneously.
    """

    _pump_simulation_events(simulations, process_events)
    ongoing_before = _ongoing_simulations(simulations)
    if ongoing_before:
        raise RuntimeError(
            "Bounded submission requires an idle RFPro queue. These simulations "
            f"are already active: {_format_simulation_list(ongoing_before)}. "
            "Wait for them to finish or remove them from the queue, then run the "
            "script again. Nothing new was submitted."
        )
    if bool(simulations.isQueueHeld):
        raise RuntimeError(
            "The RFPro queue is already held. Release the existing hold after "
            "checking the Simulation window, then run the script again. Nothing "
            "new was submitted."
        )

    queue_hold_was_set = False
    try:
        simulations.isQueueHeld = True
        queue_hold_was_set = True
        if not bool(simulations.isQueueHeld):
            raise RuntimeError("RFPro did not accept the requested queue hold.")

        submit_analysis()
        _pump_simulation_events(simulations, process_events)
        if not bool(simulations.isQueueHeld):
            raise RuntimeError(
                "RFPro released the queue hold while preparing the analysis."
            )

        staged = [
            simulation
            for simulation in list(simulations)
            if _simulation_status(simulation) == "Queued"
        ]
        if not staged:
            simulations.isQueueHeld = False
            return []

        for simulation in staged:
            simulation.setQueued(False)
        _pump_simulation_events(simulations, process_events)
        still_queued = [
            simulation
            for simulation in staged
            if _simulation_status(simulation) == "Queued"
        ]
        if still_queued:
            raise RuntimeError(
                "RFPro did not remove every staged simulation from the queue: "
                f"{_format_simulation_list(still_queued)}."
            )

        simulations.isQueueHeld = False
        return staged
    except Exception as error:
        if queue_hold_was_set:
            # Reassert the hold before inspecting state. Even if RFPro changed it
            # unexpectedly, queued jobs must not fan out to SiteCluster.
            try:
                simulations.isQueueHeld = True
            except Exception:
                pass
            try:
                ongoing = _ongoing_simulations(simulations)
            except Exception:
                ongoing = []
            if ongoing:
                raise RuntimeError(
                    "Could not safely stage the RFPro simulations for bounded "
                    "SiteCluster submission. The RFPro queue was left HELD so "
                    "no additional queued jobs can launch. Inspect the Simulation "
                    "window before releasing it. Active or queued simulations: "
                    f"{_format_simulation_list(ongoing)}."
                ) from error
            try:
                simulations.isQueueHeld = False
            except Exception:
                pass
        raise


def run_staged_simulations_with_limit(
    simulations: Any,
    staged: Sequence[Any],
    max_concurrent_simulations: int,
    stop_submitting_on_error: bool,
    process_events: Callable[[], None],
    sleep: Callable[[float], None] = time.sleep,
    poll_seconds: float = DEFAULT_BATCH_POLL_SECONDS,
) -> BatchRunResult:
    """Run staged simulations through a bounded sliding submission window."""

    if max_concurrent_simulations < 1:
        raise ValueError("Maximum active simulations must be at least 1.")
    if poll_seconds < 0:
        raise ValueError("Batch poll seconds cannot be negative.")

    pending = list(staged)
    active: list[Any] = []
    submitted_ids: list[str] = []
    completed_ids: list[str] = []
    failed: list[tuple[str, str]] = []
    submission_stopped = False

    while active or (pending and not submission_stopped):
        while (
            pending
            and len(active) < max_concurrent_simulations
            and not submission_stopped
        ):
            simulation = pending.pop(0)
            label = _simulation_label(simulation)
            try:
                simulation.setQueued(True)
            except Exception as error:
                failed.append((label, f"submission error: {error}"))
                print(f"Could not submit simulation {label}: {error}")
                if stop_submitting_on_error:
                    submission_stopped = True
                continue
            active.append(simulation)
            submitted_ids.append(label)
            print(
                f"Submitted simulation {label} "
                f"({len(active)}/{max_concurrent_simulations} active slots)."
            )

        if not active:
            continue

        _pump_simulation_events(simulations, process_events)
        still_active: list[Any] = []
        saw_terminal_status = False
        for simulation in active:
            label = _simulation_label(simulation)
            status = _simulation_status(simulation)
            if status in _ONGOING_SIMULATION_STATUSES:
                still_active.append(simulation)
                continue

            saw_terminal_status = True
            if status == "Completed":
                completed_ids.append(label)
                print(f"Completed simulation {label}.")
            else:
                failed.append((label, status))
                print(f"Simulation {label} ended with status {status!r}.")
                if stop_submitting_on_error:
                    submission_stopped = True
        active = still_active

        if active and not saw_terminal_status:
            sleep(poll_seconds)

    return BatchRunResult(
        staged_count=len(staged),
        submitted_ids=tuple(submitted_ids),
        completed_ids=tuple(completed_ids),
        failed=tuple(failed),
        remaining_ids=tuple(_simulation_label(simulation) for simulation in pending),
    )


def save_and_run_analysis_batched(
    project: Any,
    run_analysis: Callable[..., Any],
    analysis: Any,
    reuse_existing: bool,
    max_concurrent_simulations: int,
    stop_submitting_on_error: bool = DEFAULT_STOP_SUBMITTING_ON_ERROR,
    use_native_reuse_policy: bool = DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY,
    process_events: Callable[[], None] = lambda: None,
    sleep: Callable[[float], None] = time.sleep,
    poll_seconds: float = DEFAULT_BATCH_POLL_SECONDS,
) -> BatchRunResult:
    """Save, let RFPro select required jobs, then submit them with a limit."""

    if max_concurrent_simulations < 1:
        raise ValueError("Maximum active simulations must be at least 1.")
    apply_session_environment(DEFAULT_RUN_ENVIRONMENT)
    project.saveActiveProject()
    staged = stage_analysis_simulations(
        project.simulations,
        lambda: _submit_analysis(
            run_analysis, analysis, reuse_existing, use_native_reuse_policy
        ),
        process_events,
    )
    return run_staged_simulations_with_limit(
        project.simulations,
        staged,
        max_concurrent_simulations,
        stop_submitting_on_error,
        process_events,
        sleep,
        poll_seconds,
    )


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Explicitly save and run RFPro with configurable result reuse.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--analysis", default=DEFAULT_ANALYSIS_NAME, help="RFPro analysis name"
    )
    parser.add_argument(
        "--yes", action="store_true", help="start without the confirmation dialog"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=DEFAULT_MAX_CONCURRENT_SIMULATIONS,
        metavar="COUNT",
        help="maximum queued/running simulations submitted at one time",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="keep submitting remaining simulations after a job fails",
    )
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    if arguments.max_concurrent < 1:
        parser.error("--max-concurrent must be at least 1")
    return arguments


def _batch_summary(analysis: Any, result: BatchRunResult) -> str:
    if result.staged_count == 0:
        return (
            f"Saved the active project. RFPro selected no simulations to run "
            f"for analysis {analysis.name!r}; existing valid results were left "
            "untouched. Required FEM settings remain active for this RFPro session."
        )

    parts = [
        f"Finished bounded submission for analysis {analysis.name!r}.",
        f"Staged: {result.staged_count}.",
        f"Submitted: {result.submitted_count}.",
        f"Completed: {len(result.completed_ids)}.",
        f"Failed: {len(result.failed)}.",
        f"Not submitted: {len(result.remaining_ids)}.",
    ]
    if result.failed:
        failure_text = ", ".join(
            f"{label} ({status})" for label, status in result.failed[:10]
        )
        parts.append(f"Failures: {failure_text}.")
    if result.remaining_ids:
        parts.append(
            "Remaining unsubmitted: " + ", ".join(result.remaining_ids[:10]) + "."
        )
    parts.append("Required FEM settings remain active for this RFPro session.")
    return " ".join(parts)


def _print_qt_diagnostics(runtime: QtRuntime) -> None:
    ownership = "created by script" if runtime.application_was_created else "reused from RFPro"
    plugin = (
        str(runtime.plugin_file)
        if runtime.plugin_file is not None
        else "already loaded by RFPro; search path unchanged"
    )
    print(f"Python executable: {sys.executable}")
    print(f"PySide6 package: {runtime.pyside_file}")
    print(f"Qt platform plugin: {plugin}")
    print(f"Qt platform: {runtime.application.platformName()}")
    print(f"QApplication: {ownership}")
    print(f"Qt environment restored: {runtime.environment_was_restored}")


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    qt_runtime = create_or_reuse_qapplication()
    _print_qt_diagnostics(qt_runtime)

    import empro
    from empro.toolkit.analysis import runAnalysis

    analysis = _choose_analysis(empro.activeProject, arguments.analysis)
    validate_reuse_supported(empro, analysis)
    configured_count = _configured_instance_count(analysis)
    result_count = len(_available_result_ids(empro, analysis))
    reuse_existing = DEFAULT_REUSE_EXISTING_RESULTS
    use_native_reuse_policy = DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY
    preview = build_run_preview(
        analysis,
        configured_count,
        result_count,
        reuse_existing,
        use_native_reuse_policy,
        arguments.max_concurrent,
        not arguments.continue_on_error,
    )
    print(preview)
    if not arguments.yes and not _confirm_run(preview):
        print("Run cancelled; no RFPro simulations were started.")
        return

    result = save_and_run_analysis_batched(
        empro.activeProject,
        runAnalysis,
        analysis,
        reuse_existing,
        arguments.max_concurrent,
        not arguments.continue_on_error,
        use_native_reuse_policy,
        empro.gui.processEvents,
    )
    summary = _batch_summary(analysis, result)
    print(summary)
    from PySide6.QtWidgets import QMessageBox

    if result.failed or result.remaining_ids:
        QMessageBox.warning(None, "RFPro Bounded Run Finished with Errors", summary)
    else:
        QMessageBox.information(None, "RFPro Bounded Run Finished", summary)


if __name__ == "__main__":
    main()
