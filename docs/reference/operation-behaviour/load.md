# Load contract

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

See [`weaver load`](../cli/load.md), [Dependencies](shared-selection-and-identity.md), and [Catalogue](../catalogue-schema.md).