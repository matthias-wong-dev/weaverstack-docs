# Loading changes

A keyed incremental Table can apply new rows, changed values and cancellations while its definition stays installed. Your SQL returns the candidate rows and delete keys; Weaver generates the target merge and records the consumer's progress.

Continue the [first Warehouse project](first-project.md) and [its validations](tests.md). Keep StatusEvent and the CurrentStatus View unchanged. Add a new `Parcel.LiveStatus` Table over changing external records, using the same Operations item, configuration and catalogue.

## Keep the changing source separate

Keep the working `workspace-config.yml` and its existing targets. Create or reuse a separate disposable **ParcelSource** Warehouse in the same workspace to hold the changing source. Do not add it as a managed target: Build may prune undeclared content in targets it owns. All shell commands below run from your existing project root.

Add this physical mapping to `Warehouse/Operations/shortcuts.yml`, creating the file if absent. Preserve any existing `logical` mappings for the Lakehouse integration:

```yaml
physical:
  "Warehouse/Operations/Source.Parcel": "Warehouse/ParcelSource/Source.Parcel"
```

Build installs `[Source].[Parcel]` as an item-local View without taking ownership of the physical source. Warehouse physical Shortcuts stay within the configured workspace; [Shortcut reference](../reference/weaver-documents/shortcut.md) owns the exact target forms.

In a **SQL query connected to ParcelSource**, create the external table with:

```sql
if schema_id(N'Source') is null
    exec(N'create schema [Source]');

if object_id(N'[Source].[Parcel]', N'U') is null
begin
    create table [Source].[Parcel] (
        [Parcel ID] varchar(20) not null,
        [Status] varchar(30) not null,
        [Depot] varchar(30) not null,
        [Row update datetime] datetime2(6) not null
    );
end;
```

Then seed it in the same query editor. This deletes existing source rows, so use the disposable example source:

```sql
delete from [Source].[Parcel];

insert into [Source].[Parcel] (
    [Parcel ID],
    [Status],
    [Depot],
    [Row update datetime]
)
values
    ('P-1001', 'In transit', 'Central', sysutcdatetime()),
    ('P-1002', 'Delivered', 'South', sysutcdatetime());
```

Verify the source before Build:

```sql
select [Parcel ID], [Status], [Depot], [Row update datetime]
from [Source].[Parcel]
order by [Parcel ID];
```

It should return `P-1001` as `In transit` at `Central` and `P-1002` as `Delivered` at `South`. A missing source or denied access is an error to fix, not an empty change window. These source scripts sit outside `Warehouse/Operations`; Weaver does not install them.

## Let the consumer ask for its own changes

The complete `Warehouse/Operations/Parcel.LiveStatus.sql` is:

```sql
/*
Table ID: Parcel.LiveStatus

Description: Current state of active parcels.

Lineage: Parcel records supplied through the physical Source.Parcel Shortcut.

Primary key: Parcel ID

Incremental: true

Dependencies: []

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
  Depot: varchar(30)
*/
declare @bookmark_datetime datetime2(6);
set @bookmark_datetime = coalesce(
    (
        select [Bookmark datetime]
        from [_].[Bookmark]
        where [Item type] = N'Warehouse'
          and [Item name] = N'Operations'
          and [Schema name] = N'Parcel'
          and [Object name] = N'LiveStatus'
    ),
    cast('1900-01-01' as datetime2(6))
);

-- Rows to insert or update
select [Parcel ID]
     , [Status]
     , [Depot]
from [Source].[Parcel]
where [Row update datetime] > @bookmark_datetime
  and [Status] <> 'Cancelled';

-- Keys to delete
select [Parcel ID]
from [Source].[Parcel]
where [Row update datetime] > @bookmark_datetime
  and [Status] = 'Cancelled';
```

The first result set supplies every business column for insert or update candidates. The second supplies primary keys to delete. Absence from the first result set leaves a target row alone; it is not a deletion claim.

The bookmark belongs to this consumer, `Warehouse/Operations/Parcel.LiveStatus`. The source's `[Row update datetime]` says when its row changed; the catalogue's `[Bookmark datetime]` says how far this Table has processed. The initial 1900 boundary asks for all retained source rows. Later Loads read changes after the previous clean boundary.

`Dependencies: []` is required here: T-SQL inference does not resolve `[Source].[Parcel]` to a physical Warehouse Shortcut. The override removes the nonexistent managed producer edge, not the source access requirement. There is no Weaver-managed source Load to order.

## Establish the first successful boundary

Check and install once:

```bash
weaver check
weaver build --item Warehouse/Operations
```

After Build, open a **SQL query connected to Operations** and verify the installed Shortcut:

```sql
select [Parcel ID], [Status], [Depot], [Row update datetime]
from [Source].[Parcel]
order by [Parcel ID];
```

Both seeded rows should be visible. Back at the project root, load the installed Table:

```bash
weaver load Warehouse/Operations --dry-run
weaver load Warehouse/Operations
```

<!-- cli-capture: {"id": "33-incremental-first-load", "title": "Load \u00b7 establish the incremental Table", "start": "Load summary", "end": "  Workflow:", "full": true} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · establish the incremental Table">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   5
    inserted               2
    updated                0
    deleted                0
    rejected               0

</code></pre>
<details><summary>Show the complete capture</summary><pre tabindex="0" aria-label="Captured terminal output"><code>Load

  Read catalogue                                                                                           2.4s

Workspace  Weaver Example
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s

→   Load Warehouse/Operations/Parcel.LiveStatus

→   Load Warehouse/Operations/Parcel.StatusEvent

<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LiveStatus  (read 2, +2 ~0 -0 !0)                                     3.8s</span>

<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +0 ~0 -0 !0)                                    4.5s</span>

  Execute                                                                                                  4.8s

  Record what the run did                                                                                  0.5s

<span class="terminal-status-green">✓ Load                                                                                                     7.7s</span>

<span class="terminal-status-green">load succeeded: Warehouse/Operations</span>

Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   5
    inserted               2
    updated                0
    deleted                0
    rejected               0

  Workflow: [run-id]
</code></pre></details><p class="terminal-source"><a href="../../assets/cli-captures/33-incremental-first-load.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

In **Operations**, inspect the target:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[LiveStatus]
order by [Parcel ID];
```

It should contain the two seeded parcels. A clean Load sets the bookmark to the UTC instant immediately before that Load began. In a **SQL query connected to Catalogue**, record that boundary:

```sql
select [Bookmark datetime]
from [_].[Bookmark]
where [Item type] = N'Warehouse'
  and [Item name] = N'Operations'
  and [Schema name] = N'Parcel'
  and [Object name] = N'LiveStatus';
```

## Change the data, not the definition

In **ParcelSource**, change the source rows:

```sql
update [Source].[Parcel]
set [Status] = 'Delivered',
    [Row update datetime] = sysutcdatetime()
where [Parcel ID] = 'P-1001';

update [Source].[Parcel]
set [Status] = 'Cancelled',
    [Row update datetime] = sysutcdatetime()
where [Parcel ID] = 'P-1002';
```

Read the source again with the earlier source query. Both update datetimes must be later than the bookmark you recorded. Return to the project root and Load **without Build**:

```bash
weaver load Warehouse/Operations --dry-run
weaver load Warehouse/Operations
```

<!-- cli-capture: {"id": "35-incremental-changed-load", "title": "Load \u00b7 source update and cancellation", "start": "Load summary", "end": "  Workflow:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · source update and cancellation">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   4
    inserted               0
    updated                1
    deleted                1
    rejected               0

</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/35-incremental-changed-load.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

The `P-1001` candidate updates the target to `Delivered`. The source update that marks `P-1002` as `Cancelled` produces a target delete key: a source update need not become a target update. In `Operations`, the target query should now return:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | Delivered | Central |

`ParcelSource` should still retain `P-1002` as `Cancelled`. Read the catalogue query again: the consumer bookmark should be later than its first boundary. Without changing the source, run one more Load:

```bash
weaver load Warehouse/Operations
```

<!-- cli-capture: {"id": "36-incremental-noop-load", "title": "Load \u00b7 no new incremental changes", "start": "Load summary", "end": "  Workflow:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · no new incremental changes">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   3
    inserted               0
    updated                0
    deleted                0
    rejected               0

</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/36-incremental-noop-load.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

LiveStatus reads no new candidates; the original StatusEvent still reads its three constant rows. The item summary therefore shows three rows read but no inserts, updates or deletes. The empty incremental window leaves the target unchanged and advances the bookmark again. Failed, rejected, blocked and static-skip outcomes do not advance it.

A hard source deletion leaves no row for either SELECT. To propagate it, retain change evidence such as tombstones, an audit table or CDC until the consumer reads it. This simple timestamp predicate also assumes a compatible UTC time basis and source change visibility; it is not a universal change-capture query.

## Keep Build separate from a data-only run

Editing a Weaver document changes the source definition, not the installed one. Check and Build install that change; for each rebuilt loadable object, Build resets its bookmark to the initial boundary. The next Load must ask for all available history. That is why changing a VALUES constant and rebuilding it would not demonstrate this data-only loop.

The [full incremental-processing explanation](../advanced/incremental-data-processing.md#the-incremental-table-contract) covers result forms and change-source design; [Load behaviour](../reference/operation-behaviour/load.md) owns exact bookmark, reload and failure rules. [Schemas, keys and protected data](schema-and-protection.md) follows from the next question: which data can you reconstruct, and which must stay outside a managed target?
