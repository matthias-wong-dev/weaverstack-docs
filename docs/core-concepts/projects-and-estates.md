# Projects and estates

A **project** is the source you author. It groups Weaver documents beneath logical Lakehouse and Warehouse items.

An **estate** is that project model in operation: its logical items, their bindings to Fabric items, the generation installed by Build and the outcomes recorded by Load and Test.

These parts answer different questions:

- **What should Weaver install?** Read the project.
- **Where should Weaver install it?** Read the workspace configuration.
- **What has Weaver installed and run?** Read the Weaver catalogue.

## A project is organised by logical item

The first two levels of the project identify an item type and logical item name. Documents beneath an item belong to that item.

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

`Lakehouse/Landing` and `Warehouse/Operations` are project identities. They do not change when the project is built into another workspace or when its physical Fabric item names change.

A project may also contain workspace and workflow configuration, supporting code and project documentation. Weaver reads recognised documents from the item trees; not every file in the surrounding directory declares part of the estate.

## Source and installed state are separate

Editing a Weaver document changes the project. It does not change Fabric until a Build includes the owning item.

A successful Build records the installed generation and its logical-to-physical bindings in the catalogue. Load and Test then operate that installed generation. They do not switch to unbuilt source or reinterpret a changed target mapping.

This produces a direct working model:

```text
edit documents → check → Build → Load → Test
```

Build selection is an item boundary. Building one logical item updates that item; it does not install every item in the project. Load and Test have their own item selections over the installed estate.

## Operational results belong to an installed generation

Load and Test add facts about an installed generation: which work ran, whether it completed and what validations found. Those results are catalogue state, not project source.

A project can therefore differ from its installed estate while changes are being developed. Use project source to understand the intended model and catalogue state to understand the generation currently operating in a configured workspace.

Next, [Logical and physical items](logical-and-physical-items.md) explains how stable project identities are bound to Fabric.
