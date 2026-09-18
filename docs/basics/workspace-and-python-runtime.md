# Configure a workspace and Python runtime

Workspace configuration binds the logical items in a Weaver project to a physical Fabric estate. A Fabric Environment is separate: it supplies packages to Python code running in Fabric.

## Bind the project to Fabric

Create `workspace-config.yml` in the directory where you run Weaver:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

The keys under `targets` are logical item identities from the project. Their values are physical Fabric item names. The catalogue is another physical Warehouse: it records the project's installed definitions, bindings and operational state.

Commands run from this directory discover `workspace-config.yml`:

```bash
weaver build .
weaver load
weaver test
weaver health
```

Build reads the selected target bindings. Load, Test and Health use the bindings that Build recorded in the selected catalogue. Changing `targets` therefore does not retarget already installed work until Build installs the project with the new configuration.

See [Logical and physical items](../core-concepts/logical-and-physical-items.md) for this model and [Workspace configuration](../reference/configuration-files/workspace-config.md) for the exact keys, discovery and precedence rules.

## Keep development and production bindings separate

The same project can carry more than one configuration while retaining the same Weaver documents and logical identities.

```yaml title="workspace-production.yml"
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

```yaml title="workspace-development.yml"
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

Select the intended estate explicitly when the file is not named `workspace-config.yml`:

```bash
weaver build . --workspace-config workspace-development.yml
weaver load --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Use the same file for one lifecycle. Switching files changes the workspace, catalogue, optional mirror source, runtime and physical targets; it does not rename `Lakehouse/Landing` or `Warehouse/Operations`.

The `mirror` setting names a source catalogue. Loading the configuration does not run Mirror. The [Development cycle](development-cycle.md) shows how to inspect and apply that operation deliberately.

## Add a Fabric Environment for Python work

A Fabric Environment is needed when remote work imports Weaver in Fabric:

| Installed work | Published Environment containing Weaver |
| --- | --- |
| Warehouse T-SQL | Not required |
| Lakehouse Spark SQL | Not required; it can use the workspace's default Spark runtime |
| Python Table or Folder | Required for Load |
| Python Test or Assumption | Required for Test |

Check is local. Build installs Python definitions but does not run their authored methods, so neither operation requires the published Environment merely because the project contains Python. The requirement begins when Load or Test runs that Python in Fabric.

Add the Environment binding to the selected workspace configuration:

```yaml
workspace: Parcel Operations
environment: ParcelRuntime
catalogue: Warehouse/ParcelCatalogueDev

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

The binding attaches an existing published Environment to Spark sessions. It does not create or publish one.

## Publish the runtime

Use a local Fabric Environment definition, such as the directory created by `weaver initialise`, and publish it to the workspace selected by the configuration:

```bash
weaver fabric environment publish \
  --path Environment/ParcelRuntime.Environment \
  --workspace-config workspace-development.yml
```

Weaver overlays its Fabric runtime requirement, creates or updates `ParcelRuntime`, asks Fabric to publish it and waits for a terminal result. An unchanged successful definition is reported without another publication.

Republish after changing the Environment definition or the Weaver package mode. Editing a Python Table, Folder, Test or Assumption does not by itself require republication; Build installs those project changes.

The local directory layout, package overlay, publication modes and ownership rules are in [Fabric Environment definition](../reference/configuration-files/fabric-environment.md). After publication, run the normal lifecycle against the same workspace configuration. A real Python Load or Test is the check that Fabric attached the published Environment and could import Weaver.
