# Basics

Add Lakehouses, Warehouses, semantic models and Reports to one project. Start with the item you need, then use the same Build, Load, Test and Health flow across the estate.

## Author the items

- [Build a Lakehouse pipeline with Python](lakehouse-python.md) — load files and Delta Tables with dependencies expressed through imports.
- [Build a Lakehouse pipeline with Spark SQL](lakehouse-spark-sql.md) — use explicit dependencies and Table or View definitions.
- [Build a Warehouse pipeline](warehouse-pipeline.md) — build Tables and Views from T-SQL.
- [Deploy semantic models and Reports with PBIP](power-bi/deploy-pbip.md) — add native model and Report definitions to the project.
- [Connect a semantic model to source data](power-bi/fabric-integration.md) — order its refresh after a managed source and compare DAX with SQL.
- [Choose model and Report environment targets](power-bi/environments.md) — deploy the same source with another workspace configuration.
- [Validate a semantic model](power-bi/validate.md) — add a DAX Assumption.
- [Hide relationship foreign keys](power-bi/modelling-rule.md) — apply a native modelling convention.
- [Add Tests and Assumptions](tests-and-assumptions.md) — check the data beside the definitions.
- [Connect data with Shortcuts](shortcuts.md) — read managed or externally owned data.

## Develop and operate

- [The development cycle](development-cycle.md) — edit, preview Build, load changed work, validate and inspect Health.
- [Run and inspect the estate](run-and-inspect-estate.md) — operate Lakehouse and Warehouse work alongside model refreshes and validations.
- [Recover failed work](recover-failed-work.md) — choose a rerun, rebuild, remirror or reconstruction from the state left behind.

For selective runs, concurrency controls and shared model conventions, continue to [Advanced](../advanced/index.md). Exact syntax and behaviour belong in [Reference](../reference/index.md).
