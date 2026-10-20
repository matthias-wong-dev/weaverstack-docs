# Lakehouse

Write ordinary Python or Spark SQL. Weaver builds the managed files and Tables, orders their dependencies and records what each Load processed.

[Start with a Folder feeding a Table](python.md). The Python import connects the two; you keep the transformation code rather than writing another scheduler around it.

Then [add a Spark SQL transformation](spark-sql.md), [test the data](tests.md) or [load changes using a consumer bookmark](incremental.md). The bookmark belongs to the consumer, so two Tables can process the same source at their own pace.

For existing data, use [Shortcuts](shortcuts.md). [Running Python in Fabric](runtime.md) covers the matching runtime. When items need shared configuration or operations, [Coordinate your estate](../estate/index.md).
