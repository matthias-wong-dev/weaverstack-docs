# Projects and estates

A Weaver project and a running Fabric estate are related, but they are not the same thing.

- The **project** is the source you author.
- The **logical estate** is the model declared by that source: logical items, Weaver documents and their relationships.
- The **installed estate** is the generation that the last successful Build installed and recorded in the catalogue.
- The **physical estate** is the Lakehouses, Warehouses, models, Reports and objects in the service to which those definitions are bound.

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
├── Warehouse/
│   └── Operations/
│       ├── programmables/
│       ├── schemas/
│       ├── tests/
│       └── assumptions/
└── PowerBI/
    └── Parcel/
        ├── Parcel.pbip
        ├── Parcel.SemanticModel/
        ├── Parcel.Report/
        ├── tests/Parcel/
        └── assumptions/Parcel/
```

`Lakehouse/Landing`, `Warehouse/Operations`, `SemanticModel/Parcel` and `Report/Parcel` are logical item identities. They remain stable when a different workspace configuration binds the project to different Fabric item names.

The `PowerBI/Parcel` directory groups native model and Report definitions; the model and Report retain separate logical identities. Build deploys the model before its linked Report. The model’s `tests` and `assumptions` directories hold its DAX validations. See [Native project layout](../reference/power-bi/project-layout.md).

A project can also contain workspace and workflow configuration, supporting code and documentation.

## Build makes source changes operational

Editing a Weaver document changes the project and its logical model. It does not change the installed or physical estate.

```text
edit source → check source → Build → installed generation
```

Build installs the selected change and publishes catalogue state for the resulting generation. Load and Test then use that installed state and its recorded bindings, including registered model refreshes and DAX validations. Build source-data definitions first and models/Reports in a separate call against the same project.

This separation allows source and installed state to differ during development. Use the project to understand the intended estate; use the catalogue and Health to understand the estate currently in operation.

## Recorded operational state belongs to the installed generation

The catalogue combines source-data and model operational state. Load records what happened when installed work ran or a model refreshed. Test records what installed SQL, Python and DAX validations found. Rebuilding an affected object starts new current state for that installed incarnation, while operational history remains a record of earlier runs.

The next concept, [Logical and physical items](logical-and-physical-items.md), explains how `workspace-config.yml` connects stable project identities to an environment. Exact project discovery and selection rules are in [Reference](../reference/index.md).
