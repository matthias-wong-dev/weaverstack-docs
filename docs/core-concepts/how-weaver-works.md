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

## Realise and operate the estate { #build }

[Build, Load and Test](build-load-and-test.md) connect the authored project to an operating estate. Build realises selected documents in Fabric and records the installed generation. Load runs that generation's data-producing work, and Test checks the resulting estate. Health reads and summarises the state they leave.

The separation lets project source change without silently changing installed work. Build is the boundary at which edited declarations become operational.

Continue with [Projects and estates](projects-and-estates.md) for the relationship between authored source and installed state.
