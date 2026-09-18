# Folder

A Folder manages files beneath a Lakehouse `Files` area. Shared source-header, identity and metadata rules are in [Common metadata](common-metadata.md).

## Location and authored form

A Folder is a Python file directly at:

```text
Lakehouse/<Item>/Files/<Schema>__<Object>.py
```

It declares `Folder ID: Schema.Object` and one class `Schema__Object` that directly inherits `Folder` and implements one synchronous `read()` method. Folder is not supported in a Warehouse or as SQL. Runtime constructors and helper signatures are in [Python authored objects](../python/objects.md).

## Metadata

A Folder accepts the [shared keys](common-metadata.md#shared-metadata-keys) plus these keys:

| Key | Required | Accepted value | Default and effect |
| --- | --- | --- | --- |
| `Folder ID` | Yes | `Schema.Object` | No default. |
| `File key` | Yes | One non-empty glob string or a non-empty YAML list of glob strings | No default. Patterns are relative to the Folder, use `/`, and cannot be absolute or contain a `..` path component. Backslashes are normalised to `/`. |
| `Incremental` | No | Boolean | **`true`**. Incremental reconciliation preserves managed files omitted from staging unless `read()` explicitly deletes them. `false` makes staging a complete snapshot of the managed file set. |

A snapshot Folder must therefore declare `Incremental: false`; omitting the key selects incremental behaviour.

`File key` defines the files Weaver manages. A non-incremental load deletes existing files that match a declared pattern and are absent from staging. Files outside every pattern are not owned by that reconciliation. A staged file outside the patterns is rejected rather than published.

`Incremental` and `Static` are compatible: Incremental controls reconciliation, while Static controls whether another ordinary Load runs after the first clean load. `Prohibit rebuild` controls Build, not file reconciliation.

## `read()` contract

`read()` writes into the exact `StagingFolder` returned by `self.staging_folder()` for that invocation.

| Folder mode | Accepted return forms |
| --- | --- |
| Non-incremental | The issued `StagingFolder` only. `None` and any tuple are invalid. Return an empty issued staging folder for an empty snapshot. |
| Incremental | The issued `StagingFolder`; `(staging, files_to_delete)`; `None` for no work; or `(None, files_to_delete)` for deletion-only work. |

Returning a raw `Path`, a string, another `StagingFolder` instance or any staging directory not issued by Weaver is invalid.

`files_to_delete` is a sequence of exact relative file-name strings. Each name must match `File key`; it cannot be absolute, contain `..` or backslashes, name a directory, contain glob characters, enter `_changes/`, or also be staged. A single string is not a sequence for this contract.

A Load resets staging before `read()`. Successful publication removes staging; failure retains it for inspection. Rejected staged files are kept in the sibling `<Object>_Reject` folder. With fault tolerance disabled, any rejection leaves the destination unmodified; with it enabled, accepted files publish and rejected files do not.

## Complete example

A snapshot Folder at `Lakehouse/Landing/Files/Parcel__Manifest.py`:

```python
"""
Folder ID: Parcel.Manifest

Description: Current parcel manifest files.

Lineage: Carrier manifest export.

File key: "*.csv"

Incremental: false
"""

from weaver import Folder


class Parcel__Manifest(Folder):
    def read(self):
        staging = self.staging_folder()
        (staging.path / "manifest.csv").write_text(
            "parcel_id,status\n",
            encoding="utf-8",
        )
        return staging
```

## Build, Load, Test and managed state

Build installs the Folder declaration and its Python load code; it does not call `read()`. Load calls the installed `read()` and reconciles matching files. Folder does not support reload. Test does not execute a Folder, although validations or other load code may read its files.

Weaver maintains `_changes/` inside the destination Folder. Each successful change writes a timestamped JSON document containing the actual inserted, updated and deleted relative paths. Authored code cannot stage or delete that tree. The sibling `_Staging` and `_Reject` paths are runtime-managed, not additional authored documents. Folder data has no row-audit, signature or identity columns.

Build records the declaration in `_.FolderDictionary`, resolved dependencies in `_.Dependency`, and certification in `_.Registry`. Loads use current load state and bookmarks and contribute Load history/statistics. See the [catalogue schema](../catalogue-schema.md) for exact columns and [Incremental data processing](../../advanced/incremental-data-processing.md) for change-feed behaviour.
