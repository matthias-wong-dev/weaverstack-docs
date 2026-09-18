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

### A Warehouse change-feed Table

This complete T-SQL document reads an external `staging.ParcelChanges` feed. Operation codes `I` and `U` become staging candidates; `D` supplies explicit delete keys. `Dependencies: []` keeps the external staging table out of Weaver's managed dependency graph.

Create `Warehouse/Operations/Parcel.CurrentStatus.sql`:

```sql
/*
Table ID: Parcel.CurrentStatus

Description: Current parcel state from an external change feed.

Lineage: staging.ParcelChanges.

Primary key: Parcel ID

Incremental: true

Dependencies: []
*/
select [Parcel ID]
     , [Status]
     , [Depot]
from [staging].[ParcelChanges]
where [Operation code] in ('I', 'U');

select [Parcel ID]
from [staging].[ParcelChanges]
where [Operation code] = 'D';
```

The checked fixture is `examples/parcel-incremental-warehouse/Warehouse/Operations/Parcel.CurrentStatus.sql`. Check can parse the document locally. Build must query a bound Fabric Warehouse to infer the SQL result shape, and Load executes the installed T-SQL there.

## Bookmarks separate processing state from source data

`max(updated_at)` describes one query over one source shape. It can be enough for a direct source copy, but it does not record whether this particular consumer completed a load. A filtered target may not contain the source's latest timestamp, and a join or multi-source query can change through several routes that no single target column represents.

A Weaver bookmark is this Table or Folder's last successful processing boundary: the UTC instant immediately before its latest clean Load began. Each consumer has its own boundary. A clean Load advances it, including a successful incremental no-op. Failed, rejected, blocked and static-skip outcomes do not advance it.

The bookmark says where the consumer got to; source logic translates that boundary into source-specific change detection. That logic may use `files_since()`, pipeline-managed audit datetimes, CDC or change tables, source event time, a translated API cursor, or several source queries whose changes are combined into staging and delete drivers. External source time may need its own polling or cursor mapping before it can be compared with the Weaver boundary.

> **Design background:** The broader change model separates [tracking source changes](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/tracking-changes/) from [translating those changes into target actions](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/responding-to-change/); the Weaver contract above is self-contained, while those pages explain the underlying design in more depth.

Build resets the bookmark of each rebuilt loadable object to the initial boundary. The rebuilt installed generation has not processed prior history, even when an earlier generation of the same logical object had. Its next Load must therefore ask its source logic for all available history.

## Folder history as a change source

The example below implements the general contract with Weaver-managed Folder history. It keeps current parcel status in a Table. A snapshot Folder copies CSV files from an incoming area, and the incremental Table consumes only the Folder changes since that Table's last clean Load.

### Prerequisites

- Create or reuse a project containing `Lakehouse/Tracking`.
- Publish the project's Fabric Environment; both documents run Python in Fabric.
- Use the physical Tracking Lakehouse as the source host for this example. In the Fabric portal, open that Lakehouse, create `Files/parcel-source/parcel-status`, and upload:
  - `examples/parcel-incremental/source/parcel-status/P-1001.csv`
  - `examples/parcel-incremental/source/parcel-status/P-1002.csv`

`Files/parcel-source/parcel-status` is source data, not a Folder Weaver manages. Keep it outside the managed destination, `Files/Parcel/StatusFiles`. Build and Load act on the latter through `Parcel.StatusFiles`; neither treats the source directory as that Folder's destination.

Attach the physical Tracking Lakehouse to a Fabric notebook as its default Lakehouse, then verify the upload before running Load:

```python
from pathlib import Path

source_root = Path("/lakehouse/default/Files/parcel-source/parcel-status")
assert source_root.is_dir(), f"Source directory not found: {source_root}"
assert sorted(path.name for path in source_root.glob("*.csv")) == [
    "P-1001.csv",
    "P-1002.csv",
]
```

The `/lakehouse/default` path is only this verification notebook's attached-Lakehouse path. The authored Folder below resolves its installed Lakehouse instead.

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

from pathlib import Path
import shutil

from weaver import Folder


class Parcel__StatusFiles(Folder):
    def read(self):
        source_root = Path(self.lakehouse.files_root()) / "parcel-source" / "parcel-status"
        if not source_root.is_dir():
            raise FileNotFoundError(
                f"Parcel status source directory not found: {source_root}"
            )

        staging = self.staging_folder()
        for source in source_root.glob("*.csv"):
            shutil.copy2(source, staging.path / source.name)
        return staging
```

The source-directory check happens before Weaver issues or populates staging. An unavailable source raises `FileNotFoundError`; an available but intentionally empty source directory remains a valid complete snapshot.

`Incremental: false` makes each successful Folder Load a complete snapshot of the managed `*.csv` files. A source file that disappears from the source directory is therefore retired from the managed Folder. After publication, Weaver records inserted, updated and deleted managed paths in the Folder's change history; byte-identical files are not updates.

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

The import establishes the managed dependency, so an item-wide Load runs the Folder before the Table.

The bookmark belongs to `Parcel.CurrentStatus`, not to the source Folder. `files_since()` returns current managed files whose latest recorded event is strictly after that boundary. `deleted_since()` returns paths whose latest event is a deletion after the boundary; those paths normally no longer exist. The method maps deleted filenames to the Table's declared `Parcel ID` key, making Folder deletions explicit Table delete claims.

### Establish the first boundary

The two uploaded fixture files contain:

```csv title="P-1001.csv"
Parcel ID,Status,Depot
P-1001,In transit,Central
```

```csv title="P-1002.csv"
Parcel ID,Status,Depot
P-1002,Delivered,South
```

After the notebook verification succeeds, check and install the declarations once, then run the first Load:

```bash
weaver check
weaver build --item Lakehouse/Tracking
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
```

The first Folder Load publishes both files and records their insertions. The Table has its initial bookmark, so its first read includes both changes and inserts two rows. A clean Load records a new Table bookmark at the instant immediately before that read began.

Inspect the managed Folder and `Parcel.CurrentStatus` in the Lakehouse. The Table should contain `P-1001` and `P-1002`.

### Change source data, then Load without Build

Do not edit either Weaver document. In the same Fabric notebook, replace `P-1001.csv` and delete `P-1002.csv` from the same source directory:

```python
from pathlib import Path

source_root = Path("/lakehouse/default/Files/parcel-source/parcel-status")
(source_root / "P-1001.csv").write_text(
    "Parcel ID,Status,Depot\nP-1001,Delivered,Central\n",
    encoding="utf-8",
)
(source_root / "P-1002.csv").unlink()

assert [path.name for path in source_root.glob("*.csv")] == ["P-1001.csv"]
```

Run Load again against the already installed definitions:

```bash
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
```

There is deliberately no `weaver build` in this sequence. The Folder publishes one changed file and one deletion. The Table reads both events from its previous clean boundary, updates `P-1001` and deletes `P-1002` by primary key.

Inspect three results:

- `Files/Parcel/StatusFiles` contains the current `P-1001.csv` and no `P-1002.csv`;
- `Parcel.CurrentStatus` contains one `P-1001` row with status `Delivered`; and
- the latest Load activity reports the Folder changes and the Table's updated and deleted rows.

A later clean run with no source changes reaches the Table's `return None`. That no-op still consumes a complete source window and advances the bookmark.

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
