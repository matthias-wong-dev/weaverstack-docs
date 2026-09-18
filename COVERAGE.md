# Internal documentation coverage map

This maintainer-only ledger records the state of the five-section public site. It is not rendered.

## Restructure status

| Phase | Scope | Status |
| --- | --- | --- |
| 1 | Navigation and ownership | Complete. Public navigation is **Getting started / Core concepts / Basics / Advanced / Reference**. Guides, Contracts and Contributing are not public sections. |
| 2 | Getting started and Core concepts | Complete. The first-project route is self-contained, and the concept sequence covers documents, operations, catalogue state, Mirrors, Sessions, dependencies and failure. |
| 3 | Basics | Complete. Task pages use defaults and inference first, separate Python and Spark SQL paths, and cover normal development, operation and recovery. |
| 4 | Advanced | Complete. The section covers Build selection, data incrementality, history, schema, partial failure, mirroring, bundles and execution contexts. Notebook and Capacity remain CLI Reference topics. |
| 5 | Reference | Complete. Weaver documents, Python API, CLI, configuration, operation behaviour, catalogue schema, bundle format and machine-readable output have explicit owners. Generated CLI and Python blocks remain generator-owned. |
| 6 | Editorial integration | Complete on this branch. The whole rendered tree was checked for reader routes, retired paths and vocabulary, duplicated explanation, assurance and agent-facing language, future-product claims, and cross-page behavioural consistency. |

Final delivery verification must run again on the integrated head. A phase being complete here does not replace that integrated build and link check.

## Launch-critical coverage

The launch surface includes:

- a coherent route from Home through each section landing page;
- a complete Warehouse-only first project;
- normal Warehouse, Lakehouse Python and Lakehouse Spark SQL task paths;
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
- a published Fabric Environment is required for remote Python Load or Test work, not for Warehouse T-SQL, Spark SQL, Check or Build merely because Python documents exist;
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
- that a Fabric Environment is required for Warehouse-only or Spark-SQL-only work;
- that workflow files are a general orchestration language or transaction boundary;
- that Mirror copies between workspaces; or
- that source design documents are public API.

Reference may record exact current representations without converting them into cross-version guarantees.
