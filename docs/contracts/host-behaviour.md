# Host-behaviour contract

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

See [Configuration](configuration.md), [Runtime](runtime.md), [Session and workspace helpers](../reference/python/session.md), and [Fabric notebook commands](../reference/cli/fabric-notebook.md).
