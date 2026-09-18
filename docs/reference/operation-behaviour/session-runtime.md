# Session and runtime behaviour

A Session is a reusable execution context. It resolves and acquires capabilities when operations need them, then reuses healthy acquisitions across commands in the same resolved context.

## Workspace binding

`weaver.session()` resolves workspace configuration at construction. Explicit `workspace`, `catalogue` and `environment` values override values read from `workspace_config`; an already resolved `Workspace` cannot be combined with `workspace_config`.

A Session constructed with a workspace keeps that workspace name for its lifetime. A command may name the same workspace and may override catalogue or Environment within it. A command naming another workspace is refused before its operation runs.

The interactive `weaver session` command is the exception: when it starts outside a project and no workspace option is supplied, it opens with no default workspace and requires each command to name or discover one. Resources are then cached under each resolved workspace context. Notebook Sessions always have their attached workspace. A closed Session is refused rather than reopened.

Installed Load and Test targets come from the selected catalogue's installation bindings. A current workspace configuration does not redirect installed work to a different physical item.

## Host position

Session selection depends on where Weaver runs relative to the requested workspace:

| Position | Workspace and execution context |
| --- | --- |
| Desktop or another process outside the requested workspace | Weaver resolves the target through Fabric and acquires remote capabilities for that workspace. |
| Fabric notebook or Livy process addressing its attached workspace | Weaver uses the active Spark session, notebook workspace context, notebook storage and notebook identity. |
| Fabric process addressing a different workspace | Weaver uses the cross-workspace desktop-style path for that target; it does not reuse the notebook's attached Lakehouse, Spark context or identity as though they belonged to the other workspace. |

An attached Fabric Session refuses a different workspace. Host selection does not fall back to local execution when workspace resolution, authentication or a required Fabric capability fails.

## Capability acquisition, reuse and close

Creating a Session resolves configuration but does not resolve Fabric items, start Spark, open Warehouse SQL or publish anything. Operations request authentication, item resolution, OneLake storage, Spark and Warehouse SQL as needed.

A Warehouse-only operation does not start Spark. A command that names only a logical Lakehouse does not choose a Spark attachment until the installed or configured physical target has been resolved. Workflow and interactive-session preparation may start likely acquisitions early, but an unused declared capability is not treated as executed work.

Concurrent requests for one capability share one acquisition. While healthy, resolved items, credentials, storage clients, the Spark session and per-Warehouse SQL connections can be reused by later commands in the Session.

An authored statement failure does not by itself discard a healthy capability. An acquisition or transport/session failure marks that capability failed for the current operation. Weaver does not replace it part-way through that operation. At the next operation task boundary, the Session permits one bounded reacquisition; an exhausted capability remains failed and the operation that next needs it reports the failure.

A standalone operation owns the Session it creates and closes it afterward. A caller-supplied Session is borrowed and remains open. Closing flushes pending catalogue writes, releases only capabilities the Session acquired, waits for an in-progress acquisition for a bounded period, and does not acquire an unused capability merely to close it. Close and cleanup do not roll back completed target or catalogue changes.

## Credentials

The Python API accepts an injected object with the Azure `TokenCredential` shape. Without one, core library use follows `DefaultAzureCredential`; the library does not promise a narrower chain.

The desktop CLI selects, in order, a configured service principal, an existing Azure CLI sign-in, and—only when interaction is allowed—browser sign-in. `--non-interactive` omits browser sign-in. Authentication success does not supply permissions to every workspace, item, SQL endpoint, OneLake path or capacity.

Inside the attached Fabric workspace, notebook identity is used for Fabric and Warehouse access. Desktop credential environment variables are not substituted into that path. A different workspace addressed from a Fabric process must authenticate in its own cross-workspace context.

## Fabric Environment qualification

An unqualified Environment name resolves in the operation's workspace. `Workspace/Environment` may name an Environment owned by another workspace where Fabric permits that attachment. The Spark session still runs in the operation's workspace; qualification changes Environment ownership, not the Session's workspace.

Desktop Python execution requires a configured published Environment containing Weaver. Spark SQL can use Spark without importing Weaver, and Warehouse-only work does not require an Environment merely because other operations support Python. Inside an attached Fabric workspace, the active runtime supplies the Python and Spark environment.

A qualified Environment being attachable does not imply general host parity across workspaces. Notebook utilities, mounted paths, attached Lakehouses, credential flows and item operations remain host- and capability-specific.

## Runtime definition boundary

Ordinary Load and Test execute installed definitions. Editing project source has no runtime effect until Build installs the change. `test --file` is the explicit exception: it compiles and runs one source validation without installing or publishing it.

Lakehouse Python and Spark SQL use Spark; Warehouse work uses the target SQL endpoint. The engines retain their own syntax, types, errors and physical capabilities. A mixed graph may wait for a required Warehouse result to become readable by downstream Lakehouse work; Weaver applies that boundary only where the selected installed graph requires it.
