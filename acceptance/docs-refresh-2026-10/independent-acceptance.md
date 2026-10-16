# Independent acceptance and publication handoff

## Disposition

A0–A8 implementation and local handoff are complete. Independent product review accepted its reader-experience gates without blocking defects. Independent developer review found one blocking catalogue-readback instruction; it was verified against pinned declarations/tests, corrected in the public guide and fixture README, and rechecked. The final tree has no unresolved local blocking defect from those reviews.

This is **not** live acceptance, release approval, publication approval, a complete accessibility audit, screen-reader qualification, or a cross-browser/real-device result. The matching package, explicitly authorised service acceptance and publication approval remain gates.

## Independent review evidence

Product reviewer independently exercised:

- 55 route/viewport checks at phone, tablet and desktop widths;
- 20 homepage → Features → one of four children → documentation-request journeys via keyboard, touch and no JavaScript;
- five scale → performance journeys, with optional concurrency discovery;
- code/table scrolling, static benchmark/JSON consistency, separate Power BI/Fabric prerequisites and native-output limitations.

Documentation requests were intercepted and destinations checked against staged public pages. This was not a live documentation-host test. Private review screenshots/reports remain outside the public repository.

Developer reviewer independently exercised:

- all six fixtures and 53 README command lines;
- 104 exact public-guide commands and three live public Python signatures;
- complete literal first-project, Warehouse pipeline/validation and native modelling examples assembled from the proposed public pages;
- 165 focused core tests, no declared external resources;
- strict MkDocs build and five reader paths: Power BI dev/second environment; small Fabric lifecycle/change; partial rerun with omitted producer current; one-run cap; native rule followed by optional policy/custom handler.

These are production control paths against explicit offline boundaries, not real SQL/DAX or service results. Reviewer counts overlap author/parent suites and must not be summed.

## DR-01 correction

The Fabric integration guide and README incorrectly named a catalogue object `SemanticModelSource`. Actual pinned owners are `_.SemanticModelTable` and `_.Dependency`.

The corrected instructions:

- inspect Delivery metadata under logical `SemanticModel/Parcel` in `_.SemanticModelTable`;
- inspect the `_.Dependency` row whose authored `Dependency reference` is `Warehouse/Operations/Parcel.Delivery`;
- distinguish source mode/access from source identity and allow null `Source access` for the retained authored partition;
- inspect installed validation in `_.SemanticModelTest` and recorded result in `_.TestStatus`.

Evidence owners: `src/weaver/fragments/catalogue/_.SemanticModelTable.sql`, `src/weaver/fragments/catalogue/_.Dependency.sql`, `src/weaver/catalogue/tables.py` and `tests/test_semantic_source_lineage_cycle.py` at `74b4d15ee65ed2740593af1f4d459771b801b132`.

The page/README lineage instruction is synchronized. `tools/check_journey_examples.py` now checks the named readback objects against imported physical catalogue declarations, rejects the erroneous old object, and checks the shared instruction text. The Fabric fixture file-map hash was recomputed after its README changed; authored native/configuration files are unchanged.

One small syntax clarification also spells the required path argument for `--file`. Optional suggestions about changing the execution example's emphasis and the established no-Mirror configuration were not used to redefine the accepted design or expand scope.

## Parent rechecks after correction

Using the pinned source and existing interpreters:

- `tools/check_journey_examples.py --weaver-checkout <product>`: pass; 13 pages, 68 commands, five configurations, three Python keyword sets, 12 exact fixture blocks and four literal project Checks, plus actual catalogue-name/readback guard.
- `tools/check_docs_refresh_examples.py --weaver-checkout <product>`: pass; all six fixtures, 53 README commands, compiler/planner/Runner/binding boundaries and unchanged authored hashes.
- Independent reader harness rerun: pass; 104 commands, three signatures and literal first-project/validation/pipeline/rule/policy/custom/standalone examples.
- `pytest -q -p no:cacheprovider tests/test_semantic_source_lineage_cycle.py`: **8 passed in 14.81s**, core only. Authored source metadata and Dependency round-trip match the correction.
- Strict MkDocs build: pass. Paired crawl: **126 HTML pages, 20,500 local page/asset/fragment references, 166 cross-site links, zero broken targets/fragments; seven matching historical benchmark rows**.
- Ruff check/format and whitespace: pass.
- Final private preview rebuild and exact corrected-page readback are performed as delivery artifacts, not public deployment.

Broader generator, source, schema, browser, visual/contrast and clipboard evidence remains in `journey-evidence.md`, `reference-evidence.md`, `fixture-evidence.md` and the coordinated product checkpoint.

## Unavailable service gates

None of the following is reported as passed:

- real model/Report creation/update in two disposable service workspaces, actual Report bindings and card rendering;
- model/source refresh, supported existing connection binding and resolved source expressions;
- actual DAX pass/violation/query-error and DAX-versus-SQL discrepancy/correction;
- native deployed rule/policy/custom/composed/generated-model inspection;
- real catalogue lineage, installed TestStatus/history and Health readback;
- authored-file hashes before/after both actual service deployments;
- workspace-specific licence, query-identity, tenant, source and capacity eligibility;
- separate tailnet peer loading the private previews.

No paid capacity changes, tenant settings, Environment publication, credentials/gateway creation, runtime feature work, compiled-TMDL export, merge or release occurred.

## Coordinated delivery

- Product draft: https://github.com/matthias-wong-dev/weaverstack/pull/222 — `docs/product-and-scale-refresh`.
- Developer draft: https://github.com/matthias-wong-dev/weaverstack-docs/pull/3 — `docs/progressive-journeys-refresh`.
- Public behaviour pin: `74b4d15ee65ed2740593af1f4d459771b801b132`; docs base: `f35c943ed0ca423b92ab53aa571c43ae2817b74e`.
- `baseline.md` and `claims.md` own revision/exclusion and page/claim mapping. No legacy public path is deleted. Draft PR heads are read back after each push; exact final SHAs and private screenshot/preview paths are supplied in the private handoff.

## Publication order

1. Confirm a package/runtime containing the documented interfaces. PyPI `0.9.0` is not the target; no future release number is invented.
2. Assign explicitly authorised disposable service acceptance and resolve its findings. Do not use the example's production-labelled configuration as permission for real production work.
3. Once Matthias approves publication, replace the private snapshot notice with the actual matching release instructions and publish developer docs first.
4. Verify live developer URLs, then publish the product pages and verify public DNS/TLS/representative routes separately.

The draft branches and private previews are review delivery, not permission to merge or publish.
