# Get started

A Weaver project describes Microsoft Fabric items in local files and names the workspace where those items run. The shortest complete path is:

1. [Install Weaver](installation.md).
2. Initialise a project and its Fabric items.
3. Add a small declared table.
4. Check the project without contacting Fabric.
5. Build its structure, then load its data.

Follow [First project](first-project.md) for the complete command sequence.

Before you start, you need access to a Microsoft Fabric workspace and permission to create or use the Warehouse, Environment and any Lakehouse named during setup. Authentication can come from a configured service principal, an existing Azure CLI sign-in, or interactive browser sign-in. `--non-interactive` excludes browser sign-in.
