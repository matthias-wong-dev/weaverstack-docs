# Validate a semantic model

A successful refresh says the model ran, not that its measure is right. Add an Assumption to the working Parcel model, then reconcile its DAX result with independent SQL when Delivery has a managed Warehouse source.

## Start from the model you already deployed

For the Assumption, continue the [native model checkpoint](native-tmdl.md): Parcel has inline Import data, Delivery Count evaluates to 2, and its same-name overlay hides the relationship foreign key. Keep that overlay and your existing workspace configuration. You add one DAX file, not another project or deployment setup.

For direct entry, the complete [validation snapshot](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-validation) contains the same native Delivery/Depot model and the Assumption below. Configure and deploy it once using the [native task](native-tmdl.md#before-you-start), then return here. That snapshot has no initial overlay; the failure and correction below handle both start states.

DAX queries need model Read and Build permissions and an identity permitted by the tenant’s Execute Queries setting. Reconciliation also needs SELECT access to the Warehouse source. Use existing permissions; do not change tenant settings for this exercise.

## 1. Add the DAX Assumption

Create `PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax`:

```dax
/*
Assumption ID: Parcel.PositiveDeliveryCount
Description: The delivery count is positive.
*/
EVALUATE FILTER(ROW("DeliveryCount", [Delivery Count]), [DeliveryCount] <= 0)
```

The filename, metadata ID and `assumptions` directory agree. `Parcel` in the directory is the local logical model name, not the physical `Parcel_Dev`. An Assumption returns violating rows; zero rows passes. [DAX validation reference](../reference/power-bi/validations.md) owns the complete metadata rules.

## 2. Run the authored query

```bash
weaver check .
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax' --workspace-config workspace-dev.yml
```

Expect a `passed` validation node with zero violations and CLI exit 0. You do not need Build merely to edit a source query: this run evaluates the new file against the already deployed model.

`--file` explicitly selects source/file mode even when the configuration contains a catalogue. `--source .` identifies the project; it does not force file mode by itself. In the supplied catalogue-free snapshot, `--source .` alone uses source mode. Source/file mode records no installed `_.TestStatus` or Test history. Repeat `--file` for paths/directories/globs and `--name` for case-insensitive whole-validation regex seeds; each supplied name pattern must match.

To install this Assumption in a catalogue-backed project, Build the changed model declarations, then run Test without `--file`. Installed mode reads the catalogue’s validation definition and records results. Do not assume an edited local DAX file changed that installed definition.

## 3. Produce a finding without losing your overlay

Create `failure/Parcel.tmdl` with the supplied validation snapshot’s complete failure declaration:

```tmdl
table Delivery
	measure 'Delivery Count' = -1
```

Back up the existing same-name overlay first; it may contain the foreign-key rule, policy overrides or your own conventions. Use an unused `Parcel.tmdl.saved` filename and keep the same shell for correction:

```bash
test ! -e Parcel.tmdl.saved || exit 1
had_overlay=false
if test -f PowerBI/Parcel/Parcel.tmdl; then
  had_overlay=true
  cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
fi
```

Edit `PowerBI/Parcel/Parcel.tmdl` to set Delivery Count to `-1`, using the failure declaration above. Keep every other declaration in the overlay. If `table Delivery` or its measure already exists, edit that declaration rather than pasting a second one: duplicate declarations are refused. In the native rule-only checkpoint, add the Delivery section beneath the existing `model Model` annotation. In the direct-entry snapshot with no overlay, create the file with the complete failure declaration.

Deploy that changed measure and run the same source Assumption:

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax' --workspace-config workspace-dev.yml
```

Expect `failed` with one violating row, `DeliveryCount = -1`, and CLI exit 1. This is a finding, not a query failure. A permission or execution failure produces an `invalid` node and also exits 1. Python returns the validation report: inspect `succeeded`, node `status` and diagnostics rather than using a retired `strict=` argument.

## 4. Restore the prior model and rerun

Run the restoration even if Check, Build, Load or Test failed. A deliberate failed Test exits 1, so do not put restoration behind `&&` or a shell’s automatic exit-on-error:

```bash
if test "$had_overlay" = true; then
  mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
else
  rm PowerBI/Parcel/Parcel.tmdl
fi
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax' --workspace-config workspace-dev.yml
```

Expect `passed` again. The existing overlay is restored byte for byte, including its foreign-key convention. Only the direct-entry case that had no overlay removes the file created by this exercise. If the shell was interrupted, restore `Parcel.tmdl.saved` manually before deploying again.

## Compare DAX with source SQL

Continue the already loaded and refreshed [managed-source checkpoint](managed-sources.md), in `examples/parcel-powerbi-fabric`. It retains Parcel, Delivery and Depot but changes Delivery from inline data to Warehouse-backed Import. Do not provision it again to run this Test. If you came here from the inline Assumption route, complete that source change once; the inline fixture cannot supply an independent Warehouse calculation.

The managed snapshot already owns `PowerBI/Parcel/tests/Parcel/Parcel.DeliveryReconciles.dax`:

```dax
/*
Test ID: Parcel.DeliveryReconciles
Description: Model deliveries agree with the managed Warehouse table.
Expected source: Warehouse/Operations
Expected SQL: |
  SELECT SUM(Delivered) AS DeliveryCount FROM [Parcel].[Delivery]
*/
EVALUATE ROW("DeliveryCount", [Delivery Count])
```

The Test compares model DAX with the Warehouse’s independent sum of Delivered. Both should return 2:

```bash
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
weaver health --workspace-config workspace-dev.yml
```

This is installed mode: the managed-source Build installed the Test. Inspect Delivery's metadata row under logical `SemanticModel/Parcel` in `_.SemanticModelTable`, and its `_.Dependency` row whose authored `Dependency reference` is `Warehouse/Operations/Parcel.Delivery`. Source mode/access belongs in the table metadata; source identity belongs in Dependency. A null `Source access` is valid for this retained authored partition and does not mean its mapping failed.

Inspect the installed validation in `_.SemanticModelTest` and its result in `_.TestStatus`. Model refresh and Test results sit beside Warehouse state in the same catalogue. With no item selector, Health covers the managed estate, not every arbitrary item in the workspace.

### Produce and correct a discrepancy

The supplied managed snapshot’s `failure/Parcel.tmdl` preserves its source annotation and changes the measure:

```tmdl
table Delivery
	annotation 'Weaver.Source' = Warehouse/Operations/Parcel.Delivery
	measure 'Delivery Count' = SUM(Delivery[Delivered]) + 1
```

Back up the normal overlay to an unused filename, and restore it even if a command fails:

```bash
test ! -e Parcel.tmdl.saved || exit 1
cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
```

Expect a failed finding, actual 3 versus SQL expected 2, then a pass after correction. This changes the measure, not Warehouse data. Access/query errors are `invalid` validation nodes, not discrepancies; installed `_.TestStatus` records execution errors as `Error`. Failed/invalid CLI Tests exit 1. `--bind-data-sources` uses a supported existing connection; it does not create credentials or grant source access.

## Read the estate result

In a catalogue-backed project, `weaver test` without item selectors runs installed Lakehouse, Warehouse and model validations. [Run and inspect the estate](../estate/operate.md) combines those outcomes with source loads and model refreshes. Exact diagnostics and recording boundaries belong in [Test behaviour](../reference/operation-behaviour/test.md).

For cleanup, delete only example-created Reports/models, Reports first. Retire the managed fixture’s Operations Warehouse only through a scoped approved procedure; retain shared catalogues, workspaces and connections. Do not use unscoped Wipe.
