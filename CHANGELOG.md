# Changelog

## 0.14.5 - 2026-08-20

- Load each saved Mesh/Ports result through a retained deep-copy of the RFPro
  `Analysis`, with parameter-sweep interpretation disabled only on the clone
  and the selected result's `simulationPath` left valid for the renderer's
  complete lifetime.
- Prevent RFPro from substituting the first sweep point and automatically
  acknowledge only the exact native first-sweep-point mesh notification if a
  release still presents it.
- Remove direct writes to RFPro's proprietary Qt item models, which could cross
  PySide/C++ ownership boundaries and terminate RFPro without a Python
  traceback; view controls now use live actions or buttons only.
- Retain the temporary Analysis until RFPro confirms that the Mesh layer has
  been unloaded, then release it before loading another point or restoring raw
  geometry.
- Regenerate both self-contained launchers with the corrected inspector.

## 0.14.4 - 2026-08-20

- Enable and verify RFPro's **View Faces** and **Ports** controls whenever the
  geometry inspector loads a saved FEM or Momentum Mesh/Ports result.
- Disable the active Mesh renderer before changing geometry points, loading the
  next result during PDF export, or restoring the original geometry.
- Support RFPro visibility state exposed as checkable menu actions, buttons,
  or item-view rows, and report discovered controls when an expected option is
  unavailable instead of silently displaying stale view state.
- Regenerate both self-contained launchers with the updated inspector.

## 0.14.3 - 2026-08-20

- Fix saved Mesh/Ports loading by passing RFPro's native FEM and Momentum view
  bindings the required `empro.analysis.Analysis`, rather than the selected
  `empro.output.SimulationOutput` that cannot be converted to `Analysis`.
- Temporarily point the analysis at the selected result's `simulationPath`
  during the display call and restore its exact original path afterward,
  including when RFPro raises an error.
- Regenerate both self-contained launchers with the corrected geometry and
  Mesh/Ports inspector payload.

## 0.14.2 - 2026-08-19

- Convert both combined launchers into true single-file bundles containing all
  selected operation implementations; no subsequent repository script is
  located or opened at runtime.
- Execute each selected operation as a registered in-memory module, preserving
  RFPro child-script behavior and Python `@dataclass` compatibility without
  another `empro.toolkit.scripting.run()` call.
- Compress the embedded source and verify its SHA-256 digest before execution,
  with readable standalone operation scripts retained as the source of truth.
- Add `scripts/build_rfpro_bundles.py` and regression checks that ensure every
  committed payload exactly matches its standalone source and loads without
  filesystem delegation.

## 0.14.1 - 2026-08-19

- Make `rfpro_workflow.py` and `rfpro_diagnostics.py` self-contained by
  embedding the complete Qt bootstrap, dropdown, analysis selection, and
  operation-dispatch implementation in each direct entry script.
- Remove the `rfpro_tool_launcher.py` runtime dependency that caused Keysight's
  scripting loader to raise `ModuleNotFoundError` when the helper was not
  present beside the selected entry file.
- Avoid `@dataclass` in the direct entry modules so they also load under
  Keysight's `_loadModule` lifecycle, which executes a source module without
  first inserting it into `sys.modules`.
- Retain delegation only for the existing operation scripts and report their
  exact expected path if one is missing.

## 0.14.0 - 2026-08-19

- Add `rfpro_workflow.py`, a combined dropdown for CSV import, native analysis
  execution, MDIF export, and Geometry/Mesh/Ports inspection.
- Add `rfpro_diagnostics.py`, a combined dropdown for duplicate-condition,
  reuse/result-mapping, cache-inventory, and geometry diagnostics.
- Delegate each launcher choice through the documented
  `empro.toolkit.scripting.run()` loader so the existing scripts retain their
  own tested dialogs, settings, confirmations, and entry points.
- Add a read-only duplicate sweep-condition audit that expands every native
  sequence, compares evaluated parameter mappings in RFPro reference units,
  and correlates redundant configured entries with missing registered results.
- Carry the resilient Keysight Qt bootstrap in the shared launcher, including
  reuse of RFPro's existing `QApplication` and automatic platform-plugin
  discovery for script-owned applications.

## 0.13.0 - 2026-08-19

- Report configured sweep cases, RFPro-registered results, and raw circuit
  result-directory counts before MDIF collection.
- Add `DEFAULT_BYPASS_RESULT_REGISTRATION`,
  `--bypass-design-point-check`, and `--bypass-result-registration` to export
  raw `design.sio`/`proj.sio` result directories that RFPro omitted from
  `AnalysisOutput.getAvailableSimulationIds()`.
- Retain safe registered-result enumeration by default and warn that the raw
  bypass can include stale or orphaned results.

## 0.12.2 - 2026-08-18

- Remove the RFPro-side bounded submission implementation after runtime use
  showed that unqueueing and later requeueing `runAnalysis()`-owned simulations
  can desynchronize RFPro's native `SimulationsTable`.
- Restore direct native `runAnalysis()` submission so RFPro retains ownership
  of analysis expansion, result reuse, and queue state.
- Document that SiteCluster concurrency must be limited in the external
  scheduler/site submission configuration, not by mutating RFPro's analysis
  simulation table.

## 0.12.1 - 2026-08-18

- Add `DEFAULT_DEDUPLICATE_CASES` and `--allow-duplicate-cases` so append mode
  can bypass both existing-condition matching and duplicate-CSV-row matching.
- Make the confirmation preview explicitly identify when every enabled CSV row
  will be appended, including exact duplicates.
- Reject disabled duplicate matching in replace mode, where safely retaining
  existing native sequence objects requires comparison.

## 0.12.0 - 2026-08-18

- Add bounded SiteCluster submission to the explicit RFPro runner, with an
  editable/CLI maximum active-simulation count and a sliding window that
  submits a replacement only after an active job reaches a terminal status.
- Preserve RFPro's native Auto/reuse selection by staging the jobs created by
  `runAnalysis()` under `SimulationList.isQueueHeld`, unqueueing them, and then
  releasing them individually with `Simulation.setQueued(True)`.
- Refuse to mix a new bounded run with an already active or held RFPro queue.
- Stop new submissions after the first failed job by default while allowing
  already active jobs to finish; add `--continue-on-error` as an explicit
  override.
- Leave the RFPro queue held if the staging/unqueue operation cannot be
  verified, preventing an unsafe all-at-once SiteCluster launch.

## 0.11.3 - 2026-08-17

- Default the analysis runner to RFPro's native Auto/reuse launch path by using
  `waitForConfirmation=True` instead of silently authorizing overwrite.
- Prevent the legacy/fallback extraction branch from deleting registered
  results and making saved meshes disappear without a native RFPro warning.
- Retain explicit scripted reuse/overwrite as an opt-in global mode and show
  both public submission arguments in the pre-run preview.

## 0.11.2 - 2026-08-17

- Stop assigning the undocumented per-analysis
  `simulationSettings.reuseExistingResults` attribute, which is not writable in
  some RFPro analysis bindings and is not consumed by the extraction run flow.
- Keep the editable reuse global and pass it explicitly through the documented
  `runAnalysis(..., reuseExistingIfPossible=...)` argument.
- Preserve the explicit pre-run project save and persistent RFPro-session FEM
  environment overrides.

## 0.11.1 - 2026-08-17

- Fix replace-mode reuse of borrowed `ParameterSequence` wrappers: RFPro
  invalidates those wrappers as soon as their owning list is cleared, causing
  a null-PyObject dereference and leaving the sweep list empty.
- Convert replace to append-only whenever the CSV retains every existing
  condition, so matching native sequences and their ordering are untouched.
- Block a replace that would remove/change existing conditions before any
  mutation unless destructive replacement is explicitly enabled.
- Make an opted-in destructive replace use only newly constructed sequences
  plus detached pre-clear backups that are restored if installation fails.
- Add a regression fake that invalidates borrowed wrappers on `clear()`,
  matching RFPro's observed object-lifetime behavior.

## 0.11.0 - 2026-08-17

- Filter CSV headings against the active project's exact editable parameter
  names and ignore all other metadata columns, including blank cells.
- Add `DEFAULT_VALUE_SCALE` and `--scale` to apply one dimensionless
  CSV-to-RFPro multiplier while preserving RFPro expressions and units.
- Detect existing independent sweep groups from their evaluated RFPro values
  with configurable relative and absolute tolerances.
- Make append add only genuinely new conditions and perform no sequence-list
  mutation or project save when every CSV condition already exists.
- Attempt replace-mode reuse of matching native sequence wrappers while adding
  new cases, removing stale cases, and skipping duplicate CSV rows; corrected
  in 0.11.1 after RFPro lifetime testing exposed wrapper invalidation.

## 0.10.0 - 2026-08-17

- Add a **Mesh/Ports** result-status column and **Load Mesh/Ports** action to
  the sweep geometry inspector.
- Discover saved FEM and Momentum `*.ovm` data through public analysis output
  objects and load it with the RFPro Mesh/Ports geometry-view bindings used by
  Keysight's `empro.toolkit.analysis.viewMesh()` implementation.
- Map partial result sets to sweep points by parameter metadata and use result
  order only for complete result sets, avoiding unsafe shifts across unsolved
  conditions.
- Add **Mesh/Ports PDF** export using RFPro's verified **View > Export Image**
  action, landscape pages, `um` parameter formatting, missing-result
  diagnostics, and an explicit guarantee that no simulation is started.

## 0.9.0 - 2026-08-17

- Change geometry-validation reports to landscape Letter pages and compact the
  metadata, margins, spacing, and footer so the RFPro geometry occupies most
  of each page.
- Convert PDF geometry parameters from their evaluated reference length or
  explicit display unit to `um`.
- Add `DEFAULT_REPORT_PARAMETER_DECIMAL_PLACES` near the script settings for
  configurable rounding; default to three decimal places and trim trailing
  zeros from the rendered values.

## 0.8.5 - 2026-08-17

- Complete RFPro's **Enter Name for Geometry Image** `QFileDialog` by setting
  an absolute path and clicking its Save/default button on the next Qt event
  turn instead of calling `accept()` immediately after `selectFile()`.
- Record the dialog's actual `selectedFiles()`, directory, filters, acceptance
  signal, and button path in export diagnostics.
- Keep processing RFPro events for up to 12 seconds after the action returns
  so an asynchronously written image is not rejected prematurely.
- Recognize and normalize RFPro-appended `.png` filename variants before
  deciding that the native export failed.

## 0.8.4 - 2026-08-17

- Retain the complete RFPro `QMenuBar`/`QMenu`/submenu/`QAction` ownership
  chain until each **View > Export Image** save operation has returned.
- Prefer traversal of the live RFPro main-window **View** menu over a broad
  Qt child-action search that can include stale actions from transient views.
- Validate PySide wrappers with `shiboken6.isValid()` during discovery and
  immediately before triggering, skipping any action whose C++ object was
  already deleted.

## 0.8.3 - 2026-08-17

- Replace all framebuffer, widget-grab, and native-window screenshot attempts
  with RFPro's actual **View > Export Image** action.
- Drive the action's save dialog with a numbered PNG path and select PNG when
  the export dialog offers multiple image formats.
- Require RFPro to create a nonempty PNG for every included point; stop on the
  first export failure and do not create a placeholder PDF.
- Report the discovered menu action and save-dialog state when the native
  export cannot be completed, while retaining any PNGs already exported.

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
