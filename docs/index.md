# Weaver

A production data estate needs more than transformation code: it needs a definition of what should exist and recorded state of what is installed, what changed, what succeeded or failed, where incremental work resumes and what remains to do. Weaver defines and operates that stateful Microsoft Fabric estate from native SQL and Python, keeping logical project source separate from physical bindings so the same project can run from a desktop or inside Fabric and bind to different development and production estates.

## Choose a route

**New to Weaver**

[Install Weaver](getting-started/installation.md), then [create and run a first project](getting-started/first-project.md). The first-project path validates source and runs Build, Load, Test and Health against a Warehouse-only estate.

**Building a pipeline**

Start with the [Lakehouse pipeline](basics/lakehouse-python.md) or [Warehouse pipeline](basics/warehouse-pipeline.md), then add [incremental processing](advanced/incremental-data-processing.md), [Shortcuts](basics/shortcuts.md) or [validation](basics/tests-and-assumptions.md) as the project requires.

**Operating an estate**

Use [Run and inspect an estate](basics/run-and-inspect-estate.md) for the routine inspect–preview–run–verify cycle. Continue to [Troubleshooting](basics/troubleshooting.md), [Recover failed work](basics/recover-failed-work.md) or [Automation and execution contexts](advanced/automation-and-execution-contexts.md) for the relevant operating boundary.

**Understanding or integrating Weaver**

Read [How Weaver works](core-concepts/how-weaver-works.md) for the public model and [Design philosophy](core-concepts/design-philosophy.md) for the principles behind it. Use [Reference](reference/index.md) for exact interfaces and operation behaviour.
