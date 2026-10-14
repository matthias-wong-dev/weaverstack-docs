# How Weaver works

A Weaver project holds the definitions for a Fabric estate: Lakehouses, Warehouses, semantic models and Reports. Workspace configuration maps their logical names to physical items; the catalogue records what is installed and what has run.

## Keep the source in a project

Python and SQL define data work under `Lakehouse/` and `Warehouse/`. Native model and Report definitions live under `PowerBI/`. Models use standard TMDL; optional overlays and Weaver annotations add refinements and modelling rules. These play the same authoring role as the engineering declarations around SQL and Python. Tests and Assumptions live beside the items they check.

The project declares logical identities, not development or production item names. Change workspace configuration to select another destination without maintaining another copy of the source.

See [Projects and estates](projects-and-estates.md), [Weaver documents](weaver-documents.md) and [Logical and physical items](logical-and-physical-items.md).

## Build deploys definitions

Build reconciles selected source items and installs their Tables, Folders, Views, Shortcuts and validations. It also deploys native semantic models and their linked Reports. Build does not run the authored data loads or refresh models.

Build Lakehouse and Warehouse work first, then models and Reports in a separate Build call. The second call can read the installed source metadata. Both use the same project and workspace configuration; a workflow can sequence them.

## Load follows the dependency graph

Load runs installed Table and Folder work and refreshes semantic models. With no item selection it covers the installed estate. Selected source work precedes the consumers and model refreshes that depend on it.

Each consumer keeps its own successful-processing bookmark. A failed node does not discard the progress of independent work that finished. Reports use the model’s data rather than having their own data Load.

See [Dependencies](dependencies.md), [Incremental data processing](../advanced/incremental-data-processing.md) and [Fault tolerance](fault-tolerance.md).

## Test checks the data

Tests compare expected and actual rows. Assumptions return rows that violate a condition. Both can be authored for Lakehouse and Warehouse data or for semantic models using DAX.

A model’s DAX result can be checked against SQL calculated independently from its managed source. Installed results share the catalogue’s current validation state and history.

See [Build, Load and Test](build-load-and-test.md) and [Add Tests and Assumptions](../warehouse/tests.md).

## Health reads the whole estate

Health brings Build, Load and Test state together in one report. Without an item selector it covers the managed estate, including registered model refreshes and validations. It uses recorded state and physical source inventories; it does not run the work again.

That shared view matters when a source changes after a downstream load or Test passed. Health identifies the downstream work that is now behind, rather than presenting each successful run in isolation.

See [State and health](state-and-health.md) and [Run and inspect the estate](../estate/operate.md).

## Develop against existing data

Mirror borrows unchanged data through Warehouse Views and OneLake Shortcuts. Build materialises the work you change locally. The project keeps the same logical names and operating flow.

See [Mirrors](mirrors.md) and [The development cycle](../estate/development-cycle.md).
