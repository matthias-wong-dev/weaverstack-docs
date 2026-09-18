# Build a Lakehouse pipeline with Spark SQL

This guide creates two Spark SQL Tables in one Lakehouse: a seeded event Table and a current-status Table that depends on it. Spark SQL documents require an explicit `Dependencies` field, including `Dependencies: []` when there is no managed dependency.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Use a Fabric workspace where you can create or modify a catalogue Warehouse and a Lakehouse.

Spark SQL runs in Fabric Spark but does not import Weaver-authored Python, so this pipeline does not require a published Fabric Environment.

## 1. Initialise the project

Create a project containing `Lakehouse/Landing`:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-lakehouse-sql \
  --catalogue Catalogue \
  --lakehouse Landing \
  --no-example
cd parcel-lakehouse-sql
```

Replace `Parcel Development` with your workspace. Weaver writes `workspace-config.yml` and an empty `Lakehouse/Landing` directory. The command ends with `Weaver project ready in .../parcel-lakehouse-sql.`

## 2. Add the source Table

Create `Lakehouse/Landing/Tables/Parcel.Event.sql`:

```sql
/*
Table ID: Parcel.Event

Description: One row per parcel tracking event.

Lineage: A deterministic carrier feed represented by this example.

Dependencies: []

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: string
  Event sequence: integer
  Status: string
  Depot: string
*/
select *
from values
    ('P-1001', 1, 'Accepted', 'North'),
    ('P-1001', 2, 'In transit', 'Central'),
    ('P-1002', 1, 'Delivered', 'South')
as event(`Parcel ID`, `Event sequence`, `Status`, `Depot`);
```

`Dependencies: []` is required because this Spark SQL Table reads no managed object. The final query supplies its staging rows.

## 3. Add the dependent Table

Create `Lakehouse/Landing/Tables/Parcel.CurrentStatus.sql`:

```sql
/*
Table ID: Parcel.CurrentStatus

Description: The latest recorded status for each parcel.

Lineage: Parcel status events ordered by event sequence.

Dependencies:
  - Parcel.Event

Primary key: Parcel ID

Schema:
  Parcel ID: string
  Status: string
  Depot: string
*/
with ranked as (
    select `Parcel ID`
         , `Status`
         , `Depot`
         , row_number() over (
               partition by `Parcel ID`
               order by `Event sequence` desc
           ) as `Event rank`
    from Parcel.Event
)
select `Parcel ID`, `Status`, `Depot`
from ranked
where `Event rank` = 1;
```

Spark SQL still requires the explicit dependency even though Weaver can find `Parcel.Event` in the query. The declaration establishes the execution relationship; `Lineage` remains descriptive prose.

## 4. Check the documents

Validate the project locally:

```bash
weaver check
```

Weaver prints `Project valid.` The check confirms document placement, metadata, declared dependencies and the one-result-query load shape. It does not ask Spark to execute the SQL.

## 5. Build and load the item

Install both Tables, run the item-wide load and read the resulting state:

```bash
weaver build
weaver load Lakehouse/Landing
weaver health --item Lakehouse/Landing
```

Build should finish with no failed actions. Load should run `Tables/Parcel.Event` before `Tables/Parcel.CurrentStatus`; the first Table reads three rows and the second reads two. Health should show Green Build and Load sections.

## 6. Inspect the result

Query the Lakehouse SQL analytics endpoint:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

The result is:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

After editing either document, run Check and Build again, then use `weaver load Lakehouse/Landing --stale` to catch up work made stale by that Build. The [Dependencies](../core-concepts/dependencies.md) page explains why Spark SQL is an exception to inference-first authoring.
