from __future__ import annotations

import importlib.util
import sys
import types
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

    path = ROOT / relative_path
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


class FakeScripting:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def run(self, path: str, arguments: list[str]) -> None:
        self.calls.append((path, arguments))


def fake_empro_modules(scripting: FakeScripting) -> dict[str, types.ModuleType]:
    empro = types.ModuleType("empro")
    toolkit = types.ModuleType("empro.toolkit")
    scripting_module = types.ModuleType("empro.toolkit.scripting")
    scripting_module.run = scripting.run  # type: ignore[attr-defined]
    toolkit.scripting = scripting_module  # type: ignore[attr-defined]
    empro.toolkit = toolkit  # type: ignore[attr-defined]
    return {
        "empro": empro,
        "empro.toolkit": toolkit,
        "empro.toolkit.scripting": scripting_module,
    }


class RFProToolLauncherTests(unittest.TestCase):
    def test_workflow_contains_all_expected_operations(self) -> None:
        operations = {item[0]: item for item in WORKFLOW.operation_specs()}

        self.assertEqual(
            set(operations),
            {"import_csv", "run_analysis", "export_mdif", "geometry_inspector"},
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

    def test_every_operation_resolves_to_an_existing_script(self) -> None:
        for module in (WORKFLOW, DIAGNOSTICS):
            for operation in module.operation_specs():
                with self.subTest(module=module.__name__, operation=operation[0]):
                    self.assertTrue(module.tool_script_path(operation[3]).is_file())

    def test_selected_operations_are_loaded_with_the_analysis_argument(self) -> None:
        for module, operation_key, expected_filename in (
            (WORKFLOW, "export_mdif", "export_analysis_mdif.py"),
            (
                DIAGNOSTICS,
                "duplicate_conditions",
                "diagnose_duplicate_sweep_conditions.py",
            ),
        ):
            scripting = FakeScripting()
            operation = module.find_operation(operation_key)

            with self.subTest(module=module.__name__, operation=operation_key):
                with patch.dict(sys.modules, fake_empro_modules(scripting)):
                    module.run_operation(operation, "RF Analysis")

                self.assertEqual(len(scripting.calls), 1)
                path, arguments = scripting.calls[0]
                self.assertTrue(path.endswith(f"rfpro_scripts/{expected_filename}"))
                self.assertEqual(arguments, ["--analysis", "RF Analysis"])

    def test_entry_scripts_do_not_depend_on_the_removed_shared_launcher(self) -> None:
        for filename in ("rfpro_workflow.py", "rfpro_diagnostics.py"):
            source = (ROOT / "rfpro_scripts" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertNotIn("rfpro_tool_launcher", source)
                self.assertIn("def create_or_reuse_qapplication", source)
                self.assertIn("def choose_operation", source)

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
