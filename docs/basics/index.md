# Basics

Use these tasks after [First project](../getting-started/first-project.md). They cover the normal path from project source to an installed, loaded and tested estate.

## Build a pipeline

Choose the engine and authoring form for the work:

- [Build a Warehouse pipeline](warehouse-pipeline.md) — create a T-SQL Table and dependent View.
- [Build a Lakehouse pipeline with Python](lakehouse-python.md) — load files with Python and an inferred dependency.
- [Build a Lakehouse pipeline with Spark SQL](lakehouse-spark-sql.md) — create a Spark SQL Table.

Then add the behaviour the pipeline needs:

- [Add Tests and Assumptions](tests-and-assumptions.md) — install and run validations.
- [Connect items with shortcuts](shortcuts.md) — connect logical items or an external Fabric location.

## Set up repeated work

- [Configure a workspace and Python runtime](workspace-and-python-runtime.md) — bind logical items to Fabric, switch between development and production, and publish the runtime needed by Python work.
- [Work in Sessions and workflows](sessions-and-workflows.md) — reuse one execution context, then save an accepted command sequence.
- [The development cycle](development-cycle.md) — establish a mirrored development baseline and iterate with Check, Build, stale Load, Test and Health.

## Operate and recover

- [Run and inspect an estate](run-and-inspect-estate.md) — inspect state, run installed work and verify the result.
- [Troubleshooting](troubleshooting.md) — start from a Check, Build, Load, Test, Health or runtime symptom.
- [Recover failed work](recover-failed-work.md) — choose a rerun, reconstruction, validation, mirror refresh or deliberate Wipe.

For the mental model behind these tasks, start with [How Weaver works](../core-concepts/how-weaver-works.md). Use [Advanced](../advanced/index.md) for deeper mechanisms and [Reference](../reference/index.md) for exact syntax and operation behaviour.
