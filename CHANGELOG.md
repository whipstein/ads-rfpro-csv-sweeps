# Changelog

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
