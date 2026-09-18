# Weaver

Weaver builds and operates Microsoft Fabric data estates from a version-controlled project. A project declares logical Lakehouse and Warehouse items with Python, Spark SQL, T-SQL, metadata and tests. Weaver resolves dependencies, builds the required structures, runs loads and tests, and records operational state in a catalogue.

Project source stays separate from deployment configuration. The same logical item can bind to different physical Fabric items in development and production.

## Choose a route

**New to Weaver**

[Install Weaver](getting-started/installation.md), then [create and run a first project](getting-started/first-project.md). The first-project path validates source and runs Build, Load, Test and Health against a Warehouse-only estate.

**Building a pipeline**

Start with the [Lakehouse pipeline](basics/lakehouse-python.md) or [Warehouse pipeline](basics/warehouse-pipeline.md), then add [incremental processing](advanced/incremental-data-processing.md), [Shortcuts](basics/shortcuts.md) or [validation](basics/tests-and-assumptions.md) as the project requires.

**Operating an estate**

Use [Run and inspect an estate](basics/run-and-inspect-estate.md) for the routine inspect–preview–run–verify cycle. Continue to [Troubleshooting](basics/troubleshooting.md), [Recover failed work](basics/recover-failed-work.md) or [Automation and execution contexts](advanced/automation-and-execution-contexts.md) for the relevant operating boundary.

**Understanding or integrating Weaver**

Read [How Weaver works](core-concepts/how-weaver-works.md) for the public model. Use [Reference](reference/index.md) for exact interfaces and operation behaviour.

## Documentation sections

- [Getting started](getting-started/index.md) — install Weaver and complete the first lifecycle.
- [Core concepts](core-concepts/index.md) — understand the model behind those tasks.
- [Basics](basics/index.md) — complete normal authoring and operating work.
- [Advanced](advanced/index.md) — understand deeper mechanisms and specialised operating patterns.
- [Reference](reference/index.md) — look up commands, APIs, configuration and exact behaviour.

This site documents public behaviour. Product positioning belongs at `weaverstack.dev`; implementation design and internal module ownership belong in the Weaver source repository.
