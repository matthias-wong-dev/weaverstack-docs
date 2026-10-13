# Connect an authored model to a managed Warehouse

**Weaver source target:** `74b4d15ee65ed2740593af1f4d459771b801b132`. Use a Weaver build containing these interfaces. The older PyPI `0.9.0` package is not the acceptance target.

## Resources and rights

Run from this directory. Use an existing disposable Fabric workspace on capacity that supports a Warehouse, a compatible Weaver catalogue Warehouse, and an empty Operations Warehouse named by `workspace-dev.yml`. Edit both configuration files to your own disposable workspace/catalogue names. Do not use a real production workspace for the production-labelled configuration.

You need source Warehouse create/alter/load and SELECT rights, catalogue read/write rights, Power BI model/Report creation or update rights, model refresh and Report view rights, and DAX query Read/Build permissions. The tenant Execute Queries setting must permit the validation identity. Import refresh needs a supported existing service source connection and credentials with Warehouse SQL access. Weaver does not create credentials. If binding through `--bind-data-sources`, the caller must be allowed to use that existing connection. Do not enable tenant settings or bind someone else's connection merely to run this example.

This is a catalogue-backed SQL/Import route. No Lakehouse or Spark runtime is used. A SQL-only source Build does not itself require a published Fabric Environment. Do not infer that other Fabric workloads have the same prerequisites.

## Keep the ordinary model, add lineage

`Parcel.SemanticModel` is an already-authored native model with Delivery/Depot columns, a relationship and Import partitions. Delivery's native M partition navigates `Warehouse/Operations` to `[Parcel].[Delivery]`; Depot still uses inline reference data. `Parcel.tmdl` adds `Weaver.Source = Warehouse/Operations/Parcel.Delivery` to the existing Delivery table. This is not empty-table generation and does not replace its authored partition or columns.

The shared M expression in `definition/expressions.tmdl` contains a neutral placeholder endpoint. `data_sources` maps that **supported shared expression** to the configured Operations Warehouse, so Build resolves its real SQL endpoint. This is not arbitrary M substitution or a grant of source credentials. The model/Report target names are a separate mapping.

## Build the source before Power BI

```bash
weaver check .
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
weaver health --item Warehouse/Operations --item SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Do not combine the source and Power BI Build selections in one call. After source Load, `Parcel.Delivery` has three rows with Delivered values 1, 1, 0. After model refresh, the Report card displays 2. Verify the deployed shared expression uses the selected Warehouse SQL endpoint, the authored partition navigation survives, and the Report binds to the configured model.

Inspect Delivery's metadata row under logical `SemanticModel/Parcel` in `_.SemanticModelTable`, and its `_.Dependency` row whose authored `Dependency reference` is `Warehouse/Operations/Parcel.Delivery`. Source mode/access belongs in the table metadata; source identity belongs in Dependency. A null `Source access` is valid for this retained authored partition and does not mean its mapping failed.

Inspect the installed model validation in `_.SemanticModelTest` and its result in `_.TestStatus`. Health describes the recorded managed estate, not every arbitrary workspace item. Expect the DAX/SQL Test to pass and the installed result to be recorded. Inspect refresh and validation results, not only Build's exit status.

## Compare independent calculations

`PowerBI/Parcel/tests/Parcel/Parcel.DeliveryReconciles.dax` runs `ROW("DeliveryCount", [Delivery Count])` against the model. Its expected SQL sums Delivered in the supported Warehouse source. Both should return 2. `expected-results.json` records the matching and deliberately different rows.

## Deliberate discrepancy and correction

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

The failing overlay adds 1 to the model measure: actual 3 versus SQL expected 2. Expect a `failed` finding with expected/actual diagnostic rows, then `passed` after correction. This changes a measure, not the Warehouse data. The CLI exits 1 for a failed or invalid validation, and 0 for a passing run. A DAX/SQL access or query error produces an `invalid` validation node, not a discrepancy or a pass; catalogue TestStatus records execution errors as `Error`. The live gate includes both the stored TestStatus and native model/Report readback.

## Cleanup

Delete only the fixture-created Report and model, then retire this fixture's Operations Warehouse through a scoped, approved catalogue procedure. If the Warehouse was created empty solely for this example, verify it contains no other work before deleting it. Retain the shared catalogue, connections and workspace. Do not use an unscoped Wipe or delete credentials.
