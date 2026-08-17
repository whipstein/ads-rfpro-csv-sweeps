"""Export RFPro swept S-parameter results to generic MDIF.

Run this file inside the open RFPro project after the selected analysis has
results.  One ``ACDATA`` block is written per available simulation/geometry
case, with RFPro parameter metadata emitted as MDIF ``VAR`` values.

The Qt bootstrap is intentionally self-contained.  RFPro's QApplication is
reused without changing environment or library paths.  A temporary, restored
platform-plugin redirect is used only if a standalone launcher owns no app.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_OUTPUT_PATH = ""
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_PARAMETER_NAMES = ""  # Comma-separated; empty exports all metadata.
DEFAULT_REFERENCE_IMPEDANCE_OHMS = 50.0
DEFAULT_FREQUENCY_MODE = "ask"  # One of: ask, native, points, step.
DEFAULT_FREQUENCY_POINTS = 1000
DEFAULT_FREQUENCY_STEP = "1 GHz"
MAX_FREQUENCY_POINTS = 1_000_000


@dataclass(frozen=True)
class QtRuntime:
    application: Any
    pyside_file: Path
    plugin_file: Path | None
    application_was_created: bool
    environment_was_restored: bool


@dataclass(frozen=True)
class MDIFBlock:
    simulation_id: str
    parameters: tuple[tuple[str, str], ...]
    frequencies_hz: tuple[float, ...]
    labels: tuple[str, ...]
    values: tuple[tuple[complex, ...], ...]


@dataclass(frozen=True)
class FrequencyGridRequest:
    """Requested MDIF frequency sampling across each result's native span."""

    mode: str
    point_count: int | None = None
    step_hz: float | None = None


@dataclass(frozen=True)
class FrequencyRegion:
    """One enabled frequency-plan region from the selected RFPro analysis."""

    start_hz: float
    stop_hz: float


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
        "Export RFPro Analysis MDIF",
        "Analysis:",
        names,
        0,
        False,
    )
    if not accepted:
        raise RuntimeError("Analysis selection was cancelled.")
    return find_analysis(project, str(selected))


def _choose_output_path(configured_path: str, analysis_name: str) -> Path:
    if configured_path:
        return Path(configured_path).expanduser().resolve()

    from PySide6.QtWidgets import QFileDialog

    default_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", analysis_name).strip("_")
    selected, _ = QFileDialog.getSaveFileName(
        None,
        "Export RFPro analysis as MDIF",
        f"{default_name or 'rfpro_analysis'}.mdif",
        "MDIF files (*.mdif *.mdf);;All files (*)",
    )
    if not selected:
        raise RuntimeError("MDIF export was cancelled.")
    return Path(selected).expanduser().resolve()


def parse_parameter_string(text: str) -> dict[str, str]:
    """Parse RFPro's display metadata such as ``W:1 mm, L:2 mm``."""

    parsed: dict[str, str] = {}
    for part in re.split(r"\s*[,;]\s*", text.strip()):
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


def _coerce_parameter_mapping(raw: Any) -> dict[str, str]:
    if raw is None:
        return {}
    if isinstance(raw, str):
        return parse_parameter_string(raw)
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


def simulation_parameters(metadata: Any) -> dict[str, str]:
    """Read public SimulationMetaData methods with a display-string fallback."""

    mapping: dict[str, str] = {}
    for method_name in ("getParameterValues", "parameterValues"):
        method = getattr(metadata, method_name, None)
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
    display = str(getattr(metadata, "parameterString", "") or "")
    for name, value in parse_parameter_string(display).items():
        mapping.setdefault(name, value)
    return mapping


def _sweep_values(sweep: Any) -> list[str]:
    getter = getattr(sweep, "getParameterValues", None)
    if callable(getter):
        for arguments in (("ValueAndFrontendUnit",), ()):
            try:
                values = [str(value) for value in getter(*arguments)]
            except Exception:
                continue
            if values:
                return values
    values = getattr(sweep, "parameterValues", None)
    if values is not None:
        try:
            result = [str(value) for value in values]
        except TypeError:
            result = []
        if result:
            return result
    raise RuntimeError(f"Could not read values for sweep {sweep.parameterName!r}.")


def configured_parameter_cases(settings: Any) -> list[dict[str, str]]:
    """Expand each independent native ParameterSequence in RFPro order."""

    cases: list[dict[str, str]] = []
    for sequence in settings.parameterSequences:
        names: list[str] = []
        value_lists: list[list[str]] = []
        for sweep in sequence:
            names.append(str(sweep.parameterName))
            value_lists.append(_sweep_values(sweep))
        if not names:
            continue
        for combination in itertools.product(*value_lists):
            cases.append(dict(zip(names, combination)))
    return cases


def _positive_port_number(value: Any) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Unsupported RFPro port index {value!r}.") from error
    if number <= 0:
        raise ValueError(f"RFPro port indices must be positive: {number}.")
    return number


def _sparameter_label(row: int, column: int) -> str:
    if row < 10 and column < 10:
        return f"S{row}{column}"
    return f"S[{row},{column}]"


def smatrix_to_block(
    smatrix: Any,
    simulation_id: str,
    parameters: Mapping[str, str],
) -> MDIFBlock:
    """Convert a public ``DataSetMatrix`` into a generic MDIF block."""

    rows = sorted(_positive_port_number(value) for value in smatrix.rows)
    columns = sorted(_positive_port_number(value) for value in smatrix.cols)
    if rows != columns:
        raise ValueError(
            f"Simulation {simulation_id}: S-matrix is not square "
            f"(rows={rows}, columns={columns})."
        )

    matrix_entries: list[tuple[str, Any]] = []
    for row in rows:
        for column in columns:
            if (row, column) not in smatrix:
                raise ValueError(
                    f"Simulation {simulation_id}: S[{row},{column}] is missing."
                )
            matrix_entries.append((_sparameter_label(row, column), smatrix[row, column]))
    if not matrix_entries:
        raise ValueError(f"Simulation {simulation_id}: S-matrix is empty.")

    first_dataset = matrix_entries[0][1]
    dimensions = list(first_dataset.dimensions())
    if len(dimensions) != 1:
        raise ValueError(
            f"Simulation {simulation_id}: expected one frequency dimension, "
            f"found {len(dimensions)}."
        )
    point_count = len(first_dataset)
    if point_count == 0:
        raise ValueError(f"Simulation {simulation_id}: S-parameter data is empty.")
    frequency_dimension = dimensions[0]
    frequencies = tuple(float(frequency_dimension.at(index)) for index in range(point_count))

    labels = tuple(label for label, _ in matrix_entries)
    columns_of_values: list[tuple[complex, ...]] = []
    for label, dataset in matrix_entries:
        if len(dataset) != point_count:
            raise ValueError(
                f"Simulation {simulation_id}: {label} has {len(dataset)} points, "
                f"expected {point_count}."
            )
        dataset_dimensions = list(dataset.dimensions())
        if len(dataset_dimensions) != 1:
            raise ValueError(
                f"Simulation {simulation_id}: {label} is not one-dimensional."
            )
        dataset_frequencies = tuple(
            float(dataset_dimensions[0].at(index)) for index in range(point_count)
        )
        if dataset_frequencies != frequencies:
            raise ValueError(
                f"Simulation {simulation_id}: {label} uses a different frequency grid."
            )
        columns_of_values.append(
            tuple(complex(dataset.at(index)) for index in range(point_count))
        )

    rows_of_values = tuple(
        tuple(column[index] for column in columns_of_values)
        for index in range(point_count)
    )
    for frequency, row_values in zip(frequencies, rows_of_values):
        if not math.isfinite(frequency):
            raise ValueError(
                f"Simulation {simulation_id}: frequency is not finite: {frequency}."
            )
        if any(
            not math.isfinite(value.real) or not math.isfinite(value.imag)
            for value in row_values
        ):
            raise ValueError(
                f"Simulation {simulation_id}: S-parameter data contains NaN or infinity."
            )

    return MDIFBlock(
        simulation_id=str(simulation_id),
        parameters=tuple((str(name), str(value)) for name, value in parameters.items()),
        frequencies_hz=frequencies,
        labels=labels,
        values=rows_of_values,
    )


_FREQUENCY_VALUE = re.compile(
    r"^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*"
    r"(Hz|kHz|MHz|GHz|THz)?\s*$",
    re.IGNORECASE,
)
_FREQUENCY_MULTIPLIERS = {
    "hz": 1.0,
    "khz": 1.0e3,
    "mhz": 1.0e6,
    "ghz": 1.0e9,
    "thz": 1.0e12,
}


def parse_frequency_step(value: str | float | int) -> float:
    """Parse an export frequency step; a unitless value is interpreted as Hz."""

    match = _FREQUENCY_VALUE.fullmatch(str(value))
    if match is None:
        raise ValueError(
            "Frequency step must be a number optionally followed by Hz, kHz, "
            "MHz, GHz, or THz."
        )
    magnitude = float(match.group(1))
    unit = (match.group(2) or "Hz").casefold()
    step_hz = magnitude * _FREQUENCY_MULTIPLIERS[unit]
    if not math.isfinite(step_hz) or step_hz <= 0:
        raise ValueError("Frequency step must be a positive finite value.")
    return step_hz


def validate_frequency_grid_request(request: FrequencyGridRequest) -> FrequencyGridRequest:
    mode = request.mode.casefold()
    if mode == "native":
        return FrequencyGridRequest("native")
    if mode == "points":
        if request.point_count is None or not 2 <= request.point_count <= MAX_FREQUENCY_POINTS:
            raise ValueError(
                "Frequency point count must be between 2 and "
                f"{MAX_FREQUENCY_POINTS:,}."
            )
        return FrequencyGridRequest("points", point_count=request.point_count)
    if mode == "step":
        if request.step_hz is None or not math.isfinite(request.step_hz):
            raise ValueError("A positive finite frequency step is required.")
        if request.step_hz <= 0:
            raise ValueError("Frequency step must be a positive finite value.")
        return FrequencyGridRequest("step", step_hz=request.step_hz)
    raise ValueError(f"Unsupported frequency-grid mode: {request.mode!r}.")


def frequency_grid_description(request: FrequencyGridRequest) -> str:
    request = validate_frequency_grid_request(request)
    if request.mode == "native":
        return "native result frequencies"
    if request.mode == "points":
        return (
            f"{request.point_count:,} uniformly spaced points per configured range "
            "(configured single points retained)"
        )
    return (
        f"{request.step_hz:.16g} Hz maximum step per configured range "
        "(configured single points retained)"
    )


def _frequency_plan_attribute_text(plan: Any, name: str) -> str:
    """Return a printable frequency-plan attribute without requiring it."""

    try:
        value = getattr(plan, name)
    except Exception:
        return ""
    return str(value).strip()


def configured_frequency_regions(settings: Any) -> tuple[FrequencyRegion, ...]:
    """Read and normalize enabled FEM frequency plans from an analysis."""

    plan_list_method = getattr(settings, "femFrequencyPlanList", None)
    if not callable(plan_list_method):
        raise RuntimeError(
            "The selected analysis does not expose femFrequencyPlanList()."
        )
    try:
        plans = list(plan_list_method())
    except Exception as error:
        raise RuntimeError(
            f"Could not read the selected analysis frequency plans: {error}"
        ) from error

    regions: list[FrequencyRegion] = []
    for index, plan in enumerate(plans):
        if not bool(getattr(plan, "enabled", True)):
            print(f"Frequency plan {index + 1}: enabled=False; ignored.")
            continue

        sweep_type = _frequency_plan_attribute_text(plan, "sweepType")
        legacy_type = _frequency_plan_attribute_text(plan, "type")
        compute_type = _frequency_plan_attribute_text(plan, "computeType")
        is_single = any(
            "single" in value.casefold()
            for value in (sweep_type, legacy_type)
            if value
        )

        try:
            start_hz = float(plan.startFrequency)
        except Exception as error:
            raise ValueError(
                f"Enabled frequency plan {index + 1} has an unreadable start "
                f"frequency: {error}"
            ) from error
        try:
            raw_stop_hz: float | None = float(plan.stopFrequency)
            raw_stop_description = f"{raw_stop_hz:.16g}"
        except Exception as error:
            raw_stop_hz = None
            raw_stop_description = f"unreadable ({error})"
            if not is_single:
                raise ValueError(
                    f"Enabled frequency plan {index + 1} has an unreadable stop "
                    f"frequency: {error}"
                ) from error

        # RFPro's Single plan only uses startFrequency. Its stopFrequency may
        # retain a stale value from another plan or a prior edit and must not
        # be interpreted as an additional export range.
        stop_hz = start_hz if is_single else raw_stop_hz
        assert stop_hz is not None

        if not math.isfinite(start_hz) or not math.isfinite(stop_hz):
            raise ValueError(
                f"Enabled frequency plan {index + 1} has a non-finite endpoint."
            )
        if start_hz < 0.0 or stop_hz < 0.0:
            raise ValueError(
                f"Enabled frequency plan {index + 1} has a negative endpoint."
            )
        if stop_hz < start_hz:
            raise ValueError(
                f"Enabled frequency plan {index + 1} stops below its start "
                f"({start_hz:.16g} Hz > {stop_hz:.16g} Hz)."
            )

        effective_description = (
            f"{start_hz:.16g} Hz"
            if start_hz == stop_hz
            else f"{start_hz:.16g}..{stop_hz:.16g} Hz"
        )
        print(
            f"Frequency plan {index + 1}: enabled=True, "
            f"sweepType={sweep_type or '(unavailable)'!r}, "
            f"type={legacy_type or '(unavailable)'!r}, "
            f"computeType={compute_type or '(unavailable)'!r}, "
            f"raw={start_hz:.16g}..{raw_stop_description} Hz, "
            f"effective={effective_description}."
        )
        regions.append(FrequencyRegion(start_hz, stop_hz))

    if not regions:
        raise RuntimeError(
            "The selected analysis has no enabled FEM frequency plans."
        )

    normalized: list[FrequencyRegion] = []
    for region in sorted(regions, key=lambda item: (item.start_hz, item.stop_hz)):
        if not normalized or region != normalized[-1]:
            normalized.append(region)
    return tuple(normalized)


def frequency_regions_description(regions: Sequence[FrequencyRegion]) -> str:
    descriptions = []
    for region in regions:
        if region.start_hz == region.stop_hz:
            descriptions.append(f"{region.start_hz:.16g} Hz")
        else:
            descriptions.append(
                f"{region.start_hz:.16g}..{region.stop_hz:.16g} Hz"
            )
    return ", ".join(descriptions)


def _grid_by_point_count(start: float, stop: float, point_count: int) -> list[float]:
    denominator = point_count - 1
    span = stop - start
    grid = [
        start + span * index / denominator
        for index in range(point_count)
    ]
    grid[-1] = stop
    return grid


def _grid_by_step(start: float, stop: float, step_hz: float) -> list[float]:
    span = stop - start
    quotient = span / step_hz
    if not math.isfinite(quotient) or quotient > MAX_FREQUENCY_POINTS:
        raise ValueError(
            "The requested frequency step would exceed the safety limit of "
            f"{MAX_FREQUENCY_POINTS:,} points in one configured range."
        )
    nearest_integer = round(quotient)
    exact_multiple = nearest_integer >= 1 and math.isclose(
        quotient,
        nearest_integer,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    full_intervals = nearest_integer if exact_multiple else math.floor(quotient)
    point_count = int(full_intervals) + 1 + (0 if exact_multiple else 1)
    if point_count > MAX_FREQUENCY_POINTS:
        raise ValueError(
            f"The requested frequency step would create {point_count:,} points "
            f"in one configured range; the safety limit is {MAX_FREQUENCY_POINTS:,}."
        )
    grid = [start + index * step_hz for index in range(int(full_intervals) + 1)]
    if exact_multiple:
        grid[-1] = stop
    else:
        grid.append(stop)
    return grid


def build_frequency_grid(
    native_frequencies_hz: Sequence[float],
    request: FrequencyGridRequest,
    configured_regions: Sequence[FrequencyRegion] | None = None,
) -> tuple[float, ...]:
    """Build a grid within the selected analysis's configured frequency plans."""

    native = tuple(float(value) for value in native_frequencies_hz)
    if not native:
        raise ValueError("S-parameter data is empty.")
    if any(not math.isfinite(value) for value in native):
        raise ValueError("Native frequency data contains NaN or infinity.")

    request = validate_frequency_grid_request(request)
    if request.mode == "native":
        return native

    if not configured_regions:
        raise ValueError(
            "Configured analysis frequency regions are required for resampling."
        )

    frequencies: list[float] = []
    for region in configured_regions:
        start = float(region.start_hz)
        stop = float(region.stop_hz)
        if start == stop:
            region_grid = [start]
        elif request.mode == "points":
            assert request.point_count is not None
            region_grid = _grid_by_point_count(start, stop, request.point_count)
        else:
            assert request.step_hz is not None
            region_grid = _grid_by_step(start, stop, request.step_hz)

        prospective_count = len(frequencies) + len(region_grid)
        if prospective_count > MAX_FREQUENCY_POINTS:
            raise ValueError(
                f"The configured plans would export at least {prospective_count:,} "
                "points; "
                f"the safety limit is {MAX_FREQUENCY_POINTS:,}."
            )
        frequencies.extend(region_grid)
    return tuple(sorted(set(frequencies)))


def circuit_matrix_to_block(
    circuit_matrix: Any,
    simulation_id: str,
    parameters: Mapping[str, str],
    frequency_grid_request: FrequencyGridRequest | None = None,
    configured_regions: Sequence[FrequencyRegion] | None = None,
) -> MDIFBlock:
    """Convert a file-backed RFPro ``CircuitMatrix`` into an MDIF block."""

    port_count = int(circuit_matrix.numberOfPorts())
    if port_count <= 0:
        raise ValueError(f"Simulation {simulation_id}: S-matrix has no ports.")

    frequency_dataset = circuit_matrix.frequencies()
    native_frequencies = tuple(float(value) for value in frequency_dataset.data)
    try:
        frequencies = build_frequency_grid(
            native_frequencies,
            frequency_grid_request or FrequencyGridRequest("native"),
            configured_regions=configured_regions,
        )
    except ValueError as error:
        raise ValueError(f"Simulation {simulation_id}: {error}") from error

    labels = tuple(
        _sparameter_label(row + 1, column + 1)
        for row in range(port_count)
        for column in range(port_count)
    )
    rows_of_values: list[tuple[complex, ...]] = []
    for frequency in frequencies:
        if not math.isfinite(frequency):
            raise ValueError(
                f"Simulation {simulation_id}: frequency is not finite: {frequency}."
            )
        evaluated_matrix = circuit_matrix.Smatrix(frequency)
        row_values = tuple(
            complex(evaluated_matrix(row, column))
            for row in range(port_count)
            for column in range(port_count)
        )
        if any(
            not math.isfinite(value.real) or not math.isfinite(value.imag)
            for value in row_values
        ):
            raise ValueError(
                f"Simulation {simulation_id}: S-parameter data contains NaN or infinity."
            )
        rows_of_values.append(row_values)

    return MDIFBlock(
        simulation_id=str(simulation_id),
        parameters=tuple((str(name), str(value)) for name, value in parameters.items()),
        frequencies_hz=frequencies,
        labels=labels,
        values=tuple(rows_of_values),
    )


def _case_insensitive_value(mapping: Mapping[str, str], name: str) -> str | None:
    if name in mapping:
        return mapping[name]
    target = name.casefold()
    matches = [value for key, value in mapping.items() if key.casefold() == target]
    return matches[0] if len(matches) == 1 else None


def _select_parameters(
    mapping: Mapping[str, str], parameter_names: Sequence[str]
) -> dict[str, str]:
    if not parameter_names:
        return {name: mapping[name] for name in sorted(mapping, key=str.casefold)}
    selected: dict[str, str] = {}
    missing: list[str] = []
    for name in parameter_names:
        value = _case_insensitive_value(mapping, name)
        if value is None:
            missing.append(name)
        else:
            selected[name] = value
    if missing:
        raise ValueError("Parameter metadata is missing: " + ", ".join(missing))
    return selected


def collect_analysis_blocks(
    empro_module: Any,
    analysis: Any,
    parameter_names: Sequence[str],
    skip_errors: bool,
    frequency_grid_request: FrequencyGridRequest | None = None,
    configured_regions: Sequence[FrequencyRegion] | None = None,
) -> list[MDIFBlock]:
    """Walk public RFPro analysis outputs and extract every usable S-matrix."""

    from empro import toolkit

    analysis_output = empro_module.output.AnalysisOutput(analysis)
    # Preserve the public API's result order. It matches the configured sweep
    # order when older result metadata does not expose geometry parameters.
    simulation_ids = list(analysis_output.getAvailableSimulationIds())
    if not simulation_ids:
        raise RuntimeError(f"Analysis {analysis.name!r} has no available simulations.")

    configured_cases = configured_parameter_cases(analysis.simulationSettings)
    configured_matches = len(configured_cases) == len(simulation_ids)
    if configured_cases and not configured_matches:
        print(
            "Configured sweep-case count does not match available result count; "
            "result metadata will be required."
        )

    blocks: list[MDIFBlock] = []
    parameter_order: list[str] | None = list(parameter_names) if parameter_names else None
    for index, simulation_id in enumerate(simulation_ids):
        result_context = ""
        try:
            simulation_output = analysis_output.getSimulation(simulation_id)
            metadata = simulation_output.metadata()
            mapping = configured_cases[index].copy() if configured_matches else {}
            mapping.update(simulation_parameters(metadata))
            selected = _select_parameters(mapping, parameter_order or ())
            if parameter_order is None:
                if not selected:
                    raise ValueError(
                        "No geometry parameter metadata was found. Use the CSV importer "
                        "before running or specify --parameter-names after confirming "
                        "the result metadata contains those parameters."
                    )
                parameter_order = list(selected)
            else:
                selected = _select_parameters(mapping, parameter_order)

            simulation_path = str(simulation_output.simulationPath)
            if not simulation_path:
                raise ValueError("simulation output has no result path")
            # RFPro may set analysis.simulationPath to this same case directory,
            # so it is not a reliable project context.  The parent of the
            # SimulationOutput path is the result project that owns the case.
            result_context = os.path.dirname(os.path.normpath(simulation_path))
            if not result_context:
                raise ValueError(
                    f"could not derive a result-project path from {simulation_path!r}"
                )
            # Read the simulation's circuit result files directly.  RFPro's
            # nested analysis directories are not necessarily registerable
            # result-browser projects, which makes portparam.getSMatrix fail
            # before it reaches otherwise valid FEM/CTI/SIO result data.
            circuit_matrix = toolkit.getCircuitMatrix(
                proj=result_context,
                sim=str(simulation_id),
            )
            block = circuit_matrix_to_block(
                circuit_matrix,
                simulation_id=str(simulation_id),
                parameters=selected,
                frequency_grid_request=frequency_grid_request,
                configured_regions=configured_regions,
            )
            if blocks and block.labels != blocks[0].labels:
                raise ValueError(
                    f"S-parameter labels differ from simulation {blocks[0].simulation_id}."
                )
            blocks.append(block)
            print(
                f"Collected simulation {simulation_id}: "
                f"{len(block.frequencies_hz)} frequencies, {len(block.labels)} S-parameters."
            )
        except Exception as error:
            if not skip_errors:
                context_details = (
                    f" from result project {result_context!r}"
                    if result_context
                    else ""
                )
                raise RuntimeError(
                    f"Could not export simulation {simulation_id}"
                    f"{context_details}: {error}"
                ) from error
            print(f"Skipping simulation {simulation_id}: {error}")

    if not blocks:
        raise RuntimeError("No RFPro simulation produced an exportable S-matrix.")
    return blocks


_MDIF_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_NUMBER_WITH_UNIT = re.compile(
    r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s+([A-Za-z]+)$"
)


def _format_var_value(value: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError("MDIF parameter values cannot be empty.")
    if "\n" in text or "\r" in text:
        raise ValueError("MDIF parameter values cannot contain newlines.")
    number_with_unit = _NUMBER_WITH_UNIT.fullmatch(text)
    if number_with_unit:
        return "".join(number_with_unit.groups())
    if re.fullmatch(r"[A-Za-z0-9_.+\-]+", text):
        return text
    return json.dumps(text, ensure_ascii=True)


def render_mdif(blocks: Sequence[MDIFBlock], reference_impedance_ohms: float) -> str:
    if not blocks:
        raise ValueError("At least one MDIF block is required.")
    if not math.isfinite(reference_impedance_ohms) or reference_impedance_ohms <= 0:
        raise ValueError("Reference impedance must be a positive finite value.")

    parameter_names = [name for name, _ in blocks[0].parameters]
    for name in parameter_names:
        if not _MDIF_IDENTIFIER.fullmatch(name):
            raise ValueError(
                f"RFPro parameter {name!r} is not a valid generic MDIF VAR identifier."
            )

    lines = [
        "! RFPro swept S-parameter results",
        "! Generic MDIF: one ACDATA block per independent geometry case",
        "! Generated inside RFPro by export_analysis_mdif.py",
        "",
    ]
    expected_labels = blocks[0].labels
    for block in blocks:
        if block.labels != expected_labels:
            raise ValueError(
                f"Simulation {block.simulation_id} has inconsistent S-parameter labels."
            )
        current_names = [name for name, _ in block.parameters]
        if current_names != parameter_names:
            raise ValueError(
                f"Simulation {block.simulation_id} has inconsistent parameter metadata."
            )
        if len(block.values) != len(block.frequencies_hz):
            raise ValueError(
                f"Simulation {block.simulation_id} has inconsistent frequency/data rows."
            )

        lines.append(f"! simulation_id={block.simulation_id}")
        for name, value in block.parameters:
            lines.append(f"VAR {name}={_format_var_value(value)}")
        lines.append("BEGIN ACDATA")
        lines.append("% Freq " + " ".join(block.labels))
        lines.append(f"# Hz S RI R {reference_impedance_ohms:.16g}")
        for frequency, row_values in zip(block.frequencies_hz, block.values):
            if len(row_values) != len(block.labels):
                raise ValueError(
                    f"Simulation {block.simulation_id} has a malformed S-parameter row."
                )
            fields = [f"{frequency:.16g}"]
            for value in row_values:
                fields.extend((f"{value.real:.16g}", f"{value.imag:.16g}"))
            lines.append(" ".join(fields))
        lines.extend(("END", ""))
    return "\n".join(lines)


def write_mdif_atomic(
    path: Path, blocks: Sequence[MDIFBlock], reference_impedance_ohms: float
) -> None:
    """Write a complete file beside the destination, then atomically replace it."""

    parent = path.parent
    if not parent.is_dir():
        raise FileNotFoundError(f"Output directory does not exist: {parent}")
    content = render_mdif(blocks, reference_impedance_ohms)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(parent), text=True
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _parse_parameter_names(value: str) -> list[str]:
    names = [part.strip() for part in value.split(",") if part.strip()]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError("Duplicate --parameter-names: " + ", ".join(duplicates))
    return names


def _frequency_request_from_arguments(arguments: argparse.Namespace) -> FrequencyGridRequest:
    if arguments.native_frequency_grid:
        return FrequencyGridRequest("native")
    if arguments.frequency_points is not None:
        return validate_frequency_grid_request(
            FrequencyGridRequest("points", point_count=arguments.frequency_points)
        )
    if arguments.frequency_step is not None:
        return validate_frequency_grid_request(
            FrequencyGridRequest(
                "step", step_hz=parse_frequency_step(arguments.frequency_step)
            )
        )

    mode = str(DEFAULT_FREQUENCY_MODE).strip().casefold()
    if mode == "ask":
        return FrequencyGridRequest("ask")
    if mode == "native":
        return FrequencyGridRequest("native")
    if mode == "points":
        return validate_frequency_grid_request(
            FrequencyGridRequest("points", point_count=int(DEFAULT_FREQUENCY_POINTS))
        )
    if mode == "step":
        return validate_frequency_grid_request(
            FrequencyGridRequest(
                "step", step_hz=parse_frequency_step(DEFAULT_FREQUENCY_STEP)
            )
        )
    raise ValueError(
        "DEFAULT_FREQUENCY_MODE must be one of: ask, native, points, or step."
    )


def _choose_frequency_grid_request(
    requested: FrequencyGridRequest,
) -> FrequencyGridRequest:
    if requested.mode.casefold() != "ask":
        return validate_frequency_grid_request(requested)

    from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox

    choices = [
        "Native result frequencies",
        "Uniform number of points",
        "Frequency step size",
    ]
    selected, accepted = QInputDialog.getItem(
        None,
        "RFPro MDIF Frequency Grid",
        "Export frequency sampling:",
        choices,
        0,
        False,
    )
    if not accepted:
        raise RuntimeError("Frequency-grid selection was cancelled.")
    if selected == choices[0]:
        return FrequencyGridRequest("native")
    if selected == choices[1]:
        point_count, accepted = QInputDialog.getInt(
            None,
            "RFPro MDIF Frequency Grid",
            "Number of points in each configured range, including endpoints:\n"
            "(Configured single-frequency plans are retained separately.)",
            max(2, min(int(DEFAULT_FREQUENCY_POINTS), MAX_FREQUENCY_POINTS)),
            2,
            MAX_FREQUENCY_POINTS,
            1,
        )
        if not accepted:
            raise RuntimeError("Frequency point-count entry was cancelled.")
        return FrequencyGridRequest("points", point_count=point_count)

    initial_step = str(DEFAULT_FREQUENCY_STEP)
    while True:
        step_text, accepted = QInputDialog.getText(
            None,
            "RFPro MDIF Frequency Grid",
            "Frequency step (for example, 100 MHz):",
            QLineEdit.EchoMode.Normal,
            initial_step,
        )
        if not accepted:
            raise RuntimeError("Frequency-step entry was cancelled.")
        try:
            step_hz = parse_frequency_step(str(step_text))
        except ValueError as error:
            QMessageBox.warning(None, "Invalid frequency step", str(error))
            initial_step = str(step_text)
            continue
        return FrequencyGridRequest("step", step_hz=step_hz)


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export one RFPro analysis and all of its sweep results as generic MDIF.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT_PATH, help="output .mdif or .mdf path"
    )
    parser.add_argument(
        "--analysis", default=DEFAULT_ANALYSIS_NAME, help="RFPro analysis name"
    )
    parser.add_argument(
        "--parameter-names",
        default=DEFAULT_PARAMETER_NAMES,
        help="comma-separated geometry parameters to export, in MDIF order",
    )
    parser.add_argument(
        "--reference-impedance",
        type=float,
        default=DEFAULT_REFERENCE_IMPEDANCE_OHMS,
        help=(
            "single reference impedance declared in the MDIF header; "
            "this option does not renormalize RFPro data"
        ),
    )
    frequency_group = parser.add_mutually_exclusive_group()
    frequency_group.add_argument(
        "--native-frequency-grid",
        action="store_true",
        help="export the frequencies stored in each RFPro result",
    )
    frequency_group.add_argument(
        "--frequency-points",
        type=int,
        help=(
            "export this many uniformly spaced points over each configured "
            "analysis range; retain configured single frequencies"
        ),
    )
    frequency_group.add_argument(
        "--frequency-step",
        help=(
            "export with this maximum step inside each configured analysis "
            "range; accepts Hz, kHz, MHz, GHz, or THz"
        ),
    )
    parser.add_argument(
        "--skip-errors",
        action="store_true",
        help="skip result cases that cannot produce a complete S-matrix",
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="replace an existing output file"
    )
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    return arguments


def _confirm_overwrite(path: Path) -> bool:
    from PySide6.QtWidgets import QMessageBox

    answer = QMessageBox.question(
        None,
        "Replace existing MDIF?",
        f"The output file already exists:\n{path}\n\nReplace it?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return answer == QMessageBox.StandardButton.Yes


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
    parameter_names = _parse_parameter_names(arguments.parameter_names)
    requested_frequency_grid = _frequency_request_from_arguments(arguments)
    qt_runtime = create_or_reuse_qapplication()
    _print_qt_diagnostics(qt_runtime)

    import empro

    analysis = _choose_analysis(empro.activeProject, arguments.analysis)
    frequency_grid_request = _choose_frequency_grid_request(requested_frequency_grid)
    print("Frequency grid: " + frequency_grid_description(frequency_grid_request))
    frequency_regions: tuple[FrequencyRegion, ...] | None = None
    if frequency_grid_request.mode != "native":
        frequency_regions = configured_frequency_regions(analysis.simulationSettings)
        print(
            "Enabled analysis frequency plans: "
            + frequency_regions_description(frequency_regions)
        )
    output_path = _choose_output_path(arguments.output, str(analysis.name))
    if output_path.exists() and not arguments.overwrite and not _confirm_overwrite(output_path):
        print("Export cancelled; the existing MDIF was not changed.")
        return

    blocks = collect_analysis_blocks(
        empro,
        analysis,
        parameter_names=parameter_names,
        skip_errors=arguments.skip_errors,
        frequency_grid_request=frequency_grid_request,
        configured_regions=frequency_regions,
    )
    write_mdif_atomic(output_path, blocks, arguments.reference_impedance)
    summary = (
        f"Exported {len(blocks)} RFPro result cases from analysis {analysis.name!r} "
        f"to {output_path} using {frequency_grid_description(frequency_grid_request)}."
    )
    print(summary)
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.information(None, "RFPro MDIF Export", summary)


if __name__ == "__main__":
    main()
