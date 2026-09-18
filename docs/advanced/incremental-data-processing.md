# Incremental data processing


---

## Load changed parcel files incrementally

This guide keeps a current parcel-status Table in sync with a managed Folder. The Folder publishes a complete file snapshot; the Table reads only files changed since its own last clean load and explicitly retires rows for deleted files. The [Incremental-processing contract](incremental-data-processing.md) owns the precise bookmark, change and commit semantics.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Create or reuse a project with a logical `Lakehouse/Tracking` item. [First project](../getting-started/first-project.md) covers initialisation and workspace binding.
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

Use [Weaver documents](../core-concepts/weaver-documents.md) for Folder and Table ownership, [Weaver operations](../core-concepts/build-load-and-test.md) for the Build/Load boundary, and [Dependencies](../core-concepts/dependencies.md) for item-wide ordering. [Development cycle](../basics/development-cycle.md) explains how these edits move through a mirrored estate. Command selection is in the [CLI reference](../reference/cli.md); clean-load recording and failure behaviour are in the [Load contract](../reference/operation-behaviour/load.md).

---

## Incremental-processing contract

Incremental processing reconciles one installed Table or Folder against a boundary recorded in the catalogue. The authored declaration decides whether the source is a complete replacement or an incremental change set. Load does not infer incremental intent from the amount of data returned.

## Bookmark boundary

A bookmark is the timezone-aware UTC instant immediately before an object's latest clean load began. A newly built or reset loadable object has the sentinel boundary, which asks an incremental source for its complete available history.

The boundary is captured before authored `read()` work starts. It advances only after a clean successful load, including a successful incremental no-op that returns `None`. It does not advance after:

- a failed or errored load;
- a blocked or pending node;
- a load that completed with rejected input; or
- a static skip that consumed no source window.

Bookmarks are keyed by logical item, Lakehouse area where applicable, schema and object. A Table and Folder with the same `Schema.Object` therefore have distinct boundaries.

Rebuilding a loadable object resets its current bookmark and Load status for the new installed generation. Unchanged objects keep their boundaries.

## Keyed Table updates and deletes

An incremental Table has a declared primary key. Its staging rows are a partial change set:

- a key absent from the target is inserted;
- a key already present is updated when its comparison values changed;
- a target key absent from staging is retained; and
- a delete occurs only when the authored result explicitly claims that primary key.

`read()` may return staging alone or `(staging, deletes)`. The delete value is a relation containing the declared primary-key columns. `(None, deletes)` is a deletion-only load. `None` or `(None, None)` is a successful no-op for an incremental Table.

A non-incremental keyed Table treats staging as the complete source. Target rows absent from staging are deleted, and the authored method must not return a separate delete claim. An unkeyed Table replaces its contents wholesale. Returning `None` for a non-incremental Table is invalid because an empty complete source must be represented as an empty staging relation.

Incoming rows that violate recoverable key or nullability checks can be rejected under the selected fault-tolerance policy. A proposed incremental merge that would leave a declared unique key duplicated is a fatal target-validity failure under either policy.

## Folder publication and history

A Folder publishes files matching its declared managed scope. An incremental Folder adds or replaces staged files and deletes only explicitly named files. A non-incremental Folder treats staging as the complete managed snapshot and retires managed files omitted from it. Files outside the declared managed scope are not removed by replacement.

After a Folder changes, Weaver writes a change document recording inserted, updated and deleted relative paths. Byte-identical staged files are not recorded as updates. Change history is the evidence used by:

- `files_since(bookmark)` — current files whose latest recorded event after the boundary is an insert or update;
- `deleted_since(bookmark)` — paths whose latest recorded event after the boundary is a delete; and
- `latest_files()` — surviving files from the newest recorded change that left files in place.

The boundary is strict: an event at the bookmark instant is excluded. A later event for the same path supersedes an earlier event in the requested window. Returned change times are UTC, and a naive bookmark is invalid.

Physical files without a change document are not historical events. Before an ordinary non-static Folder's first authored read, Weaver records existing destination files once when no Folder history exists, so retained files enter subsequent history. Existing history suppresses that adoption. The change-history directory is Weaver metadata rather than managed Folder content.

An incremental Folder may return `None` for a no-op or `(None, deletes)` for deletion-only work. A non-incremental Folder must return its issued staging folder. Folders do not support reload.

## Stability thresholds

A keyed Table can declare delete and update percentage thresholds and a minimum target-row count at which they apply. Defaults are 5% deletes, 20% updates and 1,000,000 target rows.

The gate is evaluated after the proposed insert, update and delete sets are settled but before the target is mutated. It does not apply to wholesale replacement, an empty target or a target smaller than the minimum. A change breaches only when its percentage is strictly greater than the declared limit.

A breach leaves the target unchanged through that reconciliation path and records failure evidence. Fault tolerance does not make the proposed change acceptable. The public Python Table load can explicitly waive the stability gate for that invocation; the waiver does not alter the installed declaration.

## Stale selection

`load --stale`, or `stale=True`, narrows the selected item boundary to loadable objects whose Load health is not Green. This includes pending, failed, errored, blocked, rejected and stale objects. It uses the same freshness assessment and zoned `as_of` cutoff as Health.

Stale selection does not include borrowed objects as destination work, does not select Views and does not widen into unselected items. A local descendant can be selected because a borrowed ancestor advanced. A plan with no non-Green local work succeeds without mutation.

`as_of` is valid on Load only with stale selection. Stale and reload modes cannot be combined.

## Reload and commit boundaries

Reload applies only to selected Tables. For each Table as the run reaches it, Weaver:

1. writes and durably flushes Pending Load status and the sentinel bookmark;
2. empties the target while preserving the installed Table definition;
3. calls the ordinary authored load against the empty target and reset boundary; and
4. records the resulting Load status, statistic and clean bookmark where applicable.

The reset occurs per reached node, not across the whole plan. A fail-fast run does not reset a later node it never reaches. Reload does not add descendants or reset unselected Tables. Selecting a Folder makes the reload request invalid before execution.

If execution fails after reset or emptying, the old bookmark and target contents are not restored. The Table remains in the state established by the reset and partial execution evidence. A later reload is a new reconstruction attempt.

Ordinary successful Table and Folder loads publish target changes before their clean bookmark is committed. Catalogue recording is part of completion: an operation does not report clean success before its required state writes are durable. There is no operation-wide transaction across several selected objects.

## Defined behaviour

The Incremental-processing contract specifies that Weaver:

1. uses the instant before a clean load starts as that object's next incremental boundary;
2. advances a bookmark only for a clean success, including a no-op;
3. applies keyed incremental inserts and updates from staging and deletes only from explicit primary-key claims;
4. treats non-incremental staging as complete source state;
5. records Folder insert, update and delete history and queries it with a strict boundary;
6. selects stale work from the same assessment as Health without widening item scope;
7. evaluates stability before target mutation and keeps it independent of fault tolerance; and
8. resets and flushes each reached Table before reload empties and rereads it, without rollback.
