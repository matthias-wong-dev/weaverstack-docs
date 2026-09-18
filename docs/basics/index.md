# Basics

Basics cover normal authoring and operating work. Start with [First project](../getting-started/first-project.md) if you have not yet run Build, Load, Test and Health against a working estate.

## Build a pipeline

Choose the engine that owns the work:

- [Warehouse pipeline](warehouse-pipeline.md) — build and load a T-SQL Table with a dependent View, without Spark.
- [Lakehouse pipeline with Python](lakehouse-python.md) — load managed files into a Python Table.
- [Lakehouse pipeline with Spark SQL](lakehouse-spark-sql.md) — author and run a Spark SQL Table.

Extend that pipeline with:

- [Tests and Assumptions](tests-and-assumptions.md) — install and run validations against the estate.
- [Shortcuts](shortcuts.md) — connect logical items or expose an external Fabric location.
- [Workspace and Python runtime](workspace-and-python-runtime.md) — separate physical estate bindings from Python runtime publication.

## Develop and operate the estate

- [Sessions and workflows](sessions-and-workflows.md) — compose ordinary commands interactively or as a checked sequence.
- [The development cycle](development-cycle.md) — establish a development baseline and iterate on it.
- [Run and inspect an estate](run-and-inspect-estate.md) — inspect, preview, run and verify installed work.
- [Troubleshooting](troubleshooting.md) — diagnose project, workspace, installation, runtime and state problems from observed symptoms.
- [Recover failed work](recover-failed-work.md) — reconcile partial state, reload selected Tables, refresh a mirror or deliberately empty targets.

Use [How Weaver works](../core-concepts/how-weaver-works.md) for the model behind these tasks, [Advanced](../advanced/index.md) for deeper mechanisms and the [Reference](../reference/index.md) for exact interfaces and behaviour.
