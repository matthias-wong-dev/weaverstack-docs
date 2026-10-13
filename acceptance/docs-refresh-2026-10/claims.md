# Consequential claims and owning pages

Baseline: see [baseline](baseline.md). This is a maintainer ledger, not public copy. Every row starts **source-backed/not yet verified**; package authors add exact tests/commands/results rather than promoting evidence by assumption.

| Claim | Implementation evidence | Public owner | Mode | Initial verification |
| --- | --- | --- | --- | --- |
| Catalogue-free native model/linked Report deployment; source bytes preserved | `src/weaver/operations/build.py`, `powerbi.py`, `build_bundle/semantic.py`, `semantic_models/deployed.py`; locate catalogue-free/Report/preservation tests | `reference/power-bi/requirements-and-compatibility.md`, Build behaviour | Power BI standalone and catalogue | Source audit pending; no live deployment |
| Model refresh without persisted status in catalogue-free mode; no Report Load/Test | `operations/load.py::_refuse_without_catalogue`, `operations/test.py` | Load/Test behaviour; compatibility matrix | Mode-specific | Load source read; source tests not run |
| Target names, linked Report resolution, source expression mapping and credentials are separate | `powerbi.py`, `semantic_models/binding.py`, `expressions.py`, `config.py` | Power BI compatibility, workspace config | Both | Source audit pending |
| Build read-only preview is not bundle-only and requires existing targets | `operations/build.py`, `build_bundle/workflow.py`; `targeted/test_build_preview*` | CLI Build and Build behaviour | All selected supported types | Source audit pending |
| Plain Load regex is whole-name/case-insensitive, requires each match, operator override | `operations/load.py`, `selection.py`; `test_cli_load_representation.py` | Load CLI/behaviour; shared selection | Installed graph only | Load docstring read; tests not run |
| Ancestors/descendants expand original seeds separately inside named items | `operations/load.py`, `load_plan.py`; `targeted/test_load_recursive_selection_cycle.py` | Load behaviour; advanced partial-run task | Installed graph only | Load source read; exact fixture/test evidence pending |
| Reload empties reached tables and resets progress; cannot combine stale/reload | `operations/load.py`; reload/stale selection tests | Load behaviour | Catalogue-backed tables | Source-backed; execution pending |
| Invocation concurrency is total scheduled cap; resource caps remain | `concurrency.py`, `workspaces.py`, run/build schedulers; targeted invocation tests | Workspace config; Build/Load/Test; Advanced concurrency | Mode-specific | Source audit pending |
| File-mode Test uses names/files/source and returned report | `operations/test.py`, `semantic_validation.py`; file/DAX tests | Test CLI/Python/behaviour; Power BI validations | File vs installed | Source audit pending |
| Native modelling annotations, shared policy and composition do not generally need a catalogue | `semantic_models/{annotation,builtin_annotations,composition,extensions,tmdl}.py` | Power BI annotations/TMDL/layout and public extension API | Standalone except metadata-dependent features | Source audit pending |
| Managed-source generation and DAX/SQL require supported source metadata/access | `semantic_models/source.py`, `semantic_validation.py` | Power BI validations/compatibility | Fabric-integrated | Source audit pending; live not authorised |
| Mirror/protection is live borrowing, not backup or universal deletion protection | `operations/mirror.py`, materialisation modules; protected mirror tests | Mirror/Wipe behaviour; protection guides | Fabric | Source audit pending |
| Unbind removes catalogue claims without deleting physical items | `operations/unbind.py` | Unbind CLI/behaviour | Catalogue-backed | Source audit pending |
| Selected semantic models redeploy; Report-only skip depends on catalogue state | `build_bundle/semantic.py`, Report catalogue tests | Build behaviour; compatibility | Mode-specific | Source audit pending |
| Workflow findings, execution errors and exit outcome differ | CLI workflow dispatcher/result, operation reports | Workflow behaviour/config; machine output | CLI/workflow | Source audit pending |
| Catalogue tables/columns and bundle/JSON formats are current representations, not promised compatibility | `catalogue/tables.py`, fragments; bundle/report serialization | Catalogue schema/bundle/machine output | Selected revision | Inventory comparison pending |
| #193 F64 seven-operation benchmark and tuning probes are historical measurements | GitHub PR #193 body/comments; no new run | Product scale/JSON; Advanced performance | Synthetic source estate, not models/Reports | PR re-read and number validation pending |
| Ordinary native authoring/output does not imply compiled-TMDL export or zero runtime dependencies | Public APIs/compiler/runtime source | Power BI compatibility and product item pages | Both | Export withheld by scope; API inventory pending |

## Reader page ownership

New tasks D01–D06: `basics/power-bi/{index,deploy-pbip,environments,validate,modelling-rule,fabric-integration}.md`.
New tasks D07–D09: `advanced/{run-part-of-an-estate,concurrency,performance-and-scale}.md`.
New tasks D10–D13: `advanced/power-bi/{shared-policy,custom-annotations,model-composition,model-from-tmdl}.md`.
New reference: `reference/power-bi/{index,project-layout,tmdl,annotations,validations,requirements-and-compatibility}.md`, `reference/python/semantic-models.md`, CLI/behaviour Unbind.
Product owners remain plan section 5's canonical routes. All existing targeted pages stay on their existing URL; Fors integrates updates and cross-links after the contracts/fixtures exist.

## Gates still unresolved

- Matching public package release/version.
- Authorised disposable live acceptance including report rendering and DAX query rights.
- Independent acceptance and visual/link integration, after implementation.
- Merged upstream changes require a deliberate baseline audit, not silent incorporation.
