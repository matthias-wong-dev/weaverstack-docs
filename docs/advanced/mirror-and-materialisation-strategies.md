# Mirror and materialisation strategies

Mirror can establish more than one kind of development estate. The important choice is where each logical item's installed binding points and whether each installed object still reads source-owned data or has become local.

## Choose the estate shape

A Mirror always rebuilds a destination catalogue from an installed source catalogue. Item selection then determines which copied installations are rebound to development targets.

| Strategy | Installation binding after Mirror | Data ownership |
| --- | --- | --- |
| Source-bound copied installation | The copied binding still names the source target. | Data and execution remain at the source target. |
| Borrowed development target | The logical item is rebound to a development target containing borrowed physical forms and local execution work. | Rows or files remain source-owned. |
| Local materialisation | A later Build replaces selected borrowed forms with authored local forms in the development target. | The materialised objects become development-owned and loadable there. |

Unselected logical items remain source-bound in the copied catalogue. Selected items use the destination bindings settled for the Mirror. This permits a catalogue to describe both kinds at once.

For a borrowed Warehouse item, source Tables and Views are exposed as local Views. For a borrowed Lakehouse item, stored Tables and Folders are exposed through OneLake shortcuts and source Views through local wrapper Views. Weaver installs the execution work needed in the development target, but borrowed data is not loadable there. `_.Mirror` records the source address and borrowed physical form for each object that remains borrowed.

## Start with a catalogue-only branch

A catalogue-only Mirror rebuilds the destination catalogue without emptying or rebinding an item target. Installed and current state is copied, while operational log and load-statistic history starts empty. The copied item bindings therefore continue to name source targets.

This is useful when only one part of an estate will be developed locally. Fork the catalogue first, then Build the chosen item against its configured development target. Other items retain their copied source bindings.

A catalogue-only branch can carry existing `_.Mirror` state because it does not add another borrowing hop. Rebinding items from an already mirrored source is refused: borrowed state records one source hop, not a chain of mirrors.

## Mirror only the items that need development targets

Selective mirroring rebinds named logical items and leaves every unselected installation source-bound. It avoids creating development copies for items that will not change.

All selected destination bindings are settled before Weaver changes anything. Logical Shortcuts are recreated against those final bindings, and selected producer items are processed before selected consumers where recorded Shortcuts require it. A selected destination cannot overlap a source read by the same run or another selected destination.

Source and destination catalogues must be distinct Warehouses in the same resolved Fabric workspace. Mirror does not provide a cross-workspace catalogue copy mechanism. The [Mirror operation reference](../reference/operation-behaviour/mirror.md) defines item selection, binding checks and destructive scope.

## Let Build create a mixed estate

Build compares project source, copied certification and destination inventory. An unchanged borrowed object keeps its borrowed form and its `_.Mirror` row. When a selected borrowed object changed, or is an affected selected descendant, Build replaces the borrowed form with the authored local form and removes that object's mirror record after the physical work succeeds.

Materialisation is therefore object-selective, not an automatic conversion of the whole mirrored estate:

```text
unchanged object             → borrowed source data
changed selected object      → local development data
affected selected descendant → local development data
unselected item              → copied source binding
```

The result is a mixed estate. Load can run local materialised objects; borrowed objects continue to take their Load state from the catalogue where their data is owned. Health uses the installation and mirror records to inspect the corresponding state.

## Treat re-mirroring as a reset

A later Mirror does not refresh borrowed objects in place around local work. It empties and reconstructs the destination catalogue and every selected destination target in the settled plan. Local materialisations inside that boundary are replaced by a fresh branch from the source estate.

Use re-mirroring when the desired result is a new source baseline, not as an iteration step. Review the complete destination boundary first. Preflight failures leave destinations unchanged, but a failure after execution begins does not restore the previous catalogue or targets and does not undo destinations already completed.

The ordinary edit, Build, Load, Test and Health loop belongs in [The development cycle](../basics/development-cycle.md). Exact Mirror planning, confirmation and recovery behaviour is in the [Mirror operation reference](../reference/operation-behaviour/mirror.md).
