# Incremental data processing

Incremental Build selection and incremental data processing solve different problems. Build decides which definitions to install. Load decides which source changes an installed Table or Folder should apply.

The ordinary data loop does not require another Build:

```text
initial Build + first Load
→ change source data only
→ Load again without Build
→ inspect changed files and rows
```

The example below keeps current parcel status in a Table. A snapshot Folder copies CSV files from an incoming area, and the incremental Table consumes only the Folder changes since that Table's last clean Load.

## Prerequisites

- Create or reuse a project containing `Lakehouse/Tracking`.
- Publish the project's Fabric Environment; both documents run Python in Fabric.
- Make the external source snapshot available to the Fabric Spark session at `/mnt/parcel-source/parcel-status`. Keep this path outside the Lakehouse target that Build reconciles.

The mounted directory is source data, not a Folder Weaver manages. The managed destination will be `Files/Parcel/StatusFiles` in `Lakehouse/Tracking`. Replace the example mount with the source acquisition used by your project.

## Declare the snapshot Folder

Create `Lakehouse/Tracking/Files/Parcel__StatusFiles.py`:

```python
"""
Folder ID: Parcel.StatusFiles

Description: Current parcel status snapshots, one CSV file per parcel.

Lineage: CSV snapshots supplied in the Lakehouse incoming area.

File key: "*.csv"

Incremental: false
"""

from pathlib import Path
import shutil

from weaver import Folder


SOURCE = Path("/mnt/parcel-source/parcel-status")


class Parcel__StatusFiles(Folder):
    def read(self):
        staging = self.staging_folder()
        for source in SOURCE.glob("*.csv"):
            shutil.copy2(source, staging.path / source.name)
        return staging
```

`Incremental: false` makes each successful Folder Load a complete snapshot of the managed `*.csv` files. A source file that disappears from the incoming directory is therefore retired from the managed Folder. After publication, Weaver records inserted, updated and deleted managed paths in the Folder's change history; byte-identical files are not updates.

## Declare the incremental Table

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

        staging = None
        if changed:
            root = source.spark_path()
            staging = (
                self.spark.read.option("header", True)
                .csv([f"{root}/{path.name}" for path in sorted(changed)])
                .select(*self.columns())
            )

        deletes = None
        if deleted:
            parcel_ids = [(path.stem,) for path in sorted(deleted)]
            deletes = self.spark.createDataFrame(parcel_ids, ["Parcel ID"])

        if staging is None and deletes is None:
            return None
        return staging, deletes
```

The import establishes the managed dependency, so an item-wide Load runs the Folder before the Table.

The bookmark belongs to `Parcel.CurrentStatus`, not to the source Folder. `files_since()` returns current managed files whose latest recorded event is strictly after that boundary. `deleted_since()` returns paths whose latest event is a deletion after the boundary; those paths normally no longer exist.

An incremental Table treats staging as a change set. Rows absent from staging remain in the target. Deletion therefore requires the second return value, containing the declared primary-key columns. `None` means a successful no-op when neither window contains work.

## Establish the first boundary

Place these two source files in `/mnt/parcel-source/parcel-status`:

```csv title="P-1001.csv"
Parcel ID,Status,Depot
P-1001,In transit,Central
```

```csv title="P-1002.csv"
Parcel ID,Status,Depot
P-1002,Delivered,South
```

Check and install the declarations once, then run the first Load:

```bash
weaver check
weaver build --item Lakehouse/Tracking
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
```

The first Folder Load publishes both files and records their insertions. The Table has its initial bookmark, so its first read includes both changes and inserts two rows. A clean Load records a new Table bookmark at the instant immediately before that read began.

Inspect the managed Folder and `Parcel.CurrentStatus` in the Lakehouse. The Table should contain `P-1001` and `P-1002`.

## Change source data, then Load without Build

Do not edit either Weaver document. In the incoming source directory:

1. replace `P-1001.csv` with:

    ```csv
    Parcel ID,Status,Depot
    P-1001,Delivered,Central
    ```

2. delete `P-1002.csv`.

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

A later clean run with no source changes reaches the Table's `return None`. That no-op still consumes a complete source window and advances the bookmark. Failed, rejected, blocked and static-skip outcomes do not advance it.

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
