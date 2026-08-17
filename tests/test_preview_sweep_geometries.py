from __future__ import annotations

import importlib.util
import sys
import tempfile
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


class FakeLayout:
    def __init__(self) -> None:
        self.received_updates: list[dict[str, str]] = []

    def _updateDesignParameters(self, updates: dict[str, str]) -> str:
        self.received_updates.append(dict(updates))
        return "native update accepted"


class FakeProject:
    def __init__(
        self, formulas: dict[str, object], valid: bool = True, reason: str = ""
    ) -> None:
        self.parameters = FakeParameters(formulas)
        self.geometry = FakeGeometry(valid, reason)
        self.layout = FakeLayout()
        self.load_design_parameter_calls = 0

    def _loadOaParametersFromDesignSpec(self) -> None:
        self.load_design_parameter_calls += 1


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


class FakeCaptureImage:
    def __init__(self, null: bool = False) -> None:
        self.null = null
        self.saved_paths: list[Path] = []

    def isNull(self) -> bool:
        return self.null

    def width(self) -> int:
        return 0 if self.null else 640

    def height(self) -> int:
        return 0 if self.null else 480

    def save(self, path: str, image_format: str) -> bool:
        self.saved_paths.append(Path(path))
        Path(path).write_bytes(b"fake png")
        return image_format == "PNG"


class FakeCapturePixmap:
    def __init__(self, image: FakeCaptureImage) -> None:
        self.image = image

    def toImage(self) -> FakeCaptureImage:
        return self.image


class FakeGeometryView:
    def __init__(self, image: FakeCaptureImage) -> None:
        self.image = image
        self.update_calls = 0

    def updateView(self) -> None:
        self.update_calls += 1

    def grabFramebuffer(self) -> FakeCaptureImage:
        return self.image


class FakeGeometryViewController:
    def __init__(self) -> None:
        self.update_calls = 0

    def updateView(self) -> None:
        self.update_calls += 1


class FakeGeometryViewWidget:
    def __init__(self, image: FakeCaptureImage) -> None:
        self.image = image
        self.grab_calls = 0

    def grab(self) -> FakeCapturePixmap:
        self.grab_calls += 1
        return FakeCapturePixmap(self.image)


class FakeProjectView:
    def __init__(self, geometry_view, geometry_widget=None) -> None:
        self.geometry_view = geometry_view
        self.geometry_widget = geometry_widget
        self.show_calls = 0

    def showGeometryView(self) -> None:
        self.show_calls += 1

    def geometryView(self) -> FakeGeometryView:
        return self.geometry_view

    def geometryViewWidget(self):
        return self.geometry_widget


class FakeCaptureGui:
    def __init__(self, project_view: FakeProjectView) -> None:
        self.project_view = project_view
        self.process_events_calls = 0

    def activeProjectView(self) -> FakeProjectView:
        return self.project_view

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

    def test_sweep_point_is_submitted_to_rfpro_native_geometry_updater(self) -> None:
        project = FakeProject(
            {"W": "base-W", "L": "base-L", "unrelated": "7 mm"}
        )
        point = MODULE.SweepPoint(
            point_index=0,
            sequence_index=0,
            combination_index=0,
            values=(MODULE.SweepValue("L", "3 mm", "3 mm"),),
        )

        report = MODULE.apply_sweep_point_to_geometry(
            project, {"W": "base-W", "L": "base-L"}, point
        )

        expected = {"W": "base-W", "L": "3 mm"}
        self.assertEqual(project.load_design_parameter_calls, 1)
        self.assertEqual(project.layout.received_updates, [expected])
        self.assertEqual(report["updates"], expected)
        self.assertEqual(report["native_status"], "native update accepted")
        self.assertNotIn("unrelated", report["updates"])

    def test_baseline_geometry_is_restored_through_native_updater(self) -> None:
        project = FakeProject({"W": "changed", "L": "changed"})

        report = MODULE.restore_parameter_formulas_and_geometry(
            project, {"W": "base-W", "L": "base-L"}
        )

        expected = {"W": "base-W", "L": "base-L"}
        self.assertEqual(project.parameters.formulas, expected)
        self.assertEqual(project.layout.received_updates, [expected])
        self.assertEqual(report["updates"], expected)

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

    def test_geometry_capture_uses_the_rfpro_geometry_view_widget(self) -> None:
        image = FakeCaptureImage()
        geometry_view = FakeGeometryViewController()
        geometry_widget = FakeGeometryViewWidget(image)
        project_view = FakeProjectView(geometry_view, geometry_widget)
        gui = FakeCaptureGui(project_view)
        empro_module = type("FakeEmpro", (), {"gui": gui})()

        captured, method = MODULE.capture_geometry_view_image(
            empro_module, application=object()
        )

        self.assertIs(captured, image)
        self.assertEqual(method, "geometry view widget.grab()")
        self.assertEqual(project_view.show_calls, 1)
        self.assertEqual(geometry_view.update_calls, 1)
        self.assertEqual(geometry_widget.grab_calls, 1)
        self.assertEqual(gui.process_events_calls, 1)

    def test_geometry_capture_falls_back_to_the_scene_controller(self) -> None:
        image = FakeCaptureImage()
        geometry_view = FakeGeometryView(image)
        project_view = FakeProjectView(geometry_view)
        gui = FakeCaptureGui(project_view)
        empro_module = type("FakeEmpro", (), {"gui": gui})()

        captured, method = MODULE.capture_geometry_view_image(
            empro_module, application=object()
        )

        self.assertIs(captured, image)
        self.assertEqual(method, "geometry view controller.grabFramebuffer()")

    def test_pixmap_capture_is_normalized_to_an_image(self) -> None:
        image = FakeCaptureImage()
        self.assertIs(
            MODULE._usable_capture_image(FakeCapturePixmap(image)), image
        )
        self.assertIsNone(
            MODULE._usable_capture_image(FakeCapturePixmap(FakeCaptureImage(True)))
        )

    def test_geometry_png_is_saved_and_verified(self) -> None:
        image = FakeCaptureImage()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "point_0001.png"
            MODULE.save_geometry_image(image, output)
            self.assertEqual(output.read_bytes(), b"fake png")

    def test_report_paths_do_not_replace_prior_image_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pdf_path = Path(directory) / "geometry report.pdf"
            first = MODULE.next_available_image_directory(pdf_path)
            self.assertEqual(first.name, "geometry report_images")
            first.mkdir()
            second = MODULE.next_available_image_directory(pdf_path)
            self.assertEqual(second.name, "geometry report_images_2")
        self.assertEqual(
            MODULE.default_geometry_report_filename("My RF/Analysis"),
            "My_RF_Analysis_geometry_validation.pdf",
        )

    def test_empty_report_image_directory_is_removed_safely(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            empty = Path(directory) / "empty"
            empty.mkdir()
            self.assertTrue(MODULE.remove_empty_image_directory(empty))
            self.assertFalse(empty.exists())

            nonempty = Path(directory) / "nonempty"
            nonempty.mkdir()
            (nonempty / "point_0001.png").write_bytes(b"png")
            self.assertFalse(MODULE.remove_empty_image_directory(nonempty))
            self.assertTrue(nonempty.is_dir())

    def test_pdf_page_metadata_is_escaped_and_complete(self) -> None:
        point = MODULE.SweepPoint(
            point_index=2,
            sequence_index=1,
            combination_index=4,
            values=(MODULE.SweepValue("W<1", 1.0, "2 & 3 mm"),),
        )
        page = MODULE.GeometryReportPage(
            point=point,
            valid=False,
            message="self-intersection <edge>",
            image_path=None,
            capture_error="no image & retry",
        )

        report_html = MODULE._geometry_report_page_html(
            "Analysis <A>", page, 1, 1, 10
        )

        self.assertIn("Analysis &lt;A&gt;", report_html)
        self.assertIn("W&lt;1", report_html)
        self.assertIn("2 &amp; 3 mm", report_html)
        self.assertIn("Sweep point:</b> 3 of 10", report_html)
        self.assertIn("INVALID", report_html)
        self.assertIn("no image &amp; retry", report_html)

    def test_pdf_report_rejects_an_empty_page_set_before_loading_qt(self) -> None:
        with self.assertRaisesRegex(ValueError, "At least one"):
            MODULE.write_geometry_pdf_report(
                Path("unused.pdf"), "Analysis", [], total_point_count=0
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
