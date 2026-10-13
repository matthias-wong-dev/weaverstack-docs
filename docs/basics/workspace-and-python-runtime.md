# Configure a workspace and Python runtime

Workspace configuration chooses destinations. A Fabric Environment supplies packages to hosted work. Standalone Power BI does not require that Environment or a catalogue; use [Power BI environment switching](power-bi/environments.md) for model/Report targets.

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
| Desktop Lakehouse Build, including Spark SQL source | Matching Weaver Build runtime required for hosted execution |
| Desktop Lakehouse Load/Test, including generated Spark SQL work | Environment with Weaver required |
| Python Table or Folder | Required for Load |
| Python Test or Assumption | Required for Test |

Check is local and needs no published runtime. Build does not call authored `read()` methods, but a Spark-backed Build now admits the matching hosted Weaver runtime before mutation. Do not infer “no runtime needed” from “not running authored code”. A notebook already in Fabric uses its attached runtime. Pure Warehouse T-SQL and standalone Power BI avoid this Spark runtime prerequisite.

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

For this private source snapshot, the hosted runtime must match the local Weaver code. Use a checkout at the documented revision with Weaver installed editable and build dependencies available, then publish its wheel:

```bash
weaver fabric environment publish --path Environment/ParcelRuntime.Environment --workspace-config workspace-development.yml --dev
```

The [installation page](../getting-started/installation.md) describes the snapshot target. A normal PyPI overlay cannot supply an unpublished development version. For a matched published release, omit `--dev`. Weaver overlays the runtime requirement, creates or updates `ParcelRuntime`, asks Fabric to publish and waits for a terminal result. An unchanged successful definition is reported without another publication.

Republish after changing the Environment definition or the Weaver package mode. Editing a Python Table, Folder, Test or Assumption does not by itself require republication; Build installs those project changes.

The local directory layout, package overlay, publication modes and ownership rules are in [Fabric Environment definition](../reference/configuration-files/fabric-environment.md). After publication, run the normal lifecycle against the same workspace configuration. A real hosted Build/Load/Test establishes that Fabric attached the runtime. Build checks matching Weaver version, supported plan format, writer version and required executor capabilities before mutation; a read-only preview does not establish runtime compatibility.
