# Projects and estates

A Weaver project and a running Fabric estate are related, but they are not the same thing.

- The **project** is the source you author.
- The **logical estate** is the model declared by that source: logical items, Weaver documents and their relationships.
- The **installed estate** is the generation that the last successful Build installed and recorded in the catalogue.
- The **physical estate** is the Lakehouses, Warehouses and objects in Fabric to which that generation is bound.

These distinctions answer four different questions:

| Question | Read |
| --- | --- |
| What do we intend to build? | Project source |
| What logical items and documents make up that intent? | Logical estate |
| What generation did Build certify as installed? | Catalogue |
| Where do its objects and data exist? | Physical Fabric items |

## A project is organised by logical item

The first two directory levels identify an item kind and logical item name. Documents below that point belong to the item.

```text
project/
├── Lakehouse/
│   └── Landing/
│       ├── Files/
│       ├── Tables/
│       ├── tests/
│       └── assumptions/
└── Warehouse/
    └── Operations/
        ├── programmables/
        ├── schemas/
        ├── tests/
        └── assumptions/
```

`Lakehouse/Landing` and `Warehouse/Operations` are logical item identities. They remain stable when a different workspace configuration binds the project to different Fabric item names.

A project can also contain workspace and workflow configuration, supporting code and documentation. Only recognised Weaver documents contribute declarations to the logical estate.

## The installed estate changes only at Build

Editing a Weaver document changes the project and its logical model. It does not change the installed or physical estate.

```text
edit source → check source → Build → installed generation
```

A successful Build installs the selected change and publishes catalogue state for the resulting generation. Load and Test then use that installed state. They do not reinterpret unbuilt source or substitute a target mapping edited since the Build.

This separation allows source and installed state to differ during development. Use the project to understand the intended estate; use the catalogue and Health to understand the estate currently in operation.

## Operational state belongs to the installed generation

Load records what happened when installed data work ran. Test records what installed validations found. Rebuilding an affected object starts new current state for that installed incarnation, while operational history remains a record of earlier runs.

The next concept, [Logical and physical items](logical-and-physical-items.md), explains how `workspace-config.yml` connects stable project identities to an environment. Exact project discovery and selection rules are in [Reference](../reference/index.md).
