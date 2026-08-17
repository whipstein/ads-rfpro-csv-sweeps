# RFPro CSV Parameter Sweeps and MDIF Export

This repository provides RFPro workflow and diagnostic scripts that run
directly in an open Keysight RFPro process:

- `rfpro_scripts/import_csv_parameter_sweeps.py` installs correlated geometry
  cases from CSV into an existing RFPro analysis.
- `rfpro_scripts/export_analysis_mdif.py` exports all available swept
  S-parameter results from an analysis to one generic MDIF file.
- `rfpro_scripts/run_analysis_reuse_existing.py` explicitly starts an analysis
  later while requesting reuse of valid existing results.
- `rfpro_scripts/preview_sweep_geometries.py` expands every configured sweep
  point and displays its regenerated geometry in RFPro for inspection.
- `rfpro_scripts/diagnose_analysis_reuse.py` reports an analysis's saved reuse
  setting, result mappings, per-condition cache files, and reuse-related logs.
- `rfpro_scripts/find_reusable_simulation_caches.py` inventories unique FEM
  caches and distinguishes registered paths from historical/orphaned paths.

The current release is **0.8.5**.

## Execution model

These are in-application RFPro scripts. They use the active
`empro.activeProject` and must not be run with an unrelated system Python.
Each file is self-contained, including Qt startup, so RFPro can load any
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

## Inspect every sweep geometry

Before launching an analysis, open the modeless sweep-geometry inspector:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\rfpro_scripts\preview_sweep_geometries.py",
    ["--analysis", "My RF Analysis"],
)
```

The inspector expands the selected analysis's native `parameterSequences`.
Selecting a table row resets all swept parameters to their original formulas,
applies that row's parameter combination, switches RFPro to the geometry view,
and refreshes the 3-D model. The dialog is modeless, so the model can still be
rotated, panned, and zoomed in the main RFPro window. **Previous**, **Next**,
and **Fit View** support visual review without creating simulations. **Fit
View** only fits the geometry that is currently displayed; it does not change
the project parameters. Use **Load Selected** to explicitly regenerate and
display the highlighted table row, including when that row was already
selected and therefore did not emit another selection-change event.

Setting `activeProject.parameters` changes the values shown in RFPro's
Parameters dialog, but that alone does not regenerate the layout PCell. After
loading the OA design-spec parameter metadata, the inspector therefore resets
and assigns the point formulas and submits only the swept parameter mapping to
the active layout's native `_updateDesignParameters(Mapping[str, str])`
binding. It pumps RFPro's event loop before repainting and fitting the model.
The same path restores the baseline geometry when the inspector closes.

This targeted ADS 2026 Update 2.1 binding is not part of the public EMPro
Python API, but is the required live RFPro geometry-update path established in
`ads-rfpro-pcell-recovery`. The inspector deliberately does not call
`layout.refresh()`, replace the RFPro view, or clear `.adsPcells`.

**Check All** regenerates every point and records the result of RFPro's public
`activeProject.geometry.isValid()` check. Invalid points are highlighted and
show `reasonWhyInvalid()` when RFPro supplies a reason. A `Valid` result only
means RFPro accepts the geometry; visual review is still necessary for shapes
that are technically valid but unintended.

**Check All + PDF** prompts for a report path, regenerates and fits every sweep
point, saves one numbered PNG per exported geometry in a sibling `<report
name>_images` directory, and creates one PDF page per checked point. Each page
includes the analysis name, point/sequence/combination number, parameter
values, validity result, and RFPro's failure reason when available. Existing
image directories are never replaced; a numeric suffix is used instead.

For every point, the report invokes RFPro's actual **View > Export Image** menu
action and supplies the numbered PNG path to the save dialog. The file must
exist and be nonempty before its PDF page is accepted. If RFPro cannot expose
the action, automate its dialog, or create the PNG, the batch stops at that
point and no PDF is written; any earlier verified PNGs are preserved. This
prevents a placeholder PDF from hiding an image-export failure. If no image
was exported, the unused empty image directory is removed. Canceling after at
least one successful point writes a partial PDF and keeps every PNG exported
up to that point. The row selected before the batch is loaded again when the
operation finishes.

The action lookup prefers the live RFPro main-window **View** menu and retains
its `QMenuBar`, `QMenu`, submenu, and `QAction` wrappers until the export dialog
has finished. Deleted PySide wrappers are rejected with `shiboken6.isValid()`
instead of being triggered after their underlying C++ action has disappeared.
The RFPro filename dialog is completed by selecting an absolute PNG path and
clicking its Save/default button after Qt has committed the selection. The
script records `selectedFiles()`, keeps processing RFPro events while the image
is written, and recognizes RFPro-appended PNG suffixes before verifying the
numbered output file.

The script never saves the project and never creates, queues, reruns, or
deletes a simulation. It captures the original formulas before opening and
restores them when the inspector closes, including when a second inspector
replaces an existing one.

Useful inspector options:

```text
--analysis NAME
--zoom-to-extents
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
After confirmation it explicitly saves the active RFPro project, then calls the
public `empro.toolkit.analysis.runAnalysis()` API. A save failure stops the
operation before any simulation is submitted.

Result reuse is controlled by this global near the top of the runner:

```python
DEFAULT_REUSE_EXISTING_RESULTS = True
```

With `True`, RFPro skips existing result sets only when it still considers them
valid; missing or invalidated cases are queued. Set it to `False` to request a
run regardless of existing results, which may queue every configured instance.
The selected mode is shown in the final confirmation preview. Before saving,
the runner also assigns and verifies the same value on the analysis:

```python
analysis.simulationSettings.reuseExistingResults = DEFAULT_REUSE_EXISTING_RESULTS
```

The saved `reuseExistingResults` setting and the submission-time
`reuseExistingIfPossible` argument therefore cannot silently disagree. If the
saved setting cannot be assigned or read back, the project is not saved and no
simulation is submitted.

The runner applies these required private FEM environment controls to the
current RFPro process before submission:

```text
FEMIZER_WAVEGUIDE_HORIZONTAL_FACTOR=0.5
FEMIZER_WAVEGUIDE_VERTICAL_FACTOR=2.0
FEM_ALWAYS_SOLVE_ON_FINEST_MESH=on
```

They are shown in the final confirmation preview and remain set for the rest
of the current RFPro session, including after `runAnalysis()` returns or raises
an exception. This allows solver processes launched asynchronously from the
queue to inherit the required values. Running the script again reapplies the
same values. Importing CSV cases never sets these variables.

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
--yes
```

## Reuse diagnostics

Both reuse diagnostics are read-only: they do not save the project, modify an
analysis, create simulations, or alter result files.

To inspect the current analysis/result association, registered condition paths,
required FEM cache files, private flow version, and relevant solver-log lines:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\rfpro_scripts\diagnose_analysis_reuse.py",
    ["--analysis", "My RF Analysis"],
)
```

The summary separately reports result IDs, registered paths, `.reuse.hash`
files, and `emds_dsn/design/.reusable` markers. This prevents a cache found
elsewhere in the result tree from being mistaken for the cache registered to a
specific condition.

To locate every unique FEM cache beneath the RFPro result area and compare it
with the analysis's registered paths:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\find_reusable_simulation_caches.py",
    ["--analysis", "My RF Analysis"],
)
```

The cache finder walks two parent directories above `simulationGroupPath` by
default. Set `DEFAULT_SCAN_ROOT`, pass `--root`, or adjust `--parent-levels`
when a project's result layout differs:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\find_reusable_simulation_caches.py",
    [
        "--analysis", "My RF Analysis",
        "--root", r"C:\my_workspace\data\rfpro",
    ],
)
```

Useful diagnostic options:

```text
diagnose_analysis_reuse.py: --analysis NAME --log-limit 20
find_reusable_simulation_caches.py: --analysis NAME --root PATH --parent-levels 2
```

## MDIF export workflow

After the analysis has results, run:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\ads-rfpro-csv-sweeps\rfpro_scripts\export_analysis_mdif.py"
)
```

The interactive exporter asks whether to keep each result's native frequency
samples, generate a specified number of uniformly spaced points, or use a
frequency step size.

For an explicit, non-interactive export:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\export_analysis_mdif.py",
    [
        "--analysis", "My RF Analysis",
        "--output", r"C:\data\rfpro_sweeps.mdif",
        "--parameter-names", "W,L,Gap",
        "--frequency-points", "401",
        "--overwrite",
    ],
)
```

Use exactly one of these frequency-grid options:

```text
--native-frequency-grid
--frequency-points 401
--frequency-step "25 MHz"
```

For point-count and step-size modes, the exporter reads the enabled
`FrequencyPlan` entries from the selected analysis's
`simulationSettings.femFrequencyPlanList()`. It does not infer range boundaries
from the circuit result's internal sample frequencies.

Each configured single-frequency plan is emitted once. Each configured range
is sampled independently, including both of its configured endpoints, so no
data is generated across gaps between plans. For example, plans for `0..0 Hz`
and `1..20 GHz` produce one DC row followed by the requested sampling from
exactly 1 GHz through 20 GHz. With `--frequency-points 401`, each configured
non-single range receives 401 points; configured single points such as DC are
additional. Step mode retains the requested spacing inside every configured
range and uses a shorter final interval when necessary to include its exact
stop frequency.

RFPro's `Single` plan uses only `startFrequency`; its stored `stopFrequency`
can contain a stale value that is not shown in the analysis options. The
exporter therefore honors `sweepType` (and the legacy `type` property) and
forces a Single plan's effective stop to equal its start. It prints each
plan's raw properties and effective export region so the interpreted setup is
visible before result blocks are written.

Unitless step values are hertz, and `Hz`, `kHz`, `MHz`, `GHz`, and `THz` are
accepted. RFPro evaluates every requested S-matrix through the public
`CircuitMatrix.Smatrix(frequency)` API; this resamples existing results and
does not run another simulation.

For direct RFPro launches that cannot pass arguments, configure these globals
near the top of the exporter:

```python
DEFAULT_FREQUENCY_MODE = "ask"  # ask, native, points, or step
DEFAULT_FREQUENCY_POINTS = 201
DEFAULT_FREQUENCY_STEP = "100 MHz"
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
--native-frequency-grid
--frequency-points 401
--frequency-step "25 MHz"
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
- `python_scripts/startup.py` and `python_scripts/addons/ScaleViewZ.py` for
  `activeProjectView()`, `showGeometryView()`, `geometryView()`, `updateView()`,
  and fitting the active RFPro 3-D view.
- EMPro's shipped `python_scripts/startup.py` for
  `activeProjectView().menu(name)`, recursive menu actions, and the native
  action objects used by RFPro.
- EMPro public Python documentation for `Analysis.simulationSettings`,
  `SimulationData.reuseExistingResults`, `AnalysisList.names/index`,
  `AnalysisOutput`, `AnalysisOutput.getAvailableSimulationPaths()`,
  `SimulationOutput.metadata`, `SimulationOutput.simulationPath`,
  `DataSetMatrix`, `empro.toolkit.getCircuitMatrix()`, and
  `CircuitMatrix.Smatrix(frequency)` for frequency-grid evaluation.
- `SimulationData.femFrequencyPlanList()` and the public `FrequencyPlan`
  `enabled`, `sweepType` (legacy `type`), `startFrequency`, and `stopFrequency`
  properties for deriving the selected analysis's exact configured frequency
  regions.
- `empro.toolkit.analysis.runAnalysis()` and its
  `reuseExistingIfPossible=True` option for explicitly starting only after the
  user confirms.
- `empro.toolkit.scripting.run()` for direct in-application loading and
  `main()` invocation.
- Qt for Python's public `QAction.trigger()`, `QFileDialog.selectFile()`,
  `QTimer`, and `QPdfWriter`/`QPainter` APIs for invoking RFPro's image export,
  supplying each PNG path, and creating the multi-page PDF without an
  additional PDF dependency.

The inspector's `_loadOaParametersFromDesignSpec()` and
`layout._updateDesignParameters()` calls are intentional implementation-level
exceptions. ADS 2026 Update 2.1 does not expose a public equivalent that
regenerates the active RFPro PCell after `ParameterList.setFormula()`; the
targeted call signature and lifecycle are carried over from the verified
`ads-rfpro-pcell-recovery` runtime helper.

The three private FEM environment variables used by the explicit runner are
intentional project requirements supplied for the target RFPro installation;
they are not part of the public documented API corpus.

Final verification against the installed target release remains required.
