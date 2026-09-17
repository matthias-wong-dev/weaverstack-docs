# Weaver

Weaver builds and operates Microsoft Fabric data estates from a version-controlled project. A project declares logical Lakehouse and Warehouse items with ordinary Python, Spark SQL, T-SQL, metadata and tests. Weaver resolves their dependencies, builds the required structure, runs loads and records installed state in a catalogue.

The repository stays separate from deployment configuration. The same logical item can bind to different physical Fabric items in development and production.

## Start here

1. [Install Weaver](get-started/installation.md).
2. [Create and run a first project](get-started/first-project.md).
3. Read the [architecture overview](concepts/architecture.md) before designing a larger estate.

## Documentation

- [Get started](get-started/index.md) — install Weaver and complete a first build and load.
- [Guides](guides/index.md) — task-oriented documentation as coverage is added.
- [Architecture and concepts](concepts/index.md) — the repository, build bundle, Fabric targets and catalogue.
- [Reference](reference/index.md) — command and, later, Python API details.
- [Contracts](contracts/index.md) — stable project, configuration and machine-readable interfaces.
- [Advanced](advanced/index.md) — controlled deployment and operating patterns.
- [Contributing](contributing/index.md) — how to improve these public docs.

This site documents public behaviour. Weaver's source repository remains the authority for implementation design and internal module ownership. [Current coverage gaps](gaps.md) are listed explicitly rather than filled with inferred behaviour.
