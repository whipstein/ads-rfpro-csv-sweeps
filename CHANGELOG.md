# Changelog

## 0.8.2 - 2026-08-17

- Capture validation images from the visible RFPro
  `activeProjectView().geometryViewWidget()` established by Keysight's shipped
  EMPro application setup code, instead of relying on the non-widget
  `geometryView()` scene controller.
- Retain controller and native-window capture paths as compatibility fallbacks
  for RFPro builds whose geometry widget does not expose a direct Qt capture.
- Remove the newly created image directory when a report captures no PNGs,
  while preserving any directory that contains a successful image.

## 0.8.1 - 2026-08-17

- Submit every loaded sweep point through the active RFPro layout's targeted
  `_updateDesignParameters(Mapping[str, str])` binding after loading the OA
  design-spec parameters, so visible formula changes regenerate PCell artwork.
- Use the same targeted geometry update when restoring the original parameter
  formulas, keeping the displayed model consistent with the Parameters dialog.
- Pump the RFPro event loop before and after repainting the geometry view and
  before fitting the regenerated model.
- Continue to avoid `layout.refresh()` and workspace-wide `.adsPcells` changes.

## 0.8.0 - 2026-08-17

- Add an explicit **Load Selected** inspector action that regenerates the
  highlighted parameter combination even when the table selection has not
  changed.
- Add **Check All + PDF** to fit and capture every generated geometry, retain
  numbered PNG images, and create a multi-page validation report containing
  the parameters and RFPro validity result for each point.
- Preserve successfully captured images and create a valid partial report when
  the user cancels after at least one point.
- Keep **Fit View** limited to fitting the geometry that is already displayed,
  and document that distinction in the UI.

## 0.7.3 - 2026-08-17

- Honor each enabled frequency plan's `sweepType` or legacy `type` when
  deriving export regions.
- Treat a `Single` plan as exactly its `startFrequency`, ignoring an unrelated
  or stale hidden `stopFrequency` that previously created a phantom sweep.
- Print raw frequency-plan properties and the effective region used for
  resampling.

## 0.7.2 - 2026-08-17

- Derive resampled MDIF frequency regions from the selected analysis's enabled
  `femFrequencyPlanList()` entries instead of circuit-result sample locations.
- Preserve configured single-frequency plans such as DC and independently
  sample each configured range without filling gaps between plans.
- Print the exact enabled analysis frequency regions before exporting.

## 0.7.1 - 2026-08-17

- Preserve a simulated DC sample as a standalone export point instead of
  treating 0 Hz as the start of a continuous resampling span.
- Apply point-count and step-size sampling only to the positive native
  frequency range, preventing invented data between DC and that range.
- Treat the configured point count as the number of non-DC range points; DC is
  one additional point when present.

## 0.7.0 - 2026-08-17

- Add interactive native, point-count, and step-size frequency-grid selection
  to generic MDIF export.
- Add `--frequency-points`, `--frequency-step`, and
  `--native-frequency-grid` options for explicit RFPro launches.
- Resample over each result's inclusive native frequency span through the
  public `CircuitMatrix.Smatrix(frequency)` evaluator without re-simulation.
- Accept step units from hertz through terahertz and retain the final native
  endpoint when the requested step does not divide the span exactly.

## 0.6.0 - 2026-08-17

- Add a modeless RFPro sweep-geometry inspector that expands every native
  parameter combination and previews it in the active 3-D geometry view.
- Add Previous, Next, Fit View, and Check All controls without creating or
  queueing simulations.
- Report `geometry.isValid()` and `reasonWhyInvalid()` for every checked point,
  while retaining interactive visual inspection for unintended valid shapes.
- Restore the exact original project-parameter formulas when the inspector
  closes and never save the temporary preview state.

## 0.5.0 - 2026-08-16

- Set and verify the saved `SimulationData.reuseExistingResults` value before
  saving, then pass the same value through `reuseExistingIfPossible` when the
  analysis is submitted.
- Abort before saving or submitting if RFPro cannot retain the requested saved
  reuse setting.
- Add a read-only analysis reuse diagnostic for flow identity, sequence/result
  mappings, registered cache prerequisites, and reuse-related solver logs.
- Add a read-only unique cache inventory that distinguishes registered result
  paths from historical or orphaned FEM caches without repeating shared-tree
  matches for every condition.

## 0.4.0 - 2026-08-16

- Save the active RFPro project synchronously after confirmation and before
  submitting the analysis; a save error now prevents the run from starting.
- Add the editable `DEFAULT_REUSE_EXISTING_RESULTS` global and show its enabled
  or disabled state in the final run preview.
- Keep the required FEM environment values set globally for the remainder of
  the current RFPro session so queued solver processes inherit them.
- Remove the runner's `--no-save` option because runs now always save first.

## 0.3.2 - 2026-08-16

- Read swept FEM, CTI, or SIO circuit results directly with
  `empro.toolkit.getCircuitMatrix()` instead of requiring RFPro's nested result
  directories to register as result-browser projects.
- Add regression coverage for converting file-backed circuit matrices to MDIF.

## 0.3.1 - 2026-08-16

- Derive the owning RFPro result project from each case path and load swept
  S-parameters with that context plus the explicit simulation ID instead of
  treating each case directory as a result project.
- Add regression coverage for exporting an existing nested RFPro sweep result.

## 0.3.0 - 2026-08-16

- Apply the required waveguide horizontal factor `0.5`, vertical factor `2.0`,
  and finest-mesh setting `on` during explicit RFPro analysis submission.
- Show the private FEM environment overrides in the final run preview.
- Restore the exact previous process environment after the run call.

## 0.2.0 - 2026-08-16

- Add a separate, explicitly invoked RFPro analysis runner that requests reuse
  of valid existing results.
- Keep CSV import and simulation launch as independent user actions.
- Require confirmation immediately before starting or queuing simulations.

## 0.1.1 - 2026-08-16

- Prompt direct RFPro runs to choose between replacing all existing sweep
  sequences and appending the CSV cases.
- Retain explicit `--mode replace` and `--mode append` operation for scripted
  and non-interactive launches.

## 0.1.0 - 2026-08-16

- Add direct-in-RFPro CSV import of correlated geometry cases.
- Represent each CSV row as an independent native `ParameterSequence`.
- Add generic MDIF export for all available swept S-parameter results.
- Integrate scoped, cross-platform Qt startup from the PCell recovery project.
- Add CSV/MDIF unit tests, Qt diagnostics, examples, VS Code tasks, and CI.
