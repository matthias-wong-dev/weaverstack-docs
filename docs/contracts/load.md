# Load contract

Load executes the installed data work owned by selected Weaver items. It reads the installed estate from the Weaver catalogue; it does not read or reinterpret project source.

## Inputs and selection

A load may select logical items, installed objects by name, or every installed item.

```bash
weaver load Warehouse/Operations
weaver load --name Parcel.Status Warehouse/Operations
weaver load
```

Item selection is a hard execution boundary:

- naming no item selects every item recorded as installed in the catalogue;
- naming an item selects the loadable objects that item owns;
- a dependency does not add an unnamed item to the run;
- selecting names runs only those installed objects and does not expand or order the selection through their dependencies.

For a Lakehouse, an object name may include its area, such as `Tables/Parcel.Status` or `Files/Parcel.Events`. A Warehouse object uses `Schema.Object`. A bare `Schema.Object` is accepted where it identifies one installed object.

`--stale` narrows the run to selected objects whose load health is not Green. `--as-of` changes the freshness cutoff and is valid only with `--stale`. Selecting no work is a successful run.

`--reload` reconstructs each selected table from an empty target and a reset bookmark. It applies only to selected tables, does not add downstream objects and cannot be combined with `--stale`. Folders cannot be reloaded with this option.

## Execution boundary

Load uses definitions and physical bindings installed by Build. Changing project source does not change a load until the project has been built successfully.

Warehouse work can execute without Spark. Lakehouse work may require a Fabric Spark session. An Environment is required only when the installed work needs to import Weaver-authored Python; it is not a universal Load prerequisite.

## Dependencies

For an item-wide run, Weaver orders selected work by its installed dependency graph.

- A node runs only after its selected dependencies have succeeded.
- A failed dependency blocks the dependent node.
- Dependencies outside the selected item do not widen the run.
- Name selection is an operator override: Weaver runs only the named objects without dependency expansion or dependency ordering.

## States and outcomes

An executing node ends as one of:

- `succeeded` — the work completed;
- `succeeded_with_rejects` — the work completed and reported rejected rows;
- `failed` — the work or its dispatch failed;
- `blocked` — an upstream dependency failed or could not be validated;
- `skipped` — execution policy omitted the node.

A dry run does not execute work. Its nodes are `validated`, `invalid` or `blocked`.

The run outcome is:

- `succeeded` when all executable work succeeds;
- `succeeded_with_rejects` when all executable branches complete and at least one reports rejects;
- `partially_succeeded` when some work succeeds and some fails or is blocked;
- `failed` when no requested branch completes or fail-fast execution stops the run;
- `invalid` when a dry run cannot produce a valid executable plan.

A normal CLI load exits non-zero when the report is not successful.

## Failure and fault tolerance

Without `--fault-tolerant`, Weaver stops after the first failed branch and raises a load failure with the partial report attached where available.

With `--fault-tolerant`, independent branches continue. Work that depends on a failed node remains blocked. Fault tolerance changes how much independent work Weaver attempts; it does not turn a failed or partially successful report into success.

## Bookmarks and recorded state

A successful load records its outcome in the catalogue. Bookmark changes become durable only for work that settles successfully. A dry run creates no run record and moves no bookmark.

Reload removes the selected table's bookmark before execution, marks its load state pending, empties the selected target and then runs the installed load. Other tables and downstream objects are outside that reset unless they were selected separately.

## Defined behaviour

The Load contract specifies that Load:

1. execute the installed definitions rather than unbuilt source changes;
2. keep execution within the selected item or name boundary;
3. respect dependency order for item-wide runs;
4. block dependent work after an upstream failure;
5. preserve independent progress only when fault tolerance is requested;
6. report node and run outcomes separately;
7. leave bookmarks unchanged during a dry run;
8. record completed work before reporting a successful run.

These properties do not make catalogue tables, internal planning nodes or execution transports public extension points.

For complete examples, see [Author a Lakehouse pipeline](../guides/lakehouse-pipeline.md) and [Author a Warehouse pipeline](../guides/warehouse-pipeline.md).
