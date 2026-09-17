# Get started

Use this path to create a Warehouse-only Weaver project, validate its source, and run its complete lifecycle:

```text
initialise → check → build → load → test → health → weaver workflow full
```

## Prerequisites

- Python 3.11 or later.
- A Microsoft Fabric workspace you can modify.
- Permission to create or reuse the catalogue Warehouse and project Warehouse.

[Install Weaver](installation.md), authenticate, and run `weaver doctor` before creating the project.

## What you will create

The [first project](first-project.md) declares one Warehouse Table and one Test. `weaver check` validates the declarations locally. Build installs them, Load materialises the table, Test compares its rows, and Health reports the resulting state.

Current versions of `weaver initialise` also create or reuse the default Fabric Environment and write its definition into the project. This Warehouse-only path does not publish or use that Environment.

For the distinction between project source, physical Fabric items, and installed state, see [How Weaver works](../core-concepts/how-weaver-works.md).

## Next action

Follow [First project](first-project.md). After that, continue with the [Lakehouse pipeline](../guides/lakehouse-pipeline.md) or [Warehouse pipeline](../guides/warehouse-pipeline.md) guide.
