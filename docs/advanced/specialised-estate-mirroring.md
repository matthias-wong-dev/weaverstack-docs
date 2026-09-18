# Mirror an estate for specialised development

Mirror starts a destination catalogue from an installed source estate. You can then borrow selected item data, materialise selected items locally, or leave their copied bindings pointing at the source.

This route suits a development estate where most installed state should match an existing estate but one part needs isolated work. Mirror is destructive at every displayed destination and has no dry-run mode.

## Choose the result before running Mirror

For each logical item, choose one of three outcomes:

| Intended result | Action | Resulting binding and data |
| --- | --- | --- |
| Keep using the source item | Do not select it for Mirror or Build | The copied installation continues to name the source target. |
| Borrow source data through a development item | Select it with `weaver mirror --item` | The logical item is rebound to the development target; its data remains source-owned. |
| Own a complete development copy | Fork the catalogue, then select it with `weaver build --item` | Build installs the authored local form in the development target. |

Borrowed Warehouse Tables and Views become local Views over source relations. Borrowed Lakehouse Tables and Folders become OneLake shortcuts; source Views use local wrapper Views. Weaver copies the execution work needed by Load and Test into the destination item, but borrowed objects are not loadable there because their rows remain owned by the source.

A later Build localises a borrowed object only when that selected object changed or is an affected selected descendant. Unchanged borrowed objects remain borrowed, so one destination item can contain both borrowed and local objects.

## Prerequisites

- A source catalogue and destination catalogue in the same Fabric workspace. They must be distinct Warehouses.
- An installed source item for every logical item you intend to mirror.
- Emptyable destination items of the corresponding kind. Mirror empties them; it does not merge their contents.
- A workspace configuration that names the source, destination and development bindings, or the equivalent command options.

For example, create `workspace-development.yml`:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

`mirror` is the catalogue read from. `catalogue` is the catalogue rebuilt. A configuration containing only `catalogue` describes a source estate and cannot also supply the destination for Mirror.

## Inspect the complete destination boundary

Run Mirror interactively before using it in automation:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Lakehouse/Landing \
  --item Warehouse/Operations
```

Omitting `--item` selects every configured target. Use `--no-item` when you intend to fork only the catalogue. Do not combine `--no-item` with item selection.

Before asking for confirmation, Weaver reads and validates the source catalogue, resolves each source installation, settles final bindings and checks the destinations for conflicts. The displayed plan names the destination catalogue and every selected destination item that will be emptied. Decline the prompt if any destination is unexpected.

The preflight rejects a destination that is also read as a source, two selected logical items sharing one physical destination, or an item missing from the source installation. It also refuses to rebind an item from a source catalogue that is already mirrored: borrowed state records one source hop.

## Create a catalogue-only branch

Fork installed and current state without touching an item target:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --no-item
```

After confirmation, the destination catalogue contains copied Registry, declaration, dependency, Shortcut, bookmark, Load-status and Test-status state. Operational log and load-statistic history starts empty. Item bindings remain as recorded in the source catalogue.

Use this route before materialising only one item locally:

```bash
weaver build . \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations
```

Build reads the copied installed state, compares it with project source and installs `Warehouse/Operations` into `Warehouse/ParcelOperationsDev`. Other logical items keep their copied source bindings.

## Borrow selected data into development items

To recreate selected items as borrowed forms at their configured destinations, run:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Lakehouse/Landing \
  --item Warehouse/Operations
```

You may override one configured destination explicitly:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations=Warehouse/ParcelOperationsExperiment
```

Logical Shortcuts are recreated against the final bindings settled for this run. When one selected item points at another, Weaver orders the producer before the consumer. Physical Shortcuts retain their recorded workspace and item.

After Mirror completes, inspect the destination estate:

```bash
weaver health \
  --workspace-config workspace-development.yml \
  --item Lakehouse/Landing \
  --item Warehouse/Operations
```

Health reports the destination estate's installed and operational view. Copied catalogue state is a point-in-time branch, while a borrowed object's Load lifecycle state remains sourced from the catalogue where its data is loaded. Neither is proof that every source object remained unchanged after the mirror.

## Run it unattended only after reviewing the same scope

An unattended mirror needs both interaction policy and destructive authorisation:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations \
  --non-interactive \
  --yes
```

`--non-interactive` prevents prompts and browser sign-in. It does not authorise emptying. `--yes` authorises every destination in the settled plan. Keep the configuration and item selection under change control so the reviewed boundary is the one the job resolves.

## Recover from a failed mirror

Failures during preflight leave destinations unchanged. Once execution starts, Weaver rebuilds the destination catalogue and then processes selected item destinations in settled order. A later failure does not restore earlier contents or roll back completed destinations.

Correct the reported Fabric, copy, Shortcut or binding failure, then run Mirror again against the intended source and selection. A rerun performs a new reconstruction; it is not rollback. Do not run Load against a partially reconstructed destination merely because some targets completed.

See the [Mirror contract](../contracts/mirror.md) for copied tables, borrowed forms, localisation and failure boundaries. See [`weaver mirror`](../reference/cli/mirror.md) for complete syntax and output behaviour.
