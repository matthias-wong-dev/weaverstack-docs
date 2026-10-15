# Connect a managed Fabric source

Extend the existing Parcel project from [Power BI-only operation into a Catalogue-managed Fabric estate](index.md#two-ways-to-use-weaver-with-power-bi). Keep its inline Delivery/Depot model and linked Report, then add a Warehouse and a separate model over its data. The original Delivery Count still works without a source connection.

## Before you start

Continue the [native Parcel project](native-tmdl.md) in the same workspace, retaining its configuration and overlays. That starting path has no Catalogue; adding the Warehouse below introduces one. The workspace now needs Fabric capacity that supports Warehouse work, Warehouse create/alter/load and SELECT rights, Catalogue access, and model deployment, refresh and query permissions. Source-backed Import refresh also needs an existing supported service connection with SQL access. Weaver can bind a matching connection; adding a Catalogue does not create credentials or administer gateways.

## 1. Configure destination and source separately

From the directory containing `parcel`, extend the project:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --warehouse Operations \
  --example Parcel
cd parcel
```

If your shell is already in the project, use `--project-folder .` and stay there. Omitted existing items are retained. If Operations is already present, this is an idempotent rerun, not a request to replace it.

Initialise adds the Operations Warehouse with its independent [Table and View](../warehouse/first-project.md), their validations, and a **separate** `ParcelWarehouse` model. It introduces the required Catalogue and Environment support for the data project. It retains `Parcel.SemanticModel`, the Report and previously authored files, including any same-name Parcel overlay. New target bindings are added to `workspace-config.yml` without changing existing physical bindings. This extends the same installation; it does not replace the inline Delivery partition or change the original model’s meaning.

Open `PowerBI/Parcel/ParcelWarehouse.tmdl`:

<!-- initialise:PowerBI/Parcel/ParcelWarehouse.tmdl -->
```tmdl
model Model
	culture: en-US
	defaultMode: import
	annotation 'Weaver.BaseSemanticModels' = Parcel

table CurrentStatus
	annotation 'Weaver.Source' = Warehouse/Operations/Parcel.CurrentStatus
```
<!-- /initialise -->

The additional model composes the native Parcel foundation, so existing modelling policy still has its original Delivery/Depot tables to refine. `Weaver.Source` asks Build to generate this model’s CurrentStatus table from the managed Warehouse View. Its Import partition and columns are generated from the resolved source metadata. This is an additional model: it does not substitute a Warehouse partition into the native Delivery table. [Author from TMDL](from-tmdl.md#3-generate-from-a-managed-source-only-when-needed) explains source generation in detail.

The project’s `targets` choose physical items. Optional `data_sources` mappings can independently choose which supported physical source a logical expression reads; see [workspace mappings](../estate/environments.md). Neither setting grants SQL access or creates a service connection.

## 2. Build and load the Warehouse first

```bash
weaver check
weaver build --item Warehouse/Operations
weaver load Warehouse/Operations
```

In a SQL query connected to Operations, inspect the source:

```sql
SELECT [Parcel ID], [Status], [Depot]
FROM Parcel.CurrentStatus
ORDER BY [Parcel ID];
```

Expect P-1001 / In transit / Central and P-1002 / Delivered / South. The Warehouse’s StatusEvent Table and CurrentStatus View remain the same independent pipeline introduced in the Warehouse journey.

## 3. Bind and refresh the model

```bash
weaver build --item SemanticModel/ParcelWarehouse --bind-data-sources
weaver load Warehouse/Operations SemanticModel/ParcelWarehouse
```

Build the source and model in separate requests. `--bind-data-sources` uses an existing matching supported connection. Resolve missing or ambiguous connections with the connection’s owner; do not change tenant settings to make the example run.

The selected Warehouse work now precedes the additional model’s refresh. In the service, open **ParcelWarehouse**, choose Write DAX queries (or use the [Desktop live-connection route](native-tmdl.md#4-refresh-and-inspect-the-model)), and run:

```dax
EVALUATE
CurrentStatus
```

The model should expose the same two current-status rows. The original **Parcel** model still returns Delivery Count = 2 and its Report still uses that model. Opening Parcel rather than ParcelWarehouse would query the independent inline sample, not this managed source.

Adding a Lakehouse works the same way: Initialise retains both pipelines and adds `ParcelLakehouse` over Landing’s CurrentStatus Table. With Lakehouse and Warehouse selected, separately named Warehouse integration objects also connect the Lakehouse Event Table without replacing StatusEvent or changing the original View. [Connect items and dependencies](../estate/connected-items.md) follows that path.

[Compare DAX with source SQL](validation.md#compare-dax-with-source-sql) to validate this source-backed model in the same project. [Run and inspect the estate](../estate/operate.md) combines source Load, model refresh, Test and Health.
