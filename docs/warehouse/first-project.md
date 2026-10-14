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
  --no-example \
  --non-interactive
cd parcel-warehouse
```

Initialisation creates or reuses the `Catalogue` and `Operations` Warehouses and the `Weaver` Environment. It writes the project configuration and Environment definition but does not publish the Environment. This T-SQL task does not need a Spark runtime. `--non-interactive` prevents browser sign-in, so configure credentials as described in Installation before using it.

The command ends with `Weaver project ready in .../parcel-warehouse.` The generated `workspace-config.yml` binds `Warehouse/Operations` to the physical `Operations` Warehouse. Its relevant configuration is:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
environment: Weaver

targets:
  Warehouse/Operations: Operations
```

**Ownership:** use a disposable target for this example. Build reconciles selected managed items and may prune undeclared co-located content. Keep irreplaceable sources in a separate physical item; [Schemas, keys and protected data](schema-and-protection.md#keep-the-source-outside-the-managed-target) explains the stronger boundary.

For direct entry, the [complete journey snapshot](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-warehouse-journey) contains the SQL below plus the next page's validations. Use the two SQL files below for this first checkpoint; add `tests/` and `assumptions/` when you reach that page. The snapshot does not provision Fabric items.

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

The composite key identifies an event, not a parcel. The declared schema describes the four business columns; Weaver supplies the managed columns used for row auditing and change comparison. You do not write a target INSERT or MERGE procedure.

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

The reference to `[Parcel].[StatusEvent]` lets Weaver infer the View's dependency. `Lineage` describes the data; it does not create that edge. Build installs the Table and View in dependency order. Only the Table has data work for Load to run.

## Install the definitions, then load the rows

```bash
weaver check
weaver build --item Warehouse/Operations
weaver load Warehouse/Operations
weaver health --item Warehouse/Operations
```

Check prints `Project valid.` It parses the declarations locally; it does not submit T-SQL to Fabric. Build installs the physical Table, its generated load work and the View, but does not populate the three event rows. Its installation summary should report no failed actions.

On the first Load, `Parcel.StatusEvent` should succeed with three rows read and inserted and no rejected rows. The generated work stages the query result, matches keys, compares changed business values and records Load state. Health should show Green Build and Load sections.

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

The View now gives you one row per parcel, but a successful Load does not prove that it chose the right event. [Testing Warehouse data](tests.md) adds an independent expected result and a check for unknown statuses to this same project, without initialising another one.

If you edit either SQL document, Check and Build install the changed definition before another Load. [The development cycle](../estate/development-cycle.md) covers that loop; [Table reference](../reference/weaver-documents/table.md) owns the exact authoring and load contract.
