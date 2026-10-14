# Internal documentation coverage map

This maintainer-only ledger records the item-first revision and earlier delivery evidence. It is not rendered.

## Active item-first revision

Approved plan: `weaver-docs-item-first-reorganisation-agent-plan.md` supplied by Matthias. New navigation: Getting started / Lakehouse / Warehouse / Semantic models / Reports / Coordinate your estate / Reference. This supersedes the previous taxonomy, not its technical evidence.

| Package | Current state |
|---|---|
| Frozen evidence and retention map | Committed; 114 original pages accounted for, 35 canonical item/estate routes. See `acceptance/docs-item-first-2026-10/route-map.md`. |
| Short entrances, sitemap and guidance | Integrated; strict build and actual two-click item entrances pass. |
| Lakehouse and Warehouse | Integrated and parent-reviewed. Lakehouse: 7 local Check checkpoints / 12 exact fixture blocks; Warehouse: 5 checkpoints / 12 exact blocks. Expected service outcomes remain unobserved. |
| Models and Reports | Integrated and parent-reviewed. Seven model tasks: 12 compiled Check checkpoints / 16 exact blocks. Reports: 8 command parses / 4 exact blocks / native and offline dev/prod binding gate passed. |
| Estate and reference/link audit | Integrated; 35 canonical pages, 114 original routes, 872 old IDs and 26 direct search-excluded compatibility routes pass the rendered gate. Product links canonical. |
| Independent reader/retention reviews | Four-pair scope finished. Five reader paths and full retention independently reviewed; four verified findings corrected/rechecked by parent. Final human acceptance remains Matthias. |
| Technical/browser/search verification | Current integrated iteration passes locked build, generators and 1135 focused core cases. Browser: 410 responsive/theme checks, 8 live search queries, only active group expanded, two-click entries and no-JS/touch/keyboard pass. Final rerun follows any review corrections. |
| Draft/private-preview delivery | Corrected preview built on existing private routes; final PR heads/readback recorded in final-verification.md. No release, merge, public publication or live service acceptance. |

The earlier five-section and feedback iterations below are historical evidence.
Final reader acceptance belongs to Matthias; independent agent/editor review and
local technical checks do not replace it.

## Pinned-main refresh

Behaviour target: `74b4d15ee65ed2740593af1f4d459771b801b132`; documentation base: `f35c943ed0ca423b92ab53aa571c43ae2817b74e`. Publication is held for a matching package and explicit approval; these previews must not be mistaken for PyPI `0.9.0` documentation.

| Work package | Integrated scope | State |
| --- | --- | --- |
| A0 | Baseline, exclusions and claim/mode ownership | Recorded in `acceptance/docs-refresh-2026-10/baseline.md` and `claims.md` |
| A1 | Nine reference owners, existing reference audit, four generators | Integrated; see `reference-evidence.md` for source/test evidence and unchanged owners |
| A2 | Six complete small fixtures and explicit offline/live boundaries | Integrated; parent reran fixture checker successfully; see `fixture-evidence.md` |
| A3 | D01–D06, Fabric-first authoring with semantic models/Reports integrated beside Lakehouse/Warehouse work | Feedback revision implemented; original URLs retained, shared lifecycle explained |
| A4 | D07–D13, selective Load/concurrency/performance and optional native modelling | Implemented; exact syntax remains reference-owned |
| A5 | Fabric-first homepage/Features, ordered item pages, rounded scale results and native Power BI dbt comparison | Feedback revision coordinated in the product repository; exact timings retained in maintainer evidence |
| A6 | Navigation, contextual links, generated ownership and version notice | Integrated; final strict build and paired-site checks pass |
| A7 | Build, rendered links, examples, browser and independent reader review | Local acceptance complete; reviewer DR-01 corrected/rechecked; live deployment/query/render/licensing not run; see `independent-acceptance.md` |
| A8 | Draft PRs, private paired previews and release handoff | Both draft PRs and private proxy mappings verified; final heads/private addresses supplied in handoff; no merge or public publication |

No substantive legacy content was removed. Original routes remain reachable; retired model-specific tutorial routes now point to the shared authoring, validation and configuration owners. Exact contracts stay reference-owned. The final handoff owns integrated results, screenshot locations, precise outstanding live cases and recommended publication order.

## Fabric-first editorial feedback

The feedback revision restores Fabric primacy and Lakehouse → Warehouse → semantic model → Report discovery. Basics no longer contains a separate Power BI navigation bucket; Advanced uses Semantic models. Models are integrated into core concepts, development, recovery and the shared Build/Load/Test/Health CLI pages. Public benchmark copy is rounded and short; exact measurements are retained in `scale-measurements.md`.

The parent reviewed the revised copy and screenshots and ran focused reader-flow checks. The earlier independent reviews apply to the earlier iteration, not this new prose. Revision evidence is in `acceptance/docs-refresh-2026-10/fabric-first-feedback.md`; live/release/publication gates remain held.

## Page-ownership correction

The accepted product tagline is restored verbatim: Making Fabric easier to use. Core Weaver documents explains TMDL overlays and Weaver annotations as the semantic-model counterpart to SQL/Python engineering declarations. Native model deployment introduces ordinary TMDL before optional annotations and custom handlers. Add Tests and Assumptions owns the full DAX and DAX-to-SQL examples; workspace configuration owns model/Report environment switching. Four former top-level model-specific task leaves are compatibility pointers, not duplicated tutorial owners, and are excluded from search. Incoming narrative/product links target the new owners.

The private structural assessment is `docs-flow-correction.md` in the task scratch folder. Verification for this revision is recorded in `acceptance/docs-refresh-2026-10/page-ownership-feedback.md`.

## Acceptance follow-up

The 19 September documentation corrections are complete on `docs/acceptance-fixes`: ownership boundaries, the two incremental fixtures, Mirror prerequisites, Fabric notebook-source input, Initialise and Workflow interaction, Windows output handling and pre-release Environment publication guidance. The internal [acceptance addendum](acceptance/2026-09-19-addendum.md) preserves corrected classifications and the remaining black-box handover. Live Fabric reruns remain deliberately unclaimed until the independent tester records them against the final pull-request head.

## Launch-critical coverage

The launch surface includes:

- a coherent route from Home through each section landing page;
- a concise statement of the stateful Fabric-estate problem Weaver owns;
- the Design philosophy principles behind authoring, installation, operation and environment binding;
- a source-backed, reproducible route for moving one project between desktop and Fabric and running installed artefacts in Fabric;
- a complete Warehouse-only first project;
- normal Lakehouse Python/Spark SQL and Warehouse task paths, followed by native semantic-model and Report deployment;
- shared source/model dependency ordering, SQL/Python/DAX validation and whole-estate Health;
- the logical/physical Shortcut ownership boundary and its effect on project dependencies;
- general Python and SQL incremental Table staging/delete contracts, with consumer-owned bookmark state;
- recoverability-based guidance for external physical data and `Prohibit rebuild`;
- exact Weaver-document defaults and accepted forms;
- configuration discovery, precedence and workspace restrictions;
- CLI and public Python interfaces synchronized with the selected Weaver checkout;
- operation selection, state changes, outcomes, failure boundaries and recovery routes;
- catalogue, bundle and machine-output representations labelled as current output where no compatibility policy exists; and
- internal links across every rendered Markdown page.

The following cross-page rules are launch-critical and reconciled:

- inferred dependencies are the normal authoring path; explicit `Dependencies` replaces inference;
- Spark SQL Tables and Views require explicit `Dependencies`, including an empty list when applicable;
- document and item dependency graphs must remain acyclic;
- Mirror source, destination catalogue and destination targets resolve in one workspace;
- Folder `Incremental` defaults to `true`, while Table `Incremental` defaults to `false`;
- Sessions reuse execution context without changing operation semantics; Workflows run ordinary commands in order and do not add rollback;
- `load --stale` is the normal post-Build catch-up path, while `--name` is deliberate narrow selection and does not add dependencies;
- local Check needs no hosted runtime; Warehouse-only SQL work has no Spark runtime requirement; Spark-backed Build admits the matching Weaver/runtime even though it does not call authored `read()`, and generated Lakehouse Load/Test needs a compatible runtime;
- Build, Load, Test, Mirror, Wipe and Workflow retain their own failure and partial-state boundaries; and
- current status, bookmarks and Health findings are distinct from append-oriented Log and LoadStatistic history.

## Optional documentation depth

These additions are not launch blockers and must remain documentation work rather than implied product commitments:

- more independent domain examples after the canonical task paths;
- additional troubleshooting symptoms backed by observed failures and recovery tests;
- longer integration examples for public Python result types; and
- release-specific compatibility notes when an explicit compatibility policy exists.

## Withheld claims

The site does not claim:

- compatibility guarantees for unversioned bundle, catalogue or command-output formats;
- stability for internal Python modules;
- a universal authentication prerequisite beyond the implemented credential chain;
- that every Fabric workspace exposes every Doctor probe;
- that a Fabric Environment is required for Warehouse-only work, or that Spark-SQL-only work bypasses Spark-backed runtime admission;
- that workflow files are a general orchestration language or transaction boundary;
- universal CLI, Python and notebook parity beyond the interfaces named on the portability page;
- that Mirror copies between workspaces; or
- that source design documents are public API.

Reference may record exact current representations without converting them into cross-version guarantees.
