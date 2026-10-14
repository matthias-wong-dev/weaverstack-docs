# Reference and route-retention integration audit

## Verdict and evidence boundary

**Reference content retained; route migration is not yet an acceptance pass.** This is the approved batch-3 integration audit, not the independent final editorial/technical reviews. Starting docs worktree: `7c87f21e3be76bdabf375c405373869d55b3cb55`, branch `docs/item-first-route-audit`. Compared every original page against `routes.json`'s docs baseline, `1f5220f17e8f698ebafc6bf4bab8b297dc1797b0`.

The baseline contains **114 Markdown pages and 872 captured heading IDs**. None of those pages has disappeared. After the reference entrance edit, **110 originals are byte-identical** to that baseline. The four changed originals are Home, Getting started, Installation and the Reference entrance. All **61 original Reference pages** remain; the other 60 Reference pages, their contracts and their authored/generated examples are unchanged. All **22 retained substantive concept/deep-dive pages** remain byte-identical, including their prose, examples and headings, not merely their links.

There are **35 planned canonical item/estate pages; 24 are physically present**. The 11 missing files are the Estate sibling's task pages, not an unexplained omission. The new item tasks have not replaced the original bodies yet; their content transfer and the parent's forthcoming compatibility conversion must be evaluated separately. Keeping both bodies today is not proof that deleting the old tutorial tomorrow preserves it.

Only these repository surfaces are assigned here:

- `docs/reference/index.md`: added item-specific routes into existing contracts and contextual operation lookups; retained the complete thematic index and compatibility qualification.
- `tools/check_item_routes.py`: new read-only route/fragment/nav/search/inbound checker with built-in regression cases. No existing checker changed.
- This audit: retention evidence, precise mapping corrections and integration handoff.

No nav, original tutorial, contract, generated region, fixture, product file, parent worktree or runtime changed.

## Full-content retention, not just surviving paths

The complete per-page inventory is below. `Identical` means the entire original file was compared with `git show <docs baseline>:docs/<path>`, not inferred from a surviving heading or link. The route map remains the frozen source of original IDs.

| Content family | Substantial material inspected / transfer finding |
| --- | --- |
| Reference: documents and Python authoring | Tables, Folders, Views, validation forms, common metadata, inference/override, Shortcuts, schema metadata and Warehouse programmables retain complete authoring contracts. Public Python operations, session helpers, reports/results and exceptions retain their full generated inventories and authored qualifications. |
| Reference: CLI and operation behaviour | All command leaves and exact Build/Load/Test/Health/Mirror/Wipe/Unbind/Session/Workflow boundaries remain intact. Selection, stale/as-of, destructive reload, partial effects, concurrency, previews/bundles/install and machine output are not compressed into item tutorials. |
| Reference: native models/Reports | Discovery, native payload completeness, same-name/byPath association, unrelated byConnection, typed source mapping, existing connections, TMDL precedence, all built-ins, extension phases, DAX metadata/comparison and source-versus-installed recording remain intact. |
| Retained concepts/deep mechanisms | All 22 substantive `core-concepts/` and retained `advanced/` pages remain unchanged. These include catalogue table interpretation, ownership, dependency boundaries, failure policy, mirrored borrowing/materialisation, protected data, incremental selection/data processing, operational history, automation, bundles and portable execution. Keep these searchable at stable URLs; `not_in_nav` is not a reason to exclude them from search. |
| Lakehouse authoring | The new Python/Spark SQL/tests tasks keep Folder → Table, inferred Python import dependencies and explicitly declared Spark SQL dependencies. The new mutable-source variation preserves physical external ownership, snapshots/history, consumer bookmarks, changed/removed rows and data-only Load without Build. The old full incremental mechanism remains substantive. |
| Warehouse authoring | The new first task retains ordinary SELECT + metadata → generated load work → dependent View. Tests retain independent expected/actual relations, Assumption violations, failed versus invalid outcomes, diagnostic selection and source/file recording boundaries. The new mutable-source example retains keyed changes/bookmarks and makes its external-source fixture switch explicit. Full schemas/keys/protection explanations remain at their old deep URLs. |
| Native model + annotation | The new native task retains the model/Report pair, Import refresh/count, unchanged source, same-name overlay, many-side-only foreign-key hiding, false-as-no-op, and no security/export claim. Shared policy retains native formatting/calculation-group structure and local precedence. Custom annotations retain the complete Python handler, executable-code warning, scope/namespacing, located failure and phase authority. Composition retains explicit outputs, no base deployment, owned validations, recursive bases/cycle/repeated-ancestor refusal. Standalone TMDL retains explicit named target and partitionless source generation. |
| Managed sources and DAX | The new managed task preserves explicit destination/source distinctions, unchanged authored partitions/navigation, source-first separate Builds, Import rather than invented Direct Lake, existing connection binding and access requirements. Validation retains source/file and installed modes, `--source` not forcing file mode, repeatable file/name selectors, no source-mode TestStatus/Log, failed/invalid/planned distinctions, independent source SQL and recorded installed findings. It improves the inline failure exercise by restoring the reader's prior overlay rather than deleting their rule. |
| Reports | `reports/deploy.md` and `reports/environments.md` retain native `definition.pbir`, actual dataset/workspace readback, explicit model target, local association, same-name precedence via Reference, catalogue-free pair requirement, conditional certified Report-only Build, unrelated byConnection preservation, dev/prod unchanged-source bindings and no Report Load/Test/refresh. |
| Shared tutorials still awaiting integration | The original dependency/mapping/state/development/operations/recovery/selection/concurrency/performance/workflow bodies are still intact. Their new Estate owners cannot yet be assessed. Do not convert them to pointers before checking complete transfer, including the original tested selection graph, recovery/destructive boundaries and concurrency defaults. |

**Specific content risks before pointer conversion:**

1. `basics/shortcuts.md` originally gives a complete two-item logical-Shortcut setup, producer declaration, Warehouse View mapping, both-item Build, producer Load and consumer query. `lakehouse/shortcuts.md` intentionally presents a short extension against an *existing* Dispatch Warehouse. The complete setup/order demonstration must survive in `estate/connected-items.md` or another substantive owner, not disappear behind a root link.
2. `getting-started/first-project.md` originally continues its first Warehouse result through a Test, Health and a Python workflow. The new Warehouse first task deliberately stops before validation; `warehouse/tests.md` carries the Test and Health, and Estate automation must carry the workflow. Preserve these separate fragment intents instead of mapping all nine old steps to the first SQL page.
3. `basics/workspace-and-python-runtime.md` combines installed-binding semantics, configuration switching, optional Mirror, Report targets and hosted runtime publication. The new Report and runtime pages retain their portions. Estate must still retain the important fact that changing `targets` alone does not retarget installed Load/Test/Health until Build.
4. The old model/Report monolith has distinct native, annotation, custom-extension and managed-source sections. Their bodies survive across the new tasks; its current seven fragment overrides do not describe all those intentions. Generic fallback to the native model entrance misroutes several old fragments despite a valid URL.

## Mapping corrections for the parent

These are suggestions to the parent-owned `routes.json` and compatibility generation, not edits made here. All destinations below are actual current headings unless explicitly marked as an Estate owner pending integration.

### Split originals: add explicit fragment overrides

| Original path and fragment | Direct final destination |
| --- | --- |
| `basics/power-bi/deploy-pbip.md#before-the-source-backed-example` | `semantic-models/managed-sources.md#before-you-start` |
| Same path `#1-configure-destination-and-source-separately` | `semantic-models/managed-sources.md#1-configure-destination-and-source-separately` |
| Same path `#2-build-and-load-the-warehouse-first` | `semantic-models/managed-sources.md#2-build-and-load-the-warehouse-first` |
| Same path `#3-deploy-the-model-and-report` | `semantic-models/managed-sources.md#3-bind-and-refresh-the-model` |
| Same path `#3-deploy-the-model-and-linked-report` | `reports/deploy.md#choose-the-destination-and-build` |
| Same path `#4-refresh-and-view-the-result` | `reports/deploy.md#inspect-the-report` |
| Same path `#use-your-own-convention` | `semantic-models/custom-annotations.md` |
| Same path `#cleanup` | `reports/environments.md#remove-only-the-example-items` (native pair, not managed-source cleanup) |
| `basics/tests-and-assumptions.md#before-you-start` | `semantic-models/validation.md#start-from-the-model-you-already-deployed` |
| Same path `#1-deploy-and-refresh` | `semantic-models/validation.md#start-from-the-model-you-already-deployed` |
| Same path `#2-run-the-source-assumption` | `semantic-models/validation.md#2-run-the-authored-query` |
| Same path `#3-produce-a-finding` | `semantic-models/validation.md#3-produce-a-finding-without-losing-your-overlay` |
| Same path `#4-correct-it` | `semantic-models/validation.md#4-restore-the-prior-model-and-rerun` |
| Same path `#produce-and-correct-a-discrepancy` | `semantic-models/validation.md#produce-and-correct-a-discrepancy` |
| Same path `#read-the-estate-result` | `estate/operate.md` (pending) |
| Same path `#choose-the-validation-form` | `reference/operation-behaviour/test.md#validation-semantics` for the cross-item form comparison |
| `basics/workspace-and-python-runtime.md#1-map-the-two-destinations` | `reports/environments.md#select-the-two-destinations` |
| Same path `#2-deploy-and-refresh-each-pair` | `reports/environments.md#build-and-check-each-binding` |
| Same path `#cleanup` | `reports/environments.md#remove-only-the-example-items` |
| Same path `#add-a-fabric-environment-for-python-work` | `lakehouse/runtime.md#bind-the-runtime-you-will-use` |
| Same path `#publish-the-runtime` | `lakehouse/runtime.md#publish-the-matching-packages` |
| `basics/power-bi/modelling-rule.md#hide-relationship-foreign-keys` | `semantic-models/native-tmdl.md#hide-relationship-foreign-keys` (add this despite the page move already being present) |
| `basics/shortcuts.md#connect-managed-items-with-a-logical-shortcut`, its prerequisites and numbered steps 1–6 | `estate/connected-items.md` and its equivalent headings once integrated; the physical Shortcut section stays with Lakehouse |
| `getting-started/first-project.md#3-add-a-test`, `#7-run-the-test` | `warehouse/tests.md` and its relevant heading, not Warehouse first-project |
| Same path `#8-read-health` | `estate/catalogue-and-health.md` or the retained Warehouse tests outcome (pending final intent/heading choice) |
| Same path `#9-run-the-lifecycle-as-a-workflow` | `estate/automation-and-deployment.md` (pending) |
| `advanced/index.md#semantic-models` | `semantic-models/index.md`, not the default Estate entrance |
| `basics/index.md#author-the-items` | A compatibility section exposing all four item entrances, not a generic first-item link |

Retain the existing correct overrides for `#use-a-managed-source`, both foreign-key annotation anchors, `#semantic-model-validations`, `#compare-dax-with-source-sql`, `#warehouse-validations` and `#model-and-report-targets`. For other moved headings, link to the equivalent final heading when it survives; fallback to the owning task only when there is no narrower relevant section.

### Existing pointers and lost entrance anchors

Five original `basics/power-bi/` files are already search-excluded pointers: `environments.md`, `fabric-integration.md`, `modelling-rule.md`, `validate.md` and `index.md`. Their links still go through the old runtime/tests/PBIP/Basics/Advanced pages. Rewrite **every** contextual link in these files directly to its final task/reference; changing only their primary destination leaves chains. Keep all five captured original IDs.

Five captured IDs are currently missing in both source rendering and actual HTML:

- `getting-started/index.md#getting-started`;
- `index.md#weaver-documentation`, `#build-your-first-project`, `#add-work-to-the-project`, `#operate-the-estate`.

Preserve these entrance IDs at useful corresponding content, without locking new paragraph/headline order. `getting-started/first-project.md` is listed as a retired route but remains in nav; either make the optional starter a live retained owner in the map, or make navigation/contextual entry links go to the canonical Warehouse first task and keep the pointer out of nav. Do not silently waive the inconsistent treatment in the gate.

### Product-site links by reader intent

Read-only scan: `/opt/data/scratch/Fors/weaver-docs-refresh/product/docs`. Preserve quiet root `Developer docs` links. Change task links specifically:

| Product page / visible link | Canonical developer destination |
| --- | --- |
| Home: Get started with Fabric / Build your first Fabric project | `/warehouse/first-project/` |
| Home: Develop a project; Warehouse: Make a change | `/estate/development-cycle/` |
| Get started: first project; Lakehouse; Warehouse | `/warehouse/first-project/`, `/lakehouse/python/`, `/warehouse/first-project/` respectively |
| Get started: Deploy models and Reports / existing PBIP | `/semantic-models/native-tmdl/` (paired setup); use `/reports/deploy/` when its label specifically promises Report deployment |
| How it works and Lakehouse: Run and inspect the estate | `/estate/operate/` |
| Lakehouse: Write an incremental load | `/lakehouse/incremental/`, not the retained full multi-item incremental mechanism |
| Lakehouse / Warehouse: Use Mirror in development | `/estate/mirror/`; retain the deep materialisation page for mechanism-specific links |
| Reports: Choose environment targets | `/reports/environments/` |
| Reports: Deploy models and Reports | `/reports/deploy/` (the page's reader is the Report maintainer) |
| Reports: Report deployment reference | `/reference/power-bi/requirements-and-compatibility/#report-binding` |
| Semantic models: Deploy a model and Report / existing PBIP | `/semantic-models/native-tmdl/` |
| Semantic models / Warehouse: Connect model to source | `/semantic-models/managed-sources/` |
| Semantic models: Apply a modelling rule | `/semantic-models/native-tmdl/#hide-relationship-foreign-keys` |
| Semantic models: Share standards / Validate / Compose | `/semantic-models/shared-policy/`, `/semantic-models/validation/`, `/semantic-models/composition/` |
| Scale: Investigate a slow run | `/estate/performance/` |

The gate detects 21 distinct incoming links to mapped retired routes today. It cannot infer that a still-live deep page is the wrong practical destination: the Lakehouse incremental/Mirror and Report reference-fragment refinements above require this intent review, not merely a crawl.

## Source, platform and exact interface checks

### Same frozen implementation

Product worktree HEAD is `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`, but its behaviour/tests match the approved pin `74b4d15ee65ed2740593af1f4d459771b801b132`:

| Tree | Pinned and worktree HEAD Git tree ID |
| --- | --- |
| `src/weaver` | `53c343e9d8b21a59137830e6885631543b4caa3d` |
| `tests` | `2ba0ad5a48ef7e1c6a3bfa859213610db14ace08` |

The installed Python environment is `/opt/data/repos/weaverstack/.venv/bin/python`. **Use `PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src:/opt/data/scratch/Fors/weaver-docs-refresh/product/tests`** for direct imports/tests. A diagnostic using the checkout root instead of `/src` initially imported `/opt/data/repos/weaverstack/src/weaver`; corrected imports were verified at the frozen product checkout before direct tests. The maintained docs checkers independently print/verify their chosen checkout path.

### Permissions and definitions

- `src/weaver/fabric/semantic_model.py` uses Fabric `updateDefinition`, explicit TMSL `getDefinition` readback, Power BI model refresh and Execute Queries; `fabric/report.py` uses native Report definition APIs plus Power BI Report binding readback. `tests/test_semantic_model_auth_boundary.py` checks the separate Fabric and Power BI token audiences on the same injected credential. Deployment/readback, refresh, querying and source access are distinct capabilities, as the new tasks state.
- Microsoft specifies Contributor for model/Report creation; their delegated scopes are respectively `SemanticModel.ReadWrite.All` or `Item.ReadWrite.All`, and `Report.ReadWrite.All` or `Item.ReadWrite.All`.[1][2]
- Model/Report Get Definition requires item **read and write**, not ordinary viewer/read-only access, and the corresponding ReadWrite scopes; encrypted sensitivity labels can block those endpoints.[4][5] Keep this qualification beside native-definition inspection or in the existing requirements owner; do not imply any Report viewer can perform definition readback.
- Execute Queries requires dataset Read and Build, the tenant's Dataset Execute Queries REST API setting and `Dataset.Read.All` or `Dataset.ReadWrite.All`. Microsoft separately restricts service-principal querying for RLS/SSO datasets.[3] `semantic-models/validation.md` correctly distinguishes those rights from source SELECT and deployment permissions. No tenant setting, credential or connection was changed or tested live.
- Source nuance worth preserving during review: `build_bundle/executors/semantic.py:44–68` makes invalid-measure querying best-effort when `FabricError` prevents it: `measure_check` is `not run: ...`, not a failed deployment. Detected invalid measures fail installation. Do not strengthen the unchanged Reference phrase about invalid-measure checks into a universal guarantee that Build successfully queried every model. Native definition/readback certification and live DAX correctness remain separate.
- Native discovery's `.SemanticModel` TMDL/`definition.pbism`, complete PBIR or PBIR-Legacy payload, unchanged authored source and deployment-binding boundaries remain documented at the original exact Reference owners. Microsoft API support for other definition forms does not expand Weaver's authored-discovery contract.

### Behaviour exercised offline

**189 selected product tests passed in 86.46 seconds**, using the verified frozen import. Exact files:

```text
tests/targeted/test_load_recursive_selection_cycle.py
tests/test_cli_load_representation.py
tests/test_semantic_model_catalogue_free_cycle.py
tests/test_semantic_model_binding_boundary.py
tests/test_semantic_model_readback_cycle.py
tests/test_semantic_model_auth_boundary.py
tests/test_semantic_validation_run_cycle.py
tests/test_semantic_source_build_cycle.py
tests/test_semantic_source_preservation_cycle.py
```

Implementation cross-checks: `selection.py` compiles with `re.IGNORECASE` and uses `fullmatch`; `load_plan.py:342–376` differentiates area-qualified and unambiguous bare Lakehouse loadables. The recursive-selection test checks original-seed union, excluded sibling/other parent, repeated regex seeds, plain-name unordered override, item boundaries, dry-run non-dispatch/recording, barriers and catalogue-free refusals. Native binding/catalogue-free/readback tests exercise explicit destinations, paired selection and source/model separation with offline service boundaries. Validation tests exercise source/installed ownership and outcomes. These are not tenant/service acceptance results.

| Maintained docs check | Actual result |
| --- | --- |
| `generate_cli_reference.py --check --weaver-checkout <frozen checkout>` | 18 leaf commands across 16 pages |
| `generate_python_reference.py --check ...` | 55 public exports across 7 pages |
| `generate_semantic_reference.py --check ...` | 4 supported extension classes |
| `generate_catalogue_reference.py --check ...` | 23 catalogue table declarations |
| `check_reference_examples.py --weaver-checkout ...` | 103 commands, 6 configurations, 4 operation calls, 2 DAX files, 1 native edit |
| `check_docs_refresh_examples.py --weaver-checkout ...` | 6 real CLI Check fixtures, 53 README commands parsed; real LoadDag sets/area ambiguity and Runner invocation/resource caps; authored SHA-256 unchanged; source Assumption/DAX-SQL passed→failed→invalid→passed boundary checks |
| `check_journey_examples.py --weaver-checkout ...` | 15 original journey pages, 92 commands, 9 configs, 3 Python calls; 12 exact fixture blocks and 4 exact rendered projects Check/compile |

The last checker still targets the original journey pages. Its pass does not independently validate all new item-page snippets; use the item workers' evidence/checkers and final integrated gates for that coverage.

## Generated ownership unchanged

All four `generated/{cli,python,semantic,catalogue}-reference.json` inventories and their existing generator ownership stay unchanged. All **25 generated blocks across 25 original Reference pages** were compared byte-for-byte with the docs baseline. Aggregate fingerprint of sorted per-page generated-block hashes: `f1749ad7f0c91edd4af67e10e5bc07d3a35d8aa67812eefd770c8642a0d99b85` (SHA-256 over JSON records with path, block count and per-page block SHA-256).

A contextual Markdown-link scan found **no moved-route links inside generated regions**. There are retired narrative links in authored prose around them, including `reference/cli/{build,load,test,fabric-notebook}.md` and `reference/python/{session,objects,validation,results,errors}.md`. Parent may rewrite those authored links with reader intent. If a future generator check exposes a generated link, change its generator/ownership source and regenerate on this same freeze; do not patch the region by hand.

## Route-gate execution and remaining integration

Run in the reused locked docs environment:

```bash
/opt/data/scratch/Fors/weaver-docs-refresh/journeys/.venv/bin/python tools/check_item_routes.py --self-test
/opt/data/scratch/Fors/weaver-docs-refresh/journeys/.venv/bin/python tools/check_item_routes.py
/opt/data/scratch/Fors/weaver-docs-refresh/journeys/.venv/bin/python tools/check_item_routes.py \
  --developer-site /path/to/built/docs \
  --product-site /opt/data/scratch/Fors/weaver-docs-refresh/product/docs
```

The gate checks original paths/IDs, all canonical files and nav membership, accepted item order, search exclusion/visibility, direct per-ID destinations, pointer chains, narrative/product inbound canonicality and Markdown-versus-HTML URL resolution. It never asserts paragraph/headline order. Same-page permalink links are not falsely treated as pointer chains. `--self-test` passes **12 regression cases**, including a real rendered cross-site footer link after an article; earlier RED runs exposed missing checks and the footer/self-link bugs before correction.

**Current source gate: exit 1**, 114 originals, 872 original IDs, 24/35 canonical files, 27 compatibility routes. Rendered mode on the partial build also exits 1. This is expected before sibling/parent integration, not a waived pass:

- 11 Estate task files are absent;
- the five entrance IDs above are missing;
- 22 moved tutorial bodies have not been converted/search-excluded yet; 5 existing pointers still use old routes;
- 32 distinct live narrative links and 21 product links land on mapped retired routes;
- one retired route is still in nav;
- current unconverted bodies generate wrong-per-fragment destination findings; resolve the explicit split corrections before evaluating the finished pointers.

Strict MkDocs build into the profile scratch directory **aborted with 36 warnings**, all for those absent Estate nav/link targets. It produced partial HTML sufficient to exercise actual URL/ID/search checks, not an acceptable finished build. The modified Reference entrance introduced no broken links or fragments. Local full output is in profile scratch `item-first-route-audit-{source,rendered}.json`; the committed report does not depend on those temporary files for its original inventory or findings.

After Estate integration and parent route/product rewrites: rerun strict build, the route gate with both sites, existing paired-site asset/link crawl, all four generator checks and the complete approved technical/editorial acceptance. The route checker is not full-content, visual, live Fabric, licensing, model query, Report rendering or reader-flow acceptance.

## Complete original-page inventory

The following inventory is derived from all entries in `routes.json`, checked against the baseline's complete `docs/**/*.md` tree (both contain 114 pages). Planned move owners are not assertions that the transfer is complete. All 27 original move/split files remain unchanged at this checkpoint; the 11 absent Estate tasks prevent a finished migration verdict.

| Original page | Content versus baseline | Canonical treatment / owner |
| --- | --- | --- |
| `advanced/automation-and-execution-contexts.md` | Identical | Retain substantive owner at same URL |
| `advanced/build-bundles-and-controlled-installation.md` | Identical | Retain substantive owner at same URL |
| `advanced/concurrency.md` | Identical | Move/split: `estate/concurrency.md` (absent) |
| `advanced/incremental-build-selection.md` | Identical | Retain substantive owner at same URL |
| `advanced/incremental-data-processing.md` | Identical | Retain substantive owner at same URL |
| `advanced/index.md` | Identical | Move/split: `estate/index.md` |
| `advanced/mirror-and-materialisation-strategies.md` | Identical | Retain substantive owner at same URL |
| `advanced/partial-failures-rejected-data-and-thresholds.md` | Identical | Retain substantive owner at same URL |
| `advanced/performance-and-scale.md` | Identical | Move/split: `estate/performance.md` (absent) |
| `advanced/portable-execution-between-desktop-and-fabric.md` | Identical | Retain substantive owner at same URL |
| `advanced/power-bi/custom-annotations.md` | Identical | Move/split: `semantic-models/custom-annotations.md` |
| `advanced/power-bi/model-composition.md` | Identical | Move/split: `semantic-models/composition.md` |
| `advanced/power-bi/model-from-tmdl.md` | Identical | Move/split: `semantic-models/from-tmdl.md` |
| `advanced/power-bi/shared-policy.md` | Identical | Move/split: `semantic-models/shared-policy.md` |
| `advanced/protecting-data.md` | Identical | Retain substantive owner at same URL |
| `advanced/row-auditing-and-operational-history.md` | Identical | Retain substantive owner at same URL |
| `advanced/run-part-of-an-estate.md` | Identical | Move/split: `estate/selective-runs.md` (absent) |
| `advanced/schemas-keys-and-managed-columns.md` | Identical | Retain substantive owner at same URL |
| `basics/development-cycle.md` | Identical | Move/split: `estate/development-cycle.md` (absent) |
| `basics/index.md` | Identical | Move/split: `index.md` |
| `basics/lakehouse-python.md` | Identical | Move/split: `lakehouse/python.md` |
| `basics/lakehouse-spark-sql.md` | Identical | Move/split: `lakehouse/spark-sql.md` |
| `basics/power-bi/deploy-pbip.md` | Identical | Move/split: `semantic-models/native-tmdl.md`, `semantic-models/managed-sources.md`, `reports/deploy.md` |
| `basics/power-bi/environments.md` | Identical | Move/split: `reports/environments.md` |
| `basics/power-bi/fabric-integration.md` | Identical | Move/split: `semantic-models/managed-sources.md` |
| `basics/power-bi/index.md` | Identical | Move/split: `semantic-models/index.md` |
| `basics/power-bi/modelling-rule.md` | Identical | Move/split: `semantic-models/native-tmdl.md` |
| `basics/power-bi/validate.md` | Identical | Move/split: `semantic-models/validation.md` |
| `basics/recover-failed-work.md` | Identical | Move/split: `estate/recovery.md` (absent) |
| `basics/run-and-inspect-estate.md` | Identical | Move/split: `estate/operate.md` (absent) |
| `basics/sessions-and-workflows.md` | Identical | Move/split: `estate/automation-and-deployment.md` (absent) |
| `basics/shortcuts.md` | Identical | Move/split: `lakehouse/shortcuts.md` |
| `basics/tests-and-assumptions.md` | Identical | Move/split: `lakehouse/tests.md`, `warehouse/tests.md`, `semantic-models/validation.md` |
| `basics/troubleshooting.md` | Identical | Retain substantive owner at same URL |
| `basics/warehouse-pipeline.md` | Identical | Move/split: `warehouse/first-project.md` |
| `basics/workspace-and-python-runtime.md` | Identical | Move/split: `estate/environments.md` (absent), `lakehouse/runtime.md`, `reports/environments.md` |
| `core-concepts/build-load-and-test.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/catalogue.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/dependencies.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/design-philosophy.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/fault-tolerance.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/how-weaver-works.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/index.md` | Identical | Move/split: `estate/index.md` |
| `core-concepts/logical-and-physical-items.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/mirrors.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/projects-and-estates.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/sessions-and-workflows.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/state-and-health.md` | Identical | Retain substantive owner at same URL |
| `core-concepts/weaver-documents.md` | Identical | Retain substantive owner at same URL |
| `getting-started/first-project.md` | Identical | Move/split: `warehouse/first-project.md` |
| `getting-started/index.md` | Edited entrance/setup (not a contract) | Retain substantive owner at same URL |
| `getting-started/installation.md` | Edited entrance/setup (not a contract) | Retain substantive owner at same URL |
| `index.md` | Edited entrance/setup (not a contract) | Retain substantive owner at same URL |
| `reference/build-bundle-format.md` | Identical | Retain substantive owner at same URL |
| `reference/catalogue-schema.md` | Identical | Retain substantive owner at same URL |
| `reference/cli.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/build.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/check.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/doctor.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/fabric-capacity.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/fabric-environment.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/fabric-notebook.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/health.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/initialise.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/install.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/load.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/mirror.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/session.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/test.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/unbind.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/wipe.md` | Identical | Retain substantive owner at same URL |
| `reference/cli/workflow.md` | Identical | Retain substantive owner at same URL |
| `reference/configuration-files/fabric-environment.md` | Identical | Retain substantive owner at same URL |
| `reference/configuration-files/index.md` | Identical | Retain substantive owner at same URL |
| `reference/configuration-files/workflow.md` | Identical | Retain substantive owner at same URL |
| `reference/configuration-files/workspace-config.md` | Identical | Retain substantive owner at same URL |
| `reference/index.md` | Edited entrance/setup (not a contract) | Retain substantive owner at same URL |
| `reference/machine-readable-output.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/build.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/fault-and-outcome-vocabulary.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/health.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/index.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/load.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/mirror.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/session-runtime.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/shared-selection-and-identity.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/test.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/unbind.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/wipe.md` | Identical | Retain substantive owner at same URL |
| `reference/operation-behaviour/workflow.md` | Identical | Retain substantive owner at same URL |
| `reference/power-bi/annotations.md` | Identical | Retain substantive owner at same URL |
| `reference/power-bi/index.md` | Identical | Retain substantive owner at same URL |
| `reference/power-bi/project-layout.md` | Identical | Retain substantive owner at same URL |
| `reference/power-bi/requirements-and-compatibility.md` | Identical | Retain substantive owner at same URL |
| `reference/power-bi/tmdl.md` | Identical | Retain substantive owner at same URL |
| `reference/power-bi/validations.md` | Identical | Retain substantive owner at same URL |
| `reference/python/errors.md` | Identical | Retain substantive owner at same URL |
| `reference/python/index.md` | Identical | Retain substantive owner at same URL |
| `reference/python/objects.md` | Identical | Retain substantive owner at same URL |
| `reference/python/operations.md` | Identical | Retain substantive owner at same URL |
| `reference/python/results.md` | Identical | Retain substantive owner at same URL |
| `reference/python/semantic-models.md` | Identical | Retain substantive owner at same URL |
| `reference/python/session.md` | Identical | Retain substantive owner at same URL |
| `reference/python/validation.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/assumption.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/common-metadata.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/folder.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/overview.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/schema-metadata.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/shortcut.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/table.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/test.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/view.md` | Identical | Retain substantive owner at same URL |
| `reference/weaver-documents/warehouse-programmable.md` | Identical | Retain substantive owner at same URL |

## Sources

[1] https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model — Create Semantic Model
[2] https://learn.microsoft.com/en-us/rest/api/fabric/report/items/create-report — Create Report
[3] https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries — Execute Queries
[4] https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/get-semantic-model-definition — Get Semantic Model Definition
[5] https://learn.microsoft.com/en-us/rest/api/fabric/report/items/get-report-definition — Get Report Definition
