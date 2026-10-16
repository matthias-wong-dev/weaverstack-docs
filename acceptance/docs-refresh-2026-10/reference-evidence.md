# A1 reference and compatibility evidence

## Scope and revision

- Docs worktree: `/opt/data/scratch/Fors/weaver-docs-refresh/reference`, branch `docs/reference-compatibility-refresh`, base `a7254005fea83de8d9b11e01aed25611f781af26`.
- Behaviour target: Weaver `74b4d15ee65ed2740593af1f4d459771b801b132`. All source/test paths below refer to that revision; pinned source URLs use `https://github.com/matthias-wong-dev/weaverstack/blob/74b4d15ee65ed2740593af1f4d459771b801b132/<path>`.
- Package publication remains held for a matching approved release. The older published `weaverstack 0.9.0` is not asserted to contain these main interfaces. No future release number/date is invented.
- No push, publication, capacity operation, Fabric mutation, remote acceptance, tenant-setting change, Environment publication or package install was performed by this author. PR #220 Installation-schema and PR #208 Dashboard proposals were excluded.
- Changes are confined to `docs/reference/**`, reference tooling/manifests and this evidence file. Navigation, fixtures, `COVERAGE.md`, shared claims/baseline and product runtime are not edited by this author.

### Concurrent product-worktree movement

The product worktree initially resolved to the pinned SHA. During final verification its HEAD moved to `84add848269c39ff5fd72a9ab8e385e47c2eeedb` for concurrent product-site documentation work, with additional uncommitted website edits and a pre-existing untracked `uv.lock`. This author did not create that commit or change those files and did not restore them.

`git diff --name-status 74b4d15ee65ed2740593af1f4d459771b801b132 -- src tests pyproject.toml VERSION` was empty. Exact Git tree checks returned:

| Tree | Pinned revision | Observed HEAD |
| --- | --- | --- |
| `src` | `cbedc7f13c5f15b12e42fc5927dcefc184dbbcb0` | same |
| `tests` | `2ba0ad5a48ef7e1c6a3bfa859213610db14ace08` | same |

Thus the exercised implementation/tests remain byte-identical to the behavioural pin; the whole product checkout is not claimed unchanged. Recheck runtime trees and package/version alignment at integration/publication.

## Ownership and completed reference

The nine new owners are substantive reference pages, not journey stubs:

- `docs/reference/cli/unbind.md`
- `docs/reference/operation-behaviour/unbind.md`
- `docs/reference/power-bi/annotations.md`
- `docs/reference/power-bi/index.md`
- `docs/reference/power-bi/project-layout.md`
- `docs/reference/power-bi/requirements-and-compatibility.md`
- `docs/reference/power-bi/tmdl.md`
- `docs/reference/power-bi/validations.md`
- `docs/reference/python/semantic-models.md`

They cover discovery/naming/native files, exact merge/composition rules, all seven built-ins, DAX metadata/body/comparison/diagnostics, the authoritative catalogue-free/integrated mode matrix, supported extension methods/properties and claim-only Unbind. Existing Build/Load/Test own mode-specific operation rules rather than duplicate Power BI operation pages.

Existing narrative was reconciled for parser/API drift, name/file selectors, original-seed recursive Load scope, invocation/resource concurrency, read-only Build preview, missing Power BI target provisioning, selected-model redeployment versus source/Report fixed points, format-5 frozen installation, semantic Wipe, Mirror final publication/protected materialisation, runtime admission and Workflow findings. Public examples remain neutral and generated blocks were regenerated, never hand-edited.

Generated ownership:

| Generator/manifest | Verified surface |
| --- | --- |
| `tools/generate_cli_reference.py`, `generated/cli-reference.json` | 18 live parser leaves, 16 owner pages; includes Unbind and aliases |
| `tools/generate_python_reference.py`, `generated/python-reference.json` | 55 `weaver.__all__` exports, 7 owner pages; includes Unbind functions/results |
| `tools/generate_semantic_reference.py`, `generated/semantic-reference.json` | Explicit Annotation/TmdlDefinition classes and returned TmdlObject/TmdlCollection protocols, public members/defaults/properties; excludes private compiler/editor classes and unsupported view constructors |
| `tools/generate_catalogue_reference.py`, `generated/catalogue-reference.json` | All 23 physical table declarations including optional Mirror, all physical columns/types/nullability/keys/audits and stored vocabulary; includes semantic metadata/validations and item IDs |

The extension generator uses AST extraction, so source inspection does not execute project annotations. Catalogue extraction verifies the imported module came from the explicit checkout. Added unit tests detect unowned/retired/duplicate CLI ownership, marker errors, missing classes, duplicate members, signature/property drift, catalogue duplicates/column drift and wrong checkout imports.

## Claim → source → locally executed test

Tests below use core declarations with no external resources, checked before execution. Passing mock/representation tests establish local implementation behaviour, not a live service deployment or licensing qualification.

| Claim | Authoritative owner | Implementation | Executed test evidence |
| --- | --- | --- | --- |
| Discovery and names | `docs/reference/power-bi/project-layout.md` | `src/weaver/powerbi.py:86–147` | `tests/test_semantic_composition_declaration.py:242–256` |
| Report association precedence | `docs/reference/power-bi/project-layout.md` | `src/weaver/powerbi.py:150–222` | `tests/test_report_convention_cycle.py` |
| TMDL merge/ref/preservation | `docs/reference/power-bi/tmdl.md` | `src/weaver/semantic_models/extensions.py:293–312` | `tests/test_semantic_tmdl_package_representation.py:100–128` |
| Composition order/cycles/repeated ancestry | `docs/reference/power-bi/tmdl.md` | `src/weaver/semantic_models/composition.py:32–159` | `tests/test_semantic_composition_declaration.py:30–65` |
| Seven annotations and scopes | `docs/reference/power-bi/annotations.md` | `src/weaver/semantic_models/builtin_annotations.py` | `tests/test_semantic_annotation_validation_representation.py:70–80` |
| Trusted custom code and phases | `docs/reference/python/semantic-models.md` | `src/weaver/semantic_models/annotation.py:162–218` | `tests/test_semantic_annotation_phase_cycle.py:136–184` |
| Native editing properties/collections | `docs/reference/python/semantic-models.md` | `src/weaver/semantic_models/objects.py:84–98` | `tests/test_semantic_tmdl_objects_representation.py:87–98` |
| Source generation vs authored partition preservation | `docs/reference/power-bi/annotations.md` | `src/weaver/semantic_models/binding.py:194–278` | `tests/test_semantic_source_preservation_cycle.py:158–236` |
| Catalogue-free deploy/refresh/Tests | `docs/reference/power-bi/requirements-and-compatibility.md` | `src/weaver/operations/build.py:87–223` | `tests/test_semantic_model_catalogue_free_cycle.py:41–67` |
| Report-only and unchanged modes | `docs/reference/operation-behaviour/build.md` | `src/weaver/build_bundle/reports.py` | `tests/test_report_build_cycle.py` |
| Ordinary missing Power BI targets vs preview/bundle | `docs/reference/operation-behaviour/build.md` | `src/weaver/fabric/powerbi_items.py:19–92` | `tests/test_powerbi_item_creation_cycle.py` |
| Separate source/PowerBI Build | `docs/reference/operation-behaviour/build.md` | `src/weaver/build_bundle/workflow.py:203–237` | `tests/test_powerbi_separate_build_boundary.py` |
| Shared source mapping; existing credential binding | `docs/reference/power-bi/requirements-and-compatibility.md` | `src/weaver/semantic_models/expressions.py:68–122` | `tests/test_semantic_shared_sources_cycle.py:75–93` |
| Connection failure/binding/refresh limits | `docs/reference/power-bi/requirements-and-compatibility.md` | `src/weaver/fabric/semantic_model.py` | `tests/test_semantic_model_binding_boundary.py:176–210` |
| DAX metadata, source mode and finding/error distinction | `docs/reference/power-bi/validations.md` | `src/weaver/declaration/source.py:657–698` | `tests/test_semantic_validation_run_cycle.py:353–368` |
| Positional set comparison and keys | `docs/reference/power-bi/validations.md` | `src/weaver/runtime/relation_compare.py:41–90` | `tests/test_semantic_validation_run_cycle.py:218–236` |
| Regex and original-seed expansion | `docs/reference/operation-behaviour/load.md` | `src/weaver/load_plan.py:180–213` | `tests/targeted/test_load_recursive_selection_cycle.py` |
| Resource defaults and target name-only shape | `docs/reference/configuration-files/workspace-config.md` | `src/weaver/config.py:140–166` | `tests/test_config_declaration.py` |
| Invocation caps and file serial default | `docs/reference/operation-behaviour/test.md` | `src/weaver/operations/test.py:266–288` | `tests/targeted/test_invocation_api_concurrency_boundary.py` |
| Read-only canonical preview | `docs/reference/operation-behaviour/build.md` | `src/weaver/build_bundle/preview.py:14–138` | `tests/targeted/test_build_preview_review_representation.py` |
| Protected mirror materialisation | `docs/reference/operation-behaviour/mirror.md` | `src/weaver/build_bundle/materialisation.py` | `tests/targeted/test_protected_mirror_materialisation_cycle.py` |
| Mirror final transaction vs independent reconstruction | `docs/reference/operation-behaviour/mirror.md` | `src/weaver/mirror_plan.py:895–959` | `tests/test_mirror_boundary.py` |
| Semantic Wipe/Report refusal/Unbind | `docs/reference/operation-behaviour/wipe.md` | `src/weaver/operations/wipe.py:272–363` | `tests/test_semantic_wipe_cycle.py:202–223` |
| Claim-only removal/presence-dependent confirmation | `docs/reference/operation-behaviour/unbind.md` | `src/weaver/operations/unbind.py:150–226` | `tests/test_unbind_operation_cycle.py:133–158` |
| Workflow findings continue, exceptions stop | `docs/reference/operation-behaviour/workflow.md` | `src/weaver_cli/workflow.py:196–227` | `tests/test_workflow_cycle.py:522–549` |
| Format5 execution graph/integrity/frozen context | `docs/reference/build-bundle-format.md` | `src/weaver/mutation/models.py:290–364` | `tests/test_bundle_execution_boundary.py:554–567` |
| Exact hosted runtime admission | `docs/reference/operation-behaviour/session-runtime.md` | `src/weaver/sessions/hosted_runtime.py:30–72` | `tests/targeted/test_hosted_runtime_identity_boundary.py` |
| Physical catalogue including semantic tables/Mirror | `docs/reference/catalogue-schema.md` | `src/weaver/catalogue/tables.py` | `tests/test_public_catalogue_schema_invariant.py` |
| Report-return Python Test, current JSON/CLI status | `docs/reference/machine-readable-output.md` | `src/weaver_cli/main.py:1658–1660` | `tests/test_cli_test_representation.py` |

## Actual local commands and results

### Tooling substitution

The docs environment was already installed. No `uv sync` was run here and no product environment was created. Storage dropped below 10 MiB during concurrent setup, then parent cleanup made room for the strict build. Product/generator/tests use the existing dependency environment with explicit source precedence:

```bash
export WEAVER_CHECKOUT=/opt/data/scratch/Fors/weaver-docs-refresh/product
export PYTHONPATH="$WEAVER_CHECKOUT/src"
# Interpreter used: /opt/data/repos/weaverstack/.venv/bin/python
```

An import probe returned `/opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py`, not the old editable checkout. The documented `uv run --project` commands were not pretended to have run; the interpreter/PYTHONPATH substitution below is what actually executed.

### Generators and tooling tests (docs worktree)

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_cli_reference.py --write --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `wrote 18 leaf commands; updated 0 page(s)`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_cli_reference.py --check --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `validated 18 leaf commands across 16 page(s)`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_python_reference.py --write --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `wrote 55 public exports; updated 0 page(s)`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_python_reference.py --check --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `validated 55 public exports across 7 page(s)`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_semantic_reference.py --write --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `wrote 4 supported extension classes`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_semantic_reference.py --check --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `validated 4 supported extension classes`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_catalogue_reference.py --write --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `wrote 23 catalogue table declarations`.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/generate_catalogue_reference.py --check --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

Exit `0`: `validated 23 catalogue table declarations`.

A second full write cycle compared SHA-256 over all 65 reference Markdown/manifest artifacts before and after: byte-identical. CLI/Python reported zero page changes on that cycle. All owned pages have one generated marker pair.

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m unittest discover -s tools -p 'test_generate*reference.py' -v
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python tools/check_reference_examples.py --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
/opt/data/repos/weaverstack/.venv/bin/python -m ruff check tools/*reference*.py
/opt/data/repos/weaverstack/.venv/bin/python -m ruff format --check tools/*reference*.py
git diff --check
```

Results: 16 generator unit tests passed; 98 displayed CLI/workflow commands parsed; 6 complete workspace configurations parsed; 4 Python operation-call keyword sets matched live signatures; 2 exact DAX file blocks parsed; the exact native-editor Python example executed and its measure expression/format were verified. Lint passed, all 8 reference tools were formatted and diff whitespace passed. These checks dispatch no service commands.

### Focused product tests (product worktree)

Every selected function had exactly one argument-free `@weaver_test()` declaration. That means core scope and no declared `tds`, `livy`, `onelake` or `rest` resources. No `tests/fabric` case was run. `-p no:cacheprovider` avoided a pytest cache write.

#### Power BI/selection/bundle

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m pytest -q -p no:cacheprovider tests/targeted/test_invocation_api_concurrency_boundary.py tests/targeted/test_invocation_concurrency_boundary.py tests/targeted/test_load_recursive_selection_cycle.py tests/targeted/test_notebook_source_concurrency_boundary.py tests/test_build_bundle_model_representation.py tests/test_bundle_execution_boundary.py tests/test_cli_load_representation.py tests/test_powerbi_item_creation_cycle.py tests/test_powerbi_separate_build_boundary.py tests/test_report_binding_boundary.py tests/test_report_build_cycle.py tests/test_report_catalogue_cycle.py tests/test_report_convention_cycle.py tests/test_report_destructive_boundary.py tests/test_semantic_annotation_build_cycle.py tests/test_semantic_annotation_composition_cycle.py tests/test_semantic_annotation_declaration.py tests/test_semantic_annotation_exclude_cycle.py tests/test_semantic_annotation_origins_representation.py tests/test_semantic_annotation_phase_cycle.py tests/test_semantic_annotation_representation.py tests/test_semantic_annotation_source_cycle.py tests/test_semantic_annotation_validation_representation.py tests/test_semantic_composition_build_cycle.py tests/test_semantic_composition_declaration.py tests/test_semantic_composition_source_representation.py tests/test_semantic_custom_annotation_declaration.py tests/test_semantic_extension_cycle.py tests/test_semantic_extension_representation.py tests/test_semantic_model_catalogue_free_cycle.py tests/test_semantic_shared_sources_cycle.py tests/test_semantic_source_preservation_cycle.py tests/test_semantic_tmdl_objects_representation.py tests/test_semantic_tmdl_package_representation.py tests/test_semantic_validation_build_cycle.py tests/test_semantic_validation_declaration.py tests/test_semantic_validation_journey_representation.py tests/test_semantic_validation_run_cycle.py tests/test_semantic_wipe_boundary.py tests/test_semantic_wipe_cycle.py tests/test_semantic_wipe_declaration.py tests/test_semantic_wipe_representation.py tests/test_unbind_cycle.py tests/test_unbind_operation_cycle.py tests/test_workflow_cycle.py tests/test_workspace_config_discovery_declaration.py
```

Exit `0`; 717 passed in 122.66s (0:02:02).

#### Configuration/preview/protection/Mirror

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m pytest -q -p no:cacheprovider tests/targeted/test_build_preview_representation.py tests/targeted/test_build_preview_review_representation.py tests/targeted/test_build_preview_typed_identity_representation.py tests/targeted/test_materialisation_live_assertion_boundary.py tests/targeted/test_materialisation_native_program_boundary.py tests/targeted/test_materialisation_publication_boundary.py tests/targeted/test_native_materialisation_boundary.py tests/targeted/test_protected_mirror_materialisation_cycle.py tests/test_build_preview_semantic_validation_cycle.py tests/test_catalogue_tables_declaration.py tests/test_cli_mirror_representation.py tests/test_cli_test_representation.py tests/test_config_declaration.py tests/test_delta_protocol_declaration.py tests/test_file_lakehouse_dispatch_boundary.py tests/test_file_test_workspace_boundary.py tests/test_mirror_boundary.py tests/test_mirror_plan_boundary.py tests/test_public_catalogue_schema_invariant.py
```

Exit `0`; 620 passed in 44.33s.

#### Hosted runtime admission

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m pytest -q -p no:cacheprovider tests/targeted/test_hosted_runtime_identity_boundary.py tests/targeted/test_hosted_runtime_session_boundary.py
```

Exit `0`; 15 passed in 1.90s.

#### Deployment/connections/REST/readback

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_semantic_model_build_cycle.py tests/test_semantic_model_mutation_boundary.py tests/test_semantic_model_binding_boundary.py tests/test_semantic_source_build_cycle.py tests/test_semantic_source_lineage_cycle.py tests/test_semantic_m_source_representation.py tests/test_semantic_model_rest_boundary.py tests/test_semantic_model_session_boundary.py tests/test_semantic_model_runner_cycle.py tests/test_powerbi_cli_requirements_boundary.py tests/test_report_definition_representation.py
```

Exit `0`; 207 passed in 75.21s (0:01:15).

The four runs cover 78 distinct test files and report 1,559 passing test cases in total. No live-resource case is included. Recursive/concurrency evidence partly overlaps the parent’s separate check; it is not counted as new live acceptance.

After the parent reiterated runtime/Workflow drift, the three affected files were rechecked for argument-free `@weaver_test()` declarations and rerun without recursive/concurrency duplication:

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_workflow_cycle.py tests/targeted/test_hosted_runtime_identity_boundary.py tests/targeted/test_hosted_runtime_session_boundary.py
```

Exit `0`: `51 passed in 3.06s`, core scope and no declared resources. This rerun is a subset, not 51 additional distinct cases. Both Workflow owner pages distinguish collected Test/Health findings from immediately stopping errors; Build and Session runtime owners distinguish hosted Spark-backed admission from Warehouse-only/standalone Power BI work.

### Strict build and internal links

```bash
.venv/bin/mkdocs build --strict --site-dir /opt/data/profiles/editor/cache/scratch/weaver-reference-site
```

Exit `0`, final build completed in 3.52 seconds. MkDocs emitted INFO listing the nine new pages absent from navigation, as expected because the coordinator owns `mkdocs.yml`; it was not a strict-build failure. Material emitted its own generic MkDocs-2 warning banner. No navigation or dependency changes were made to silence either message.

A standard-library HTML parser crawled all 102 generated HTML pages, resolved 14,624 local anchor links and checked fragment IDs: zero broken targets/fragments. External links, deployed routes, rendering/screenshots, accessibility and independent reader/live acceptance were not exercised here. The local site output is disposable scratch, not a published site.

## Corrections found during verification

- The first offline DAX snippet check rejected missing `Description` on the displayed Test. `_parse_validation` calls `_parse_text` with a required non-empty value. The exact snippet and required-key narrative were corrected, and the checker then passed both displayed files. This was an authoring error corrected before commit, not a product defect.
- An initial tool lint run reported non-executable shebangs, regex aliases/import formatting, literal-dict style and deliberate local-sample `exec`. Executable modes/format/style were corrected; only the explicit local documentation sample execution has a explained `S102` waiver. Final lint/format checks passed.
- Source/check docs saying no authored Python runs needed the custom-annotation exception: trusted annotation module bodies execute during parsing, including Check; handlers execute during Build compilation.
- Install no longer accepts workspace/configuration options. Reference examples and bundle prose now use the frozen manifest context, not stale CLI arguments.
- Bundle format is 5, not 3; loader now checks sealed identity, graph, completion/protection rules and unknown fields. Sequential batch-barrier claims were removed.
- Build does not call an authored `read()`, but hosted Spark-backed mutation still requires compatible Weaver runtime admission. Warehouse-only and Power BI-only modes are separate.
- Source `AGENTS.md` contains stale semantic-model-only/no-Report statements. Pinned implementation and executed Report/catalogue-free tests outrank those statements; source prose was not modified.

## Complete existing-page audit

All 52 pre-existing Reference pages were reviewed. 41 changed (including generated-only pages); the following 11 were reviewed unchanged against their parser/export or source-declaration authority. Their relevant rules remain scoped to their own data/notebook/administration surface and were not promoted to universal Power BI behaviour:

- `docs/reference/cli/fabric-capacity.md`
- `docs/reference/cli/fabric-notebook.md`
- `docs/reference/cli/mirror.md`
- `docs/reference/cli/session.md`
- `docs/reference/python/validation.md`
- `docs/reference/weaver-documents/common-metadata.md`
- `docs/reference/weaver-documents/folder.md`
- `docs/reference/weaver-documents/schema-metadata.md`
- `docs/reference/weaver-documents/shortcut.md`
- `docs/reference/weaver-documents/view.md`
- `docs/reference/weaver-documents/warehouse-programmable.md`

The affected narrative scan found no active obsolete `strict=`, singular operation `file=`, target-level execution controls, or old unnamed overlay instructions. Retired spellings occur only in explicit rejection/migration notes. There is no universal unchanged-Build no-op claim. Native authored semantic bases require TMDL; deployed TMSL readback is not `model.bim` authoring support. No compiled-TMDL export, RLS/partition preservation guarantee, external arbitrary M substitution or universal no-Environment promise was introduced.

## Remaining integration and publication gates

- Coordinator adds the nine new reference paths to navigation, updates older non-reference journeys/runtime/install examples, integrates fixture/journey branches, and reconciles `COVERAGE.md` and the shared ledger.
- Matching package availability/version context is still a publication gate. Recheck generated facts after integration against the explicit behavioural checkout.
- No live Power BI/Fabric deployment, refresh, binding, permission, licence/capacity, native service readback, cleanup or benchmark acceptance is claimed. A7 must exercise approved disposable targets independently.
- No local visual/a11y screenshot sweep or cross-site deployed URL check was performed under this A1 boundary. The strict build and local link crawl are necessary but not those gates.
- Product website data/benchmark changes observed concurrently belong to the parent; this reference author did not run or qualify the historical benchmark.
