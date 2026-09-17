# How Weaver works

Weaver turns project files into an installed data estate in Microsoft Fabric.

A project contains Weaver documents grouped beneath logical Lakehouse and Warehouse items. Workspace configuration binds those logical items to Fabric items in a workspace. This keeps the authored model separate from the names and locations used by each environment.

```text
Weaver project
  logical items
    Weaver documents
          │
          │ workspace binding
          ▼
Fabric workspace
  physical Lakehouses and Warehouses
  Weaver catalogue
```

## Declare the estate

Weaver documents describe Tables, Folders, Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata. Their paths, document types and metadata establish the logical estate: what belongs to each item, how documents are identified and which documents depend on others.

The project is the authored model. It does not describe every object that happens to exist in a Fabric workspace.

## Physical bindings

A logical item has a project identity such as `Lakehouse/Landing` or `Warehouse/Operations`. Workspace configuration maps that identity to a physical Lakehouse or Warehouse and identifies the Warehouse used for Weaver's catalogue.

The same project can use different workspace configuration in development and production. The logical item names and Weaver documents remain unchanged while the workspace, catalogue and physical targets differ.

## Build, Load and Test

Build, Load and Test are the fundamental lifecycle.

### Build

Build reads the project, resolves the selected logical items and their dependencies, and installs their definitions into the bound Fabric items. A successful Build records the installed generation and bindings in the catalogue.

### Load

Load runs the installed data work for the selected items. It reads the definitions and bindings recorded by Build rather than reparsing edited project files.

### Test

Test runs the installed Tests and Assumptions for the selected items and records their outcomes.

This boundary allows source to move ahead while the previously built generation continues to run. Build the changed items when the edited declarations should become operational.

Dependencies affect Build impact and execution order inside the selected scope. They do not add unselected items to an operation.

Continue with [Projects and estates](projects-and-estates.md) for the relationship between authored source and installed state.
