# Automation and execution contexts

Automation must make three choices explicit: where Weaver runs, how that process authenticates without unexpected interaction, and which command result is the machine interface. A command line that works at an interactive desktop does not by itself define an unattended job.

## The host supplies the execution context

Weaver exposes the same lifecycle operations from a desktop process and from Python running inside Fabric, but the host supplies different capabilities.

| Context | Workspace and identity | Spark and data access |
| --- | --- | --- |
| Desktop or external runner | Resolves the configured Fabric workspace and uses the desktop credential chain. | Uses Fabric APIs, OneLake and Warehouse SQL endpoints. Lakehouse Python or Spark SQL work acquires a remote Spark session in the target workspace. Python work requires a published Environment containing Weaver; Spark SQL can use the workspace's default Spark runtime. |
| Fabric process addressing its attached workspace | Uses the notebook's current workspace and notebook identity. | Uses the active Spark session, notebook storage context and Fabric-hosted item resolution. Desktop credentials are not substituted. |
| Fabric process addressing another workspace | Uses the cross-workspace Session path and authenticates to the requested workspace independently. | Acquires capabilities for that target workspace; it does not reuse the notebook's attached Lakehouse or identity as though the workspaces were one host. |

A Session belongs to one physical workspace. It is not moved to another workspace between commands. If the selected host cannot supply a required capability, the operation fails rather than falling back to local execution or silently changing target.

Fabric availability remains an execution boundary. Capacity state, workspace permissions, Environment publication, item existence and service-side timing are properties of the workspace at run time; a local Check or successful plan does not establish them.

## Sessions reuse acquired capabilities

Each remote operation runs through a Session. A standalone operation creates a Session and closes it afterward. An interactive session, workflow or Python caller can supply one Session to several operations; the caller-owned Session remains open.

Capabilities are acquired from the host only when required. A Warehouse-only operation does not start Spark merely because other operations support Lakehouses. When a command needs Spark, Warehouse SQL, storage or item resolution, the Session acquires that capability and can reuse the healthy instance for later commands in the same workspace. Concurrent requests for the same capability share one acquisition.

A failed authored statement does not by itself discard a healthy capability. A capability or remote-session failure can make that resource unavailable for the failed operation; a later operation may perform a bounded reacquisition. Closing the Session releases capabilities it acquired and does not start unused capabilities merely to close them.

Workflows reuse one Session and can prepare their combined known capabilities before the first command. This changes startup timing, not command selection, authority or failure behaviour. Each command retains its own state boundary, and the workflow stops when one command fails. See [Sessions and workflows](../core-concepts/sessions-and-workflows.md).

## Make unattended policy explicit

Non-interactive policy and destructive authorisation are separate controls.

- Non-interactive execution forbids reading standard input, waiting for keypresses and opening browser sign-in. Missing input or authorisation becomes an error.
- Destructive authorisation approves the destinations or sequence already settled by the command. It does not configure credentials or make the process non-interactive.

An unattended job that may empty or reconstruct state needs both the non-interactive policy and explicit destructive authorisation. Keep the workspace configuration, item selection and artifact identity under change control so the authorised scope is the scope the job resolves.

A workflow requires sequence authorisation before it starts. That one authorisation is propagated to its entries, while the non-interactive policy can only become stricter inside the sequence. Completed commands remain applied if a later command fails.

The [CLI reference](../reference/cli.md) identifies which commands expose each control and which operations are destructive.

## Supply credentials before the job starts

For desktop execution, Weaver's CLI credential chain tries a configured service principal, then an existing Azure CLI sign-in. Interactive execution can also use browser sign-in. Non-interactive execution omits the browser path.

Store service-principal secrets or certificate material in the runner's secret store, not in project files, workflow definitions, command arguments or bundles. The identity also needs the Fabric control-plane, SQL and OneLake permissions required by the selected operations. Authentication success does not imply permission to every target capability.

Inside the attached Fabric workspace, notebook identity is the host credential. Supplying desktop credential environment variables does not replace that identity for the attached-workspace path. A request from a Fabric process to another workspace uses the independently authenticated cross-workspace context instead.

Use Doctor in the same runner and interaction mode to separate credential and connectivity failures from lifecycle failures. See [Session and runtime behaviour](../reference/operation-behaviour/session-runtime.md) for credential selection and host boundaries.

## Treat machine-readable output as the automation interface

For a command that advertises machine-readable output, use that output and the process status together:

1. capture standard output as the command-specific result document;
2. retain standard error separately for authentication, configuration and host diagnostics;
3. fail the job on a non-zero process status; and
4. validate the fields the automation consumes rather than parsing the human renderer.

There is no single JSON schema shared by every Weaver command, and not every command exposes JSON output. A workflow provides ordered command execution and a process status, not a universal structured envelope for all nested results. When automation needs one operation's structured report, invoke that operation through its advertised machine interface.

Do not infer long-term compatibility from an unversioned result document. The [Machine-readable interfaces](../reference/machine-readable-output.md) page records the exact command fields, stream behaviour and current exit conditions.
