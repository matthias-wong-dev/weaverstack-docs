# Mirrors

A Mirror creates a development estate from another installed estate. It lets a project keep the same logical items and Weaver documents while development uses different physical Fabric items.

The result is not simply a second copy of every dataset. Weaver can represent unchanged data as borrowed from the source and materialise only the parts that development changes.

## Borrowed data and local data

Immediately after mirroring, selected development items expose the source estate's installed data through local borrowed forms. A Warehouse uses Views over source relations. A Lakehouse uses shortcuts for stored Tables and Folders, with local wrapper Views where needed.

Borrowed data remains owned and loaded at its source. The destination contains the installed definitions and execution work needed to reason about the estate, but a borrowed object is not a local load target.

A local object is different: its data and operational state belong to the development target. Load writes it in development, and later operations read its state from the destination catalogue.

## Destination bindings create the development estate

Workspace configuration binds logical items to physical targets. A development configuration normally names:

- the destination catalogue;
- the catalogue to mirror from; and
- development targets for the same logical items used by the project.

The logical identity `Warehouse/Operations`, for example, can bind to one Warehouse in production and another in development. The Weaver documents do not acquire development-specific identities. Selecting the configuration changes the physical estate in which operations work.

Mirror settles those destination bindings before applying them. Logical Shortcuts are recreated against the final bindings, so relationships between project items continue to use logical identity rather than development target names.

## Build turns borrowed objects into local objects

Build compares project source with the installed state copied from the source estate. An unchanged borrowed object keeps its borrowed representation. When Build selects a changed borrowed object, or an affected descendant within the Build selection, it replaces that representation with the authored local form.

This produces a **mixed development estate**:

```text
unchanged objects  → borrowed source data
changed objects    → local development data
affected consumers → local development data
```

The boundary can move with each Build. A developer can change one part of the project while unchanged dependencies continue to resolve to source data.

Build selection still matters. Objects outside the selected items are not materialised merely because another item was built.

## `_.Mirror` records what is still borrowed

The destination catalogue's `_.Mirror` table identifies installed objects whose physical form still borrows from the source. `_.Registry` continues to describe each object's logical installed declaration; `_.Mirror` adds the source address and borrowed physical form.

When Build successfully materialises an object locally, its `_.Mirror` record is removed as part of publishing the new installation. Objects whose rows remain are still borrowed. Health uses this distinction to read current Load state from the correct catalogue and to check the expected physical form.

The [Catalogue](catalogue.md) places `_.Mirror` among the other installed and operational state. See [Mirror behaviour](../reference/operation-behaviour/mirror.md) for command selection, confirmation, copied state, destructive scope and failure boundaries.
