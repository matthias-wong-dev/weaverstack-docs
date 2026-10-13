# Weaver documentation

Weaver builds and operates Microsoft Fabric estates: Lakehouses, Warehouses, semantic models and Reports. Keep Python, SQL and native Power BI definitions in one project. Build deploys them, Load moves data and refreshes models, Test checks results, and Health reports the managed estate’s state together.

## Build your first project

[Install Weaver](getting-started/installation.md), then [create a small Fabric project](getting-started/first-project.md). Take one Table and Test through the complete lifecycle before adding more items.

## Add work to the project

- [Build a Lakehouse pipeline with Python](basics/lakehouse-python.md) or [Spark SQL](basics/lakehouse-spark-sql.md).
- [Build a Warehouse pipeline with T-SQL](basics/warehouse-pipeline.md).
- [Deploy semantic models and Reports with PBIP](basics/power-bi/deploy-pbip.md), then [connect the model to managed source data](basics/power-bi/deploy-pbip.md#use-a-managed-source).

[Basics](basics/index.md) covers everyday authoring, development and operations. [Core concepts](core-concepts/index.md) explains the project, dependencies, catalogue and state behind them.

## Operate the estate

[Run and inspect the estate](basics/run-and-inspect-estate.md) with the same configuration across its items. A source load and a model refresh belong to the same dependency graph; one Health report shows whether their data and validations are current.

[Advanced](advanced/index.md) covers selective runs, concurrency, incremental loading, recovery and shared semantic-model conventions. [Reference](reference/index.md) owns exact syntax, commands, APIs and operation behaviour.
