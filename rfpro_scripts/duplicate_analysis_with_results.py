"""Duplicate an RFPro analysis and its complete saved simulation-result group.

Run this script inside RFPro. It deep-clones the selected Analysis, allocates a
new simulation-group ID, copies the source group directory without modifying
it, registers the cloned Analysis, verifies its public AnalysisOutput paths,
and saves the project. It never starts or queues a simulation.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_DUPLICATE_NAME = ""


@dataclass(frozen=True)
class QtRuntime:
    application: Any
    pyside_file: Path
    plugin_file: Path | None
    application_was_created: bool
    environment_was_restored: bool


@dataclass(frozen=True)
class DuplicatePlan:
    source_name: str
    duplicate_name: str
    source_group: str
    duplicate_group: str
    source_group_path: Path
    duplicate_group_path: Path
    registered_result_ids: tuple[str, ...]
    registered_result_paths: tuple[Path, ...]
    source_size_bytes: int


@dataclass(frozen=True)
class DuplicateResult:
    duplicate: Any
    plan: DuplicatePlan
    verified_result_ids: tuple[str, ...]


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


def analysis_names(project: Any) -> list[str]:
    return [str(name) for name in project.analyses.names()]


def find_analysis(project: Any, name: str) -> Any:
    names = analysis_names(project)
    if not names:
        raise RuntimeError("The active RFPro project contains no analyses.")
    if name:
        if name not in names:
            raise ValueError(
                f"Analysis {name!r} does not exist. Available analyses: "
                + ", ".join(names)
            )
        return project.analyses[project.analyses.index(name)]
    if len(names) == 1:
        return project.analyses[0]
    raise ValueError(
        "Set DEFAULT_ANALYSIS_NAME or pass --analysis. Available analyses: "
        + ", ".join(names)
    )


def default_duplicate_name(source_name: str, existing_names: Sequence[str]) -> str:
    existing = set(existing_names)
    candidate = f"{source_name} Copy"
    suffix = 2
    while candidate in existing:
        candidate = f"{source_name} Copy {suffix}"
        suffix += 1
    return candidate


def validate_duplicate_name(name: str, existing_names: Sequence[str]) -> str:
    cleaned = str(name).strip()
    if not cleaned:
        raise ValueError("The duplicate analysis name cannot be empty.")
    if cleaned in set(existing_names):
        raise ValueError(f"An analysis named {cleaned!r} already exists.")
    return cleaned


def _call_or_value(value: Any, default: Any = None) -> Any:
    if value is None:
        return default
    try:
        return value() if callable(value) else value
    except Exception:
        return default


def running_simulation_descriptions(project: Any) -> list[str]:
    """Return public simulation entries that are running or waiting to run."""

    active: list[str] = []
    active_status_words = ("queue", "pending", "submit", "start", "running", "solving")
    for index, simulation in enumerate(project.simulations):
        is_running = bool(_call_or_value(getattr(simulation, "isRunning", None), False))
        has_running_status = bool(
            _call_or_value(getattr(simulation, "hasRunningStatus", None), False)
        )
        status = str(_call_or_value(getattr(simulation, "status", None), "") or "")
        status_is_active = any(word in status.casefold() for word in active_status_words)
        if not (is_running or has_running_status or status_is_active):
            continue
        name = str(getattr(simulation, "name", "") or f"simulation {index + 1}")
        path = str(_call_or_value(getattr(simulation, "simulationPath", None), "") or "")
        active.append(f"{name} (status={status or 'active'}, path={path or 'unknown'})")
    return active


def normalized_path(path: Path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def path_is_within(path: Path, root: Path) -> bool:
    try:
        return os.path.commonpath((normalized_path(path), normalized_path(root))) == normalized_path(root)
    except ValueError:
        return False


def remap_group_path(path_text: str, source_group: Path, duplicate_group: Path) -> str:
    """Map one source-group path to the same relative duplicate-group path."""

    if not str(path_text or "").strip():
        return ""
    source_path = Path(str(path_text))
    if not path_is_within(source_path, source_group):
        raise RuntimeError(
            f"Analysis simulationPath {source_path} is outside its simulation "
            f"group {source_group}; it cannot be copied safely."
        )
    relative = Path(os.path.relpath(str(source_path), str(source_group)))
    return str(duplicate_group / relative)


def directory_size(path: Path) -> int:
    total = 0
    for root, _directories, filenames in os.walk(path, followlinks=False):
        for filename in filenames:
            file_path = Path(root) / filename
            try:
                total += file_path.stat(follow_symlinks=False).st_size
            except OSError:
                pass
    return total


def _valid_group_id(group: Any) -> str:
    text = str(group or "").strip()
    if not text or text in {".", ".."} or Path(text).name != text:
        raise RuntimeError(f"RFPro returned an invalid simulation-group ID: {text!r}")
    return text


def prepare_duplicate_plan(
    empro_module: Any,
    project: Any,
    source: Any,
    duplicate_name: str,
) -> DuplicatePlan:
    duplicate_name = validate_duplicate_name(duplicate_name, analysis_names(project))
    output = empro_module.output.AnalysisOutput(source)
    result_ids = tuple(str(value) for value in (output.getAvailableSimulationIds() or []))
    result_paths = tuple(
        Path(str(value)) for value in (output.getAvailableSimulationPaths() or [])
    )
    if not result_ids:
        raise RuntimeError(
            f"Analysis {source.name!r} exposes no registered solved results. "
            "There is no public result mapping to duplicate and verify."
        )
    if len(result_ids) != len(result_paths):
        raise RuntimeError(
            f"Analysis {source.name!r} has inconsistent public result metadata: "
            f"{len(result_ids)} simulation IDs and {len(result_paths)} paths. "
            "Run the analysis reuse diagnostic before duplicating it."
        )
    source_group = _valid_group_id(getattr(source, "simulationGroup", ""))
    source_group_text = str(getattr(source, "simulationGroupPath", "") or "").strip()
    if not source_group_text:
        raise RuntimeError(
            f"Analysis {source.name!r} has no simulationGroupPath. Run and save "
            "the analysis before duplicating its solved data."
        )
    source_group_path = Path(source_group_text)
    if not source_group_path.is_dir():
        raise FileNotFoundError(
            f"The source simulation-group directory does not exist: {source_group_path}"
        )
    outside = [path for path in result_paths if not path_is_within(path, source_group_path)]
    if outside:
        details = "\n  ".join(str(path) for path in outside)
        raise RuntimeError(
            "RFPro reports result paths outside the source simulation group; "
            f"a complete copy cannot be guaranteed:\n  {details}"
        )

    duplicate_group = _valid_group_id(project.simulations.getNextSimulationGroup())
    if duplicate_group == source_group:
        raise RuntimeError(
            "RFPro returned the source analysis's existing simulation-group ID "
            f"{source_group!r}; the duplicate was not created."
        )
    duplicate_group_path = source_group_path.parent / duplicate_group
    if duplicate_group_path.exists():
        raise FileExistsError(
            "RFPro's next simulation-group destination already exists. Nothing "
            f"was overwritten: {duplicate_group_path}"
        )
    size = directory_size(source_group_path)
    free = shutil.disk_usage(source_group_path.parent).free
    if size > free:
        raise OSError(
            f"The result copy needs {_format_bytes(size)}, but only "
            f"{_format_bytes(free)} is free beside {source_group_path}."
        )

    return DuplicatePlan(
        source_name=str(source.name),
        duplicate_name=duplicate_name,
        source_group=source_group,
        duplicate_group=duplicate_group,
        source_group_path=source_group_path,
        duplicate_group_path=duplicate_group_path,
        registered_result_ids=result_ids,
        registered_result_paths=result_paths,
        source_size_bytes=size,
    )


def _format_bytes(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024.0 or unit == "TiB":
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} TiB"


def copy_group_atomically(
    source: Path,
    destination: Path,
    copytree: Callable[..., Any] = shutil.copytree,
) -> None:
    """Copy to a private sibling, then publish the complete directory at once."""

    staging = destination.with_name(
        f".{destination.name}.rfpro-duplicate-{uuid.uuid4().hex}"
    )
    try:
        copytree(source, staging, copy_function=shutil.copy2, symlinks=True)
        os.replace(staging, destination)
    except Exception:
        if staging.is_dir():
            shutil.rmtree(staging)
        raise


def clone_analysis_for_plan(source: Any, plan: DuplicatePlan) -> Any:
    duplicate = source.clone()
    duplicate.name = plan.duplicate_name
    duplicate.simulationGroup = plan.duplicate_group
    duplicate.simulationPath = remap_group_path(
        str(getattr(source, "simulationPath", "") or ""),
        plan.source_group_path,
        plan.duplicate_group_path,
    )
    return duplicate


def verify_duplicate_output(
    empro_module: Any,
    duplicate: Any,
    plan: DuplicatePlan,
) -> tuple[str, ...]:
    actual_group = _valid_group_id(getattr(duplicate, "simulationGroup", ""))
    if actual_group != plan.duplicate_group:
        raise RuntimeError(
            f"Duplicate analysis group changed from {plan.duplicate_group!r} "
            f"to {actual_group!r}."
        )
    group_path_text = str(getattr(duplicate, "simulationGroupPath", "") or "").strip()
    if group_path_text and normalized_path(Path(group_path_text)) != normalized_path(
        plan.duplicate_group_path
    ):
        raise RuntimeError(
            "RFPro resolved the duplicate analysis to the wrong result group: "
            f"{group_path_text}; expected {plan.duplicate_group_path}."
        )

    output = empro_module.output.AnalysisOutput(duplicate)
    result_ids = tuple(str(value) for value in (output.getAvailableSimulationIds() or []))
    result_paths = tuple(
        Path(str(value)) for value in (output.getAvailableSimulationPaths() or [])
    )
    if sorted(result_ids) != sorted(plan.registered_result_ids):
        raise RuntimeError(
            "RFPro did not register the same solved-result IDs for the duplicate. "
            f"Source={list(plan.registered_result_ids)!r}; "
            f"duplicate={list(result_ids)!r}."
        )
    if len(result_paths) != len(plan.registered_result_paths):
        raise RuntimeError(
            "RFPro registered a different number of result paths for the "
            f"duplicate: source={len(plan.registered_result_paths)}, "
            f"duplicate={len(result_paths)}."
        )
    invalid_paths = [
        path
        for path in result_paths
        if not path_is_within(path, plan.duplicate_group_path) or not path.is_dir()
    ]
    if invalid_paths:
        details = "\n  ".join(str(path) for path in invalid_paths)
        raise RuntimeError(
            "RFPro's duplicate result paths do not resolve inside the copied "
            f"simulation group:\n  {details}"
        )
    return result_ids


def execute_duplicate_plan(
    empro_module: Any,
    project: Any,
    source: Any,
    plan: DuplicatePlan,
) -> DuplicateResult:
    """Copy and register a previously validated duplicate plan."""

    duplicate = clone_analysis_for_plan(source, plan)
    copy_group_atomically(plan.source_group_path, plan.duplicate_group_path)

    appended = False
    save_attempted = False
    try:
        with project:
            project.analyses.append(duplicate)
        appended = True
        project.simulations.refresh()
        verified_ids = verify_duplicate_output(empro_module, duplicate, plan)
        save_attempted = True
        project.saveActiveProject()
    except Exception as error:
        if not save_attempted:
            rollback_errors: list[str] = []
            if appended:
                try:
                    with project:
                        del project.analyses[project.analyses.index(plan.duplicate_name)]
                    project.simulations.refresh()
                except Exception as rollback_error:
                    rollback_errors.append(f"analysis rollback failed: {rollback_error}")
            if not rollback_errors:
                try:
                    shutil.rmtree(plan.duplicate_group_path)
                except Exception as rollback_error:
                    rollback_errors.append(f"result-directory rollback failed: {rollback_error}")
            if rollback_errors:
                raise RuntimeError(
                    f"Analysis duplication failed: {error}. "
                    + "; ".join(rollback_errors)
                    + f". Preserve and inspect {plan.duplicate_group_path}."
                ) from error
        raise RuntimeError(
            f"Analysis duplication failed: {error}. The source analysis was not "
            "modified. Because a project save was attempted, the copied result "
            f"directory was preserved at {plan.duplicate_group_path}."
        ) from error

    return DuplicateResult(duplicate, plan, verified_ids)


def duplicate_analysis_with_results(
    empro_module: Any,
    project: Any,
    source: Any,
    duplicate_name: str,
) -> DuplicateResult:
    """Perform a guarded, independently addressable analysis/result copy."""

    active = running_simulation_descriptions(project)
    if active:
        details = "\n  ".join(active)
        raise RuntimeError(
            "Wait for every RFPro simulation to finish before copying result "
            f"data. Active or queued simulations:\n  {details}"
        )

    # Persist the source analysis/result mapping before any filesystem copy.
    project.saveActiveProject()
    plan = prepare_duplicate_plan(empro_module, project, source, duplicate_name)
    return execute_duplicate_plan(empro_module, project, source, plan)


def execute_confirmed_duplicate_plan(
    empro_module: Any,
    project: Any,
    source: Any,
    plan: DuplicatePlan,
) -> DuplicateResult:
    """Save the source mapping, then execute the plan shown to the user."""

    active = running_simulation_descriptions(project)
    if active:
        details = "\n  ".join(active)
        raise RuntimeError(
            "Wait for every RFPro simulation to finish before copying result "
            f"data. Active or queued simulations:\n  {details}"
        )
    validate_duplicate_name(plan.duplicate_name, analysis_names(project))
    current_group = _valid_group_id(getattr(source, "simulationGroup", ""))
    current_group_path = Path(
        str(getattr(source, "simulationGroupPath", "") or "")
    )
    if current_group != plan.source_group or normalized_path(
        current_group_path
    ) != normalized_path(plan.source_group_path):
        raise RuntimeError(
            "The source analysis result group changed after the confirmation "
            "preview. Run the duplicate operation again."
        )
    if plan.duplicate_group_path.exists():
        raise FileExistsError(
            "The confirmed destination appeared before copying. Nothing was "
            f"overwritten: {plan.duplicate_group_path}"
        )
    project.saveActiveProject()
    return execute_duplicate_plan(empro_module, project, source, plan)


def build_confirmation(plan: DuplicatePlan) -> str:
    return "\n".join(
        (
            f"Source analysis: {plan.source_name}",
            f"New analysis: {plan.duplicate_name}",
            f"Source result group: {plan.source_group_path}",
            f"New independent result group: {plan.duplicate_group_path}",
            f"Registered solved points: {len(plan.registered_result_ids)}",
            f"Data to copy: {_format_bytes(plan.source_size_bytes)}",
            "",
            "The entire result group will be copied. No simulation will be started,",
            "and the source analysis and its result files will not be modified.",
        )
    )


def _choose_duplicate_name(
    project: Any, source: Any, requested: str
) -> str | None:
    names = analysis_names(project)
    if requested:
        return validate_duplicate_name(requested, names)
    from PySide6.QtWidgets import QInputDialog

    suggested = default_duplicate_name(str(source.name), names)
    selected, accepted = QInputDialog.getText(
        None,
        "Duplicate RFPro analysis and results",
        "New analysis name:",
        text=suggested,
    )
    if not accepted:
        return None
    return validate_duplicate_name(str(selected), names)


def _confirm(plan: DuplicatePlan) -> bool:
    from PySide6.QtWidgets import QMessageBox

    return (
        QMessageBox.question(
            None,
            "Duplicate RFPro analysis and solved data?",
            build_confirmation(plan),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        == QMessageBox.StandardButton.Yes
    )


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Duplicate an RFPro analysis and its saved result group."
    )
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS_NAME)
    parser.add_argument("--new-name", default=DEFAULT_DUPLICATE_NAME)
    parser.add_argument("--yes", action="store_true", help="copy without confirmation")
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    return arguments


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    qt_runtime = create_or_reuse_qapplication()
    _print_qt_diagnostics(qt_runtime)

    import empro

    project = empro.activeProject
    source = find_analysis(project, arguments.analysis)
    duplicate_name = _choose_duplicate_name(project, source, arguments.new_name)
    if duplicate_name is None:
        print("Analysis duplication cancelled; no files or analyses were changed.")
        return

    active = running_simulation_descriptions(project)
    if active:
        details = "\n  ".join(active)
        raise RuntimeError(
            "Wait for every RFPro simulation to finish before duplicating an "
            f"analysis and its results:\n  {details}"
        )
    plan = prepare_duplicate_plan(empro, project, source, duplicate_name)
    preview = build_confirmation(plan)
    print(preview)
    if not arguments.yes and not _confirm(plan):
        print("Analysis duplication cancelled; no files or analyses were changed.")
        return

    result = execute_confirmed_duplicate_plan(
        empro,
        project,
        source,
        plan,
    )
    summary = (
        f"Created analysis {result.plan.duplicate_name!r} with independent "
        f"simulation group {result.plan.duplicate_group!r} and verified "
        f"{len(result.verified_result_ids)} solved result(s). No simulation was started."
    )
    print(summary)
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.information(None, "RFPro Analysis Duplicated", summary)


if __name__ == "__main__":
    main()
