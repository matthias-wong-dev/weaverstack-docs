# Guides

Guides show how to complete a task with Weaver. Each guide states its prerequisites, uses a small independent example and links to the exact concept or reference needed for detail.

Begin with [First project](../get-started/first-project.md) to initialise a project and run Build, Load, Test and Health.

## Author a pipeline

- [Lakehouse pipeline](lakehouse-pipeline.md) — load managed files into a Python Table, then add a separate Spark SQL Table.
- [Warehouse pipeline](warehouse-pipeline.md) — build and load a T-SQL Table with a dependent View, without Spark.

## Extend and operate a pipeline

- [Incremental loads](incremental-loads.md) — process changed and deleted files from a managed Folder using a Table bookmark.
- [Shortcuts](shortcuts.md) — connect logical items or expose an external Fabric location.
- [Validation](validation.md) — install and run Tests and Assumptions against an estate.
- [Workspaces and Fabric Environments](environments.md) — separate physical estate bindings from Python runtime publication.

Use [How Weaver works](../core-concepts/how-weaver-works.md) for the model behind the steps, the [CLI reference](../reference/cli.md) for exact command forms, and the [Load contract](../contracts/load.md) for selection and failure behaviour.
