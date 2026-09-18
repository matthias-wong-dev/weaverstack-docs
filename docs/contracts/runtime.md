# Runtime contract

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

A returned primitive failure remains a failed node; it is not converted to success because no Python exception escaped. An unhandled authored exception or malformed primitive result also fails that node. Fault tolerance decides what other selected work may still run, as defined by the [Fault-tolerance contract](fault-tolerance.md).

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

See [Load](load.md), [Test](test.md), [Catalogue](catalogue.md), [Python operations](../reference/python/operations.md), and [Session and workspace helpers](../reference/python/session.md).
