"""Interactively preview geometry and saved Mesh/Ports sweep results in RFPro.

Run this script inside the open RFPro project. It expands the selected
analysis's native ``parameterSequences``, applies one point at a time to the
active project, and refreshes RFPro's geometry view. For solved conditions it
can also load and export RFPro's saved Mesh/Ports result view. No simulations
are created, queued, deleted, or otherwise modified.

The original project-parameter formulas are restored when the inspector
closes. The script deliberately does not save the project.
"""

from __future__ import annotations

import argparse
import html
import itertools
import math
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


# Edit this when RFPro's Run Script command cannot pass arguments.
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_ZOOM_TO_EXTENTS = False
# Number of digits after the decimal point for PDF geometry values in um.
DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES = 3
_INSPECTOR_REGISTRY_ATTRIBUTE = "_rfpro_sweep_geometry_inspectors"


@dataclass(frozen=True)
class SweepValue:
    """One evaluated native sweep value and its user-facing representation."""

    parameter_name: str
    value: Any
    display: str


@dataclass(frozen=True)
class SweepPoint:
    """One expanded parameter combination from one native sequence."""

    point_index: int
    sequence_index: int
    combination_index: int
    values: tuple[SweepValue, ...]


@dataclass(frozen=True)
class QtRuntime:
    """Objects and diagnostics kept alive for the complete RFPro operation."""

    application: Any
    pyside_file: Path
    plugin_file: Path | None
    application_was_created: bool
    environment_was_restored: bool


@dataclass(frozen=True)
class GeometryReportPage:
    """One sweep-point report page and its optional exported RFPro image."""

    point: SweepPoint
    valid: bool | None
    message: str
    image_path: Path | None
    capture_error: str = ""
    status_label: str = ""


@dataclass(frozen=True)
class MeshPortsResult:
    """One saved RFPro result and its discovered Mesh/Ports data."""

    simulation_id: str
    simulation_output: Any
    parameters: tuple[tuple[str, str], ...]
    mesh_kind: str | None
    mesh_file: Path | None
    unavailable_reason: str = ""


@dataclass(frozen=True)
class MeshPortsInventory:
    """Safe mapping between configured sweep points and saved RFPro results."""

    analysis_output: Any
    results_by_point: tuple[tuple[int, MeshPortsResult], ...]
    missing_point_indices: tuple[int, ...]
    missing_mesh_point_indices: tuple[int, ...]
    unmatched_result_ids: tuple[str, ...]
    diagnostics: tuple[str, ...]

    def result_for_point(self, point_index: int) -> MeshPortsResult | None:
        for candidate_index, result in self.results_by_point:
            if candidate_index == point_index:
                return result
        return None

    def available_results(self) -> tuple[tuple[int, MeshPortsResult], ...]:
        return tuple(
            (point_index, result)
            for point_index, result in self.results_by_point
            if result.mesh_file is not None and result.mesh_kind is not None
        )


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


def _choose_analysis(project: Any, requested_name: str) -> Any:
    names = analysis_names(project)
    if requested_name or len(names) <= 1:
        return find_analysis(project, requested_name)

    from PySide6.QtWidgets import QInputDialog

    selected, accepted = QInputDialog.getItem(
        None,
        "RFPro Sweep Geometry Inspector",
        "Analysis:",
        names,
        0,
        False,
    )
    if not accepted:
        raise RuntimeError("Analysis selection was cancelled.")
    return find_analysis(project, str(selected))


def _value_text(value: Any) -> str:
    """Return a stable display string for an EMPro expression or numeric value."""

    formula = getattr(value, "formula", None)
    if callable(formula):
        try:
            return str(formula())
        except Exception:
            pass
    return str(value)


def _evaluated_sweep_values(sweep: Any) -> list[Any]:
    values = getattr(sweep, "parameterValues", None)
    if values is not None:
        evaluated = list(values)
        if evaluated:
            return evaluated

    get_values = getattr(sweep, "getParameterValues", None)
    if callable(get_values):
        values = get_values()
        if isinstance(values, str):
            return [values]
        evaluated = list(values or [])
        if evaluated:
            return evaluated
    return []


def _display_sweep_values(sweep: Any, evaluated: Sequence[Any]) -> list[str]:
    """Prefer preserved formulas when the binding exposes them unambiguously."""

    get_values = getattr(sweep, "getParameterValues", None)
    if callable(get_values):
        try:
            displayed = get_values()
        except Exception:
            displayed = None
        if isinstance(displayed, str):
            if len(evaluated) == 1:
                return [displayed]
        elif displayed is not None:
            displayed_values = list(displayed)
            if len(displayed_values) == len(evaluated):
                return [_value_text(value) for value in displayed_values]
    return [_value_text(value) for value in evaluated]


def expand_parameter_sequences(settings: Any) -> list[SweepPoint]:
    """Expand every native sequence into the parameter points RFPro will run."""

    if not bool(settings.parameterSweepEnabled):
        raise RuntimeError("Parameter sweeping is disabled for the selected analysis.")

    points: list[SweepPoint] = []
    for sequence_index, sequence in enumerate(settings.parameterSequences):
        sweep_definitions: list[tuple[str, list[Any], list[str]]] = []
        seen_names: set[str] = set()
        for sweep in sequence:
            name = str(sweep.parameterName)
            if not name:
                raise ValueError(f"Sequence {sequence_index + 1} has an unnamed parameter.")
            if name in seen_names:
                raise ValueError(
                    f"Sequence {sequence_index + 1} repeats parameter {name!r}."
                )
            seen_names.add(name)
            evaluated = _evaluated_sweep_values(sweep)
            if not evaluated:
                raise ValueError(
                    f"Sequence {sequence_index + 1}, parameter {name!r}, has no values."
                )
            displayed = _display_sweep_values(sweep, evaluated)
            sweep_definitions.append((name, evaluated, displayed))

        if not sweep_definitions:
            continue

        choices: list[list[tuple[str, Any, str]]] = []
        for name, evaluated, displayed in sweep_definitions:
            choices.append(
                [
                    (name, value, displayed[index])
                    for index, value in enumerate(evaluated)
                ]
            )

        for combination_index, combination in enumerate(itertools.product(*choices)):
            values = tuple(
                SweepValue(parameter_name=name, value=value, display=display)
                for name, value, display in combination
            )
            points.append(
                SweepPoint(
                    point_index=len(points),
                    sequence_index=sequence_index,
                    combination_index=combination_index,
                    values=values,
                )
            )

    if not points:
        raise RuntimeError("The selected analysis contains no parameter sweep points.")
    return points


def swept_parameter_names(points: Iterable[SweepPoint]) -> list[str]:
    return sorted({value.parameter_name for point in points for value in point.values})


def snapshot_parameter_formulas(project: Any, names: Iterable[str]) -> dict[str, Any]:
    parameters = project.parameters
    available = {str(name) for name in parameters.names()}
    requested = list(names)
    missing = sorted(set(requested) - available)
    if missing:
        raise ValueError(
            "Sweep parameters are missing from the active project: " + ", ".join(missing)
        )
    return {name: parameters.formula(name) for name in requested}


def apply_sweep_point(
    project: Any, baseline_formulas: dict[str, Any], point: SweepPoint
) -> None:
    """Reset all swept parameters to baseline, then apply one combination."""

    parameters = project.parameters
    for name, formula in baseline_formulas.items():
        parameters.setFormula(name, formula)
    for sweep_value in point.values:
        parameters.setFormula(sweep_value.parameter_name, sweep_value.value)


def restore_parameter_formulas(project: Any, baseline_formulas: dict[str, Any]) -> None:
    """Restore the formulas captured before interactive sweep inspection."""

    for name, formula in baseline_formulas.items():
        project.parameters.setFormula(name, formula)


def _native_geometry_update_bindings(project: Any) -> tuple[Any, Any]:
    """Resolve the targeted RFPro PCell update path before changing formulas."""

    load_design_parameters = getattr(
        project, "_loadOaParametersFromDesignSpec", None
    )
    if not callable(load_design_parameters):
        raise RuntimeError(
            "The active RFPro project does not expose the ADS 2026 design-spec "
            "parameter loader _loadOaParametersFromDesignSpec()."
        )

    layout = getattr(project, "layout", None)
    native_update = getattr(layout, "_updateDesignParameters", None)
    if not callable(native_update):
        raise RuntimeError(
            "The active RFPro layout does not expose the targeted PCell geometry "
            "updater _updateDesignParameters(Mapping[str, str])."
        )
    return load_design_parameters, native_update


def _current_parameter_formula_strings(
    project: Any, parameter_names: Iterable[str]
) -> dict[str, str]:
    """Read the formulas that will be passed to RFPro's layout updater."""

    formula_method = getattr(project.parameters, "formula", None)
    if not callable(formula_method):
        raise RuntimeError(
            "The active RFPro project does not expose ParameterList.formula()."
        )

    updates: dict[str, str] = {}
    for name in parameter_names:
        formula = str(formula_method(name))
        if not formula:
            raise ValueError(f"RFPro parameter {name!r} has an empty formula.")
        updates[name] = formula
    if not updates:
        raise ValueError("At least one RFPro geometry parameter is required.")
    return updates


def apply_sweep_point_to_geometry(
    project: Any, baseline_formulas: dict[str, Any], point: SweepPoint
) -> dict[str, Any]:
    """Set one point and submit its formulas to the active layout updater."""

    load_design_parameters, native_update = _native_geometry_update_bindings(project)
    load_design_parameters()
    apply_sweep_point(project, baseline_formulas, point)
    updates = _current_parameter_formula_strings(project, baseline_formulas)
    native_status = native_update(updates)
    return {"updates": updates, "native_status": str(native_status)}


def restore_parameter_formulas_and_geometry(
    project: Any, baseline_formulas: dict[str, Any]
) -> dict[str, Any]:
    """Restore baseline formulas and regenerate their active-layout geometry."""

    load_design_parameters, native_update = _native_geometry_update_bindings(project)
    load_design_parameters()
    restore_parameter_formulas(project, baseline_formulas)
    updates = _current_parameter_formula_strings(project, baseline_formulas)
    native_status = native_update(updates)
    return {"updates": updates, "native_status": str(native_status)}


def geometry_validity(project: Any) -> tuple[bool | None, str]:
    """Return the public project-geometry validity result when available."""

    geometry = project.geometry
    is_valid = getattr(geometry, "isValid", None)
    if not callable(is_valid):
        return None, "RFPro does not expose geometry.isValid() in this release."
    try:
        valid = bool(is_valid())
    except Exception as error:
        return False, f"Geometry validity check failed: {error}"
    if valid:
        return True, "Geometry is valid."

    reason_method = getattr(geometry, "reasonWhyInvalid", None)
    if callable(reason_method):
        try:
            reason = str(reason_method() or "").strip()
        except Exception as error:
            reason = f"Could not obtain invalidity reason: {error}"
    else:
        reason = ""
    return False, reason or "RFPro reports invalid geometry without a reason."


def refresh_geometry_view(empro_module: Any, zoom_to_extents: bool = False) -> None:
    """Show and repaint RFPro's active geometry view."""

    project_view = empro_module.gui.activeProjectView()
    project_view.showGeometryView()
    empro_module.gui.processEvents()
    geometry_view = project_view.geometryView()
    geometry_view.updateView()
    empro_module.gui.processEvents()
    if zoom_to_extents:
        geometry_view.zoomGeometryViewToExtents()
        empro_module.gui.processEvents()


def _call_or_value(value: Any, default: Any = None) -> Any:
    """Read either a Qt-style method or an EMPro wrapper property."""

    if value is None:
        return default
    try:
        return value() if callable(value) else value
    except Exception:
        return default


def _getattr_or_default(value: Any, name: str, default: Any = None) -> Any:
    """Read an attribute without propagating a deleted PySide-wrapper error."""

    try:
        return getattr(value, name, default)
    except (RuntimeError, ReferenceError):
        return default


def _qt_object_is_valid(value: Any) -> bool:
    """Return whether a Shiboken wrapper still owns a callable C++ object."""

    try:
        import shiboken6
    except ImportError:
        return True

    validator = getattr(shiboken6, "isValid", None)
    if not callable(validator):
        shiboken_type = getattr(shiboken6, "Shiboken", None)
        validator = getattr(shiboken_type, "isValid", None)
    if not callable(validator):
        return True
    try:
        return bool(validator(value))
    except TypeError:
        # Portable tests and EMPro wrapper objects need not be Shiboken types.
        return True
    except (RuntimeError, ReferenceError):
        return False


def _action_text(action: Any) -> str:
    return str(
        _call_or_value(_getattr_or_default(action, "text"), "") or ""
    )


def _normalized_action_text(text: str) -> str:
    without_mnemonics = str(text).replace("&", "").replace("…", " ")
    return " ".join(re.findall(r"[a-z0-9]+", without_mnemonics.casefold()))


def _iter_menu_actions_with_owners(
    menu: Any,
    owner_prefix: tuple[Any, ...] = (),
) -> Iterable[tuple[Any, tuple[Any, ...]]]:
    """Yield menu actions together with the wrappers that keep them alive."""

    pending = [(menu, owner_prefix + (menu,))]
    seen_menus: set[int] = set()
    while pending:
        current, owners = pending.pop()
        if current is None or id(current) in seen_menus:
            continue
        seen_menus.add(id(current))
        actions = _call_or_value(
            _getattr_or_default(current, "actions"), []
        ) or []
        for action in actions:
            action_owners = owners + (action,)
            yield action, action_owners
            submenu = _call_or_value(
                _getattr_or_default(action, "menu"), None
            )
            if submenu is not None:
                pending.append((submenu, action_owners + (submenu,)))


def _action_is_enabled(action: Any) -> bool:
    enabled = _call_or_value(
        _getattr_or_default(action, "isEnabled"),
        _call_or_value(_getattr_or_default(action, "enabled"), True),
    )
    return bool(enabled)


def _action_can_trigger(action: Any) -> bool:
    return callable(_getattr_or_default(action, "trigger")) or callable(
        _getattr_or_default(action, "onTriggered")
    )


def _action_trigger(action: Any) -> None:
    """Activate the same QAction slot used by a manual menu click."""

    if not _qt_object_is_valid(action):
        raise RuntimeError(
            "RFPro's resolved Export Image QAction was deleted before it "
            "could be triggered."
        )
    trigger = _getattr_or_default(action, "trigger")
    if callable(trigger):
        trigger()
        return
    on_triggered = _getattr_or_default(action, "onTriggered")
    if callable(on_triggered):
        try:
            on_triggered(False)
        except TypeError:
            on_triggered()
        return
    raise RuntimeError(
        f"The RFPro action {_action_text(action)!r} exposes no trigger method."
    )


def find_rfpro_export_image_action(
    project_view: Any,
    application: Any,
    qt_action_type: type[Any] | None = None,
) -> tuple[Any, str, tuple[Any, ...]]:
    """Find RFPro's View > Export Image action without invoking it."""

    records: list[tuple[int, Any, str, tuple[Any, ...]]] = []
    discovered: list[str] = []

    def record_menu_candidates(
        menu: Any,
        owner_prefix: tuple[Any, ...],
        source: str,
        base_score: int,
    ) -> None:
        for action, owners in _iter_menu_actions_with_owners(
            menu, owner_prefix
        ):
            text = _action_text(action)
            if text:
                discovered.append(f"{source}: {text}")
            normalized = _normalized_action_text(text)
            if "export" not in normalized or "image" not in normalized:
                continue
            if not _qt_object_is_valid(action):
                discovered.append(f"{source} action is already deleted: {text}")
                continue
            if not _action_can_trigger(action):
                discovered.append(
                    f"{source} action cannot be triggered from Python: {text}"
                )
                continue
            score = base_score + (50 if normalized == "export image" else 0)
            score += 20 if _action_is_enabled(action) else 0
            records.append((score, action, f"{source} > {text}", owners))

    try:
        view_menu = project_view.menu("view")
    except Exception as error:
        view_menu = None
        discovered.append(f"RFPro View menu unavailable: {error}")
    if view_menu is not None:
        record_menu_candidates(
            view_menu, (project_view,), "RFPro View menu", 300
        )

    if qt_action_type is None:
        try:
            from PySide6.QtGui import QAction

            qt_action_type = QAction
        except Exception:
            qt_action_type = None
    if qt_action_type is not None:
        seen_actions: set[int] = set()
        top_levels = _call_or_value(
            _getattr_or_default(application, "topLevelWidgets"), []
        ) or []
        for top_level in top_levels:
            window_title = str(
                _call_or_value(
                    _getattr_or_default(top_level, "windowTitle"), ""
                )
                or ""
            )
            title_normalized = window_title.casefold()
            title_score = (
                20
                if "rfpro" in title_normalized or "empro" in title_normalized
                else 0
            )

            # Prefer the live main-window menu bar. Unlike an unconstrained
            # findChildren() search, this follows View's current owner chain.
            menu_bars: list[Any] = []
            menu_bar = _call_or_value(
                _getattr_or_default(top_level, "menuBar"), None
            )
            if menu_bar is not None:
                menu_bars.append(menu_bar)
            try:
                from PySide6.QtWidgets import QMenuBar
            except Exception:
                QMenuBar = None  # type: ignore[assignment,misc]
            find_children = _getattr_or_default(top_level, "findChildren")
            if callable(find_children) and QMenuBar is not None:
                try:
                    for candidate in find_children(QMenuBar):
                        if candidate not in menu_bars:
                            menu_bars.append(candidate)
                except Exception:
                    pass
            for candidate_menu_bar in menu_bars:
                root_actions = _call_or_value(
                    _getattr_or_default(candidate_menu_bar, "actions"), []
                ) or []
                for root_action in root_actions:
                    root_text = _action_text(root_action)
                    if _normalized_action_text(root_text) != "view":
                        continue
                    live_view_menu = _call_or_value(
                        _getattr_or_default(root_action, "menu"), None
                    )
                    if live_view_menu is None:
                        continue
                    record_menu_candidates(
                        live_view_menu,
                        (top_level, candidate_menu_bar, root_action),
                        f"Qt window {window_title!r} View menu",
                        400 + title_score,
                    )

            # Retain the broad lookup only as a compatibility fallback for
            # RFPro builds whose main window does not expose menuBar().
            if not callable(find_children):
                continue
            try:
                actions = find_children(qt_action_type)
            except Exception:
                continue
            for action in actions:
                if id(action) in seen_actions:
                    continue
                seen_actions.add(id(action))
                if not _qt_object_is_valid(action):
                    continue
                text = _action_text(action)
                normalized = _normalized_action_text(text)
                if "export" not in normalized or "image" not in normalized:
                    continue
                discovered.append(f"Qt window {window_title!r}: {text}")
                if not _action_can_trigger(action):
                    continue
                score = 200 if normalized == "export image" else 150
                score += title_score
                if _action_is_enabled(action):
                    score += 10
                records.append(
                    (
                        score,
                        action,
                        f"Qt window {window_title!r} > {text}",
                        (top_level, action),
                    )
                )

    if not records:
        details = "\n  ".join(discovered[-40:]) or "no menu actions were visible"
        raise RuntimeError(
            "RFPro's Export Image action was not found. Discovered menu state:\n  "
            + details
        )
    records.sort(key=lambda record: record[0], reverse=True)
    for _score, action, description, owners in records:
        if not _qt_object_is_valid(action):
            discovered.append(f"Candidate became invalid: {description}")
            continue
        if not _action_is_enabled(action):
            discovered.append(f"Candidate is disabled: {description}")
            continue
        return action, description, owners
    details = "\n  ".join(discovered[-40:])
    raise RuntimeError(
        "Every discovered RFPro Export Image action was invalid or disabled:\n  "
        + details
    )


class QtSaveDialogAutomation:
    """Supply a filename to the save dialog opened by Export Image."""

    def __init__(
        self,
        application: Any,
        output_path: Path,
        timeout_seconds: float = 8.0,
    ) -> None:
        from PySide6.QtCore import QTimer, Qt
        from PySide6.QtWidgets import QComboBox, QFileDialog, QLineEdit, QPushButton

        self.application = application
        self.output_path = output_path.expanduser().resolve()
        self.timeout_seconds = timeout_seconds
        self.output_wait_seconds = 12.0
        self.timer_type = QTimer
        self.dont_use_native_dialogs_attribute = (
            Qt.ApplicationAttribute.AA_DontUseNativeDialogs
        )
        self.file_dialog_type = QFileDialog
        self.push_button_type = QPushButton
        self.line_edit_type = QLineEdit
        self.combo_box_type = QComboBox
        self.timer = QTimer()
        self.timer.setInterval(25)
        self.timer.timeout.connect(self._poll)
        self.started_at = 0.0
        self.file_dialog_was_accepted = False
        self.file_dialog_accept_requested = False
        self.file_dialog_accept_scheduled = False
        self.file_dialog_accept_method = "not requested"
        self.file_dialog: Any = None
        self.file_dialog_selected_files: list[str] = []
        self.file_dialog_directory = ""
        self.file_dialog_name_filters: list[str] = []
        self.file_dialog_selected_name_filter = ""
        self.custom_dialog_was_advanced = False
        self.custom_filename_was_set = False
        self.timed_out = False
        self.observed_dialogs: list[str] = []
        self.native_dialogs_were_disabled = False

    def start(self) -> None:
        test_attribute = getattr(self.application, "testAttribute", None)
        set_attribute = getattr(self.application, "setAttribute", None)
        if callable(test_attribute) and callable(set_attribute):
            self.native_dialogs_were_disabled = bool(
                test_attribute(self.dont_use_native_dialogs_attribute)
            )
            set_attribute(self.dont_use_native_dialogs_attribute, True)
        self.started_at = time.monotonic()
        self.timer.start()

    def stop(self) -> None:
        self.timer.stop()
        if not self.native_dialogs_were_disabled:
            set_attribute = getattr(self.application, "setAttribute", None)
            if callable(set_attribute):
                set_attribute(self.dont_use_native_dialogs_attribute, False)

    def diagnostics(self) -> str:
        details = ", ".join(self.observed_dialogs) or "no modal dialog was exposed"
        return (
            f"save requested={self.file_dialog_accept_requested}; "
            f"accepted signal={self.file_dialog_was_accepted}; "
            f"accept method={self.file_dialog_accept_method}; "
            f"selected files={self.file_dialog_selected_files!r}; "
            f"directory={self.file_dialog_directory!r}; "
            f"selected filter={self.file_dialog_selected_name_filter!r}; "
            f"filters={self.file_dialog_name_filters!r}; "
            f"custom dialog advanced={self.custom_dialog_was_advanced}; "
            f"custom filename set={self.custom_filename_was_set}; "
            f"timed out={self.timed_out}; observed={details}"
        )

    def _visible_dialogs(self) -> list[Any]:
        candidates: list[Any] = []
        active = _call_or_value(
            getattr(self.application, "activeModalWidget", None), None
        )
        if active is not None:
            candidates.append(active)
        top_levels = _call_or_value(
            getattr(self.application, "topLevelWidgets", None), []
        ) or []
        for widget in top_levels:
            if widget not in candidates:
                candidates.append(widget)
        return candidates

    def _describe_dialog(self, dialog: Any) -> str:
        title = str(
            _call_or_value(getattr(dialog, "windowTitle", None), "") or ""
        )
        return f"{type(dialog).__name__}({title!r})"

    def _capture_file_dialog_state(self, dialog: Any) -> None:
        selected_files = _call_or_value(
            _getattr_or_default(dialog, "selectedFiles"), []
        ) or []
        if selected_files:
            self.file_dialog_selected_files = [
                str(path) for path in selected_files
            ]
        directory = _call_or_value(
            _getattr_or_default(dialog, "directory"), None
        )
        captured_directory = str(
            _call_or_value(
                _getattr_or_default(directory, "absolutePath"), directory or ""
            )
            or ""
        )
        if captured_directory:
            self.file_dialog_directory = captured_directory
        name_filters = _call_or_value(
            _getattr_or_default(dialog, "nameFilters"), []
        ) or []
        if name_filters:
            self.file_dialog_name_filters = [
                str(value) for value in name_filters
            ]
        selected_name_filter = str(
            _call_or_value(
                _getattr_or_default(dialog, "selectedNameFilter"), ""
            )
            or ""
        )
        if selected_name_filter:
            self.file_dialog_selected_name_filter = selected_name_filter

    def _file_dialog_accepted(self, dialog: Any) -> None:
        self.file_dialog_was_accepted = True
        self._capture_file_dialog_state(dialog)

    def _activate_file_dialog_save(self) -> None:
        dialog = self.file_dialog
        if dialog is None or not _qt_object_is_valid(dialog):
            self.file_dialog_accept_method = "dialog was deleted before Save"
            return
        self._capture_file_dialog_state(dialog)
        find_children = _getattr_or_default(dialog, "findChildren")
        buttons = (
            find_children(self.push_button_type)
            if callable(find_children)
            else []
        )
        ranked_buttons: list[tuple[int, Any, str]] = []
        for button in buttons:
            button_text = _normalized_action_text(
                str(
                    _call_or_value(_getattr_or_default(button, "text"), "")
                    or ""
                )
            )
            is_default = bool(
                _call_or_value(
                    _getattr_or_default(button, "isDefault"), False
                )
            )
            rank = {"save": 40, "export": 30, "ok": 20}.get(
                button_text, 10 if is_default else 0
            )
            if rank:
                ranked_buttons.append((rank, button, button_text or "default"))
        if ranked_buttons:
            _rank, button, button_text = max(
                ranked_buttons, key=lambda item: item[0]
            )
            self.file_dialog_accept_requested = True
            self.file_dialog_accept_method = f"clicked {button_text!r} button"
            try:
                button.click()
            except Exception as error:
                self.file_dialog_accept_method += f"; click failed: {error}"
            return
        accept = _getattr_or_default(dialog, "accept")
        if callable(accept):
            self.file_dialog_accept_requested = True
            self.file_dialog_accept_method = "direct accept() fallback"
            try:
                accept()
            except Exception as error:
                self.file_dialog_accept_method += f"; call failed: {error}"
            return
        self.file_dialog_accept_method = "no Save button or accept() method"

    def _poll(self) -> None:
        if self.file_dialog_was_accepted:
            return
        dialogs = self._visible_dialogs()
        for dialog in dialogs:
            visible = _call_or_value(getattr(dialog, "isVisible", None), True)
            if not visible:
                continue
            description = self._describe_dialog(dialog)
            if description not in self.observed_dialogs:
                self.observed_dialogs.append(description)
            if isinstance(dialog, self.file_dialog_type):
                if self.file_dialog_accept_scheduled:
                    continue
                try:
                    dialog.setAcceptMode(
                        self.file_dialog_type.AcceptMode.AcceptSave
                    )
                    dialog.setDefaultSuffix("png")
                    dialog.setDirectory(str(self.output_path.parent))
                    name_filters = dialog.nameFilters()
                    for name_filter in name_filters:
                        if "png" in str(name_filter).casefold():
                            dialog.selectNameFilter(name_filter)
                            break
                    dialog.selectFile(str(self.output_path))
                    find_children = _getattr_or_default(
                        dialog, "findChildren"
                    )
                    line_edits = (
                        find_children(self.line_edit_type)
                        if callable(find_children)
                        else []
                    )
                    for line_edit in line_edits:
                        object_name = _normalized_action_text(
                            str(
                                _call_or_value(
                                    _getattr_or_default(
                                        line_edit, "objectName"
                                    ),
                                    "",
                                )
                                or ""
                            )
                        )
                        if object_name == "filenameedit":
                            line_edit.setText(self.output_path.name)
                            break
                    accepted_signal = _getattr_or_default(dialog, "accepted")
                    connect = _getattr_or_default(accepted_signal, "connect")
                    if callable(connect):
                        connect(lambda: self._file_dialog_accepted(dialog))
                    self.file_dialog = dialog
                    self.file_dialog_accept_scheduled = True
                    self._capture_file_dialog_state(dialog)
                    self.timer_type.singleShot(
                        0, self._activate_file_dialog_save
                    )
                except Exception as error:
                    self.file_dialog_accept_method = (
                        f"dialog setup failed: {error}"
                    )
                    continue
                return

            title = _normalized_action_text(
                str(
                    _call_or_value(
                        getattr(dialog, "windowTitle", None), ""
                    )
                    or ""
                )
            )
            if (
                not self.custom_dialog_was_advanced
                and ("export" in title or "save" in title)
                and "image" in title
            ):
                find_children = getattr(dialog, "findChildren", None)
                if callable(find_children):
                    combo_boxes = find_children(self.combo_box_type)
                    for combo_box in combo_boxes:
                        for index in range(combo_box.count()):
                            if "png" in str(combo_box.itemText(index)).casefold():
                                combo_box.setCurrentIndex(index)
                                break
                    line_edits = find_children(self.line_edit_type)
                    for line_edit in line_edits:
                        metadata = " ".join(
                            str(
                                _call_or_value(
                                    getattr(line_edit, attribute_name, None), ""
                                )
                                or ""
                            )
                            for attribute_name in (
                                "objectName",
                                "placeholderText",
                                "toolTip",
                                "accessibleName",
                                "text",
                            )
                        ).casefold()
                        if len(line_edits) == 1 or any(
                            token in metadata
                            for token in ("file", "path", "name", ".png")
                        ):
                            line_edit.setText(str(self.output_path))
                            self.custom_filename_was_set = True
                            break
                buttons = (
                    find_children(self.push_button_type)
                    if callable(find_children)
                    else []
                )
                for button in buttons:
                    button_text = _normalized_action_text(
                        str(
                            _call_or_value(getattr(button, "text", None), "")
                            or ""
                        )
                    )
                    is_default = bool(
                        _call_or_value(getattr(button, "isDefault", None), False)
                    )
                    if button_text in {"export", "save", "ok"} or is_default:
                        self.custom_dialog_was_advanced = True
                        self.timer_type.singleShot(0, button.click)
                        return

        if time.monotonic() - self.started_at < self.timeout_seconds:
            return
        self.timed_out = True
        active = _call_or_value(
            getattr(self.application, "activeModalWidget", None), None
        )
        if active is not None:
            title = _normalized_action_text(
                str(
                    _call_or_value(getattr(active, "windowTitle", None), "") or ""
                )
            )
            if (
                "rfpro sweep geometry" not in title
                and "geometry validation" not in title
            ):
                reject = getattr(active, "reject", None)
                if callable(reject):
                    reject()


def _rfpro_export_candidate_paths(
    output_path: Path,
    automation: Any,
) -> list[Path]:
    """Return exact and RFPro-suffixed paths that may contain the export."""

    expected = output_path.expanduser().resolve()
    raw_paths: list[Path] = [expected]
    for selected in getattr(automation, "file_dialog_selected_files", []):
        try:
            selected_path = Path(str(selected)).expanduser()
            if not selected_path.is_absolute():
                selected_path = expected.parent / selected_path
            raw_paths.append(selected_path.resolve())
        except (OSError, RuntimeError, ValueError):
            continue

    candidates: list[Path] = []

    def add(candidate: Path) -> None:
        if candidate not in candidates:
            candidates.append(candidate)

    for raw_path in raw_paths:
        add(raw_path)
        if raw_path.suffix.casefold() == ".png":
            add(raw_path.with_suffix(""))
            add(Path(str(raw_path) + ".png"))
        else:
            add(raw_path.with_suffix(".png"))
            add(Path(str(raw_path) + ".png"))
    try:
        for sibling in expected.parent.glob(f"{expected.stem}*"):
            if sibling.suffix.casefold() == ".png":
                add(sibling.resolve())
    except OSError:
        pass
    return candidates


def _wait_for_rfpro_exported_png(
    empro_module: Any,
    application: Any,
    output_path: Path,
    automation: Any,
) -> Path | None:
    """Pump RFPro until its dialog-selected PNG is completely materialized."""

    expected = output_path.expanduser().resolve()
    timeout_seconds = max(
        0.0, float(getattr(automation, "output_wait_seconds", 0.0))
    )
    deadline = time.monotonic() + timeout_seconds
    while True:
        for candidate in _rfpro_export_candidate_paths(expected, automation):
            try:
                if not candidate.is_file() or candidate.stat().st_size <= 0:
                    continue
                if candidate != expected:
                    if expected.exists():
                        raise FileExistsError(
                            f"Refusing to replace existing image: {expected}"
                        )
                    candidate.replace(expected)
                return expected
            except (FileNotFoundError, OSError):
                continue
        if time.monotonic() >= deadline:
            return None
        process_application_events = _getattr_or_default(
            application, "processEvents"
        )
        if callable(process_application_events):
            process_application_events()
        empro_module.gui.processEvents()
        time.sleep(0.025)


def export_geometry_view_png(
    empro_module: Any,
    application: Any,
    output_path: Path,
    automation_factory: Any = QtSaveDialogAutomation,
    qt_action_type: type[Any] | None = None,
) -> str:
    """Invoke RFPro's View > Export Image command and verify its PNG."""

    output_path = output_path.expanduser().resolve()
    if output_path.exists():
        raise FileExistsError(f"Refusing to replace existing image: {output_path}")
    project_view = empro_module.gui.activeProjectView()
    project_view.showGeometryView()
    geometry_view = project_view.geometryView()
    geometry_view.updateView()
    empro_module.gui.processEvents()
    action, description, owner_references = find_rfpro_export_image_action(
        project_view,
        application,
        qt_action_type=qt_action_type,
    )
    automation = automation_factory(application, output_path)
    automation.start()
    try:
        _action_trigger(action)
        exported_path = _wait_for_rfpro_exported_png(
            empro_module,
            application,
            output_path,
            automation,
        )
    finally:
        automation.stop()
    # Keep the QMenu/QAction owner chain alive until the blocking export and
    # its save dialog have completely returned.
    _ = owner_references
    empro_module.gui.processEvents()
    if exported_path is None:
        diagnostics = getattr(automation, "diagnostics", lambda: "unavailable")()
        candidates = ", ".join(
            str(path)
            for path in _rfpro_export_candidate_paths(output_path, automation)
        )
        raise RuntimeError(
            f"{description} was triggered, but RFPro did not create {output_path}. "
            f"Save-dialog diagnostics: {diagnostics}; checked paths={candidates}"
        )
    return description


def default_geometry_report_filename(analysis_name: str) -> str:
    """Build a portable default filename from the selected analysis name."""

    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", str(analysis_name)).strip("._-")
    return f"{stem or 'rfpro'}_geometry_validation.pdf"


def default_mesh_ports_report_filename(analysis_name: str) -> str:
    """Build a portable default filename for saved Mesh/Ports results."""

    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", str(analysis_name)).strip("._-")
    return f"{stem or 'rfpro'}_mesh_ports_validation.pdf"


def next_available_image_directory(pdf_path: Path) -> Path:
    """Choose a sibling image directory without replacing an older capture set."""

    base = pdf_path.with_name(f"{pdf_path.stem}_images")
    candidate = base
    suffix = 2
    while candidate.exists():
        candidate = base.with_name(f"{base.name}_{suffix}")
        suffix += 1
    return candidate


def remove_empty_image_directory(image_directory: Path | None) -> bool:
    """Remove a report image directory only when it contains no files."""

    if image_directory is None or not image_directory.is_dir():
        return False
    try:
        image_directory.rmdir()
    except OSError:
        return False
    return True


_REPORT_LENGTH_PATTERN = re.compile(
    r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    r"\s*([A-Za-z\u00b5\u03bc\"]*)\s*$"
)
_REPORT_LENGTH_TO_UM = {
    "": 1.0e6,
    "m": 1.0e6,
    "cm": 1.0e4,
    "mm": 1.0e3,
    "um": 1.0,
    "micron": 1.0,
    "microns": 1.0,
    "nm": 1.0e-3,
    "pm": 1.0e-6,
    "mil": 25.4,
    "mils": 25.4,
    "in": 25400.0,
    "inch": 25400.0,
    "inches": 25400.0,
    '"': 25400.0,
}


def geometry_report_value_micrometers(value: SweepValue) -> float:
    """Convert one evaluated length value to micrometers for the PDF."""

    display = str(value.display).replace("\u00b5", "u").replace("\u03bc", "u")
    match = _REPORT_LENGTH_PATTERN.fullmatch(display)
    if match is not None:
        unit = match.group(2).casefold()
        factor = _REPORT_LENGTH_TO_UM.get(unit)
        if factor is not None:
            scaled = float(match.group(1)) * factor
            if math.isfinite(scaled):
                return scaled
    try:
        reference_value = float(value.value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Geometry parameter {value.parameter_name!r} value "
            f"{value.display!r} could not be converted to um."
        ) from error
    scaled = reference_value * 1.0e6
    if not math.isfinite(scaled):
        raise ValueError(
            f"Geometry parameter {value.parameter_name!r} is not finite."
        )
    return scaled


def format_geometry_report_value(
    value: SweepValue,
    decimal_places: int = DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES,
) -> str:
    """Format one geometry length as a rounded, compact ASCII um value."""

    if (
        isinstance(decimal_places, bool)
        or not isinstance(decimal_places, int)
        or not 0 <= decimal_places <= 12
    ):
        raise ValueError(
            "PDF geometry decimal places must be an integer from 0 through 12."
        )
    scaled = geometry_report_value_micrometers(value)
    rounded = round(scaled, decimal_places)
    if rounded == 0:
        rounded = 0.0
    text = f"{rounded:.{decimal_places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return f"{text} um"


def parse_result_parameter_string(text: str) -> dict[str, str]:
    """Parse RFPro metadata such as ``W:1 mm, L:2 mm``."""

    parsed: dict[str, str] = {}
    for part in re.split(r"\s*[,;]\s*", str(text).strip()):
        if not part:
            continue
        separator = "=" if "=" in part else ":" if ":" in part else ""
        if not separator:
            continue
        name, value = part.split(separator, 1)
        name = name.strip()
        value = value.strip()
        if name and value:
            parsed[name] = value
    return parsed


def _coerce_result_parameter_mapping(raw: Any) -> dict[str, str]:
    if raw is None:
        return {}
    if isinstance(raw, str):
        return parse_result_parameter_string(raw)
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
        pairs = list(raw)
    except (TypeError, ValueError):
        return {}
    result: dict[str, str] = {}
    for item in pairs:
        if isinstance(item, (tuple, list)) and len(item) == 2:
            result[str(item[0])] = str(item[1])
            continue
        name = getattr(item, "name", None)
        value = getattr(item, "value", None)
        if name is not None and value is not None:
            result[str(name)] = str(value)
    return result


def simulation_result_parameters(metadata: Any) -> dict[str, str]:
    """Read public SimulationMetaData parameter accessors and display text."""

    mapping: dict[str, str] = {}
    for method_name in ("getParameterValues", "parameterValues"):
        method = getattr(metadata, method_name, None)
        if not callable(method):
            continue
        for arguments in ((), ("ValueAndFrontendUnit",)):
            try:
                candidate = _coerce_result_parameter_mapping(method(*arguments))
            except Exception:
                continue
            if candidate:
                mapping.update(candidate)
                break
    display = str(getattr(metadata, "parameterString", "") or "")
    for name, value in parse_result_parameter_string(display).items():
        mapping.setdefault(name, value)
    return mapping


def _normalized_parameter_text(value: Any) -> str:
    return re.sub(r"\s+", "", str(value)).casefold()


def _parameter_text_reference_value(value: Any) -> float | None:
    """Convert a simple length/result value to RFPro reference meters."""

    display = str(value).replace("\u00b5", "u").replace("\u03bc", "u")
    match = _REPORT_LENGTH_PATTERN.fullmatch(display)
    if match is None:
        return None
    unit = match.group(2).casefold()
    factor = _REPORT_LENGTH_TO_UM.get(unit)
    if factor is None:
        return None
    reference_value = float(match.group(1)) * factor / 1.0e6
    return reference_value if math.isfinite(reference_value) else None


def _sweep_value_matches_result(value: SweepValue, result_text: str) -> bool:
    if _normalized_parameter_text(value.display) == _normalized_parameter_text(
        result_text
    ):
        return True

    result_reference = _parameter_text_reference_value(result_text)
    if result_reference is None:
        return False
    point_reference = _parameter_text_reference_value(value.display)
    if point_reference is None:
        try:
            point_reference = float(value.value)
        except (TypeError, ValueError):
            point_reference = None
    if point_reference is None or not math.isfinite(point_reference):
        return False
    return math.isclose(
        point_reference,
        result_reference,
        rel_tol=1.0e-10,
        abs_tol=1.0e-15,
    )


def _matching_point_indices(
    parameters: Mapping[str, str], points: Sequence[SweepPoint]
) -> list[int]:
    """Return points whose complete value tuple matches result metadata."""

    if not parameters:
        return []
    values_by_name = {
        str(name).casefold(): str(value) for name, value in parameters.items()
    }
    matches: list[int] = []
    for point in points:
        if not point.values:
            continue
        if all(
            value.parameter_name.casefold() in values_by_name
            and _sweep_value_matches_result(
                value,
                values_by_name[value.parameter_name.casefold()],
            )
            for value in point.values
        ):
            matches.append(point.point_index)
    return matches


def find_mesh_ports_data(
    simulation_output: Any,
) -> tuple[str | None, Path | None, str]:
    """Find the saved OVM consumed by RFPro's public Mesh/Ports viewer."""

    raw_path = str(getattr(simulation_output, "simulationPath", "") or "").strip()
    if not raw_path:
        return None, None, "The saved simulation has no simulationPath."
    simulation_path = Path(raw_path).expanduser()
    candidates = (
        ("FEM", simulation_path / "emds_dsn" / "design", "options.xml"),
        ("Momentum", simulation_path / "work", "proj.opt"),
    )
    checked: list[str] = []
    for mesh_kind, result_directory, marker_name in candidates:
        marker = result_directory / marker_name
        checked.append(str(result_directory))
        if not marker.is_file():
            continue
        try:
            mesh_files = sorted(
                path for path in result_directory.rglob("*.ovm") if path.is_file()
            )
        except OSError as error:
            return (
                None,
                None,
                f"Could not inspect {mesh_kind} Mesh/Ports data: {error}",
            )
        if mesh_files:
            return mesh_kind, mesh_files[0], ""
    return (
        None,
        None,
        "No saved Mesh/Ports *.ovm was found under " + " or ".join(checked) + ".",
    )


def discover_mesh_ports_results(
    empro_module: Any,
    analysis: Any,
    points: Sequence[SweepPoint],
) -> MeshPortsInventory:
    """Map saved simulations to configured points without starting any jobs."""

    diagnostics: list[str] = []
    try:
        analysis_output = empro_module.output.AnalysisOutput(analysis)
        simulation_ids = [
            (value, str(value))
            for value in analysis_output.getAvailableSimulationIds()
        ]
    except Exception as error:
        return MeshPortsInventory(
            analysis_output=None,
            results_by_point=(),
            missing_point_indices=tuple(point.point_index for point in points),
            missing_mesh_point_indices=(),
            unmatched_result_ids=(),
            diagnostics=(f"Could not enumerate saved analysis results: {error}",),
        )

    results: list[MeshPortsResult] = []
    for raw_simulation_id, simulation_id in simulation_ids:
        try:
            simulation_output = analysis_output.getSimulation(raw_simulation_id)
        except Exception as error:
            diagnostics.append(
                f"Simulation {simulation_id} could not be loaded: {error}"
            )
            continue
        try:
            parameters = simulation_result_parameters(simulation_output.metadata())
        except Exception as error:
            parameters = {}
            diagnostics.append(
                f"Simulation {simulation_id} metadata could not be read: {error}"
            )
        mesh_kind, mesh_file, unavailable_reason = find_mesh_ports_data(
            simulation_output
        )
        results.append(
            MeshPortsResult(
                simulation_id=simulation_id,
                simulation_output=simulation_output,
                parameters=tuple(parameters.items()),
                mesh_kind=mesh_kind,
                mesh_file=mesh_file,
                unavailable_reason=unavailable_reason,
            )
        )

    assignments: dict[int, MeshPortsResult] = {}
    unmatched: list[MeshPortsResult] = []
    for result in results:
        parameters = dict(result.parameters)
        candidate_indices = [
            index
            for index in _matching_point_indices(parameters, points)
            if index not in assignments
        ]
        if candidate_indices:
            selected_index = candidate_indices[0]
            assignments[selected_index] = result
            if len(candidate_indices) > 1:
                diagnostics.append(
                    f"Simulation {result.simulation_id} matched duplicate parameter "
                    f"points; assigned it to point {selected_index + 1}."
                )
        else:
            unmatched.append(result)

    # RFPro preserves configured order when it returns a complete result set.
    # Use that complete-list behavior only for results whose metadata could not
    # establish a unique mapping. Never guess positions in a partial result set.
    if len(results) == len(points):
        still_unmatched: list[MeshPortsResult] = []
        result_positions = {id(result): index for index, result in enumerate(results)}
        for result in unmatched:
            point_index = points[result_positions[id(result)]].point_index
            if point_index not in assignments:
                assignments[point_index] = result
                diagnostics.append(
                    f"Simulation {result.simulation_id} was mapped to point "
                    f"{point_index + 1} by complete result order because its "
                    "parameter metadata was insufficient."
                )
            else:
                still_unmatched.append(result)
        unmatched = still_unmatched

    assigned_indices = set(assignments)
    missing_point_indices = tuple(
        point.point_index
        for point in points
        if point.point_index not in assigned_indices
    )
    missing_mesh_point_indices = tuple(
        point_index
        for point_index, result in assignments.items()
        if result.mesh_file is None or result.mesh_kind is None
    )
    return MeshPortsInventory(
        analysis_output=analysis_output,
        results_by_point=tuple(sorted(assignments.items())),
        missing_point_indices=missing_point_indices,
        missing_mesh_point_indices=tuple(sorted(missing_mesh_point_indices)),
        unmatched_result_ids=tuple(result.simulation_id for result in unmatched),
        diagnostics=tuple(diagnostics),
    )


def display_mesh_ports_result(
    empro_module: Any,
    result: MeshPortsResult,
    zoom_to_extents: bool = True,
) -> None:
    """Load one saved result through RFPro's Mesh/Ports geometry-view binding."""

    if result.mesh_kind is None or result.mesh_file is None:
        raise RuntimeError(
            result.unavailable_reason
            or f"Simulation {result.simulation_id} has no saved Mesh/Ports data."
        )
    project_view = empro_module.gui.activeProjectView()
    project_view.showGeometryView()
    empro_module.gui.processEvents()
    geometry_view = project_view.geometryView()
    method_name = (
        "displayFemMesh" if result.mesh_kind == "FEM" else "displayMomMesh"
    )
    display_method = getattr(geometry_view, method_name, None)
    if not callable(display_method):
        raise RuntimeError(
            f"RFPro's geometry view does not expose {method_name}() in this release."
        )
    display_method(result.simulation_output)
    empro_module.gui.processEvents()
    if zoom_to_extents:
        geometry_view.zoomGeometryViewToExtents()
        empro_module.gui.processEvents()


def mesh_ports_inventory_summary(
    inventory: MeshPortsInventory, total_point_count: int
) -> str:
    available = len(inventory.available_results())
    no_result = len(inventory.missing_point_indices)
    no_mesh = len(inventory.missing_mesh_point_indices)
    unmatched = len(inventory.unmatched_result_ids)
    return (
        f"Mesh/Ports available: {available}/{total_point_count}; "
        f"no matched saved result: {no_result}; "
        f"saved result without mesh: {no_mesh}; "
        f"unmatched saved results: {unmatched}"
    )


def mesh_ports_inventory_details(
    inventory: MeshPortsInventory, total_point_count: int
) -> str:
    """Build user-facing details without overwhelming RFPro message boxes."""

    lines = [mesh_ports_inventory_summary(inventory, total_point_count)]

    def point_list(indices: Sequence[int]) -> str:
        shown = [str(index + 1) for index in indices[:20]]
        if len(indices) > 20:
            shown.append(f"... ({len(indices) - 20} more)")
        return ", ".join(shown)

    if inventory.missing_point_indices:
        lines.append(
            "Points without a matched saved result: "
            + point_list(inventory.missing_point_indices)
        )
    if inventory.missing_mesh_point_indices:
        lines.append(
            "Points with a saved result but no Mesh/Ports data: "
            + point_list(inventory.missing_mesh_point_indices)
        )
    if inventory.unmatched_result_ids:
        lines.append(
            "Saved result IDs that could not be matched: "
            + ", ".join(inventory.unmatched_result_ids[:20])
        )
    if inventory.diagnostics:
        lines.append("Diagnostics: " + " | ".join(inventory.diagnostics[:5]))
    return "\n".join(lines)


def _geometry_report_page_html(
    analysis_name: str,
    page: GeometryReportPage,
    page_number: int,
    report_page_count: int,
    total_point_count: int,
    parameter_decimal_places: int = DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES,
    report_title: str = "RFPro Geometry Validation",
) -> str:
    """Render the wrapped metadata header used on one PDF page."""

    point = page.point
    parameters = " &nbsp; | &nbsp; ".join(
        f"<b>{html.escape(value.parameter_name)}</b>="
        f"{html.escape(format_geometry_report_value(value, parameter_decimal_places))}"
        for value in point.values
    ) or "(baseline parameters)"
    if page.valid is True:
        status_color = "#1b5e20"
        status = page.status_label or "Valid"
    elif page.valid is False:
        status_color = "#b71c1c"
        status = page.status_label or "INVALID"
    else:
        status_color = "#795500"
        status = page.status_label or "Automatic validity unavailable"
    details = page.message
    if page.capture_error:
        details += f" Capture: {page.capture_error}"

    return f"""
<style>
  body {{ font-family: sans-serif; font-size: 8.5pt; color: #202124; }}
  h1 {{ font-size: 15pt; margin: 0 0 3px 0; }}
  p {{ margin: 1px 0; }}
</style>
<h1>{html.escape(report_title)}</h1>
<p><b>Analysis:</b> {html.escape(str(analysis_name))}
   &nbsp;&nbsp; <b>Sweep point:</b> {point.point_index + 1} of {total_point_count}
   &nbsp;&nbsp; <b>Sequence:</b> {point.sequence_index + 1}
   &nbsp;&nbsp; <b>Combination:</b> {point.combination_index + 1}</p>
<p style="margin-top: 3px;"><b>Geometry parameters (um):</b> {parameters}</p>
<p style="color: {status_color}; margin-top: 3px;">
  <b>{html.escape(status)}:</b> {html.escape(details)}
</p>
""".strip()


def write_geometry_pdf_report(
    output_path: Path,
    analysis_name: str,
    pages: Sequence[GeometryReportPage],
    total_point_count: int,
    parameter_decimal_places: int = DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES,
    report_title: str = "RFPro Geometry Validation",
) -> None:
    """Create a fitted multi-page PDF using RFPro's existing PySide6 runtime."""

    if not pages:
        raise ValueError("At least one checked geometry point is required for a PDF.")

    from PySide6.QtCore import QRectF, QSizeF, Qt
    from PySide6.QtGui import (
        QColor,
        QImage,
        QPageLayout,
        QPageSize,
        QPainter,
        QPdfWriter,
        QTextDocument,
    )

    writer = QPdfWriter(str(output_path))
    writer.setCreator("ads-rfpro-csv-sweeps")
    writer.setTitle(f"{report_title} - {analysis_name}")
    writer.setResolution(150)
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.Letter))
    if not writer.setPageOrientation(QPageLayout.Orientation.Landscape):
        raise RuntimeError("Qt could not set the PDF report to landscape mode.")

    painter = QPainter()
    if not painter.begin(writer):
        raise RuntimeError(f"Qt could not create the PDF report at {output_path}.")
    try:
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        for page_index, report_page in enumerate(pages):
            if page_index and not writer.newPage():
                raise RuntimeError(
                    f"Qt could not start PDF page {page_index + 1}."
                )

            page_width = float(writer.width())
            page_height = float(writer.height())
            margin = float(writer.resolution()) * 0.22
            spacing = float(writer.resolution()) * 0.05
            footer_height = float(writer.resolution()) * 0.16
            content_width = page_width - 2.0 * margin

            header = QTextDocument()
            header.setHtml(
                _geometry_report_page_html(
                    analysis_name,
                    report_page,
                    page_index + 1,
                    len(pages),
                    total_point_count,
                    parameter_decimal_places,
                    report_title,
                )
            )
            header.setTextWidth(content_width)
            natural_header_height = float(header.size().height())
            maximum_header_height = page_height * 0.25
            header_scale = min(
                1.0, maximum_header_height / max(1.0, natural_header_height)
            )
            header_height = natural_header_height * header_scale
            painter.save()
            painter.translate(margin, margin)
            painter.scale(header_scale, header_scale)
            header.drawContents(
                painter,
                QRectF(
                    0.0,
                    0.0,
                    content_width,
                    natural_header_height,
                ),
            )
            painter.restore()

            image_top = margin + header_height + spacing
            image_height = max(
                float(writer.resolution()),
                page_height - image_top - margin - footer_height,
            )
            image_bounds = QRectF(margin, image_top, content_width, image_height)

            image = (
                QImage(str(report_page.image_path))
                if report_page.image_path is not None
                else QImage()
            )
            if not image.isNull():
                scaled_size = QSizeF(image.size())
                scaled_size.scale(
                    image_bounds.size(), Qt.AspectRatioMode.KeepAspectRatio
                )
                target = QRectF(
                    image_bounds.x()
                    + (image_bounds.width() - scaled_size.width()) / 2.0,
                    image_bounds.y()
                    + (image_bounds.height() - scaled_size.height()) / 2.0,
                    scaled_size.width(),
                    scaled_size.height(),
                )
                painter.drawImage(target, image)
            else:
                painter.setPen(QColor("#b71c1c"))
                painter.drawRect(image_bounds)
                painter.drawText(
                    image_bounds,
                    int(
                        Qt.AlignmentFlag.AlignCenter
                        | Qt.TextFlag.TextWordWrap
                    ),
                    report_page.capture_error
                    or "No geometry image was captured for this point.",
                )

            painter.setPen(QColor("#5f6368"))
            painter.drawText(
                QRectF(
                    margin,
                    page_height - margin - footer_height,
                    content_width,
                    footer_height,
                ),
                int(Qt.AlignmentFlag.AlignCenter),
                f"Point {report_page.point.point_index + 1} - "
                f"page {page_index + 1} of {len(pages)}",
            )
    finally:
        painter.end()

    if not output_path.is_file() or output_path.stat().st_size <= 0:
        raise RuntimeError(f"The PDF report was not written to {output_path}.")


def _status_text(valid: bool | None, message: str) -> str:
    if valid is True:
        return "Valid"
    if valid is False:
        return "INVALID: " + message
    return "Viewed; automatic validity unavailable"


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactively preview every geometry point in an RFPro analysis sweep."
    )
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS_NAME)
    parser.add_argument(
        "--zoom-to-extents",
        action="store_true",
        default=DEFAULT_ZOOM_TO_EXTENTS,
        help="fit the geometry view whenever a point is selected",
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


def create_inspector_dialog(
    empro_module: Any,
    project: Any,
    analysis: Any,
    points: Sequence[SweepPoint],
    baseline_formulas: dict[str, Any],
    zoom_to_extents: bool,
) -> Any:
    """Create a modeless dialog so RFPro's 3-D view remains interactive."""

    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QDialog,
        QFileDialog,
        QHBoxLayout,
        QLabel,
        QMessageBox,
        QProgressDialog,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
    )

    parameter_names = swept_parameter_names(points)

    class SweepGeometryInspector(QDialog):
        def __init__(self) -> None:
            super().__init__(None)
            self._restored = False
            self._applying = False
            self._active_view_text = "Geometry"
            self._mesh_inventory: MeshPortsInventory | None = None
            self._statuses: list[tuple[bool | None, str] | None] = [
                None for _ in points
            ]
            self.setWindowTitle(f"RFPro Sweep Geometry Inspector — {analysis.name}")
            self.resize(1100, 650)
            self.setWindowModality(Qt.WindowModality.NonModal)
            self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

            layout = QVBoxLayout(self)
            instructions = QLabel(
                "Select a row to apply that parameter combination to RFPro's active "
                "geometry view. Use Load Selected to explicitly regenerate the "
                "highlighted row; Fit View only fits the geometry already displayed. "
                "Load Mesh/Ports displays a matched saved simulation result. "
                "No simulation is created or queued. Original parameter formulas are "
                "restored when this window closes."
            )
            instructions.setWordWrap(True)
            layout.addWidget(instructions)

            geometry_column = 2 + len(parameter_names)
            mesh_ports_column = geometry_column + 1
            self._geometry_column = geometry_column
            self._mesh_ports_column = mesh_ports_column
            self.table = QTableWidget(len(points), 4 + len(parameter_names))
            self.table.setHorizontalHeaderLabels(
                ["Point", "Sequence", *parameter_names, "Geometry", "Mesh/Ports"]
            )
            self.table.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )
            self.table.setSelectionMode(
                QAbstractItemView.SelectionMode.SingleSelection
            )
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.table.setSortingEnabled(False)

            for row, point in enumerate(points):
                values_by_name = {
                    value.parameter_name: value.display for value in point.values
                }
                cells = [
                    str(point.point_index + 1),
                    str(point.sequence_index + 1),
                    *(values_by_name.get(name, "(baseline)") for name in parameter_names),
                    "Not checked",
                    "Scanning saved results...",
                ]
                for column, text in enumerate(cells):
                    item = QTableWidgetItem(text)
                    item.setToolTip(text)
                    self.table.setItem(row, column, item)

            self.table.resizeColumnsToContents()
            self.table.currentCellChanged.connect(self._selection_changed)
            layout.addWidget(self.table)

            controls = QHBoxLayout()
            self.previous_button = QPushButton("Previous")
            self.next_button = QPushButton("Next")
            self.load_selected_button = QPushButton("Load Selected")
            self.fit_button = QPushButton("Fit View")
            self.check_all_button = QPushButton("Check All")
            self.report_button = QPushButton("Check All + PDF")
            self.load_mesh_ports_button = QPushButton("Load Mesh/Ports")
            self.mesh_ports_report_button = QPushButton("Mesh/Ports PDF")
            close_button = QPushButton("Close and Restore")
            self.previous_button.clicked.connect(self._previous)
            self.next_button.clicked.connect(self._next)
            self.load_selected_button.clicked.connect(self._load_selected)
            self.fit_button.clicked.connect(self._fit_view)
            self.check_all_button.clicked.connect(self._check_all)
            self.report_button.clicked.connect(self._check_all_with_pdf)
            self.load_mesh_ports_button.clicked.connect(
                self._load_selected_mesh_ports
            )
            self.mesh_ports_report_button.clicked.connect(
                self._export_mesh_ports_with_pdf
            )
            close_button.clicked.connect(self.close)
            self.load_selected_button.setToolTip(
                "Regenerate and display the parameter combination in the highlighted row."
            )
            self.fit_button.setToolTip(
                "Fit the geometry currently displayed; this does not load a table row."
            )
            self.report_button.setToolTip(
                "Check every point, save one PNG per geometry, and create a PDF."
            )
            self.load_mesh_ports_button.setToolTip(
                "Display the selected condition's saved RFPro Mesh/Ports result; "
                "this never starts a simulation."
            )
            self.mesh_ports_report_button.setToolTip(
                "Export every available saved Mesh/Ports result to PNG and PDF; "
                "unsolved or missing-mesh conditions are skipped."
            )
            for button in (
                self.previous_button,
                self.next_button,
                self.load_selected_button,
                self.fit_button,
                self.check_all_button,
                self.report_button,
                self.load_mesh_ports_button,
                self.mesh_ports_report_button,
                close_button,
            ):
                controls.addWidget(button)
            controls.addStretch(1)
            layout.addLayout(controls)

            self.summary = QLabel()
            self.summary.setWordWrap(True)
            layout.addWidget(self.summary)

            self._refresh_mesh_ports_inventory()

            self.table.blockSignals(True)
            self.table.selectRow(0)
            self.table.blockSignals(False)
            self._apply_row(0)

        def _set_status(
            self, row: int, valid: bool | None, message: str
        ) -> None:
            self._statuses[row] = (valid, message)
            item = self.table.item(row, self._geometry_column)
            item.setText(_status_text(valid, message))
            item.setToolTip(message)
            if valid is True:
                item.setBackground(QColor("#c8e6c9"))
            elif valid is False:
                item.setBackground(QColor("#ffcdd2"))
            else:
                item.setBackground(QColor("#fff9c4"))
            self.table.resizeColumnToContents(self._geometry_column)
            self._update_summary(row)

        def _refresh_mesh_ports_inventory(self) -> MeshPortsInventory:
            inventory = discover_mesh_ports_results(
                empro_module,
                analysis,
                points,
            )
            self._mesh_inventory = inventory
            missing_mesh = set(inventory.missing_mesh_point_indices)
            for row, point in enumerate(points):
                result = inventory.result_for_point(point.point_index)
                item = self.table.item(row, self._mesh_ports_column)
                if result is None:
                    item.setText("No matched saved result")
                    item.setToolTip(
                        "No saved simulation could be safely matched to this "
                        "parameter condition."
                    )
                    item.setBackground(QColor("#eeeeee"))
                elif point.point_index in missing_mesh:
                    item.setText(f"Simulation {result.simulation_id}: no mesh")
                    item.setToolTip(result.unavailable_reason)
                    item.setBackground(QColor("#fff9c4"))
                else:
                    item.setText(
                        f"{result.mesh_kind} simulation {result.simulation_id}"
                    )
                    item.setToolTip(
                        f"Saved Mesh/Ports data: {result.mesh_file}"
                    )
                    item.setBackground(QColor("#c8e6c9"))
            self.table.resizeColumnToContents(self._mesh_ports_column)
            for diagnostic in inventory.diagnostics:
                print(f"Mesh/Ports inventory: {diagnostic}")
            current_row = self.table.currentRow()
            if current_row >= 0:
                self._update_summary(current_row)
            return inventory

        def _update_summary(self, current_row: int) -> None:
            checked = sum(status is not None for status in self._statuses)
            invalid = sum(
                status is not None and status[0] is False
                for status in self._statuses
            )
            point = points[current_row]
            values = ", ".join(
                f"{value.parameter_name}={value.display}" for value in point.values
            )
            self.summary.setText(
                f"Showing point {current_row + 1} of {len(points)}: {values}\n"
                f"Current view: {self._active_view_text}\n"
                f"Checked: {checked}/{len(points)}; invalid/errors: {invalid}\n"
                + (
                    mesh_ports_inventory_summary(
                        self._mesh_inventory,
                        len(points),
                    )
                    if self._mesh_inventory is not None
                    else "Mesh/Ports results have not been scanned."
                )
            )
            self.previous_button.setEnabled(current_row > 0)
            self.next_button.setEnabled(current_row + 1 < len(points))

        def _apply_row(
            self,
            row: int,
            force_fit: bool | None = None,
            log_native_status: bool = True,
        ) -> bool:
            if self._applying or row < 0 or row >= len(points):
                return False
            self._applying = True
            try:
                update_report = apply_sweep_point_to_geometry(
                    project, baseline_formulas, points[row]
                )
                empro_module.gui.processEvents()
                fit_view = zoom_to_extents if force_fit is None else force_fit
                refresh_geometry_view(empro_module, fit_view)
                self._active_view_text = "Geometry"
                valid, message = geometry_validity(project)
                self._set_status(row, valid, message)
                if log_native_status:
                    print(
                        f"Loaded geometry point {row + 1}: RFPro native update "
                        f"status={update_report['native_status']!r}."
                    )
                return True
            except Exception as error:
                message = f"Could not generate geometry: {error}"
                self._set_status(row, False, message)
                print(f"Point {row + 1}: {message}")
                return False
            finally:
                self._applying = False

        def _selection_changed(
            self, current_row: int, _current_column: int, _old_row: int, _old_column: int
        ) -> None:
            self._apply_row(current_row)

        def _previous(self) -> None:
            row = self.table.currentRow()
            if row > 0:
                self.table.selectRow(row - 1)

        def _next(self) -> None:
            row = self.table.currentRow()
            if row + 1 < len(points):
                self.table.selectRow(row + 1)

        def _load_selected(self) -> None:
            self._apply_row(max(0, self.table.currentRow()))

        def _load_selected_mesh_ports(self) -> None:
            row = max(0, self.table.currentRow())
            inventory = self._refresh_mesh_ports_inventory()
            result = inventory.result_for_point(points[row].point_index)
            if result is None:
                QMessageBox.information(
                    self,
                    "No saved Mesh/Ports result",
                    "No saved simulation could be safely matched to the selected "
                    "condition. The script did not start a simulation.",
                )
                return
            if result.mesh_file is None or result.mesh_kind is None:
                QMessageBox.information(
                    self,
                    "Mesh/Ports data unavailable",
                    result.unavailable_reason
                    or "The selected saved result contains no Mesh/Ports data.",
                )
                return
            try:
                display_mesh_ports_result(empro_module, result, True)
            except Exception as error:
                QMessageBox.warning(
                    self,
                    "Could not load Mesh/Ports result",
                    f"Simulation {result.simulation_id}: {error}",
                )
                return
            self._active_view_text = (
                f"{result.mesh_kind} Mesh/Ports - simulation {result.simulation_id}"
            )
            self._update_summary(row)
            print(
                f"Loaded point {row + 1} saved {result.mesh_kind} Mesh/Ports "
                f"result from simulation {result.simulation_id}."
            )

        def _fit_view(self) -> None:
            try:
                refresh_geometry_view(empro_module, True)
            except Exception as error:
                QMessageBox.warning(self, "Could not fit geometry view", str(error))

        def _check_all(self) -> None:
            self._run_check_all(None)

        def _check_all_with_pdf(self) -> None:
            selected_path, _selected_filter = QFileDialog.getSaveFileName(
                self,
                "Save RFPro Geometry Validation Report",
                default_geometry_report_filename(str(analysis.name)),
                "PDF files (*.pdf)",
            )
            if not selected_path:
                return
            pdf_path = Path(selected_path).expanduser().resolve()
            if pdf_path.suffix.casefold() != ".pdf":
                pdf_path = pdf_path.with_suffix(".pdf")
            self._run_check_all(pdf_path)

        def _export_mesh_ports_with_pdf(self) -> None:
            selected_path, _selected_filter = QFileDialog.getSaveFileName(
                self,
                "Save RFPro Mesh/Ports Validation Report",
                default_mesh_ports_report_filename(str(analysis.name)),
                "PDF files (*.pdf)",
            )
            if not selected_path:
                return
            pdf_path = Path(selected_path).expanduser().resolve()
            if pdf_path.suffix.casefold() != ".pdf":
                pdf_path = pdf_path.with_suffix(".pdf")
            self._run_mesh_ports_export(pdf_path)

        def _run_mesh_ports_export(self, pdf_path: Path) -> None:
            selected_row = max(0, self.table.currentRow())
            inventory = self._refresh_mesh_ports_inventory()
            available_results = inventory.available_results()
            if not available_results:
                QMessageBox.information(
                    self,
                    "No Mesh/Ports data available",
                    mesh_ports_inventory_details(inventory, len(points))
                    + "\n\nNo simulation was started.",
                )
                return

            image_directory = next_available_image_directory(pdf_path)
            try:
                image_directory.mkdir(parents=True, exist_ok=False)
            except Exception as error:
                QMessageBox.warning(
                    self,
                    "Could not create Mesh/Ports image directory",
                    str(error),
                )
                return

            pages_by_index = {point.point_index: point for point in points}
            report_pages: list[GeometryReportPage] = []
            exported_image_count = 0
            export_failure = ""
            progress = QProgressDialog(
                "Loading and exporting available saved Mesh/Ports results...",
                "Cancel",
                0,
                len(available_results),
                self,
            )
            progress.setWindowTitle("RFPro Mesh/Ports Export")
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setMinimumDuration(0)
            for export_index, (point_index, result) in enumerate(available_results):
                if progress.wasCanceled():
                    break
                point = pages_by_index[point_index]
                progress.setLabelText(
                    f"Loading point {point_index + 1} Mesh/Ports result "
                    f"({export_index + 1} of {len(available_results)})..."
                )
                progress.setValue(export_index)
                empro_module.gui.processEvents()
                safe_simulation_id = re.sub(
                    r"[^A-Za-z0-9._-]+", "_", result.simulation_id
                ).strip("._-") or "result"
                image_path = image_directory / (
                    f"point_{point_index + 1:04d}_simulation_"
                    f"{safe_simulation_id}_mesh_ports.png"
                )
                try:
                    display_mesh_ports_result(empro_module, result, True)
                    self._active_view_text = (
                        f"{result.mesh_kind} Mesh/Ports - simulation "
                        f"{result.simulation_id}"
                    )
                    export_method = export_geometry_view_png(
                        empro_module,
                        QApplication.instance(),
                        image_path,
                    )
                except Exception as error:
                    export_failure = (
                        f"Point {point_index + 1}, simulation "
                        f"{result.simulation_id}, could not be exported from "
                        f"RFPro's Mesh/Ports view:\n{error}"
                    )
                    print(export_failure)
                    break
                exported_image_count += 1
                print(
                    f"Exported point {point_index + 1} {result.mesh_kind} "
                    f"Mesh/Ports via {export_method}: {image_path}"
                )
                report_pages.append(
                    GeometryReportPage(
                        point=point,
                        valid=True,
                        message=(
                            f"Saved simulation {result.simulation_id}; "
                            f"{result.mesh_kind} Mesh/Ports result."
                        ),
                        image_path=image_path,
                        status_label="Mesh/Ports loaded",
                    )
                )

            if not progress.wasCanceled():
                progress.setValue(len(available_results))
            else:
                progress.close()

            self.table.blockSignals(True)
            self.table.selectRow(selected_row)
            self.table.blockSignals(False)
            self._apply_row(selected_row)

            if export_failure:
                removed_empty_directory = (
                    exported_image_count == 0
                    and remove_empty_image_directory(image_directory)
                )
                image_note = (
                    "No PNG images were exported; the empty image directory "
                    "was removed."
                    if removed_empty_directory
                    else f"Successfully exported PNG files remain in:\n{image_directory}"
                )
                QMessageBox.warning(
                    self,
                    "RFPro Mesh/Ports export failed",
                    export_failure
                    + "\n\nNo PDF was created because every PDF page must "
                    "have its verified RFPro-exported PNG.\n\n"
                    + image_note,
                )
                return
            if not report_pages:
                remove_empty_image_directory(image_directory)
                return
            try:
                write_geometry_pdf_report(
                    pdf_path,
                    str(analysis.name),
                    report_pages,
                    len(points),
                    report_title="RFPro Mesh/Ports Validation",
                )
            except Exception as error:
                QMessageBox.warning(
                    self,
                    "Could not create Mesh/Ports PDF",
                    f"{error}\n\nCaptured PNG files remain in:\n{image_directory}",
                )
                return

            completion = (
                f"Created {len(report_pages)} Mesh/Ports PDF page(s) from "
                f"{len(available_results)} available saved result(s).\n\n"
                f"PDF:\n{pdf_path}\n\nPNG images:\n{image_directory}\n\n"
                + mesh_ports_inventory_details(inventory, len(points))
                + "\n\nNo simulation was started."
            )
            if progress.wasCanceled():
                completion = (
                    "The export was canceled; a partial report was saved.\n\n"
                    + completion
                )
            QMessageBox.information(
                self,
                "Mesh/Ports report created",
                completion,
            )

        def _run_check_all(self, pdf_path: Path | None) -> None:
            selected_row = max(0, self.table.currentRow())
            image_directory = (
                next_available_image_directory(pdf_path)
                if pdf_path is not None
                else None
            )
            if image_directory is not None:
                try:
                    image_directory.mkdir(parents=True, exist_ok=False)
                except Exception as error:
                    QMessageBox.warning(
                        self,
                        "Could not create report image directory",
                        str(error),
                    )
                    return

            report_pages: list[GeometryReportPage] = []
            exported_image_count = 0
            export_failure = ""
            progress = QProgressDialog(
                (
                    "Generating, checking, and exporting every geometry point..."
                    if pdf_path is not None
                    else "Generating and checking every geometry point..."
                ),
                "Cancel",
                0,
                len(points),
                self,
            )
            progress.setWindowTitle("RFPro Sweep Geometry Check")
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setMinimumDuration(0)
            for row in range(len(points)):
                if progress.wasCanceled():
                    break
                progress.setLabelText(
                    f"Generating point {row + 1} of {len(points)}..."
                )
                progress.setValue(row)
                empro_module.gui.processEvents()
                generated = self._apply_row(
                    row,
                    force_fit=True if pdf_path is not None else None,
                    log_native_status=False,
                )
                if pdf_path is not None:
                    status = self._statuses[row]
                    assert status is not None
                    valid, message = status
                    if generated:
                        assert image_directory is not None
                        image_path = image_directory / f"point_{row + 1:04d}.png"
                        try:
                            export_method = export_geometry_view_png(
                                empro_module,
                                QApplication.instance(),
                                image_path,
                            )
                            exported_image_count += 1
                            print(
                                f"Exported point {row + 1} via "
                                f"{export_method}: {image_path}"
                            )
                        except Exception as error:
                            export_failure = (
                                f"Point {row + 1} could not be exported through "
                                f"RFPro's View > Export Image command:\n{error}"
                            )
                            print(export_failure)
                            break
                    else:
                        export_failure = (
                            f"Point {row + 1} geometry generation failed; RFPro's "
                            "Export Image command was not invoked."
                        )
                        print(export_failure)
                        break
                    report_pages.append(
                        GeometryReportPage(
                            point=points[row],
                            valid=valid,
                            message=message,
                            image_path=image_path,
                        )
                    )
            if not progress.wasCanceled():
                progress.setValue(len(points))
            else:
                progress.close()
            self.table.blockSignals(True)
            self.table.selectRow(selected_row)
            self.table.blockSignals(False)
            self._apply_row(selected_row)

            if pdf_path is None:
                return
            if export_failure:
                removed_empty_directory = (
                    exported_image_count == 0
                    and remove_empty_image_directory(image_directory)
                )
                image_note = (
                    "No PNG images were exported; the empty image directory "
                    "was removed."
                    if removed_empty_directory
                    else f"Successfully exported PNG files remain in:\n{image_directory}"
                )
                QMessageBox.warning(
                    self,
                    "RFPro image export failed",
                    export_failure
                    + "\n\nNo PDF was created because every PDF page must have "
                    "its verified RFPro-exported PNG.\n\n"
                    + image_note,
                )
                return
            if not report_pages:
                remove_empty_image_directory(image_directory)
                return
            try:
                write_geometry_pdf_report(
                    pdf_path,
                    str(analysis.name),
                    report_pages,
                    len(points),
                )
            except Exception as error:
                removed_empty_directory = (
                    exported_image_count == 0
                    and remove_empty_image_directory(image_directory)
                )
                image_note = (
                    "No geometry images were exported; the empty image "
                    "directory was removed."
                    if removed_empty_directory
                    else f"Captured PNG files remain in:\n{image_directory}"
                )
                QMessageBox.warning(
                    self,
                    "Could not create geometry PDF",
                    f"{error}\n\n{image_note}",
                )
                return

            removed_empty_directory = (
                exported_image_count == 0
                and remove_empty_image_directory(image_directory)
            )
            image_note = (
                "No PNG images were exported; the empty image directory was removed."
                if removed_empty_directory
                else f"PNG images:\n{image_directory}"
            )
            completion = (
                f"Created {len(report_pages)} PDF page(s) from "
                f"{len(points)} sweep point(s).\n\n"
                f"PDF:\n{pdf_path}\n\n{image_note}"
            )
            if progress.wasCanceled():
                completion = (
                    "The check was canceled; a partial report was saved.\n\n"
                    + completion
                )
            QMessageBox.information(
                self, "Geometry report created", completion
            )

        def restore_original_parameters(self) -> None:
            if self._restored:
                return
            self._restored = True
            try:
                update_report = restore_parameter_formulas_and_geometry(
                    project, baseline_formulas
                )
                empro_module.gui.processEvents()
                refresh_geometry_view(empro_module, zoom_to_extents)
                print(
                    "Restored original RFPro project-parameter formulas and "
                    "geometry: native update status="
                    f"{update_report['native_status']!r}."
                )
            except Exception as error:
                print(f"WARNING: could not restore original parameter formulas: {error}")

        def closeEvent(self, event: Any) -> None:
            self.restore_original_parameters()
            event.accept()

    return SweepGeometryInspector()


def _close_existing_inspectors(application: Any) -> None:
    """Restore and close a prior inspector before capturing a new baseline."""

    existing_dialogs = list(
        getattr(application, _INSPECTOR_REGISTRY_ATTRIBUTE, [])
    )
    for existing in existing_dialogs:
        try:
            existing.close()
        except Exception as error:
            print(f"WARNING: could not close an existing geometry inspector: {error}")
    application.processEvents()


def _show_modeless(application: Any, dialog: Any) -> None:
    """Keep the inspector alive on RFPro's persistent QApplication object."""

    registry = list(getattr(application, _INSPECTOR_REGISTRY_ATTRIBUTE, []))
    registry.append(dialog)
    setattr(application, _INSPECTOR_REGISTRY_ATTRIBUTE, registry)

    def remove_dialog(*_arguments: Any) -> None:
        current = list(
            getattr(application, _INSPECTOR_REGISTRY_ATTRIBUTE, [])
        )
        if dialog in current:
            current.remove(dialog)
            setattr(application, _INSPECTOR_REGISTRY_ATTRIBUTE, current)

    dialog.destroyed.connect(remove_dialog)
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    qt_runtime = create_or_reuse_qapplication()
    _print_qt_diagnostics(qt_runtime)
    _close_existing_inspectors(qt_runtime.application)

    # RFPro owns the active project and the 3-D view used by this inspector.
    import empro

    project = empro.activeProject
    analysis = _choose_analysis(project, arguments.analysis)
    settings = analysis.simulationSettings
    points = expand_parameter_sequences(settings)
    names = swept_parameter_names(points)
    baseline_formulas = snapshot_parameter_formulas(project, names)

    configured_count = int(settings.numberOfParameterInstances)
    if configured_count != len(points):
        print(
            "WARNING: Python expansion produced "
            f"{len(points)} point(s), while RFPro reports {configured_count}. "
            "Review the table before relying on the inspector."
        )

    print(
        f"Opening geometry inspector for analysis {analysis.name!r}: "
        f"{len(points)} point(s), {len(names)} swept parameter(s)."
    )
    try:
        dialog = create_inspector_dialog(
            empro,
            project,
            analysis,
            points,
            baseline_formulas,
            arguments.zoom_to_extents,
        )
        _show_modeless(qt_runtime.application, dialog)
    except Exception:
        try:
            restore_parameter_formulas_and_geometry(project, baseline_formulas)
            empro.gui.processEvents()
            refresh_geometry_view(empro, arguments.zoom_to_extents)
        except Exception as restore_error:
            print(
                "WARNING: the inspector failed to open and the original parameter "
                f"formulas could not be fully restored: {restore_error}"
            )
        raise


if __name__ == "__main__":
    main()
