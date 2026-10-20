# Warehouse

A Warehouse Table begins with a T-SQL SELECT and a small metadata comment. Weaver installs the physical Table and its load machinery, then records the work it runs.

[Build a first Table and View](first-project.md), then [test their data](tests.md). You keep SQL for the transformation and its independent checks.

When the source changes, [Loading changes](incremental.md) shows how candidate rows and explicit delete keys become target updates around a consumer bookmark. [Schemas, keys and protected data](schema-and-protection.md) covers the next design decisions.

For shared deployment and operation, [Coordinate your estate](../estate/index.md).
