# Basics

Choose the task you need. Power BI deployment does not require finishing a Warehouse tutorial first.

## Power BI

- [Deploy an existing PBIP](power-bi/deploy-pbip.md): one native model and linked Report.
- [Development and production](power-bi/environments.md): one source, different target names/workspaces.
- [Validate a semantic model](power-bi/validate.md): one DAX Assumption from source.
- [Apply a modelling rule](power-bi/modelling-rule.md): hide foreign keys with a native annotation.
- [Connect a model to a Fabric estate](power-bi/fabric-integration.md): optional managed lineage, refresh and SQL reconciliation.

## Build pipelines

- [Warehouse SQL](warehouse-pipeline.md): a Table and dependent View.
- [Lakehouse Python](lakehouse-python.md): files and a Table with an inferred dependency.
- [Lakehouse Spark SQL](lakehouse-spark-sql.md): a Table with explicit dependencies.
- [Tests and Assumptions](tests-and-assumptions.md): expected/actual comparisons and violating rows.
- [Shortcuts](shortcuts.md): connect managed or external data without confusing ownership.

## Run your project

- [Workspace and Python runtime](workspace-and-python-runtime.md): choose bindings and publish a runtime only for work that needs it.
- [Sessions and workflows](sessions-and-workflows.md): reuse context and coordinate ordinary commands.
- [Development cycle](development-cycle.md): small change → inspect → Build → catch up → Test.
- [Run and inspect](run-and-inspect-estate.md): ordinary operations and recorded state.
- [Troubleshooting](troubleshooting.md): a detected condition and the next action.
- [Recover failed work](recover-failed-work.md): rerun, reconstruct or deliberately retire work.

Use [Advanced](../advanced/index.md) for optional controls and modelling mechanisms, and [Reference](../reference/index.md) for the complete interface.
