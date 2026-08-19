"""Self-contained RFPro import/run/export/geometry workflow dropdown."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any, Sequence


# Edit this key to change the preselected dropdown operation.
DEFAULT_OPERATION = "import_csv"

_OPERATIONS = (
    (
        "import_csv",
        "Import CSV parameter sweeps",
        "Select a CSV and append or synchronize independent correlated geometry "
        "conditions without starting a simulation.",
        "import_csv_parameter_sweeps.py",
    ),
    (
        "run_analysis",
        "Save and run analysis",
        "Apply the persistent FEM environment settings, save the active project, "
        "and start through RFPro's native Auto/reuse policy.",
        "run_analysis_reuse_existing.py",
    ),
    (
        "export_mdif",
        "Export analysis results to MDIF",
        "Export registered or explicitly selected raw swept S-parameter results "
        "with native, point-count, or step-size frequency sampling.",
        "export_analysis_mdif.py",
    ),
    (
        "geometry_inspector",
        "Geometry and Mesh/Ports inspector",
        "Open the sweep-point inspector for regenerated geometry validation, "
        "saved Mesh/Ports viewing, PNG capture, and PDF reports.",
        "preview_sweep_geometries.py",
    ),
)


class QtRuntime:
    """Qt startup result without dataclass loader-registration assumptions."""

    def __init__(
        self,
        application: Any,
        pyside_file: Path,
        plugin_file: Path | None,
        application_was_created: bool,
        environment_was_restored: bool,
    ) -> None:
        self.application = application
        self.pyside_file = pyside_file
        self.plugin_file = plugin_file
        self.application_was_created = application_was_created
        self.environment_was_restored = environment_was_restored


def expected_qt_platform_plugin() -> str:
    if sys.platform.startswith("linux"):
        return "libqxcb.so"
    if sys.platform == "win32":
        return "qwindows.dll"
    if sys.platform == "darwin":
        return "libqcocoa.dylib"
    raise RuntimeError(f"Unsupported Qt platform: {sys.platform}")


def locate_qt_platform_plugin(pyside_file: Path) -> Path:
    """Check configured/package paths, then bounded product fallback roots."""

    from PySide6.QtCore import QCoreApplication, QLibraryInfo

    plugin_name = expected_qt_platform_plugin()
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
    for environment_name in (
        "QT_QPA_PLATFORM_PLUGIN_PATH",
        "QT_PLUGIN_PATH",
    ):
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
    for environment_name in ("HPEESOF_DIR", "EMPROHOME"):
        value = os.environ.get(environment_name)
        if value:
            fallback_roots.append(Path(value))

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
        "Run the ADS Qt runtime diagnostic with this exact interpreter."
    )


def validate_linux_plugin(plugin_file: Path) -> None:
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
        raise RuntimeError(
            f"Could not inspect Qt plugin {plugin_file}: {error}"
        ) from error
    unresolved = [
        line.strip()
        for line in (result.stdout + result.stderr).splitlines()
        if "not found" in line
    ]
    if unresolved:
        details = "\n  ".join(unresolved)
        raise RuntimeError(
            f"Qt found {plugin_file}, but required libraries are missing:\n"
            f"  {details}"
        )


def create_or_reuse_qapplication() -> QtRuntime:
    """Reuse product-owned Qt, or create script-owned Qt with scoped redirect."""

    try:
        import PySide6
    except Exception as error:
        raise RuntimeError(
            "PySide6 could not be imported. Run with the bundled Keysight "
            f"interpreter or directly in ADS/EMPro/RFPro, not {sys.executable!r}."
        ) from error

    from PySide6.QtWidgets import QApplication

    pyside_file = Path(PySide6.__file__).resolve()
    application = QApplication.instance()
    if application is not None:
        return QtRuntime(application, pyside_file, None, False, True)

    plugin_file = locate_qt_platform_plugin(pyside_file)
    validate_linux_plugin(plugin_file)
    if sys.platform.startswith("linux"):
        selected_platform = os.environ.get("QT_QPA_PLATFORM", "").lower()
        has_display = bool(
            os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
        )
        if not has_display and selected_platform not in {"offscreen", "minimal"}:
            raise RuntimeError(
                "No DISPLAY or WAYLAND_DISPLAY is available for graphical "
                "Keysight Qt. Launch from a graphical session; this bootstrap "
                "does not force offscreen mode."
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
        os.environ.get(variable) == previous
        if was_set
        else variable not in os.environ
    )
    return QtRuntime(application, pyside_file, plugin_file, True, restored)


def print_qt_diagnostics(runtime: QtRuntime) -> None:
    ownership = (
        "created by script"
        if runtime.application_was_created
        else "reused from ADS/EMPro/RFPro"
    )
    plugin = (
        str(runtime.plugin_file)
        if runtime.plugin_file is not None
        else "already loaded by product; search path unchanged"
    )
    print(f"Python executable: {sys.executable}")
    print(f"PySide6 package: {runtime.pyside_file}")
    print(f"Qt platform plugin: {plugin}")
    print(f"Qt platform: {runtime.application.platformName()}")
    print(f"QApplication: {ownership}")
    print(f"Qt environment restored: {runtime.environment_was_restored}")


def operation_specs() -> tuple[tuple[str, str, str, str], ...]:
    return _OPERATIONS


def find_operation(operation_key: str) -> tuple[str, str, str, str]:
    for operation in operation_specs():
        if operation[0] == operation_key:
            return operation
    available = ", ".join(operation[0] for operation in operation_specs())
    raise ValueError(
        f"Unknown workflow operation {operation_key!r}. Available: {available}"
    )


def choose_operation() -> tuple[str, str, str, str] | None:
    from PySide6.QtWidgets import (
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QLabel,
        QVBoxLayout,
    )

    operations = operation_specs()
    dialog = QDialog()
    dialog.setWindowTitle("RFPro Workflow")
    dialog.setMinimumWidth(520)
    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel("Choose an RFPro workflow operation:"))

    combo = QComboBox()
    for key, label, _description, _filename in operations:
        combo.addItem(label, key)
    default_index = next(
        (
            index
            for index, operation in enumerate(operations)
            if operation[0] == DEFAULT_OPERATION
        ),
        0,
    )
    combo.setCurrentIndex(default_index)
    layout.addWidget(combo)

    description = QLabel()
    description.setWordWrap(True)
    description.setMinimumHeight(55)
    layout.addWidget(description)

    def update_description(index: int) -> None:
        description.setText(operations[index][2])

    combo.currentIndexChanged.connect(update_description)
    update_description(combo.currentIndex())

    buttons = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok
        | QDialogButtonBox.StandardButton.Cancel
    )
    buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Run")
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return None
    return operations[combo.currentIndex()]


def choose_analysis_name(project: Any, configured_name: str = "") -> str | None:
    from PySide6.QtWidgets import QInputDialog

    names = [str(name) for name in project.analyses.names()]
    if not names:
        raise RuntimeError("The active RFPro project contains no analyses.")
    if configured_name:
        if configured_name not in names:
            raise ValueError(
                f"Analysis {configured_name!r} does not exist. Available: "
                + ", ".join(names)
            )
        return configured_name
    if len(names) == 1:
        return names[0]
    selected, accepted = QInputDialog.getItem(
        None,
        "Select RFPro analysis",
        "Analysis:",
        names,
        0,
        False,
    )
    return str(selected) if accepted else None


def tool_script_path(filename: str) -> Path:
    path = Path(__file__).resolve().parent / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"Selected RFPro workflow script does not exist: {path}"
        )
    return path


def run_operation(operation: Sequence[str], analysis_name: str) -> None:
    from empro.toolkit import scripting

    _key, label, _description, filename = operation
    path = tool_script_path(filename)
    print(f"Launching RFPro workflow: {label} ({path})")
    scripting.run(str(path), ["--analysis", analysis_name])


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Combined RFPro workflow launcher.")
    parser.add_argument("--operation", default="")
    parser.add_argument("--analysis", default="")
    arguments, unknown = parser.parse_known_args(argv)
    if unknown:
        print("Ignoring RFPro/launcher arguments: " + " ".join(unknown))
    if arguments.operation:
        find_operation(arguments.operation)
    return arguments


def main(argv: Sequence[str] | None = None) -> None:
    arguments = _parse_arguments(argv)
    qt_runtime = create_or_reuse_qapplication()
    print_qt_diagnostics(qt_runtime)

    import empro

    operation = (
        find_operation(arguments.operation)
        if arguments.operation
        else choose_operation()
    )
    if operation is None:
        print("RFPro workflow selection cancelled; nothing was run.")
        return
    analysis_name = choose_analysis_name(empro.activeProject, arguments.analysis)
    if analysis_name is None:
        print("RFPro analysis selection cancelled; nothing was run.")
        return

    try:
        run_operation(operation, analysis_name)
    except Exception as error:
        traceback.print_exc()
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.critical(
            None,
            "RFPro workflow failed",
            f"{operation[1]} failed:\n\n{error}\n\n"
            "See the RFPro Python console for the complete traceback.",
        )
        raise


if __name__ == "__main__":
    main()
