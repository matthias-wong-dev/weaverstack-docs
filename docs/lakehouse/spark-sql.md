# Working with Spark SQL

Keep the Python event pipeline and add one SQL transformation: the latest status for each parcel. Weaver installs it as another Delta Table and orders its Load after the event Table.

Start from the working [Python checkpoint](python.md) in `parcel-lakehouse-python`. Direct entrants can use that page and the [checked snapshot's checkpoint list](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-lakehouse). Keep `Files/Parcel__Events.py` and `Tables/Parcel__Event.py`; do not create a second Event document or initialise another project.

## Add the current-status query

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

The window selects the last event by sequence. Spark SQL Tables require explicit `Dependencies`, even when the query names the managed source. Here `Parcel.Event` is the Python Table from the previous page. A Spark SQL Table without managed inputs would use `Dependencies: []`; `Lineage` remains descriptive.

## Install the addition and run it

Use the same workspace configuration and already published matching Environment:

```bash
weaver check
weaver build --item Lakehouse/Landing
weaver load Lakehouse/Landing
weaver health --item Lakehouse/Landing
```

Check should print `Project valid.` It validates the declaration and SQL program shape, not Spark's execution of the query. Build should install CurrentStatus without failed actions. Item-wide Load should run the existing Folder, Event and then CurrentStatus. CurrentStatus should read two rows; Health should show Green Build and Load sections. Adding this project SQL does not itself require republishing the Environment.

## Read the current statuses

Query the same Lakehouse SQL analytics endpoint once CurrentStatus is visible:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

The expected result is:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

A successful Load tells you the query ran. It does not establish that the latest-event rule selected the right rows. [Test these same Tables](tests.md) against an independent expected result and reject unknown event statuses.

[Table reference](../reference/weaver-documents/table.md#spark-sql) owns the SQL body rules. For the shared ordering and selection model, see [Connect items and dependencies](../estate/connected-items.md).
