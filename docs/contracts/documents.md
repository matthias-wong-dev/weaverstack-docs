# Weaver documents contract

A Weaver document is an authored file that declares part of one logical Lakehouse or Warehouse item. Its path establishes its owner and, where applicable, its Lakehouse area. Its metadata and authored name establish its kind and `Schema.Object` identity.

Check and Build read documents statically. They do not import or execute authored Python while discovering a project.

## Supported document families

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

Exact metadata keys, method return values and SQL program forms remain in the [authoring guides](../guides/index.md) and [Python API reference](../reference/python/index.md). The placement and agreement rules below are part of the document contract because they decide whether a file is a declaration at all.

## Data and validation documents

A Python object filename uses `Schema__Object.py`; a SQL object filename uses `Schema.Object.sql`. The metadata ID uses `Schema.Object`. All components must agree exactly, including case.

A Python document must contain exactly one directly declared Weaver class. The class name must equal the filename stem, inherit the class named by its metadata kind and provide that kind's required authored methods. Helper classes may coexist in the module but do not declare additional Weaver documents. A View is authored in SQL, not Python, and a Folder is authored in Python, not SQL.

A SQL document's metadata kind determines whether it is a Table, View, Test or Assumption. Weaver validates the supported result-query shape without submitting the SQL. SQL syntax and engine behaviour that cannot be established statically remain the responsibility of Spark SQL or the Warehouse endpoint when the installed work runs.

Tests and Assumptions are declarations but do not materialise relations. In a Lakehouse their identities carry no `Tables` or `Files` area; in a Warehouse they share the item's ordinary `Schema.Object` namespace with Tables and Views. Tests and Assumptions also share one validation namespace with each other.

## Shortcuts

A shortcut belongs to the item containing its shortcut file. Its authored destination establishes the local identity that Build manages.

- A Lakehouse shortcut can declare a Table, Folder or schema destination.
- A Warehouse shortcut declares a View destination.
- A logical shortcut names another Weaver document and must resolve with exact case inside the same project.
- A physical shortcut names a Fabric location directly.

A shortcut destination must not collide with another declaration in the same logical namespace. A logical shortcut crosses item boundaries; it cannot point back into its declaring item. See [Shortcuts](../guides/shortcuts.md) for the Python and YAML declaration forms.

## Warehouse programmables

An authored Warehouse programmable is one `.sql` file directly under `programmables/`. The filename names `Schema.Procedure`, and the file must contain exactly one `CREATE OR ALTER PROCEDURE` declaration for that name. This agreement is case-insensitive; the managed identity retains the filename's spelling. Programmables belong only to Warehouse items and may not create into Weaver's reserved schema.

Build installs a programmable as managed Warehouse structure. It is not a Table, View or separately loadable data declaration.

## Schema metadata

Every object or validation identity implies its schema. A separate schema document is optional unless the project needs to describe that schema or declare it before any object uses it.

A schema document is `schemas/<Schema>.yml`. Its filename and `Schema ID` must match exactly, including case. It may describe an otherwise unused schema. It does not create a second schema when an object already implies the same identity.

## Supporting files

A Lakehouse `lib/` tree, and the recognised shortcut files, accompany installed work but are not independently selectable documents. Files elsewhere do not become supporting content merely because they sit below an item; unsupported ordinary files are ignored, while files that present themselves as malformed declarations are errors under the [Project contract](project.md).

## Agreement and failure

Document discovery fails when any source of identity or type disagrees:

- path versus supported item kind or Lakehouse area;
- validation directory versus `Test ID` or `Assumption ID`;
- filename versus metadata ID;
- Python filename versus class name, base class or required methods;
- SQL filename versus metadata ID;
- schema filename versus `Schema ID`;
- programmable filename versus created procedure;
- shortcut destination versus its declaring item or an existing identity.

An exact duplicate and a case-only collision are both errors. Weaver does not select one declaration by traversal order.

## Defined behaviour

The Weaver documents contract specifies that Weaver:

1. recognises only the supported families and authored locations above;
2. derives ownership from the logical item path;
3. includes `Tables` or `Files` in each Lakehouse data identity;
4. requires path, filename, metadata kind, metadata identity and Python class to agree where each applies;
5. reads declarations without executing authored Python;
6. keeps supporting files distinct from selectable documents;
7. rejects unsupported combinations and identity collisions before Build changes Fabric.
