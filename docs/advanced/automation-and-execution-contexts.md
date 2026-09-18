# Automation and execution contexts


---

## Run Weaver unattended

This guide runs Weaver from a scheduler or build runner without choosing a CI vendor. The example validates a project locally, then runs its Build, Load, Test and Health sequence against Fabric.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) on the runner and confirm `weaver --version` works.
- Give the runner a project and workspace configuration. This documentation repository includes the checked fixture at `examples/parcel-automation/`.
- Authenticate before the job starts. A non-interactive invocation tries a configured Azure service principal, then an existing Azure CLI sign-in. It does not open browser sign-in. For a service principal, configure `AZURE_CLIENT_ID` and `AZURE_TENANT_ID`, plus either `AZURE_CLIENT_SECRET` or `AZURE_CLIENT_CERTIFICATE_PATH`, in the runner's secret store. Do not put credentials in the repository or command line.
- Grant that identity the Fabric and data-plane permissions required by the operations in the job.

Run `weaver doctor --workspace "Parcel Development" --non-interactive --json` in the runner environment when checking authentication and connectivity separately.

## Set the two interaction controls deliberately

`--non-interactive` prevents an invocation from reading standard input, waiting for a keypress, offering a retry or opening browser sign-in. Missing input or authorisation is then an error. It does **not** authorise destructive work.

`--yes` grants authorisation. It does not make an invocation non-interactive, configure credentials or fill missing arguments. An unattended destructive command needs both options:

```bash
weaver wipe Warehouse/ParcelOperationsDev \
  --workspace "Parcel Development" \
  --non-interactive \
  --yes
```

A workflow also requires authorisation before it starts. Pass both options for an unattended workflow even when its listed commands are not individually destructive: `--non-interactive` forbids the confirmation prompt, while `--yes` authorises the displayed sequence and its commands.

## Validate before contacting Fabric

From the fixture directory, run the local parser first:

```bash
cd examples/parcel-automation
mkdir -p .weaver-results
weaver check . \
  --non-interactive \
  --json > .weaver-results/check.json
```

`check` does not contact Fabric. A zero exit status and a JSON document on standard output are the checkpoint. Treat any non-zero status as a failed job and retain standard error with the JSON result directory.

## Run the ordered lifecycle

The fixture's `workflow.yml` contains the whole sequence:

```yaml
workflows:
  verify:
    - weaver check .
    - weaver build . --item Warehouse/Operations --workspace-config workspace-config.yml
    - weaver load Warehouse/Operations --workspace-config workspace-config.yml
    - weaver test Warehouse/Operations --workspace-config workspace-config.yml
    - weaver health --item Warehouse/Operations --workspace-config workspace-config.yml
```

Run it without a terminal:

```bash
weaver workflow verify \
  --file workflow.yml \
  --non-interactive \
  --yes
```

The workflow prints the numbered sequence before execution. It runs the entries in order in one Session and returns non-zero when a command fails. It stops at that command; later entries do not run, and completed work is not rolled back. See [Fault tolerance](../core-concepts/fault-tolerance.md) for the operation-specific failure boundaries.

## Capture machine-readable results

A workflow has no `--json` option. Use its exit status and human log as the run-level record. When automation needs a command's structured result, invoke that command directly with `--json`:

```bash
weaver build . \
  --item Warehouse/Operations \
  --workspace-config workspace-config.yml \
  --non-interactive \
  --json > .weaver-results/build.json

weaver health \
  --item Warehouse/Operations \
  --workspace-config workspace-config.yml \
  --non-interactive \
  --json > .weaver-results/health.json
```

Commands advertise machine-readable output individually. Do not add `--json` to a command whose help does not list it, and do not parse the human renderer as JSON. A report-producing command exits non-zero when its result is unsuccessful; Health exits non-zero for Amber or Red. Preserve standard error separately so an authentication, configuration or parser error is not mistaken for a report.

## Interpret failures

- **The job asks for input or browser sign-in:** the invocation omitted `--non-interactive`, or a wrapper removed it.
- **The job says to pass `--yes`:** authorisation is missing. Add it only after reviewing the exact destructive command or workflow sequence.
- **Credential acquisition fails:** configure a service principal or complete `az login` before the job. `--yes` does not affect authentication.
- **A workflow reports `Workflow stopped at [N]`:** command `N` failed. Inspect that command's error and the [Catalogue](../core-concepts/catalogue.md) or Health state before rerunning. Earlier commands may already have changed Fabric.
- **Local check succeeds but Fabric work fails:** the declarations parsed; the live workspace, permissions or platform operation did not. Local checks are not evidence of a successful Fabric run.

## Next actions

Use [Sessions and workflows](../basics/sessions-and-workflows.md) when the sequence itself needs editing or interactive diagnosis. Use [Promote a bundle](build-bundles-and-controlled-installation.md) to separate Build planning from installation. [Weaver operations](../core-concepts/build-load-and-test.md), the [Development cycle](../basics/development-cycle.md), the [CLI reference](../reference/cli.md) and [Contracts](../reference/operation-behaviour/index.md) define the adjacent lifecycle and command boundaries.

---

## Runtime contract

The Weaver runtime executes work from one resolved workspace, catalogue and installed target context. Project discovery establishes declarations; Build installs executable definitions; Load and Test run those installed definitions except for the explicit source-file Test mode.

## When authored work executes

Check and project discovery read Python statically and parse supported SQL forms. They do not import authored Python or run a data load or validation.

Build does not call authored Python `read()`, `expected()` or `actual()` methods. It can submit SQL needed to establish and install a SQL definition, including obtaining a Table's result shape when no schema was declared. That Build-time work establishes installable structure; it is not a successful Load or Test and publishes no such outcome.

Load executes installed data work:

- an installed Lakehouse Python Table or Folder imports its deployed module and calls its load implementation;
- an installed Spark SQL Table executes through the generated runtime definition installed for that document;
- an installed Warehouse Table executes its installed load procedure;
- a View has no independent authored Load method.

Test executes installed Test and Assumption definitions. `test --file`, or `file=` in Python, is the exception: it compiles and executes the selected source validation for one installed target without installing or publishing it as estate state.

A source edit does not change Load or installed Test behaviour until Build installs a new definition. Runtime execution does not reopen the project to choose between source and installed code.

## Session, catalogue and target context

Every remote operation runs through one Session. A caller-supplied Session is borrowed and remains open; an operation-created Session closes when the operation finishes. A closed Session is rejected rather than reopened.

A Session fixes one Fabric workspace. The operation may select a catalogue and Environment within that workspace, but it cannot move the Session to another workspace. Catalogue-backed execution resolves logical items and installed objects from the selected catalogue. The recorded installation binding decides the physical target; current workspace configuration does not redirect an installed Load or Test.

An installed Lakehouse object receives:

- the Spark session selected for the operation;
- the resolved physical Lakehouse for its installed item;
- the installed logical identity and selected catalogue context when recording is required.

Objects created by authored Python from another runtime object inherit its Spark, Lakehouse and catalogue context. Warehouse work executes against the resolved installed Warehouse. A command without the Session capability required by its installed work fails rather than executing in an unrelated local context.

## Installed Python scope

Deployed Python modules are resolved from the installed runtime tree for one logical item and physical target. Modules deployed together can import their own supporting `lib/` and object modules. Identically named modules in another item or target remain separate.

One run may reuse modules from the same installed tree. The import scope closes at the end of the run so a later run imports the definition left by the latest Build. A failed import, missing deployed module or missing declared class fails that runtime node and identifies the installed definition that must be rebuilt.

This isolation is runtime behaviour, not a public package layout. The generated package names, import finder and installed directory structure are not application APIs.

## Spark and Warehouse execution boundaries

Lakehouse Python and Spark SQL work requires Spark in the target workspace. Warehouse data work executes through the Warehouse SQL endpoint and does not require Spark merely because the operation also supports Lakehouses.

A mixed installed graph can require an explicit readiness boundary between Warehouse production and a downstream Lakehouse read. Weaver waits only where the installed graph requires that publication. If the Warehouse load moved no rows, there is nothing new to publish. If new data cannot become readable before the boundary settles, the dependent runtime work fails rather than reading a result that Weaver has not established as ready.

The runtime does not imply engine parity. Spark SQL and Warehouse T-SQL retain their own syntax, type systems, execution errors and physical capabilities.

## Result publication

Runtime work produces an operation result in Weaver's public outcome vocabulary. Load and installed Test settle each selected node before the operation completes. Required current status, history and bookmark writes are flushed before a completed report is returned or an intolerant failure is raised.

A returned primitive failure remains a failed node; it is not converted to success because no Python exception escaped. An unhandled authored exception or malformed primitive result also fails that node. Fault tolerance decides what other selected work may still run, as defined by the [Fault-tolerance contract](../reference/operation-behaviour/fault-and-outcome-vocabulary.md).

Targeted Test diagnostics belong to the invocation result. They are not durable catalogue evidence. Source-file Test and dry-run modes publish no installed runtime state.

## Cleanup and failure

An operation closes only capabilities it created. A supplied Session and its healthy reusable capabilities remain available to the caller. Session close releases acquired capabilities; capabilities never acquired are not started merely to close them.

A runtime import scope is released after its run. Failure to release a still-live remote scope is reported without replacing the already settled operation outcome; the affected session should not be used for rebuilt Python until it has been restarted. An interpreter that has already ended needs no further cleanup.

Cleanup does not roll back target changes or catalogue evidence already committed. Recovery starts from the remaining installed and runtime state under the owning operation's contract.

## Defined behaviour

The Runtime contract specifies that Weaver:

1. does not execute authored Python during Check, discovery or Build;
2. runs installed definitions for Load and ordinary Test, with source-file Test as the explicit non-installed mode;
3. resolves runtime work through one Session, workspace, catalogue and installed physical binding;
4. isolates deployed Python by installed item and target within a run and releases that scope before a later run;
5. keeps Spark execution and Warehouse SQL execution as distinct target capabilities;
6. waits for cross-engine publication only where selected dependency work requires it;
7. settles runtime outcomes and required catalogue writes before reporting completion; and
8. releases operation-owned capabilities without closing a borrowed Session or rolling back completed effects.

See [Load](../reference/operation-behaviour/load.md), [Test](../reference/operation-behaviour/test.md), [Catalogue](../reference/catalogue-schema.md), [Python operations](../reference/python/operations.md), and [Session and workspace helpers](../reference/python/session.md).

---

## Host-behaviour contract

Weaver exposes the same lifecycle operations from a desktop process and from Python running in a Fabric notebook, but the host determines where execution capabilities and credentials come from. A Session selects that host behaviour for one workspace.

## Desktop execution

Outside the Fabric workspace being addressed, Weaver uses a desktop Session. It resolves the workspace through Fabric APIs and acquires capabilities only when an operation needs them.

- Fabric control-plane and OneLake access use the selected desktop credential context.
- Warehouse work uses the target Warehouse SQL endpoint.
- Lakehouse Python or Spark SQL work requires a published Fabric Environment and a remote Spark session in the target workspace.
- A Warehouse-only operation does not start Spark solely because other Weaver operations can use it.

A Session can reuse healthy acquired capabilities across commands. Concurrent requests for the same capability share one acquisition. A failed authored statement does not by itself discard a healthy session; an acquisition or session failure can mark that capability for a bounded reacquisition before a later operation.

## Execution inside the attached Fabric workspace

When Weaver is running in a Fabric notebook and the requested workspace is the notebook's current workspace, it uses the notebook host:

- the active Spark session supplies Spark execution;
- notebook runtime context supplies the attached workspace;
- notebook identity supplies Fabric and Warehouse authentication;
- notebook storage and item resolution are used for that workspace.

Desktop credentials are not substituted into this in-workspace path. An injected client or Session remains authoritative when the public operation accepts one.

The notebook Session is attached to one physical workspace. It refuses a request to execute against another workspace rather than applying the attached Spark session or notebook identity to that target.

## Cross-workspace requests from a notebook process

Running inside Fabric does not make every workspace an in-workspace target. When the requested workspace differs from the notebook's current workspace, host selection uses the cross-workspace Session path rather than the attached notebook Session.

That path must independently resolve and authenticate to the target workspace and acquire any remote Spark, Warehouse or storage capability the operation requires. It does not reuse the notebook's attached Lakehouse as the target, and logical item names do not become Spark attachments.

A qualified Fabric Environment may be owned by another workspace when Fabric accepts that attachment. The Spark session still runs in the consumer workspace named by the operation. Cross-workspace Environment access therefore requires both the consumer workspace context and access to the qualified Environment; an unqualified Environment name is resolved in the selected workspace.

Cross-workspace support is capability-specific. A supported Environment attachment does not imply that every notebook utility, mounted path, credential flow or item operation behaves as though both workspaces were one host.

## Context and capability acquisition

Constructing a Session resolves configuration and workspace context but does not by itself start Spark, open Warehouse SQL or resolve every item. Operations declare the capabilities they need, and the Session acquires them on demand.

A lifecycle sequence may acquire its known capabilities and attach required Lakehouses before its first command. Preparation changes startup timing, not selection or authority: the catalogue still supplies the installed target context, each operation keeps its own write boundary and one Session still belongs to one workspace.

Capability cleanup follows ownership. An operation-created Session closes after the operation. A supplied Session remains open. Closing releases capabilities that were acquired and does not acquire unused capabilities for the sake of releasing them.

## Supported differences

The shared Session contract covers Python execution, Spark SQL batches, Warehouse SQL, Delta Table creation and host-position reporting. Equal call shape does not mean equal mechanism or universal host parity.

| Behaviour | Desktop | Attached Fabric workspace | Different workspace from a notebook process |
| --- | --- | --- | --- |
| Workspace context | Explicit or configured target workspace | Current notebook workspace | Explicit or configured target workspace |
| Spark | Acquired remotely when required | Active notebook Spark session | Acquired for the target workspace when required |
| Warehouse SQL | Target SQL endpoint with desktop credential context | Target SQL endpoint with notebook identity | Target SQL endpoint under the cross-workspace Session context |
| Browser sign-in | May be available in interactive mode | Not used for the attached notebook path | Depends on the selected cross-workspace Session and interaction policy |
| Workspace change inside one Session | Not supported | Not supported | Not supported |
| Attached Lakehouse | Not implicit | Available to the notebook host | Not reused as the target workspace's Lakehouse |

Commands and operations must fail when the selected host cannot supply a required capability. They must not fall back to local execution merely because remote workspace resolution, authentication or resource acquisition failed.

## Evidence boundary

Source and automated tests define Session selection, same-workspace refusal, credential separation, lazy acquisition, capability signatures and cleanup. Hosted tests also exercise deployed Python dispatch and a qualified cross-workspace Environment against configured Fabric test estates.

Those checkpoints do not make live Fabric state part of this contract. Capacity availability, tenant policy, workspace permissions, Environment publication, item existence and service-side timing are established only by the workspace where an operation runs. No live Fabric operation was performed to author this page, and this contract does not claim an observed outcome for an arbitrary tenant or workspace.

## Defined behaviour

The Host-behaviour contract specifies that Weaver:

1. selects an attached notebook Session only for the Fabric workspace the process is currently running in;
2. uses notebook context and identity in that attached workspace without constructing desktop credentials for it;
3. uses the cross-workspace Session path when a notebook process addresses another workspace;
4. fixes each Session to one workspace and refuses a workspace switch;
5. acquires Spark, Warehouse SQL, storage and resolution capabilities only when required;
6. does not start Spark for work whose resolved requirements do not include it;
7. shares healthy resources within a Session and releases only acquired, owned resources; and
8. reports unsupported or unavailable host capabilities instead of changing the execution target.

See [Configuration](../reference/configuration-files/workspace-config.md), [Runtime](../reference/operation-behaviour/session-runtime.md), [Session and workspace helpers](../reference/python/session.md), and [Fabric notebook commands](../reference/cli/fabric-notebook.md).
