# Working with Spark SQL

Keep the Python event pipeline and inspect its generated SQL transformation: the latest status for each parcel. Weaver installs it as another Delta Table and orders its Load after the event Table.

Use the [Python project](python.md) in `parcel`. Initialise wrote this SQL file into the same Landing item, and the first Load already ran it.

## Inspect the current-status query {#add-the-current-status-query}

Open `Lakehouse/Landing/Tables/Parcel.CurrentStatus.sql`:

<!-- initialise:Lakehouse/Landing/Tables/Parcel.CurrentStatus.sql -->
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
<!-- /initialise -->

The window selects the last event by sequence. Spark SQL Tables require explicit `Dependencies`, even when the query names the managed source. Here `Parcel.Event` is the Python Table from the previous page. A Spark SQL Table without managed inputs would use `Dependencies: []`; `Lineage` remains descriptive.

## It already ran {#install-the-addition-and-run-it}

You do not need to run anything new. The first pipeline Load ran CurrentStatus straight after Event, because `Dependencies` names Event:

```text
✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +3 ~0 -0 !0)
→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus
✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +2 ~0 -0 !0)
```

When you edit this query, the loop is the same as for Python: `weaver check`, `weaver build --item Lakehouse/Landing`, then `weaver load Lakehouse/Landing --stale` to rerun what the Build changed. Editing project SQL does not require republishing the Environment.

## Read the current statuses

Query the Landing SQL analytics endpoint:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

The query returns:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

[Test these same Tables](tests.md) against an independent expected result and reject unknown event statuses.

[Table reference](../reference/weaver-documents/table.md#spark-sql) owns the SQL body rules. For the shared ordering and selection model, see [Connect items and dependencies](../estate/connected-items.md).
