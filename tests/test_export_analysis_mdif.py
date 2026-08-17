from __future__ import annotations

import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "export_analysis_mdif.py"
SPEC = importlib.util.spec_from_file_location("export_analysis_mdif", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

POSITIVE_RANGE = (MODULE.FrequencyRegion(1.0e9, 2.0e9),)
DC_AND_POSITIVE_RANGE = (
    MODULE.FrequencyRegion(0.0, 0.0),
    MODULE.FrequencyRegion(1.0e9, 2.0e9),
)


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


class FakeEvaluatedCircuitMatrix:
    def __init__(self, values: list[list[complex]]) -> None:
        self.values = values

    def __call__(self, row: int, column: int) -> complex:
        return self.values[row][column]


class FakeCircuitMatrix:
    def __init__(self) -> None:
        self._frequencies = [1.0e9, 2.0e9]
        self.sampled_frequencies: list[float] = []
        self._values = {
            1.0e9: [
                [0.1 + 0.2j, 0.4 + 0.5j],
                [0.7 + 0.8j, 1.0 + 1.1j],
            ],
            2.0e9: [
                [0.2 + 0.3j, 0.5 + 0.6j],
                [0.8 + 0.9j, 1.1 + 1.2j],
            ],
        }

    @staticmethod
    def numberOfPorts() -> int:
        return 2

    def frequencies(self) -> object:
        return types.SimpleNamespace(data=self._frequencies)

    def Smatrix(self, frequency: float) -> FakeEvaluatedCircuitMatrix:
        self.sampled_frequencies.append(frequency)
        if frequency in self._values:
            return FakeEvaluatedCircuitMatrix(self._values[frequency])
        ratio = (frequency - self._frequencies[0]) / (
            self._frequencies[1] - self._frequencies[0]
        )
        first = self._values[self._frequencies[0]]
        last = self._values[self._frequencies[1]]
        interpolated = [
            [
                first[row][column]
                + (last[row][column] - first[row][column]) * ratio
                for column in range(2)
            ]
            for row in range(2)
        ]
        return FakeEvaluatedCircuitMatrix(interpolated)


class FakeDcCircuitMatrix(FakeCircuitMatrix):
    def __init__(self) -> None:
        super().__init__()
        # RFPro's circuit sampling may represent a configured DC solve with a
        # small positive internal sample. The analysis plan remains exactly DC.
        self._frequencies = [1.0e-6, 1.0e9, 2.0e9]
        self._values[0.0] = [
            [0.0 + 0.0j, 0.0 + 0.0j],
            [0.0 + 0.0j, 0.0 + 0.0j],
        ]
        self._values[1.0e-6] = self._values[0.0]


class FakeSweep:
    def __init__(self, name: str, values: list[str]) -> None:
        self.parameterName = name
        self.values = values

    def getParameterValues(self, mode: str = "") -> list[str]:
        return self.values


class FakeFrequencyPlan:
    def __init__(
        self,
        start: float,
        stop: float,
        enabled: bool = True,
        sweep_type: str | None = None,
        legacy_type: str | None = None,
        compute_type: str = "Simulated",
    ) -> None:
        self.startFrequency = start
        self.stopFrequency = stop
        self.enabled = enabled
        self.sweepType = sweep_type or ("Single" if start == stop else "Linear")
        self.type = legacy_type or self.sweepType
        self.computeType = compute_type


class FakeFrequencySettings:
    def __init__(self, plans: list[FakeFrequencyPlan]) -> None:
        self._plans = plans

    def femFrequencyPlanList(self) -> list[FakeFrequencyPlan]:
        return self._plans


class FakeSettings:
    def __init__(self) -> None:
        self.parameterSequences = [
            [FakeSweep("W", ["1 mm", "2 mm"]), FakeSweep("L", ["3 mm"])],
            [FakeSweep("W", ["5 mm"]), FakeSweep("L", ["6 mm"])],
        ]


class FakeSingleCaseSettings:
    def __init__(self) -> None:
        self.parameterSequences = [[FakeSweep("W", ["1 mm"])]]


class FakeSimulationOutput:
    simulationPath = "/project/rfpro/000001/000002"

    @staticmethod
    def metadata() -> object:
        return object()


class FakeAnalysisOutput:
    def __init__(self, analysis: object) -> None:
        self.analysis = analysis

    @staticmethod
    def getAvailableSimulationIds() -> list[str]:
        return ["000002"]

    @staticmethod
    def getSimulation(simulation_id: str) -> FakeSimulationOutput:
        if simulation_id != "000002":
            raise KeyError(simulation_id)
        return FakeSimulationOutput()


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

    def test_circuit_matrix_is_exported_in_row_major_order(self) -> None:
        matrix = FakeCircuitMatrix()
        block = MODULE.circuit_matrix_to_block(
            matrix, "000001", {"W": "1 mm", "L": "2 mm"}
        )
        self.assertEqual(block.labels, ("S11", "S12", "S21", "S22"))
        self.assertEqual(block.frequencies_hz, (1.0e9, 2.0e9))
        self.assertEqual(block.values[0][2], 0.7 + 0.8j)
        self.assertEqual(matrix.sampled_frequencies, [1.0e9, 2.0e9])

    def test_frequency_step_parser_accepts_engineering_units(self) -> None:
        self.assertEqual(MODULE.parse_frequency_step("100 MHz"), 100.0e6)
        self.assertEqual(MODULE.parse_frequency_step("2.5GHz"), 2.5e9)
        self.assertEqual(MODULE.parse_frequency_step("1000"), 1000.0)
        with self.assertRaisesRegex(ValueError, "positive"):
            MODULE.parse_frequency_step("0 MHz")
        with self.assertRaisesRegex(ValueError, "optionally followed"):
            MODULE.parse_frequency_step("one GHz")

    def test_point_count_grid_is_uniform_and_includes_endpoints(self) -> None:
        grid = MODULE.build_frequency_grid(
            [1.0e9, 2.0e9],
            MODULE.FrequencyGridRequest("points", point_count=5),
            configured_regions=POSITIVE_RANGE,
        )
        self.assertEqual(
            grid,
            (1.0e9, 1.25e9, 1.5e9, 1.75e9, 2.0e9),
        )

    def test_step_grid_preserves_requested_steps_and_appends_stop(self) -> None:
        grid = MODULE.build_frequency_grid(
            [1.0e9, 2.0e9],
            MODULE.FrequencyGridRequest("step", step_hz=400.0e6),
            configured_regions=POSITIVE_RANGE,
        )
        self.assertEqual(grid, (1.0e9, 1.4e9, 1.8e9, 2.0e9))
        exact_grid = MODULE.build_frequency_grid(
            [1.0e9, 2.0e9],
            MODULE.FrequencyGridRequest("step", step_hz=500.0e6),
            configured_regions=POSITIVE_RANGE,
        )
        self.assertEqual(exact_grid, (1.0e9, 1.5e9, 2.0e9))
        wider_than_span = MODULE.build_frequency_grid(
            [1.0e9, 2.0e9],
            MODULE.FrequencyGridRequest("step", step_hz=10.0e12),
            configured_regions=POSITIVE_RANGE,
        )
        self.assertEqual(wider_than_span, (1.0e9, 2.0e9))

    def test_step_grid_preserves_dc_without_filling_the_gap(self) -> None:
        grid = MODULE.build_frequency_grid(
            [1.0e-6, 1.0e9, 1.5e9, 2.0e9],
            MODULE.FrequencyGridRequest("step", step_hz=400.0e6),
            configured_regions=DC_AND_POSITIVE_RANGE,
        )
        self.assertEqual(grid, (0.0, 1.0e9, 1.4e9, 1.8e9, 2.0e9))
        self.assertNotIn(400.0e6, grid)
        self.assertNotIn(800.0e6, grid)

    def test_each_configured_range_is_sampled_without_filling_gaps(self) -> None:
        regions = (
            MODULE.FrequencyRegion(0.0, 0.0),
            MODULE.FrequencyRegion(1.0e9, 2.0e9),
            MODULE.FrequencyRegion(3.0e9, 4.0e9),
        )
        grid = MODULE.build_frequency_grid(
            [1.0e-6, 1.0e9, 4.0e9],
            MODULE.FrequencyGridRequest("step", step_hz=600.0e6),
            configured_regions=regions,
        )
        self.assertEqual(
            grid,
            (0.0, 1.0e9, 1.6e9, 2.0e9, 3.0e9, 3.6e9, 4.0e9),
        )
        self.assertNotIn(2.6e9, grid)

    def test_point_count_applies_per_configured_range(self) -> None:
        grid = MODULE.build_frequency_grid(
            [1.0e-6, 1.0e9, 2.0e9],
            MODULE.FrequencyGridRequest("points", point_count=3),
            configured_regions=DC_AND_POSITIVE_RANGE,
        )
        self.assertEqual(grid, (0.0, 1.0e9, 1.5e9, 2.0e9))
        dc_only = MODULE.build_frequency_grid(
            [1.0e-6],
            MODULE.FrequencyGridRequest("points", point_count=3),
            configured_regions=(MODULE.FrequencyRegion(0.0, 0.0),),
        )
        self.assertEqual(dc_only, (0.0,))

    def test_circuit_export_does_not_evaluate_inside_dc_to_range_gap(self) -> None:
        matrix = FakeDcCircuitMatrix()
        block = MODULE.circuit_matrix_to_block(
            matrix,
            "000001",
            {"W": "1 mm"},
            MODULE.FrequencyGridRequest("step", step_hz=400.0e6),
            configured_regions=DC_AND_POSITIVE_RANGE,
        )
        expected = (0.0, 1.0e9, 1.4e9, 1.8e9, 2.0e9)
        self.assertEqual(block.frequencies_hz, expected)
        self.assertEqual(matrix.sampled_frequencies, list(expected))

    def test_circuit_matrix_can_be_resampled_by_point_count(self) -> None:
        matrix = FakeCircuitMatrix()
        block = MODULE.circuit_matrix_to_block(
            matrix,
            "000001",
            {"W": "1 mm"},
            MODULE.FrequencyGridRequest("points", point_count=3),
            configured_regions=POSITIVE_RANGE,
        )
        self.assertEqual(block.frequencies_hz, (1.0e9, 1.5e9, 2.0e9))
        self.assertEqual(matrix.sampled_frequencies, [1.0e9, 1.5e9, 2.0e9])
        self.assertAlmostEqual(block.values[1][0].real, 0.15)
        self.assertAlmostEqual(block.values[1][0].imag, 0.25)

    def test_enabled_analysis_frequency_plans_define_export_regions(self) -> None:
        settings = FakeFrequencySettings(
            [
                # A Single plan may retain an irrelevant hidden stop value.
                FakeFrequencyPlan(0.0, 900.0e6, sweep_type="Single"),
                FakeFrequencyPlan(1.0e9, 2.0e9),
                FakeFrequencyPlan(100.0e6, 200.0e6, enabled=False),
            ]
        )
        self.assertEqual(
            MODULE.configured_frequency_regions(settings),
            DC_AND_POSITIVE_RANGE,
        )

    def test_single_plan_hidden_stop_does_not_create_phantom_sweep(self) -> None:
        settings = FakeFrequencySettings(
            [
                FakeFrequencyPlan(0.0, 900.0e6, sweep_type="Single"),
                FakeFrequencyPlan(1.0e9, 2.0e9, sweep_type="Linear"),
            ]
        )
        regions = MODULE.configured_frequency_regions(settings)
        grid = MODULE.build_frequency_grid(
            [1.0e-6, 1.0e9, 2.0e9],
            MODULE.FrequencyGridRequest("points", point_count=10),
            configured_regions=regions,
        )
        self.assertEqual(len(grid), 11)
        self.assertEqual(grid[0], 0.0)
        self.assertEqual(grid[1], 1.0e9)
        self.assertEqual(grid[-1], 2.0e9)
        self.assertFalse(any(0.0 < frequency < 1.0e9 for frequency in grid))

    def test_resampling_requires_analysis_frequency_regions(self) -> None:
        with self.assertRaisesRegex(ValueError, "required"):
            MODULE.build_frequency_grid(
                [1.0e-6, 1.0e9, 2.0e9],
                MODULE.FrequencyGridRequest("step", step_hz=400.0e6),
            )

    def test_frequency_options_create_the_requested_mode(self) -> None:
        point_arguments = MODULE._parse_arguments(["--frequency-points", "101"])
        self.assertEqual(
            MODULE._frequency_request_from_arguments(point_arguments),
            MODULE.FrequencyGridRequest("points", point_count=101),
        )
        step_arguments = MODULE._parse_arguments(
            ["--frequency-step", "25 MHz"]
        )
        self.assertEqual(
            MODULE._frequency_request_from_arguments(step_arguments),
            MODULE.FrequencyGridRequest("step", step_hz=25.0e6),
        )

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

    def test_smatrix_uses_parent_result_context_and_simulation_id(self) -> None:
        calls: list[tuple[object, object]] = []
        fake_toolkit = types.ModuleType("empro.toolkit")

        def get_circuit_matrix(proj: object = None, sim: object = None) -> FakeCircuitMatrix:
            calls.append((proj, sim))
            return FakeCircuitMatrix()

        fake_toolkit.getCircuitMatrix = get_circuit_matrix  # type: ignore[attr-defined]
        fake_empro_package = types.ModuleType("empro")
        fake_empro_package.toolkit = fake_toolkit  # type: ignore[attr-defined]

        analysis = types.SimpleNamespace(
            name="RF Analysis",
            # Some RFPro versions expose the leaf here too; the exporter must
            # derive the owning result project from SimulationOutput instead.
            simulationPath=FakeSimulationOutput.simulationPath,
            simulationSettings=FakeSingleCaseSettings(),
        )
        empro_module = types.SimpleNamespace(
            output=types.SimpleNamespace(AnalysisOutput=FakeAnalysisOutput)
        )
        modules = {
            "empro": fake_empro_package,
            "empro.toolkit": fake_toolkit,
        }

        with mock.patch.dict(sys.modules, modules):
            blocks = MODULE.collect_analysis_blocks(
                empro_module,
                analysis,
                parameter_names=("W",),
                skip_errors=False,
            )

        self.assertEqual(len(blocks), 1)
        self.assertEqual(calls, [("/project/rfpro/000001", "000002")])
        self.assertNotEqual(calls[0][0], analysis.simulationPath)
        self.assertNotEqual(calls[0][0], FakeSimulationOutput.simulationPath)


if __name__ == "__main__":
    unittest.main()
