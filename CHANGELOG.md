# Changelog

## 0.3.1 - 2026-08-16

- Load swept S-parameters with the RFPro analysis result context and explicit
  simulation ID instead of treating each case directory as a result project.
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
