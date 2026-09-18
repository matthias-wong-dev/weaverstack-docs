# Design philosophy

Weaver is shaped around the distinction between what a project declares, what Build installs and what later operations do. The principles below explain the consequences of that distinction for authoring and operating a Fabric estate.

## Natural authoring

> **Use SQL and Python as SQL and Python. Add only the declaration needed to identify, build and operate the estate.**

A Weaver document keeps its executable body in T-SQL, Spark SQL or Python. Its path and metadata add a logical identity such as `Parcel.Event`, the owning item and the properties Weaver needs for the lifecycle. Physical workspace, Lakehouse and Warehouse names stay in workspace configuration rather than authored logic.

Consequences:

- Python imports and SQL relation references supply dependencies where inference is supported.
- Spark SQL Tables and Views still require an explicit `Dependencies` field, including `Dependencies: []` when no managed dependency exists.
- An explicit `Dependencies` field replaces inference rather than extending it.
- `Lineage`, foreign keys and other descriptive references describe the estate; they do not create execution dependencies.

See [Weaver documents](weaver-documents.md), [Dependencies](dependencies.md) and [Common metadata](../reference/weaver-documents/common-metadata.md) for the authoring rules.

## Declaration and execution are separate

> **Build defines the installed estate. Load and Test operate it.**

```text
project source
    │ Build
    ▼
installed estate
    ├── Load
    └── Test
         │
         ▼
operational state
```

Build interprets project source, resolves its physical bindings and installs definitions and executable work. Load and Test then read that installed generation from the catalogue; they do not reopen the project. Editing source therefore changes the intended estate, but the operating estate changes only after Build installs a new generation.

This gives Build, Load and Test distinct state and failure boundaries. Build can install load code without executing it. Load changes data and load state. Test records validation outcomes. A failure in one boundary does not turn the others into one transaction. [Build, Load and Test](build-load-and-test.md) owns the lifecycle model; [operation behaviour](../reference/operation-behaviour/index.md) defines each boundary precisely.

## Reconcile change rather than recreate the estate

> **Compare desired, installed and operational state, then act on the difference.**

Build compares authored declarations, catalogue certification and physical inventory. Signatures identify changed definitions; managed dependencies identify affected descendants within the selected items; unchanged installed definitions remain in place. Load uses bookmarks and current health to select or process outstanding data work. In a mirrored development estate, unchanged objects can remain borrowed while changed or affected objects become local.

This principle is not a universal “incremental” promise. `Incremental` has specific Table and Folder meanings, with document-specific defaults. Rebuilding loadable work resets its current Load state and bookmark, and reload explicitly reconstructs selected Tables. Re-mirroring is also a deliberate reset: it reconstructs the selected destination boundary from a new source baseline rather than refreshing around local work.

The detailed mechanisms are [incremental Build selection](../advanced/incremental-build-selection.md), [incremental data processing](../advanced/incremental-data-processing.md) and [Mirror and materialisation strategies](../advanced/mirror-and-materialisation-strategies.md).

## Fabric-native by construction

> **Fabric is the execution environment and the home of the installed estate, not merely a notebook front end.**

Build installs executable work into Fabric: Warehouse relations and procedures, Lakehouse runtime modules and generated runtime primitives for Spark SQL-authored work. Load and Test execute that installed work against the catalogue and physical items. A desktop process can orchestrate remote Fabric capabilities; Python already running in the target Fabric workspace can use the host's active context. In both cases, the estate and its recorded state remain in Fabric rather than in a desktop process that must stay in the execution path.

The available capabilities and invocation form depend on the host, so this principle does not imply that every CLI command has an identical Python or notebook counterpart. [Portable execution between desktop and Fabric](../advanced/portable-execution-between-desktop-and-fabric.md) covers the supported paths and their qualifications. [Automation and execution contexts](../advanced/automation-and-execution-contexts.md) defines how sessions obtain Fabric capabilities.

## Operational state is data

> **Record the estate's state in queryable catalogue tables.**

The catalogue records installed bindings and definitions, dependencies, current bookmarks, Load and Test status, execution history, row counts and borrowed Mirror state. Workflow identifiers correlate related work. Managed row-audit datetimes describe the current lifecycle state of stored rows, while Health combines installed, operational and optional physical evidence into a current estate view.

This separates current state from history and makes partial outcomes inspectable after the process that produced them has ended. `_.Installation`, `_.Registry` and `_.Dependency` describe installed state; `_.Bookmark`, `_.LoadStatus` and `_.TestStatus` describe current operation state; `_.Log` and `_.LoadStatistic` retain operation history; `_.Mirror` identifies borrowed objects.

See [Catalogue](catalogue.md), [State and health](state-and-health.md), [Row auditing and operational history](../advanced/row-auditing-and-operational-history.md) and the [catalogue schema reference](../reference/catalogue-schema.md).

## Failure is local

> **Record failure at the affected unit and preserve the state that remains.**

Failure policy is operation-specific. A fault-tolerant Load can continue independent selected work after one node fails, while blocked work records that a required boundary was not established. Test records each validation outcome. Build stops later installation barriers when their prerequisites fail. In every case, completed work and its evidence remain visible.

Build, Load, Test and Workflow have no operation-wide rollback. Recovery starts from the actual installed, data and catalogue state left behind; it is a new operation, not the continuation of a hidden transaction. [Fault tolerance](fault-tolerance.md) explains the model, and [fault and outcome vocabulary](../reference/operation-behaviour/fault-and-outcome-vocabulary.md) defines the exact outcomes and barriers.

## One project, many estates

> **Physical environment is a binding, not a fork of the logical project.**

Logical item and document identities remain stable while workspace configuration supplies a workspace, catalogue and physical targets. Development and production can therefore use the same authored project with different configurations. Each catalogue records the generation and bindings actually installed in that estate, and Load and Test follow those installed bindings rather than an edited configuration that has not been built.

Mirror can establish a development baseline from another installed estate without adding development-specific names to authored files. Changed work can then become local while unchanged work remains borrowed. See [Logical and physical items](logical-and-physical-items.md), [Mirrors](mirrors.md), [The development cycle](../basics/development-cycle.md) and [workspace configuration reference](../reference/configuration-files/workspace-config.md).
