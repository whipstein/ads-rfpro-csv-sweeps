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
    def __init__(self) -> None:
        self.numberOfParameterInstances = 5
        self.reuseExistingResults = False


class FakeAnalysis:
    name = "RF Setup"
    analysisType = 7

    def __init__(self) -> None:
        self.simulationSettings = FakeSettings()


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
        preview = MODULE.build_run_preview(FakeAnalysis(), 5, 3, True)
        self.assertIn("Potentially missing instances: 2", preview)
        self.assertIn("Existing-result reuse: enabled", preview)
        self.assertIn("Persisted analysis reuse setting: True", preview)
        self.assertIn("reuse valid existing results", preview)
        self.assertIn("will be saved before submission", preview)
        self.assertIn("remain set for the current RFPro session", preview)
        self.assertIn("starts the analysis now", preview)
        self.assertIn("FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR=0.5", preview)
        self.assertIn("FEMIZER_WAVEGUIDE_VERTICAL_FACTOR=2.0", preview)
        self.assertIn("FEM_ALWAYS_SOLVE_ON_FINEST_MESH=on", preview)

    def test_preview_warns_when_reuse_is_disabled(self) -> None:
        preview = MODULE.build_run_preview(FakeAnalysis(), 5, 3, False)
        self.assertIn("Existing-result reuse: disabled", preview)
        self.assertIn("run regardless of existing results", preview)
        self.assertIn("All configured instances may be queued", preview)

    def test_public_runner_receives_reuse_flags(self) -> None:
        calls: list[tuple[object, dict[str, object]]] = []

        def fake_run(analysis: object, **kwargs: object) -> str:
            calls.append((analysis, kwargs))
            return "queued"

        analysis = FakeAnalysis()
        result = MODULE.run_analysis_reusing_results(
            fake_run, analysis, reuse_existing=True
        )
        self.assertEqual(result, "queued")
        self.assertTrue(analysis.simulationSettings.reuseExistingResults)
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

    def test_project_is_saved_before_submission(self) -> None:
        events: list[str] = []

        class FakeProject:
            @staticmethod
            def saveActiveProject() -> None:
                events.append("save")

        def fake_run(_analysis: object, **kwargs: object) -> str:
            events.append("run")
            self.assertFalse(kwargs["reuseExistingIfPossible"])
            self.assertTrue(kwargs["saveProject"])
            return "queued"

        analysis = FakeAnalysis()
        result = MODULE.save_and_run_analysis(
            FakeProject(), fake_run, analysis, reuse_existing=False
        )
        self.assertEqual(result, "queued")
        self.assertFalse(analysis.simulationSettings.reuseExistingResults)
        self.assertEqual(events, ["save", "run"])

    def test_persisted_reuse_setting_is_applied_before_save(self) -> None:
        events: list[str] = []

        class TrackedSettings:
            def __init__(self) -> None:
                self._reuse = False

            @property
            def reuseExistingResults(self) -> bool:
                return self._reuse

            @reuseExistingResults.setter
            def reuseExistingResults(self, value: bool) -> None:
                self._reuse = value
                events.append(f"reuse={value}")

        class TrackedAnalysis:
            simulationSettings = TrackedSettings()

        class FakeProject:
            @staticmethod
            def saveActiveProject() -> None:
                events.append("save")

        def fake_run(_analysis: object, **_kwargs: object) -> str:
            events.append("run")
            return "queued"

        MODULE.save_and_run_analysis(
            FakeProject(), fake_run, TrackedAnalysis(), reuse_existing=True
        )

        self.assertEqual(events, ["reuse=True", "save", "run"])

    def test_reuse_setting_failure_prevents_save_and_submission(self) -> None:
        events: list[str] = []

        class BadSettings:
            @property
            def reuseExistingResults(self) -> bool:
                return False

            @reuseExistingResults.setter
            def reuseExistingResults(self, _value: bool) -> None:
                raise RuntimeError("unsupported")

        class BadAnalysis:
            simulationSettings = BadSettings()

        class FakeProject:
            @staticmethod
            def saveActiveProject() -> None:
                events.append("save")

        def fake_run(_analysis: object, **_kwargs: object) -> None:
            events.append("run")

        with self.assertRaisesRegex(RuntimeError, "Nothing was started"):
            MODULE.save_and_run_analysis(
                FakeProject(), fake_run, BadAnalysis(), reuse_existing=True
            )
        self.assertEqual(events, [])

    def test_save_failure_prevents_submission(self) -> None:
        run_called = False

        class FakeProject:
            @staticmethod
            def saveActiveProject() -> None:
                raise RuntimeError("save failed")

        def fake_run(_analysis: object, **_kwargs: object) -> None:
            nonlocal run_called
            run_called = True

        with self.assertRaisesRegex(RuntimeError, "save failed"):
            MODULE.save_and_run_analysis(
                FakeProject(),
                fake_run,
                FakeAnalysis(),
                reuse_existing=True,
            )
        self.assertFalse(run_called)

    def test_required_fem_environment_persists_after_submission(self) -> None:
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
            persisted = {name: os.environ.get(name) for name in names}

        self.assertEqual(observed, MODULE.DEFAULT_RUN_ENVIRONMENT)
        self.assertEqual(persisted, MODULE.DEFAULT_RUN_ENVIRONMENT)

    def test_existing_fem_environment_is_replaced_and_left_set(self) -> None:
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
            persisted = {name: os.environ.get(name) for name in existing}

        self.assertEqual(persisted, MODULE.DEFAULT_RUN_ENVIRONMENT)

    def test_fem_environment_persists_when_submission_fails(self) -> None:
        names = list(MODULE.DEFAULT_RUN_ENVIRONMENT)

        def fake_run(_analysis: object, **_kwargs: object) -> str:
            raise RuntimeError("submission failed")

        with patch.dict(os.environ, {}, clear=False):
            for name in names:
                os.environ.pop(name, None)
            with self.assertRaisesRegex(RuntimeError, "submission failed"):
                MODULE.run_analysis_reusing_results(fake_run, FakeAnalysis(), True)
            persisted = {name: os.environ.get(name) for name in names}

        self.assertEqual(persisted, MODULE.DEFAULT_RUN_ENVIRONMENT)

    def test_unsupported_analysis_type_is_rejected_before_running(self) -> None:
        MODULE.validate_reuse_supported(FakeEmpro, FakeAnalysis())
        unsupported = FakeAnalysis()
        unsupported.analysisType = 99
        with self.assertRaisesRegex(ValueError, "Nothing was started"):
            MODULE.validate_reuse_supported(FakeEmpro, unsupported)


if __name__ == "__main__":
    unittest.main()
