# Internal documentation coverage map

This maintainer-only ledger records the state of the five-section public site. It is not rendered.

## Restructure status

| Phase | Scope | Status |
| --- | --- | --- |
| 1 | Navigation and ownership | Complete. Public navigation is **Getting started / Core concepts / Basics / Advanced / Reference**. Guides, Contracts and Contributing are not public sections. |
| 2 | Getting started and Core concepts | Complete. The first-project route is self-contained, and the concept sequence covers documents, operations, catalogue state, Mirrors, Sessions, dependencies and failure. |
| 3 | Basics | Complete. Task pages use defaults and inference first, separate Python and Spark SQL paths, distinguish logical and physical Shortcuts, and cover normal development, operation and recovery. |
| 4 | Advanced | Complete. The section covers Build selection, the general incremental Table and bookmark contracts, portable desktop/Fabric execution, history, schema, data protection, partial failure, mirroring, bundles and execution contexts. Notebook and Capacity remain CLI Reference topics. |
| 5 | Reference | Complete. Weaver documents, Python API, CLI, configuration, operation behaviour, catalogue schema, bundle format and machine-readable output have explicit owners. Generated CLI and Python blocks remain generator-owned. |
| 6 | Editorial integration | Complete on this branch. The whole rendered tree was checked for reader routes, retired paths and vocabulary, duplicated explanation, assurance and agent-facing language, future-product claims, and cross-page behavioural consistency. |

Final delivery verification must run again on the integrated head. A phase being complete here does not replace that integrated build and link check.

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

No substantive legacy page was removed. The original paths remain owners; new task pages link to reference rather than copying exhaustive contracts. The final handoff owns integrated results, screenshot locations, precise outstanding live cases and recommended publication order.

## Fabric-first editorial feedback

The feedback revision restores Fabric primacy and Lakehouse → Warehouse → semantic model → Report discovery. Basics no longer contains a separate Power BI navigation bucket; Advanced uses Semantic models. Models are integrated into core concepts, development, recovery and the shared Build/Load/Test/Health CLI pages. Public benchmark copy is rounded and short; exact measurements are retained in `scale-measurements.md`.

The parent reviewed the revised copy and screenshots and ran focused reader-flow checks. The earlier independent reviews apply to the earlier iteration, not this new prose. Revision evidence is in `acceptance/docs-refresh-2026-10/fabric-first-feedback.md`; live/release/publication gates remain held.

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
