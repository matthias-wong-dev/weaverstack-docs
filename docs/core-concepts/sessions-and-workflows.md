# Sessions and workflows


---

## Weaver operations

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

Exact commands and options belong in [Reference](../reference/index.md). The [Build](../reference/operation-behaviour/build.md), [Load](../reference/operation-behaviour/load.md), [Test](../reference/operation-behaviour/test.md), [Workflow](../reference/operation-behaviour/workflow.md), [Selection](../reference/operation-behaviour/shared-selection-and-identity.md), and [State and health](../reference/operation-behaviour/health.md) contracts own the precise operation boundaries. [Runtime](../reference/operation-behaviour/session-runtime.md) and [Host behaviour](../reference/operation-behaviour/session-runtime.md) define where installed work executes. [Signatures and change detection](../advanced/incremental-build-selection.md) defines how Build distinguishes installed work from changed and impacted work.

---

## Workflow contract

A Workflow is a named sequence of Weaver CLI commands. It composes existing commands in one Session and workspace; it does not introduce a second operation language or a transaction around the sequence.

## Workflow file

The default file is `./workflow.yml`. `--file PATH` selects another YAML file. The document must contain a top-level `workflows` mapping, and the requested name must map to a non-empty list of strings:

```yaml
workflows:
  refresh:
    - build ./parcel --item Warehouse/Operations
    - load Warehouse/Operations
    - test Warehouse/Operations
```

Each string is one ordinary Weaver command line. A leading `weaver` is optional, and quoted arguments are preserved:

```yaml
workflows:
  refresh:
    - weaver build . --workspace-config "parcel development.yml"
```

Every entry is parsed by the normal Weaver command parser before anything runs. An invalid command or option fails the Workflow before its first entry.

A Workflow is not a shell. Pipes, redirection, command substitution, environment expansion, command chaining and non-Weaver programs are rejected. `session` is excluded because the Workflow already owns a Session, and `workflow` is excluded so Workflows cannot nest.

## Shared workspace and Session

Every entry runs in one Session and one Fabric workspace. Outer `--workspace`, `--workspace-config`, `--catalogue` and `--environment` values provide defaults inherited by entries that do not set them. An entry may resolve to the same workspace configuration, but entries cannot select different workspaces.

If the caller supplies an open Session, the Workflow joins it and leaves it open. Otherwise the Workflow opens one Session for the complete sequence. Entries share one workflow identifier, which correlates catalogue evidence produced by Load and Test.

The Workflow prepares the union of capabilities and known Lakehouse attachments required by its entries before running the first command. This reuse does not alter the individual operation contracts or permit an entry to move to another workspace.

## Validation, display and confirmation

Weaver loads the named sequence, parses every entry and resolves the shared workspace before displaying or executing it. It displays the workflow file and the complete numbered sequence.

Without `--yes`, an interactive invocation asks once whether to execute that displayed sequence. Declining runs nothing and is not an execution failure. If confirmation is required but no prompt is available, the Workflow fails and names `--yes` as the required action.

Confirmation authorises the complete displayed sequence, including destructive entries, so individual commands do not ask again. `--non-interactive` is inherited by every entry and can only make interaction stricter; it prevents input, keypress waits and browser sign-in but does not imply approval. Unattended execution therefore requires `--non-interactive --yes`.

## Ordered execution and failure

Entries run in file order with their ordinary parsed arguments. The Workflow stops at the first entry that returns a failure status or raises a Weaver error. The failing entry is reported, and later entries do not run.

A Workflow is not transactional. State changed by completed entries, and partial state left by the failing entry under that operation's own contract, remains in place. Weaver does not roll earlier Build, Load, Test, Mirror or Wipe effects back when a later entry fails. Recovery is the recovery procedure for the operation that failed, followed by rerunning an appropriate sequence.

Each entry retains its own selection, dry-run, fault-tolerance, strictness, confirmation and result semantics. Workflow composition changes only Session reuse, shared workspace resolution, one-time confirmation, correlation and stop-on-first-failure behaviour.

## Outcome

A Workflow succeeds only when every entry succeeds. It reports the number of completed commands. On failure it identifies the first unsuccessful entry and returns a non-zero status. `--timings` reports Session timings after either success or failure.

A user who declines an available confirmation receives a zero status because no execution was attempted. Missing non-interactive authorisation is a failure and returns non-zero.

## Defined behaviour

The Workflow contract specifies that Workflow:

1. reads one named, non-empty sequence from the selected YAML file;
2. accepts ordinary Weaver command lines and rejects shell language and nested sessions or Workflows;
3. parses every entry and resolves one shared workspace before execution;
4. runs entries in file order through one supplied or managed Session;
5. applies outer interaction and workspace values as inherited defaults without allowing a workspace change;
6. displays and confirms the complete sequence once;
7. stops at the first failed status or Weaver error; and
8. leaves completed and partial operation state in place rather than rolling the sequence back.

See [`weaver workflow`](../reference/cli/workflow.md), [Session and workspace helpers](../reference/python/session.md), and the contracts for each command placed in the sequence.
