# Deploy a native semantic model

Deploy native PBIP/TMDL, query a measure, then hide relationship foreign keys with one modelling rule. Weaver applies the rule to the deployed definition without editing the native files.

## Native files first

A PBIP project contains the model’s native TMDL and its Report definitions. You can also author a model directly in a named TMDL file; [native project layout](../reference/power-bi/project-layout.md) describes both forms.

## Before you start

[Install Weaver](../getting-started/installation.md). Use an existing disposable Fabric workspace where you can create or reuse the catalogue Warehouse and Environment, and create, read and refresh semantic models. The workspace licence and capacity must support Import models. Use existing permissions; this exercise does not require changing tenant settings.

Parcel has three inline sample rows, two depots, a relationship and a Delivery Count measure. Its model needs no Lakehouse or source Warehouse workload. If you already have a Parcel project, extend that same folder rather than starting again.

## 1. Choose the destination

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --semantic-model Parcel \
  --example Parcel
cd parcel
```

Initialise writes the native model and linked Report under `PowerBI/Parcel/`. It preserves existing source files and bindings when extending a project. Build creates the Power BI items; Initialise sets up the project’s catalogue and Environment. This inline model’s Build and refresh do not start Spark or require Environment publication.

Open `PowerBI/Parcel/Parcel.pbip` in Desktop to inspect the native project. Open `PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl` in your editor. The generated table includes the sample partition and measure:

<!-- initialise:PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl -->
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
			    Source = #table(type table [ParcelId = Int64.Type, DepotId = Int64.Type, Delivered = Int64.Type], {{1, 10, 1}, {2, 10, 1}, {3, 20, 0}})
			in
			    Source
```
<!-- /initialise -->

`workspace-config.yml` already binds `SemanticModel/Parcel` and `Report/Parcel` to their physical names. Keep any existing source bindings. [Environment mappings](../estate/environments.md) covers choosing other physical destinations without changing the source.

## 2. Check the project

```bash
weaver check
```

Check reads local declarations and definitions. It does not execute M/DAX, deploy items or test service permissions.

## 3. Deploy the native model

```bash
weaver build --item SemanticModel/Parcel
```

This selects **only the inline semantic model**, even if your project also has source-backed models. Find `Parcel` in your workspace. The Report stays local until you [deploy it](../reports/deploy.md).

## 4. Refresh and inspect the model

```bash
weaver load SemanticModel/Parcel
```

In the workspace, open the deployed **Parcel** semantic model and choose **Write DAX queries**. Run:

```dax
EVALUATE
ROW("DeliveryCount", [Delivery Count])
```

The result should be **DeliveryCount = 2**. [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view) needs model write permission and the workspace’s existing web modelling setting. If it is unavailable, connect Power BI Desktop to the published Parcel semantic model using a live connection and run the query in Desktop’s DAX query view with Read and Build permission. Do not query the local PBIP instead: you are checking the deployed model.

Create a Report connected to that deployed model and expand Delivery and Depot in its normal **Data** field list. Before applying the rule, both tables expose `DepotId`.

<span id="hide-relationship-foreign-keys"></span>

## AutoHideForeignKeys: hide relationship foreign keys

### Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model rather than declaring another one.

### Deploy and inspect

```bash
weaver check
weaver build --item SemanticModel/Parcel
weaver load SemanticModel/Parcel
```

Reopen the Report connected to the deployed model and check its normal field list with hidden fields excluded:

- `Delivery[DepotId]` is now hidden.
- `Depot[DepotId]` remains visible.
- Delivery Count still evaluates to 2.

The native files and inline data remain in place. Desktop does not execute Weaver annotations when opening the local PBIP; inspect the service-connected model for the change. Hidden fields are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild. Setting it to `false` is a no-op, not an instruction to undo an independently authored native hide.

<details markdown="1">
<summary>Inspect the native relationship</summary>

### Inspect the relationship the rule uses

Open `PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl`:

<!-- initialise:PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl -->
```tmdl
relationship Delivery_Depot
	fromColumn: Delivery.DepotId
	toColumn: Depot.DepotId
	fromCardinality: many
	toCardinality: one
	crossFilteringBehavior: oneDirection
```
<!-- /initialise -->

The rule hides the many-side key from the field list, not the one-side key.

</details>

## Carry the convention to the next model

When this convention belongs on several models, [share it in `PowerBI/policy.tmdl`](shared-policy.md). The next task keeps Parcel and its local overlay, adding common formatting and a calculation group.

[Validate the model](validation.md) to check its number, or [connect a managed Fabric source](managed-sources.md) by adding a source-backed model alongside this inline model. [Weaver documents](../core-concepts/weaver-documents.md#native-models-overlays-and-annotations) explains how overlays fit beside native definitions.
