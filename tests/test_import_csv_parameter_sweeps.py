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
    pass


class FakeSettings:
    def __init__(self) -> None:
        self.parameterSequences = FakeParameterSequenceList(["existing"])
        self.parameterSweepEnabled = False


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

    def test_unknown_reserved_column_is_rejected(self) -> None:
        path = self.write_csv("W,__group__\n0.4 mm,g1\n")
        with self.assertRaisesRegex(ValueError, "Unknown reserved"):
            MODULE.read_sweep_csv(path)

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


if __name__ == "__main__":
    unittest.main()
