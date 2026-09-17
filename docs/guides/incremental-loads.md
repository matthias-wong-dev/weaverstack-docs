# Load changed parcel files incrementally

This guide keeps a current parcel-status Table in sync with a managed Folder. The Folder publishes a complete file snapshot; the Table reads only files changed since its own last clean load and explicitly retires rows for deleted files.

## Prerequisites

- [Install Weaver](../get-started/installation.md) and confirm `weaver --version` works.
- Create or reuse a project with a logical `Lakehouse/Tracking` item. [First project](../get-started/first-project.md) covers initialisation and workspace binding.
- Publish the project's Fabric Environment before Load. Both declarations below run Python in Fabric.

The checked fixture for this guide is `examples/parcel-incremental/`.

## Add the managed Folder

Create this structure beneath the project root:

```text
Lakehouse/
└── Tracking/
    ├── Files/
    │   └── Parcel__StatusFiles.py
    └── Tables/
        └── Parcel__CurrentStatus.py
```

Create `Lakehouse/Tracking/Files/Parcel__StatusFiles.py`:

```python
"""
Folder ID: Parcel.StatusFiles

Description: Current parcel status snapshots, one CSV file per parcel.

Lineage: A carrier snapshot represented by this example.

File key: "*.csv"

Incremental: false
"""

from weaver import Folder

SNAPSHOT = {
    "P-1001.csv": "Parcel ID,Status,Depot\nP-1001,In transit,Central\n",
    "P-1002.csv": "Parcel ID,Status,Depot\nP-1002,Delivered,South\n",
}


class Parcel__StatusFiles(Folder):
    def read(self):
        staging = self.staging_folder()
        for name, content in SNAPSHOT.items():
            (staging.path / name).write_text(content, encoding="utf-8")
        return staging
```

`Incremental: false` means each successful Folder load treats staging as the complete managed snapshot. A file removed from `SNAPSHOT` is removed from the destination. Weaver records changes to files matching `File key` in the Folder's change history; files outside that managed scope do not enter this history.

Replace the in-module `SNAPSHOT` with source acquisition appropriate to your project. Keep the declaration and the `staging_folder()` return contract unchanged.

## Read the Folder from the Table's bookmark

Create `Lakehouse/Tracking/Tables/Parcel__CurrentStatus.py`:

```python
"""
Table ID: Parcel.CurrentStatus

Description: The latest status supplied for each parcel.

Lineage: $Files/Parcel.StatusFiles

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

`self.bookmark()` is the Table's boundary, not the Folder's. It is the UTC instant immediately before this Table's latest clean load began. Before the first clean load it is a sentinel, so the first read includes all recorded files.

`files_since(bookmark)` returns current files whose latest change is strictly after the boundary. `deleted_since(bookmark)` returns paths retired strictly after it; those paths normally no longer exist. Both mappings also carry each change time as their value. This example only needs their path keys.

The Table is incremental, so absence from the changed-file window does not delete a row. The second return value is an explicit delete claim. It contains the declared primary key derived from each deleted filename. Returning `None` when both windows are empty is a successful no-op and avoids starting a table reconciliation job.

## Check, build and load

From the project root, run the local check:

```bash
weaver check
```

A successful check confirms that metadata, paths, identities, the import dependency and Python syntax parse. It does not execute `read()`, Spark or Folder change-history access, and it does not prove the load will run in Fabric.

Install the declarations and publish the Environment:

```bash
weaver build --item Lakehouse/Tracking
weaver fabric environment publish \
  --path Environment/Weaver.Environment
```

Preview and run the item-wide load:

```bash
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
weaver health --item Lakehouse/Tracking
```

The dry run should place `Files/Parcel.StatusFiles` before `Tables/Parcel.CurrentStatus`. In Fabric, the first successful Load should leave two managed CSV files and two rows in `Parcel.CurrentStatus`. Confirm those outcomes in the Lakehouse; local `weaver check` cannot observe them.

## Exercise a changed file and a deletion

Edit `SNAPSHOT`: change the status in `P-1001.csv` and remove the `P-1002.csv` entry. Then reinstall the changed source and load the item:

```bash
weaver check
weaver build --item Lakehouse/Tracking
weaver load Lakehouse/Tracking --dry-run
weaver load Lakehouse/Tracking
```

The Folder load records the changed `P-1001.csv` and deleted `P-1002.csv`. The dependent Table reads both changes from the same Table bookmark, updates the `P-1001` row and deletes the `P-1002` row by primary key. Verify the resulting row and the Load statistics in Fabric.

A later clean run with no Folder changes reaches `return None`. That no-op is still a clean load, so the Table bookmark advances. A failed load or a load with rejected rows does not advance it; the next attempt reads from the previous clean boundary.

## Recover without corrupting the window

Use reload only when a Table must be reconstructed from zero:

```bash
weaver load Lakehouse/Tracking \
  --name Tables/Parcel.CurrentStatus \
  --reload
```

Reload resets the selected Table's bookmark, empties it before `read()` and then runs the incremental code from the initial boundary. It does not reload the Folder; Folders do not support reload. Because name selection runs exactly the named object, make sure the Folder's current files contain every row needed to reconstruct the Table.

`Static: true` is a separate load-once policy. After an object's first clean load, later ordinary loads record a static skip without calling `read()`. A Table reload clears that state and runs the Table again. Do not mark a changing Folder or Table static.

If `files_since()` reports managed files without usable change history, load the Folder successfully to publish a new change before retrying the Table. Do not manufacture `_changes` records or edit the [catalogue](../core-concepts/catalogue.md) by hand.

## Next action

Use [Weaver documents](../core-concepts/weaver-documents.md) for Folder and Table ownership, [Weaver operations](../core-concepts/weaver-operations.md) for the Build/Load boundary, and [Dependencies](../core-concepts/dependencies.md) for item-wide ordering. [Development cycle](../core-concepts/development-cycle.md) explains how these edits move through a mirrored estate. Command selection is in the [CLI reference](../reference/cli.md); clean-load recording and failure behaviour are in the [Load contract](../contracts/load.md).
