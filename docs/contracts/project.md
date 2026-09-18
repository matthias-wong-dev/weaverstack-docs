# Project contract

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

See the [Weaver documents contract](documents.md) for the supported document families and how a path becomes an identity.

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
