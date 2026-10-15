# Loading changes

A keyed incremental Table can apply new rows, changed values and cancellations while its definition stays installed. Your SQL returns the candidate rows and delete keys; Weaver generates the target merge and records the consumer's progress.

The [first project](first-project.md) and [its validations](tests.md) use a constant event feed and a latest-status View. This page is a **complete mutable-source variation**, not an edit to that fixture. It keeps `Warehouse/Operations` and the same parcel IDs, but `Parcel.CurrentStatus` is now a managed **Table** over external current-state records, rather than a View over `Parcel.StatusEvent`. Use the existing [incremental Warehouse snapshot](../assets/examples/parcel-incremental-warehouse.zip) in its own project directory and disposable targets. Do not overlay it on the first project's installed View or carry its fixed expected-row Test into this variation.

Save the `parcel-incremental-warehouse.zip` download in an empty working directory, then extract its repository-relative paths and enter the project:

```bash
python -m zipfile -e parcel-incremental-warehouse.zip .
cd examples/parcel-incremental-warehouse
```

## Keep the changing source separate

Use the [documented installation and access](../getting-started/installation.md). In your workspace, create three Warehouses: `ParcelCatalogue`, `ParcelOperations` and `ParcelSource`. All shell commands below run from the incremental snapshot's root. Its `workspace-config.yml` contains:

```yaml
workspace: Parcel Development
catalogue: Warehouse/ParcelCatalogue

targets:
  Warehouse/Operations: ParcelOperations
```

`ParcelSource` is deliberately absent from `targets`. Build may prune undeclared co-located content in managed targets, so the mutable source must remain outside `ParcelOperations`.

The snapshot's `Warehouse/Operations/shortcuts.yml` presents the external Table locally:

```yaml
physical:
  "Warehouse/Operations/Source.Parcel": "Warehouse/ParcelSource/Source.Parcel"
```

Build installs `[Source].[Parcel]` as an item-local View without taking ownership of the physical source. Warehouse physical Shortcuts stay within the configured workspace; [Shortcut reference](../reference/weaver-documents/shortcut.md) owns the exact target forms.

In a **SQL query connected to ParcelSource**, run `source/ParcelSource/01-setup.sql`:

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

Then run `source/ParcelSource/02-seed.sql` in the same query editor. This deletes existing source rows, so use the disposable example source:

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

The complete `Warehouse/Operations/Parcel.CurrentStatus.sql` is:

```sql
/*
Table ID: Parcel.CurrentStatus

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
          and [Object name] = N'CurrentStatus'
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

The bookmark belongs to this consumer, `Warehouse/Operations/Parcel.CurrentStatus`. The source's `[Row update datetime]` says when its row changed; the catalogue's `[Bookmark datetime]` says how far this Table has processed. The initial 1900 boundary asks for all retained source rows. Later Loads read changes after the previous clean boundary.

`Dependencies: []` is required here: T-SQL inference does not resolve `[Source].[Parcel]` to a physical Warehouse Shortcut. The override removes the nonexistent managed producer edge, not the source access requirement. There is no Weaver-managed source Load to order.

## Establish the first successful boundary

Check and install once:

```bash
weaver check
weaver build --item Warehouse/Operations
```

After Build, open a **SQL query connected to ParcelOperations** and verify the installed Shortcut:

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

In **ParcelOperations**, inspect the target:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

It should contain the two seeded parcels. A clean Load sets the bookmark to the UTC instant immediately before that Load began. In a **SQL query connected to ParcelCatalogue**, record that boundary:

```sql
select [Bookmark datetime]
from [_].[Bookmark]
where [Item type] = N'Warehouse'
  and [Item name] = N'Operations'
  and [Schema name] = N'Parcel'
  and [Object name] = N'CurrentStatus';
```

## Change the data, not the definition

In **ParcelSource**, run `source/ParcelSource/03-change.sql`:

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

The `P-1001` candidate updates the target to `Delivered`. The source update that marks `P-1002` as `Cancelled` produces a target delete key: a source update need not become a target update. In `ParcelOperations`, the target query should now return:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | Delivered | Central |

`ParcelSource` should still retain `P-1002` as `Cancelled`. Read the catalogue query again: the consumer bookmark should be later than its first boundary. Without changing the source, run one more Load:

```bash
weaver load Warehouse/Operations
```

The empty window leaves the target unchanged and advances the bookmark again. Failed, rejected, blocked and static-skip outcomes do not advance it.

A hard source deletion leaves no row for either SELECT. To propagate it, retain change evidence such as tombstones, an audit table or CDC until the consumer reads it. This simple timestamp predicate also assumes a compatible UTC time basis and source change visibility; it is not a universal change-capture query.

## Keep Build separate from a data-only run

Editing a Weaver document changes the source definition, not the installed one. Check and Build install that change; for each rebuilt loadable object, Build resets its bookmark to the initial boundary. The next Load must ask for all available history. That is why changing a VALUES constant and rebuilding it would not demonstrate this data-only loop.

The [full incremental-processing explanation](../advanced/incremental-data-processing.md#the-incremental-table-contract) covers result forms and change-source design; [Load behaviour](../reference/operation-behaviour/load.md) owns exact bookmark, reload and failure rules. [Schemas, keys and protected data](schema-and-protection.md) follows from the next question: which data can you reconstruct, and which must stay outside a managed target?
