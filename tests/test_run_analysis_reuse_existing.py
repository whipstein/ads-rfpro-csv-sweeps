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
        self.assertIn("Existing-result policy: RFPro native Auto/dialog", preview)
        self.assertIn("Submission option: waitForConfirmation=True", preview)
        self.assertIn("Submission option: reuseExistingIfPossible=True", preview)
        self.assertIn("native analysis launch path", preview)
        self.assertIn("do not approve an overwrite", preview)
        self.assertIn("will be saved before submission", preview)
        self.assertIn("native simulation table and queue lifecycle", preview)
        self.assertIn("SiteCluster may receive every required simulation", preview)
        self.assertIn("remain set for the current RFPro session", preview)
        self.assertIn("starts the analysis now", preview)
        self.assertIn("FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR=0.5", preview)
        self.assertIn("FEMIZER_WAVEGUIDE_VERTICAL_FACTOR=2.0", preview)
        self.assertIn("FEM_ALWAYS_SOLVE_ON_FINEST_MESH=on", preview)

    def test_preview_warns_when_reuse_is_disabled(self) -> None:
        preview = MODULE.build_run_preview(FakeAnalysis(), 5, 3, False, False)
        self.assertIn("Existing-result policy: scripted overwrite", preview)
        self.assertIn("Submission option: waitForConfirmation=False", preview)
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
        self.assertEqual(
            calls,
            [
                (
                    analysis,
                    {
                        "waitForConfirmation": True,
                        "saveProject": True,
                        "reuseExistingIfPossible": True,
                    },
                )
            ],
        )

    def test_scripted_reuse_must_be_explicitly_selected(self) -> None:
        calls: list[dict[str, object]] = []

        def fake_run(_analysis: object, **kwargs: object) -> str:
            calls.append(kwargs)
            return "queued"

        MODULE.run_analysis_reusing_results(
            fake_run,
            FakeAnalysis(),
            reuse_existing=True,
            use_native_reuse_policy=False,
        )

        self.assertEqual(calls[0]["waitForConfirmation"], False)
        self.assertEqual(calls[0]["reuseExistingIfPossible"], True)

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
            self.assertTrue(kwargs["waitForConfirmation"])
            self.assertTrue(kwargs["saveProject"])
            return "queued"

        analysis = FakeAnalysis()
        result = MODULE.save_and_run_analysis(
            FakeProject(), fake_run, analysis, reuse_existing=False
        )
        self.assertEqual(result, "queued")
        self.assertEqual(events, ["save", "run"])

    def test_unsupported_persistent_reuse_attribute_is_never_accessed(self) -> None:
        events: list[str] = []

        class GuardedSettings:
            @property
            def reuseExistingResults(self) -> bool:
                raise AssertionError("run script must not read this attribute")

            @reuseExistingResults.setter
            def reuseExistingResults(self, _value: bool) -> None:
                raise AssertionError("run script must not write this attribute")

        class GuardedAnalysis:
            simulationSettings = GuardedSettings()

        class FakeProject:
            @staticmethod
            def saveActiveProject() -> None:
                events.append("save")

        def fake_run(_analysis: object, **_kwargs: object) -> str:
            events.append("run")
            return "queued"

        MODULE.save_and_run_analysis(
            FakeProject(), fake_run, GuardedAnalysis(), reuse_existing=True
        )

        self.assertEqual(events, ["save", "run"])

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
