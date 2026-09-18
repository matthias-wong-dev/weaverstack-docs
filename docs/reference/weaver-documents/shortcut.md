# Shortcut

| Family | Lakehouse authored form | Warehouse authored form | Identity established by |
| --- | --- | --- | --- |
| Table | Python or Spark SQL under `Tables/` | T-SQL at the item root | item path, `Tables` area for a Lakehouse, filename and `Table ID` |
| Folder | Python under `Files/` | Not supported | item path, `Files` area, filename and `Folder ID` |
| View | Spark SQL under `Tables/` | T-SQL at the item root | item path, `Tables` area for a Lakehouse, filename and `View ID` |
| Test | Python or Spark SQL under `tests/` | T-SQL under `tests/` | item path, directory, filename and `Test ID` |
| Assumption | Python or Spark SQL under `assumptions/` | T-SQL under `assumptions/` | item path, directory, filename and `Assumption ID` |
| Shortcut | `shortcuts.py` | `shortcuts.yml` | declaring item, authored destination name and shortcut kind |
| Warehouse programmable | Not supported | T-SQL under `programmables/` | item path, filename and the procedure created by the statement |
| Schema metadata | YAML under `schemas/` | YAML under `schemas/` | item path, filename and `Schema ID` |

The owning item selects the SQL dialect: SQL in a Lakehouse is Spark SQL; SQL in a Warehouse is T-SQL. A suffix does not select another dialect.

Exact metadata keys, method return values and SQL program forms remain in the [authoring guides](../../basics/index.md) and [Python API reference](../python/index.md). The placement and agreement rules below are part of the document contract because they decide whether a file is a declaration at all.

A shortcut belongs to the item containing its shortcut file. Its authored destination establishes the local identity that Build manages.

- A Lakehouse shortcut can declare a Table, Folder or schema destination.
- A Warehouse shortcut declares a View destination.
- A logical shortcut names another Weaver document and must resolve with exact case inside the same project.
- A physical shortcut names a Fabric location directly.

A shortcut destination must not collide with another declaration in the same logical namespace. A logical shortcut crosses item boundaries; it cannot point back into its declaring item. See [Shortcuts](../../basics/shortcuts.md) for the Python and YAML declaration forms.
