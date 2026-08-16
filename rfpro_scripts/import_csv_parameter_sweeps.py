"""Import correlated RFPro geometry cases from a CSV file.

Run this file inside the open RFPro project.  Every enabled CSV row becomes
one independent ``ParameterSequence``.  A row's parameter values therefore
remain correlated and are not expanded into a Cartesian product.

The Qt bootstrap is intentionally self-contained.  It reuses RFPro's existing
QApplication without changing the process environment.  Only a standalone
launcher that does not yet own QApplication receives a temporary, restored
``QT_QPA_PLATFORM_PLUGIN_PATH`` while the application is constructed.
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


# Edit these defaults when RFPro's Run Script command cannot pass arguments.
DEFAULT_CSV_PATH = ""
DEFAULT_ANALYSIS_NAME = ""
DEFAULT_IMPORT_MODE = "ask"  # "ask", "replace", or "append"
DEFAULT_SAVE_PROJECT = True

_RESERVED_COLUMNS = {"__case__", "__comment__", "__enabled__"}
_FALSE_VALUES = {"0", "false", "no", "off", "disabled"}
_TRUE_VALUES = {"", "1", "true", "yes", "on", "enabled"}


@dataclass(frozen=True)
class SweepCase:
    """One correlated geometry-parameter case from one CSV row."""

    source_row: int
    label: str
    parameters: tuple[tuple[str, str], ...]
    comment: str = ""


@dataclass(frozen=True)
class QtRuntime:
    """Objects and diagnostics kept alive for the complete RFPro operation."""

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


def _enabled_cell(value: str, row_number: int) -> bool:
    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    raise ValueError(
        f"CSV row {row_number}: __enabled__ must be one of "
        "true/false, yes/no, on/off, or 1/0."
    )


def read_sweep_csv(path: Path) -> list[SweepCase]:
    """Read a header-based CSV whose enabled rows are correlated cases."""

    if not path.is_file():
        raise FileNotFoundError(f"CSV file does not exist: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")

        headers = [header.strip() if header is not None else "" for header in reader.fieldnames]
        if any(not header for header in headers):
            raise ValueError("CSV contains an empty column name.")
        duplicates = sorted({name for name in headers if headers.count(name) > 1})
        if duplicates:
            raise ValueError(f"CSV contains duplicate columns: {', '.join(duplicates)}")
        unknown_reserved = sorted(
            name for name in headers if name.startswith("__") and name not in _RESERVED_COLUMNS
        )
        if unknown_reserved:
            raise ValueError(
                "Unknown reserved CSV columns: " + ", ".join(unknown_reserved)
            )

        parameter_names = [name for name in headers if not name.startswith("__")]
        if not parameter_names:
            raise ValueError("CSV must contain at least one RFPro parameter column.")

        # DictReader retains the original, possibly whitespace-padded field names.
        original_by_stripped = dict(zip(headers, reader.fieldnames))
        cases: list[SweepCase] = []
        for row_number, raw_row in enumerate(reader, start=2):
            if None in raw_row:
                raise ValueError(
                    f"CSV row {row_number} contains more values than the header."
                )
            row = {
                stripped: (raw_row.get(original, "") or "").strip()
                for stripped, original in original_by_stripped.items()
            }
            if not any(row.values()):
                continue
            if "__enabled__" in row and not _enabled_cell(row["__enabled__"], row_number):
                continue

            values: list[tuple[str, str]] = []
            for name in parameter_names:
                value = row[name]
                if not value:
                    raise ValueError(
                        f"CSV row {row_number}: parameter {name!r} has no value. "
                        "Every independent case must be complete."
                    )
                if "," in value:
                    raise ValueError(
                        f"CSV row {row_number}: parameter {name!r} contains a comma. "
                        "One CSV cell must define exactly one RFPro value."
                    )
                if "\n" in value or "\r" in value:
                    raise ValueError(
                        f"CSV row {row_number}: parameter {name!r} contains a newline."
                    )
                values.append((name, value))

            label = row.get("__case__", "") or f"row-{row_number}"
            cases.append(
                SweepCase(
                    source_row=row_number,
                    label=label,
                    parameters=tuple(values),
                    comment=row.get("__comment__", ""),
                )
            )

    if not cases:
        raise ValueError(f"CSV contains no enabled sweep cases: {path}")
    return cases


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


def validate_cases_against_project(project: Any, cases: Sequence[SweepCase]) -> None:
    """Require exact, editable RFPro project-parameter names."""

    available = {str(name) for name in project.parameters.names()}
    requested = {name for case in cases for name, _ in case.parameters}
    missing = sorted(requested - available)
    if missing:
        raise ValueError(
            "CSV columns are not RFPro project parameters: " + ", ".join(missing)
        )
    noneditable = sorted(
        name for name in requested if not project.parameters.isEditable(name)
    )
    if noneditable:
        raise ValueError(
            "CSV parameters are not editable in the active project: "
            + ", ".join(noneditable)
        )


def build_parameter_sequences(empro_module: Any, cases: Sequence[SweepCase]) -> list[Any]:
    """Build all native objects before mutating the selected analysis."""

    sequences: list[Any] = []
    for case in cases:
        sequence = empro_module.simulation.ParameterSequence()
        for parameter_name, formula in case.parameters:
            sweep = empro_module.simulation.SingleParameterSweep()
            sweep.parameterName = parameter_name
            sweep.setParameterValues(formula)
            sequence.append(sweep)
        sequences.append(sequence)
    return sequences


def install_parameter_sequences(
    settings: Any, sequences: Iterable[Any], mode: str
) -> tuple[int, int]:
    """Install independent sequences and return previous/final sequence counts."""

    if mode not in {"replace", "append"}:
        raise ValueError(f"Unknown import mode: {mode!r}")
    before = len(settings.parameterSequences)
    if mode == "replace":
        settings.parameterSequences.clear()
    for sequence in sequences:
        settings.parameterSequences.append(sequence)
    settings.parameterSweepEnabled = True
    return before, len(settings.parameterSequences)


def _choose_analysis(project: Any, requested_name: str) -> Any:
    names = analysis_names(project)
    if requested_name or len(names) <= 1:
        return find_analysis(project, requested_name)

    from PySide6.QtWidgets import QInputDialog

    selected, accepted = QInputDialog.getItem(
        None,
        "RFPro CSV Parameter Sweeps",
        "Analysis:",
        names,
        0,
        False,
    )
    if not accepted:
        raise RuntimeError("Analysis selection was cancelled.")
    return find_analysis(project, str(selected))


def _choose_csv_path(configured_path: str) -> Path:
    if configured_path:
        return Path(configured_path).expanduser().resolve()

    from PySide6.QtWidgets import QFileDialog

    selected, _ = QFileDialog.getOpenFileName(
        None,
        "Select RFPro geometry sweep CSV",
        "",
        "CSV files (*.csv);;All files (*)",
    )
    if not selected:
        raise RuntimeError("CSV selection was cancelled.")
    return Path(selected).expanduser().resolve()


def _choose_import_mode(settings: Any, configured_mode: str) -> str:
    """Resolve replace/append explicitly before changing the analysis."""

    if configured_mode in {"replace", "append"}:
        return configured_mode
    if configured_mode != "ask":
        raise ValueError(f"Unknown import mode: {configured_mode!r}")

    from PySide6.QtWidgets import QInputDialog

    choices = (
        "Replace all existing sweep sequences",
        "Append CSV cases to existing sweep sequences",
    )
    selected, accepted = QInputDialog.getItem(
        None,
        "RFPro CSV Parameter Sweeps",
        (
            f"The analysis currently has {len(settings.parameterSequences)} sweep "
            "sequence(s).\nChoose how to import the CSV cases:"
        ),
        choices,
        1,
        False,
    )
    if not accepted:
        raise RuntimeError("Import-mode selection was cancelled.")
    return "replace" if str(selected) == choices[0] else "append"


def _preview_text(analysis: Any, path: Path, cases: Sequence[SweepCase], mode: str) -> str:
    parameter_names = [name for name, _ in cases[0].parameters]
    existing_count = len(analysis.simulationSettings.parameterSequences)
    resulting_count = len(cases) if mode == "replace" else existing_count + len(cases)
    lines = [
        f"Analysis: {analysis.name}",
        f"CSV: {path}",
        f"Mode: {mode}",
        f"Existing sweep sequences: {existing_count}",
        f"Resulting sweep sequences: {resulting_count}",
        f"Independent cases: {len(cases)}",
        "Parameters: " + ", ".join(parameter_names),
        "",
    ]
    for case in cases[:8]:
        values = ", ".join(f"{name}={value}" for name, value in case.parameters)
        lines.append(f"{case.label}: {values}")
    if len(cases) > 8:
        lines.append(f"... and {len(cases) - 8} more cases")
    return "\n".join(lines)


def _confirm_import(text: str) -> bool:
    from PySide6.QtWidgets import QMessageBox

    answer = QMessageBox.question(
        None,
        "Install RFPro parameter sweeps?",
        text,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return answer == QMessageBox.StandardButton.Yes


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import correlated RFPro geometry cases from CSV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--csv", default=DEFAULT_CSV_PATH, help="input CSV path")
    parser.add_argument(
        "--analysis", default=DEFAULT_ANALYSIS_NAME, help="target RFPro analysis name"
    )
    parser.add_argument(
        "--mode",
        choices=("ask", "replace", "append"),
        default=DEFAULT_IMPORT_MODE,
        help="ask in RFPro, replace existing sequences, or append independent cases",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="leave the active project modified but unsaved",
    )
    parser.add_argument(
        "--yes", action="store_true", help="install without the confirmation dialog"
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

    # RFPro owns the active project; importing empro here preserves that state.
    import empro

    project = empro.activeProject
    analysis = _choose_analysis(project, arguments.analysis)
    csv_path = _choose_csv_path(arguments.csv)
    cases = read_sweep_csv(csv_path)
    validate_cases_against_project(project, cases)
    sequences = build_parameter_sequences(empro, cases)
    import_mode = _choose_import_mode(analysis.simulationSettings, arguments.mode)

    preview = _preview_text(analysis, csv_path, cases, import_mode)
    print(preview)
    if not arguments.yes and not _confirm_import(preview):
        print("Import cancelled; the RFPro analysis was not changed.")
        return

    before, after = install_parameter_sequences(
        analysis.simulationSettings, sequences, import_mode
    )
    should_save = DEFAULT_SAVE_PROJECT and not arguments.no_save
    if should_save:
        project.saveActiveProject()

    summary = (
        f"Installed {len(cases)} independent CSV cases in analysis {analysis.name!r}. "
        f"Parameter sequences: {before} -> {after}. "
        f"Project saved: {should_save}. No simulation was started."
    )
    print(summary)
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.information(None, "RFPro CSV Parameter Sweeps", summary)


if __name__ == "__main__":
    main()
