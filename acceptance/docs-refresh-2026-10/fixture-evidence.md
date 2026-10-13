# A2 fixture evidence

## Baseline and scope

- Docs base: `f35c943ed0ca423b92ab53aa571c43ae2817b74e`; branch `docs/progressive-journeys-refresh`.
- Runtime source: `74b4d15ee65ed2740593af1f4d459771b801b132`. The product-site worktree advanced during verification to `84add848269c39ff5fd72a9ab8e385e47c2eeedb`; `git diff 74b4d15ee65ed2740593af1f4d459771b801b132 HEAD -- src tests pyproject.toml` is empty. The checker verifies both committed and working runtime differences before importing the checkout's `src/weaver`, and prints the actual HEAD. It does not pretend the documentation-only HEAD is the runtime baseline.
- Created only the six assigned fixture directories, `tools/check_docs_refresh_examples.py`, and this evidence file. Public pages, navigation, generators, existing examples and runtime were not edited by this fixture author.
- Publication remains held for the corresponding package. No new release number was assigned. PyPI `0.9.0` is not the target for these main-branch interfaces.
- No live Fabric/Power BI operation, paid capacity change, Environment publication, credential binding, Wipe, push or publication was performed.

## Evidence labels

**Locally checked** means the real pinned parser, compiler, CLI parser, report encoder, Load planner or Runner executed here. TestSession/InventoryClient and primitive/query answers are explicit offline test boundaries. They do not evaluate DAX/M/T-SQL or certify Microsoft service acceptance. The optional PBIR schema check fetched public Microsoft schemas; it did not contact a tenant.

**Source-backed** means the named pinned implementation and its focused offline tests establish the claimed boundary. Persisted catalogue outcomes in those tests are recorded by doubles, not observed in a real catalogue.

**Remotely exercised:** none. All service gates below are **not run** by instruction, not silently accepted.

## Actual commands and results

From the journeys worktree, using the existing interpreter and no package installation:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/data/repos/weaverstack/.venv/bin/python tools/check_docs_refresh_examples.py --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit 0. Final output:

```text
Source runtime matches 74b4d15ee65ed2740593af1f4d459771b801b132; checkout HEAD 84add848269c39ff5fd72a9ab8e385e47c2eeedb
PASS: parcel-powerbi: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged
PASS: file Assumption boundary inputs -> passed, failed, invalid, passed
PASS: parcel-powerbi-validation: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged
PASS: parcel-powerbi-standards: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged
PASS: parcel-powerbi-variants: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged
PASS: fixture LoadDag exact sets, cross-item scope, original-seed union and regex refusals
PASS: real LoadDag Lakehouse bare-area ambiguity and both qualified identities
PASS: fixture real Runner total cap 2, per-Warehouse 4, observed peak 2
PASS: fixture real Runner total cap 2, per-Warehouse 1, observed peak 2
PASS: parcel-load-selection: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged
PASS: file DAX/SQL boundary inputs -> passed, failed, invalid, passed
PASS: parcel-powerbi-fabric: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged
PASS: 6 fixtures; 53 README Weaver commands parsed; no live service exercised
```

Each CLI Check is a separate real `weaver_cli.main.main()` invocation with `--json --non-interactive`, importing the pinned source through PYTHONPATH. No Check result is substituted with a test double. The command parser also accepted all 53 Weaver command lines in the six reader READMEs without executing their live actions.

The default checker blocks socket connections and imports only the checkout's runtime and small offline helpers. Temporary failure/area probes are removed on exit. It compares every fixture file's SHA-256 before and after local checks; this is local source-preservation evidence, **not** a before/after service-deployment hash check.

Separate public-schema verification:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/hermes/.venv/bin/python tools/check_docs_refresh_examples.py --check-pbir-schemas
```

Exit 0: `PASS: 36 PBIR JSON documents; 8 public Microsoft schemas fetched; no Fabric calls`.

This optional mode requires `jsonschema`. It was already present in the Hermes interpreter, not in the Weaver interpreter; no package or environment was installed. Default offline checks do not require it. It validates definition.pbir, report/version/page/pages metadata and the visible card definition against their declared Microsoft schemas, including referenced visual/query schemas. Embedded schemas' declared `$id` aliases are cached without rewriting their contents. Schema validity does not prove the Report renders or its data query succeeds.

Lint/format:

```bash
/opt/data/repos/weaverstack/.venv/bin/python -m ruff check tools/check_docs_refresh_examples.py examples/parcel-powerbi-standards/PowerBI/annotations/Parcel__DisplayFolder.py
/opt/data/repos/weaverstack/.venv/bin/python -m ruff format --check tools/check_docs_refresh_examples.py examples/parcel-powerbi-standards/PowerBI/annotations/Parcel__DisplayFolder.py
git diff --check
```

Ruff check passes; formatting was applied and checked before commit. Diff whitespace check passes. The editor's missing-import diagnostics reflect its separate interpreter; actual execution imports the pinned checkout and its offline helpers successfully.

### Focused source suite

From the product checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:tests/targeted /opt/data/repos/weaverstack/.venv/bin/python -m pytest -q -p no:cacheprovider tests/targeted/test_load_recursive_selection_cycle.py tests/targeted/test_invocation_concurrency_boundary.py tests/targeted/test_invocation_api_concurrency_boundary.py tests/test_cli_load_representation.py tests/test_semantic_validation_run_cycle.py tests/test_semantic_model_catalogue_free_cycle.py tests/test_report_build_cycle.py tests/test_semantic_composition_build_cycle.py tests/test_semantic_annotation_representation.py tests/test_semantic_custom_annotation_declaration.py tests/test_powerbi_separate_build_boundary.py tests/test_cli_test_representation.py tests/test_semantic_shared_sources_cycle.py
```

Exit 0: **311 passed in 57.87s**; Weaver summary `core 311`, no declared live resources. No `tests/fabric` test was run.

Earlier verification groups passed 268 tests in 45.89s and 43 tests in 13.40s. One attempted supplementary command named a nonexistent `test_semantic_shared_source_representation.py` and exited 4 with no tests run; discovery found `test_semantic_shared_sources_cycle.py`, which passed and is included in the final combined 311-test run. This failed discovery attempt is not counted as a passing run.

## What is proven locally

| Fixture | Local evidence | Service result still required |
| --- | --- | --- |
| parcel-powerbi | Full PBIP/Import model, relationship and six-file Report definition; both neutral configs parse; real encoder resolves linked Report to each environment's model through an offline inventory; non-binding Report parts and all authored bytes remain unchanged. | Create/update both model/Report target pairs, refresh, view card = 2, inspect native definitions and actual Report bindings; compare authored hashes before/after both service deployments. |
| parcel-powerbi-validation | Real source/file-mode `weaver.test` returns passed → failed → invalid → passed for explicit boundary input rows/errors. Failing overlay really compiles Delivery Count = -1. No catalogue workflow/history is created in source mode. | DAX Execute Queries, licence/permissions, deliberate measure finding and correction against deployed model, CLI outcomes with real query responses. |
| parcel-powerbi-standards | Effective native TMDL hides only Delivery[DepotId], retains the one-side/unrelated columns, applies native shared formatting and local override, retains Display calculation group/Current item, and sets native displayFolder through the trusted Annotation class. Unrelated partitions are preserved. Empty custom value refuses with located diagnostic. | Inspect deployed native visibility/format/group/folder and render `2 deliveries`; ensure service accepts the native calculation group. The compiler retains that group's native TMDL rather than proving its engine behavior locally. |
| parcel-powerbi-variants | Real item-selector/binding functions resolve exactly the four explicitly named output items in both configs; no base target exists. Broad PowerBI/Parcel expansion includes base and consequently refuses for missing base target. Effective Operations adds Delivery Rate; Executive excludes InternalCosts table; separate model-owned validations and correctly linked Reports; base source parts remain unchanged. | Deploy only the outputs, inspect effective native variants and both bindings, execute both independent validations, and verify no physical base was created. |
| parcel-load-selection | Catalogue projected by pinned production constructors from these native SQL files; real LoadDag checks exact seed/ancestors/descendants/both sets, whole-name/case-insensitive/repeated regexes, invalid/no-match refusals, item scope and cross-item shortcut. Tiny temporary area probe verifies bare Lakehouse ambiguity and Tables/Files qualifiers. Real Runner over this fixture's seven-node graph observes total peak 2 and respects per-Warehouse ceilings, with dependency edges completed before consumers start. | Build/preload in disposable Warehouses; inspect real partial-run outcomes, current omitted Depot, unchanged out-of-scope data/bookmarks and real capacity/resource behavior. |
| parcel-powerbi-fabric | Complete authored Import model with supported shared source expression, native partition navigation and Weaver.Source reference to the managed SQL table. Binding preserves authored partitions/columns and records logical dependency; no empty-table generation. Real source-mode validation comparator returns passed → failed → invalid → passed for explicit DAX/SQL boundary answers. | Build/load source first, model/Report second; resolve real endpoint and approved connection; refresh; inspect native model/Report and catalogue lineage, TestStatus/health; exercise actual SQL/DAX discrepancy and correction. |

Focused source tests additionally establish sibling/upstream exclusion (`test_both_directions_expand_original_seeds_separately`), plain-name unordered override, scope on shared targets, area-qualified selection, preview non-dispatch, reload boundaries, public source/catalogue-free refusals, resource/total concurrency intersection, model-before-Report ordering, failure readback, source-first/PowerBI-second refusal, independent variant selection, and supported source-expression substitution. The fixtures' own graph and compiler checks are not replacement implementations of those algorithms.

### Important corrections found during verification

- `Weaver.Exclude` supports table/column scope, not measure scope. Executive therefore excludes the small native **InternalCosts table**. No runtime change was made.
- Failed query execution is an **invalid validation node**; installed TestStatus uses `Error`. A violated Assumption/Test is `failed`. The CLI returns 1 for failed/invalid verdicts and 0 for a passing run; Python returns a report. The READMEs and validation manifests now distinguish these.
- Diagnostic rows are collected for named/file selections. The deliberate finding commands use an explicit `--name`, not a claim that an unfiltered test run always emits all rows.
- Health uses repeated `--item`, not positional item arguments. The fixture command parser caught and corrected that error.
- The published Report schema requires `themeCollection`; all six Reports now include it, and all 36 PBIR JSON files validate.
- Missing-base composition reports the model/project scope; custom-annotation value errors report the authored file/line. The checker asserts those actual forms separately.
- Per-Warehouse limit 1 can still permit total concurrency 2 across two Warehouses. The probe now checks each Warehouse's peak rather than wrongly treating the resource cap as a run-wide cap.

No unresolved local fixture failure remains. There is no claim that these offline checks satisfy live A7 acceptance.

## Hash snapshot and inventory

The following digests cover the complete fixture file maps after successful verification. Each digest is `sha256(json.dumps(relative_path_to_sha256, sort_keys=True).encode())`; per-file hashes are re-created by the checker for its before/after comparison. Files include README/config/manifest, not just TMDL. Re-run the checker and update this snapshot if fixture files change during integration.

| Fixture | Files | File-map SHA-256 |
| --- | ---: | --- |
| parcel-powerbi | 17 | `729d6cd68fb4ff422e4c8a82dce0b02b1f9f3a3ce3ce546b032aa1c71d700f50` |
| parcel-powerbi-validation | 19 | `706181a2c221427d96b878b1be3d2c579eaf43e7b1322c6a07006f48a65a1563` |
| parcel-powerbi-standards | 21 | `02c88d78912010813c68805e0c332955507e4787b35a68179395323466e4e786` |
| parcel-powerbi-variants | 36 | `03c40a9c4c93a1f176ac429dcc17993b45017d39ebb7fab2b16dba63ec02370e` |
| parcel-load-selection | 15 | `6172d3f16b19b0d079de37831e82cd08906a44f3179402418bbd9318209f6d42` |
| parcel-powerbi-fabric | 23 | `94e42e00c3bdd4eb412e04238c049564d69d0a5fbb6c8e74b09ef441aaaaebc8` |

131 fixture files plus the checker and this report: 133 assigned files. The Fabric README was corrected during independent review to name the actual `_.SemanticModelTable`/`_.Dependency` readback; its snapshot above is the corrected file map. Fixture commands, configurations and native definitions did not change. Exact fixture inventory follows.

### examples/parcel-powerbi

```text
PowerBI/Parcel/Parcel.Report/definition.pbir
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/Parcel.Report/definition/pages/pages.json
PowerBI/Parcel/Parcel.Report/definition/report.json
PowerBI/Parcel/Parcel.Report/definition/version.json
PowerBI/Parcel/Parcel.SemanticModel/definition.pbism
PowerBI/Parcel/Parcel.SemanticModel/definition/database.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/model.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Depot.tmdl
PowerBI/Parcel/Parcel.pbip
README.md
expected-results.json
workspace-dev.yml
workspace-prod.yml
```

### examples/parcel-powerbi-validation

```text
PowerBI/Parcel/Parcel.Report/definition.pbir
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/Parcel.Report/definition/pages/pages.json
PowerBI/Parcel/Parcel.Report/definition/report.json
PowerBI/Parcel/Parcel.Report/definition/version.json
PowerBI/Parcel/Parcel.SemanticModel/definition.pbism
PowerBI/Parcel/Parcel.SemanticModel/definition/database.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/model.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Depot.tmdl
PowerBI/Parcel/Parcel.pbip
PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax
README.md
expected-results.json
failure/Parcel.tmdl
workspace-dev.yml
workspace-prod.yml
```

### examples/parcel-powerbi-standards

```text
PowerBI/Parcel/Parcel.Report/definition.pbir
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/Parcel.Report/definition/pages/pages.json
PowerBI/Parcel/Parcel.Report/definition/report.json
PowerBI/Parcel/Parcel.Report/definition/version.json
PowerBI/Parcel/Parcel.SemanticModel/definition.pbism
PowerBI/Parcel/Parcel.SemanticModel/definition/database.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/model.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Depot.tmdl
PowerBI/Parcel/Parcel.pbip
PowerBI/Parcel/Parcel.tmdl
PowerBI/annotations/Parcel__DisplayFolder.py
PowerBI/policy.tmdl
README.md
expected-results.json
failure/Parcel.tmdl
workspace-dev.yml
workspace-prod.yml
```

### examples/parcel-powerbi-variants

```text
PowerBI/Parcel/ParcelBase.SemanticModel/definition.pbism
PowerBI/Parcel/ParcelBase.SemanticModel/definition/database.tmdl
PowerBI/Parcel/ParcelBase.SemanticModel/definition/model.tmdl
PowerBI/Parcel/ParcelBase.SemanticModel/definition/relationships.tmdl
PowerBI/Parcel/ParcelBase.SemanticModel/definition/tables/Delivery.tmdl
PowerBI/Parcel/ParcelBase.SemanticModel/definition/tables/Depot.tmdl
PowerBI/Parcel/ParcelBase.SemanticModel/definition/tables/InternalCosts.tmdl
PowerBI/Parcel/ParcelExecutive.Report/definition.pbir
PowerBI/Parcel/ParcelExecutive.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/ParcelExecutive.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/ParcelExecutive.Report/definition/pages/pages.json
PowerBI/Parcel/ParcelExecutive.Report/definition/report.json
PowerBI/Parcel/ParcelExecutive.Report/definition/version.json
PowerBI/Parcel/ParcelExecutive.SemanticModel/definition.pbism
PowerBI/Parcel/ParcelExecutive.SemanticModel/definition/database.tmdl
PowerBI/Parcel/ParcelExecutive.SemanticModel/definition/model.tmdl
PowerBI/Parcel/ParcelExecutive.pbip
PowerBI/Parcel/ParcelExecutive.tmdl
PowerBI/Parcel/ParcelOperations.Report/definition.pbir
PowerBI/Parcel/ParcelOperations.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/ParcelOperations.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/ParcelOperations.Report/definition/pages/pages.json
PowerBI/Parcel/ParcelOperations.Report/definition/report.json
PowerBI/Parcel/ParcelOperations.Report/definition/version.json
PowerBI/Parcel/ParcelOperations.SemanticModel/definition.pbism
PowerBI/Parcel/ParcelOperations.SemanticModel/definition/database.tmdl
PowerBI/Parcel/ParcelOperations.SemanticModel/definition/model.tmdl
PowerBI/Parcel/ParcelOperations.pbip
PowerBI/Parcel/ParcelOperations.tmdl
PowerBI/Parcel/assumptions/ParcelExecutive/Parcel.PositiveDeliveryCount.dax
PowerBI/Parcel/assumptions/ParcelOperations/Parcel.PositiveDeliveryCount.dax
README.md
expected-results.json
failure/ParcelExecutive.tmdl
workspace-dev.yml
workspace-prod.yml
```

### examples/parcel-load-selection

```text
README.md
Warehouse/Operations/Parcel.Daily.sql
Warehouse/Operations/Parcel.Events.sql
Warehouse/Operations/Parcel.RawEvents.sql
Warehouse/Operations/Parcel.Summary.sql
Warehouse/Operations/Reference.Depot.sql
Warehouse/Operations/Reference.Service.sql
Warehouse/Operations/schemas/Parcel.yml
Warehouse/Operations/schemas/Reference.yml
Warehouse/Reporting/Parcel.DashboardInput.sql
Warehouse/Reporting/schemas/Parcel.yml
Warehouse/Reporting/shortcuts.yml
expected-results.json
workspace-dev.yml
workspace-prod.yml
```

### examples/parcel-powerbi-fabric

```text
PowerBI/Parcel/Parcel.Report/definition.pbir
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/Parcel.Report/definition/pages/pages.json
PowerBI/Parcel/Parcel.Report/definition/report.json
PowerBI/Parcel/Parcel.Report/definition/version.json
PowerBI/Parcel/Parcel.SemanticModel/definition.pbism
PowerBI/Parcel/Parcel.SemanticModel/definition/database.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/expressions.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/model.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Depot.tmdl
PowerBI/Parcel/Parcel.pbip
PowerBI/Parcel/Parcel.tmdl
PowerBI/Parcel/tests/Parcel/Parcel.DeliveryReconciles.dax
README.md
Warehouse/Operations/Parcel.Delivery.sql
Warehouse/Operations/schemas/Parcel.yml
expected-results.json
failure/Parcel.tmdl
workspace-dev.yml
workspace-prod.yml
```

## Held gates and handoff

Before publication, obtain explicit authorisation for the named disposable workspaces. Execute the reader commands against the matching package, verify native service readback and licence/permissions, retain before/after authored hashes, record actual model refresh/Report rendering/validation/cross-item results, and clean up only fixture-created items. Source-to-service claims are currently source-backed or locally checked, never remotely exercised.

Parent integration owns strict site build, public page/nav/cross-link/prose integration, independent reader walkthroughs and publication alignment. Concurrent parent edits in the journeys worktree are not part of this fixture commit. No push or publication is authorised by this evidence.
