# Fault tolerance

Fault tolerance controls what Weaver attempts after part of an operation fails. It does not make failed work successful, erase completed work or turn an operation into a transaction.

The useful distinction is between three kinds of remaining work:

- **blocked work** cannot proceed because required upstream work did not establish usable state;
- **independent work** does not depend on the failure and may still be able to run;
- **pending work** was otherwise runnable but was not started after fail-fast execution stopped scheduling new work.

These distinctions describe the state left by an operation, not just its terminal message.

> **Design background:** [The fault-tolerance principle](https://principlesofdataengineering.org/docs/quality-reliability/fault-tolerance/) treats containment as preserving usable work while surfacing failures clearly. Weaver represents that containment through blocked, independent, pending, failed and completed states rather than treating a mixed result as success.

## Fail-fast and fault-tolerant execution

Fail-fast execution stops scheduling otherwise-ready work after the first execution failure. Work downstream of an unsatisfied dependency is blocked; unrelated work that has not started remains pending.

A fault-tolerant Load keeps scheduling work after a failure. Independent branches can complete, and settled execution failures do not by themselves prevent later selected work from being attempted. Work that could not be resolved or validated before execution still blocks its descendants. Fault tolerance therefore increases the amount of useful work attempted; it does not remove dependency or validity boundaries.

The final operation still reports the failure. A run in which some work succeeded and some failed or was blocked leaves partial state rather than being converted into success.

Fault tolerance also applies within supported Table and Folder loads when incoming rows or files can be rejected while accepted input is published. That is separate from graph continuation: a target-invalidating change or another non-recoverable condition can still fail the individual load. The [Load reference](../reference/operation-behaviour/load.md) defines the exact distinction.

## Policies belong to operations

Build, Load and Test do not share one universal failure policy.

Build does not offer Load's fault-tolerant execution mode. Installation work completed before a Build failure can remain physically applied, while unsuccessful installation is not certified as a successful generation.

Test attempts the installed validations in its selection and records each result. A failed validation is a finding about the data; a validation that could not run is a different condition. One validation does not produce data needed by another, so Test does not use Load's dependency continuation policy.

A Workflow adds another boundary. It stops at the first command that fails even when that command used fault-tolerant execution internally. Commands completed earlier in the Workflow remain applied.

## Partial state and recovery

Weaver does not apply operation-wide rollback to Build, Load, Test or Workflow execution. Completed work remains completed, and a failing unit can leave operation-specific partial effects. Recorded outcomes and Health show what was established, failed, blocked or left stale.

Recovery is a new operation against that remaining state. Correct the source or platform condition, inspect the affected estate, then rerun the appropriate Build, Load or Test. A retry does not resume an invisible transaction; it reconciles or executes from the state now present.

This is why failure policy must be considered together with selection. A broad fault-tolerant Load can preserve progress on unrelated branches, while a narrow rerun can target recovery after the cause is fixed.

See [Fault and outcome vocabulary](../reference/operation-behaviour/fault-and-outcome-vocabulary.md) for exact outcomes and operation-specific barriers. The [Build](../reference/operation-behaviour/build.md), [Load](../reference/operation-behaviour/load.md), [Test](../reference/operation-behaviour/test.md) and [Workflow](../reference/operation-behaviour/workflow.md) references define their precise failure behaviour.
