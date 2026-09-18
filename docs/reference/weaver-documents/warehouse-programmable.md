# Warehouse programmable

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

An authored Warehouse programmable is one `.sql` file directly under `programmables/`. The filename names `Schema.Procedure`, and the file must contain exactly one `CREATE OR ALTER PROCEDURE` declaration for that name. This agreement is case-insensitive; the managed identity retains the filename's spelling. Programmables belong only to Warehouse items and may not create into Weaver's reserved schema.

Build installs a programmable as managed Warehouse structure. It is not a Table, View or separately loadable data declaration.
