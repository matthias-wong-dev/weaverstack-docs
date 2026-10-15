# Loading changes and bookmarks

Update one carrier file, remove another, and Load the installed pipeline again. The Folder records what changed; the incremental Table uses its own bookmark to read those changes and apply updates and explicit deletes.

Continue the [Landing project](tests.md) in the same folder. Keep Events, Event, CurrentStatus and their validations. Add a separate `Parcel.StatusFiles` Folder and incremental `Parcel.LiveStatus` Table for changing carrier snapshots. The original constant example stays available and unchanged.

## Let the consumer remember its progress

The bookmark belongs to the consumer, not the source. It is the UTC instant immediately before that consumer's last clean Load began. Two Tables consuming the same Folder therefore read changes using separate boundaries; loading one does not move the other's bookmark. A clean no-op advances the boundary too; failed or rejected work does not.

`Incremental: true` makes a Table's returned rows candidates for insert or update. Missing candidates do not delete existing rows. This example also returns explicit primary-key delete rows derived from removed filenames. [Table reference](../reference/weaver-documents/table.md#body-and-return-contract) owns all accepted return forms.

## Provision the external Lakehouse

Keep your working `workspace-config.yml`, catalogue, Landing target and published Environment. Create or reuse a separate external **ParcelSourceArchive** Lakehouse in the same workspace for the mutable carrier data. Do not add it to `targets`: Build owns the managed target and may prune undeclared co-located content; the external archive must remain outside that scope.

In the Fabric portal, open `ParcelSourceArchive`, create `Files/parcel-status`, and upload two CSV files with the contents below:

- `P-1001.csv`
- `P-1002.csv`

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

## Declare the physical Folder Shortcut

Create `Lakehouse/Landing/shortcuts.py`:

```python
from weaver import Shortcut


Parcel__StatusSource = Shortcut(
    shortcut_type="folder",
    target_type="physical",
    target="Lakehouse/ParcelSourceArchive/Files/parcel-status",
)
```

The assignment name creates the local destination `Files/Parcel/StatusSource`. The physical target remains outside Weaver ownership and contributes no managed producer or project dependency edge.

## Declare the snapshot Folder

Create `Lakehouse/Landing/Files/Parcel__StatusFiles.py`:

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

## Declare the incremental Table

Create `Lakehouse/Landing/Tables/Parcel__LiveStatus.py`:

```python
"""
Table ID: Parcel.LiveStatus

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


class Parcel__LiveStatus(Table):
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

The Folder import establishes the managed dependency, so item-wide Load runs `Parcel.StatusFiles` before `Parcel.LiveStatus`. The physical Shortcut import in the Folder records an external boundary, not a managed producer.

The bookmark belongs to `Parcel.LiveStatus`, not to the source Folder. `files_since()` returns current managed files whose latest event is strictly after that boundary. `deleted_since()` returns paths whose latest event is a deletion after the boundary; those paths normally no longer exist. The code maps deleted filenames to the Table's declared `Parcel ID` key, making Folder deletions explicit Table delete claims.

## Establish the first boundary

Use the [matching Fabric runtime](runtime.md) already published for Landing. If you changed its package requirements, republish; otherwise these added project files do not require another Environment publication. From the **same project root**, check and install the additions:

```bash
weaver check
weaver build --item Lakehouse/Landing
```

After Build, attach `Landing` as the default Lakehouse of a **Fabric notebook** and verify the installed Shortcut before Load:

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
weaver load Lakehouse/Landing --dry-run
weaver load Lakehouse/Landing
```

The first Folder Load should publish both files and record their insertions. The Table starts at the initial bookmark, so its first read should include both changes and insert two rows. A clean Load records a new Table bookmark at the instant immediately before that read began.

In the same notebook, inspect the managed Table:

```python
spark.sql("SELECT `Parcel ID`, Status, Depot FROM Parcel.LiveStatus ORDER BY `Parcel ID`").show(truncate=False)
```

It should contain `P-1001` as `In transit` at `Central` and `P-1002` as `Delivered` at `South`. The managed Folder should contain both CSV files.

In a **SQL query connected to Catalogue**, record the Table's first successful boundary:

```sql
select [Bookmark datetime]
from [_].[Bookmark]
where [Item type] = N'Lakehouse'
  and [Item name] = N'Landing'
  and [Schema name] = N'Tables/Parcel'
  and [Object name] = N'LiveStatus';
```

## Change source data, then Load without Build

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
weaver load Lakehouse/Landing --dry-run
weaver load Lakehouse/Landing
```

There is deliberately no `weaver build` in this sequence. The Folder should publish one changed file and one deletion. The Table should read both events from its previous clean boundary, update `P-1001`, and delete `P-1002` by primary key.

Inspect three results:

- `Files/Parcel/StatusFiles` contains the current `P-1001.csv` and no `P-1002.csv`;
- `Parcel.LiveStatus` contains one `P-1001` row with status `Delivered`; and
- the latest Load activity reports the Folder changes and the Table's updated and deleted rows.

Run `weaver load Lakehouse/Landing` once more without changing the source. The clean run reaches the Table's `return None`: managed files and target rows remain unchanged, while the consumer bookmark advances again.

## Build only when the declaration changes

The second Load changes source data only. Editing a Folder or Table instead changes the installed code only after Check and Build. For each rebuilt loadable object, Build resets current Load state and its bookmark to the initial boundary; the next Load must ask that new generation for all available history. Use `weaver load Lakehouse/Landing --stale` for post-Build catch-up, not as a substitute for the data-only sequence above.

With a working mutable source, [Shortcuts and existing data](shortcuts.md) explains how to choose a managed logical source or an external physical boundary. For shared run state and recovery, continue to [Catalogue and Health](../estate/catalogue-and-health.md) and [Recover failed work](../estate/recovery.md).

The retained [incremental processing deep dive](../advanced/incremental-data-processing.md) covers source change evidence and other source types. [Load behaviour](../reference/operation-behaviour/load.md), [Python authored objects](../reference/python/objects.md) and [Row auditing and operational history](../advanced/row-auditing-and-operational-history.md) own exact processing and inspection rules.
