from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_module_like_rfpro(name: str, relative_path: str):
    """Mirror empro.toolkit.addon._loadModule without sys.modules insertion."""

    return load_path_like_rfpro(name, ROOT / relative_path)


def load_path_like_rfpro(name: str, path: Path):
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DIAGNOSTICS = load_module(
    "rfpro_diagnostics",
    "rfpro_scripts/rfpro_diagnostics.py",
)
WORKFLOW = load_module(
    "rfpro_workflow",
    "rfpro_scripts/rfpro_workflow.py",
)
BUILDER = load_module(
    "build_rfpro_bundles",
    "scripts/build_rfpro_bundles.py",
)


class RFProToolLauncherTests(unittest.TestCase):
    def test_workflow_contains_all_expected_operations(self) -> None:
        operations = {item[0]: item for item in WORKFLOW.operation_specs()}

        self.assertEqual(
            set(operations),
            {
                "import_csv",
                "run_analysis",
                "duplicate_analysis",
                "export_mdif",
                "geometry_inspector",
            },
        )
        self.assertEqual(
            operations["duplicate_analysis"][3],
            "duplicate_analysis_with_results.py",
        )
        self.assertEqual(
            operations["geometry_inspector"][3],
            "preview_sweep_geometries.py",
        )

    def test_diagnostics_contains_all_expected_operations(self) -> None:
        operations = {item[0]: item for item in DIAGNOSTICS.operation_specs()}

        self.assertEqual(
            set(operations),
            {
                "duplicate_conditions",
                "analysis_reuse",
                "cache_inventory",
                "geometry_inspector",
            },
        )
        self.assertEqual(
            operations["duplicate_conditions"][3],
            "diagnose_duplicate_sweep_conditions.py",
        )

    def test_every_operation_contains_the_exact_canonical_script(self) -> None:
        for module in (WORKFLOW, DIAGNOSTICS):
            for operation in module.operation_specs():
                with self.subTest(module=module.__name__, operation=operation[0]):
                    filename, source = module.embedded_tool_source(operation[0])
                    expected = (ROOT / "rfpro_scripts" / filename).read_text(
                        encoding="utf-8"
                    )
                    self.assertEqual(filename, operation[3])
                    self.assertEqual(source, expected)

    def test_selected_operations_receive_the_analysis_argument_in_memory(self) -> None:
        for module, operation_key in (
            (WORKFLOW, "export_mdif"),
            (WORKFLOW, "duplicate_analysis"),
            (DIAGNOSTICS, "duplicate_conditions"),
        ):
            operation = module.find_operation(operation_key)
            calls: list[tuple[str, list[str]]] = []

            with self.subTest(module=module.__name__, operation=operation_key):
                with patch.object(
                    module,
                    "execute_embedded_tool",
                    side_effect=lambda key, arguments: calls.append(
                        (key, list(arguments))
                    ),
                ):
                    module.run_operation(operation, "RF Analysis")

                self.assertEqual(
                    calls,
                    [(operation_key, ["--analysis", "RF Analysis"])],
                )

    def test_embedded_tool_executes_as_a_registered_dataclass_module(self) -> None:
        child_source = """\
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Invocation:
    arguments: tuple[str, ...]

received = None

def main(argv):
    global received
    received = Invocation(tuple(argv))
"""
        module_name = "_rfpro_workflow_embedded_export_mdif"
        self.addCleanup(sys.modules.pop, module_name, None)

        with patch.object(
            WORKFLOW,
            "embedded_tool_source",
            return_value=("test_child.py", child_source),
        ):
            WORKFLOW.execute_embedded_tool(
                "export_mdif",
                ["--analysis", "RF Analysis"],
            )

        child_module = sys.modules[module_name]
        self.assertEqual(
            child_module.received.arguments,
            ("--analysis", "RF Analysis"),
        )

    def test_every_actual_embedded_tool_loads_in_memory(self) -> None:
        for launcher in (WORKFLOW, DIAGNOSTICS):
            for operation in launcher.operation_specs():
                with self.subTest(
                    launcher=launcher.__name__,
                    operation=operation[0],
                ):
                    filename, child_module = launcher.load_embedded_tool_module(
                        operation[0]
                    )
                    self.addCleanup(sys.modules.pop, child_module.__name__, None)
                    self.assertEqual(filename, operation[3])
                    self.assertTrue(callable(child_module.main))

    def test_each_launcher_works_when_copied_without_sibling_scripts(self) -> None:
        for launcher_name in ("rfpro_workflow.py", "rfpro_diagnostics.py"):
            with self.subTest(launcher=launcher_name):
                with tempfile.TemporaryDirectory() as directory:
                    isolated_path = Path(directory) / launcher_name
                    isolated_path.write_bytes(
                        (ROOT / "rfpro_scripts" / launcher_name).read_bytes()
                    )
                    isolated = load_path_like_rfpro(
                        "isolated_" + launcher_name.removesuffix(".py"),
                        isolated_path,
                    )
                    self.assertEqual(
                        [
                            path.name
                            for path in Path(directory).iterdir()
                            if path.is_file()
                        ],
                        [launcher_name],
                    )
                    for operation in isolated.operation_specs():
                        _filename, child_module = isolated.load_embedded_tool_module(
                            operation[0]
                        )
                        self.addCleanup(sys.modules.pop, child_module.__name__, None)
                        self.assertTrue(callable(child_module.main))

    def test_entry_scripts_do_not_depend_on_the_removed_shared_launcher(self) -> None:
        for filename in ("rfpro_workflow.py", "rfpro_diagnostics.py"):
            source = (ROOT / "rfpro_scripts" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertNotIn("rfpro_tool_launcher", source)
                self.assertNotIn("scripting.run(", source)
                self.assertIn("def create_or_reuse_qapplication", source)
                self.assertIn("def choose_operation", source)
                self.assertIn("def load_embedded_tool_module", source)
                self.assertIn("def execute_embedded_tool", source)

    def test_committed_embedded_sources_are_current(self) -> None:
        self.assertEqual(BUILDER.build(check_only=True), [])

    def test_entries_load_with_keysights_unregistered_module_lifecycle(self) -> None:
        for filename in ("rfpro_workflow.py", "rfpro_diagnostics.py"):
            module_name = "rfpro_loader_test_" + filename.removesuffix(".py")
            with self.subTest(filename=filename):
                module = load_module_like_rfpro(
                    module_name,
                    f"rfpro_scripts/{filename}",
                )
                self.assertTrue(callable(module.main))
                self.assertNotIn(module_name, sys.modules)


if __name__ == "__main__":
    unittest.main()
