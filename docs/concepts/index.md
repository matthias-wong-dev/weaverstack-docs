# Architecture and concepts

Weaver separates four concerns that are easy to conflate:

1. a repository declares logical items and documents;
2. workspace configuration binds logical items to physical Fabric targets;
3. build produces and installs a frozen deployment plan;
4. the catalogue records installed and operational state.

Read the [architecture overview](architecture.md) for this model and the boundary between build and load.

Future concept pages will cover logical identity, dependencies, shortcuts, catalogue state, incremental selection, validation, health and execution sessions. Their intended homes are listed in the [coverage gap map](../gaps.md).
