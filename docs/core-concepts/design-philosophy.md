# Design philosophy

Weaver is shaped around the distinction between what a project declares, what Build installs and what later operations do. These are architectural choices, not styling preferences. They decide whether the estate remains understandable when it spans engines, environments and failed runs.

## Natural authoring

> **Use SQL and Python as SQL and Python. What you write should still make sense to the engine and to another engineer.**

A SQL body should not need a templating engine to turn macros into the statement Fabric eventually sees. In a Weaver document, the authored body remains T-SQL or Spark SQL; the declaration sits in a comment that the SQL engine already understands. Python remains a module with classes and imports, not another language encoded inside configuration.

Weaver adds the information the lifecycle genuinely needs: a logical identity such as `Parcel.Event`, the owning item and a small amount of metadata. It does not need a second naming system to disguise relation names, or a parallel graph that repeats relationships already present in code.

Consequences:

- Python imports and SQL relation references supply dependencies where inference is supported.
- Spark SQL Tables and Views still require an explicit `Dependencies` field, including `Dependencies: []` when no managed dependency exists.
- An explicit `Dependencies` field replaces inference rather than extending it.
- `Lineage`, foreign keys and other descriptive references describe the estate; they do not create execution dependencies.
- Physical workspace, Lakehouse and Warehouse names stay in workspace configuration rather than leaking into authored logic.

See [Weaver documents](weaver-documents.md), [Dependencies](dependencies.md) and [Common metadata](../reference/weaver-documents/common-metadata.md) for the authoring rules.

## Declaration and execution are separate

> **Build defines the installed estate. Load and Test operate it. Installing code is not the same job as running data.**

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

Build interprets project source, resolves its physical bindings and installs definitions and executable work. Load and Test then use that installed generation from the catalogue; they do not reinterpret whichever files happen to be on disk when a run begins. Editing source changes the intended estate, but the operating estate changes only after Build installs a new generation.

That boundary is what makes frozen Build bundles, repeatable runtime work and inspection of the installed generation possible. It also keeps failures honest: a Build failure, a failed Load and a failed validation are different events with different remaining state, not one vague project failure. [Build, Load and Test](build-load-and-test.md) owns the lifecycle model; [operation behaviour](../reference/operation-behaviour/index.md) defines each boundary precisely.

## Reconcile change rather than recreate the estate

> **Rebuilding everything is not a change strategy. Compare desired, installed and operational state, then act on the difference.**

Build compares authored declarations, catalogue certification and physical inventory. Signatures identify changed definitions; managed dependencies identify affected descendants within the selected items; unchanged installed definitions remain in place. Load uses bookmarks and current health to select or process outstanding data work.

Development follows the same rule. A code branch should not require another full copy and reload of production data before useful work can begin. Mirror forks the installed catalogue and can present unchanged source data through OneLake shortcuts and Warehouse views. Changed or affected objects become local when Build installs them; the rest can remain borrowed. Code and data can therefore branch together without duplicating the whole estate.

This principle is not a universal “incremental” slogan. `Incremental` has specific Table and Folder meanings, with document-specific defaults. Rebuilding loadable work resets its current Load state and bookmark, and reload explicitly reconstructs selected Tables. Re-mirroring is also a deliberate reset: it reconstructs the selected destination boundary from a new source baseline rather than refreshing around local work.

The detailed mechanisms are [incremental Build selection](../advanced/incremental-build-selection.md), [incremental data processing](../advanced/incremental-data-processing.md) and [Mirror and materialisation strategies](../advanced/mirror-and-materialisation-strategies.md).

## Fabric-native by construction

> **Fabric should execute Fabric work. A permanent external runtime should not become part of the estate merely because it initiated the run.**

Build installs executable work into Fabric: Warehouse relations and procedures, Lakehouse runtime modules and generated runtime primitives for Spark SQL-authored work. Load and Test execute that installed work against the catalogue and physical items. A desktop process can orchestrate Fabric remotely; Python already running in the target workspace can use the host's active context. In both cases, the executable estate and its recorded state live in Fabric rather than in a desktop process or separate hosted service that must remain alive.

Notebook support is therefore a consequence, not the principle itself. The same project can be built and operated inside Fabric because Weaver does not make an external process the hidden owner of project meaning or runtime state. The available capabilities and invocation form still depend on the host; not every CLI helper has an identical Python or notebook counterpart.

[Portable execution between desktop and Fabric](../advanced/portable-execution-between-desktop-and-fabric.md) covers the supported paths and their qualifications. [Automation and execution contexts](../advanced/automation-and-execution-contexts.md) defines how Sessions obtain Fabric capabilities.

## Operational state is data

> **Operational state is queryable data. Logs are evidence, not the estate's memory.**

A run log alone cannot say which generation is installed, where an incremental read resumes, whether a validation is stale or which objects still borrow source data. A detached manifest can describe what a tool compiled, but it cannot by itself prove what is installed now or what happened after installation. Weaver records those facts in the estate's catalogue, alongside execution history and row movement. Workflow identifiers correlate related work, and Health turns installed, operational and optional physical evidence into a current estate view.

`_.Installation`, `_.Registry` and `_.Dependency` describe installed state. `_.Bookmark`, `_.LoadStatus` and `_.TestStatus` describe current operation state. `_.Log` and `_.LoadStatistic` retain operation history. `_.Mirror` identifies borrowed objects. Managed row-audit datetimes describe the lifecycle state of stored rows.

The state remains available after the process that produced it has ended, including when the result is partial. See [Catalogue](catalogue.md), [State and health](state-and-health.md), [Row auditing and operational history](../advanced/row-auditing-and-operational-history.md) and the [catalogue schema reference](../reference/catalogue-schema.md).

## Failure is local

> **A large estate is not one atomic transaction. Fail the affected work, record what was blocked and preserve what completed.**

Failure policy is operation-specific. A fault-tolerant Load can continue independent selected work after one node fails, while blocked work records that a required boundary was not established. Test records each validation outcome. Build stops later installation barriers when their prerequisites fail. Completed work and its evidence remain visible rather than being hidden behind an operation-wide success flag or an imaginary rollback.

Build, Load, Test and Workflow have no operation-wide rollback. Recovery starts from the actual installed, data and catalogue state left behind; it is a new operation, not the continuation of a hidden transaction. [Fault tolerance](fault-tolerance.md) explains the model, and [fault and outcome vocabulary](../reference/operation-behaviour/fault-and-outcome-vocabulary.md) defines the exact outcomes and barriers.

## One project, many estates

> **Development and production are physical bindings, not forks of the logical project.**

Logical item and document identities remain stable while workspace configuration supplies a workspace, catalogue and physical targets. Environment names and deployment-specific Fabric item names do not belong in the SQL and Python merely because the project moves. Each catalogue records the generation and bindings actually installed in that estate, and Load and Test follow those installed bindings rather than an edited configuration that has not been built.

Mirror can establish a development baseline from another installed estate without adding development-specific names to authored files. Changed work can then become local while unchanged work remains borrowed. See [Logical and physical items](logical-and-physical-items.md), [Mirrors](mirrors.md), [The development cycle](../basics/development-cycle.md) and [workspace configuration reference](../reference/configuration-files/workspace-config.md).
