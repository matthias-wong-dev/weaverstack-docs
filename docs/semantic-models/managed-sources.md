# Connect a managed Fabric source

Keep Parcel’s inline Delivery/Depot model and add a model over the working Warehouse. The original Delivery Count still works without a source connection; the new model demonstrates source-to-model coordination.

## Before you start

Continue the [native Parcel project](native-tmdl.md). Use its same workspace, catalogue, configuration and overlays. You need Warehouse create/alter/load and SELECT rights, catalogue access, and model deployment, refresh and query permissions. Source-backed Import refresh also needs an existing supported service connection with SQL access. Weaver can bind a matching connection; it does not create credentials or administer gateways.

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

Initialise adds the independent [Warehouse Table and View](../warehouse/first-project.md), their validations, and a **separate** `ParcelWarehouse` model. It retains `Parcel.SemanticModel`, the Report and any same-name Parcel overlay. It also adds the new target bindings to `workspace-config.yml` without changing existing physical names.

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
