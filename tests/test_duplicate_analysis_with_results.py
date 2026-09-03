from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "duplicate_analysis_with_results.py"
SPEC = importlib.util.spec_from_file_location("duplicate_analysis_with_results", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeAnalysis:
    def __init__(
        self,
        name: str,
        result_root: Path,
        group: str,
        simulation_path: str,
        relative_duplicate_group_path: bool = False,
        results_registered: bool = True,
    ) -> None:
        self.name = name
        self.result_root = result_root
        self.simulationGroup = group
        self.simulationPath = simulation_path
        self.relative_duplicate_group_path = relative_duplicate_group_path
        self.results_registered = results_registered
        self.settings = {"frequency": "20 GHz"}

    @property
    def simulationGroupPath(self) -> str:
        if self.relative_duplicate_group_path and self.simulationGroup != "000001":
            return f"./{self.simulationGroup}"
        return str(self.result_root / self.simulationGroup)

    def clone(self):
        duplicate = FakeAnalysis(
            self.name,
            self.result_root,
            self.simulationGroup,
            self.simulationPath,
            self.relative_duplicate_group_path,
            False,
        )
        duplicate.settings = dict(self.settings)
        return duplicate


class FakeAnalyses:
    def __init__(self, values) -> None:
        self.values = list(values)

    def names(self):
        return [value.name for value in self.values]

    def index(self, name: str) -> int:
        return self.names().index(name)

    def append(self, value) -> int:
        self.values.append(value)
        return len(self.values) - 1

    def __getitem__(self, index: int):
        return self.values[index]

    def __delitem__(self, index: int) -> None:
        del self.values[index]


class FakeSimulationList(list):
    def __init__(self, next_group: str = "000002", values=()) -> None:
        super().__init__(values)
        self.next_group = next_group
        self.refresh_calls = 0

    def getNextSimulationGroup(self) -> str:
        return self.next_group

    def refresh(self) -> None:
        self.refresh_calls += 1


class FakeSimulation:
    def __init__(self, path: str) -> None:
        self.path = path
        self.isRunning = False
        self.status = "Completed"
        self.queue_calls = 0

    def simulationPath(self) -> str:
        return self.path

    def setQueued(self, _queued=True) -> None:
        self.queue_calls += 1


class FakeProject:
    def __init__(self, analyses, simulations=None, empty_registration=False) -> None:
        self.analyses = FakeAnalyses(analyses)
        self.simulations = simulations or FakeSimulationList()
        self.empty_registration = empty_registration
        self.create_calls = []
        self.save_calls = 0
        self.saved_analysis_count = len(self.analyses.values)

    def __enter__(self):
        return self

    def __exit__(self, _kind, _value, _traceback) -> None:
        return None

    def saveActiveProject(self) -> None:
        self.save_calls += 1
        self.saved_analysis_count = len(self.analyses.values)

    def createSimulationsFromAnalysis(self, *arguments):
        if len(self.analyses.values) != self.saved_analysis_count:
            raise RuntimeError("Cannot create simulation sweep: there are unsaved changes")
        self.create_calls.append(arguments)
        if self.empty_registration:
            return []
        existing_paths = arguments[2]
        analysis = arguments[3]
        created = [FakeSimulation(path) for path in existing_paths]
        self.simulations.extend(created)
        analysis.results_registered = True
        return created


class FakeAnalysisOutput:
    def __init__(self, analysis: FakeAnalysis, omit_duplicate: bool = False) -> None:
        self.analysis = analysis
        self.omit_duplicate = omit_duplicate

    def getAvailableSimulationIds(self):
        if not self.analysis.results_registered or (
            self.omit_duplicate and self.analysis.simulationGroup != "000001"
        ):
            return []
        return ["000001", "000002"]

    def getAvailableSimulationPaths(self):
        if not self.analysis.results_registered or (
            self.omit_duplicate and self.analysis.simulationGroup != "000001"
        ):
            return []
        root = self.analysis.result_root / self.analysis.simulationGroup
        return [str(root / "000001"), str(root / "000002")]


class FakeOutputModule:
    def __init__(self, omit_duplicate: bool = False) -> None:
        self.omit_duplicate = omit_duplicate

    def AnalysisOutput(self, analysis):
        return FakeAnalysisOutput(analysis, self.omit_duplicate)


class FakeEmpro:
    def __init__(self, omit_duplicate: bool = False) -> None:
        self.output = FakeOutputModule(omit_duplicate)


class EmptyOutputModule:
    class AnalysisOutput:
        def __init__(self, _analysis) -> None:
            pass

        @staticmethod
        def getAvailableSimulationIds():
            return []

        @staticmethod
        def getAvailableSimulationPaths():
            return []


class EmptyEmpro:
    output = EmptyOutputModule()


def make_source(root: Path) -> FakeAnalysis:
    group = root / "000001"
    for simulation_id in ("000001", "000002"):
        simulation = group / simulation_id
        (simulation / "emds_dsn" / "design").mkdir(parents=True)
        (simulation / ".reuse.hash").write_text(
            f"hash-{simulation_id}", encoding="utf-8"
        )
        (simulation / "emds_dsn" / "design" / ".reusable").write_text(
            "", encoding="utf-8"
        )
    return FakeAnalysis("RF Setup", root, "000001", str(group / "000001"))


class DuplicateAnalysisTests(unittest.TestCase):
    def test_default_duplicate_name_skips_existing_copy_names(self) -> None:
        self.assertEqual(
            MODULE.default_duplicate_name(
                "RF Setup", ["RF Setup", "RF Setup Copy", "RF Setup Copy 2"]
            ),
            "RF Setup Copy 3",
        )

    def test_plan_uses_new_group_and_requires_all_results_inside_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            project = FakeProject([source])

            plan = MODULE.prepare_duplicate_plan(
                FakeEmpro(), project, source, "RF Setup Copy"
            )

            self.assertEqual(plan.duplicate_group, "000002")
            self.assertEqual(plan.duplicate_group_path, root / "000002")
            self.assertEqual(plan.registered_result_ids, ("000001", "000002"))
            self.assertGreater(plan.source_size_bytes, 0)

    def test_clone_uses_group_without_deprecated_simulation_path_assignment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            project = FakeProject([source])
            plan = MODULE.prepare_duplicate_plan(
                FakeEmpro(), project, source, "RF Setup Copy"
            )

            duplicate = MODULE.clone_analysis_for_plan(source, plan)

            self.assertEqual(duplicate.name, "RF Setup Copy")
            self.assertEqual(duplicate.simulationGroup, "000002")
            self.assertEqual(duplicate.simulationPath, source.simulationPath)
            duplicate.settings["frequency"] = "40 GHz"
            self.assertEqual(source.settings["frequency"], "20 GHz")

    def test_relative_duplicate_group_path_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            source.relative_duplicate_group_path = True
            project = FakeProject([source])

            result = MODULE.duplicate_analysis_with_results(
                FakeEmpro(), project, source, "RF Setup Copy"
            )

            self.assertEqual(result.duplicate.simulationGroupPath, "./000002")
            self.assertEqual(result.verified_result_ids, ("000001", "000002"))

    def test_relative_result_paths_are_resolved_inside_duplicate_group(self) -> None:
        group = Path("C:/results/rfpro/000004")

        self.assertEqual(
            MODULE.resolve_result_path(Path("./000004/000026"), group),
            group / "000026",
        )
        self.assertEqual(
            MODULE.resolve_result_path(Path("./000026"), group),
            group / "000026",
        )

    def test_duplicate_copies_hidden_cache_data_and_registers_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            project = FakeProject([source])

            result = MODULE.duplicate_analysis_with_results(
                FakeEmpro(), project, source, "RF Setup Copy"
            )

            copied = root / "000002"
            self.assertTrue((copied / "000001" / ".reuse.hash").is_file())
            self.assertTrue(
                (copied / "000002" / "emds_dsn" / "design" / ".reusable").is_file()
            )
            self.assertEqual(project.analyses.names(), ["RF Setup", "RF Setup Copy"])
            self.assertEqual(result.verified_result_ids, ("000001", "000002"))
            # Source mapping, duplicate/group assignment, then registrations.
            self.assertEqual(project.save_calls, 3)
            self.assertEqual(project.simulations.refresh_calls, 0)
            self.assertEqual(len(project.create_calls), 1)
            create_call = project.create_calls[0]
            self.assertEqual(create_call[0:2], (True, False))
            self.assertEqual(
                create_call[2],
                [str(copied / "000001"), str(copied / "000002")],
            )
            self.assertIs(create_call[3], result.duplicate)
            self.assertEqual(create_call[4:], ({}, {}))
            self.assertTrue(all(sim.queue_calls == 0 for sim in project.simulations))

    def test_registered_result_mismatch_rolls_back_and_saves_removal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            project = FakeProject([source])

            with self.assertRaisesRegex(RuntimeError, "did not register the same"):
                MODULE.duplicate_analysis_with_results(
                    FakeEmpro(omit_duplicate=True),
                    project,
                    source,
                    "RF Setup Copy",
                )

            self.assertEqual(project.analyses.names(), ["RF Setup"])
            self.assertFalse((root / "000002").exists())
            self.assertTrue((root / "000001" / "000001" / ".reuse.hash").is_file())
            self.assertEqual(project.save_calls, 3)
            self.assertEqual(len(project.simulations), 0)
            self.assertEqual(project.simulations.refresh_calls, 1)

    def test_empty_rfpro_registration_rolls_back_and_saves_removal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            project = FakeProject([source], empty_registration=True)

            with self.assertRaisesRegex(RuntimeError, "returned no simulation records"):
                MODULE.duplicate_analysis_with_results(
                    FakeEmpro(), project, source, "RF Setup Copy"
                )

            self.assertEqual(project.analyses.names(), ["RF Setup"])
            self.assertFalse((root / "000002").exists())
            self.assertEqual(project.save_calls, 3)

    def test_running_or_queued_simulation_prevents_save_and_copy(self) -> None:
        class RunningSimulation:
            name = "Current solve"
            isRunning = True
            status = "Running"

            @staticmethod
            def simulationPath() -> str:
                return "results/000001/000001"

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            simulations = FakeSimulationList(values=[RunningSimulation()])
            project = FakeProject([source], simulations)

            with self.assertRaisesRegex(RuntimeError, "Wait for every RFPro simulation"):
                MODULE.duplicate_analysis_with_results(
                    FakeEmpro(), project, source, "RF Setup Copy"
                )

            self.assertEqual(project.save_calls, 0)
            self.assertFalse((root / "000002").exists())

    def test_duplicate_name_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            existing = FakeAnalysis("Existing", root, "000003", "")
            project = FakeProject([source, existing])

            with self.assertRaisesRegex(ValueError, "already exists"):
                MODULE.prepare_duplicate_plan(
                    FakeEmpro(), project, source, "Existing"
                )

    def test_analysis_without_registered_results_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = make_source(root)
            project = FakeProject([source])

            with self.assertRaisesRegex(RuntimeError, "no registered solved results"):
                MODULE.prepare_duplicate_plan(
                    EmptyEmpro(), project, source, "RF Setup Copy"
                )

    def test_confirmation_is_required_by_default(self) -> None:
        arguments = MODULE._parse_arguments([])
        self.assertFalse(arguments.yes)


if __name__ == "__main__":
    unittest.main()
