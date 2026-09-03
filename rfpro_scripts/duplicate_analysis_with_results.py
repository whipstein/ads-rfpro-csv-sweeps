"""Duplicate an RFPro analysis and its complete saved simulation-result group.

Run this script inside RFPro. It deep-clones the selected Analysis, lets RFPro
create the new simulation group and inactive target records, atomically copies
each solved source point into the corresponding registered target path,
refreshes the output result browser, and verifies its public AnalysisOutput
paths. It never queues or starts a simulation.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable, Sequence


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_DUPLICATE_NAME = ""
DEFAULT_RESUME_GROUP_ID = ""
DEFAULT_REGISTRATION_TIMEOUT_SECONDS = 300.0
REGISTRATION_POLL_INTERVAL_SECONDS = 0.1


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
    target_result_paths: tuple[Path, ...] = ()
    transplant_source_results: bool = False
    redundant_copied_group_path: Path | None = None


@dataclass(frozen=True)
class DuplicateResult:
    duplicate: Any
    plan: DuplicatePlan
    verified_result_ids: tuple[str, ...]


@dataclass(frozen=True)
class SourceResultInventory:
    result_ids: tuple[str, ...]
    result_paths: tuple[Path, ...]
    group: str
    group_path: Path
    size_bytes: int


class AmbiguousResumeGroupsError(RuntimeError):
    def __init__(self, message: str, candidates: Sequence[Path]) -> None:
        super().__init__(message)
        self.candidates = tuple(candidates)


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


def active_simulation_descriptions(simulations: Sequence[Any]) -> list[str]:
    """Describe simulation records that are running or waiting to run."""

    active: list[str] = []
    active_status_prefixes = (
        "queue",
        "pending",
        "submit",
        "start",
        "running",
        "solving",
        "preprocess",
        "meshing",
        "postprocess",
        "interrupt",
        "killing",
    )
    for index, simulation in enumerate(simulations):
        is_running = bool(_call_or_value(getattr(simulation, "isRunning", None), False))
        has_running_status = bool(
            _call_or_value(getattr(simulation, "hasRunningStatus", None), False)
        )
        status = str(_call_or_value(getattr(simulation, "status", None), "") or "")
        status_key = (
            status.casefold().replace(" ", "").replace("_", "").rsplit(".", 1)[-1]
        )
        status_is_active = any(
            status_key.startswith(prefix) for prefix in active_status_prefixes
        )
        if not (is_running or has_running_status or status_is_active):
            continue
        name = str(getattr(simulation, "name", "") or f"simulation {index + 1}")
        path = str(_call_or_value(getattr(simulation, "simulationPath", None), "") or "")
        active.append(f"{name} (status={status or 'active'}, path={path or 'unknown'})")
    return active


def running_simulation_descriptions(project: Any) -> list[str]:
    """Return public simulation entries that are running or waiting to run."""

    return active_simulation_descriptions(list(project.simulations))


def normalized_path(path: Path) -> str:
    return os.path.normcase(os.path.abspath(str(path)))


def path_is_within(path: Path, root: Path) -> bool:
    try:
        return os.path.commonpath((normalized_path(path), normalized_path(root))) == normalized_path(root)
    except ValueError:
        return False


def resolve_result_path(path: Path, group_path: Path) -> Path:
    """Resolve RFPro's absolute or group-relative result-path representation."""

    if path.is_absolute():
        return path
    normalized = Path(os.path.normpath(str(path)))
    # RFPro can report either ./<group>/<simulation> relative to the RFPro
    # results root, or ./<simulation> relative to simulationGroupPath.
    if len(normalized.parts) > 1 and normalized.parts[0] == group_path.name:
        return group_path.parent / normalized
    return group_path / normalized


def reported_group_path_matches(
    reported_text: str,
    expected_path: Path,
    expected_group: str,
) -> bool:
    """Accept RFPro's absolute path or its canonical ./<group> spelling."""

    text = str(reported_text or "").strip()
    if not text:
        return False
    reported = Path(text)
    if reported.is_absolute():
        return normalized_path(reported) == normalized_path(expected_path)
    return os.path.normpath(text) == expected_group


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


def _optional_group_id(group: Any) -> str | None:
    """Return a safe group ID, or None when RFPro exposes no usable value."""

    text = str(group or "").strip()
    if not text or text in {".", ".."} or Path(text).name != text:
        return None
    return text


def _source_relative_result_paths(
    inventory: SourceResultInventory,
) -> tuple[Path, ...]:
    return tuple(
        Path(os.path.relpath(path, inventory.group_path))
        for path in inventory.result_paths
    )


def _complete_resume_group_candidate(
    path: Path,
    inventory: SourceResultInventory,
) -> bool:
    """Require a sibling group containing every copied source-result path."""

    if normalized_path(path.parent) != normalized_path(inventory.group_path.parent):
        return False
    if normalized_path(path) == normalized_path(inventory.group_path):
        return False
    if not path.is_dir():
        return False
    return all(
        (path / relative_path).is_dir()
        for relative_path in _source_relative_result_paths(inventory)
    )


def _analysis_owned_group_ids(project: Any, excluded_name: str) -> set[str]:
    owned: set[str] = set()
    for name in analysis_names(project):
        if name == excluded_name:
            continue
        analysis = project.analyses[project.analyses.index(name)]
        group = _optional_group_id(getattr(analysis, "simulationGroup", ""))
        if group is not None:
            owned.add(group)
    return owned


def _record_group_candidates(
    project: Any,
    inventory: SourceResultInventory,
) -> set[Path]:
    """Infer result-group roots from public Simulation.group/path values."""

    root = inventory.group_path.parent
    relatives = _source_relative_result_paths(inventory)
    candidates: set[Path] = set()
    for simulation in project.simulations:
        group = _optional_group_id(
            _call_or_value(getattr(simulation, "group", None), "")
        )
        if group is not None:
            candidates.add(root / group)

        path_text = str(
            _call_or_value(getattr(simulation, "simulationPath", None), "") or ""
        ).strip()
        if not path_text:
            continue
        reported = Path(path_text)
        if reported.is_absolute():
            for relative in relatives:
                candidate = reported
                for _part in relative.parts:
                    candidate = candidate.parent
                if normalized_path(candidate / relative) == normalized_path(reported):
                    candidates.add(candidate)
        else:
            parts = Path(os.path.normpath(path_text)).parts
            for relative in relatives:
                count = len(relative.parts)
                if len(parts) != count + 1 or tuple(parts[-count:]) != relative.parts:
                    continue
                candidates.add(root / parts[0])
    return {
        path
        for path in candidates
        if _optional_group_id(path.name) is not None
        and _complete_resume_group_candidate(path, inventory)
    }


def _simulation_record_group_and_path(
    simulation: Any,
    results_root: Path,
) -> tuple[Path, Path] | None:
    """Resolve one public Simulation record to its sibling group and path."""

    group = _optional_group_id(
        _call_or_value(getattr(simulation, "group", None), "")
    )
    path_text = str(
        _call_or_value(getattr(simulation, "simulationPath", None), "") or ""
    ).strip()
    if not path_text:
        return None
    reported = Path(path_text)
    if reported.is_absolute():
        simulation_path = reported
        if group is not None:
            group_path = results_root / group
        else:
            try:
                relative = Path(os.path.relpath(simulation_path, results_root))
            except ValueError:
                return None
            if len(relative.parts) < 2:
                return None
            group_path = results_root / relative.parts[0]
    else:
        normalized = Path(os.path.normpath(path_text))
        if group is not None:
            group_path = results_root / group
            simulation_path = (
                results_root / normalized
                if normalized.parts and normalized.parts[0] == group
                else group_path / normalized
            )
        elif len(normalized.parts) >= 2:
            group_path = results_root / normalized.parts[0]
            simulation_path = results_root / normalized
        else:
            return None
    if normalized_path(group_path.parent) != normalized_path(results_root):
        return None
    if not path_is_within(simulation_path, group_path):
        return None
    return group_path, simulation_path


def registered_resume_group_candidates(
    project: Any,
    inventory: SourceResultInventory,
    duplicate_name: str,
) -> dict[Path, tuple[tuple[Any, ...], tuple[Path, ...]]]:
    """Find complete inactive Created-record groups not owned by another analysis."""

    owned = _analysis_owned_group_ids(project, duplicate_name)
    grouped: dict[Path, list[tuple[Any, Path]]] = {}
    for simulation in project.simulations:
        resolved = _simulation_record_group_and_path(
            simulation,
            inventory.group_path.parent,
        )
        if resolved is None:
            continue
        group_path, simulation_path = resolved
        if group_path.name == inventory.group or group_path.name in owned:
            continue
        grouped.setdefault(group_path, []).append((simulation, simulation_path))

    expected_count = len(inventory.result_paths)
    candidates: dict[Path, tuple[tuple[Any, ...], tuple[Path, ...]]] = {}
    for group_path, entries in grouped.items():
        records = tuple(record for record, _path in entries)
        paths = tuple(path for _record, path in entries)
        if len(paths) != expected_count or len(set(map(normalized_path, paths))) != len(
            paths
        ):
            continue
        if active_simulation_descriptions(records):
            continue
        if not all(path.is_dir() for path in paths):
            continue
        candidates[group_path] = records, paths
    return candidates


def _analysis_output_matches_paths(
    empro_module: Any,
    analysis: Any,
    group_path: Path,
    expected_paths: Sequence[Path],
) -> bool:
    try:
        output = empro_module.output.AnalysisOutput(analysis)
        ids = tuple(str(value) for value in (output.getAvailableSimulationIds() or []))
        raw_paths = tuple(
            Path(str(value)) for value in (output.getAvailableSimulationPaths() or [])
        )
        paths = tuple(resolve_result_path(path, group_path) for path in raw_paths)
    except Exception:
        return False
    return len(ids) == len(expected_paths) and sorted(
        map(normalized_path, paths)
    ) == sorted(map(normalized_path, expected_paths))


def recover_resume_group(
    project: Any,
    duplicate: Any,
    inventory: SourceResultInventory,
    requested_group: str = "",
) -> tuple[str, Path]:
    """Resolve an incomplete duplicate's copied group without guessing."""

    root = inventory.group_path.parent
    duplicate_name = str(duplicate.name)
    requested = str(requested_group or "").strip()
    current = _optional_group_id(getattr(duplicate, "simulationGroup", ""))
    if requested:
        requested = _valid_group_id(requested)
        if current is not None and current != requested:
            raise RuntimeError(
                f"Existing analysis {duplicate_name!r} is already associated with "
                f"group {current!r}, not requested resume group {requested!r}."
            )
        candidate = root / requested
        if not _complete_resume_group_candidate(candidate, inventory):
            raise RuntimeError(
                f"Requested resume group {requested!r} does not contain every "
                f"copied source-result directory: {candidate}"
            )
        return requested, candidate

    group_path_text = str(
        getattr(duplicate, "simulationGroupPath", "") or ""
    ).strip()
    metadata_path: Path | None = None
    if group_path_text:
        reported = Path(group_path_text)
        if reported.is_absolute():
            candidate = reported
        else:
            normalized = Path(os.path.normpath(group_path_text))
            candidate = root / normalized if len(normalized.parts) == 1 else Path()
        if (
            candidate != Path()
            and _optional_group_id(candidate.name) is not None
            and _complete_resume_group_candidate(candidate, inventory)
        ):
            metadata_path = candidate

    if current is not None:
        candidate = root / current
        if metadata_path is not None and normalized_path(metadata_path) != normalized_path(
            candidate
        ):
            raise RuntimeError(
                f"Existing analysis {duplicate_name!r} reports conflicting result "
                f"metadata: simulationGroup={current!r}, "
                f"simulationGroupPath={group_path_text!r}."
            )
        if not _complete_resume_group_candidate(candidate, inventory):
            raise RuntimeError(
                f"Existing analysis {duplicate_name!r} points to incomplete or "
                f"missing copied result group {candidate}."
            )
        return current, candidate
    if metadata_path is not None:
        return metadata_path.name, metadata_path

    owned = _analysis_owned_group_ids(project, duplicate_name)
    record_candidates = {
        path
        for path in _record_group_candidates(project, inventory)
        if path.name not in owned
    }
    if len(record_candidates) == 1:
        candidate = next(iter(record_candidates))
        return candidate.name, candidate
    if len(record_candidates) > 1:
        candidates = tuple(sorted(record_candidates, key=lambda path: str(path)))
        raise AmbiguousResumeGroupsError(
            f"Existing analysis {duplicate_name!r} has an empty simulationGroup, "
            "and multiple Created-record groups match its copied results: "
            f"{[str(path) for path in candidates]!r}.",
            candidates,
        )

    filesystem_candidates = {
        path
        for path in root.iterdir()
        if path.name.isdigit()
        and path.name not in owned
        and _complete_resume_group_candidate(path, inventory)
    }
    if len(filesystem_candidates) == 1:
        candidate = next(iter(filesystem_candidates))
        return candidate.name, candidate
    candidates = tuple(sorted(filesystem_candidates, key=lambda path: str(path)))
    if candidates:
        raise AmbiguousResumeGroupsError(
            f"Existing analysis {duplicate_name!r} has an empty simulationGroup, "
            "and multiple unassigned copied groups match: "
            f"{[str(path) for path in candidates]!r}.",
            candidates,
        )
    raise RuntimeError(
        f"Existing analysis {duplicate_name!r} has an empty simulationGroup, and "
        "no unassigned sibling group contains every expected result directory."
    )


def source_result_inventory(
    empro_module: Any,
    source: Any,
) -> SourceResultInventory:
    """Read and validate the source analysis's complete public result mapping."""

    output = empro_module.output.AnalysisOutput(source)
    result_ids = tuple(str(value) for value in (output.getAvailableSimulationIds() or []))
    raw_result_paths = tuple(
        Path(str(value)) for value in (output.getAvailableSimulationPaths() or [])
    )
    if not result_ids:
        raise RuntimeError(
            f"Analysis {source.name!r} exposes no registered solved results. "
            "There is no public result mapping to duplicate and verify."
        )
    if len(result_ids) != len(raw_result_paths):
        raise RuntimeError(
            f"Analysis {source.name!r} has inconsistent public result metadata: "
            f"{len(result_ids)} simulation IDs and {len(raw_result_paths)} paths. "
            "Run the analysis reuse diagnostic before duplicating it."
        )
    source_group_text = str(getattr(source, "simulationGroup", "") or "").strip()
    source_group = _optional_group_id(source_group_text)
    if source_group is None:
        raise RuntimeError(
            f"Source analysis {source.name!r} has an empty or invalid "
            f"simulationGroup ({source_group_text!r}). When resuming a preserved "
            "copy, select the original solved analysis as the source, then enter "
            "the incomplete duplicate's exact name in the next dialog."
        )
    source_group_path_text = str(
        getattr(source, "simulationGroupPath", "") or ""
    ).strip()
    if not source_group_path_text:
        raise RuntimeError(
            f"Analysis {source.name!r} has no simulationGroupPath. Run and save "
            "the analysis before duplicating its solved data."
        )
    source_group_path = Path(source_group_path_text)
    if not source_group_path.is_dir():
        raise FileNotFoundError(
            f"The source simulation-group directory does not exist: {source_group_path}"
        )
    result_paths = tuple(
        resolve_result_path(path, source_group_path) for path in raw_result_paths
    )
    outside = [path for path in result_paths if not path_is_within(path, source_group_path)]
    if outside:
        details = "\n  ".join(str(path) for path in outside)
        raise RuntimeError(
            "RFPro reports result paths outside the source simulation group; "
            f"a complete copy cannot be guaranteed:\n  {details}"
        )
    return SourceResultInventory(
        result_ids=result_ids,
        result_paths=result_paths,
        group=source_group,
        group_path=source_group_path,
        size_bytes=directory_size(source_group_path),
    )


def prepare_duplicate_plan(
    empro_module: Any,
    project: Any,
    source: Any,
    duplicate_name: str,
) -> DuplicatePlan:
    duplicate_name = validate_duplicate_name(duplicate_name, analysis_names(project))
    inventory = source_result_inventory(empro_module, source)

    duplicate_group = _valid_group_id(project.simulations.getNextSimulationGroup())
    if duplicate_group == inventory.group:
        raise RuntimeError(
            "RFPro returned the source analysis's existing simulation-group ID "
            f"{inventory.group!r}; the duplicate was not created."
        )
    duplicate_group_path = inventory.group_path.parent / duplicate_group
    if duplicate_group_path.exists():
        raise FileExistsError(
            "RFPro's next simulation-group destination already exists. Nothing "
            f"was overwritten: {duplicate_group_path}"
        )
    free = shutil.disk_usage(inventory.group_path.parent).free
    if inventory.size_bytes > free:
        raise OSError(
            f"The result copy needs {_format_bytes(inventory.size_bytes)}, but only "
            f"{_format_bytes(free)} is free beside {inventory.group_path}."
        )

    return DuplicatePlan(
        source_name=str(source.name),
        duplicate_name=duplicate_name,
        source_group=inventory.group,
        duplicate_group=duplicate_group,
        source_group_path=inventory.group_path,
        duplicate_group_path=duplicate_group_path,
        registered_result_ids=inventory.result_ids,
        registered_result_paths=inventory.result_paths,
        source_size_bytes=inventory.size_bytes,
    )


def prepare_resume_plan(
    empro_module: Any,
    project: Any,
    source: Any,
    duplicate_name: str,
    resume_group: str = "",
) -> tuple[Any, DuplicatePlan]:
    """Validate an existing preserved duplicate for refresh-only resumption."""

    name = str(duplicate_name).strip()
    names = analysis_names(project)
    if name == str(source.name):
        raise ValueError("The source analysis cannot resume itself as a duplicate.")
    if name not in names:
        raise ValueError(f"Existing duplicate analysis {name!r} was not found.")
    duplicate = project.analyses[project.analyses.index(name)]
    inventory = source_result_inventory(empro_module, source)

    # A failed older duplication can leave the full copied data in one group
    # while RFPro's backend registers its inactive Created records in another.
    # Refresh first and prefer the record-owning group as the final target.
    for _attempt in range(3):
        process_rfpro_events(empro_module)
        try:
            refresh_simulation_table(project)
        except Exception:
            time.sleep(REGISTRATION_POLL_INTERVAL_SECONDS)
        else:
            break
    registered_groups = registered_resume_group_candidates(
        project,
        inventory,
        name,
    )
    resume_group_text = str(resume_group or "").strip()
    requested = _optional_group_id(resume_group_text)
    if resume_group_text and requested is None:
        _valid_group_id(resume_group_text)
    registered_group_path: Path | None = None
    if requested is not None:
        requested_path = inventory.group_path.parent / requested
        if requested_path in registered_groups:
            registered_group_path = requested_path
    elif len(registered_groups) == 1:
        registered_group_path = next(iter(registered_groups))
    elif len(registered_groups) > 1:
        candidates = tuple(sorted(registered_groups, key=lambda path: str(path)))
        raise AmbiguousResumeGroupsError(
            f"Existing analysis {name!r} has Created records in multiple "
            f"unowned groups: {[str(path) for path in candidates]!r}.",
            candidates,
        )

    if registered_group_path is not None:
        _records, target_paths = registered_groups[registered_group_path]
        current = _optional_group_id(getattr(duplicate, "simulationGroup", ""))
        redundant_path = None
        if current is not None and current != registered_group_path.name:
            possible = inventory.group_path.parent / current
            if possible.is_dir():
                redundant_path = possible
        plan = DuplicatePlan(
            source_name=str(source.name),
            duplicate_name=name,
            source_group=inventory.group,
            duplicate_group=registered_group_path.name,
            source_group_path=inventory.group_path,
            duplicate_group_path=registered_group_path,
            registered_result_ids=inventory.result_ids,
            registered_result_paths=inventory.result_paths,
            source_size_bytes=inventory.size_bytes,
            target_result_paths=target_paths,
            transplant_source_results=(
                current != registered_group_path.name
                or not _analysis_output_matches_paths(
                    empro_module,
                    duplicate,
                    registered_group_path,
                    target_paths,
                )
            ),
            redundant_copied_group_path=redundant_path,
        )
        return duplicate, plan

    duplicate_group, duplicate_group_path = recover_resume_group(
        project,
        duplicate,
        inventory,
        resume_group,
    )
    if duplicate_group == inventory.group:
        raise RuntimeError(
            "The existing analysis shares the source simulation group and is "
            "not an independent preserved duplicate."
        )

    plan = DuplicatePlan(
        source_name=str(source.name),
        duplicate_name=name,
        source_group=inventory.group,
        duplicate_group=duplicate_group,
        source_group_path=inventory.group_path,
        duplicate_group_path=duplicate_group_path,
        registered_result_ids=inventory.result_ids,
        registered_result_paths=inventory.result_paths,
        source_size_bytes=directory_size(duplicate_group_path),
    )
    missing = [path for path in remapped_result_paths(plan) if not path.is_dir()]
    if missing:
        details = "\n  ".join(str(path) for path in missing)
        raise RuntimeError(
            "The preserved duplicate is missing copied result directories:\n  "
            + details
        )
    return duplicate, plan


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
    # Do not assign Analysis.simulationPath. Its setter is deprecated in RFPro;
    # the new simulationGroup and copied group directory are authoritative.
    return duplicate


def remapped_result_paths(plan: DuplicatePlan) -> tuple[Path, ...]:
    """Map every source result path to the same location in the copied group."""

    return tuple(
        plan.duplicate_group_path
        / Path(os.path.relpath(path, plan.source_group_path))
        for path in plan.registered_result_paths
    )


def expected_target_result_paths(plan: DuplicatePlan) -> tuple[Path, ...]:
    return plan.target_result_paths or remapped_result_paths(plan)


def begin_simulation_creation_lifecycle(project: Any) -> Callable[[], Any]:
    """Enter the modified-state guard used by RFPro's shipped runAnalysis."""

    cache = getattr(project, "_cacheProjectModifiedBeforeRunAnalysis", None)
    invalidate = getattr(project, "_invalidateProjectModifiedBeforeRunAnalysis", None)
    if not callable(cache) or not callable(invalidate):
        raise RuntimeError(
            "This RFPro runtime does not expose the project modified-state "
            "lifecycle required for nonqueued result registration."
        )
    cache()
    return invalidate


def register_duplicate_results(
    project: Any,
    duplicate: Any,
    plan: DuplicatePlan,
) -> tuple[Any, ...]:
    """Ask RFPro to create empty target records without queueing a solve.

    RFPro's shipped workflows use the first ``False`` argument when records
    must be created before a later, explicit ``setQueued(True)`` call.  This
    operation intentionally performs only that nonqueued creation step.
    """

    try:
        simulations = project.createSimulationsFromAnalysis(
            False,
            False,
            [],
            duplicate,
            {},
            {},
        )
    except Exception as error:
        raise RuntimeError(
            "RFPro could not create nonqueued result associations for the "
            f"duplicate analysis: {error}"
        ) from error

    # RFPro must own creation of the target group and paths. Supplying already
    # copied paths can make its backend allocate a second group, separating the
    # analysis records from the solved data. An empty existing-path list creates
    # inactive targets for the cloned sweep; solved data is copied into those
    # registered paths only after creation completes.
    return tuple(simulations or ())


def verify_nonqueued_registration(
    registered: Sequence[Any],
    plan: DuplicatePlan,
) -> None:
    """Require the returned records to be inactive and point at the copy."""

    expected_paths = expected_target_result_paths(plan)
    active = active_simulation_descriptions(registered)
    if active:
        details = "\n  ".join(active)
        raise RuntimeError(
            "RFPro unexpectedly queued or started a copied-result record even "
            f"though addToQueue was False:\n  {details}"
        )

    registered_paths: list[Path] = []
    for simulation in registered:
        path_text = str(
            _call_or_value(getattr(simulation, "simulationPath", None), "") or ""
        ).strip()
        if not path_text:
            raise RuntimeError(
                "RFPro returned a nonqueued simulation record without a "
                "simulation path."
            )
        registered_paths.append(
            resolve_result_path(Path(path_text), plan.duplicate_group_path)
        )

    expected_normalized = sorted(normalized_path(path) for path in expected_paths)
    registered_normalized = sorted(normalized_path(path) for path in registered_paths)
    if registered_normalized != expected_normalized:
        raise RuntimeError(
            "RFPro associated different paths than the copied results. "
            f"Expected={[str(path) for path in expected_paths]!r}; "
            f"registered={[str(path) for path in registered_paths]!r}."
        )


def copied_result_records(
    project: Any,
    plan: DuplicatePlan,
) -> tuple[tuple[Any, ...], tuple[Path, ...]]:
    """Return records in the copied group and their resolved paths."""

    records: list[Any] = []
    paths: list[Path] = []
    for simulation in project.simulations:
        text = str(
            _call_or_value(getattr(simulation, "simulationPath", None), "") or ""
        ).strip()
        if not text:
            continue
        path = resolve_result_path(Path(text), plan.duplicate_group_path)
        if path_is_within(path, plan.duplicate_group_path):
            records.append(simulation)
            paths.append(path)
    return tuple(records), tuple(paths)


def process_rfpro_events(empro_module: Any) -> None:
    """Allow RFPro's asynchronous simulation-table updates to be delivered."""

    callback = getattr(getattr(empro_module, "gui", None), "processEvents", None)
    if callable(callback):
        callback()


def refresh_simulation_table(project: Any) -> None:
    """Reload RFPro's Python simulation-list wrapper from its native table."""

    callback = getattr(project.simulations, "refresh", None)
    if not callable(callback):
        raise RuntimeError("RFPro's SimulationList exposes no refresh() method.")
    callback()


def ensure_duplicate_group_binding(
    project: Any,
    duplicate: Any,
    plan: DuplicatePlan,
) -> bool:
    """Restore a missing group assignment on RFPro's registered analysis object."""

    current_text = str(getattr(duplicate, "simulationGroup", "") or "").strip()
    current = _optional_group_id(current_text)
    if current == plan.duplicate_group:
        return False
    recoverable_split = (
        plan.transplant_source_results
        and plan.redundant_copied_group_path is not None
        and current == plan.redundant_copied_group_path.name
    )
    if current_text and not recoverable_split:
        raise RuntimeError(
            f"Duplicate analysis {plan.duplicate_name!r} changed to unexpected "
            f"simulation group {current_text!r}; expected {plan.duplicate_group!r}."
        )
    with project:
        duplicate.simulationGroup = plan.duplicate_group
    restored = _optional_group_id(getattr(duplicate, "simulationGroup", ""))
    if restored != plan.duplicate_group:
        raise RuntimeError(
            f"RFPro did not retain the recovered simulation-group assignment "
            f"{plan.duplicate_group!r} on analysis {plan.duplicate_name!r}."
        )
    return True


def wait_for_created_target_records(
    empro_module: Any,
    project: Any,
    plan: DuplicatePlan,
    returned_records: Sequence[Any],
    timeout_seconds: float = DEFAULT_REGISTRATION_TIMEOUT_SECONDS,
) -> tuple[tuple[Any, ...], tuple[Path, ...], Path]:
    """Wait until RFPro publishes every inactive target path it created."""

    timeout = max(0.0, float(timeout_seconds))
    deadline = time.monotonic() + timeout
    expected_count = len(plan.registered_result_paths)
    last_detail = "RFPro has not exposed any target records yet."
    returned_active = active_simulation_descriptions(returned_records)
    if returned_active:
        details = "\n  ".join(returned_active)
        raise RuntimeError(
            "RFPro unexpectedly queued or started a new duplicate record even "
            f"though addToQueue was False:\n  {details}"
        )

    while True:
        process_rfpro_events(empro_module)
        refresh_error = ""
        try:
            refresh_simulation_table(project)
        except Exception as error:
            refresh_error = str(error)
        try:
            records, paths = copied_result_records(project, plan)
        except Exception as error:
            last_detail = f"simulation-table inspection failed: {error}"
        else:
            active = active_simulation_descriptions(records)
            if active:
                details = "\n  ".join(active)
                raise RuntimeError(
                    "RFPro unexpectedly queued or started a new duplicate "
                    f"record:\n  {details}"
                )
            unique_paths = {normalized_path(path) for path in paths}
            if (
                len(records) == expected_count
                and len(paths) == expected_count
                and len(unique_paths) == expected_count
                and all(path.is_dir() for path in paths)
            ):
                return records, paths, plan.duplicate_group_path
            if not records:
                inventory = SourceResultInventory(
                    result_ids=plan.registered_result_ids,
                    result_paths=plan.registered_result_paths,
                    group=plan.source_group,
                    group_path=plan.source_group_path,
                    size_bytes=plan.source_size_bytes,
                )
                alternate_groups = registered_resume_group_candidates(
                    project,
                    inventory,
                    plan.duplicate_name,
                )
                if len(alternate_groups) == 1:
                    group_path, (alternate_records, alternate_paths) = next(
                        iter(alternate_groups.items())
                    )
                    return alternate_records, alternate_paths, group_path
            last_detail = (
                f"expected {expected_count} inactive target records in "
                f"{plan.duplicate_group_path}; observed paths="
                f"{[str(path) for path in paths]!r}"
            )
        if refresh_error:
            last_detail += "; latest SimulationList.refresh() error: " + refresh_error
        if time.monotonic() >= deadline:
            raise RuntimeError(
                "Timed out waiting for RFPro to create the duplicate's inactive "
                "target records. " + last_detail
            )
        time.sleep(REGISTRATION_POLL_INTERVAL_SECONDS)


def refresh_result_browser(empro_module: Any) -> None:
    """Reload saved output data after the result associations are created."""

    try:
        browser = empro_module.output.resultBrowser()
        browser.refresh()
    except Exception as error:
        raise RuntimeError(
            "RFPro could not refresh its output result browser after copying "
            f"the result group: {error}"
        ) from error


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
    if not reported_group_path_matches(
        group_path_text,
        plan.duplicate_group_path,
        plan.duplicate_group,
    ):
        raise RuntimeError(
            "RFPro resolved the duplicate analysis to the wrong result group: "
            f"{group_path_text}; expected {plan.duplicate_group_path}."
        )

    output = empro_module.output.AnalysisOutput(duplicate)
    result_ids = tuple(str(value) for value in (output.getAvailableSimulationIds() or []))
    raw_result_paths = tuple(
        Path(str(value)) for value in (output.getAvailableSimulationPaths() or [])
    )
    expected_paths = expected_target_result_paths(plan)
    if len(result_ids) != len(expected_paths):
        raise RuntimeError(
            "RFPro did not expose the expected number of solved results for the "
            f"duplicate. Expected={len(expected_paths)}; "
            f"duplicate IDs={list(result_ids)!r}."
        )
    if len(raw_result_paths) != len(expected_paths):
        raise RuntimeError(
            "RFPro exposed a different number of result paths for the "
            f"duplicate: expected={len(expected_paths)}, "
            f"duplicate={len(raw_result_paths)}."
        )
    result_paths = tuple(
        resolve_result_path(path, plan.duplicate_group_path)
        for path in raw_result_paths
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
    if sorted(map(normalized_path, result_paths)) != sorted(
        map(normalized_path, expected_paths)
    ):
        raise RuntimeError(
            "RFPro exposed different duplicate result paths than its Created "
            f"records. Expected={[str(path) for path in expected_paths]!r}; "
            f"observed={[str(path) for path in result_paths]!r}."
        )
    return result_ids


def wait_for_duplicate_registration(
    empro_module: Any,
    project: Any,
    duplicate: Any,
    plan: DuplicatePlan,
    returned_records: Sequence[Any],
    timeout_seconds: float = DEFAULT_REGISTRATION_TIMEOUT_SECONDS,
) -> tuple[tuple[Any, ...], tuple[str, ...]]:
    """Wait for asynchronous Created records and their output association."""

    timeout = max(0.0, float(timeout_seconds))
    deadline = time.monotonic() + timeout
    expected_paths = expected_target_result_paths(plan)
    expected_normalized = sorted(normalized_path(path) for path in expected_paths)
    last_detail = "RFPro has not exposed any copied-group records yet."
    records_saved = False

    returned_active = active_simulation_descriptions(returned_records)
    if returned_active:
        details = "\n  ".join(returned_active)
        raise RuntimeError(
            "RFPro unexpectedly queued or started a returned copied-result "
            f"record even though addToQueue was False:\n  {details}"
        )

    while True:
        process_rfpro_events(empro_module)
        simulation_refresh_error = ""
        try:
            refresh_simulation_table(project)
        except Exception as error:
            # The native table can be transiently inconsistent while its
            # asynchronous creator publishes multiple records. Keep pumping
            # events and retry instead of treating that intermediate mismatch
            # as corruption or deleting the owning analysis.
            simulation_refresh_error = str(error)
        try:
            records, record_paths = copied_result_records(project, plan)
        except Exception as error:
            last_detail = f"simulation-table inspection failed: {error}"
            if simulation_refresh_error:
                last_detail += (
                    "; latest SimulationList.refresh() error: "
                    + simulation_refresh_error
                )
        else:
            active = active_simulation_descriptions(records)
            if active:
                details = "\n  ".join(active)
                raise RuntimeError(
                    "RFPro unexpectedly queued or started a copied-result "
                    f"record even though addToQueue was False:\n  {details}"
                )

            observed_normalized = sorted(
                normalized_path(path) for path in record_paths
            )
            if observed_normalized == expected_normalized:
                verify_nonqueued_registration(records, plan)
                binding_restored = ensure_duplicate_group_binding(
                    project,
                    duplicate,
                    plan,
                )
                if not records_saved or binding_restored:
                    # Persist the asynchronously created records before asking
                    # the output layer to associate them with the duplicate.
                    # RFPro can clear a clone's group while publishing those
                    # records, so reassert it on the registered analysis first.
                    project.saveActiveProject()
                    records_saved = True
                try:
                    refresh_result_browser(empro_module)
                    result_ids = verify_duplicate_output(
                        empro_module, duplicate, plan
                    )
                except Exception as error:
                    last_detail = str(error)
                else:
                    return records, result_ids
            else:
                last_detail = (
                    "waiting for copied-result records: "
                    f"expected={[str(path) for path in expected_paths]!r}; "
                    f"observed={[str(path) for path in record_paths]!r}"
                )
                if simulation_refresh_error:
                    last_detail += (
                        "; latest SimulationList.refresh() error: "
                        + simulation_refresh_error
                    )

        if time.monotonic() >= deadline:
            raise RuntimeError(
                "Timed out waiting for RFPro to finish its asynchronous "
                "nonqueued result registration. " + last_detail
            )
        time.sleep(REGISTRATION_POLL_INTERVAL_SECONDS)


def execute_duplicate_plan(
    empro_module: Any,
    project: Any,
    source: Any,
    plan: DuplicatePlan,
) -> DuplicateResult:
    """Create inactive RFPro targets, then copy solved data without queueing."""

    duplicate = clone_analysis_for_plan(source, plan)

    appended = False
    registration_attempted = False
    registered: tuple[Any, ...] = ()
    replacements: tuple[tuple[Path, Path], ...] = ()
    try:
        # RFPro's public runAnalysis() uses this guard around simulation-record
        # creation. The duplicate is saved before creation so the backend sees
        # a persistent analysis/group association.
        end_creation_lifecycle = begin_simulation_creation_lifecycle(project)
        try:
            with project:
                appended_index = project.analyses.append(duplicate)
            appended = True
            # AnalysisList.append() publicly returns the index of the object
            # registered in RFPro. Continue with that authoritative object;
            # the pre-append clone can be detached from the analysis tree.
            duplicate = project.analyses[appended_index]
            with project:
                duplicate.simulationGroup = plan.duplicate_group
            project.saveActiveProject()
            registration_attempted = True
            registered = register_duplicate_results(project, duplicate, plan)
        finally:
            end_creation_lifecycle()
        print(
            "RFPro nonqueued target creation was requested; waiting up to "
            f"{DEFAULT_REGISTRATION_TIMEOUT_SECONDS:g} seconds for its inactive "
            "Created records."
        )
        registered, target_paths, target_group_path = wait_for_created_target_records(
            empro_module,
            project,
            plan,
            registered,
            timeout_seconds=DEFAULT_REGISTRATION_TIMEOUT_SECONDS,
        )
        plan = replace(
            plan,
            duplicate_group=target_group_path.name,
            duplicate_group_path=target_group_path,
            target_result_paths=target_paths,
            transplant_source_results=True,
        )
        if _optional_group_id(getattr(duplicate, "simulationGroup", "")) != (
            plan.duplicate_group
        ):
            with project:
                duplicate.simulationGroup = plan.duplicate_group
            project.saveActiveProject()
        replacements = transplant_source_results(project, plan)
        print(
            "Solved source data was copied into RFPro's registered inactive "
            "target paths; verifying the duplicate output association."
        )
        registered, verified_ids = wait_for_duplicate_registration(
            empro_module,
            project,
            duplicate,
            plan,
            registered,
            timeout_seconds=DEFAULT_REGISTRATION_TIMEOUT_SECONDS,
        )
        cleanup_errors = discard_result_transplant_backups(replacements)
        if cleanup_errors:
            print(
                "Duplicate results verified, but temporary Created-directory "
                "backups could not be removed: " + "; ".join(cleanup_errors)
            )
    except Exception as error:
        if registration_attempted:
            rollback_errors = rollback_result_transplants(replacements)
            # RFPro can return before its backend finishes adding Created
            # records. Once requested, never delete the owning analysis or
            # result group automatically—even an empty return is inconclusive.
            observed_records: tuple[Any, ...] = ()
            observed_paths: tuple[Path, ...] = ()
            try:
                observed_records, observed_paths = copied_result_records(project, plan)
            except Exception:
                pass
            active = active_simulation_descriptions(registered)
            for description in active_simulation_descriptions(observed_records):
                if description not in active:
                    active.append(description)
            state = "active" if active else "inactive or still being created"
            paths = [str(path) for path in observed_paths]
            rollback_detail = (
                "; target-data rollback errors=" + repr(rollback_errors)
                if rollback_errors
                else "; any replaced target directories were restored"
            )
            raise RuntimeError(
                f"Analysis duplication could not be verified: {error}. RFPro's "
                "registration request may still be completing asynchronously, "
                "so its duplicate analysis and Created records were preserved"
                f"{rollback_detail}. Observed records are {state}; "
                f"observed paths={paths!r}. Do not create another copy. After "
                "the records settle, rerun this operation with the original "
                "source analysis and the exact preserved duplicate name to "
                "resume recovery."
            ) from error

        rollback_errors: list[str] = []
        analysis_rollback_succeeded = not appended
        if appended:
            try:
                with project:
                    del project.analyses[project.analyses.index(plan.duplicate_name)]
                try:
                    project.saveActiveProject()
                    analysis_rollback_succeeded = True
                except Exception as rollback_error:
                    rollback_errors.append(f"rollback save failed: {rollback_error}")
            except Exception as rollback_error:
                rollback_errors.append(f"analysis rollback failed: {rollback_error}")
        if analysis_rollback_succeeded:
            try:
                if plan.duplicate_group_path.is_dir():
                    shutil.rmtree(plan.duplicate_group_path)
            except Exception as rollback_error:
                rollback_errors.append(
                    f"result-directory rollback failed: {rollback_error}"
                )
            else:
                try:
                    # Drop the removed group from the output browser's memory.
                    refresh_result_browser(empro_module)
                except Exception as rollback_error:
                    rollback_errors.append(
                        f"output-browser rollback refresh failed: {rollback_error}"
                    )
        if rollback_errors:
            raise RuntimeError(
                f"Analysis duplication failed: {error}. "
                + "; ".join(rollback_errors)
                + f". Inspect the project and {plan.duplicate_group_path}."
            ) from error
        raise RuntimeError(
            f"Analysis duplication failed: {error}. The source analysis was not "
            "modified, and the duplicate analysis and copied result directory "
            "were rolled back before any registration request was made."
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


def _simulation_path_key(path: Path) -> tuple[int, int | str]:
    name = path.name
    return (0, int(name)) if name.isdigit() else (1, name.casefold())


def _parse_parameter_string(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in re.split(r"\s*[,;]\s*", str(text).strip()):
        separator = "=" if "=" in part else ":" if ":" in part else ""
        if not separator:
            continue
        name, value = part.split(separator, 1)
        if name.strip() and value.strip():
            parsed[name.strip()] = value.strip()
    return parsed


def _coerce_parameter_mapping(raw: Any) -> dict[str, str]:
    if raw is None:
        return {}
    if isinstance(raw, str):
        return _parse_parameter_string(raw)
    if isinstance(raw, Mapping) or hasattr(raw, "items"):
        try:
            return {
                str(name): str(value)
                for name, value in raw.items()
                if str(name) and value is not None
            }
        except Exception:
            return {}
    try:
        values = list(raw)
    except (TypeError, ValueError):
        return {}
    result: dict[str, str] = {}
    for value in values:
        if isinstance(value, (tuple, list)) and len(value) == 2:
            result[str(value[0])] = str(value[1])
            continue
        name = getattr(value, "name", None)
        item_value = getattr(value, "value", None)
        if name is not None and item_value is not None:
            result[str(name)] = str(item_value)
    return result


def _simulation_parameter_signature(simulation: Any) -> tuple[tuple[str, str], ...] | None:
    mapping: dict[str, str] = {}
    for attribute in ("getParameterValues", "parameterValues"):
        method = getattr(simulation, attribute, None)
        if not callable(method):
            continue
        for arguments in ((), ("ValueAndFrontendUnit",)):
            try:
                candidate = _coerce_parameter_mapping(method(*arguments))
            except Exception:
                continue
            if candidate:
                mapping.update(candidate)
                break
    for name, value in _parse_parameter_string(
        str(getattr(simulation, "parameterString", "") or "")
    ).items():
        mapping.setdefault(name, value)
    if not mapping:
        return None
    return tuple(
        sorted(
            (str(name), re.sub(r"\s+", "", str(value)).casefold())
            for name, value in mapping.items()
        )
    )


def _simulation_records_by_path(project: Any, results_root: Path) -> dict[str, Any]:
    records: dict[str, Any] = {}
    for simulation in project.simulations:
        resolved = _simulation_record_group_and_path(simulation, results_root)
        if resolved is None:
            continue
        _group_path, simulation_path = resolved
        records[normalized_path(simulation_path)] = simulation
    return records


def source_to_target_result_mapping(
    project: Any,
    plan: DuplicatePlan,
) -> tuple[tuple[Path, Path], ...]:
    """Map a cloned sweep's ordered source results to RFPro-created targets."""

    sources = sorted(plan.registered_result_paths, key=_simulation_path_key)
    targets = sorted(expected_target_result_paths(plan), key=_simulation_path_key)
    if len(sources) != len(targets):
        raise RuntimeError(
            "Cannot copy solved data because the source and RFPro-created target "
            f"counts differ: source={len(sources)}, target={len(targets)}."
        )

    records = _simulation_records_by_path(project, plan.source_group_path.parent)
    source_records = [records.get(normalized_path(path)) for path in sources]
    target_records = [records.get(normalized_path(path)) for path in targets]
    if all(record is not None for record in source_records + target_records):
        source_signatures = [
            _simulation_parameter_signature(record) for record in source_records
        ]
        target_signatures = [
            _simulation_parameter_signature(record) for record in target_records
        ]
        if all(signature is not None for signature in source_signatures + target_signatures):
            source_by_signature = dict(zip(source_signatures, sources))
            target_by_signature = dict(zip(target_signatures, targets))
            if (
                len(source_by_signature) == len(sources)
                and len(target_by_signature) == len(targets)
            ):
                if set(source_by_signature) != set(target_by_signature):
                    raise RuntimeError(
                        "RFPro-created target parameter combinations do not match "
                        "the source solved-result combinations; no data was copied."
                    )
                print("Matched source and target result paths by parameter values.")
                return tuple(
                    (source_by_signature[signature], target_by_signature[signature])
                    for signature in sorted(source_by_signature, key=str)
                )

    print(
        "RFPro did not expose unique parameter dictionaries for every source and "
        "target record; mapping cloned sweep points by simulation-ID order."
    )
    return tuple(zip(sources, targets))


def transplant_source_results(
    project: Any,
    plan: DuplicatePlan,
) -> tuple[tuple[Path, Path], ...]:
    """Atomically replace inactive RFPro-created point directories with solved data."""

    replacements: list[tuple[Path, Path]] = []
    active_stage: Path | None = None
    try:
        for source, target in source_to_target_result_mapping(project, plan):
            if not path_is_within(source, plan.source_group_path):
                raise RuntimeError(f"Source result escaped its group: {source}")
            if not path_is_within(target, plan.duplicate_group_path):
                raise RuntimeError(f"Target result escaped its group: {target}")
            if not source.is_dir() or not target.is_dir():
                raise RuntimeError(
                    f"Source or target result directory is missing: {source} -> {target}"
                )
            token = uuid.uuid4().hex
            active_stage = target.with_name(f".{target.name}.rfpro-copy-{token}")
            backup = target.with_name(f".{target.name}.rfpro-created-{token}")
            # Start from RFPro's Created directory so any target-only identity
            # metadata survives, then overlay the complete solved source point.
            shutil.copytree(
                target,
                active_stage,
                copy_function=shutil.copy2,
                symlinks=True,
            )
            shutil.copytree(
                source,
                active_stage,
                copy_function=shutil.copy2,
                symlinks=True,
                dirs_exist_ok=True,
            )
            os.replace(target, backup)
            try:
                os.replace(active_stage, target)
            except Exception:
                os.replace(backup, target)
                raise
            active_stage = None
            replacements.append((target, backup))
    except Exception as error:
        if active_stage is not None and active_stage.is_dir():
            shutil.rmtree(active_stage)
        rollback_errors: list[str] = []
        for target, backup in reversed(replacements):
            try:
                if target.is_dir():
                    shutil.rmtree(target)
                os.replace(backup, target)
            except Exception as rollback_error:
                rollback_errors.append(f"{target}: {rollback_error}")
        detail = (
            " Rollback errors: " + "; ".join(rollback_errors)
            if rollback_errors
            else " Created target directories were restored."
        )
        raise RuntimeError(f"Copying solved data into RFPro targets failed: {error}.{detail}") from error
    return tuple(replacements)


def rollback_result_transplants(
    replacements: Sequence[tuple[Path, Path]],
) -> list[str]:
    errors: list[str] = []
    for target, backup in reversed(replacements):
        try:
            if target.is_dir():
                shutil.rmtree(target)
            os.replace(backup, target)
        except Exception as error:
            errors.append(f"{target}: {error}")
    return errors


def discard_result_transplant_backups(
    replacements: Sequence[tuple[Path, Path]],
) -> list[str]:
    errors: list[str] = []
    for _target, backup in replacements:
        try:
            if backup.is_dir():
                shutil.rmtree(backup)
        except Exception as error:
            errors.append(f"{backup}: {error}")
    return errors


def resume_existing_duplicate_plan(
    empro_module: Any,
    project: Any,
    duplicate: Any,
    plan: DuplicatePlan,
) -> DuplicateResult:
    """Refresh and verify a preserved duplicate without creating more records."""

    active = running_simulation_descriptions(project)
    if active:
        details = "\n  ".join(active)
        raise RuntimeError(
            "Only inactive Created records can be resumed. Wait for or cancel "
            f"active simulations first:\n  {details}"
        )
    project.saveActiveProject()
    if ensure_duplicate_group_binding(project, duplicate, plan):
        # Persist the recovered association before refreshing the native
        # simulation table and output browser.
        project.saveActiveProject()
    replacements: tuple[tuple[Path, Path], ...] = ()
    if plan.transplant_source_results:
        print(
            "RFPro created the duplicate records in a different result group. "
            "Copying solved source data into those inactive registered paths."
        )
        replacements = transplant_source_results(project, plan)
    print(
        f"Refreshing preserved duplicate {plan.duplicate_name!r}; waiting up to "
        f"{DEFAULT_REGISTRATION_TIMEOUT_SECONDS:g} seconds for its existing "
        "Created records and output association."
    )
    try:
        _records, verified_ids = wait_for_duplicate_registration(
            empro_module,
            project,
            duplicate,
            plan,
            (),
            timeout_seconds=DEFAULT_REGISTRATION_TIMEOUT_SECONDS,
        )
    except Exception as error:
        rollback_errors = rollback_result_transplants(replacements)
        detail = (
            " Rollback errors: " + "; ".join(rollback_errors)
            if rollback_errors
            else " RFPro's original inactive Created directories were restored."
        )
        raise RuntimeError(f"Duplicate recovery failed: {error}.{detail}") from error
    cleanup_errors = discard_result_transplant_backups(replacements)
    if cleanup_errors:
        print(
            "Duplicate results verified, but temporary Created-directory backups "
            "could not be removed: " + "; ".join(cleanup_errors)
        )
    return DuplicateResult(duplicate, plan, verified_ids)


def build_confirmation(plan: DuplicatePlan) -> str:
    return "\n".join(
        (
            f"Source analysis: {plan.source_name}",
            f"New analysis: {plan.duplicate_name}",
            f"Source result group: {plan.source_group_path}",
            f"RFPro target group: {plan.duplicate_group_path}",
            f"Registered solved points: {len(plan.registered_result_ids)}",
            f"Data to copy: {_format_bytes(plan.source_size_bytes)}",
            "",
            "RFPro will first create inactive target records and directories.",
            "Each target point will then be atomically replaced with its matching",
            "solved source point. No simulation will be queued or started, and",
            "the source analysis and result files will not be modified.",
        )
    )


def build_resume_confirmation(plan: DuplicatePlan) -> str:
    lines = [
        f"Source analysis: {plan.source_name}",
        f"Existing duplicate: {plan.duplicate_name}",
        f"RFPro-registered simulation group: {plan.duplicate_group}",
        f"Registered result group: {plan.duplicate_group_path}",
        f"Expected solved points: {len(plan.registered_result_ids)}",
    ]
    if plan.transplant_source_results:
        lines.extend(
            (
                "",
                "RFPro registered inactive Created records in a different group",
                "than the earlier copied data. Each Created point directory will be",
                "backed up and atomically replaced with its solved source point.",
                "Backups are removed only after RFPro verifies every result.",
            )
        )
        if plan.redundant_copied_group_path is not None:
            lines.append(
                "The redundant earlier copy is left unchanged: "
                + str(plan.redundant_copied_group_path)
            )
    lines.extend(
        (
            "",
            "RFPro's simulation table and output association will be refreshed.",
            "No new simulation records will be requested or queued.",
        )
    )
    return "\n".join(lines)


def _choose_duplicate_name(
    project: Any, source: Any, requested: str
) -> str | None:
    names = analysis_names(project)
    if requested:
        cleaned = str(requested).strip()
        if not cleaned:
            raise ValueError("The duplicate analysis name cannot be empty.")
        return cleaned
    from PySide6.QtWidgets import QInputDialog

    suggested = default_duplicate_name(str(source.name), names)
    selected, accepted = QInputDialog.getText(
        None,
        "Duplicate RFPro analysis and results",
        "New analysis name, or existing incomplete copy to resume:",
        text=suggested,
    )
    if not accepted:
        return None
    cleaned = str(selected).strip()
    if not cleaned:
        raise ValueError("The duplicate analysis name cannot be empty.")
    return cleaned


def _confirm(plan: DuplicatePlan, resume_existing: bool = False) -> bool:
    from PySide6.QtWidgets import QMessageBox

    return (
        QMessageBox.question(
            None,
            (
                "Resume RFPro copied-results association?"
                if resume_existing
                else "Duplicate RFPro analysis and solved data?"
            ),
            (
                build_resume_confirmation(plan)
                if resume_existing
                else build_confirmation(plan)
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        == QMessageBox.StandardButton.Yes
    )


def _choose_resume_group(candidates: Sequence[Path]) -> str | None:
    from PySide6.QtWidgets import QInputDialog

    labels = [str(path) for path in candidates]
    selected, accepted = QInputDialog.getItem(
        None,
        "Recover RFPro duplicate result group",
        "Multiple Created-record groups match. Select the group for this duplicate:",
        labels,
        0,
        False,
    )
    if not accepted:
        return None
    return Path(str(selected)).name


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Duplicate an RFPro analysis and its saved result group."
    )
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS_NAME)
    parser.add_argument("--new-name", default=DEFAULT_DUPLICATE_NAME)
    parser.add_argument("--resume-group", default=DEFAULT_RESUME_GROUP_ID)
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
    resume_existing = duplicate_name in analysis_names(project)
    if resume_existing:
        try:
            duplicate, plan = prepare_resume_plan(
                empro,
                project,
                source,
                duplicate_name,
                arguments.resume_group,
            )
        except AmbiguousResumeGroupsError as error:
            selected_group = _choose_resume_group(error.candidates)
            if selected_group is None:
                print("Duplicate recovery cancelled; nothing was changed.")
                return
            duplicate, plan = prepare_resume_plan(
                empro,
                project,
                source,
                duplicate_name,
                selected_group,
            )
        preview = build_resume_confirmation(plan)
    else:
        plan = prepare_duplicate_plan(empro, project, source, duplicate_name)
        preview = build_confirmation(plan)
    print(preview)
    if not arguments.yes and not _confirm(plan, resume_existing):
        print("Analysis duplication cancelled; no files or analyses were changed.")
        return

    if resume_existing:
        result = resume_existing_duplicate_plan(
            empro,
            project,
            duplicate,
            plan,
        )
    else:
        result = execute_confirmed_duplicate_plan(
            empro,
            project,
            source,
            plan,
        )
    summary = (
        f"{'Recovered' if resume_existing else 'Created'} analysis "
        f"{result.plan.duplicate_name!r} with independent "
        f"simulation group {result.plan.duplicate_group!r} and verified "
        f"{len(result.verified_result_ids)} solved result(s). No simulation was started."
    )
    print(summary)
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.information(None, "RFPro Analysis Duplicated", summary)


if __name__ == "__main__":
    main()
