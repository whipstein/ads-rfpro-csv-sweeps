from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "import_csv_parameter_sweeps.py"
SPEC = importlib.util.spec_from_file_location("import_csv_parameter_sweeps", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeSingleParameterSweep:
    def __init__(self) -> None:
        self.parameterName = ""
        self.values: list[str] = []

    def setParameterValues(self, value: str) -> None:
        self.values = [value]


class FakeParameterSequence(list):
    pass


class FakeSimulationModule:
    ParameterSequence = FakeParameterSequence
    SingleParameterSweep = FakeSingleParameterSweep


class FakeEmpro:
    simulation = FakeSimulationModule


class FakeParameterSequenceList(list):
    def __init__(self, values=()) -> None:
        super().__init__(values)
        self.clear_calls = 0
        self.append_calls = 0

    def clear(self) -> None:
        self.clear_calls += 1
        super().clear()

    def append(self, value) -> None:
        self.append_calls += 1
        super().append(value)


class FakeSettings:
    def __init__(self, sequences=("existing",), enabled: bool = False) -> None:
        self.parameterSequences = FakeParameterSequenceList(sequences)
        self.parameterSweepEnabled = enabled


class FakeEvaluatedSweep:
    def __init__(self, name: str, values) -> None:
        self.parameterName = name
        self.parameterValues = list(values)


def evaluated_sequence(**parameters):
    return FakeParameterSequence(
        FakeEvaluatedSweep(name, values) for name, values in parameters.items()
    )


class FakeParameters:
    def __init__(self, names: list[str], noneditable: set[str] | None = None) -> None:
        self._names = names
        self._noneditable = noneditable or set()

    def names(self) -> list[str]:
        return self._names

    def isEditable(self, name: str) -> bool:
        return name not in self._noneditable


class FakeProject:
    def __init__(self, parameters: FakeParameters) -> None:
        self.parameters = parameters


class CSVImportTests(unittest.TestCase):
    def write_csv(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "sweeps.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_rows_are_complete_independent_cases(self) -> None:
        path = self.write_csv(
            "__case__,__enabled__,W,L,__comment__\n"
            "case-a,yes,0.40 mm,1.2 mm,training\n"
            "case-b,no,0.50 mm,1.3 mm,disabled\n"
            "case-c,true,0.60 mm,1.4 mm,verification\n"
        )

        cases = MODULE.read_sweep_csv(path)

        self.assertEqual([case.label for case in cases], ["case-a", "case-c"])
        self.assertEqual(
            cases[0].parameters,
            (("W", "0.40 mm"), ("L", "1.2 mm")),
        )
        self.assertEqual(cases[1].source_row, 4)

    def test_missing_value_is_rejected(self) -> None:
        path = self.write_csv("W,L\n0.4 mm,\n")
        with self.assertRaisesRegex(ValueError, "Every independent case must be complete"):
            MODULE.read_sweep_csv(path)

    def test_comma_inside_value_is_rejected(self) -> None:
        path = self.write_csv('W,L\n"0.4 mm,0.5 mm",1.2 mm\n')
        with self.assertRaisesRegex(ValueError, "contains a comma"):
            MODULE.read_sweep_csv(path)

    def test_unknown_reserved_column_is_ignored(self) -> None:
        path = self.write_csv("W,__group__\n0.4 mm,g1\n")
        data = MODULE.read_sweep_csv_data(path, ["W"])

        self.assertEqual(data.cases[0].parameters, (("W", "0.4 mm"),))
        self.assertEqual(data.ignored_columns, ("__group__",))

    def test_nonparameter_columns_are_ignored_using_live_project_names(self) -> None:
        path = self.write_csv(
            "verification_sequence,W,L,notes\n"
            ",0.4 mm,1.2 mm,training\n"
        )

        data = MODULE.read_sweep_csv_data(path, ["W", "L"])

        self.assertEqual(data.parameter_names, ("W", "L"))
        self.assertEqual(
            data.ignored_columns,
            ("verification_sequence", "notes"),
        )
        self.assertEqual(
            data.cases[0].parameters,
            (("W", "0.4 mm"), ("L", "1.2 mm")),
        )

    def test_csv_requires_at_least_one_live_parameter_heading(self) -> None:
        path = self.write_csv("verification_sequence,notes\n1,check\n")
        with self.assertRaisesRegex(ValueError, "no headings matching"):
            MODULE.read_sweep_csv_data(path, ["W", "L"])

    def test_global_value_scale_wraps_each_rfpro_expression(self) -> None:
        path = self.write_csv("W,L\n400,0.5 mm\n")

        data = MODULE.read_sweep_csv_data(path, ["W", "L"], 1.0e-6)

        self.assertEqual(data.value_scale, 1.0e-6)
        self.assertEqual(
            data.cases[0].parameters,
            (("W", "(400)*1e-06"), ("L", "(0.5 mm)*1e-06")),
        )
        self.assertEqual(MODULE.scale_sweep_expression("2 mm", 1.0), "2 mm")
        with self.assertRaisesRegex(ValueError, "must be finite"):
            MODULE.validated_value_scale(float("nan"))

    def test_project_parameter_validation(self) -> None:
        case = MODULE.SweepCase(2, "one", (("W", "1 mm"), ("L", "2 mm")))
        project = FakeProject(FakeParameters(["W", "L"]))
        MODULE.validate_cases_against_project(project, [case])

        with self.assertRaisesRegex(ValueError, "not RFPro project parameters"):
            MODULE.validate_cases_against_project(
                FakeProject(FakeParameters(["W"])), [case]
            )
        with self.assertRaisesRegex(ValueError, "not editable"):
            MODULE.validate_cases_against_project(
                FakeProject(FakeParameters(["W", "L"], {"L"})), [case]
            )

    def test_one_native_sequence_is_built_per_csv_row(self) -> None:
        cases = [
            MODULE.SweepCase(2, "a", (("W", "1 mm"), ("L", "2 mm"))),
            MODULE.SweepCase(3, "b", (("W", "3 mm"), ("L", "4 mm"))),
        ]

        sequences = MODULE.build_parameter_sequences(FakeEmpro, cases)

        self.assertEqual(len(sequences), 2)
        self.assertEqual(
            [(sweep.parameterName, sweep.values) for sweep in sequences[0]],
            [("W", ["1 mm"]), ("L", ["2 mm"])],
        )
        settings = FakeSettings()
        before, after = MODULE.install_parameter_sequences(
            settings, sequences, mode="replace"
        )
        self.assertEqual((before, after), (1, 2))
        self.assertTrue(settings.parameterSweepEnabled)

    def test_append_preserves_existing_sequences(self) -> None:
        settings = FakeSettings()
        before, after = MODULE.install_parameter_sequences(
            settings, [["new"]], mode="append"
        )
        self.assertEqual((before, after), (1, 2))
        self.assertEqual(settings.parameterSequences[0], "existing")

    def test_append_plan_retains_matches_and_adds_only_new_conditions(self) -> None:
        existing = evaluated_sequence(W=[1.0e-3], L=[2.0e-3])
        matching = evaluated_sequence(W=[1.0e-3 + 5.0e-13], L=[2.0e-3])
        new = evaluated_sequence(W=[3.0e-3], L=[4.0e-3])
        duplicate_new = evaluated_sequence(L=[4.0e-3], W=[3.0e-3])
        settings = FakeSettings([existing], enabled=True)

        plan = MODULE.plan_parameter_sequence_import(
            settings,
            [matching, new, duplicate_new],
            "append",
            relative_tolerance=1.0e-9,
            absolute_tolerance=1.0e-15,
        )

        self.assertEqual(plan.reused_existing_count, 1)
        self.assertEqual(plan.added_count, 1)
        self.assertEqual(plan.duplicate_csv_count, 1)
        self.assertEqual(plan.removed_existing_count, 0)
        self.assertIs(plan.final_sequences[0], existing)
        self.assertIs(plan.final_sequences[1], new)

        before, after = MODULE.apply_parameter_sequence_import_plan(settings, plan)
        self.assertEqual((before, after), (1, 2))
        self.assertEqual(settings.parameterSequences.clear_calls, 0)
        self.assertEqual(settings.parameterSequences.append_calls, 1)
        self.assertIs(settings.parameterSequences[0], existing)

    def test_all_matching_append_is_a_true_no_op(self) -> None:
        existing = evaluated_sequence(W=[1.0e-3])
        matching = evaluated_sequence(W=[1.0e-3 + 1.0e-14])
        settings = FakeSettings([existing], enabled=True)

        plan = MODULE.plan_parameter_sequence_import(
            settings,
            [matching],
            "append",
            relative_tolerance=1.0e-9,
            absolute_tolerance=1.0e-15,
        )
        MODULE.apply_parameter_sequence_import_plan(settings, plan)

        self.assertFalse(plan.mutation_required)
        self.assertEqual(settings.parameterSequences.clear_calls, 0)
        self.assertEqual(settings.parameterSequences.append_calls, 0)
        self.assertIs(settings.parameterSequences[0], existing)

    def test_replace_plan_reuses_matching_native_objects(self) -> None:
        retained = evaluated_sequence(W=[1.0e-3])
        stale = evaluated_sequence(W=[2.0e-3])
        matching = evaluated_sequence(W=[1.0e-3 + 5.0e-13])
        new = evaluated_sequence(W=[3.0e-3])
        settings = FakeSettings([retained, stale], enabled=True)

        plan = MODULE.plan_parameter_sequence_import(
            settings,
            [matching, new],
            "replace",
            relative_tolerance=1.0e-9,
            absolute_tolerance=1.0e-15,
        )

        self.assertEqual(plan.reused_existing_count, 1)
        self.assertEqual(plan.added_count, 1)
        self.assertEqual(plan.removed_existing_count, 1)
        self.assertIs(plan.final_sequences[0], retained)
        self.assertIs(plan.final_sequences[1], new)

    def test_match_tolerances_must_be_finite_and_nonnegative(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite nonnegative"):
            MODULE.validated_match_tolerance(-1.0, "Tolerance")
        with self.assertRaisesRegex(ValueError, "finite nonnegative"):
            MODULE.validated_match_tolerance(float("inf"), "Tolerance")

    def test_import_mode_can_be_explicit_or_interactive(self) -> None:
        settings = FakeSettings()
        self.assertEqual(MODULE._choose_import_mode(settings, "replace"), "replace")
        self.assertEqual(MODULE._choose_import_mode(settings, "append"), "append")
        self.assertEqual(MODULE._parse_arguments([]).mode, "ask")
        self.assertEqual(MODULE._parse_arguments(["--scale", "1e-6"]).scale, 1.0e-6)
        with self.assertRaisesRegex(ValueError, "Unknown import mode"):
            MODULE._choose_import_mode(settings, "invalid")


if __name__ == "__main__":
    unittest.main()
