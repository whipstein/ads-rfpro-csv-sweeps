# RFPro CSV Parameter Sweeps and MDIF Export

This repository provides RFPro workflow and diagnostic scripts that run
directly in an open Keysight RFPro process:

- `rfpro_scripts/rfpro_workflow.py` opens one dropdown for CSV import,
  analysis execution, MDIF export, or Geometry/Mesh/Ports inspection.
- `rfpro_scripts/rfpro_diagnostics.py` opens one dropdown for the duplicate
  condition audit, reuse/result mapping report, reusable-cache inventory, or
  Geometry/Mesh/Ports inspection.
- `rfpro_scripts/import_csv_parameter_sweeps.py` installs correlated geometry
  cases from CSV into an existing RFPro analysis.
- `rfpro_scripts/export_analysis_mdif.py` exports all available swept
  S-parameter results from an analysis to one generic MDIF file.
- `rfpro_scripts/run_analysis_reuse_existing.py` explicitly starts an analysis
  later while requesting reuse of valid existing results through RFPro's native
  analysis queue lifecycle.
- `rfpro_scripts/preview_sweep_geometries.py` expands every configured sweep
  point, displays its regenerated geometry, and loads or exports available
  saved Mesh/Ports results in RFPro for inspection.
- `rfpro_scripts/diagnose_analysis_reuse.py` reports an analysis's result
  mappings, per-condition cache files, and reuse-related logs.
- `rfpro_scripts/find_reusable_simulation_caches.py` inventories unique FEM
  caches and distinguishes registered paths from historical/orphaned paths.
- `rfpro_scripts/diagnose_duplicate_sweep_conditions.py` expands the configured
  parameter sequences and reports conditions that evaluate to the same RFPro
  reference-unit values.

The current release is **0.14.0**.

## Execution model

These are in-application RFPro scripts. They use the active
`empro.activeProject` and must not be run with an unrelated system Python.
The standalone tools are self-contained, including Qt startup. The two compact
combined entry scripts delegate to their sibling shared launcher, which carries
the same Qt startup implementation. The repository does not need to be
installed as a Python package.

From RFPro's Python console, run a script with the documented scripting
loader:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\ads-rfpro-csv-sweeps\rfpro_scripts\import_csv_parameter_sweeps.py"
)
```

For the combined dropdowns, use:

```python
from empro.toolkit import scripting

scripting.run(r"C:\path\to\rfpro_scripts\rfpro_workflow.py")
scripting.run(r"C:\path\to\rfpro_scripts\rfpro_diagnostics.py")
```

The workflow dropdown contains **Import CSV parameter sweeps**, **Save and run
analysis**, **Export analysis results to MDIF**, and **Geometry and Mesh/Ports
inspector**. The diagnostics dropdown contains **Duplicate sweep-condition
audit**, **Analysis reuse and result mappings**, **Reusable simulation-cache
inventory**, and the same geometry inspector. Each selection delegates through
`empro.toolkit.scripting.run()` to the existing tested script, so its own
preview, confirmation, and settings remain authoritative.

The launcher first selects the operation and then the analysis. To preselect
both without showing those two chooser dialogs, pass their keys directly:

```python
scripting.run(
    r"C:\path\to\rfpro_scripts\rfpro_workflow.py",
    ["--operation", "geometry_inspector", "--analysis", "My RF Analysis"],
)
scripting.run(
    r"C:\path\to\rfpro_scripts\rfpro_diagnostics.py",
    ["--operation", "duplicate_conditions", "--analysis", "My RF Analysis"],
)
```

Run a standalone child script when it needs additional command-line options;
the combined launchers intentionally pass only the selected analysis and let
interactive child dialogs collect the rest.

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
        "--mode", "append",
        "--scale", "1e-6",
        "--yes",
    ],
)
```

You can instead edit the `DEFAULT_*` constants near the top of each production
script when the RFPro launcher cannot pass arguments.

## CSV contract

CSV headings whose exact, case-sensitive names match editable parameters in
`empro.activeProject.parameters` are imported. Every other heading is ignored
as metadata, so columns such as `verification_sequence` may be present and may
contain empty cells. Each enabled data row is one independent, correlated
geometry case:

```csv
__case__,__enabled__,verification_sequence,W,L,Gap,__comment__
case_001,true,,0.40 mm,1.20 mm,0.10 mm,training point
case_002,true,,0.55 mm,1.20 mm,0.12 mm,training point
case_003,false,1,0.70 mm,1.40 mm,0.15 mm,temporarily excluded
```

See `examples/geometry_cases.csv` for a ready-to-edit file.

Rules:

- One row becomes one native `ParameterSequence`.
- Every matched RFPro parameter cell in an enabled row must be non-empty.
- Headings that do not match an editable live-project parameter are ignored,
  even when their cells are blank. The confirmation preview lists them.
- Values are RFPro expressions, including units, such as `0.40 mm`.
- `DEFAULT_VALUE_SCALE` or `--scale` applies one dimensionless multiplier to
  every imported expression. For example, CSV value `400` with `--scale 1e-6`
  is installed as `(400)*1e-06`; values with units and formulas are preserved
  inside the scaled expression.
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
explicit. In `append` mode, existing sequences are never removed or replaced:
CSV cases matching an existing independent parameter group are skipped and
only new conditions are appended. This is the recommended mode when rows were
added to a previously imported CSV.

In `replace` mode, a CSV that contains every existing condition plus new points
is handled through the same append-only path, preserving the owning RFPro list
and every existing native sequence. If the CSV omits or changes an existing
condition, replacement would require clearing RFPro's owning
`ParameterSequenceList`. That operation is blocked by default because clearing
the list immediately invalidates Python wrappers borrowed from it and because
rebuilding the sweep definitions can invalidate result reuse.

An intentional destructive synchronization requires both `--mode replace` and
`--allow-destructive-replace`, or
`DEFAULT_ALLOW_DESTRUCTIVE_REPLACE = True`. It rebuilds the list exclusively
from newly constructed sequences, never from invalidated borrowed wrappers.
Before clearing, it creates detached copies of the prior definitions and uses
them for rollback if installation fails. Treat this opt-in operation as likely
to require result revalidation or simulation. Duplicate CSV rows are skipped
in both modes. If append finds that every condition already exists, the
importer does not mutate the sequence list and does not save the unchanged
project.

Matching uses the public evaluated `SingleParameterSweep.parameterValues`, so
equivalent unit expressions compare in RFPro reference units. It uses
`math.isclose()` with `DEFAULT_MATCH_REL_TOLERANCE` and
`DEFAULT_MATCH_ABS_TOLERANCE`; the same settings are available as
`--match-rel-tol` and `--match-abs-tol`. The preview reports retained, added,
skipped, and removed counts before confirmation. The script never creates or
queues simulations.

Setting both tolerances to zero disables only approximate matching; exact
evaluated matches are still duplicates. To bypass matching completely in
append mode, set:

```python
DEFAULT_DEDUPLICATE_CASES = False
```

or pass `--allow-duplicate-cases`. With this explicit override, every enabled
CSV row is appended without comparing it to existing RFPro conditions or to
earlier CSV rows. The confirmation preview states that duplicate matching is
disabled. Exact duplicates will also be appended, so restore the default after
the intended import if repeated conditions are not desired. This override is
rejected in replace mode because it cannot safely determine which existing
native sequences should be retained.

For non-interactive use, pass `--mode replace` or `--mode append`. You can also
set `DEFAULT_IMPORT_MODE` near the top of the script to either value to make it
the fixed behavior for launches that cannot pass arguments.

Useful importer options:

```text
--csv PATH
--analysis NAME
--mode {ask,replace,append}
--scale FACTOR
--match-rel-tol FACTOR
--match-abs-tol REFERENCE_VALUE
--allow-duplicate-cases
--allow-destructive-replace
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

Reports use landscape Letter pages with a compact metadata header so the RFPro
geometry image receives most of the printable area. Geometry parameters in the
PDF are converted to `um` and rounded using
`DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES` near the top of
`preview_sweep_geometries.py`; the default is three decimal places. Trailing
zeros are removed for a cleaner presentation.

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

### Inspect and export saved Mesh/Ports results

The inspector scans the selected analysis through
`empro.output.AnalysisOutput`, adds a **Mesh/Ports** status column, and maps
saved simulation results to configured sweep points. Partial result sets are
matched by parameter metadata. Positional order is used only when RFPro
returns a complete result set, so an unsolved point cannot silently shift all
later result-to-condition assignments.

**Load Mesh/Ports** loads the selected condition's saved result into RFPro's
combined Mesh/Ports result view and fits it to the window. FEM results use the
saved `*.ovm` under `<simulationPath>/emds_dsn/design`; Momentum results use
the saved `*.ovm` under `<simulationPath>/work`. The table distinguishes an
available result, an unmatched or unsolved point, and a saved result whose
mesh data is missing.

**Mesh/Ports PDF** scans again, then loads and exports every available saved
Mesh/Ports result through RFPro's same **View > Export Image** command used by
the raw-geometry report. It creates one verified PNG and one landscape PDF
page per available result. The completion message lists points with no matched
result, points whose result has no saved mesh, and result IDs that could not be
matched safely. Missing conditions are skipped; they are never simulated or
queued. If an actual view or image export fails, the batch stops and does not
create a misleading PDF.

Mesh/Ports reports use the same `um` scaling and
`DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES` rounding setting as geometry
reports. Because a solver Mesh/Ports view depends on a saved `*.ovm`, raw
geometry can still be inspected before simulation but a mesh cannot be shown
for a condition that has never produced mesh data.

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

The script deliberately does not throttle SiteCluster by holding, unqueueing,
and later requeueing RFPro-created analysis simulations. Those simulations are
owned by RFPro's native `SimulationsTable`; changing their queue membership
after `runAnalysis()` can desynchronize that table and produce
`SimulationsTable has corrupt state: number of simulations mismatch!`.

Set the concurrency or license limit in the SiteCluster scheduler submission
configuration instead. RFPro can then create and submit its analysis table
normally while the scheduler limits how many solver jobs run at once. The
exact setting is scheduler/site-template specific and is not inferred by this
repository.

The safe default follows RFPro's native analysis launch path, preserving the
same Auto reuse policy and native confirmation behavior used when starting the
analysis from the GUI:

```python
DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY = True
DEFAULT_REUSE_EXISTING_RESULTS = True
```

Keep `DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY=True` for normal use. RFPro then
owns the final Auto/reuse decision and may display its native confirmation
after the script's preview. Do not approve an overwrite there unless a full
rerun is intended. The script still passes the explicit reuse preference as a
secondary option, but it does not bypass RFPro's native policy:

```python
runAnalysis(
    analysis,
    waitForConfirmation=DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY,
    saveProject=True,
    reuseExistingIfPossible=DEFAULT_REUSE_EXISTING_RESULTS,
)
```

Setting `DEFAULT_USE_RFPRO_NATIVE_REUSE_POLICY=False` restores direct scripted
submission. With that setting, `DEFAULT_REUSE_EXISTING_RESULTS=True` requests
reuse and `False` requests overwrite. Direct submission is not the safe
default: in RFPro's legacy/fallback extraction branch,
`waitForConfirmation=False` authorizes overwrite and the branch does not
consume `reuseExistingIfPossible`. That path can remove registered results and
make their saved meshes disappear from the geometry inspector.

The script deliberately does not assign
`analysis.simulationSettings.reuseExistingResults`. Although that attribute
appears in generated `SimulationData` reference output, it is undocumented and
is not the control consumed by the RFPro extraction run flow. In some RFPro
analysis bindings it also cannot be assigned. The supported
`reuseExistingIfPossible` submission argument remains explicit on every run,
while the native-policy global controls whether RFPro gets the final
Auto/overwrite decision.

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

## Diagnostics

All three console diagnostics are read-only: they do not save the project,
modify an analysis, create simulations, or alter result files.

To investigate a configured-point count that is larger than the submitted or
registered-result count, run the duplicate-condition audit:

```python
from empro.toolkit import scripting

scripting.run(
    r"C:\path\to\rfpro_scripts\diagnose_duplicate_sweep_conditions.py",
    ["--analysis", "My RF Analysis"],
)
```

The audit expands every native `ParameterSequence`, evaluates public
`SingleParameterSweep.parameterValues` in RFPro reference units, and compares
complete parameter mappings with the same relative/absolute tolerance model as
the CSV importer. It prints the sequence and combination numbers for each
duplicate group, the configured and Python-expanded point counts, registered
simulation IDs/paths, and RFPro's sequence/result mappings. If the number of
redundant entries equals the registered-result shortfall—for example, three
redundant conditions alongside 48 configured entries and 45 results—the report
marks coalescing of repeated conditions as consistent with the counts, while
making clear that the count match alone is not proof.

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
diagnose_duplicate_sweep_conditions.py: --analysis NAME --match-rel-tol FACTOR --match-abs-tol REFERENCE_VALUE
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
DEFAULT_BYPASS_RESULT_REGISTRATION = False
```

The exporter uses `empro.output.AnalysisOutput` to enumerate analysis result
cases and `empro.toolkit.getCircuitMatrix()` to read each case's FEM, CTI, or
SIO result files directly. This avoids treating nested RFPro analysis folders
as standalone result-browser projects. The owning result directory is derived
from each simulation output path, and the leaf directory is selected by
simulation ID. Parameter values come from the result metadata, with the
configured analysis sweep as a fallback when its expanded case count matches
the results.

At the start of collection, the exporter reports three independent counts:
configured sweep cases, RFPro-registered results, and raw circuit-result
directories. The configured-case comparison never filters results; it only
controls whether positional geometry values are a safe metadata fallback.
Without `--skip-errors`, any per-result failure stops the export rather than
silently producing a partial file.

If RFPro registers fewer results than actually exist on disk, enable the
explicit bypass:

```python
DEFAULT_BYPASS_RESULT_REGISTRATION = True
```

or pass `--bypass-design-point-check` (also available as
`--bypass-result-registration`). The bypass scans the selected analysis's
direct `simulationGroupPath` children for the public RFPro EM result layouts
`emds_dsn/design/design.sio` and `work/proj.sio`, then exports those raw result
directories instead of limiting collection to
`AnalysisOutput.getAvailableSimulationIds()`. If all 48 raw directories exist
and match 48 configured cases, all 48 can be assigned their positional sweep
metadata. If only 45 raw result directories exist, no bypass can supply the
three missing S-matrices.

This option can include stale or orphaned result directories that RFPro no
longer associates with the analysis. Review the printed inventory and restore
the safe `False` default after the exceptional export.

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
--bypass-design-point-check
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
  `AnalysisList.names/index`,
  `AnalysisOutput`, `AnalysisOutput.getAvailableSimulationPaths()`,
  `SimulationOutput.metadata`, `SimulationOutput.simulationPath`,
  `DataSetMatrix`, `empro.toolkit.getCircuitMatrix()`, and
  `CircuitMatrix.Smatrix(frequency)` for frequency-grid evaluation.
- `SimulationData.femFrequencyPlanList()` and the public `FrequencyPlan`
  `enabled`, `sweepType` (legacy `type`), `startFrequency`, and `stopFrequency`
  properties for deriving the selected analysis's exact configured frequency
  regions.
- `empro.toolkit.analysis.runAnalysis()` and its documented `saveProject=True`
  and `reuseExistingIfPossible=True` options for saving and explicitly starting
  only after the user confirms.
- The shipped command-line simulation example was checked to distinguish its
  supported `createSimulation(False)` followed by `setQueued(True)` lifecycle
  from RFPro analysis simulations created and owned by `runAnalysis()`.
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
