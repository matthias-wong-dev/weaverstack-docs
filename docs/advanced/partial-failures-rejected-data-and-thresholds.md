# Partial failures, rejected data and stability thresholds


---

## Fault-tolerance contract

Fault tolerance controls how much selected work is attempted after a failure. It does not change a failed outcome, retry work, widen selection, undo completed changes or make an operation transactional.

Failure barriers differ by operation. A continuation rule for Load does not apply to Build, Test or a workflow.

## Build barriers

Build has no fault-tolerant mode. Installation is divided by ordered barriers. When an action fails, that sequence fails, every planned action receives a reported outcome and later installation work is skipped. Catalogue certification that depends on failed physical work is not published as successful.

Actions completed before the barrier remain applied. Build does not roll them back as one operation. A later Build reads the project, catalogue and inventory again and reconciles the state it finds; it does not resume the earlier report.

A Build result reports failure and preserves its per-action evidence. Preflight failures that occur before installation runs leave the plan unexecuted rather than producing successful action outcomes.

## Load barriers

An item-wide Load uses the installed dependency graph. There are two distinct kinds of upstream problem.

A **resolved execution failure** occurs after Weaver resolved the node and attempted its installed work. Without fault tolerance, the first such failure stops later scheduling, blocks its dependants and leaves otherwise independent nodes that were not reached pending. With fault tolerance:

- independent selected branches continue; and
- a selected dependant may run after the failed upstream node has settled.

The dependant reads the state left by that failed execution. The upstream node is not treated as successful.

An **unresolved or invalid node** cannot be dispatched as valid installed work. Its descendants remain blocked under either policy. Fault tolerance still permits unrelated valid branches to run. A dependency cycle is invalid before this continuation rule can apply.

Name selection remains an override: it contains only the named installed objects and has no dependency expansion or dependency ordering to continue through.

The final report retains failed, blocked and pending outcomes. Fault tolerance can therefore produce more completed work, but a mixed report is still partially successful and exits non-zero. When no requested branch completes, or fail-fast stops the run, the run fails.

## Rejected input and invalid target state

For a Table or Folder, fault tolerance also controls recoverable incoming-row or incoming-file rejection. Without it, rejected input stops that object's load before the target is modified through the reconciliation path. With it, rejected input is excluded and accepted input can be published; the result records rejects and does not advance the bookmark.

Fault tolerance does not permit a change that would leave a declared unique key invalid. It also does not waive a stability threshold. Those conditions fail the object without applying the proposed target change through that path. A separate explicit threshold waiver applies only to the Table load that receives it.

## Test barriers

An installed Test run evaluates every selected Test and Assumption. A failed validation is a completed finding; a validation that cannot run is an invalid outcome. Neither blocks another selected validation because validations are independent consumers, not a producer chain.

Test therefore uses continuation internally but exposes no Load fault-tolerance switch. A one-file source Test has one selected validation and publishes no installed-estate status or history.

## Workflow barriers

A workflow parses and settles its sequence before execution, then runs commands in file order. It stops at the first command that returns failure or raises a Weaver error. Later commands do not run.

Fault tolerance remains local to a nested Load. If that Load finishes with a failed or partially successful report, the workflow stops even though the Load attempted additional branches. Commands completed earlier in the workflow remain applied.

An interactive Session has a different boundary: a failed command returns to its prompt, allowing a later command to be issued as a new operation. If an acquired execution capability fails, Weaver does not replace it part-way through the failed operation; a later operation may attempt to reacquire it.

## Recording partial work

Build reports each planned installation action as succeeded, failed or skipped. Load and installed Test runs record settled node outcomes with their workflow identifier. A blocked Load records current status and log evidence but no Load statistic because no data work ran. Bookmarks advance only for clean successful loads.

A workflow shares one workflow identifier across recorded Load and Test work that actually ran. The failed command and earlier commands can therefore be correlated; later commands have no outcomes because they were not executed.

No operation in this contract retries failed work automatically. A later attempt is a new operation against the state left behind.

## Defined behaviour

The Fault-tolerance contract specifies that Weaver:

1. stops Build at its installation barrier and skips later planned work;
2. stops ordinary Load scheduling after an execution failure while reporting every planned node;
3. lets fault-tolerant Load continue independent work and descendants of settled execution failures;
4. keeps descendants of unresolved or invalid Load work blocked;
5. keeps row-rejection continuation separate from target-validity and stability checks;
6. evaluates selected validations independently;
7. stops a workflow after its first unsuccessful command; and
8. preserves completed effects and evidence without operation-wide rollback or automatic retry.

---

## Load contract

Load executes the installed data work owned by selected Weaver items. It reads installed definitions, bindings, dependencies and current state from the catalogue; it does not read or reinterpret project source.

## Item and name selection

A Load may select logical items, installed objects by name, or every installed item:

```bash
weaver load Lakehouse/Landing Warehouse/Operations
weaver load Lakehouse/Landing --name Tables/Parcel.Status
weaver load
```

Item selection is a hard execution boundary:

- naming no item selects every item recorded in `_.Installation`;
- naming an item selects the loadable Tables and Folders that item owns;
- a dependency does not add an unnamed item to the run;
- a missing item installation is an error rather than an empty selection.

`--name` is repeatable and selects exact installed objects inside the item boundary. A Lakehouse name may include its area, such as `Tables/Parcel.Status` or `Files/Parcel.Events`; a bare `Schema.Object` is accepted only where it identifies one object. A Warehouse name is `Schema.Object`.

Name selection is an operator override. It runs only the named objects, without adding dependencies or dependency ordering between the names.

## Installed graph and ordering

An item-wide Load uses the installed dependency graph. Selected upstream load work precedes selected downstream work. Dependencies outside the item boundary may explain an installed relationship but do not widen the run.

Selection can omit an intermediate loadable, as `--stale` may do. Where two selected objects remain connected through omitted installed work, their ordering relationship is retained. Weaver also includes the required publication or endpoint readiness between selected Lakehouse and Warehouse work where the installed graph requires it.

## Stale selection

`--stale` narrows the item boundary to loadable objects whose Load health is not Green. It uses the same assessment as `weaver health`, including missing or non-successful Load state, freshness and managed upstream state. A static object that has loaded remains Green regardless of age; a static object that has never loaded is selected.

`--as-of` sets the freshness cutoff and is valid only with `--stale`. It must carry a time zone and defaults to 24 hours before the operation started. If every object in scope is Green, the empty Load succeeds.

Stale selection preserves ordering among selected work; it does not pull a Green upstream object into the run. `--stale` and `--reload` cannot be combined.

## Dry runs

`--dry-run` reads the installed estate, selects and orders work, and resolves what each selected object would execute. It does not execute authored work, refresh an endpoint, create a run record, change current Load state or move a bookmark.

A dry-run node is:

- `validated` when its installed work and prerequisites resolve;
- `invalid` when its own installed work or target cannot be resolved;
- `blocked` when an unresolved upstream node prevents validation.

A dry run is `succeeded` when every selected node validates, including when no work is selected, and `invalid` otherwise. A reload dry run still validates that every selected object is a Table and reports reload mode without resetting state.

## Reload

`--reload` reconstructs each selected Table from zero. Immediately before that Table executes, Weaver resets its bookmark to the initial boundary and marks its current Load state pending. The installed reload then empties and reconstructs the target.

Reload follows the selection exactly. It does not add downstream objects, and a selected node that is never reached keeps its prior bookmark and state. Folders are not reloadable; a selection containing one is rejected before execution, including during a dry run.

## Execution failures and fault tolerance

Without `--fault-tolerant`, the first failed or invalid node stops new scheduling. A dependant of failed or unresolved work is `blocked`; otherwise-ready nodes that were not reached remain `pending`. Weaver records the complete planned report, then raises a Load error with the partial report and available result evidence.

With `--fault-tolerant`, Weaver continues independent branches. A dependant may also run after an upstream execution failure has settled, and reads whatever state that failed execution left. This rule applies only to resolved work that started and produced a failure outcome. An unresolved or invalid upstream node still blocks its descendants.

Fault tolerance changes how much selected work is attempted. It does not change a failed node to success and does not make a failed or partially successful run successful.

## Node and run outcomes

An execution node ends as one of:

- `succeeded` — it completed without rejected rows;
- `succeeded_with_rejects` — valid work completed and rejected rows were reported;
- `failed` — installed work failed after execution started;
- `invalid` — the installed work or target could not be resolved before execution;
- `blocked` — an unresolved or unsatisfied upstream node prevented execution;
- `skipped` — policy or host support omitted the work;
- `pending` — fail-fast execution stopped before otherwise-ready work began.

The run outcome is:

- `succeeded` when no selected node failed, including an empty run;
- `succeeded_with_rejects` when selected branches completed and at least one reported rejects;
- `partially_succeeded` when some work succeeded or was skipped and some failed, was invalid or was blocked;
- `failed` when no requested branch completed successfully;
- `invalid` when a dry run cannot resolve a valid plan.

The normal CLI exits non-zero for failed, partially successful or invalid reports. An intolerant execution raises only after its report has been recorded; a fault-tolerant execution returns the unsuccessful report.

## Bookmarks and catalogue recording

Every node in an executed plan receives a final `_.Log` record, including blocked and pending nodes. A loadable object's latest outcome is also written to `_.LoadStatus`; executed load work writes `_.LoadStatistic`. These records distinguish a load refusal from an execution error and preserve available row counts.

A bookmark advances only when an executed load reports a new successful boundary. Rejected, failed, blocked, pending and static-skip outcomes do not advance it. Reload resets the selected Table's boundary before execution starts, so a failed reload remains visibly reset rather than restoring the old bookmark.

Weaver flushes the required catalogue records before returning a completed report or raising an intolerant Load failure. A catalogue write failure is an operation failure. A dry run writes none of this state.

## Defined behaviour

The Load contract specifies that Load:

1. executes installed definitions rather than unbuilt source changes;
2. keeps execution inside the selected item and optional name boundary;
3. orders item-wide and stale selections through the installed dependency graph;
4. treats named objects as exact selections without graph expansion or ordering;
5. performs dry-run resolution without execution or catalogue mutation;
6. keeps reload resets local to selected Tables reached for execution;
7. permits descendants of settled execution failures under fault tolerance while blocking descendants of unresolved or invalid work;
8. reports node outcomes separately from the run outcome; and
9. records every executed plan outcome durably before reporting completion.

See [`weaver load`](../reference/cli/load.md), [Dependencies](../reference/operation-behaviour/shared-selection-and-identity.md), and [Catalogue](../reference/catalogue-schema.md).
