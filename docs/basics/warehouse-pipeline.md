# Build a Warehouse pipeline

This guide creates one Warehouse Table and a dependent View, installs them, loads the Table and queries the View.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Use a Fabric workspace where you can create or modify a catalogue Warehouse and a target Warehouse.

## 1. Initialise the project

Create a project containing `Warehouse/Operations`:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-warehouse \
  --catalogue Catalogue \
  --warehouse Operations \
  --no-example
cd parcel-warehouse
```

Replace `Parcel Development` with your workspace. Weaver creates or reuses the Fabric items, writes `workspace-config.yml` and creates an empty `Warehouse/Operations` directory. The command ends with `Weaver project ready in .../parcel-warehouse.`

## 2. Add the Table

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

The Warehouse item now contains a Table document named `Parcel.StatusEvent`. Its query will produce three rows when Load runs it.

## 3. Add the dependent View

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

Weaver infers the dependency from the relation referenced in the query. `Lineage` is descriptive metadata; it does not create the dependency. Build installs the View definition, while Load runs the Table that supplies its rows.

## 4. Check the documents

Validate the project locally:

```bash
weaver check
```

Weaver prints `Project valid.` The check confirms that both documents parse, their filenames agree with their declared identities and the View reference resolves. It does not submit T-SQL to Fabric.

## 5. Build the item

Install the project:

```bash
weaver build
```

The installation summary should report no failed actions. The installed estate now contains the `Parcel.StatusEvent` Table, its load work and the `Parcel.CurrentStatus` View. Build does not run the Table query.

## 6. Load and inspect the result

Run all installed load work in the item, then read its state:

```bash
weaver load Warehouse/Operations
weaver health --item Warehouse/Operations
```

Load should report `Parcel.StatusEvent` as succeeded with three rows read. Health should show Green Build and Load sections for the item.

Query the Warehouse SQL endpoint:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

The View returns:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

Edit either document, run `weaver check` and `weaver build` again, then use `weaver load Warehouse/Operations --stale` to catch up work made stale by that Build. Use `--name` only when deliberately diagnosing or reconstructing selected installed work. Exact selection rules are in the [Load operation reference](../reference/operation-behaviour/load.md).
