# Develop using Mirror

Borrow an installed estate’s data for development, then materialise only the objects your changes need. Keep the same project documents and logical identities while the development configuration selects different physical targets.

Use Mirror only after the [ordinary development loop](development-cycle.md) is understood. **It empties and reconstructs the destination catalogue and every selected destination target**, including local materialisations there. Source items remain untouched. It is a baseline reset, not an iteration command.

## Prepare existing destinations in the same workspace

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

<!-- review-todo: mirror -->
!!! warning "TODO — capture this Mirror plan and resulting Health"
    No reset/re-mirror scope is approved, so the command above has not been run. After approving the exact disposable destination scope, capture its plan, confirmation and resulting Health. Do not substitute illustrative output.
<!-- /review-todo -->

Weaver resolves the source bindings, then displays the source catalogue, destination catalogue and each logical-to-destination target mapping before it asks once for confirmation. Compare that settled plan with the source and destination names checked above, then confirm it if correct or decline it if not. Mirror has no dry-run mode, and declining leaves the destinations unchanged.

Mirror empties and reconstructs the displayed destination catalogue and targets from the source estate. Unchanged objects begin as borrowed source data. The destination catalogue records that state, while the project's logical items and Weaver documents remain unchanged.

Inspect the baseline:

```bash
weaver health --workspace-config workspace-development.yml
```

See [Mirrors](../core-concepts/mirrors.md) for borrowed and local data. Exact Mirror selection, authorisation and failure boundaries are in [Mirror operation behaviour](../reference/operation-behaviour/mirror.md).

## Change only the work that needs to become local

After a successful Mirror, keep the same project source and use its development configuration for Check, Build preview, Build, Load, Test and Health. The [development cycle](development-cycle.md#edit-and-iterate) is unchanged.

Build compares source with copied installed declarations. Unchanged borrowed objects stay borrowed. A changed selected object, or an affected selected descendant, becomes local after successful installation and loses its `_.Mirror` row. Items outside the Build selection do not materialise just because another item changed. Load operates local materialisations; borrowed data continues to be loaded and owned at its source.

Warehouse borrowed Tables/Views are presented through local Views. Lakehouse stored Tables/Folders use shortcuts, with local wrapper Views for source Views. Health reads borrowed current Load state from the source catalogue and local state from development. A mixed estate is an ordinary result, not evidence that every object has been copied.

Selected changed or impacted protected Tables/Folders use preserving materialisation rather than empty reconstruction: Warehouse CTAS, Delta shallow clone or native recursive Folder copy. That path retains the established bookmark but is not an atomic estate snapshot; shallow clones require source file retention. Protection does not protect against Wipe or deliberate re-mirroring. Keep irreplaceable source data outside ordinary managed target ownership. See [Protecting data](../advanced/protecting-data.md).

## Reset only when a new source baseline is intended

Run Mirror again only when the displayed destination catalogue and selected targets should be replaced. Local work inside that boundary is not preserved as a fallback. Preflight failures leave destinations unchanged; a failure after mutation begins does not restore the old catalogue or targets and does not undo already completed destinations. Inspect remaining state before retrying.

Selective mirroring still copies the destination catalogue, but only selected items are rebound to development targets; unselected copied installations remain source-bound. A catalogue-only Mirror copies installed/current state without emptying an item target, and destination Log/LoadStatistic history starts empty. It is not an isolated writable copy of every source binding. Rebinding from an already mirrored source is refused rather than chaining borrowing hops.

[Mirror and materialisation strategies](../advanced/mirror-and-materialisation-strategies.md) explains these narrower estate shapes. [Mirror behaviour](../reference/operation-behaviour/mirror.md) owns exact selection, binding and failure rules. Once the baseline is in place, return to [ordinary development](development-cycle.md), not another reset.
