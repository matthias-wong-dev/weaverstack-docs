# Incremental data processing

Incremental Build selection and incremental data processing solve different problems. Build decides which definitions to install. Load decides which source changes an installed Table or Folder should apply.

The ordinary data loop does not require another Build:

```text
initial Build + first Load
→ change source data only
→ Load again without Build
→ inspect changed files and rows
```

## The incremental Table contract

An incremental Table returns the candidate rows to insert or update and, when needed, the keys of rows to delete. Weaver compares the staging candidates with the target and applies genuine inserts and updates. Rows that are absent from staging remain in the target; absence is not an implicit delete.

For a Python Table declared with `Incremental: true`, `read()` accepts four useful forms:

| Return value | Meaning |
| --- | --- |
| `staging` | Insert or update candidates, with no delete claim. |
| `(staging, deletes)` | Insert or update candidates and explicit delete keys. |
| `None` | No candidates and no deletes: a successful no-op. |
| `(None, deletes)` | Deletion-only work. Weaver supplies an empty staging frame with the target shape. |

`staging` contains every declared business column. `deletes` contains the declared primary-key columns; an incremental Table therefore requires a primary key. Delete keys can come from CDC tombstones, cancellations, deleted files, an API status, project-specific queries or another source. The target query decides which target keys should be deleted: a source insert, update or delete does not necessarily become the same target operation after filters, joins or aggregation.

SQL-authored Tables express the same contract with result sets. The first result set supplies staging rows. An optional second supplies delete keys and requires both `Incremental: true` and a primary key. Setup statements may precede those result sets. See [Table](../reference/weaver-documents/table.md#body-and-return-contract) for the Spark SQL and T-SQL statement rules.

### A Warehouse Table over an ordinary source

This example keeps the mutable source Table in a separate physical Warehouse named `ParcelSource`. `Warehouse/Operations` is the only managed Warehouse item. Its physical Shortcut presents the external Table locally as `[Source].[Parcel]`; the source Warehouse is not a Build target.

All paths in this section are relative to `examples/parcel-incremental-warehouse`.

#### Configure the managed Warehouse

Create `workspace-config.yml`:

```yaml
workspace: Parcel Development
catalogue: Warehouse/ParcelCatalogue

targets:
  Warehouse/Operations: ParcelOperations
```

Create the `ParcelCatalogue`, `ParcelOperations`, and `ParcelSource` Warehouses in the **Parcel Development** workspace. Do not add `ParcelSource` to `targets`: Build reconciles selected managed items and may prune undeclared co-located content inside them.

Create `Warehouse/Operations/shortcuts.yml`:

```yaml
physical:
  "Warehouse/Operations/Source.Parcel": "Warehouse/ParcelSource/Source.Parcel"
```

This is the supported Warehouse Shortcut declaration surface. `workspace-config.yml` binds the managed destination; `shortcuts.yml` maps the item-local View to the external physical Table. Warehouse physical Shortcuts are limited to the configured workspace.

#### Provision and seed the external source

The source scripts live outside `Warehouse/Operations`, so Weaver does not parse or install them. In the Fabric portal, open a **SQL query connected to the ParcelSource Warehouse** and run `source/ParcelSource/01-setup.sql`:

```sql
if schema_id(N'Source') is null
    exec(N'create schema [Source]');

if object_id(N'[Source].[Parcel]', N'U') is null
begin
    create table [Source].[Parcel] (
        [Parcel ID] varchar(20) not null,
        [Status] varchar(40) not null,
        [Depot] varchar(40) not null,
        [Row update datetime] datetime2(6) not null
    );
end;
```

In the same `ParcelSource` query editor, run `source/ParcelSource/02-seed.sql`:

```sql
delete from [Source].[Parcel];

insert into [Source].[Parcel] (
    [Parcel ID],
    [Status],
    [Depot],
    [Row update datetime]
)
values
    ('P-1001', 'In transit', 'Central', sysdatetime()),
    ('P-1002', 'Delivered', 'South', sysdatetime());
```

Verify source access in that query editor before Build:

```sql
select [Parcel ID], [Status], [Depot], [Row update datetime]
from [Source].[Parcel]
order by [Parcel ID];
```

The query must return `P-1001` and `P-1002`. A missing Warehouse, schema, Table, or permission must be fixed at the external source rather than represented as an empty incremental window.

#### Declare the incremental consumer

Create `Warehouse/Operations/Parcel.CurrentStatus.sql`:

```sql
/*
Table ID: Parcel.CurrentStatus

Description: Current state of active parcels.

Lineage: ParcelSource Source.Parcel.

Primary key: Parcel ID

Incremental: true

Dependencies: []
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

The first result set supplies insert and update candidates. The second supplies explicit primary keys to delete. Both use the bookmark owned by `Warehouse/Operations/Parcel.CurrentStatus`.

`Dependencies: []` is required by the current checker here. T-SQL dependency inference does not resolve `[Source].[Parcel]` to a physical Warehouse Shortcut, even though Build installs that item-local View. The override suppresses only the nonexistent managed producer edge; the external source still has no Weaver-managed ordering.

From the **example project root**, validate and install the managed Warehouse, then run its first Load:

```bash
weaver check
weaver build --item Warehouse/Operations
weaver load Warehouse/Operations --dry-run
weaver load Warehouse/Operations
```

After Build, verify the installed Shortcut from a **SQL query connected to ParcelOperations**:

```sql
select [Parcel ID], [Status], [Depot], [Row update datetime]
from [Source].[Parcel]
order by [Parcel ID];
```

Then query `[Parcel].[CurrentStatus]`; it should contain both seeded parcels.

#### Change source rows, then Load without Build

In the **ParcelSource query editor**, run `source/ParcelSource/03-change.sql`:

```sql
update [Source].[Parcel]
set [Status] = 'Delivered',
    [Row update datetime] = sysdatetime()
where [Parcel ID] = 'P-1001';

update [Source].[Parcel]
set [Status] = 'Cancelled',
    [Row update datetime] = sysdatetime()
where [Parcel ID] = 'P-1002';
```

Verify the two source statuses there, then return to the **example project root** and Load the already installed definition:

```bash
weaver load Warehouse/Operations --dry-run
weaver load Warehouse/Operations
```

`P-1001` is an upsert from the first result set. The update of `P-1002` to `Cancelled` becomes a target delete from the second result set: source change type and target action type differ. Absence from the first result set is not a deletion claim. A hard source deletion leaves no row for either query, so propagation would require retained evidence such as a tombstone, audit row, or CDC record.

The complete checked fixture is `examples/parcel-incremental-warehouse`. Local Check validates its authored shape. Build, Shortcut resolution, Load, and the stated row results require a Fabric workspace and remain pending remote execution.

## Bookmarks separate processing state from source data

`[Row update datetime]` in the example is a source audit datetime. `[_].[Bookmark].[Bookmark datetime]` is the processing boundary owned by this consumer. They are not the same state: the source records when its row changed, while the bookmark records how far this Table's successful Loads have processed.

A Weaver bookmark is this Table or Folder's last successful processing boundary: the UTC instant immediately before its latest clean Load began. Each consumer has its own boundary. A clean Load advances it, including a successful incremental no-op. Failed, rejected, blocked and static-skip outcomes do not advance it.

For a direct source whose audit datetimes use the same time basis, a predicate such as `where [Row update datetime] > @bookmark_datetime` is a simple fit. The 1900 sentinel makes the initial run ask for all retained source rows. This pattern still depends on the source retaining a row or other evidence for every change that still needs a target action until the consumer can read it.

Complex joins and multiple sources may have several audit rhythms rather than one usable `max(updated_at)`. The consumer still owns one bookmark, but each source must interpret that boundary through its own change evidence. One source may use an audit datetime, another CDC or a change table, another `files_since()`, and another an API cursor with overlap or polling logic. The query combines those source-specific interpretations into staging candidates and delete keys.

> **Design background:** The broader change model separates [tracking source changes](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/tracking-changes/) from [translating those changes into target actions](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/responding-to-change/); the Weaver contract above is self-contained, while those pages explain the underlying design in more depth.

Build resets the bookmark of each rebuilt loadable object to the initial boundary. The rebuilt installed generation has not processed prior history, even when an earlier generation of the same logical object had. Its next Load must therefore ask its source logic for all available history.

## Folder history as a change source

This example keeps source files in a separate physical Lakehouse, `ParcelSourceArchive`, outside Weaver's managed targets. A physical Folder Shortcut exposes that source inside the managed `ParcelTracking` Lakehouse. A non-incremental Folder takes complete snapshots through the Shortcut, and the incremental Table consumes only the managed Folder changes since that Table's last clean Load.

All paths in this section are relative to `examples/parcel-incremental`.

### Provision the external Lakehouse

Create the `ParcelCatalogue` Warehouse, `ParcelTracking` Lakehouse, published `ParcelRuntime` Environment, and separate `ParcelSourceArchive` Lakehouse in the **Parcel Development** workspace. Create `workspace-config.yml`:

```yaml
workspace: Parcel Development
catalogue: Warehouse/ParcelCatalogue
environment: ParcelRuntime

targets:
  Lakehouse/Tracking: ParcelTracking
```

`ParcelSourceArchive` is deliberately absent from `targets`. Build reconciles `ParcelTracking` and may prune undeclared co-located content there; it must not select the external archive.

In the Fabric portal, open `ParcelSourceArchive`, create `Files/parcel-status`, and upload these checked files:

- `source/parcel-status/P-1001.csv`
- `source/parcel-status/P-1002.csv`

The complete uploaded files are:

```csv title="P-1001.csv"
Parcel ID,Status,Depot
P-1001,In transit,Central
```

```csv title="P-1002.csv"
Parcel ID,Status,Depot
P-1002,Delivered,South
```

Attach `ParcelSourceArchive` as the default Lakehouse of a **Fabric notebook** and verify the upload there:

```python
from pathlib import Path

source_root = Path("/lakehouse/default/Files/parcel-status")
assert source_root.is_dir(), f"Source directory not found: {source_root}"
assert sorted(path.name for path in source_root.glob("*.csv")) == [
    "P-1001.csv",
    "P-1002.csv",
]
```

This notebook path verifies the attached external Lakehouse only. The installed Folder code below reads the local Shortcut through Weaver's public `path()` interface.

### Declare the physical Folder Shortcut

Create `Lakehouse/Tracking/shortcuts.py`:

```python
from weaver import Shortcut


Parcel__StatusSource = Shortcut(
    shortcut_type="folder",
    target_type="physical",
    target="Lakehouse/ParcelSourceArchive/Files/parcel-status",
)
```

The assignment name creates the local destination `Files/Parcel/StatusSource`. The physical target remains outside Weaver ownership and contributes no managed producer or project dependency edge.

### Declare the snapshot Folder

Create `Lakehouse/Tracking/Files/Parcel__StatusFiles.py`:

```python
"""
Folder ID: Parcel.StatusFiles

Description: Current parcel status snapshots, one CSV file per parcel.

Lineage: A carrier snapshot represented by this example.

File key: "*.csv"

Incremental: false
"""

import shutil

from shortcuts import Parcel__StatusSource
from weaver import Folder


class Parcel__StatusFiles(Folder):
    def read(self):
        source_root = Parcel__StatusSource(self).path()
        if not source_root.is_dir():
            raise FileNotFoundError(
                f"Parcel status source directory not found: {source_root}"
            )

        staging = self.staging_folder()
        for source in sorted(source_root.glob("*.csv")):
            shutil.copy2(source, staging.path / source.name)
        return staging
```

The deployed `shortcuts` module supplies a Folder reader. Its `path()` method returns the resolved Lakehouse's mounted `pathlib.Path` for ordinary Python file access; `spark_path()` is a separate string interface for Spark and is not passed to `pathlib`.

The source existence check happens before Weaver issues or populates staging. An unavailable source raises `FileNotFoundError`. An existing but intentionally empty source directory passes the check and remains a valid complete snapshot. `Incremental: false` makes each successful Load a complete snapshot, so a source file that disappears is retired from the managed Folder. Weaver records inserted, updated, and deleted managed paths; byte-identical files are not updates.

### Declare the incremental Table

Create `Lakehouse/Tracking/Tables/Parcel__CurrentStatus.py`:

```python
"""
Table ID: Parcel.CurrentStatus

Description: The latest status supplied for each parcel.

Lineage: Parcel status snapshots managed by Parcel.StatusFiles.

Primary key: Parcel ID

Incremental: true

Schema:
  Parcel ID: string
  Status: string
  Depot: string
"""

from Files.Parcel__StatusFiles import Parcel__StatusFiles
from weaver import Table


class Parcel__CurrentStatus(Table):
    def read(self):
        source = Parcel__StatusFiles(self)
        bookmark = self.bookmark()
        changed = source.files_since(bookmark)
        deleted = source.deleted_since(bookmark)

        staged = None
        if changed:
            root = source.spark_path()
            staged = (
                self.spark.read.option("header", True)
                .csv([f"{root}/{path.name}" for path in sorted(changed)])
                .select(*self.columns())
            )

        deletes = None
        if deleted:
            parcel_ids = [(path.stem,) for path in sorted(deleted)]
            deletes = self.spark.createDataFrame(parcel_ids, ["Parcel ID"])

        if staged is None and deletes is None:
            return None
        return staged, deletes
```

The Folder import establishes the managed dependency, so item-wide Load runs `Parcel.StatusFiles` before `Parcel.CurrentStatus`. The physical Shortcut import in the Folder records an external boundary, not a managed producer.

The bookmark belongs to `Parcel.CurrentStatus`, not to the source Folder. `files_since()` returns current managed files whose latest event is strictly after that boundary. `deleted_since()` returns paths whose latest event is a deletion after the boundary; those paths normally no longer exist. The code maps deleted filenames to the Table's declared `Parcel ID` key, making Folder deletions explicit Table delete claims.

### Establish the first boundary

From the **example project root**, check and install the declarations once:

```bash
weaver check
weaver build --item Lakehouse/Tracking
```

After Build, attach `ParcelTracking` as the default Lakehouse of a **Fabric notebook** and verify the installed Shortcut before Load:

```python
from pathlib import Path

shortcut_root = Path("/lakehouse/default/Files/Parcel/StatusSource")
assert shortcut_root.is_dir(), f"Shortcut source not visible: {shortcut_root}"
assert sorted(path.name for path in shortcut_root.glob("*.csv")) == [
    "P-1001.csv",
    "P-1002.csv",
]
```

Then, from the **example project root**, run the first Load:

```bash
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
```

The first Folder Load publishes both files and records their insertions. The Table has its initial bookmark, so its first read includes both changes and inserts two rows. A clean Load records a new Table bookmark at the instant immediately before that read began.

Inspect the managed Folder and `Parcel.CurrentStatus` in `ParcelTracking`. The Table should contain `P-1001` and `P-1002`.

### Change source data, then Load without Build

Do not edit either Weaver document. In a **Fabric notebook with `ParcelSourceArchive` attached as its default Lakehouse**, replace `P-1001.csv` and delete `P-1002.csv`:

```python
from pathlib import Path

source_root = Path("/lakehouse/default/Files/parcel-status")
assert source_root.is_dir(), f"Source directory not found: {source_root}"
(source_root / "P-1001.csv").write_text(
    "Parcel ID,Status,Depot\nP-1001,Delivered,Central\n",
    encoding="utf-8",
)
(source_root / "P-1002.csv").unlink()

assert sorted(path.name for path in source_root.glob("*.csv")) == ["P-1001.csv"]
```

From the **example project root**, run Load against the already installed definitions:

```bash
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
```

There is deliberately no `weaver build` in this sequence. The Folder publishes one changed file and one deletion. The Table reads both events from its previous clean boundary, updates `P-1001`, and deletes `P-1002` by primary key.

Inspect three results:

- `Files/Parcel/StatusFiles` contains the current `P-1001.csv` and no `P-1002.csv`;
- `Parcel.CurrentStatus` contains one `P-1001` row with status `Delivered`; and
- the latest Load activity reports the Folder changes and the Table's updated and deleted rows.

A later clean run with no source changes reaches the Table's `return None`. That no-op still consumes a complete source window and advances the bookmark.

Local Check validates the complete fixture's authored shape. Physical Shortcut creation, mounted-path access, Load, and the stated file and row results require Fabric and remain pending remote execution.

## Declaration changes cross the Build boundary

The sequence above changes data while leaving the installed code and metadata alone. If you instead edit either Weaver document, the installed declaration does not change until Build runs:

```text
edit declaration
→ check
→ Build
→ Load the new installed generation
```

Build can select changed work and affected descendants. For each loadable object it rebuilds, Weaver resets the current Load state and bookmark to the initial boundary. The next Load therefore asks that installed generation for all available history, not only events since the pre-Build bookmark. In the normal development loop, use `weaver load --stale` after Build to run the objects whose state is now non-Green.

That reset is why editing a source constant inside a Weaver document and rebuilding it is not an ordinary incremental-data demonstration: it combines a declaration change, Build impact and bookmark reset with the data change being measured.

Use [Load behaviour](../reference/operation-behaviour/load.md) for exact bookmark, reload and selection rules. [Python authored objects](../reference/python/objects.md) defines the Folder and Table return forms, and [Row auditing and operational history](row-auditing-and-operational-history.md) explains where current state and Load activity are recorded.
