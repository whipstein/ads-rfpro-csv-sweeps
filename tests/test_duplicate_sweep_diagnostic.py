from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "diagnose_duplicate_sweep_conditions.py"
SPEC = importlib.util.spec_from_file_location(
    "diagnose_duplicate_sweep_conditions", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeSweep:
    def __init__(self, name: str, numeric: list[float], display: list[str]) -> None:
        self.parameterName = name
        self.parameterValues = numeric
        self._display = display

    def getParameterValues(self, mode: str = "") -> list[str]:
        return self._display


class FakeSettings:
    def __init__(self) -> None:
        self.parameterSequences = [
            [FakeSweep("W", [1.0, 2.0], ["1 mm", "2 mm"])],
            [FakeSweep("W", [1.0 + 1.0e-12], ["1000.000000001 um"])],
            [FakeSweep("W", [2.0], ["2 mm"])],
        ]
        self.numberOfParameterInstances = 4


class FakeAnalysisOutput:
    def __init__(self, _analysis: object) -> None:
        pass

    @staticmethod
    def getAvailableSimulationIds() -> list[str]:
        return ["000001", "000002"]

    @staticmethod
    def getAvailableSimulationPaths() -> list[str]:
        return ["/results/000001", "/results/000002"]

    @staticmethod
    def getAvailableSequenceAndSimulationIds() -> list[tuple[int, str]]:
        return [(1, "000001"), (1, "000002")]


class DuplicateSweepDiagnosticTests(unittest.TestCase):
    def test_expansion_and_tolerant_duplicate_groups(self) -> None:
        points = MODULE.expand_configured_points(FakeSettings())
        groups = MODULE.duplicate_point_groups(points, 1.0e-9, 1.0e-15)

        self.assertEqual(len(points), 4)
        self.assertEqual(groups, [[0, 2], [1, 3]])
        self.assertEqual(points[2]["display"]["W"], "1000.000000001 um")

    def test_different_parameter_sets_do_not_match(self) -> None:
        left = {"W": 1.0}
        right = {"L": 1.0}
        self.assertFalse(MODULE.point_values_match(left, right, 1.0e-9, 1.0e-15))

    def test_report_correlates_duplicate_and_result_shortfall_counts(self) -> None:
        analysis = types.SimpleNamespace(
            name="RF Analysis",
            simulationSettings=FakeSettings(),
        )
        empro_module = types.SimpleNamespace(
            output=types.SimpleNamespace(AnalysisOutput=FakeAnalysisOutput)
        )
        stream = io.StringIO()

        with contextlib.redirect_stdout(stream):
            MODULE.print_duplicate_sweep_report(
                empro_module, analysis, 1.0e-9, 1.0e-15
            )

        text = stream.getvalue()
        self.assertIn("Redundant configured entries: 2", text)
        self.assertIn("Unique evaluated conditions: 2", text)
        self.assertIn("Configured-minus-registered count: 2", text)
        self.assertIn("consistent with RFPro coalescing", text)

    def test_negative_tolerance_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            MODULE.validated_tolerance(-1.0, "Tolerance")


if __name__ == "__main__":
    unittest.main()
