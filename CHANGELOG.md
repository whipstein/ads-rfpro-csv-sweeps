# Changelog

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
