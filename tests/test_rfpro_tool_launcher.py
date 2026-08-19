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


LAUNCHER = load_module(
    "rfpro_tool_launcher",
    "rfpro_scripts/rfpro_tool_launcher.py",
)
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
    def test_workflow_contains_geometry_inspector(self) -> None:
        operations = {item[0]: item for item in LAUNCHER.operation_specs("workflow")}

        self.assertEqual(
            operations["geometry_inspector"][3],
            "preview_sweep_geometries.py",
        )

    def test_diagnostics_contains_duplicate_audit_and_geometry_inspector(self) -> None:
        operations = {
            item[0]: item for item in LAUNCHER.operation_specs("diagnostics")
        }

        self.assertEqual(
            operations["duplicate_conditions"][3],
            "diagnose_duplicate_sweep_conditions.py",
        )
        self.assertEqual(
            operations["geometry_inspector"][3],
            "preview_sweep_geometries.py",
        )

    def test_every_operation_resolves_to_an_existing_script(self) -> None:
        for category in ("workflow", "diagnostics"):
            for operation in LAUNCHER.operation_specs(category):
                with self.subTest(category=category, operation=operation[0]):
                    self.assertTrue(LAUNCHER.tool_script_path(operation[3]).is_file())

    def test_selected_operation_is_loaded_with_the_analysis_argument(self) -> None:
        scripting = FakeScripting()
        operation = LAUNCHER.find_operation("workflow", "export_mdif")

        with patch.dict(sys.modules, fake_empro_modules(scripting)):
            LAUNCHER.run_operation(operation, "RF Analysis")

        self.assertEqual(len(scripting.calls), 1)
        path, arguments = scripting.calls[0]
        self.assertTrue(path.endswith("rfpro_scripts/export_analysis_mdif.py"))
        self.assertEqual(arguments, ["--analysis", "RF Analysis"])

    def test_direct_entry_scripts_delegate_to_the_shared_launcher(self) -> None:
        for module, category in (
            (DIAGNOSTICS, "diagnostics"),
            (WORKFLOW, "workflow"),
        ):
            scripting = FakeScripting()
            with self.subTest(category=category):
                with patch.dict(sys.modules, fake_empro_modules(scripting)):
                    module.main(["--analysis", "RF Analysis"])

                self.assertEqual(len(scripting.calls), 1)
                path, arguments = scripting.calls[0]
                self.assertTrue(path.endswith("rfpro_scripts/rfpro_tool_launcher.py"))
                self.assertEqual(
                    arguments,
                    ["--category", category, "--analysis", "RF Analysis"],
                )


if __name__ == "__main__":
    unittest.main()
