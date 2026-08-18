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


class FakeSimulation:
    def __init__(
        self,
        simulation_id: str,
        status: str = "Ready",
        dequeue_works: bool = True,
        queue_error: Exception | None = None,
    ) -> None:
        self._simulation_id = simulation_id
        self.status = status
        self.dequeue_works = dequeue_works
        self.queue_error = queue_error
        self.queue_calls: list[bool] = []

    def id(self) -> str:
        return self._simulation_id

    def setQueued(self, queued: bool) -> None:
        self.queue_calls.append(queued)
        if queued and self.queue_error is not None:
            raise self.queue_error
        if queued:
            self.status = "Queued"
        elif self.dequeue_works:
            self.status = "Ready"


class FakeSimulationList(list[FakeSimulation]):
    def __init__(self, *simulations: FakeSimulation) -> None:
        super().__init__(simulations)
        self.isQueueHeld = False
        self.refresh_count = 0

    def refresh(self) -> None:
        self.refresh_count += 1


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
        self.assertIn("Maximum active simulations: 1", preview)
        self.assertIn("stop submitting new jobs after the first error", preview)
        self.assertIn("staged under queue hold", preview)
        self.assertIn("remain set for the current RFPro session", preview)
        self.assertIn("stays open until every submitted simulation finishes", preview)
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
        self.assertEqual(arguments.max_concurrent, 1)
        self.assertFalse(arguments.continue_on_error)

    def test_max_concurrent_argument_must_be_positive(self) -> None:
        with self.assertRaises(SystemExit):
            MODULE._parse_arguments(["--max-concurrent", "0"])

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

    def test_staging_holds_then_unqueues_every_selected_simulation(self) -> None:
        first = FakeSimulation("000001")
        second = FakeSimulation("000002")
        simulations = FakeSimulationList(first, second)
        events: list[str] = []

        def submit() -> None:
            self.assertTrue(simulations.isQueueHeld)
            events.append("submit")
            first.setQueued(True)
            second.setQueued(True)

        staged = MODULE.stage_analysis_simulations(simulations, submit, lambda: None)

        self.assertEqual(staged, [first, second])
        self.assertEqual(events, ["submit"])
        self.assertEqual(first.queue_calls, [True, False])
        self.assertEqual(second.queue_calls, [True, False])
        self.assertEqual([first.status, second.status], ["Ready", "Ready"])
        self.assertFalse(simulations.isQueueHeld)

    def test_staging_refuses_to_mix_with_an_active_queue(self) -> None:
        simulations = FakeSimulationList(FakeSimulation("old", "Running"))
        submit_called = False

        def submit() -> None:
            nonlocal submit_called
            submit_called = True

        with self.assertRaisesRegex(RuntimeError, "requires an idle RFPro queue"):
            MODULE.stage_analysis_simulations(simulations, submit, lambda: None)

        self.assertFalse(submit_called)
        self.assertFalse(simulations.isQueueHeld)

    def test_failed_dequeue_leaves_rfpro_queue_held(self) -> None:
        simulation = FakeSimulation("000001", dequeue_works=False)
        simulations = FakeSimulationList(simulation)

        def submit() -> None:
            simulation.setQueued(True)

        with self.assertRaisesRegex(RuntimeError, "queue was left HELD"):
            MODULE.stage_analysis_simulations(simulations, submit, lambda: None)

        self.assertTrue(simulations.isQueueHeld)
        self.assertEqual(simulation.status, "Queued")

    def test_unexpected_hold_release_is_reasserted_for_running_jobs(self) -> None:
        simulation = FakeSimulation("000001")
        simulations = FakeSimulationList(simulation)

        def submit() -> None:
            simulation.status = "Running"
            simulations.isQueueHeld = False

        with self.assertRaisesRegex(RuntimeError, "queue was left HELD"):
            MODULE.stage_analysis_simulations(simulations, submit, lambda: None)

        self.assertTrue(simulations.isQueueHeld)
        self.assertEqual(simulation.status, "Running")

    def test_scheduler_maintains_sliding_concurrency_limit(self) -> None:
        staged = [FakeSimulation(f"{index:06d}") for index in range(1, 5)]
        simulations = FakeSimulationList(*staged)
        observed_active_counts: list[int] = []

        def process_events() -> None:
            active = [
                simulation
                for simulation in simulations
                if simulation.status in MODULE._ONGOING_SIMULATION_STATUSES
            ]
            observed_active_counts.append(len(active))
            if active:
                active[0].status = "Completed"

        result = MODULE.run_staged_simulations_with_limit(
            simulations,
            staged,
            max_concurrent_simulations=2,
            stop_submitting_on_error=True,
            process_events=process_events,
            sleep=lambda _seconds: None,
            poll_seconds=0,
        )

        self.assertEqual(result.submitted_ids, ("000001", "000002", "000003", "000004"))
        self.assertEqual(result.completed_ids, result.submitted_ids)
        self.assertEqual(result.failed, ())
        self.assertEqual(result.remaining_ids, ())
        self.assertLessEqual(max(observed_active_counts), 2)
        self.assertIn(2, observed_active_counts)

    def test_scheduler_stops_new_submissions_after_first_failure(self) -> None:
        staged = [FakeSimulation(f"{index:06d}") for index in range(1, 4)]
        simulations = FakeSimulationList(*staged)

        def process_events() -> None:
            for simulation in simulations:
                if simulation.status == "Queued":
                    simulation.status = "Failed"
                    break

        result = MODULE.run_staged_simulations_with_limit(
            simulations,
            staged,
            max_concurrent_simulations=1,
            stop_submitting_on_error=True,
            process_events=process_events,
            sleep=lambda _seconds: None,
            poll_seconds=0,
        )

        self.assertEqual(result.submitted_ids, ("000001",))
        self.assertEqual(result.failed, (("000001", "Failed"),))
        self.assertEqual(result.remaining_ids, ("000002", "000003"))

    def test_batched_runner_saves_before_staging_and_preserves_reuse_flags(self) -> None:
        simulation = FakeSimulation("000001")
        simulations = FakeSimulationList(simulation)
        events: list[str] = []

        class FakeProject:
            def __init__(self) -> None:
                self.simulations = simulations

            @staticmethod
            def saveActiveProject() -> None:
                events.append("save")

        def fake_run(_analysis: object, **kwargs: object) -> None:
            events.append("run")
            self.assertTrue(simulations.isQueueHeld)
            self.assertTrue(kwargs["waitForConfirmation"])
            self.assertTrue(kwargs["reuseExistingIfPossible"])
            simulation.setQueued(True)

        def process_events() -> None:
            if simulation.queue_calls == [True, False, True]:
                simulation.status = "Completed"

        result = MODULE.save_and_run_analysis_batched(
            FakeProject(),
            fake_run,
            FakeAnalysis(),
            reuse_existing=True,
            max_concurrent_simulations=1,
            process_events=process_events,
            sleep=lambda _seconds: None,
            poll_seconds=0,
        )

        self.assertEqual(events, ["save", "run"])
        self.assertEqual(result.completed_ids, ("000001",))


if __name__ == "__main__":
    unittest.main()
