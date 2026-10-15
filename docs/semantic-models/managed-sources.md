# Connect a managed Fabric source

The native model can participate in the same dependency graph as its source data. `Weaver.Source` identifies the managed Table; source Load then precedes model refresh, and Health can identify a model that is behind its source.

Continue with Parcel, Delivery and Depot, but change **Delivery’s partition from inline Import data to Warehouse-backed Import**. The complete [Fabric integration snapshot](../assets/examples/parcel-powerbi-fabric.zip) supplies that changed partition, a shared SQL expression, the Operations source and a reconciliation Test. Work from `examples/parcel-powerbi-fabric`; do not add `Weaver.Source` to the inline fixture and expect its data to switch. Depot remains inline reference data.

Use this source-backed project in a separate directory from the [inline model](native-tmdl.md). The logical model name remains Parcel. To keep the earlier visibility rule, merge it into this project’s same-name overlay without overwriting its source annotation.

## Before you start

Use the [complete Fabric integration project](../assets/examples/parcel-powerbi-fabric.zip) from its example directory. Configure an existing disposable Fabric workspace, compatible Weaver catalogue Warehouse and an empty Operations Warehouse. This SQL/Import route uses no Lakehouse or Spark runtime; Warehouse-only Build does not require a published Fabric Environment.

You need Warehouse create/alter/load and SELECT rights, catalogue read/write, model/Report deployment and refresh/view rights. Import refresh needs an existing supported service connection and credentials with Warehouse SQL access. Weaver does not create credentials. Only request binding to a connection you are permitted to use.

If you do not yet have a catalogue, the [first Fabric project](../warehouse/first-project.md) supplies the setup route. Do not point this exercise at an existing production estate.

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

`Weaver.Source` adds managed lineage. It does not replace this table's authored partitions/columns, load its source or grant access. The fixture already changes the native Delivery partition to read the shared expression:

```tmdl
/// Three parcel events, including two delivered parcels.
table Delivery
	measure 'Delivery Count' = SUM(Delivery[Delivered])
		formatString: 0
	measure InternalCost = 7
		formatString: 0.00
	column ParcelId
		dataType: int64
		sourceColumn: ParcelId
		summarizeBy: none
	column DepotId
		dataType: int64
		sourceColumn: DepotId
		summarizeBy: none
	column Delivered
		dataType: int64
		sourceColumn: Delivered
		summarizeBy: sum
	partition Delivery = m
		mode: import
		source =
			let
			    Source = #"Warehouse/Operations",
			    Data = Source{[Schema="Parcel", Item="Delivery"]}[Data]
			in
			    Data
```

The fixture’s `definition/expressions.tmdl` declares the supported expression that Build resolves:

```tmdl
expression 'Warehouse/Operations' = Sql.Database("replace-with-warehouse-sql-endpoint", "Parcel_Operations_Dev")
```

Both partitions remain Import; this task does not switch to Direct Lake or generate an empty table. [Author from TMDL](from-tmdl.md#3-generate-from-a-managed-source-only-when-needed) covers generation when no partition is authored.

## 2. Build and load the Warehouse first

```bash
weaver check .
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --workspace-config workspace-dev.yml
```

In Fabric, open a SQL query connected to `Parcel_Operations_Dev` (or your configured Operations Warehouse) and verify the source before deploying the model:

```sql
SELECT ParcelId, DepotId, Delivered
FROM Parcel.Delivery
ORDER BY ParcelId;

SELECT SUM(Delivered) AS DeliveryCount
FROM Parcel.Delivery;
```

The first query should return three rows with Delivered values 1, 1, 0; the second should return 2.

## 3. Bind and refresh the model

```bash
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Source-data definitions and model/Report definitions use separate Build calls against the same project and configuration. Do not combine their selections into one Build. `PowerBI/Parcel` also deploys the linked Report; [Report deployment](../reports/deploy.md) owns its binding checks. `--bind-data-sources` requests supported binding to an existing matching connection; it does not administer gateways or create credentials. Inspect the model's resolved shared expression and retained partition navigation, its refresh outcome and the Report's actual model binding. The Report card should show 2.

After source Load and model refresh, the Warehouse and model should contain the same three delivery rows, but a successful refresh does not establish that the measure is right. [Compare DAX with source SQL](validation.md#compare-dax-with-source-sql) in this same checkpoint: its existing Test independently sums Delivered in the Warehouse. Keep the loaded source and refreshed model; there is no second provisioning sequence.

[Run and inspect the estate](../estate/operate.md) brings source Load, model refresh, Test and Health together.

For cleanup, delete only this fixture’s newly created Report/model, then retire its disposable Operations Warehouse through a scoped approved procedure. Keep existing shared catalogues, workspaces and connections; do not use unscoped Wipe.
