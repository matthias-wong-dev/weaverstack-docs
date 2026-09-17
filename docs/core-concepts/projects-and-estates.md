# Projects and estates

A **project** is the source you author. It declares the Fabric items and resources that Weaver should build, load and test. An **estate** is that model considered as a whole: the logical items in the project, their physical Fabric targets and the state Weaver records after installing and operating them.

Keeping those meanings separate helps answer three different questions:

- **What should exist?** Read the project.
- **Where should it exist?** Read the workspace configuration and installed bindings.
- **What is installed and healthy now?** Read the Weaver catalogue through Load, Test and Health.

[How Weaver works](how-weaver-works.md) places those questions in the normal lifecycle. [Logical and physical items](logical-and-physical-items.md) explains how a declaration is bound to Fabric.

## A project declares the desired estate

A project groups resources beneath logical Lakehouse and Warehouse items:

```text
parcel-ops/
├── workspace-config.yml
├── workflow.yml
├── Lakehouse/
│   └── Landing/
│       ├── Files/
│       └── Tables/
└── Warehouse/
    └── Operations/
```

`Lakehouse/Landing` and `Warehouse/Operations` are stable project identities. The documents beneath them declare resources such as parcel event folders, Delta tables, Warehouse tables, views, Tests and Assumptions. See [Resources and artefacts](resources-and-artefacts.md) for the distinction between those declarations and what Weaver installs from them.

The project is desired state, not a description of whatever happens to be in Fabric. Editing `Warehouse/Operations/Parcel.Status.sql` changes the desired estate. It does not change the installed estate until a successful Build includes `Warehouse/Operations`.

The [Lakehouse pipeline](../guides/lakehouse-pipeline.md) and [Warehouse pipeline](../guides/warehouse-pipeline.md) show the project layouts for each item kind.

## The installed estate is a built generation

Build reads project source, resolves the selected logical items to physical targets, and reconciles those targets with the selected declarations. A successful Build also records the installed generation and its bindings in the Weaver catalogue.

That installed generation is the authority for later operations:

- Load runs the installed data work, not the current files in the project folder.
- Test runs the installed Tests and Assumptions.
- Health reports the installed items and their build, load and test state.

This means source and installed state can differ deliberately while you are editing. Run `weaver check` to validate the edited project locally; run Build when that version should become operational. The [First project](../get-started/first-project.md) demonstrates the complete transition from one declaration to a healthy installed estate.

Build selection matters. Building one item updates that item, not every item in the project. The same boundary applies to later item-level operations; consult the [CLI reference](../reference/cli.md#item-and-target-selection) for each command's syntax.

## Operational state belongs to the installed estate

After Build, Load and Test add operational facts: which installed work ran, which validations passed, and whether the selected estate remains current and successful. Those facts do not become project source. They are records about one installed generation in one configured workspace.

A useful working loop is therefore:

```text
edit project → check → build selected items → load → test → health
```

Changing a declaration without rebuilding leaves Load and Test on the previous installed generation. Changing only the workspace configuration does not redirect already installed work either: Build uses configuration to establish bindings, while Load and Test use the bindings recorded by the successful Build. The [Load contract](../contracts/load.md#execution-boundary) defines that boundary precisely.

## Project folder, source and repository

These terms differ only where the distinction changes an action:

- A **project folder** is the local directory that holds the project. It commonly contains `workspace-config.yml`, `workflow.yml`, documentation and the `Lakehouse/` or `Warehouse/` trees.
- A **source** is the input passed to Build. It can be a project folder or, inside a Fabric session, an `abfss` location. Build's positional `SOURCE` selects this input.
- A **repository** is Weaver's parsed model of the recognised item declarations in that source. Files outside the recognised item trees can belong to the surrounding project without becoming Weaver declarations.
- A **Git repository** is version control. It may contain one Weaver project, several project folders or additional software; it is not itself a Weaver identity.

In the common case, running `weaver build` from a project folder makes all four ideas feel like one directory. Keep the distinction in mind when a command names another source, when a Git repository contains more than one project, or when workspace configuration must vary without changing declarations.

Next, read [Logical and physical items](logical-and-physical-items.md) to decide where this project can be installed, or [Resources and artefacts](resources-and-artefacts.md) to understand what one declaration contributes to the estate.
