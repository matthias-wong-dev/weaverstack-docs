# Weaver documents


---

## Project contract

A project is the source tree Weaver reads to declare logical Lakehouse and Warehouse items. The project root is the exact folder passed to Check or Build. When no folder is passed, both operations use the current directory; project discovery does not search parent directories.

The root folder name is the project name. It is case-sensitive and must be one logical name: non-empty, without surrounding whitespace or `/`, `\\`, `.` or `:`.

## Recognised item structure

The first two directory levels establish each logical item:

```text
parcel-project/
├── Lakehouse/
│   └── Landing/
│       ├── Files/
│       ├── Tables/
│       ├── assumptions/
│       ├── lib/
│       ├── schemas/
│       ├── tests/
│       └── shortcuts.py
└── Warehouse/
    └── Operations/
        ├── assumptions/
        ├── programmables/
        ├── schemas/
        ├── tests/
        ├── shortcuts.yml
        └── Parcel.Status.sql
```

Only `Lakehouse/<Name>` and `Warehouse/<Name>` establish items. Their spelling is exact. A Lakehouse data declaration belongs directly under `Tables/` or `Files/`; a Warehouse Table or View belongs directly under the item root. Tests, Assumptions, schema documents and Warehouse programmables belong directly under their named directories. These declaration directories do not accept another nesting level.

A Lakehouse `lib/` tree contains supporting files used by authored Python. Its complete contents travel with the installed work and affect the owning item's change signature, but they are not independently selectable Weaver documents.

See the [Weaver documents contract](overview.md) for the supported document families and how a path becomes an identity.

## What Check consumes

Check reads the complete project rooted at its positional folder and applies the same source discovery and declaration validation used to prepare a Build. It validates recognised paths, metadata, identities, class and SQL document structure, shortcuts, dependencies and collisions.

Check is source-only. It does not load `workspace-config.yml`, contact Fabric, start Spark or execute authored Python. A successful Check establishes that Weaver can read the project; it does not establish that authored work will execute successfully on Fabric.

## What Build consumes

Build reads and validates the complete project before contacting Fabric or installing selected items. Item selection limits what the Build installs; it does not turn the source reader into a partial-project check. An invalid declaration anywhere in the project can therefore stop a Build even when its item was not selected.

Build also consumes the selected workspace, catalogue and item bindings. When no source is passed on the CLI, the project root is the current directory. In a Fabric session, the notebook's process-local working tree may supply that default source. A local Check accepts only a local folder; Build may additionally accept an `abfss` source inside a Fabric session.

Build does not call authored Table, Folder, Test or Assumption methods. It installs the definitions produced from the project. Load and Test later consume those installed definitions from the catalogue, not the project tree.

## Ignored content

Weaver owns the `Lakehouse/` and `Warehouse/` item trees. Ordinary files and directories beside those trees, such as project documentation, notebooks, CI configuration and semantic-model exports, are not declarations and do not affect project or item signatures.

Within an item:

- files under a directory named `_ignore` are excluded from discovery and signatures;
- common version-control, virtual-environment, Python-cache, test-cache and editor temporary files are excluded;
- unrecognised ordinary files are ignored rather than becoming declarations;
- a Lakehouse `lib/` tree and item shortcut file are recognised supporting content and are not ignored.

Ignored content does not become an extension point. A file is included only when it occupies a supported authored location and form.

## Discovery errors

Weaver fails discovery rather than ignoring content that presents itself as a malformed or misplaced declaration. This includes:

- a Weaver declaration at the project root or beneath an unrecognised item type;
- a Lakehouse declaration outside its required `Tables/`, `Files/`, `tests/` or `assumptions/` location;
- a Warehouse relation below a Lakehouse area or a Lakehouse-only document in a Warehouse;
- an unsupported nested declaration directory;
- a recognised declaration whose filename, metadata identity, document kind or Python class disagree;
- duplicate identities, including identities that differ only by case;
- authored content in a reserved item or schema.

A folder containing Weaver-shaped declarations but no `Lakehouse/<Name>` or `Warehouse/<Name>` item is not a project. The operation fails against the selected root instead of adopting a deeper or adjacent tree.

## Defined behaviour

The Project contract specifies that Weaver:

1. treats the selected folder, not a parent search, as the project boundary;
2. derives logical items only from the first two recognised path components;
3. reads the complete project for Check and for Build preparation;
4. never executes authored Python during project discovery;
5. excludes unrelated and explicitly ignored content from declarations and signatures;
6. refuses malformed, misplaced, duplicate and reserved declarations;
7. keeps source validation separate from workspace binding and remote execution.

These rules define observable project behaviour. They do not expose the repository reader, signatures, generated files or intermediate project model as public APIs.

---

## Weaver documents contract

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

Exact metadata keys, method return values and SQL program forms remain in the [authoring guides](../../basics/index.md) and [Python API reference](../python/index.md). The placement and agreement rules below are part of the document contract because they decide whether a file is a declaration at all.

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

A shortcut destination must not collide with another declaration in the same logical namespace. A logical shortcut crosses item boundaries; it cannot point back into its declaring item. See [Shortcuts](../../basics/shortcuts.md) for the Python and YAML declaration forms.

## Warehouse programmables

An authored Warehouse programmable is one `.sql` file directly under `programmables/`. The filename names `Schema.Procedure`, and the file must contain exactly one `CREATE OR ALTER PROCEDURE` declaration for that name. This agreement is case-insensitive; the managed identity retains the filename's spelling. Programmables belong only to Warehouse items and may not create into Weaver's reserved schema.

Build installs a programmable as managed Warehouse structure. It is not a Table, View or separately loadable data declaration.

## Schema metadata

Every object or validation identity implies its schema. A separate schema document is optional unless the project needs to describe that schema or declare it before any object uses it.

A schema document is `schemas/<Schema>.yml`. Its filename and `Schema ID` must match exactly, including case. It may describe an otherwise unused schema. It does not create a second schema when an object already implies the same identity.

## Supporting files

A Lakehouse `lib/` tree, and the recognised shortcut files, accompany installed work but are not independently selectable documents. Files elsewhere do not become supporting content merely because they sit below an item; unsupported ordinary files are ignored, while files that present themselves as malformed declarations are errors under the [Project contract](overview.md).

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

The [Schema contract](../../advanced/schemas-keys-and-managed-columns.md) defines columns, keys, inference and managed-column boundaries.
