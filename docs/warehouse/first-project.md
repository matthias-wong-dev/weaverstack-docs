# A first Warehouse Table and View

Keep the transformation as a T-SQL SELECT. A metadata comment tells Weaver which Table to maintain; Build generates its load work, and Load applies the rows and records the result. Here, three parcel events feed a View showing each parcel's latest status.

Use the [documented Weaver installation](../getting-started/installation.md) and a Fabric workspace where you can create or modify Warehouses. The example uses `Parcel Development`; substitute your workspace name. All shell commands after setup run from the project root.

## Give the SQL a home

Create an empty project:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-warehouse \
  --catalogue Catalogue \
  --environment Weaver \
  --warehouse Operations \
  --no-example
cd parcel-warehouse
```

Initialise creates or reuses the named items and writes `workspace-config.yml`. This SQL task needs no Spark runtime; if interactive setup offers Environment publication, decline it for this Warehouse task. Use the project below, or the [complete example files](../assets/examples/parcel-warehouse-journey.zip); start with the two SQL files and add their validations on the next page.

<details markdown="1">
<summary>See the generated workspace bindings</summary>

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
environment: Weaver

targets:
  Warehouse/Operations: Operations
```

`Warehouse/Operations` is the logical item; `Operations` is its physical Warehouse. Use your actual workspace name.

</details>

## Write the event Table

Create `Warehouse/Operations/Parcel.StatusEvent.sql`:

```sql
/*
Table ID: Parcel.StatusEvent

Description: One row per parcel status event.

Lineage: A deterministic carrier feed represented by this example.

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: varchar(20)
  Event sequence: int
  Status: varchar(30)
  Depot: varchar(50)
*/
select v.[Parcel ID]
     , v.[Event sequence]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 1, 'Accepted', 'North'),
    ('P-1001', 2, 'In transit', 'Central'),
    ('P-1002', 1, 'Delivered', 'South')
) as v ([Parcel ID], [Event sequence], [Status], [Depot]);
```

The key identifies one event. Keep the SQL as a SELECT; the declaration describes the Table that should receive it.

## Read the latest event through a View

Create `Warehouse/Operations/Parcel.CurrentStatus.sql`:

```sql
/*
View ID: Parcel.CurrentStatus

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
    from [Parcel].[StatusEvent]
)
select [Parcel ID]
     , [Status]
     , [Depot]
from ranked
where [Event rank] = 1;
```

The View reads the event Table and keeps the most recent row for each parcel.

## Install the definitions, then load the rows

**Use disposable targets.** Build manages the selected item and may prune undeclared co-located content. Keep irreplaceable sources in a separate physical item; [target ownership](schema-and-protection.md#keep-the-source-outside-the-managed-target) explains the boundary.

```bash
weaver check
weaver build --item Warehouse/Operations
weaver load Warehouse/Operations
weaver health --item Warehouse/Operations
```

Check should print `Project valid.` Build should report no failed actions. The first Load should read and insert three event rows with no rejects; Health should show Green Build and Load sections.

In a SQL query connected to **Operations**, read the View:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

## What happened around the SELECT

Build created the physical Table, generated its loading procedure and installed the dependent View. The SQL reference supplied the dependency; `Lineage` is descriptive. Load staged the query result, matched keys and reconciled changed values according to the Table’s policy. It also recorded the row changes and processing state for Health. You wrote neither an INSERT/MERGE procedure nor a second load-order definition.

The View now gives you one row per parcel, but a successful Load does not prove that it chose the right event. [Testing Warehouse data](tests.md) adds an independent expected result and a check for unknown statuses to this same project, without initialising another one.

If you edit either SQL document, Check and Build install the changed definition before another Load. [The development cycle](../estate/development-cycle.md) covers that loop; [Table reference](../reference/weaver-documents/table.md) owns the exact authoring and load contract.
