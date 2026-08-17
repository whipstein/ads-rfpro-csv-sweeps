"""Explicitly save and run an RFPro analysis with configurable result reuse.

This script is intentionally separate from the CSV importer. Importing sweep
cases never launches a simulation. Run this file inside RFPro only when the
analysis is ready to be queued. The active project is saved immediately before
the public ``runAnalysis`` API is called. Existing-result reuse is controlled
by an editable global option passed through the public submission API. Required
private FEM environment overrides are applied to the RFPro process before
submission and remain set for the rest of the current RFPro session so
asynchronously launched solvers inherit them.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_REUSE_EXISTING_RESULTS = True
DEFAULT_RUN_ENVIRONMENT = {
    "FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR": "0.5",
    "FEMIZER_WAVEGUIDE_VERTICAL_FACTOR": "2.0",
    "FEM_ALWAYS_SOLVE_ON_FINEST_MESH": "on",
}


@dataclass(frozen=True)
class QtRuntime:
    application: Any
    pyside_file: Path
    plugin_file: Path | None
    application_was_created: bool
    environment_was_restored: bool


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
) -> str:
    environment_preview = "\n".join(
        f"  {name}={value}" for name, value in DEFAULT_RUN_ENVIRONMENT.items()
    )
    if reuse_existing:
        reuse_preview = (
            "Existing-result reuse: enabled",
            "RFPro will be asked to reuse valid existing results.",
            "Missing or invalidated instances may be queued for simulation.",
        )
    else:
        reuse_preview = (
            "Existing-result reuse: disabled",
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
            f"Submission option: reuseExistingIfPossible={bool(reuse_existing)}",
            "",
            "FEM run environment:",
            environment_preview,
            "",
            reuse_preview[1],
            reuse_preview[2],
            "The active RFPro project will be saved before submission.",
            "The FEM environment will remain set for the current RFPro session.",
            "This action starts the analysis now.",
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
    run_analysis: Callable[..., Any], analysis: Any, reuse_existing: bool
) -> Any:
    """Apply persistent FEM settings and submit with the requested reuse mode."""

    apply_session_environment(DEFAULT_RUN_ENVIRONMENT)
    return _submit_analysis(run_analysis, analysis, reuse_existing)


def _submit_analysis(
    run_analysis: Callable[..., Any], analysis: Any, reuse_existing: bool
) -> Any:
    """Submit an already prepared analysis through the public RFPro API."""

    return run_analysis(
        analysis,
        waitForConfirmation=False,
        saveProject=True,
        reuseExistingIfPossible=reuse_existing,
    )


def save_and_run_analysis(
    project: Any,
    run_analysis: Callable[..., Any],
    analysis: Any,
    reuse_existing: bool,
) -> Any:
    """Prepare and save synchronously, then submit the requested reuse mode."""

    apply_session_environment(DEFAULT_RUN_ENVIRONMENT)
    project.saveActiveProject()
    return _submit_analysis(run_analysis, analysis, reuse_existing)


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
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    return arguments


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
    preview = build_run_preview(
        analysis,
        configured_count,
        result_count,
        reuse_existing,
    )
    print(preview)
    if not arguments.yes and not _confirm_run(preview):
        print("Run cancelled; no RFPro simulations were started.")
        return

    save_and_run_analysis(
        empro.activeProject,
        runAnalysis,
        analysis,
        reuse_existing,
    )
    reuse_summary = "enabled" if reuse_existing else "disabled"
    summary = (
        f"Saved the active project and started analysis {analysis.name!r} "
        f"with submission-time existing-result reuse {reuse_summary}. "
        "Required FEM settings remain active for the current RFPro session."
    )
    print(summary)
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.information(None, "RFPro Analysis Started", summary)


if __name__ == "__main__":
    main()
