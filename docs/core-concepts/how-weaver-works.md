# How Weaver works

Weaver turns authored project files into an installed and observable data estate in Microsoft Fabric.

```text
Weaver documents
      ↓ Build
installed estate
      ↓ Load
data + load state
      ↓ Test
validation state
      ↓ Health
current estate view
```

Each stage has a different source of truth. Keeping those stages separate explains why editing a file does not immediately change a running estate, and why Load and Test continue to use the last successful Build.

## Author Weaver documents

A project groups Weaver documents beneath logical Lakehouse and Warehouse items. A document's path, kind, metadata and authored body describe what should exist and what work Weaver should install.

The logical names belong to the project. A [workspace configuration](logical-and-physical-items.md) binds them to Lakehouses and Warehouses in a Fabric workspace.

## Build installs a generation

Build interprets the selected project source, resolves its physical bindings and installs the required definitions and executable work. A successful Build records the installed generation and its bindings in the [catalogue](catalogue.md).

That installed generation is the boundary between source and operation. Editing project files changes the intended estate; Build makes those edits operational.

## Load runs installed data work

Load starts from catalogue state, not from the files currently on disk. It runs the installed work for Tables and Folders in the selected logical items, changes their data and records the result.

## Test runs installed validations

Test also starts from the installed generation. It runs Tests and Assumptions against estate data and records whether each validation passed, failed or could not run.

## Health reads the estate

Health combines installed declarations, current Load and Test state and, by default, physical inventory. It reports the estate as it stands; it does not install or execute authored work.

## Mirror can establish a development baseline

Mirror creates a development catalogue from another installed estate and presents selected source data through development targets. The development estate can therefore begin with borrowed data. When Build installs a changed borrowed object locally, that object becomes local while unchanged objects can remain borrowed.

Mirror changes how a development estate begins; the normal Build → Load → Test → Health lifecycle remains the same. See [Mirrors](mirrors.md) for that model.

Continue with [Projects and estates](projects-and-estates.md) for the distinction between source, logical model, installed generation and physical Fabric state.
