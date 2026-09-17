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

## Operate and automate an estate

- [Operate an estate](operate-estate.md) — inspect, preview, run and verify an installed estate.
- [Troubleshooting](troubleshooting.md) — diagnose project, workspace, installation, runtime and state problems from their observed symptoms.
- [Recovery](recovery.md) — reconcile partial state, reload selected Tables, refresh a mirror or deliberately empty targets.
- [Automation](automation.md) — run Weaver unattended with explicit interaction, authentication and output boundaries.
- [Sessions and workflows](sessions-and-workflows.md) — compose ordinary commands interactively or as a checked sequence.
- [Promote a build bundle](promote-a-bundle.md) — separate destination-specific Build planning from installation.

Use [How Weaver works](../core-concepts/how-weaver-works.md) for the model behind the steps, the [CLI reference](../reference/cli.md) for exact command forms, and the [Load contract](../contracts/load.md) for selection and failure behaviour.
