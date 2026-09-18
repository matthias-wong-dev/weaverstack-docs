# Workspace configuration

A workspace configuration binds logical Weaver items to physical Fabric items. It also selects the catalogue, optional Spark runtime and optional Mirror source used in that estate.

## File and discovery

The conventional filename is exactly `workspace-config.yml`. Automatic discovery checks only the process's current working directory. It does not search parent directories, inspect the Build source path or try other filenames.

`--workspace-config PATH` selects that file instead of the discovered file. The path may name any file; its basename has no semantic meaning.

The file must contain one YAML mapping. An empty document, YAML `null` and a mapping without `workspace` all fail because `workspace` is required.

## Complete shape

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
environment: Platform Runtimes/ParcelRuntime
mirror: Warehouse/ParcelCatalogue

execution:
  parallel_workers: 8

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations:
    name: ParcelOperationsDev
    execution:
      parallel_workers: 4
```

Only the keys shown above are accepted. Unknown keys are rejected at the top level and inside `execution` or a target mapping. The retired top-level keys `lakehouses` and `warehouses` are rejected; use `targets`.

## Top-level keys

| Key | Shape | Required | Default | Meaning and restrictions |
| --- | --- | --- | --- | --- |
| `workspace` | non-empty string | yes | — | Fabric workspace in which the workload, catalogue and targets are resolved. Fabric-name validation applies. |
| `catalogue` | `Warehouse/Name` | no | unset | Warehouse holding the Weaver catalogue. The kind must be the literal `Warehouse`; a workspace-qualified value is not accepted here. |
| `environment` | `Environment` or `Workspace/Environment` | no | unset | Published Fabric Environment attached to Spark work. A qualified reference may select an Environment owned by another workspace. This key does not create or publish it. |
| `mirror` | `Warehouse/Name` or `Workspace/Warehouse/Name` | no | unset | Source catalogue for Mirror and mirrored-state reads. Although the qualified form parses, Mirror and mirrored-state reads reject a source outside the resolved `workspace`. |
| `execution` | mapping | no | `{}` | Workspace-level execution settings. |
| `targets` | mapping from logical item to target declaration | no | `{}` | Build and Mirror destination bindings. An operation that needs an absent binding fails when resolving that item. |

`workspace`, Environment components, catalogue names and physical target names use Fabric-name validation. Leading and trailing whitespace is removed. A name must not be empty, consist only of dots, or contain `/`, `\\`, `:`, `*`, `?`, `"`, `<`, `>` or `|`. The `/` characters shown in catalogue and Environment references are separators between validated components.

### `execution`

```yaml
execution:
  parallel_workers: 8
```

| Key | Accepted value | Default |
| --- | --- | --- |
| `parallel_workers` | integer greater than zero; booleans are not integers here | unset |

An unset value leaves parallelism to the operation or executor. There is no configuration-level numeric default.

### `targets`

Each key is an exact logical item identity:

```text
Lakehouse/Name
Warehouse/Name
```

Each value has one of two shapes:

```yaml
# Short form
Lakehouse/Landing: ParcelLandingDev

# Long form
Warehouse/Operations:
  name: ParcelOperationsDev
  execution:
    parallel_workers: 4
```

The short-form string and long-form `name` are physical Fabric item names, not typed target references. The logical key supplies the physical kind: a `Lakehouse/...` key binds a Lakehouse and a `Warehouse/...` key binds a Warehouse.

The long form accepts only `name` and `execution`. `name` is required. Its `execution` mapping has the same single `parallel_workers` key as the top-level mapping. A target-level value overrides the workspace-level value for that item; otherwise the workspace-level setting applies.

`targets` may be absent or empty. Two logical items may parse with the same physical name, but one Build or Mirror cannot install two ordinary items of the same kind into one destination. A valid configuration therefore does not prove that all its bindings can be used together.

## What each binding controls

- `workspace` chooses the Fabric workspace context.
- `catalogue` is a separate Warehouse binding for installed definitions and operational state. It is never an implicit target for a logical Warehouse.
- `targets` supplies physical destinations to Build and Mirror. Build records the settled bindings in the catalogue.
- Load, Test and Health read installed bindings from the selected catalogue; they do not retarget installed work from the current `targets` mapping.
- `environment` selects a published runtime for Spark work. It is neither a target nor a publication instruction.
- `mirror` identifies a source catalogue. Loading the configuration neither reads that catalogue nor runs Mirror.

## Workspace resolution and precedence

An operation resolves its base workspace in this order:

1. an explicit `--workspace` and/or `--workspace-config`;
2. the Workspace already owned by a supplied Session;
3. `workspace-config.yml` in the current working directory;
4. the current Fabric notebook workspace;
5. an error if no workspace can be resolved.

The details are consequential:

- `--workspace-config FILE` loads `FILE` and bypasses automatic discovery.
- `--workspace NAME` without `--workspace-config` bypasses automatic discovery and creates a workspace with no configured catalogue, Environment, Mirror source, execution settings or targets.
- Supplying both uses the file as the base and replaces only its `workspace` value.
- Explicit `--catalogue` and `--environment` values replace the corresponding value on whichever base won, including a Session-owned Workspace.
- A Session is considered only when neither an explicit workspace nor an explicit configuration was supplied.
- A discovered file is considered before Fabric notebook context. Discovery is not based on the project directory passed to `build SOURCE`.

Health has no Environment argument because it executes no authored Spark work. Check reads project source locally and does not resolve this configuration.

## Configuration selection

Development and production are ordinary files selected by path. Their filenames and suffixes have no recognised meaning.

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

```bash
weaver build . --workspace-config workspace-development.yml
weaver load --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
```

Both files bind the same logical items. Selecting a file changes the physical estate addressed by the operation; it does not rename the project, items or documents.

## Mirror source and destination resolution

Mirror resolves its two catalogue roles separately:

1. source: explicit `--mirror`, then configured `mirror`, then configured `catalogue`;
2. destination: explicit `--catalogue`, otherwise configured `catalogue` only when a configured `mirror` is present.

A configuration containing only `catalogue` therefore describes a possible source estate, not an inferred destination. The destination must be supplied separately. A configuration containing both uses `mirror` as the source and `catalogue` as the destination.

Both catalogues must resolve to distinct Warehouses in the selected `workspace`. A value such as `Production/Warehouse/ParcelCatalogue` is accepted by the configuration parser but rejected by Mirror when `workspace` is not `Production`; it does not enable cross-workspace mirroring. Destination targets also belong to the selected workspace because target declarations carry names, not workspace qualifiers.

The development example above is valid because its source catalogue, destination catalogue and destination targets all belong to `Parcel Operations`.

## Validation boundary

Configuration loading validates YAML shape, accepted keys, logical item syntax, reference syntax, Fabric names and positive worker counts. It does not contact Fabric. Existence, item kind, permissions, Environment publication state and catalogue compatibility are checked only by operations that use those references.

Operation-specific requirements remain separate:

- catalogue-backed operations require a resolved `catalogue`;
- Build and Mirror require a destination binding for each selected item unless `ITEM=TARGET` supplies it;
- Build with no `--item` requires at least one configured target;
- Mirror applies the source/destination rules above;
- remote runtime work may require a published Environment.

See [Fabric Environment definition](fabric-environment.md), [Shared selection and identity](../operation-behaviour/shared-selection-and-identity.md) and the individual [operation behaviour](../operation-behaviour/index.md) pages.
