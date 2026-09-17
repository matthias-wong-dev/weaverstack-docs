# Weaver

Weaver builds and operates Microsoft Fabric data estates from a version-controlled project. A project declares logical Lakehouse and Warehouse items with Python, Spark SQL, T-SQL, metadata and tests. Weaver resolves their dependencies, builds the required structures, runs loads and tests, and records operational state in a catalogue.

The project stays separate from deployment configuration. The same logical item can bind to different physical Fabric items in development and production.

## Start here

1. [Install Weaver](get-started/installation.md).
2. [Create and run a first project](get-started/first-project.md).
3. Author a [Lakehouse pipeline](guides/lakehouse-pipeline.md) or [Warehouse pipeline](guides/warehouse-pipeline.md).
4. Read [How Weaver works](core-concepts/how-weaver-works.md) for the product's core model.

## Documentation

- [Get started](get-started/index.md) — install Weaver and run the basic lifecycle.
- [Guides](guides/index.md) — complete a specific task.
- [Core concepts](core-concepts/index.md) — understand the model needed to reason about Weaver.
- [Reference](reference/index.md) — look up commands and supported interfaces.
- [Contracts](contracts/index.md) — read the behaviour Weaver guarantees.
- [Advanced](advanced/index.md) — work with specialised operating patterns.
- [Contributing](contributing/index.md) — improve the public documentation.

This site documents public behaviour. Implementation design and internal module ownership belong in the Weaver source repository.
