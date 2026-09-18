# Sessions and workflows

A Session and a Workflow solve related but different problems. A Session provides shared execution context. A Workflow gives ordinary Weaver commands a repeatable order.

## A Session is shared execution context

Each operation reaches Fabric through a Session. An operation can open one for itself, or several operations can share a Session supplied by the CLI, a workflow or Python code.

Within one workspace, the shared Session can reuse capabilities it has already acquired: authentication, workspace and item resolution, Warehouse connections, OneLake access and Spark execution context. Reuse avoids reacquiring the same remote resources for each command. It does not change what Build, Load, Test or Health means, and it does not merge their selections or state changes.

The host determines how those capabilities are obtained. A desktop process may acquire remote Fabric capabilities; code already running in the target Fabric workspace can use its active context. Livy is one mechanism used when remote Spark execution is needed, not the definition of a Session.

A Session owns only the resources it opened. Supplying an existing Session lets later operations continue to use it after one operation completes.

## A Workflow orders ordinary commands

A Workflow is a named, ordered sequence of Weaver commands. The commands are parsed and run as the same commands available outside a Workflow:

```text
Build → Load → Test → Health
```

Each entry keeps its normal selection, validation, state changes and failure behaviour. Workflow is not a second execution language, and it does not reinterpret the lifecycle.

The sequence runs in one Session and one workspace. Weaver can prepare the combined capabilities needed by the commands before the first entry, then reuse them across the sequence. Load and Test evidence produced during the sequence also shares a workflow identifier, making related outcomes easier to correlate.

## Composition does not create a transaction

Commands still complete one at a time. If a command fails, later commands do not run, but changes made by earlier commands remain. Partial state left by the failing command is governed by that command's own behaviour. A Workflow does not add operation-wide rollback around the sequence.

This makes a Workflow useful for recording an accepted operating sequence, not for hiding the boundaries between its steps. Diagnose and recover the operation that failed, then rerun the appropriate sequence against the state that remains.

See the [Workflow operation reference](../reference/operation-behaviour/workflow.md) for the exact file format and execution rules, and [Session and runtime](../reference/operation-behaviour/session-runtime.md) for capability and host behaviour. [Fault tolerance](fault-tolerance.md) explains failure and partial state across commands.
