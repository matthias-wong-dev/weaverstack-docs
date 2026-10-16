# Working with Spark SQL

Keep the Python event pipeline and inspect its generated SQL transformation: the latest status for each parcel. Weaver installs it as another Delta Table and orders its Load after the event Table.

Use the [Python project](python.md) in `parcel`, with `Files/Parcel__Events.py` and `Tables/Parcel__Event.py` already working. Initialise has already written the SQL file below in that same Landing item.

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

## Run the transformation {#install-the-addition-and-run-it}

Use the same workspace configuration and already published matching Environment:

```bash
weaver check
weaver build --item Lakehouse/Landing
weaver load Lakehouse/Landing
```

<!-- cli-capture: {"id": "46-lakehouse-load", "title": "CurrentStatus · step from the first pipeline Load"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="CurrentStatus · step from the first pipeline Load">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.3s

Workspace  Weaver Example
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s

  Wait for Spark session                                                                                  35.4s

→   Load Lakehouse/Landing/Files/Parcel.Events

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Files/Parcel.Events  (read 1, +1 ~0 -0 !0)                                      3.6s</span>

→   Load Lakehouse/Landing/Tables/Parcel.Event

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +3 ~0 -0 !0)                                     12.2s</span>

→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +2 ~0 -0 !0)                             12.1s</span>

  Execute                                                                                                 27.8s

  Record what the run did                                                                                  0.0s

<span class="terminal-status-green">✓ Load                                                                                                    1m14s</span>

<span class="terminal-status-green">load succeeded: Lakehouse/Landing</span>

Load summary
<span class="terminal-status-green">    3 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   6
    inserted               6
    updated                0
    deleted                0
    rejected               0

  Workflow: [run-id]
</code></pre>
</figure>
<!-- /cli-capture -->

The first pipeline Load already ran this generated transformation after Event and read two current-status rows. Repeating the item-wide Load keeps that dependency order. Editing this project SQL does not itself require republishing the Environment.

```bash
weaver health --item Lakehouse/Landing
```

## Read the current statuses

Query the same Lakehouse SQL analytics endpoint once CurrentStatus is visible:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

The live SQL query returned:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

A successful Load tells you the query ran. It does not establish that the latest-event rule selected the right rows. [Test these same Tables](tests.md) against an independent expected result and reject unknown event statuses.

[Table reference](../reference/weaver-documents/table.md#spark-sql) owns the SQL body rules. For the shared ordering and selection model, see [Connect items and dependencies](../estate/connected-items.md).
