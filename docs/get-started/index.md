# Get started

A Weaver project declares logical Fabric items in local files and names the workspace where those items run. The shortest complete path is:

1. [Install Weaver](installation.md).
2. Initialise a project and its Fabric items.
3. Declare one table and one Test.
4. Check the project locally.
5. Build, load, test and inspect health.
6. Run the same lifecycle through a workflow.

Follow [First project](first-project.md) for the complete command sequence.

You need access to a Microsoft Fabric workspace and permission to create or use the Warehouses named during setup. Current versions of `weaver initialise` also create or reuse a Fabric Environment; the Warehouse-only first project does not publish or use it.
