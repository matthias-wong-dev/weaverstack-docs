# Guides

Guides complete a task. Start with [First project](../get-started/first-project.md) if you have not yet run Build, Load, Test and Health against a working estate.

## Build a pipeline

Choose the engine that owns the work:

- [Lakehouse pipeline](lakehouse-pipeline.md) — load managed files into a Python Table, then add a separate Spark SQL Table.
- [Warehouse pipeline](warehouse-pipeline.md) — build and load a T-SQL Table with a dependent View, without Spark.

Extend that pipeline with:

- [Incremental loads](incremental-loads.md) — process changed and deleted managed files using a Table bookmark.
- [Shortcuts](shortcuts.md) — connect logical items or expose an external Fabric location.
- [Validation](validation.md) — install and run Tests and Assumptions against the estate.
- [Workspaces and Fabric Environments](environments.md) — separate physical estate bindings from Python runtime publication.

## Operate the estate

- [Operate an estate](operate-estate.md) — inspect, preview, run and verify installed work.
- [Troubleshooting](troubleshooting.md) — diagnose project, workspace, installation, runtime and state problems from observed symptoms.
- [Recovery](recovery.md) — reconcile partial state, reload selected Tables, refresh a mirror or deliberately empty targets.

Start with the operating guide for routine work. Move to Troubleshooting when you need to identify the failing boundary; use Recovery only after you understand the state and intended effect.

## Automate and promote

- [Automation](automation.md) — run Weaver unattended with explicit interaction, authentication and output boundaries.
- [Sessions and workflows](sessions-and-workflows.md) — compose ordinary commands interactively or as a checked sequence.
- [Promote a build bundle](promote-a-bundle.md) — separate destination-specific Build planning from installation.

Use [How Weaver works](../core-concepts/how-weaver-works.md) for the model behind these tasks, the [CLI reference](../reference/cli.md) for exact command forms and [Contracts](../contracts/index.md) for operation-specific selection, state and failure behaviour.