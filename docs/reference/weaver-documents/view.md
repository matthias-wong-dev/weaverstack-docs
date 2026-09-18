# View

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

A Python object filename uses `Schema__Object.py`; a SQL object filename uses `Schema.Object.sql`. The metadata ID uses `Schema.Object`. All components must agree exactly, including case.

A Python document must contain exactly one directly declared Weaver class. The class name must equal the filename stem, inherit the class named by its metadata kind and provide that kind's required authored methods. Helper classes may coexist in the module but do not declare additional Weaver documents. A View is authored in SQL, not Python, and a Folder is authored in Python, not SQL.

A SQL document's metadata kind determines whether it is a Table, View, Test or Assumption. Weaver validates the supported result-query shape without submitting the SQL. SQL syntax and engine behaviour that cannot be established statically remain the responsibility of Spark SQL or the Warehouse endpoint when the installed work runs.

Tests and Assumptions are declarations but do not materialise relations. In a Lakehouse their identities carry no `Tables` or `Files` area; in a Warehouse they share the item's ordinary `Schema.Object` namespace with Tables and Views. Tests and Assumptions also share one validation namespace with each other.
