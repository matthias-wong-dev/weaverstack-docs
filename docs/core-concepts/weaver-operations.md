# Weaver operations

Build, Load and Test connect authored Weaver documents to an operating Fabric estate. They are separate operations over successive states:

```text
Weaver documents
      │
      │ Build
      ▼
installed definitions and work
      │
      │ Load
      ▼
data and recorded load state
      │
      │ Test
      ▼
recorded validation outcomes
```

Health reads and summarises the resulting state. It does not install definitions, run data-producing work or run validations, so it is not a fourth materialising operation.

## Build realises the authored estate

Build is the operation that interprets project source. It reads the selected project documents, applies the selected workspace configuration's physical bindings and uses declared dependencies to determine affected work and order it. It then installs or changes the corresponding definitions and work in the bound Fabric items.

A successful Build records the installed generation in the [Weaver catalogue](catalogue.md). That record connects each logical item and document to the definitions and work that later operations use. Editing a document changes the authored estate; Build is what makes that change part of the installed estate.

Different documents give Build different work:

- **Tables** become stored relations together with any data-producing work declared for them.
- **Folders** become managed file scopes together with their data-producing work.
- **Views** become query-defined relations. Their query is realised by Build rather than run as a separate Load.
- **Tests and Assumptions** become installed validations. Build does not run them.
- **Shortcuts** become installed connections to data elsewhere. They can also place their consumers after the data they expose in Build order.
- **Warehouse programmables** become installed stored procedures. They are installed definitions, not independently loadable documents.
- **Schema metadata** contributes installed schema declarations and descriptions; it has no independent Load or Test step.

Build can therefore affect a document even when that document will never participate in Load or Test.

## Load runs the installed data work

Load starts from the installed generation recorded in the catalogue. It resolves the selected logical items to their installed Fabric targets, runs the installed data-producing work for Tables and Folders, and records the resulting operational state.

Load does not reinterpret project source. If a Table or Folder document has changed since the last Build, Load continues to run the previously installed work. Build the change before expecting Load to use it.

Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata have no independent Load step. They can still affect a Load: an installed View or Shortcut can supply data to loadable work, and dependencies can order selected loadable documents. The operation changes data only through the installed work it runs.

## Test checks the installed estate

Test runs installed Tests and Assumptions against the estate produced by Build and Load. A Test compares expected and actual relations; an Assumption finds rows that contradict a condition. Test records their outcomes in the catalogue.

Test reads estate data but does not install definitions or materialise business data. Changing a Test or Assumption document does not change the installed validation until Build installs the new generation.

## Selection sets the operating boundary

Each operation has a selection of logical items or documents. Build interprets source within its selection; Load and Test select from what the catalogue says is installed. Dependencies determine affected Build work and execution order where applicable, but they do not turn every dependency into an implicit request to operate on another logical item.

[Dependencies](dependencies.md) owns the dependency model, including cross-item relationships and operation-specific selection rules.

## A Session carries operations to Fabric

A Session is the execution context through which an operation reaches Fabric. Build, Load and Test keep the same selection, catalogue and state-change semantics whether Weaver starts on a desktop or already runs inside Fabric.

An operation can open a Session for itself. Several operations can instead use one Session, as they do in the interactive CLI and in a workflow. They then share the resolved workspace and item context, credentials and Fabric execution resources already acquired for that workspace. Closing an operation-created Session releases its resources; a Session supplied by the caller remains open for later operations.

The host changes the path to Fabric, not the operation. On a desktop, the Session acquires remote Fabric capabilities as an operation needs them. Inside the Fabric workspace being addressed, it uses that workspace's active execution context. A notebook addressing another workspace takes the desktop path. Authentication, Spark availability and other host prerequisites can therefore differ even though the project, catalogue and operation mean the same thing.

## A workflow composes ordinary operations

A workflow is an ordered sequence of ordinary Weaver commands run in one Session and one workspace. Each command keeps its normal Build, Load, Test or other operation semantics; the workflow is not another execution engine or a replacement lifecycle.

The shared Session preserves workspace resolution and acquired execution context across the sequence. Recorded Load and Test work from the sequence shares one workflow identifier, which correlates those outcomes without making the sequence transactional. Failure between commands is covered by [Fault tolerance](fault-tolerance.md).

## Health reports the resulting state

Health combines installed declarations, current Load and Test state and, when requested, physical inventory. It reports what Build installed and what later operations recorded; it does not advance the estate through another lifecycle stage.

Exact commands and options belong in [Reference](../reference/index.md). The [Build](../contracts/build.md), [Load](../contracts/load.md), [Test](../contracts/test.md), [Workflow](../contracts/workflow.md), [Selection](../contracts/selection.md), and [State and health](../contracts/state-and-health.md) contracts own the precise operation boundaries. [Runtime](../contracts/runtime.md) and [Host behaviour](../contracts/host-behaviour.md) define where installed work executes. [Signatures and change detection](../contracts/signatures-and-change-detection.md) defines how Build distinguishes installed work from changed and impacted work.
