# Connect items and dependencies

What should a Warehouse read when the data comes from a Lakehouse? Name the existing producer in a logical Shortcut. Weaver installs the connection in order and keeps its dependency with the project.

Continue [Landing’s working Parcel pipeline](../lakehouse/python.md) in the same `parcel` project. Its Folder feeds Event and CurrentStatus. Add a Warehouse without replacing those sources or their configuration.

## Present Landing’s Event in Operations {#present-landings-event-in-dispatch}

From the directory containing the project, run:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --warehouse Operations \
  --example Parcel
cd parcel
```

If already inside `parcel`, use `--project-folder .` instead. Initialise reads Landing’s existing binding, retains its files and adds Operations. The catalogue and published runtime stay in place. Use disposable managed targets: Build may prune undeclared co-located content; keep irreplaceable external sources outside them.

Operations keeps its own seeded `Parcel.StatusEvent` Table, CurrentStatus View and validations. The cross-item additions have distinct names. Open `Warehouse/Operations/shortcuts.yml`:

<!-- initialise:Warehouse/Operations/shortcuts.yml -->
```yaml
logical:
  Warehouse/Operations/Parcel.LakehouseEvent: Lakehouse/Landing/Tables/Parcel.Event
```
<!-- /initialise -->

The mapping reads from destination to source. Build presents Landing’s Event Table through the logical `Parcel.LakehouseEvent` Shortcut View. This does not replace StatusEvent.

Open `Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql` to see the additional loadable Table:

<!-- initialise:Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql -->
```sql
/*
Table ID: Parcel.LakehouseCurrentStatus

Primary key: Parcel ID

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
  Depot: varchar(50)

Description: The latest recorded status for each parcel.

Lineage: Parcel status events ordered by event sequence.
*/
with ranked as (
    select [Parcel ID]
         , [Status]
         , [Depot]
         , row_number() over (
               partition by [Parcel ID]
               order by [Event sequence] desc
           ) as [Event rank]
    from [Parcel].[LakehouseEvent]
)
select [Parcel ID]
     , [Status]
     , [Depot]
from ranked
where [Event rank] = 1;
```
<!-- /initialise -->

The SQL reference connects this new Table to Landing. Build orders the selected source and Shortcut; Load waits for the supported SQL-endpoint readiness boundary before the Warehouse reads the Lakehouse.

```bash
weaver check
weaver build --item Lakehouse/Landing --item Warehouse/Operations
weaver load Lakehouse/Landing Warehouse/Operations
weaver health --item Lakehouse/Landing --item Warehouse/Operations
```

In Operations’s SQL query editor:

```sql
SELECT [Parcel ID], [Status], [Depot]
FROM Parcel.LakehouseCurrentStatus
ORDER BY [Parcel ID];
```

Expect P-1001 / In transit / Central and P-1002 / Delivered / South. `Parcel.CurrentStatus` still reads Operations’s independent seeded StatusEvent Table. `Parcel.LakehouseCurrentStatus` reads Landing’s managed data. Their names keep those meanings separate.

The source identity in `shortcuts.yml` stays unchanged when [workspace mappings](environments.md) choose different physical destinations.

## Order selected work, not every related item

Python imports and supported Warehouse SQL references normally supply document dependencies without a second authored graph. An explicit `Dependencies` declaration replaces inference, including an empty list. Spark SQL data documents still require that field explicitly. The item graph must be acyclic.

For a connection with loadable work on both sides, select both logical items in an item-wide Load. Weaver orders selected producers before consumers and inserts supported OneLake-publication and SQL-endpoint readiness barriers where the installed cross-engine path requires them. The Shortcut View has no separate Load, but its consuming LakehouseCurrentStatus Table does. Name both Landing and Operations when you want that selected cross-item work ordered together.

Dependencies never add an unnamed item. Build changes affected descendants only inside selected items; item-wide Load orders only its selected work. Plain `--name` Load is an operator override without inferred dependency ordering or readiness barriers. [Run part of an estate](selective-runs.md) shows how deliberate ancestor/descendant expansion restores ordering within the requested boundary.

A physical Shortcut or a directly qualified external relation is different: it identifies data outside this project’s ownership, not a managed producer that Weaver can Build or order. See [Shortcuts and existing data](../lakehouse/shortcuts.md) for that boundary and [Dependencies](../core-concepts/dependencies.md) for the complete reasoning.

## Extend the same coordination to a model

A semantic model’s `Weaver.Source` annotation can connect its Table to a managed source. Estate Load then places selected source work before model refresh, and Health can show a model behind its source. A linked Report depends on the model for deployment, but has no data Load or Test of its own.

Add `--semantic-model Parcel --example Parcel` with Initialise against this same folder to generate the independent inline model and Report plus separately named `ParcelLakehouse` and `ParcelWarehouse` models. Build source items before source-backed models, using an existing approved service connection. [Connect a managed Fabric source](../semantic-models/managed-sources.md) explains the additional models; it never replaces the native Delivery partition.

Once the connections work, [map development and production](environments.md) without changing those logical source identities. [How Weaver works](../core-concepts/how-weaver-works.md) follows the source into installed operations; [Design philosophy](../core-concepts/design-philosophy.md) explains the choices behind keeping native authoring and queryable state.
