# The development cycle

Make a small source change, inspect its Build preview, install it, catch up data and validate the result. Lakehouse and Warehouse changes, semantic-model refreshes and DAX validations use the same project and operating state. Mirror can supply existing data for development.

## Optional: establish a mirrored development baseline

Mirror works between existing physical Fabric items in one workspace. The source catalogue and its recorded source targets must already contain the estate to copy. The destination catalogue Warehouse and every selected destination target must also exist. Mirror empties and reconstructs their contents; it does not create a Warehouse, Lakehouse or other Fabric item. It never empties the source items.

For one concrete setup, suppose the existing source estate in the `Parcel Operations` workspace uses the catalogue Warehouse `ParcelCatalogue` and target Warehouse `ParcelOperations`:

1. In the Fabric portal, open `Parcel Operations` and verify that both source Warehouses exist and that `ParcelCatalogue` is the catalogue for the installed source estate.
2. In that same workspace, create two empty Warehouses named `ParcelCatalogueDev` and `ParcelOperationsDev`. Creating these destinations in the portal leaves the project and source estate unchanged.
3. Add this separate development configuration beside the project:

```yaml title="workspace-development.yml"
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Warehouse/Operations: ParcelOperationsDev
```

Before mutation, check the portal item list and the configuration together. The intended boundary is:

```text
source catalogue:      Warehouse/ParcelCatalogue
destination catalogue: Warehouse/ParcelCatalogueDev
target:                 Warehouse/Operations
source physical item:   Warehouse/ParcelOperations
destination item:       Warehouse/ParcelOperationsDev
workspace:               Parcel Operations
```

The source physical item comes from the binding recorded in the source catalogue. It is not supplied by the development configuration. Stop if any name or item type differs, or if a source and destination are not in the same workspace.

Run Mirror once:

```bash
weaver mirror --workspace-config workspace-development.yml
```

Weaver resolves the source bindings, then displays the source catalogue, destination catalogue and each logical-to-destination target mapping before it asks once for confirmation. Compare that settled plan with the source and destination names checked above, then confirm it if correct or decline it if not. Mirror has no dry-run mode, and declining leaves the destinations unchanged.

Mirror empties and reconstructs the displayed destination catalogue and targets from the source estate. Unchanged objects begin as borrowed source data. The destination catalogue records that state, while the project's logical items and Weaver documents remain unchanged.

Inspect the baseline:

```bash
weaver health --workspace-config workspace-development.yml
```

See [Mirrors](../core-concepts/mirrors.md) for borrowed and local data. Exact Mirror selection, authorisation and failure boundaries are in [Mirror operation behaviour](../reference/operation-behaviour/mirror.md).

## Edit and iterate

Use this loop after an initial successful source-item Build, with or without Mirror:

```text
edit
  → check
  → build
  → load --stale
  → test
  → health
  → repeat
```

After editing and checking, inspect the Build scope first:

```bash
weaver check .
weaver build . --item Warehouse/Operations --dry-run --workspace-config workspace-development.yml
```

The preview reads existing targets and shows selected work and destructive consequences without installing or changing catalogue/runtime state. It is not a retained executable bundle, and cannot provision missing selected Power BI targets. Use ordinary Build for a first deployment.

Run the inspected source-item loop against the same development configuration:

```bash
weaver check

weaver build . \
  --workspace-config workspace-development.yml

weaver load \
  --stale \
  --workspace-config workspace-development.yml

weaver test \
  --workspace-config workspace-development.yml

weaver health \
  --workspace-config workspace-development.yml
```

Check validates project source locally. Build compares that source with the mirrored installed state. Changed borrowed objects and affected descendants inside the Build selection become local; unchanged objects remain borrowed.

Build resets changed loadable work to a non-Green state. `load --stale` selects the installed loadable objects that now need work while leaving Green objects alone. Test runs the installed validations, and Health shows the resulting Load, Tests and Build state.

Run the loop item-wide by default. Use `--name` only for deliberate targeting, diagnosis or Table reconstruction; plain named Load does not add or order dependencies. [Run part of an estate](../advanced/run-part-of-an-estate.md) teaches deliberate ancestor/descendant expansion with a preview.

## Include semantic models and Reports

Keep their native definitions under `PowerBI/` in the same project. Use the same workspace configuration, with [development and production target mappings](power-bi/environments.md) for the model and Report.

Build source-data changes first, then deploy a changed model or Report in a separate call:

```bash
weaver build . --item PowerBI/Parcel --workspace-config workspace-development.yml
weaver load --stale --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

This example assumes `PowerBI/Parcel` is present and its targets are configured. Build deploys the model before its linked Report. The estate-wide commands then cover source data, model refreshes and their validations. A source change can make the model stale even when its definition has not changed. See [Connect a semantic model to source data](power-bi/fabric-integration.md).

Re-mirror only when the intended result is a fresh source baseline. It replaces local materialisations inside the displayed destination boundary; it is a reset, not an iteration step.
