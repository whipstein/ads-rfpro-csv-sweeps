from __future__ import annotations

import importlib.util
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "run_analysis_reuse_existing.py"
SPEC = importlib.util.spec_from_file_location("run_analysis_reuse_existing", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeSettings:
    numberOfParameterInstances = 5


class FakeAnalysis:
    name = "RF Setup"
    analysisType = 7
    simulationSettings = FakeSettings()


class FakeAnalysisClass:
    EMFUAnalysisType = 7
    EMUDAnalysisType = 8
    EMFUPEAnalysisType = 10
    EMUDPEAnalysisType = 11


class FakeAnalysisModule:
    Analysis = FakeAnalysisClass


class FakeEmpro:
    analysis = FakeAnalysisModule


class ReuseRunnerTests(unittest.TestCase):
    def test_preview_makes_manual_start_and_reuse_explicit(self) -> None:
        preview = MODULE.build_run_preview(FakeAnalysis(), 5, 3)
        self.assertIn("Potentially missing instances: 2", preview)
        self.assertIn("reuse valid existing results", preview)
        self.assertIn("starts the analysis now", preview)
        self.assertIn("FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR=0.5", preview)
        self.assertIn("FEMIZER_WAVEGUIDE_VERTICAL_FACTOR=2.0", preview)
        self.assertIn("FEM_ALWAYS_SOLVE_ON_FINEST_MESH=on", preview)

    def test_public_runner_receives_reuse_flags(self) -> None:
        calls: list[tuple[object, dict[str, object]]] = []

        def fake_run(analysis: object, **kwargs: object) -> str:
            calls.append((analysis, kwargs))
            return "queued"

        analysis = FakeAnalysis()
        result = MODULE.run_analysis_reusing_results(
            fake_run, analysis, save_project=True
        )
        self.assertEqual(result, "queued")
        self.assertEqual(
            calls,
            [
                (
                    analysis,
                    {
                        "waitForConfirmation": False,
                        "saveProject": True,
                        "reuseExistingIfPossible": True,
                    },
                )
            ],
        )

    def test_confirmation_is_enabled_by_default(self) -> None:
        arguments = MODULE._parse_arguments([])
        self.assertFalse(arguments.yes)
        self.assertFalse(arguments.no_save)

    def test_required_fem_environment_is_active_only_during_run(self) -> None:
        observed: dict[str, str | None] = {}

        def fake_run(_analysis: object, **_kwargs: object) -> str:
            for name in MODULE.DEFAULT_RUN_ENVIRONMENT:
                observed[name] = os.environ.get(name)
            return "queued"

        names = list(MODULE.DEFAULT_RUN_ENVIRONMENT)
        with patch.dict(os.environ, {}, clear=False):
            for name in names:
                os.environ.pop(name, None)
            MODULE.run_analysis_reusing_results(fake_run, FakeAnalysis(), True)
            restored = {name: os.environ.get(name) for name in names}

        self.assertEqual(observed, MODULE.DEFAULT_RUN_ENVIRONMENT)
        self.assertEqual(restored, {name: None for name in names})

    def test_existing_fem_environment_is_restored_exactly(self) -> None:
        existing = {
            "FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR": "old-horizontal",
            "FEMIZER_WAVEGUIDE_VERTICAL_FACTOR": "",
            "FEM_ALWAYS_SOLVE_ON_FINEST_MESH": "off",
        }

        def fake_run(_analysis: object, **_kwargs: object) -> str:
            self.assertEqual(
                {name: os.environ.get(name) for name in existing},
                MODULE.DEFAULT_RUN_ENVIRONMENT,
            )
            return "queued"

        with patch.dict(os.environ, existing, clear=False):
            MODULE.run_analysis_reusing_results(fake_run, FakeAnalysis(), True)
            restored = {name: os.environ.get(name) for name in existing}

        self.assertEqual(restored, existing)

    def test_fem_environment_is_restored_when_run_fails(self) -> None:
        names = list(MODULE.DEFAULT_RUN_ENVIRONMENT)

        def fake_run(_analysis: object, **_kwargs: object) -> str:
            raise RuntimeError("submission failed")

        with patch.dict(os.environ, {}, clear=False):
            for name in names:
                os.environ.pop(name, None)
            with self.assertRaisesRegex(RuntimeError, "submission failed"):
                MODULE.run_analysis_reusing_results(fake_run, FakeAnalysis(), True)
            restored = {name: os.environ.get(name) for name in names}

        self.assertEqual(restored, {name: None for name in names})

    def test_unsupported_analysis_type_is_rejected_before_running(self) -> None:
        MODULE.validate_reuse_supported(FakeEmpro, FakeAnalysis())
        unsupported = FakeAnalysis()
        unsupported.analysisType = 99
        with self.assertRaisesRegex(ValueError, "Nothing was started"):
            MODULE.validate_reuse_supported(FakeEmpro, unsupported)


if __name__ == "__main__":
    unittest.main()
