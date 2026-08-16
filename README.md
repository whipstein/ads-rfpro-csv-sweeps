# RFPro CSV Parameter Sweeps and MDIF Export

This repository provides three scripts that run directly in an open Keysight
RFPro process:

- `rfpro_scripts/import_csv_parameter_sweeps.py` installs correlated geometry
  cases from CSV into an existing RFPro analysis.
- `rfpro_scripts/export_analysis_mdif.py` exports all available swept
  S-parameter results from an analysis to one generic MDIF file.
- `rfpro_scripts/run_analysis_reuse_existing.py` explicitly starts an analysis
  later while requesting reuse of valid existing results.

The current release is **0.3.0**.

## Execution model

These are in-application RFPro scripts. They use the active
`empro.activeProject` and must not be run with an unrelated system Python.
Each file is self-contained, including Qt startup, so RFPro can load either
file without installing this repository as a Python package.

From RFPro's Python console, run a script with the documented scripting
loader:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\ads-rfpro-csv-sweeps\rfpro_scripts\import_csv_parameter_sweeps.py"
)
```

With no arguments, the importer opens dialogs for the analysis and CSV file,
then explicitly asks whether to replace all existing sweep sequences or append
the CSV cases. It shows a preview and asks for final confirmation before making
the change. Append is preselected in the interactive chooser. The exporter
similarly asks for the analysis and output MDIF path.

RFPro's scripting loader can also pass the argument list expected by
`main(argv)`:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\import_csv_parameter_sweeps.py",
    [
        "--csv", r"C:\data\geometry_cases.csv",
        "--analysis", "My RF Analysis",
        "--mode", "replace",
        "--yes",
    ],
)
```

You can instead edit the `DEFAULT_*` constants near the top of each production
script when the RFPro launcher cannot pass arguments.

## CSV contract

The required CSV columns are the exact, case-sensitive names of editable
parameters in `empro.activeProject.parameters`. Each enabled data row is one
independent, correlated geometry case:

```csv
__case__,__enabled__,W,L,Gap,__comment__
case_001,true,0.40 mm,1.20 mm,0.10 mm,training point
case_002,true,0.55 mm,1.20 mm,0.12 mm,training point
case_003,false,0.70 mm,1.40 mm,0.15 mm,temporarily excluded
```

See `examples/geometry_cases.csv` for a ready-to-edit file.

Rules:

- One row becomes one native `ParameterSequence`.
- Every parameter cell in an enabled row must be non-empty.
- Values are RFPro expressions, including units, such as `0.40 mm`.
- A cell cannot contain a comma because RFPro interprets commas as multiple
  sweep values; that would break the one-row/one-case relationship.
- Empty rows are ignored.
- `__enabled__` is optional and accepts `true/false`, `yes/no`, `on/off`, or
  `1/0`.
- `__case__` and `__comment__` are optional descriptive CSV metadata. They are
  used in the preview and are not RFPro geometry parameters.

The important distinction is correlation. Given rows `(W=1, L=10)` and
`(W=2, L=20)`, the importer creates exactly those two cases. It does not create
the Cartesian combinations `(1,20)` and `(2,10)`.

## Import workflow

1. Open the RFPro project containing the geometry parameters and target
   analysis.
2. Run `import_csv_parameter_sweeps.py` inside that RFPro process.
3. Select the analysis and CSV, then review the preview.
4. Confirm the change.
5. Inspect the analysis's parameter sweep in RFPro, then run it through the
   normal RFPro workflow.

The default mode is `ask`, so an interactive RFPro run always makes the choice
explicit. In `replace` mode, existing `parameterSequences` are cleared only
after the complete CSV has been parsed, validated, and converted to native
objects. In `append` mode, all existing sequences are preserved and the CSV
cases are added after them. The preview reports the selected operation before
the final confirmation. The script enables the parameter sweep, saves the
active project by default, and does not create or queue simulations.

For non-interactive use, pass `--mode replace` or `--mode append`. You can also
set `DEFAULT_IMPORT_MODE` near the top of the script to either value to make it
the fixed behavior for launches that cannot pass arguments.

Useful importer options:

```text
--csv PATH
--analysis NAME
--mode {ask,replace,append}
--no-save
--yes
```

## Explicitly run with existing-result reuse

Importing or appending CSV cases never launches a simulation. When the analysis
is ready, explicitly run the separate reuse script:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\rfpro_scripts\run_analysis_reuse_existing.py"
)
```

The script asks you to choose an analysis, reports the configured instance and
existing-result counts, and defaults the final start confirmation to **No**.
After confirmation it calls the public `empro.toolkit.analysis.runAnalysis()`
API with `reuseExistingIfPossible=True`. RFPro skips existing result sets only
when it still considers them valid; missing or invalidated cases are queued.

The runner also applies these required private FEM environment controls for
the complete `runAnalysis()` call:

```text
FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR=0.5
FEMIZER_WAVEGUIDE_VERTICAL_FACTOR=2.0
FEM_ALWAYS_SOLVE_ON_FINEST_MESH=on
```

They are shown in the final confirmation preview. The script records whether
each variable was originally unset, empty, or assigned another value, then
restores that exact state after RFPro accepts the run request, including when
the call raises an exception. Importing CSV cases never sets these variables.

For an explicit scripted launch:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\run_analysis_reuse_existing.py",
    ["--analysis", "My RF Analysis", "--yes"],
)
```

Useful runner options:

```text
--analysis NAME
--no-save
--yes
```

## MDIF export workflow

After the analysis has results, run:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\ads-rfpro-csv-sweeps\rfpro_scripts\export_analysis_mdif.py"
)
```

For an explicit, non-interactive export:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\export_analysis_mdif.py",
    [
        "--analysis", "My RF Analysis",
        "--output", r"C:\data\rfpro_sweeps.mdif",
        "--parameter-names", "W,L,Gap",
        "--overwrite",
    ],
)
```

The exporter uses `empro.output.AnalysisOutput` to enumerate analysis result
cases and `empro.toolkit.getCircuitMatrix()` to read each case's FEM, CTI, or
SIO result files directly. This avoids treating nested RFPro analysis folders
as standalone result-browser projects. The owning result directory is derived
from each simulation output path, and the leaf directory is selected by
simulation ID. Parameter values come from the result metadata, with the
configured analysis sweep as a fallback when its expanded case count matches
the results.

The output contains one block per result:

```text
! simulation_id=000001
VAR W=0.40mm
VAR L=1.20mm
BEGIN ACDATA
% Freq S11 S12 S21 S22
# Hz S RI R 50
...
END
```

Writes are atomic: the complete MDIF is written beside the destination and
then moved into place. Existing files require confirmation unless
`--overwrite` is supplied. By default one bad or incomplete simulation stops
the export; `--skip-errors` explicitly permits partial output.

`--reference-impedance` declares the single reference resistance in the MDIF
header. It does not renormalize RFPro's S-parameters. Keep the default 50 ohms
only when that matches the results being exported.

Useful exporter options:

```text
--output PATH
--analysis NAME
--parameter-names W,L,Gap
--reference-impedance 50
--skip-errors
--overwrite
```

## Integrated Qt behavior

All production scripts carry the startup implementation from
`ads-rfpro-pcell-recovery`:

1. Import PySide6 and check for an existing `QApplication` before searching
   for any plugin.
2. Reuse RFPro-owned Qt without changing the environment or library paths.
3. For a script-owned app, ask `QLibraryInfo` and
   `QCoreApplication.libraryPaths()` for plugin roots, then check standard
   PySide6, ADS, and EMPro locations.
4. On Linux, report unresolved `ldd` dependencies and require a graphical
   display for graphical RFPro.
5. Redirect `QT_QPA_PLATFORM_PLUGIN_PATH` only during `QApplication([])`
   construction and restore the exact previous state in `finally`.
6. Keep the application object alive for the complete RFPro operation.

The scripts do not install a second PySide6 and do not force an offscreen
platform for RFPro.

If startup fails, run these with the exact RFPro interpreter and launcher:

```python
from empro.toolkit import scripting

scripting.run(r"C:\path\to\scripts\diagnose_qt.py")
scripting.run(r"C:\path\to\scripts\test_qt_startup.py")
```

## Local static validation

The RFPro API is imported only inside `main()`, allowing CSV and MDIF logic to
be tested without Keysight software:

```bash
python -m py_compile rfpro_scripts/*.py scripts/*.py
python -m unittest discover -s tests -v
```

Runtime validation still must happen inside the target RFPro release. Syntax
checks cannot exercise native RFPro state, result files, or Qt platform
loading.

## Verified API basis and limitation

No ADS/EMPro installation is available on the development machine. The code
was therefore checked in reference-only mode against the bundled ADS 2026
Update 2.1 and EMPro 2026 corpus:

- `python_scripts/demo/commandline/run_simulation.py` for
  `parameterSweepEnabled`, `ParameterSequence`, and `SingleParameterSweep`.
- `python_scripts/addons/CreateScript.py` for serializing
  `parameterSequences` and unit-preserving sweep values.
- `python_scripts/addons/SimpleParameterSweep.py` for editable project
  parameters and `setParameterValues()`.
- EMPro public Python documentation for `Analysis.simulationSettings`,
  `AnalysisList.names/index`, `AnalysisOutput`, `SimulationOutput.metadata`,
  `SimulationOutput.simulationPath`, `DataSetMatrix`, and
  `empro.toolkit.getCircuitMatrix()`.
- `empro.toolkit.analysis.runAnalysis()` and its
  `reuseExistingIfPossible=True` option for explicitly starting only after the
  user confirms.
- `empro.toolkit.scripting.run()` for direct in-application loading and
  `main()` invocation.

The three private FEM environment variables used by the explicit runner are
intentional project requirements supplied for the target RFPro installation;
they are not part of the public documented API corpus.

Final verification against the installed target release remains required.
