# Configuration contract

Workspace configuration binds a project to one Fabric estate. It names the Fabric workspace, catalogue Warehouse, optional Fabric Environment, optional mirror source, execution settings and logical-item targets. It does not declare project documents or change their logical identities.

The conventional filename is `workspace-config.yml`. Automatic discovery checks only the current working directory; it does not search parent directories or infer the configuration from a separately supplied Build source path.

## Keys

`workspace` is the only required top-level key. The supported keys are:

| Key | Value | Behaviour |
| --- | --- | --- |
| `workspace` | non-empty Fabric workspace name | Workspace in which unqualified bindings are resolved |
| `catalogue` | `Warehouse/Name` | Warehouse that records the installed estate and operational state |
| `environment` | `Environment` or `Workspace/Environment` | Published Fabric Environment attached when Spark work requires it |
| `mirror` | `Warehouse/Name` or `Workspace/Warehouse/Name` | Source catalogue for an explicit Mirror operation |
| `execution.parallel_workers` | positive integer | Default parallel-worker setting |
| `targets` | mapping keyed by logical item identity | Physical Lakehouse and Warehouse bindings used by Build |

A complete form is:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
environment: ParcelRuntime
mirror: Parcel Production/Warehouse/ParcelCatalogue

execution:
  parallel_workers: 8

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations:
    name: ParcelOperationsDev
    execution:
      parallel_workers: 4
```

A target key is an exact `Lakehouse/<Name>` or `Warehouse/<Name>` logical item. Its value is either a physical item name or a mapping containing `name` and optional `execution.parallel_workers`. The logical key supplies the physical kind. An item-level worker setting overrides the workspace default for that item; when absent, the workspace default applies.

The `catalogue` key must name a Warehouse. It is not a project target and does not satisfy a missing `targets` entry. The `environment` key binds a published runtime definition; it neither creates nor publishes that Environment. The `mirror` key records a source catalogue; loading the configuration does not run Mirror.

## Resolution and precedence

Workspace context resolves in this order:

1. an explicitly supplied workspace name or workspace-configuration file;
2. a Workspace already owned by the supplied Session;
3. `workspace-config.yml` in the current working directory;
4. the current Fabric notebook workspace;
5. an error stating that a workspace is required.

An explicit `--workspace-config` path is loaded instead of the discovered file. Within a resolved configuration, explicit workspace, catalogue and Environment arguments override the corresponding configured values. Supplying an explicit workspace without a configuration bypasses automatic configuration discovery; it does not inherit discovered catalogue or target values. Supplying both an explicit workspace and an explicit configuration retains the configuration's other values while replacing its workspace.

A Session's Workspace takes precedence over automatic file discovery, but an explicit workspace or configuration takes precedence over the Session. Explicit catalogue and Environment arguments can override whichever base Workspace was selected.

Target bindings come from the selected configuration unless Build's item selection supplies an explicit `ITEM=TARGET` binding. Load, Test and Health do not reinterpret the current `targets` mapping; they read the installed item bindings from the selected catalogue.

## Development and production switching

Development and production are selected by choosing different configuration files, not by changing project paths or logical identities. For example:

```yaml
# workspace-production.yml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogue
targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

```yaml
# workspace-development.yml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue
targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

Both files bind `Lakehouse/Landing` and `Warehouse/Operations`. Selecting one changes the physical workspace context, catalogue, optional mirror source, Environment and targets for that operation. It does not rename the items or alter their Weaver documents. The filenames and physical-name suffixes above are examples, not recognised environment labels.

Use one selected configuration throughout a Build, Load and Test lifecycle. Selecting another file addresses another estate even when the project source is unchanged. Mirror uses the selected configuration's `catalogue` as its destination, `mirror` as its source and `targets` as destination bindings; it runs only when explicitly requested.

## Failure boundaries

Configuration loading fails before an operation proceeds when:

- the file is absent, is not a YAML mapping or omits `workspace`;
- a top-level, execution or target key is unknown;
- a workspace, catalogue, Environment, mirror or physical target has an invalid shape or name;
- `catalogue` does not name a Warehouse;
- a target key is not a canonical logical item identity;
- a target mapping omits `name`;
- `parallel_workers` is not a positive integer.

Retired `lakehouses` and `warehouses` sections are rejected; use one item-keyed `targets` mapping.

Parsing a configuration does not require `catalogue` or `targets`. Individual operations enforce what they need:

- Check reads no workspace configuration;
- catalogue-backed operations fail if no catalogue is resolved;
- Build without explicit items fails when no configured targets select an item;
- resolving an item fails when it has no configured or explicit target;
- a configuration may map two logical items to one physical name, but Build refuses an installation that conflicts with another logical item's claim;
- remote workspace, item, Environment and permission failures occur after local configuration has parsed and are not configuration-schema success.

A valid configuration therefore establishes names and bindings, not the existence, accessibility or compatibility of the referenced Fabric items.

## Defined behaviour

The Configuration contract specifies that Weaver:

1. accepts only the documented keys and value shapes;
2. discovers `workspace-config.yml` only in the current working directory;
3. applies explicit values, Session inheritance, file discovery and notebook fallback in the stated order;
4. binds logical target keys to same-kind physical Fabric items;
5. keeps catalogue, Environment, mirror and project-target roles separate;
6. switches estates by selecting configuration, without changing logical identity;
7. rejects malformed or incomplete values before remote work and leaves remote existence checks to the operation that uses them.

See [Configure workspaces and Fabric Environments](../../basics/workspace-and-python-runtime.md) for an end-to-end setup and the [CLI reference](../cli.md) for command options.
