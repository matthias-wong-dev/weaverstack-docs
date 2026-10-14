# Shortcuts and existing data

Read existing Fabric data through a local Lakehouse name without copying it into another authored source Table. Use a physical Shortcut for externally owned data; use a logical Shortcut when another Weaver item owns the producer.

The Landing pipeline remains unchanged. This optional task adds access to a separate carrier archive. The [incremental variation](incremental.md) uses this same physical boundary in `Lakehouse/Tracking`, then snapshots the files and consumes their changes. Continue there if you want the complete loadable pipeline rather than access alone.

## Expose an external carrier archive

Use an existing `ParcelSourceArchive` Lakehouse in the configured workspace, outside this project's managed targets, containing `Files/parcel-status`. Verify the source exists and is readable before Build. Create `Lakehouse/Landing/shortcuts.py`:

```python
from weaver import Shortcut


Parcel__StatusSource = Shortcut(
    shortcut_type="folder",
    target_type="physical",
    target="Lakehouse/ParcelSourceArchive/Files/parcel-status",
)
```

The assignment creates the local Folder Shortcut `Files/Parcel/StatusSource`. Build manages that destination, not the external archive. Do not add `ParcelSourceArchive` as a managed target: Build may prune undeclared co-located content inside selected managed items. No managed producer or project graph edge is created for the external source.

From the existing Landing project root, install the addition:

```bash
weaver check
weaver build --item Lakehouse/Landing
```

Check validates the declaration without contacting Fabric. Build should create the local Shortcut; it has no separate Load. In a Fabric notebook with the **Landing destination Lakehouse** attached as default, verify the installed path and its files:

```python
from pathlib import Path

shortcut_root = Path("/lakehouse/default/Files/Parcel/StatusSource")
assert shortcut_root.is_dir(), f"Shortcut source not visible: {shortcut_root}"
print(sorted(path.name for path in shortcut_root.glob("*.csv")))
```

The path should expose the archive's current CSV files. That readback, not local Check, establishes source access. An unavailable directory is not an empty snapshot; the [incremental Folder](incremental.md#declare-the-snapshot-folder) guards this distinction before staging anything.

In installed Python `read()` code, use the generated reader for this local destination:

```python
from shortcuts import Parcel__StatusSource

# Inside a Table or Folder read() method:
source_root = Parcel__StatusSource(self).path()
```

`path()` returns a mounted `pathlib.Path` for ordinary file access. `spark_path()` returns a string URI for Spark readers; do not pass it to `pathlib` as if it were a mounted path. A physical Lakehouse Shortcut may name another source workspace with `workspace="Carrier Shared"`; without it, the configured workspace is used.

## Keep a managed source's logical identity

When another Weaver item owns the data, retain its project identity instead of an external physical address. For example, an existing `Warehouse/Dispatch` in this project can present Landing's Python Event as a View with `Warehouse/Dispatch/shortcuts.yml`:

```yaml
logical:
  "Warehouse/Dispatch/Parcel.Event": "Lakehouse/Landing/Tables/Parcel.Event"
```

This declaration maps destination to source. It reuses the Event already loaded in Landing, not another seed. The configured physical bindings may change between environments while the logical target stays the same. Unlike a physical Shortcut, it carries a managed cross-item dependency and records the relationship in the catalogue. Warehouse Shortcuts are Views and do not have their own Load step.

This is an optional cross-item extension, not a requirement for the Lakehouse journey. [Connect items and dependencies](../estate/connected-items.md) owns the complete setup, source-before-consumer order and selection boundaries. Dependencies do not silently add an unselected item to Build or Load; select each item whose installed work should change. [Workspace mappings](../estate/environments.md) owns environment switching.

Use [Shortcut reference](../reference/weaver-documents/shortcut.md) for accepted Folder, Table, schema and View forms. Warehouse physical View Shortcuts are restricted to the configured workspace; their YAML has no workspace override. To process this archive into rows, follow the [complete mutable-source variation](incremental.md).
