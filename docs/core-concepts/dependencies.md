# Dependencies

A dependency says that one declared object reads another. Weaver uses dependencies to order work, find the structural impact of a change and explain why later work cannot run yet.

Dependencies do not widen a command's selection. They order work only within the logical items the command selected.

## Inferred and explicit dependencies

Weaver normally discovers dependencies from the declaration itself:

- Python imports of another object in the same item identify that object as upstream.
- SQL relation references identify the tables and views the statement reads.
- Logical shortcuts connect a consumer to an object owned by another logical item.

Discovery is static. `weaver check` does not import authored Python or execute SQL to find dependencies.

A declaration can instead provide an explicit dependency list. When it does, that list replaces inference; it does not supplement it. An explicitly empty list therefore means that the object has no managed dependencies. Spark SQL objects require this explicit choice because a query may read paths or other sources that SQL relation discovery cannot represent completely.

Keep the exact declaration syntax with the relevant authoring form. The [Lakehouse pipeline](../guides/lakehouse-pipeline.md) shows both a dependency inferred from a Python import and an explicit empty list for Spark SQL. The [Warehouse pipeline](../guides/warehouse-pipeline.md) shows a dependency inferred from T-SQL.

## Identity includes the item

A dependency resolves to a logical identity, not just a `Schema.Object` name. The owning item is part of that identity, and a Lakehouse identity also distinguishes its `Files` and `Tables` areas.

This means:

- the same `Schema.Object` may exist independently in several items;
- a Lakehouse Folder and Table may share a `Schema.Object` without becoming one object;
- a two-part reference resolves within the consuming item;
- a managed cross-item read needs a logical shortcut that identifies the producer.

See [Projects and estates](projects-and-estates.md), [Logical and physical items](logical-and-physical-items.md), and [Resources and artefacts](resources-and-artefacts.md) for the identities that Build and later operations preserve.

## What dependencies change during Build

Build uses the complete project graph to establish a deterministic structural order. An upstream object is built before its dependent objects, including across logical items when both are in scope.

Dependencies also determine change impact. A new or changed declaration can require its downstream dependants to be rebuilt even when their own files did not change. This is why a small source edit can produce a larger Build selection.

Selection remains a hard boundary. Selecting one item for Build does not add an upstream or downstream item. Weaver applies dependency impact and ordering to the selected project items and leaves omitted items untouched. The [CLI reference](../reference/cli.md#item-and-target-selection) defines Build's item-selection grammar.

Cycles have no valid structural order. `weaver check` and Build reject dependency cycles, including cycles that appear only when relationships between items are considered. If installed catalogue state cannot form an acyclic graph, Load, Test and Health refuse to treat it as a runnable estate. Fix the declarations or shortcuts rather than trying to control their file order.

## What dependencies change during Load

An item-wide Load reads the installed dependency graph from the [Weaver catalogue](catalogue.md). It runs selected upstream work before selected downstream work, and a failed upstream load blocks the dependent work.

The item boundary still wins. If a selected object depends on an object in an unselected item, that dependency does not pull the other item into the run. Select both items when both should run:

```bash
weaver load Lakehouse/Landing Warehouse/Operations
```

Name selection is different from dependency ordering. `load --name` is an operator override that runs exactly the named installed objects, without adding or ordering their dependencies. It is useful for a deliberate targeted rerun, not as a request for an affected subgraph.

The [Load contract](../contracts/load.md) owns the exact selection, ordering, blocking and failure behaviour. The [CLI reference](../reference/cli.md#load-test-and-health-selection) owns the command syntax.

## What dependencies change during Test

A Test or Assumption may depend on the data objects it reads. Those dependencies make the validation a terminal consumer of installed data; a Test or Assumption cannot itself be a dependency target.

An item-wide Test selects the installed validations owned by the named items. It does not add another item because a validation reads data there. Validations run in a stable identity order rather than a test-to-test dependency order: their declared dependencies describe the data they check, not a sequence among validations.

Name selection again stays inside the selected item scope. See the [CLI reference](../reference/cli.md#load-test-and-health-selection) for item-wide and named Test forms.

## Use the graph, not file order

Do not encode sequencing by renaming files or relying on discovery order. Declare the read in Python, SQL, metadata or a logical shortcut, then use `weaver check` before Build.

[How Weaver works](how-weaver-works.md) places dependency resolution in the full lifecycle. [First project](../get-started/first-project.md) shows that lifecycle with one item; the two authoring guides show how the graph grows as objects begin to read one another.
