from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "rfpro_scripts" / "preview_sweep_geometries.py"
SPEC = importlib.util.spec_from_file_location("preview_sweep_geometries", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeSweep:
    def __init__(self, name: str, values: list[float], displayed=None) -> None:
        self.parameterName = name
        self.parameterValues = values
        self._displayed = values if displayed is None else displayed

    def getParameterValues(self):
        return self._displayed


class FakeSettings:
    def __init__(self, sequences, enabled: bool = True) -> None:
        self.parameterSweepEnabled = enabled
        self.parameterSequences = sequences
        self.numberOfParameterInstances = 0


class FakeParameters:
    def __init__(self, formulas: dict[str, object]) -> None:
        self.formulas = dict(formulas)
        self.calls: list[tuple[str, object]] = []

    def names(self):
        return list(self.formulas)

    def formula(self, name: str):
        return self.formulas[name]

    def setFormula(self, name: str, value: object) -> None:
        self.calls.append((name, value))
        self.formulas[name] = value


class FakeGeometry:
    def __init__(self, valid: bool, reason: str = "") -> None:
        self.valid = valid
        self.reason = reason

    def isValid(self) -> bool:
        return self.valid

    def reasonWhyInvalid(self) -> str:
        return self.reason


class FakeProject:
    def __init__(
        self, formulas: dict[str, object], valid: bool = True, reason: str = ""
    ) -> None:
        self.parameters = FakeParameters(formulas)
        self.geometry = FakeGeometry(valid, reason)


class FakeSignal:
    def __init__(self) -> None:
        self.callbacks = []

    def connect(self, callback) -> None:
        self.callbacks.append(callback)

    def emit(self) -> None:
        for callback in list(self.callbacks):
            callback()


class FakeDialog:
    def __init__(self) -> None:
        self.destroyed = FakeSignal()
        self.close_calls = 0
        self.shown = False

    def close(self) -> None:
        self.close_calls += 1
        self.destroyed.emit()

    def show(self) -> None:
        self.shown = True

    def raise_(self) -> None:
        pass

    def activateWindow(self) -> None:
        pass


class FakeApplication:
    def __init__(self) -> None:
        self.process_events_calls = 0

    def processEvents(self) -> None:
        self.process_events_calls += 1


class PreviewSweepGeometryTests(unittest.TestCase):
    def test_sequences_expand_as_concatenated_cartesian_products(self) -> None:
        settings = FakeSettings(
            [
                [
                    FakeSweep("W", [1.0, 2.0], ["1 mm", "2 mm"]),
                    FakeSweep("L", [10.0, 20.0], ["10 mm", "20 mm"]),
                ],
                [FakeSweep("Gap", [0.5], "0.5 mm")],
            ]
        )

        points = MODULE.expand_parameter_sequences(settings)

        self.assertEqual(len(points), 5)
        self.assertEqual([point.sequence_index for point in points], [0, 0, 0, 0, 1])
        self.assertEqual(
            [(value.parameter_name, value.value, value.display) for value in points[1].values],
            [("W", 1.0, "1 mm"), ("L", 20.0, "20 mm")],
        )
        self.assertEqual(points[-1].values[0].display, "0.5 mm")

    def test_disabled_or_empty_sweep_is_rejected(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            MODULE.expand_parameter_sequences(FakeSettings([], enabled=False))
        with self.assertRaisesRegex(ValueError, "has no values"):
            MODULE.expand_parameter_sequences(
                FakeSettings([[FakeSweep("W", [], [])]])
            )

    def test_duplicate_parameter_in_sequence_is_rejected(self) -> None:
        settings = FakeSettings(
            [[FakeSweep("W", [1.0]), FakeSweep("W", [2.0])]]
        )
        with self.assertRaisesRegex(ValueError, "repeats parameter"):
            MODULE.expand_parameter_sequences(settings)

    def test_apply_resets_all_swept_parameters_before_point_values(self) -> None:
        project = FakeProject({"W": "base-W", "L": "base-L"})
        point = MODULE.SweepPoint(
            point_index=0,
            sequence_index=1,
            combination_index=0,
            values=(MODULE.SweepValue("L", 3.0, "3 mm"),),
        )

        MODULE.apply_sweep_point(
            project, {"W": "base-W", "L": "base-L"}, point
        )

        self.assertEqual(
            project.parameters.calls,
            [("W", "base-W"), ("L", "base-L"), ("L", 3.0)],
        )
        self.assertEqual(project.parameters.formulas["W"], "base-W")
        self.assertEqual(project.parameters.formulas["L"], 3.0)

        MODULE.restore_parameter_formulas(
            project, {"W": "base-W", "L": "base-L"}
        )
        self.assertEqual(project.parameters.formulas["L"], "base-L")

    def test_snapshot_requires_every_sweep_parameter(self) -> None:
        project = FakeProject({"W": "1 mm"})
        self.assertEqual(
            MODULE.snapshot_parameter_formulas(project, ["W"]), {"W": "1 mm"}
        )
        with self.assertRaisesRegex(ValueError, "missing"):
            MODULE.snapshot_parameter_formulas(project, ["W", "L"])

    def test_geometry_validity_reports_reason(self) -> None:
        self.assertEqual(
            MODULE.geometry_validity(FakeProject({}, valid=True)),
            (True, "Geometry is valid."),
        )
        self.assertEqual(
            MODULE.geometry_validity(
                FakeProject({}, valid=False, reason="self-intersection")
            ),
            (False, "self-intersection"),
        )

    def test_existing_inspector_is_closed_before_new_one_is_registered(self) -> None:
        application = FakeApplication()
        first = FakeDialog()
        second = FakeDialog()

        MODULE._show_modeless(application, first)
        MODULE._close_existing_inspectors(application)

        self.assertEqual(first.close_calls, 1)
        self.assertEqual(application.process_events_calls, 1)
        self.assertEqual(
            getattr(application, MODULE._INSPECTOR_REGISTRY_ATTRIBUTE), []
        )

        MODULE._show_modeless(application, second)
        self.assertEqual(
            getattr(application, MODULE._INSPECTOR_REGISTRY_ATTRIBUTE), [second]
        )
        self.assertTrue(second.shown)


if __name__ == "__main__":
    unittest.main()
