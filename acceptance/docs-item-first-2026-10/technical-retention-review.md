# Independent technical retention review

## Verdict

**Substantive capability and exact-example retention pass at `8a94013`; final fragment-intent acceptance has one P2 defect. No confirmed P0/P1 correctness or destructive-safety defect was found.** The physical-Shortcut explanation survives intact in its new task, but its old physical-Shortcut fragment sends the reader to the managed-item task instead. Correct that direct destination before calling the migration fully accepted.

This is the fourth/final approved batch's independent technical/full-content review, not live Fabric acceptance, publication approval or the independent reader/visual review. Only this report is changed and committed.

## Evidence and scope

- Reviewed docs: `/opt/data/scratch/Fors/weaver-docs-refresh/item-first-retention-review`, branch `docs/item-first-retention-review`, starting HEAD `8a94013`.
- **Original content** came from `git show 1f5220f17e8f698ebafc6bf4bab8b297dc1797b0:docs/<path>`. Current old-route stubs were inspected for routing only, never substituted for the original substantive bodies.
- Read the approved plan `/opt/data/profiles/editor/attachments/weaver-docs-item-first-reorganisation-agent-plan.md`, `routes.json`, `route-map.md`, docs AGENTS/PROSE/CONTRIBUTING and product PROSE before judging transfer.
- Product evidence: `/opt/data/scratch/Fors/weaver-docs-refresh/product`, HEAD `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`; behaviour pin `74b4d15ee65ed2740593af1f4d459771b801b132`. `git diff --quiet <pin> -- src tests pyproject.toml` returned 0. `src` tree IDs at both revisions: `cbedc7f13c5f15b12e42fc5927dcefc184dbbcb0`; `tests`: `2ba0ad5a48ef7e1c6a3bfa859213610db14ace08`.
- Reused `/opt/data/repos/weaverstack/.venv/bin/python`, with `PYTHONPATH=<product>/src:<product>/tests`. Verified imports resolved to `<product>/src/weaver/__init__.py`, not the environment's other editable checkout. No install was needed.
- Reused locked MkDocs environment `/opt/data/scratch/Fors/weaver-docs-refresh/journeys/.venv`. Fresh strict build: `/opt/data/profiles/editor/cache/scratch/item-first-retention-site`.
- Product `docs/` was read-only here. Its parent's uncommitted changes are eight HTML files, 28 inserted/deleted link lines. Product H1 remains exactly **Making Fabric easier to use**. No runtime, test, fixture, nav, root-guide, tool or product edit was made by this reviewer.

## Prioritized genuine defect

### P2 — external physical-Shortcut fragment routes to the managed-connection tutorial

**Evidence:** `docs/basics/shortcuts.md:46–48` links `#connect-external-data-with-a-physical-shortcut` to `../estate/connected-items.md`. The same wrong owner is explicitly recorded under `fragment_overrides` in `acceptance/docs-item-first-2026-10/routes.json`. Fresh built HTML at `basics/shortcuts/index.html` preserves the old ID and renders `../../estate/connected-items/` as its continuation.

The original section at `1f5220f:docs/basics/shortcuts.md` teaches `target_type="physical"`, external `ParcelSourceArchive`, local `Files/Parcel/StatusSource`, generated reader `path()` versus `spark_path()`, optional source workspace and the unmanaged-source/pruning boundary. Those facts now live in **`docs/lakehouse/shortcuts.md:9–64`**, particularly `#expose-an-external-carrier-archive`. The current Estate destination instead opens with managed Landing → Dispatch lineage and only gives the external boundary a short link-back paragraph at line 62.

**Consequence:** the old fragment resolves but does not directly reach its substantive owner. No capability body is lost and this is not a unsafe runtime command; it is a genuine reader-intent regression under the plan's direct-fragment acceptance rule. The route checker passes because the pointer agrees with the same mistaken mapping, not because it can infer physical-versus-logical intent (`tools/check_item_routes.py:207–237`).

**Bounded correction for the owner:** change that override and its compatibility continuation directly to `lakehouse/shortcuts.md#expose-an-external-carrier-archive`. Keep the original ID and search exclusion. Leave the logical managed-connection fragments with Estate. Rebuild and rerun the existing route/paired-site gates; inspect the actual destination as well as the passing gate. This report does not edit the parent-owned mapping or pointer.

## Complete retention accounting

The baseline has **114 Markdown pages**, not 115: the unfiltered Git tree also contains a non-Markdown file. Every original Markdown route still exists, with all **872 captured original heading IDs**. All **35 canonical item/estate owners** are present. **26 routes** are direct search-excluded compatibility pages; the optional `getting-started/first-project.md` is deliberately retained live, not classified as retired. The accepted entrance aliases are present.

Whole-file comparison against the original gives **65 byte-identical files, 18 with authored-link-only changes, 26 compatibility conversions, four revised entrances/setup pages and one live optional starter**. Link-only classification normalizes Markdown link destinations, not prose or fenced examples; actual link deltas were reviewed. This accounting does not treat a stub as preserved original prose.

All **61 Reference pages** remain. Of these, **51 are byte-identical, nine change authored links only, and the Reference entrance adds item routing without removing its thematic coverage**. All **25 generated blocks on 25 pages** and all four `generated/{cli,python,semantic,catalogue}-reference.json` inventories are byte-identical to `1f5220f`. Re-running their four generators against the frozen source also passed; rewritten authored links did not change generated bytes.

All **22 retained substantive concept/deep-dive pages** remain complete: 14 byte-identical and eight authored-link-only. The still-live Troubleshooting page is also link-only. These remain searchable/contextually linked rather than being demoted to compatibility pointers. Full original-page disposition and owner inventory appears below.

### Capability transfer, not just surviving URLs

All paths in this table are under `docs/`. The source hierarchy is task → retained mechanism → exact Reference, not an assertion that every old paragraph must appear verbatim in the shorter task.

| Original capability | Substantive owners and retention finding |
| --- | --- |
| Python Folder → Delta Table | `lakehouse/python.md`: complete staged CSV Folder and Python Table; inferred `Files.Parcel__Events` import edge, descriptive Lineage, first runtime publication, Build/Load/Health and source-edit loop retained. |
| Spark SQL authoring | `lakehouse/spark-sql.md`: adds CurrentStatus to that same Python pipeline instead of restarting with a second SQL seed. Explicit `Dependencies`, including empty-list form, result-query shape and hosted-runtime qualification survive; `reference/weaver-documents/table.md#spark-sql` still owns the complete SQL contract. The redundant first seeded Table example is not a lost capability. |
| Lakehouse validation | `lakehouse/tests.md`, Test/Assumption document and Python references: independent expected rows, violating rows, inference for SQL validations, installed versus file recording, named failure/restoration and complete Python interfaces retained. |
| Mutable files/bookmarks | `lakehouse/incremental.md` plus unchanged `advanced/incremental-data-processing.md`: explicit separate Tracking snapshot; external ownership; missing-source refusal before staging; complete snapshot insertion/update/deletion; consumer-specific `files_since`/`deleted_since`; explicit delete keys; clean no-op bookmark advance and data-only Load without Build. |
| Shortcuts and cross-item ordering | `lakehouse/shortcuts.md` carries full physical-source/readback/reader forms; `estate/connected-items.md` carries complete working Landing → Dispatch logical mapping, configuration addition, selected both-item Build, source Load and endpoint query. Logical versus physical ownership, unnamed-item boundary, readiness and explicit dependency override survive. P2 above affects retrieval, not these bodies. |
| Warehouse first Table/View | `warehouse/first-project.md`: original StatusEvent and CurrentStatus SQL unchanged; generated load machinery, inferred View dependency, explicit managed-target ownership, three events/two current statuses. No Spark publication is invented for T-SQL. |
| Warehouse validation | `warehouse/tests.md`: same installed event/View project; independent expected/actual relations, optional diagnostic key, event Assumption, failed versus invalid outcomes, complete deliberate finding/restoration and source/file-mode boundary. Original independent Status seed example is deduplicated, not required as a second setup. |
| Warehouse incremental/schema/protection | `warehouse/incremental.md`: unchanged complete external-source scripts, physical View Shortcut, two-result keyed consumer SQL, timestamp visibility/tombstone qualifications, data-only change/no-op/bookmark readback. `warehouse/schema-and-protection.md` links full retained schema/key/audit/protection mechanisms; managed keys are not sold as physical indexes or enforced foreign keys. |
| Native model plus built-in rule | `semantic-models/native-tmdl.md`: normal PBIP/TMDL before annotation, complete same-name AutoHideForeignKeys overlay, many-side-only visibility, unchanged partitions/relationship, false-as-no-op, no RLS/OLS or export claim. Catalogue-free manual configuration remains separate from Initialise. |
| Shared standards/custom Python | `semantic-models/shared-policy.md`: exact native formatting/calculation-group policy and local override, plus transfer of the foreign-key rule into shared policy. `custom-annotations.md`: complete trusted executable handler, namespace/scopes/located failure, native property edit, schema/post_schema authority and once-per-final-model application remain. |
| Composition/standalone TMDL | `semantic-models/composition.md`: exact four-output selection, base not deployed, owned validations not inherited, raw recursive local bases, cycles/repeated-ancestor refusal, audience variants and security qualification. `from-tmdl.md`: both complete named standalone forms, explicit target, partitionless source generation versus retained authored partitions, Import versus Direct Lake prerequisites. |
| Managed model source | `semantic-models/managed-sources.md`: Warehouse-backed Delivery deliberately replaces inline partition; Depot remains inline; separate source then model/Report Builds, native shared expression and exact navigation, typed mappings, explicit lineage, supported existing connection, no credential creation. |
| DAX source/installed modes | `semantic-models/validation.md`: complete Assumption and independent DAX/SQL Test; repeatable file/name selectors, `--source` not forcing file mode, no source/file TestStatus/history, installed recording, failed/invalid/exit distinctions, exact catalogue fields. Failure exercise preserves existing rule/custom overlay and handles no-overlay direct entry instead of deleting a continuing reader's convention. |
| Reports and dev/prod | `reports/deploy.md` and `reports/environments.md`: native complete payload/byPath, destination-specific model/workspace ID readback, unchanged authored association, conditional certified Report-only Build, same-name precedence and unrelated byConnection preservation via Reference. No Report Load/Test/refresh is invented. |
| Whole-estate mapping/state | `estate/environments.md` separates workspace/config/runtime/destination/source controls; installed Load/Test/Health use Build-recorded bindings, not new `targets` alone. `catalogue-and-health.md` keeps current state versus history, queryable real catalogue tables, registered model/DAX status, no independent Report refresh health and no extra work merely to inspect state. |
| Ordinary development/operation/recovery | `estate/development-cycle.md`, `operate.md`, `recovery.md`: Check → preview → Build → Load → Test → Health; model/source separate Builds; installed/source boundary; no rollback; selected expanded reload destruction; partial fault-tolerant state; stability versus null/unique rules; Wipe catalogue default, explicit unbind retention and physical-target semantics. |
| Mirror/materialisation | `estate/mirror.md` transfers the old complete same-workspace prerequisite/config/settled-plan example out of the normal opening loop. Destination reset, source untouched, optional baseline, mixed borrowed/local state, preserving protected materialisation/bookmarks, source retention, partial failure and source-bound omitted copied installations all survive with deep/reference owners. |
| Selectors and concurrency | `estate/selective-runs.md` retains the full tested RawEvents/Events/Daily/Summary/Depot graph and oracle, all eight original fences and original-seed union. `estate/concurrency.md` retains all five original fences, invocation-wide cap, resource defaults, per-Warehouse ceiling, shared Spark application and serial source-test default. Neither Spark capacity nor unnamed item scope is silently enlarged. |
| Performance/automation/bundles | `estate/performance.md` preserves fixed-workload critical-path/wait/overhead investigation, sessions/workflow timings, endpoints and the observed synthetic F64 context; not an SLA or distinct-source-record claim. `automation-and-deployment.md` retains Session → workflow → Fabric host → frozen destination bundle, complete commands, failure/finding continuation, credentials distinction and no rollback. Existing deep bundle/portable/context/history bodies are preserved. |
| Optional first project and general entrances | Old first-project Table/Test/Health/workflow capability now lives in the Warehouse and Estate tasks above. Its live optional starter retains direct Test/Health/workflow fragment intent. Installation keeps exact private-source preview, older published package distinction, editable checkout for `--dev`, appropriate authentication and runtime boundaries. Home/Getting started/Reference no longer impose the old taxonomy. |

## Source-backed safety cross-check

Source paths below are relative to the frozen product checkout; the cited tests were actually executed offline.

| Contract | Code and exercised evidence | Finding |
| --- | --- | --- |
| Whole-name case-insensitive regex/repeated seeds | `src/weaver/selection.py:15–57` compiles `re.IGNORECASE`, uses `fullmatch`, refuses every unmatched pattern and unions matches. `tests/targeted/test_load_recursive_selection_cycle.py`, CLI representation and the real fixture LoadDag checker pass. | Exact tutorial and Reference facts retained. |
| Original-seed union/hard item scope/plain-name override | `src/weaver/load_plan.py:240–290` scopes the graph to requested items before expansion; `src/weaver/graph.py:232–256` expands each original seed in each requested direction. Plain names bypass inferred ordering at `load_plan.py:247–257`. | Both-direction Events omits Depot/sibling prerequisites; Reporting requires explicit item selection. Source's “exact-name” comment does not override the regex implementation. |
| Reload/partial outcomes | Existing recursive/reload/stale/dry-run/failure/contract tests plus real fixture LoadDag; `reference/operation-behaviour/load.md` remains byte-identical. | Reached expanded Tables are emptied/reset, Folders refused, stale/reload incompatible and prior data not restored on failure. Warnings are at the new action, not only buried in Reference. |
| Invocation versus resource concurrency | Actual defaults in `src/weaver/workspaces.py:158–196`: Build Warehouse/Spark/OneLake/Shortcut `2/4/8/2`; run Spark/Warehouse `4/4`. Runner cap/resource-boundary and API tests pass. Fixture Runner observes peak 2 with per-Warehouse 4 and 1. | Tutorial defaults/cap intersect dependency/resource limits; they do not configure cluster/capacity. |
| Source/model separation and Report Build-only lifecycle | Hosted-session mixed-request refusal test, model binding/catalogue-free/source/readback tests, native/offline Report encoder. | Separate Build calls retained; paired catalogue-free linked Report selection, certified installed Report-only exception and actual model/workspace binding remain distinct. |
| DAX recording and catalogue names | Existing `test_semantic_validation_run_cycle.py`, source/build/preservation tests and generator schema check; `reference/catalogue-schema.md` is unchanged. | Readback prose keeps the exact four required names `_.SemanticModelTable`, `_.Dependency`, `_.SemanticModelTest`, `_.TestStatus`; the complete catalogue also retains separate `_.SemanticModelMeasure` and `_.SemanticModelRelationship` records. Source identity belongs in Dependency and null Source access can be valid for a retained partition. Source/file outcomes are not installed history. |
| Runtime admission | `tests/targeted/test_hosted_runtime_session_boundary.py` and `test_hosted_endpoint_runtime_boundary.py` pass; tests refuse mutation before hosted admission and skip it for planning/Warehouse-only mode. | Matching version/plan/writer/executor requirements precede Spark mutation; Check/preview is not hosted admission. Attached notebook and pure T-SQL/native model paths remain qualified. |
| Protected Build is not Wipe/Mirror retention | `test_incremental_build_install.py`, protected materialisation and rebuilt-runtime-state tests pass. Materialisation test explicitly excludes retained Bookmark reset (`test_protected_mirror_materialisation_cycle.py:71–88`). Existing Wipe/Mirror boundary tests also pass. | Existing protected replacement can be skipped while other work proceeds; new objects can install. Preserving CTAS/shallow clone/copy retains bookmarks but is not a deep backup or guard against reload/Wipe/re-mirror. |

### Measure-query denial is not automatically fatal Build

`src/weaver/build_bundle/executors/semantic.py:44–68` returns `measure_check = "not run: ..."` on `FabricError` from invalid-measure querying. It raises `InstallError` when invalid measures are actually returned. `src/weaver/operations/build.py:325–329` presents the skipped check as a warning. Executed tests `test_deployment_reports_whether_its_measures_were_checked`, `test_deployment_with_an_invalid_measure_fails_naming_it` and `test_build_says_what_it_bound_and_what_it_could_not_check` establish this distinction (`tests/test_semantic_model_binding_boundary.py:291–350`).

The unchanged Reference's “invalid-measure checks gate certification” must not be strengthened into a promise that every successful Build queried DAX, or that query denial always fails deployment. The new tasks already distinguish deployment/readback, model refresh, query/source access and actual Report rendering. This is a reviewed source nuance, **not a new fatal defect or evidence of observed service queries**.

## Fresh executed results

Every passing row below is this review's execution at the integrated worktree, not copied from the earlier worker counts.

| Gate | Actual result |
| --- | --- |
| Four generator `--check` runs | CLI: 18 leaves/16 pages; Python: 55 exports/7 pages; semantic: four extension classes; catalogue: 23 declarations; all exit 0. |
| Generator regression suite | `python -m unittest discover -s tools -p 'test_generate*reference.py'`: 16 tests, OK. |
| `check_reference_examples.py` | 103 commands, six configurations, four operation calls, two DAX files, one native edit; exit 0. |
| `check_docs_refresh_examples.py` | Six real local CLI Check fixtures, 53 README commands parsed; real LoadDag selections/area ambiguity, real Runner cap, file Assumption and DAX/SQL boundary-input passed → failed → invalid → passed; authored hashes unchanged; exit 0. |
| Updated `check_journey_examples.py` | **15 new journey owners, 81 commands**, nine configs, three Python calls; 12 byte-identical fixture blocks, four assembled Check projects, local policy/rule/standalone compilation; exit 0. The earlier 92-command old-page result is not reused. |
| `check_lakehouse_examples.py` | Seven checkpoints; 30 commands, six task pages, 11 Python blocks, 12 synchronized blocks, two configs, three generated modules; complete production declaration edges; exit 0. |
| `examples/parcel-warehouse-journey/check.py` | Five assembled Check checkpoints, 25 commands, two configurations, six authored SQL blocks, 14 SQL program blocks, 12 exact fixture matches; fixture hashes unchanged; exit 0. This parser does not execute native T-SQL. |
| `check_semantic_examples.py` | Seven pages; 48 commands, three configs, one Python block; 16 exact fixture blocks, 12 assembled Check checkpoints; effective visibility/partition/relationship/policy/custom-folder and prior-overlay branches pass, fixtures unchanged. |
| Extra exact restoration/compiler check | Scratch `item-first-retention-failure-check.py`: exact Assumption shell branches restore original bytes/existence after an intervening local exit 1 for rule/custom/absent states. Published empty custom annotation produces real local `_DeclarationError` at `PowerBI/Parcel/Parcel.tmdl:6`; restored prior overlay compiles with `Parcel metrics`. No DAX or service result is inferred from the local shell status. |
| `check_report_examples.py` | Eight parsed commands, four exact JSON/YAML occurrences, 17 fixture hashes unchanged; native payload and production encoder offline dev/prod binding pass; service readback explicitly not exercised. |
| Committed Estate authored reproducer | First Python fence in `estate-evidence.md`, changing only ROOT to this worktree: 12 pages, 75 bash/six Session/six workflow forms; five complete configs/two config fragments, one Shortcut, three Python calls, 15 catalogue identifiers, four actual Check projects, two synchronized configs; exit 0, network denied. |
| Focused frozen-source tests | 25 existing files: **706 passed in 120.70s**; six additional runtime/protection/catalogue files: **114 passed in 12.30s**. **820 tests in 31 distinct files**, `-m 'not fabric'`, explicit socket network refusal, verified frozen imports. File lists below. |
| `check_fabric_first_story.py` | Discovery, rounded scale, native comparison, shared lifecycle pass; four shared CLI leaves, 94 authored commands parsed; exit 0. |
| Fresh strict MkDocs build | Exit 0, 5.10s; no build warnings. Material printed its upstream MkDocs-2 notice, not a site validation failure. |
| `check_item_routes.py --self-test` | 12 regression cases, OK. |
| Fresh rendered route gate with product site | 114 originals, 872 IDs, 35/35 owners, 26 compatibility routes, 3,735 documentation links, errors `[]`. Mechanical pass does not waive the independently identified P2 intent defect. |
| `check_paired_sites.py` | 161 HTML pages, 24,385 local links/assets, 201 cross-site links, seven benchmark rows, zero broken links/fragments. |
| `git diff --check` | Exit 0 before report creation; report-only staged scope verified at commit. |

Harness corrections, not content defects: the semantic checker uses `WEAVER_CHECKOUT` environment plus optional positional docs root, not the other checkers' `--weaver-checkout` argument. An initial wrong invocation raised `KeyError`; the documented environment form above passed. Extracting the committed Estate reproducer needs an anchored closing fence because its Python contains literal triple backticks. An initial extraction failed to parse; anchored extraction passed without changing repository files. An early inventory-print command let shell backticks execute; the corrected quoted command produced the complete real inventory below. These failed harness attempts are not represented as successful runs.

## Bounded reproduction

From the reviewed docs worktree, use existing environments and read-only/local checks:

```bash
PRODUCT=/opt/data/scratch/Fors/weaver-docs-refresh/product
PYTHON=/opt/data/repos/weaverstack/.venv/bin/python
DOCSPY=/opt/data/scratch/Fors/weaver-docs-refresh/journeys/.venv/bin/python
export WEAVER_CHECKOUT="$PRODUCT"
export PYTHONPATH="$PRODUCT/src:$PRODUCT/tests"

"$PYTHON" -c 'import weaver; print(weaver.__file__)'
git -C "$PRODUCT" diff --quiet 74b4d15ee65ed2740593af1f4d459771b801b132 -- src tests pyproject.toml

for name in cli python semantic catalogue; do
  "$PYTHON" "tools/generate_${name}_reference.py" --check --weaver-checkout "$PRODUCT"
done
"$DOCSPY" -m unittest discover -s tools -p 'test_generate*reference.py'
for name in reference docs_refresh journey report; do
  "$PYTHON" "tools/check_${name}_examples.py" --weaver-checkout "$PRODUCT"
done
"$PYTHON" tools/check_semantic_examples.py
"$PYTHON" tools/check_lakehouse_examples.py --docs . --product "$PRODUCT"
"$PYTHON" examples/parcel-warehouse-journey/check.py --weaver-checkout "$PRODUCT"
"$PYTHON" tools/check_fabric_first_story.py --product-site "$PRODUCT/docs" --weaver-checkout "$PRODUCT"

"$DOCSPY" -m mkdocs build --strict --site-dir /opt/data/profiles/editor/cache/scratch/item-first-retention-site
"$DOCSPY" tools/check_item_routes.py --self-test
"$DOCSPY" tools/check_item_routes.py \
  --developer-site /opt/data/profiles/editor/cache/scratch/item-first-retention-site \
  --product-site "$PRODUCT/docs"
"$DOCSPY" tools/check_paired_sites.py \
  --developer-site /opt/data/profiles/editor/cache/scratch/item-first-retention-site \
  --product-site "$PRODUCT/docs"
```

For the Estate authored run, extract the first Python block of the existing `estate-evidence.md` with `re.findall(r'^```python\n(.*?)^```\s*$', text, re.M | re.S)[0]`, replace only its `item-first-estate` ROOT path with this worktree and execute with the same interpreter/import path. Its code already denies network. The extra restoration check is at `/opt/data/profiles/editor/cache/scratch/item-first-retention-failure-check.py`; this scratch path is supplementary, not a new maintained tool or remote evidence.

Focused product tests were run from PRODUCT using `pytest.main(['-q', '-m', 'not fabric', *paths])` after checking `weaver.__file__` belongs to `PRODUCT/src` and replacing `socket.socket.connect` and `socket.create_connection` with a function raising `AssertionError('Network forbidden')`. The first set is the 17 files in `estate-evidence.md:210–227`, plus:

```text
tests/test_cli_load_representation.py
tests/test_semantic_model_catalogue_free_cycle.py
tests/test_semantic_model_binding_boundary.py
tests/test_semantic_model_readback_cycle.py
tests/test_semantic_model_auth_boundary.py
tests/test_semantic_validation_run_cycle.py
tests/test_semantic_source_build_cycle.py
tests/test_semantic_source_preservation_cycle.py
```

The second set:

```text
tests/test_incremental_build_install.py
tests/targeted/test_protected_mirror_materialisation_cycle.py
tests/targeted/test_rebuilt_runtime_state_invariant.py
tests/targeted/test_hosted_runtime_session_boundary.py
tests/targeted/test_hosted_endpoint_runtime_boundary.py
tests/test_public_catalogue_schema_invariant.py
```

## Acceptance limits

No real Fabric provisioning, capacity/tenant change, credential/connection administration, service Build/Load/Test/Health, model refresh, live DAX/SQL, Report binding/readback/rendering, runtime publication/admission, Mirror/Wipe or benchmark rerun occurred. Production functions and existing tests used explicit offline boundary inputs; they are not invented observed service responses. The tutorial's expected rows, cards, Green states and remote outcomes remain **expected**, not this review's observations.

The private-source preview and matching published-package constraint remain visible; no release, effective-TMDL export, publication, GitHub/Asana operation, push or delegation is claimed. Search index visibility and link resolution were checked, not search ranking or desktop/mobile usability. Human reader-flow and visual acceptance belong to the companion review. The P2 fragment correction belongs to parent integration; safety/deep/reference/example retention does not excuse it.

## Full original-page inventory

Paths are relative to `docs/`. “Byte-identical” compares complete original/current contents. “Authored links only” retains complete prose and examples. “Compatibility; transfer reviewed” describes routing, while the substantive owner column and capability table establish transfer; it does not count the stub itself as full content. Entrance rows describe navigation rather than displaced interfaces. The physical-Shortcut row has the P2 retrieval defect above.

| Original page | Disposition versus original | Substantive owner(s) |
| --- | --- | --- |
| `advanced/automation-and-execution-contexts.md` | authored links only | `advanced/automation-and-execution-contexts.md` |
| `advanced/build-bundles-and-controlled-installation.md` | byte-identical | `advanced/build-bundles-and-controlled-installation.md` |
| `advanced/concurrency.md` | compatibility; transfer reviewed | `estate/concurrency.md` |
| `advanced/incremental-build-selection.md` | byte-identical | `advanced/incremental-build-selection.md` |
| `advanced/incremental-data-processing.md` | byte-identical | `advanced/incremental-data-processing.md` |
| `advanced/index.md` | compatibility; transfer reviewed | `estate/index.md` |
| `advanced/mirror-and-materialisation-strategies.md` | authored links only | `advanced/mirror-and-materialisation-strategies.md` |
| `advanced/partial-failures-rejected-data-and-thresholds.md` | byte-identical | `advanced/partial-failures-rejected-data-and-thresholds.md` |
| `advanced/performance-and-scale.md` | compatibility; transfer reviewed | `estate/performance.md` |
| `advanced/portable-execution-between-desktop-and-fabric.md` | byte-identical | `advanced/portable-execution-between-desktop-and-fabric.md` |
| `advanced/power-bi/custom-annotations.md` | compatibility; transfer reviewed | `semantic-models/custom-annotations.md` |
| `advanced/power-bi/model-composition.md` | compatibility; transfer reviewed | `semantic-models/composition.md` |
| `advanced/power-bi/model-from-tmdl.md` | compatibility; transfer reviewed | `semantic-models/from-tmdl.md` |
| `advanced/power-bi/shared-policy.md` | compatibility; transfer reviewed | `semantic-models/shared-policy.md` |
| `advanced/protecting-data.md` | authored links only | `advanced/protecting-data.md` |
| `advanced/row-auditing-and-operational-history.md` | byte-identical | `advanced/row-auditing-and-operational-history.md` |
| `advanced/run-part-of-an-estate.md` | compatibility; transfer reviewed | `estate/selective-runs.md` |
| `advanced/schemas-keys-and-managed-columns.md` | byte-identical | `advanced/schemas-keys-and-managed-columns.md` |
| `basics/development-cycle.md` | compatibility; transfer reviewed | `estate/development-cycle.md`, `estate/mirror.md` |
| `basics/index.md` | compatibility; transfer reviewed | `index.md` |
| `basics/lakehouse-python.md` | compatibility; transfer reviewed | `lakehouse/python.md` |
| `basics/lakehouse-spark-sql.md` | compatibility; transfer reviewed | `lakehouse/spark-sql.md` |
| `basics/power-bi/deploy-pbip.md` | compatibility; transfer reviewed | `semantic-models/native-tmdl.md`, `semantic-models/managed-sources.md`, `reports/deploy.md`, `semantic-models/custom-annotations.md`, `reports/environments.md` |
| `basics/power-bi/environments.md` | compatibility; transfer reviewed | `reports/environments.md` |
| `basics/power-bi/fabric-integration.md` | compatibility; transfer reviewed | `semantic-models/managed-sources.md` |
| `basics/power-bi/index.md` | compatibility; transfer reviewed | `semantic-models/index.md` |
| `basics/power-bi/modelling-rule.md` | compatibility; transfer reviewed | `semantic-models/native-tmdl.md` |
| `basics/power-bi/validate.md` | compatibility; transfer reviewed | `semantic-models/validation.md` |
| `basics/recover-failed-work.md` | compatibility; transfer reviewed | `estate/recovery.md` |
| `basics/run-and-inspect-estate.md` | compatibility; transfer reviewed | `estate/operate.md` |
| `basics/sessions-and-workflows.md` | compatibility; transfer reviewed | `estate/automation-and-deployment.md` |
| `basics/shortcuts.md` | compatibility; transfer reviewed | `lakehouse/shortcuts.md`, `estate/connected-items.md` |
| `basics/tests-and-assumptions.md` | compatibility; transfer reviewed | `lakehouse/tests.md`, `warehouse/tests.md`, `semantic-models/validation.md` |
| `basics/troubleshooting.md` | authored links only | `basics/troubleshooting.md` |
| `basics/warehouse-pipeline.md` | compatibility; transfer reviewed | `warehouse/first-project.md` |
| `basics/workspace-and-python-runtime.md` | compatibility; transfer reviewed | `estate/environments.md`, `lakehouse/runtime.md`, `reports/environments.md` |
| `core-concepts/build-load-and-test.md` | byte-identical | `core-concepts/build-load-and-test.md` |
| `core-concepts/catalogue.md` | byte-identical | `core-concepts/catalogue.md` |
| `core-concepts/dependencies.md` | authored links only | `core-concepts/dependencies.md` |
| `core-concepts/design-philosophy.md` | authored links only | `core-concepts/design-philosophy.md` |
| `core-concepts/fault-tolerance.md` | byte-identical | `core-concepts/fault-tolerance.md` |
| `core-concepts/how-weaver-works.md` | authored links only | `core-concepts/how-weaver-works.md` |
| `core-concepts/index.md` | compatibility; transfer reviewed | `estate/index.md` |
| `core-concepts/logical-and-physical-items.md` | authored links only | `core-concepts/logical-and-physical-items.md` |
| `core-concepts/mirrors.md` | byte-identical | `core-concepts/mirrors.md` |
| `core-concepts/projects-and-estates.md` | byte-identical | `core-concepts/projects-and-estates.md` |
| `core-concepts/sessions-and-workflows.md` | byte-identical | `core-concepts/sessions-and-workflows.md` |
| `core-concepts/state-and-health.md` | byte-identical | `core-concepts/state-and-health.md` |
| `core-concepts/weaver-documents.md` | authored links only | `core-concepts/weaver-documents.md` |
| `getting-started/first-project.md` | live optional starter | `warehouse/first-project.md`, `warehouse/tests.md`, `estate/catalogue-and-health.md`, `estate/automation-and-deployment.md` |
| `getting-started/index.md` | revised entrance/setup | `getting-started/index.md` |
| `getting-started/installation.md` | revised entrance/setup | `getting-started/installation.md` |
| `index.md` | revised entrance/setup | `index.md` |
| `reference/build-bundle-format.md` | byte-identical | `reference/build-bundle-format.md` |
| `reference/catalogue-schema.md` | byte-identical | `reference/catalogue-schema.md` |
| `reference/cli.md` | byte-identical | `reference/cli.md` |
| `reference/cli/build.md` | authored links only | `reference/cli/build.md` |
| `reference/cli/check.md` | byte-identical | `reference/cli/check.md` |
| `reference/cli/doctor.md` | byte-identical | `reference/cli/doctor.md` |
| `reference/cli/fabric-capacity.md` | byte-identical | `reference/cli/fabric-capacity.md` |
| `reference/cli/fabric-environment.md` | byte-identical | `reference/cli/fabric-environment.md` |
| `reference/cli/fabric-notebook.md` | authored links only | `reference/cli/fabric-notebook.md` |
| `reference/cli/health.md` | byte-identical | `reference/cli/health.md` |
| `reference/cli/initialise.md` | byte-identical | `reference/cli/initialise.md` |
| `reference/cli/install.md` | byte-identical | `reference/cli/install.md` |
| `reference/cli/load.md` | authored links only | `reference/cli/load.md` |
| `reference/cli/mirror.md` | byte-identical | `reference/cli/mirror.md` |
| `reference/cli/session.md` | byte-identical | `reference/cli/session.md` |
| `reference/cli/test.md` | authored links only | `reference/cli/test.md` |
| `reference/cli/unbind.md` | byte-identical | `reference/cli/unbind.md` |
| `reference/cli/wipe.md` | byte-identical | `reference/cli/wipe.md` |
| `reference/cli/workflow.md` | byte-identical | `reference/cli/workflow.md` |
| `reference/configuration-files/fabric-environment.md` | byte-identical | `reference/configuration-files/fabric-environment.md` |
| `reference/configuration-files/index.md` | byte-identical | `reference/configuration-files/index.md` |
| `reference/configuration-files/workflow.md` | byte-identical | `reference/configuration-files/workflow.md` |
| `reference/configuration-files/workspace-config.md` | byte-identical | `reference/configuration-files/workspace-config.md` |
| `reference/index.md` | revised entrance/setup | `reference/index.md` |
| `reference/machine-readable-output.md` | byte-identical | `reference/machine-readable-output.md` |
| `reference/operation-behaviour/build.md` | byte-identical | `reference/operation-behaviour/build.md` |
| `reference/operation-behaviour/fault-and-outcome-vocabulary.md` | byte-identical | `reference/operation-behaviour/fault-and-outcome-vocabulary.md` |
| `reference/operation-behaviour/health.md` | byte-identical | `reference/operation-behaviour/health.md` |
| `reference/operation-behaviour/index.md` | byte-identical | `reference/operation-behaviour/index.md` |
| `reference/operation-behaviour/load.md` | byte-identical | `reference/operation-behaviour/load.md` |
| `reference/operation-behaviour/mirror.md` | byte-identical | `reference/operation-behaviour/mirror.md` |
| `reference/operation-behaviour/session-runtime.md` | byte-identical | `reference/operation-behaviour/session-runtime.md` |
| `reference/operation-behaviour/shared-selection-and-identity.md` | byte-identical | `reference/operation-behaviour/shared-selection-and-identity.md` |
| `reference/operation-behaviour/test.md` | byte-identical | `reference/operation-behaviour/test.md` |
| `reference/operation-behaviour/unbind.md` | byte-identical | `reference/operation-behaviour/unbind.md` |
| `reference/operation-behaviour/wipe.md` | byte-identical | `reference/operation-behaviour/wipe.md` |
| `reference/operation-behaviour/workflow.md` | byte-identical | `reference/operation-behaviour/workflow.md` |
| `reference/power-bi/annotations.md` | byte-identical | `reference/power-bi/annotations.md` |
| `reference/power-bi/index.md` | byte-identical | `reference/power-bi/index.md` |
| `reference/power-bi/project-layout.md` | byte-identical | `reference/power-bi/project-layout.md` |
| `reference/power-bi/requirements-and-compatibility.md` | byte-identical | `reference/power-bi/requirements-and-compatibility.md` |
| `reference/power-bi/tmdl.md` | byte-identical | `reference/power-bi/tmdl.md` |
| `reference/power-bi/validations.md` | byte-identical | `reference/power-bi/validations.md` |
| `reference/python/errors.md` | authored links only | `reference/python/errors.md` |
| `reference/python/index.md` | byte-identical | `reference/python/index.md` |
| `reference/python/objects.md` | authored links only | `reference/python/objects.md` |
| `reference/python/operations.md` | byte-identical | `reference/python/operations.md` |
| `reference/python/results.md` | authored links only | `reference/python/results.md` |
| `reference/python/semantic-models.md` | byte-identical | `reference/python/semantic-models.md` |
| `reference/python/session.md` | authored links only | `reference/python/session.md` |
| `reference/python/validation.md` | authored links only | `reference/python/validation.md` |
| `reference/weaver-documents/assumption.md` | byte-identical | `reference/weaver-documents/assumption.md` |
| `reference/weaver-documents/common-metadata.md` | byte-identical | `reference/weaver-documents/common-metadata.md` |
| `reference/weaver-documents/folder.md` | byte-identical | `reference/weaver-documents/folder.md` |
| `reference/weaver-documents/overview.md` | byte-identical | `reference/weaver-documents/overview.md` |
| `reference/weaver-documents/schema-metadata.md` | byte-identical | `reference/weaver-documents/schema-metadata.md` |
| `reference/weaver-documents/shortcut.md` | byte-identical | `reference/weaver-documents/shortcut.md` |
| `reference/weaver-documents/table.md` | byte-identical | `reference/weaver-documents/table.md` |
| `reference/weaver-documents/test.md` | byte-identical | `reference/weaver-documents/test.md` |
| `reference/weaver-documents/view.md` | byte-identical | `reference/weaver-documents/view.md` |
| `reference/weaver-documents/warehouse-programmable.md` | byte-identical | `reference/weaver-documents/warehouse-programmable.md` |
