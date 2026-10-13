# How Weaver works

Weaver deploys native Power BI projects and manages authored Python/SQL work in Fabric. Choose the route that fits the work; a persistent catalogue is not a prerequisite for standalone Power BI.

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

This diagram is the catalogue-backed Fabric route. [Power BI deployment](../basics/power-bi/deploy-pbip.md) starts with a native model and linked Report instead. Each stage has a different source of truth. Keeping those stages separate explains why editing a file does not immediately change a running estate, and why Load and Test continue to use the last successful Build.

## Author Weaver documents

A project groups Python/SQL Weaver documents beneath logical Lakehouse and Warehouse items, and native model/Report definitions beneath `PowerBI/<project>`. Power BI definitions keep their own native syntax rather than needing a data-document metadata header. A document's path, kind, metadata and authored body describe what should exist and what work Weaver should install.

The logical names belong to the project. A [workspace configuration](logical-and-physical-items.md) binds them to Lakehouses and Warehouses in a Fabric workspace.

## Build installs a generation

Build interprets the selected project source, resolves its physical bindings and installs the required definitions and executable work. With a catalogue, a successful Build records the installed generation and its bindings there. Without one, Power BI Build uses configured targets, deploys and verifies the selected native items without persistent Weaver records. Source items and Power BI items use separate Build calls.

That installed generation is the boundary between source and operation. Editing project files changes the intended estate; Build makes those edits operational.

## Load runs installed data work

Catalogue-backed Load starts from installed state, not unbuilt definitions on disk. Catalogue-free Load instead refreshes named deployed semantic models through configured targets; Reports have no Load step. It runs the installed work for Tables and Folders in the selected logical items, changes their data and records the result.

## Test runs installed validations

Catalogue-mode Test starts from installed validations. Source/file mode reads authored validations and runs them against deployed objects without recording catalogue history; a DAX Assumption can use this mode on a standalone model. It runs Tests and Assumptions against estate data and records whether each validation passed, failed or could not run.

## Health reads the estate

Health combines installed declarations, current Load and Test state and, by default, physical inventory. It reports the estate as it stands; it does not install or execute authored work.

## Mirror can establish a development baseline

Mirror creates a development catalogue from another installed estate and presents selected source data through development targets. The development estate can therefore begin with borrowed data. When Build installs a changed borrowed object locally, that object becomes local while unchanged objects can remain borrowed.

Mirror changes how a development estate begins; the normal Build → Load → Test → Health lifecycle remains the same. See [Mirrors](mirrors.md) for that model.

Continue with [Projects and estates](projects-and-estates.md) for the distinction between source, logical model, installed generation and physical Fabric state.
