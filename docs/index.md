# Weaver

Weaver builds and operates Microsoft Fabric data estates from a version-controlled project. A project declares logical Lakehouse and Warehouse items with Python, Spark SQL, T-SQL, metadata and tests. Weaver resolves dependencies, builds the required structures, runs loads and tests, and records operational state in a catalogue.

Project source stays separate from deployment configuration. The same logical item can bind to different physical Fabric items in development and production.

## Choose a route

**New to Weaver**

[Install Weaver](get-started/installation.md), then [create and run a first project](get-started/first-project.md). The first-project path validates source and runs Build, Load, Test and Health against a Warehouse-only estate.

**Building a pipeline**

Start with the [Lakehouse pipeline](guides/lakehouse-pipeline.md) or [Warehouse pipeline](guides/warehouse-pipeline.md), then add [incremental loads](guides/incremental-loads.md), [Shortcuts](guides/shortcuts.md) or [validation](guides/validation.md) as the project requires.

**Operating an estate**

Use [Operate an estate](guides/operate-estate.md) for the routine inspect–preview–run–verify cycle. Continue to [Troubleshooting](guides/troubleshooting.md), [Recovery](guides/recovery.md) or [Automation](guides/automation.md) for the relevant operating boundary.

**Understanding or integrating Weaver**

Read [How Weaver works](core-concepts/how-weaver-works.md) for the public model. Use [Reference](reference/index.md) for exact interfaces and [Contracts](contracts/index.md) for specified behaviour.

## Documentation sections

- [Get started](get-started/index.md) — install Weaver and complete the first lifecycle.
- [Guides](guides/index.md) — complete authoring, operating and automation tasks.
- [Core concepts](core-concepts/index.md) — understand the model behind those tasks.
- [Reference](reference/index.md) — look up commands, APIs and current formats.
- [Contracts](contracts/index.md) — determine selection, ordering, state and failure behaviour.
- [Advanced](advanced/index.md) — apply specialised operating patterns.
- [Contributing](contributing/index.md) — improve and validate the public documentation.

This site documents public behaviour. Product positioning belongs at `weaverstack.dev`; implementation design and internal module ownership belong in the Weaver source repository.