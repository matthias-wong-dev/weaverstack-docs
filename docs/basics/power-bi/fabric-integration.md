# Connect a semantic model to source data

Connect a native model to a managed Warehouse Table. The source and model share a dependency graph: Load can refresh them in order, Test can compare their numbers, and one Health report covers the estate.

## Before you start

Use the [complete Fabric integration project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-fabric) from its example directory. Configure an existing disposable Fabric workspace, compatible Weaver catalogue Warehouse and an empty Operations Warehouse. This SQL/Import route uses no Lakehouse or Spark runtime; Warehouse-only Build does not require a published Fabric Environment.

You need Warehouse create/alter/load and SELECT rights, catalogue read/write, model/Report deployment, refresh/view rights and DAX query Read/Build access with the tenant setting permitting your identity. Import refresh needs an existing supported service connection and credentials with Warehouse SQL access. Weaver does not create credentials. Only request binding to a connection you are permitted to use.

If you do not yet have a catalogue, the [first Fabric project](../../getting-started/first-project.md) supplies the setup route. Do not point this exercise at an existing production estate.

## 1. Configure destination and source separately

`workspace-dev.yml`:

```yaml
workspace: Parcel Fabric Development
catalogue: Warehouse/Parcel_Catalogue_Dev
targets:
  Warehouse/Operations: Parcel_Operations_Dev
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
data_sources:
  Warehouse/Operations: Warehouse/Parcel_Operations_Dev
```

`targets` maps logical items to physical names. `data_sources` maps a supported shared M expression to the physical Warehouse. The native `definition/expressions.tmdl` contains that shared expression; its authored partition still navigates `[Parcel].[Delivery]`. This mapping resolves the selected Warehouse endpoint, not arbitrary M text or an external database.

The existing Delivery table is refined by `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
table Delivery
	annotation 'Weaver.Source' = Warehouse/Operations/Parcel.Delivery
```

`Weaver.Source` adds managed lineage. It does not replace this table's authored partitions/columns, load its source or grant access.

## 2. Build and load the Warehouse first

```bash
weaver check .
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --workspace-config workspace-dev.yml
```

The source table contains three rows with Delivered values 1, 1, 0. Confirm it is loaded before deploying/refreshing the model.

## 3. Deploy the model and Report

```bash
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Source-data definitions and model/Report definitions use separate Build calls against the same project and configuration. `--bind-data-sources` requests supported binding to an existing matching connection; it does not administer gateways or create credentials. Inspect the model's resolved shared expression and retained partition navigation, its refresh outcome and the Report's actual model binding. The Report card should show 2.

## 4. Compare DAX with SQL

The supplied model-owned Test evaluates Delivery Count and compares it with the Warehouse's sum of Delivered. Both should return 2:

```bash
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
weaver health --workspace-config workspace-dev.yml
```

Inspect Delivery's metadata row under logical `SemanticModel/Parcel` in `_.SemanticModelTable`, and its `_.Dependency` row whose authored `Dependency reference` is `Warehouse/Operations/Parcel.Delivery`. Source mode/access belongs in the table metadata; source identity belongs in Dependency. A null `Source access` is valid for this retained authored partition and does not mean its mapping failed.

The Test result and the model’s refresh state appear beside Warehouse state in the same catalogue. Inspect the installed validation in `_.SemanticModelTest` and its result in `_.TestStatus`. With no item selector, Health covers the managed estate.

## 5. Run the estate together

Once both items are installed, use the ordinary estate-wide commands:

```bash
weaver load --workspace-config workspace-dev.yml
weaver test --workspace-config workspace-dev.yml
weaver health --workspace-config workspace-dev.yml
```

Load selects the installed source and model, placing source work before the model refresh. Test runs the installed Warehouse and model validations. Health shows whether their data and validation results are current. The source-only project’s operating flow now covers the model too.

## 6. Show and correct a discrepancy

The fixture's failing overlay makes the model measure one greater than the source calculation:

```bash
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

Expect a failed finding, actual 3 versus expected 2, then a pass after correction. Restore the original overlay even if a command fails. Access/query errors are `invalid` validation nodes, not discrepancies; installed TestStatus records them as `Error`. Failed/invalid CLI Tests exit 1.

For cleanup, delete only fixture-created Reports/models, then retire its Operations Warehouse through a scoped approved procedure. Keep the shared catalogue, workspace and connections. Do not use unscoped Wipe.

## Related tasks

- [Look up source mapping and credential boundaries](../../reference/power-bi/requirements-and-compatibility.md#source-mapping-and-connections).
- [Look up validation comparison rules](../../reference/power-bi/validations.md).
- [Optionally generate a model from managed metadata](../../advanced/power-bi/model-from-tmdl.md).
