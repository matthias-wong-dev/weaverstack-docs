# How Weaver works

A Weaver project declares a logical estate of Microsoft Fabric items. Workspace configuration binds that estate to physical items in a Fabric workspace.

That separation matters. Project source can stay the same while development and production use different Lakehouses, Warehouses and catalogue Warehouses.

## The core model

```text
Project declarations
        ↓
Physical bindings
        ↓
Build
        ↓
Load / Test
        ↓
Operational state
        ↓
Health
```

### Project declarations

A project contains logical items such as:

```text
Lakehouse/Landing
Warehouse/Operations
```

Documents beneath those items declare tables, folders, views, tests, assumptions, shortcuts and supported Warehouse objects. These declarations describe the estate Weaver should build and operate.

### Physical bindings

`workspace-config.yml` names the Fabric workspace, catalogue Warehouse and physical target for each logical item:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue

targets:
  Lakehouse/Landing: Landing_Dev
  Warehouse/Operations: Operations_Dev
```

A logical item and its physical target are not the same thing. The logical name belongs to the project. The physical name belongs to one configured workspace.

### Build

Build reads the project, resolves identities and dependencies, compares the declared estate with Fabric and applies the required structural changes. It installs the definitions that later load and test operations run.

Build changes structure. It does not perform the project's data loads.

### Load and test

Load runs the installed data work for the selected logical items. Test runs the installed Tests and Assumptions. Dependencies determine ordering within the selected scope; selecting an item does not silently add another item.

Both operations record their outcomes in the Weaver catalogue.

### Operational state and health

The catalogue records what Weaver installed and what later runs did. Health reads that state and reports whether builds, loads and tests are current and successful for the selected estate.

Project source remains the declaration of intent. The catalogue is the record of the installed estate and its operation.

## The normal lifecycle

```text
initialise → check → build → load → test → health
```

A generated workflow can run build, load, test and health in one Session:

```bash
weaver workflow full
```

See [First project](../get-started/first-project.md) for the smallest complete path and the [Load contract](../contracts/load.md) for a precise example of behaviour users can rely on.
