# Get started

This path creates a Warehouse-only Weaver project, validates its source and runs its complete lifecycle:

```text
initialise → check → build → load → test → health
                         ↘ workflow full ↗
```

## Prerequisites

- Python 3.11 or later.
- A Microsoft Fabric workspace you can modify.
- Permission to create or reuse the catalogue Warehouse and project Warehouse.

[Install Weaver](installation.md), authenticate and run `weaver doctor` before creating the project.

## Complete the first lifecycle

[First project](first-project.md) declares one Warehouse Table and one Test. It takes you through each operation separately so you can inspect its effect, then runs `weaver workflow full` as the composed form of the same lifecycle.

`weaver check` validates project declarations locally. Build installs definitions, Load materialises the Table, Test compares its rows, and Health reports the resulting state.

`weaver initialise` also creates or reuses the default Fabric Environment and writes its definition into the project. This Warehouse-only path does not publish or use that Environment.

## Continue from the working project

Choose the next route by execution engine:

- [Lakehouse pipeline](../guides/lakehouse-pipeline.md) — author Python and Spark SQL Tables backed by a Fabric Environment.
- [Warehouse pipeline](../guides/warehouse-pipeline.md) — author T-SQL Tables and Views without Spark.

Read [How Weaver works](../core-concepts/how-weaver-works.md) when you need the distinction between project source, physical Fabric items and catalogue state. Use [Troubleshooting](../guides/troubleshooting.md) if Doctor, Build, Load or Test does not reach the expected result.