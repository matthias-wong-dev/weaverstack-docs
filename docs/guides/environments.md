# Configure workspaces and Fabric Environments

Three settings are often called an environment even though they control different things:

1. **Workspace configuration** selects a Fabric workspace, catalogue, physical targets, optional mirror source and optional Fabric Environment binding.
2. **Fabric Environment publication** creates or updates the runtime definition that can supply Weaver and other Python packages to Fabric Spark.
3. **Development or production selection** is the choice of workspace-configuration file for a command. The Weaver documents and logical item names stay the same.

This guide configures those boundaries for a parcel project without repeating the full [Development cycle](../core-concepts/development-cycle.md).

## Prerequisites

- [Install Weaver](../get-started/installation.md) and confirm `weaver --version` works.
- Access to the named Fabric workspace and items.
- One project containing the logical items `Lakehouse/Landing` and `Warehouse/Operations`, or adapt those keys to your project.
- The checked example files under `examples/parcel-environment/` in the documentation repository.

## 1. Bind the production estate

Create `workspace-production.yml` in the project root:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

This file provides physical context:

- `workspace` names the Fabric workspace;
- `catalogue` names the Warehouse that records Weaver's installed and operational state;
- each key under `targets` is a stable logical item;
- each target value is a physical Fabric item of the kind named by its key.

The catalogue Warehouse is not the target for `Warehouse/Operations`. [Logical and physical items](../core-concepts/logical-and-physical-items.md) explains why those identities remain separate.

## 2. Bind the development estate

Create `workspace-development.yml` beside the production file:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

This pattern is grounded in a working multi-estate project: production and development files live beside the same declarations, keep the logical target keys unchanged and vary the catalogue and physical item names. The names here are parcel examples rather than a required naming convention.

In the development configuration:

- `catalogue` is the destination development catalogue;
- `mirror` is the source production catalogue;
- `targets` bind the same logical items to development Fabric items.

The configuration does not perform a mirror. It supplies the source, destination and target bindings that `weaver mirror` uses when you explicitly run that operation. Mirror is destructive within its settled destination boundary; inspect its plan as described in the [Development cycle](../core-concepts/development-cycle.md).

## 3. Select production or development explicitly

Pass the intended file to each command:

```bash
weaver build . \
  --workspace-config workspace-development.yml

weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-development.yml

weaver test Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-development.yml
```

For production, replace the path with `workspace-production.yml`.

This option is the deployment switch. It does not rewrite declaration paths or IDs. Build reads target bindings from the selected configuration and records them in that catalogue. Load and Test then resolve installed logical items through the selected catalogue. Use one configuration consistently for a lifecycle; selecting the production file for one command and the development file for the next addresses different estates.

If a project instead uses the conventional filename `workspace-config.yml`, commands run from that directory discover it automatically. An explicit `--workspace-config` selects a named file and wins over discovery. Explicit workspace, catalogue or Environment options override their configured values; exact precedence belongs in the [CLI reference](../reference/cli.md).

## 4. Decide whether the work needs a Fabric Environment

A Fabric Environment is a Spark runtime dependency, not a synonym for the development or production estate.

| Authored work | Uses Fabric Spark | Needs a configured, published Environment carrying Weaver |
| --- | --- | --- |
| Warehouse T-SQL Table, View, Test or Assumption | No | No |
| Lakehouse Spark SQL | Yes | No; it can use the workspace's default Spark runtime |
| Python Table or Folder Load work | Yes | Yes |
| Python Test or Assumption | Yes | Yes |

Warehouse-only work uses the Warehouse SQL endpoint. Do not publish or configure an Environment merely because a configuration file represents development or production.

Spark SQL needs a Lakehouse-backed Spark session, but authored SQL does not import Weaver at runtime. Python-authored Load and Test work imports Weaver classes in Fabric, so the selected workspace configuration must name a published Environment containing Weaver. Build installs those Python definitions but does not run their authored methods; publication is required before Load or Test executes them, not before local Check.

## 5. Add the runtime binding for Python work

For development Python work, create `workspace-python-development.yml`:

```yaml
workspace: Parcel Operations
environment: ParcelRuntime
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

`environment: ParcelRuntime` is a binding used when Weaver starts a Fabric Spark session. Weaver resolves the Fabric Environment and attaches its published libraries to that session. The field does not create or publish the Environment, and adding it does not make this file “development”; the catalogue, mirror and targets establish that estate selection.

An unqualified Environment name belongs to the configured Fabric workspace. A `Workspace/Environment` reference can name an Environment owned by another workspace. Keep the unqualified form when the runtime and target workspace are the same.

## 6. Publish the Fabric Environment definition

The fixture contains this definition:

```text
Environment/
└── ParcelRuntime.Environment/
    ├── .platform
    └── Libraries/
        └── PublicLibraries/
            └── environment.yml
```

`Environment/ParcelRuntime.Environment/.platform` is:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Environment",
    "displayName": "ParcelRuntime"
  },
  "config": {
    "version": "2.0"
  }
}
```

`Environment/ParcelRuntime.Environment/Libraries/PublicLibraries/environment.yml` is:

```yaml
dependencies:
  - pip:
      - weaverstack
```

The `.platform` file declares a Fabric item of type `Environment` with display name `ParcelRuntime`. The directory name and that display name agree. No `Setting/Sparkcompute.yml` is present, so the definition does not pin Spark settings or a runtime version; Fabric applies the workspace defaults.

Publish the local definition into the workspace selected by the Python development configuration:

```bash
weaver fabric environment publish \
  --path Environment/ParcelRuntime.Environment \
  --workspace-config workspace-python-development.yml
```

The observable result is a JSON report naming `ParcelRuntime` and whether Weaver created, updated or found the Environment unchanged. Publication may take several minutes. A successful unchanged result does not republish.

Publication sends the complete local Environment definition and overlays Weaver's runtime requirement. It does not Build project declarations, change catalogue or target bindings, or choose between development and production for later commands. The workspace configuration used by those later commands supplies the attachment binding.

Republish after changing the Environment definition or the Weaver package mode. Ordinary edits to Python Table, Folder, Test or Assumption modules are installed by Build and do not by themselves require Environment republication.

## 7. Check each boundary

Check project declarations locally:

```bash
weaver check
```

This parses Weaver documents without contacting Fabric. It does not parse publication success out of Fabric or prove that Python imports in the remote Spark runtime.

Check connectivity to the Fabric workspace named by the configuration:

```bash
weaver doctor --workspace "Parcel Operations"
```

Doctor takes an explicit workspace name and does not read project configuration. It probes Fabric connectivity and available item types; it does not prove that a particular configuration file selected the intended catalogue, targets or Environment.

Then Build and dry-run the Python work with the selected file:

```bash
weaver build . \
  --workspace-config workspace-python-development.yml

weaver load Lakehouse/Landing \
  --workspace-config workspace-python-development.yml \
  --dry-run

weaver test Lakehouse/Landing \
  --workspace-config workspace-python-development.yml \
  --dry-run
```

These checkpoints answer different questions:

- Check validates source structure locally.
- Doctor verifies connectivity to the explicitly named Fabric workspace.
- Environment publication verifies the runtime definition reached Fabric and settled.
- Build installs declarations and records their physical bindings.
- dry runs show installed Load or Test selection without executing authored work.
- a real Python Load or Test proves that Fabric attached the configured published Environment and could import Weaver.

Parser success is not remote runtime evidence. Conversely, a published Environment does not prove that the selected project configuration binds to it.

## Troubleshooting and next action

If Warehouse-only work reports a Spark or Environment prerequisite, confirm that the selected scope contains only Warehouse logical items and that the command uses their Warehouse bindings. A configuration does not need an `environment` key for that path.

If Python Load or Test says that a Lakehouse requires a Fabric Environment with Weaver installed, verify all three conditions: the selected configuration has an `environment` binding, the referenced Environment exists, and its latest definition was published successfully. Then rerun the failed operation; publication does not resume it.

If work reaches the wrong catalogue or target, print and inspect the `--workspace-config` path used for every command. Do not fix the symptom by renaming logical item directories. [Catalogue](../core-concepts/catalogue.md) explains the recorded bindings, [Weaver operations](../core-concepts/weaver-operations.md) separates installation from execution, and [Fault tolerance](../core-concepts/fault-tolerance.md) explains what remains after an operation fails. Use [Weaver documents](../core-concepts/weaver-documents.md) for the authored forms and the [CLI reference](../reference/cli.md) for exhaustive options and configuration grammar.
