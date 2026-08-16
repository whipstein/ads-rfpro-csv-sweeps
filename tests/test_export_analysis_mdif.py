from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "export_analysis_mdif.py"
SPEC = importlib.util.spec_from_file_location("export_analysis_mdif", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeDimension:
    def __init__(self, values: list[float]) -> None:
        self.values = values

    def at(self, index: int) -> float:
        return self.values[index]


class FakeDataSet:
    def __init__(self, frequencies: list[float], values: list[complex]) -> None:
        self.frequency = FakeDimension(frequencies)
        self.values = values

    def dimensions(self) -> list[FakeDimension]:
        return [self.frequency]

    def at(self, index: int) -> complex:
        return self.values[index]

    def __len__(self) -> int:
        return len(self.values)


class FakeMatrix:
    def __init__(self) -> None:
        frequency = [1.0e9, 2.0e9]
        self.rows = [1, 2]
        self.cols = [1, 2]
        self.data = {
            (1, 1): FakeDataSet(frequency, [0.1 + 0.2j, 0.2 + 0.3j]),
            (1, 2): FakeDataSet(frequency, [0.4 + 0.5j, 0.5 + 0.6j]),
            (2, 1): FakeDataSet(frequency, [0.7 + 0.8j, 0.8 + 0.9j]),
            (2, 2): FakeDataSet(frequency, [1.0 + 1.1j, 1.1 + 1.2j]),
        }

    def __contains__(self, key: tuple[int, int]) -> bool:
        return key in self.data

    def __getitem__(self, key: tuple[int, int]) -> FakeDataSet:
        return self.data[key]


class FakeSweep:
    def __init__(self, name: str, values: list[str]) -> None:
        self.parameterName = name
        self.values = values

    def getParameterValues(self, mode: str = "") -> list[str]:
        return self.values


class FakeSettings:
    def __init__(self) -> None:
        self.parameterSequences = [
            [FakeSweep("W", ["1 mm", "2 mm"]), FakeSweep("L", ["3 mm"])],
            [FakeSweep("W", ["5 mm"]), FakeSweep("L", ["6 mm"])],
        ]


class MDIFExportTests(unittest.TestCase):
    def test_parameter_metadata_parsing(self) -> None:
        self.assertEqual(
            MODULE.parse_parameter_string("W: 1 mm, L=2 mm"),
            {"W": "1 mm", "L": "2 mm"},
        )
        self.assertEqual(
            MODULE._coerce_parameter_mapping([("W", 1.0), ("L", "2 mm")]),
            {"W": "1.0", "L": "2 mm"},
        )

    def test_configured_sequences_expand_independently(self) -> None:
        cases = MODULE.configured_parameter_cases(FakeSettings())
        self.assertEqual(
            cases,
            [
                {"W": "1 mm", "L": "3 mm"},
                {"W": "2 mm", "L": "3 mm"},
                {"W": "5 mm", "L": "6 mm"},
            ],
        )

    def test_smatrix_is_exported_in_row_major_order(self) -> None:
        block = MODULE.smatrix_to_block(
            FakeMatrix(), "000001", {"W": "1 mm", "L": "2 mm"}
        )
        self.assertEqual(block.labels, ("S11", "S12", "S21", "S22"))
        self.assertEqual(block.frequencies_hz, (1.0e9, 2.0e9))
        self.assertEqual(block.values[0][2], 0.7 + 0.8j)

    def test_inconsistent_sparameter_frequency_grid_is_rejected(self) -> None:
        matrix = FakeMatrix()
        matrix.data[(2, 2)] = FakeDataSet(
            [1.0e9, 2.1e9], [1.0 + 1.1j, 1.1 + 1.2j]
        )
        with self.assertRaisesRegex(ValueError, "different frequency grid"):
            MODULE.smatrix_to_block(matrix, "000001", {"W": "1 mm"})

    def test_generic_mdif_contains_one_block_and_var_metadata(self) -> None:
        block = MODULE.smatrix_to_block(
            FakeMatrix(), "000001", {"W": "1 mm", "L": "2 mm"}
        )
        text = MODULE.render_mdif([block], 50.0)
        self.assertIn("VAR W=1mm", text)
        self.assertIn("VAR L=2mm", text)
        self.assertIn("% Freq S11 S12 S21 S22", text)
        self.assertIn("# Hz S RI R 50", text)
        self.assertEqual(text.count("BEGIN ACDATA"), 1)
        self.assertEqual(text.count("END"), 1)

    def test_atomic_writer_replaces_complete_destination(self) -> None:
        block = MODULE.smatrix_to_block(
            FakeMatrix(), "000001", {"W": "1 mm", "L": "2 mm"}
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.mdif"
            path.write_text("old", encoding="utf-8")
            MODULE.write_mdif_atomic(path, [block], 50.0)
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("! RFPro swept S-parameter results"))
            self.assertNotIn("old", text)

    def test_invalid_mdif_parameter_name_is_rejected(self) -> None:
        block = MODULE.smatrix_to_block(FakeMatrix(), "1", {"bad name": "1 mm"})
        with self.assertRaisesRegex(ValueError, "not a valid"):
            MODULE.render_mdif([block], 50.0)


if __name__ == "__main__":
    unittest.main()
