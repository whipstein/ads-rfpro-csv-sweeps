from __future__ import annotations

import gc
import importlib.util
import sys
import tempfile
import unittest
import weakref
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
    def __init__(self, top_levels=None) -> None:
        self.process_events_calls = 0
        self.top_levels = list(top_levels or [])

    def processEvents(self) -> None:
        self.process_events_calls += 1

    def topLevelWidgets(self):
        return list(self.top_levels)


class FakeGeometryViewController:
    def __init__(self) -> None:
        self.update_calls = 0
        self.zoom_calls = 0
        self.fem_mesh_calls = []
        self.momentum_mesh_calls = []

    def updateView(self) -> None:
        self.update_calls += 1

    def zoomGeometryViewToExtents(self) -> None:
        self.zoom_calls += 1

    def displayFemMesh(self, simulation_output) -> None:
        self.fem_mesh_calls.append(simulation_output)

    def displayMomMesh(self, simulation_output) -> None:
        self.momentum_mesh_calls.append(simulation_output)


class FakeAction:
    def __init__(self, text: str, on_trigger=None, menu=None) -> None:
        self.text = text
        self.enabled = True
        self.on_trigger = on_trigger
        self.menu = menu
        self.trigger_calls = 0

    def trigger(self) -> None:
        self.trigger_calls += 1
        if self.on_trigger is not None:
            self.on_trigger()


class FakeMenu:
    def __init__(self, actions) -> None:
        self._actions = list(actions)

    def actions(self):
        return list(self._actions)


class FakeWindow:
    def __init__(self, title: str, menu_bar: FakeMenu) -> None:
        self.title = title
        self.menu_bar = menu_bar

    def windowTitle(self) -> str:
        return self.title

    def menuBar(self) -> FakeMenu:
        return self.menu_bar

    def findChildren(self, _child_type):
        return []


class FakeSaveDialogAutomation:
    def __init__(self, _application, _output_path: Path) -> None:
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def diagnostics(self) -> str:
        return "fake automation"


class GarbageCollectingSaveDialogAutomation(FakeSaveDialogAutomation):
    def start(self) -> None:
        super().start()
        gc.collect()


class WaitingSaveDialogAutomation(FakeSaveDialogAutomation):
    output_wait_seconds = 0.25


class FakeProjectView:
    def __init__(self, geometry_view, view_menu=None) -> None:
        self.geometry_view = geometry_view
        self.view_menu = view_menu or FakeMenu([])
        self.show_calls = 0

    def showGeometryView(self) -> None:
        self.show_calls += 1

    def geometryView(self):
        return self.geometry_view

    def menu(self, name: str):
        if name != "view":
            raise KeyError(name)
        return self.view_menu


class FakeCaptureGui:
    def __init__(self, project_view: FakeProjectView) -> None:
        self.project_view = project_view
        self.process_events_calls = 0

    def activeProjectView(self) -> FakeProjectView:
        return self.project_view

    def processEvents(self) -> None:
        self.process_events_calls += 1


class FakeSimulationMetadata:
    def __init__(self, parameters=None, parameter_string: str = "") -> None:
        self.parameters = parameters
        self.parameterString = parameter_string

    def getParameterValues(self, *_arguments):
        return self.parameters


class FakeSimulationOutput:
    def __init__(self, simulation_path: Path, metadata: FakeSimulationMetadata) -> None:
        self.simulationPath = str(simulation_path)
        self._metadata = metadata

    def metadata(self) -> FakeSimulationMetadata:
        return self._metadata


class FakeAnalysisOutput:
    def __init__(self, simulations) -> None:
        self.simulations = dict(simulations)

    def getAvailableSimulationIds(self):
        return list(self.simulations)

    def getSimulation(self, simulation_id):
        return self.simulations[str(simulation_id)]


class FakeOutputNamespace:
    def AnalysisOutput(self, analysis):
        return analysis.analysis_output


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

    def test_saved_fem_and_momentum_mesh_ports_data_are_discovered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fem_output = FakeSimulationOutput(
                root / "fem_case", FakeSimulationMetadata()
            )
            fem_directory = root / "fem_case" / "emds_dsn" / "design"
            fem_directory.mkdir(parents=True)
            (fem_directory / "options.xml").write_text("options")
            fem_mesh = fem_directory / "mesh" / "final.ovm"
            fem_mesh.parent.mkdir()
            fem_mesh.write_bytes(b"mesh")

            momentum_output = FakeSimulationOutput(
                root / "mom_case", FakeSimulationMetadata()
            )
            momentum_directory = root / "mom_case" / "work"
            momentum_directory.mkdir(parents=True)
            (momentum_directory / "proj.opt").write_text("options")
            momentum_mesh = momentum_directory / "mesh.ovm"
            momentum_mesh.write_bytes(b"mesh")

            self.assertEqual(
                MODULE.find_mesh_ports_data(fem_output),
                ("FEM", fem_mesh, ""),
            )
            self.assertEqual(
                MODULE.find_mesh_ports_data(momentum_output),
                ("Momentum", momentum_mesh, ""),
            )

    def test_partial_saved_results_are_mapped_by_parameter_metadata(self) -> None:
        points = (
            MODULE.SweepPoint(
                0,
                0,
                0,
                (MODULE.SweepValue("W", 1.0e-3, "1 mm"),),
            ),
            MODULE.SweepPoint(
                1,
                0,
                1,
                (MODULE.SweepValue("W", 2.0e-3, "2 mm"),),
            ),
            MODULE.SweepPoint(
                2,
                0,
                2,
                (MODULE.SweepValue("W", 3.0e-3, "3 mm"),),
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            simulation_path = Path(directory) / "case"
            mesh_directory = simulation_path / "emds_dsn" / "design"
            mesh_directory.mkdir(parents=True)
            (mesh_directory / "options.xml").write_text("options")
            (mesh_directory / "point.ovm").write_bytes(b"mesh")
            simulation = FakeSimulationOutput(
                simulation_path,
                FakeSimulationMetadata({"W": "2000 um"}),
            )
            analysis = type(
                "FakeAnalysis",
                (),
                {"analysis_output": FakeAnalysisOutput({"000002": simulation})},
            )()
            empro_module = type(
                "FakeEmpro", (), {"output": FakeOutputNamespace()}
            )()

            inventory = MODULE.discover_mesh_ports_results(
                empro_module, analysis, points
            )

        self.assertEqual(
            [
                (index, result.simulation_id)
                for index, result in inventory.results_by_point
            ],
            [(1, "000002")],
        )
        self.assertEqual(inventory.missing_point_indices, (0, 2))
        self.assertEqual(inventory.unmatched_result_ids, ())

    def test_partial_result_without_metadata_is_not_positionally_guessed(self) -> None:
        points = (
            MODULE.SweepPoint(
                0,
                0,
                0,
                (MODULE.SweepValue("W", 1.0e-3, "1 mm"),),
            ),
            MODULE.SweepPoint(
                1,
                0,
                1,
                (MODULE.SweepValue("W", 2.0e-3, "2 mm"),),
            ),
        )
        simulation = FakeSimulationOutput(
            Path("missing"), FakeSimulationMetadata(None)
        )
        analysis = type(
            "FakeAnalysis",
            (),
            {"analysis_output": FakeAnalysisOutput({"000009": simulation})},
        )()
        empro_module = type(
            "FakeEmpro", (), {"output": FakeOutputNamespace()}
        )()

        inventory = MODULE.discover_mesh_ports_results(
            empro_module, analysis, points
        )

        self.assertEqual(inventory.results_by_point, ())
        self.assertEqual(inventory.missing_point_indices, (0, 1))
        self.assertEqual(inventory.unmatched_result_ids, ("000009",))

    def test_complete_results_can_fall_back_to_public_result_order(self) -> None:
        points = (
            MODULE.SweepPoint(
                0,
                0,
                0,
                (MODULE.SweepValue("W", 1.0e-3, "1 mm"),),
            ),
            MODULE.SweepPoint(
                1,
                0,
                1,
                (MODULE.SweepValue("W", 2.0e-3, "2 mm"),),
            ),
        )
        simulations = {
            "000001": FakeSimulationOutput(
                Path("missing_1"), FakeSimulationMetadata(None)
            ),
            "000002": FakeSimulationOutput(
                Path("missing_2"), FakeSimulationMetadata(None)
            ),
        }
        analysis = type(
            "FakeAnalysis",
            (),
            {"analysis_output": FakeAnalysisOutput(simulations)},
        )()
        empro_module = type(
            "FakeEmpro", (), {"output": FakeOutputNamespace()}
        )()

        inventory = MODULE.discover_mesh_ports_results(
            empro_module, analysis, points
        )

        self.assertEqual(
            [
                (index, result.simulation_id)
                for index, result in inventory.results_by_point
            ],
            [(0, "000001"), (1, "000002")],
        )
        self.assertEqual(inventory.missing_mesh_point_indices, (0, 1))

    def test_mesh_ports_display_uses_verified_geometry_view_binding(self) -> None:
        simulation_output = object()
        result = MODULE.MeshPortsResult(
            simulation_id="000002",
            simulation_output=simulation_output,
            parameters=(),
            mesh_kind="FEM",
            mesh_file=Path("mesh.ovm"),
        )
        geometry_view = FakeGeometryViewController()
        project_view = FakeProjectView(geometry_view)
        gui = FakeCaptureGui(project_view)
        empro_module = type("FakeEmpro", (), {"gui": gui})()

        MODULE.display_mesh_ports_result(empro_module, result, True)

        self.assertEqual(project_view.show_calls, 1)
        self.assertEqual(geometry_view.fem_mesh_calls, [simulation_output])
        self.assertEqual(geometry_view.momentum_mesh_calls, [])
        self.assertEqual(geometry_view.zoom_calls, 1)
        self.assertGreaterEqual(gui.process_events_calls, 3)

    def test_momentum_mesh_ports_display_uses_momentum_binding(self) -> None:
        simulation_output = object()
        result = MODULE.MeshPortsResult(
            simulation_id="000003",
            simulation_output=simulation_output,
            parameters=(),
            mesh_kind="Momentum",
            mesh_file=Path("mesh.ovm"),
        )
        geometry_view = FakeGeometryViewController()
        project_view = FakeProjectView(geometry_view)
        gui = FakeCaptureGui(project_view)
        empro_module = type("FakeEmpro", (), {"gui": gui})()

        MODULE.display_mesh_ports_result(empro_module, result, False)

        self.assertEqual(geometry_view.fem_mesh_calls, [])
        self.assertEqual(geometry_view.momentum_mesh_calls, [simulation_output])
        self.assertEqual(geometry_view.zoom_calls, 0)

    def test_export_image_action_is_found_recursively_in_the_view_menu(self) -> None:
        export_action = FakeAction("&Export Image...")
        submenu_action = FakeAction("Export", menu=FakeMenu([export_action]))
        project_view = FakeProjectView(
            FakeGeometryViewController(), FakeMenu([submenu_action])
        )

        action, description, owners = MODULE.find_rfpro_export_image_action(
            project_view,
            FakeApplication(),
            qt_action_type=None,
        )

        self.assertIs(action, export_action)
        self.assertEqual(description, "RFPro View menu > &Export Image...")
        self.assertIn(project_view, owners)
        self.assertIn(project_view.view_menu, owners)
        self.assertIn(submenu_action.menu, owners)
        self.assertIn(export_action, owners)

    def test_live_qt_view_menu_is_preferred_and_its_owners_are_retained(self) -> None:
        wrapper_action = FakeAction("Export Image...")
        live_action = FakeAction("Export Image...")
        view_action = FakeAction("&View", menu=FakeMenu([live_action]))
        window = FakeWindow("RFPro", FakeMenu([view_action]))
        project_view = FakeProjectView(
            FakeGeometryViewController(), FakeMenu([wrapper_action])
        )

        action, description, owners = MODULE.find_rfpro_export_image_action(
            project_view,
            FakeApplication([window]),
            qt_action_type=FakeAction,
        )

        self.assertIs(action, live_action)
        self.assertEqual(
            description, "Qt window 'RFPro' View menu > Export Image..."
        )
        self.assertIn(window, owners)
        self.assertIn(window.menu_bar, owners)
        self.assertIn(view_action.menu, owners)

    def test_deleted_export_action_is_rejected_before_trigger(self) -> None:
        action = FakeAction("Export Image...")
        original_validator = MODULE._qt_object_is_valid
        MODULE._qt_object_is_valid = lambda candidate: candidate is not action
        try:
            with self.assertRaisesRegex(RuntimeError, "deleted before"):
                MODULE._action_trigger(action)
        finally:
            MODULE._qt_object_is_valid = original_validator

        self.assertEqual(action.trigger_calls, 0)

    def test_missing_export_action_reports_the_view_menu_contents(self) -> None:
        project_view = FakeProjectView(
            FakeGeometryViewController(), FakeMenu([FakeAction("Fit View")])
        )

        with self.assertRaisesRegex(
            RuntimeError, "View menu: Fit View"
        ):
            MODULE.find_rfpro_export_image_action(
                project_view,
                FakeApplication(),
                qt_action_type=None,
            )

    def test_geometry_png_uses_rfpro_export_image_action_and_is_verified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "point_0001.png"
            export_action = FakeAction(
                "Export Image...", lambda: output.write_bytes(b"rfpro png")
            )
            geometry_view = FakeGeometryViewController()
            project_view = FakeProjectView(
                geometry_view, FakeMenu([export_action])
            )
            gui = FakeCaptureGui(project_view)
            empro_module = type("FakeEmpro", (), {"gui": gui})()

            method = MODULE.export_geometry_view_png(
                empro_module,
                FakeApplication(),
                output,
                automation_factory=FakeSaveDialogAutomation,
            )

            self.assertEqual(output.read_bytes(), b"rfpro png")
            self.assertEqual(method, "RFPro View menu > Export Image...")
            self.assertEqual(export_action.trigger_calls, 1)
            self.assertEqual(project_view.show_calls, 1)
            self.assertEqual(geometry_view.update_calls, 1)

    def test_export_keeps_a_transient_view_menu_alive_until_trigger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "point_0001.png"
            geometry_view = FakeGeometryViewController()

            class OwnerSensitiveAction(FakeAction):
                def __init__(self, owner) -> None:
                    super().__init__("Export Image...")
                    self.owner_reference = weakref.ref(owner)

                def trigger(self) -> None:
                    if self.owner_reference() is None:
                        raise RuntimeError("menu owner was already deleted")
                    output.write_bytes(b"rfpro png")

            class TransientMenuProjectView(FakeProjectView):
                def __init__(self) -> None:
                    super().__init__(geometry_view)

                def menu(self, name: str):
                    if name != "view":
                        raise KeyError(name)
                    owner = FakeMenu([])
                    owner._actions.append(OwnerSensitiveAction(owner))
                    return owner

            project_view = TransientMenuProjectView()
            gui = FakeCaptureGui(project_view)
            empro_module = type("FakeEmpro", (), {"gui": gui})()

            MODULE.export_geometry_view_png(
                empro_module,
                FakeApplication(),
                output,
                automation_factory=GarbageCollectingSaveDialogAutomation,
                qt_action_type=None,
            )

            self.assertEqual(output.read_bytes(), b"rfpro png")

    def test_export_waits_for_rfpro_to_write_after_the_action_returns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "point_0001.png"

            class DelayedImageApplication(FakeApplication):
                def processEvents(self) -> None:
                    super().processEvents()
                    if self.process_events_calls == 2:
                        output.write_bytes(b"delayed rfpro png")

            export_action = FakeAction("Export Image...")
            project_view = FakeProjectView(
                FakeGeometryViewController(), FakeMenu([export_action])
            )
            gui = FakeCaptureGui(project_view)
            empro_module = type("FakeEmpro", (), {"gui": gui})()

            MODULE.export_geometry_view_png(
                empro_module,
                DelayedImageApplication(),
                output,
                automation_factory=WaitingSaveDialogAutomation,
            )

            self.assertEqual(output.read_bytes(), b"delayed rfpro png")

    def test_export_normalizes_an_rfpro_appended_png_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "point_0001.png"
            appended = Path(str(output) + ".png")
            export_action = FakeAction(
                "Export Image...", lambda: appended.write_bytes(b"rfpro png")
            )
            project_view = FakeProjectView(
                FakeGeometryViewController(), FakeMenu([export_action])
            )
            gui = FakeCaptureGui(project_view)
            empro_module = type("FakeEmpro", (), {"gui": gui})()

            MODULE.export_geometry_view_png(
                empro_module,
                FakeApplication(),
                output,
                automation_factory=FakeSaveDialogAutomation,
            )

            self.assertEqual(output.read_bytes(), b"rfpro png")
            self.assertFalse(appended.exists())

    def test_export_fails_when_rfpro_does_not_create_the_png(self) -> None:
        export_action = FakeAction("Export Image...")
        project_view = FakeProjectView(
            FakeGeometryViewController(), FakeMenu([export_action])
        )
        gui = FakeCaptureGui(project_view)
        empro_module = type("FakeEmpro", (), {"gui": gui})()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "point_0001.png"
            with self.assertRaisesRegex(
                RuntimeError, "triggered, but RFPro did not create"
            ):
                MODULE.export_geometry_view_png(
                    empro_module,
                    FakeApplication(),
                    output,
                    automation_factory=FakeSaveDialogAutomation,
                )

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
        self.assertEqual(
            MODULE.default_mesh_ports_report_filename("My RF/Analysis"),
            "My_RF_Analysis_mesh_ports_validation.pdf",
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
            values=(MODULE.SweepValue("W<1", 0.002000003, "2.000003 mm"),),
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
        self.assertIn("2000.003 um", report_html)
        self.assertIn("Geometry parameters (um)", report_html)
        self.assertIn("Sweep point:</b> 3 of 10", report_html)
        self.assertIn("INVALID", report_html)
        self.assertIn("no image &amp; retry", report_html)

    def test_report_geometry_values_are_scaled_and_rounded_in_um(self) -> None:
        self.assertEqual(
            MODULE.format_geometry_report_value(
                MODULE.SweepValue("W", 0.000123456789, "0.123456789 mm"),
                3,
            ),
            "123.457 um",
        )
        self.assertEqual(
            MODULE.format_geometry_report_value(
                MODULE.SweepValue("Gap", 2.5e-6, "parameter_formula"),
                4,
            ),
            "2.5 um",
        )
        self.assertEqual(
            MODULE.format_geometry_report_value(
                MODULE.SweepValue("Pitch", 1.0, "4 mil"),
                2,
            ),
            "101.6 um",
        )

    def test_mesh_ports_report_has_specific_title_and_status(self) -> None:
        point = MODULE.SweepPoint(
            0,
            0,
            0,
            (MODULE.SweepValue("W", 1.0e-3, "1 mm"),),
        )
        page = MODULE.GeometryReportPage(
            point=point,
            valid=True,
            message="Saved simulation 000001.",
            image_path=Path("point.png"),
            status_label="Mesh/Ports loaded",
        )

        report_html = MODULE._geometry_report_page_html(
            "Analysis",
            page,
            1,
            1,
            1,
            report_title="RFPro Mesh/Ports Validation",
        )

        self.assertIn("RFPro Mesh/Ports Validation", report_html)
        self.assertIn("Mesh/Ports loaded", report_html)

    def test_report_geometry_decimal_setting_is_validated(self) -> None:
        value = MODULE.SweepValue("W", 1.0e-6, "1 um")
        with self.assertRaisesRegex(ValueError, "integer from 0 through 12"):
            MODULE.format_geometry_report_value(value, -1)
        with self.assertRaisesRegex(ValueError, "integer from 0 through 12"):
            MODULE.format_geometry_report_value(value, True)

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
