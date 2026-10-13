# Author a model from TMDL

A standalone named TMDL file can supply a model without a native `.SemanticModel` directory. Choose this when you want to author the definition directly; existing PBIP projects do not need to convert.

## 1. Write one complete model

Create a new project with `PowerBI/Parcel/ParcelSummary.tmdl`:

```tmdl
model Model
    culture: en-US
    defaultMode: import

table Delivery
    measure 'Delivery Count' = SUM(Delivery[Delivered])
        formatString: 0
    column Delivered
        dataType: int64
        sourceColumn: Delivered
        summarizeBy: sum
    partition Delivery = m
        mode: import
        source =
            let
                Source = #table(type table [Delivered = Int64.Type], {{1}, {1}, {0}})
            in
                Source
```

The filename declares `SemanticModel/ParcelSummary`. There is no Report in this example. If a same-name native `ParcelSummary.SemanticModel` exists, this file instead overlays it; do not mistake that for two independent definitions.

Create `workspace-dev.yml`, using your existing disposable Power BI workspace:

```yaml
workspace: Parcel BI Development
targets:
  SemanticModel/ParcelSummary: Parcel_Summary_Dev
```

Use the [ordinary service licensing and permissions](../../basics/power-bi/deploy-pbip.md). The inline Import partition needs no managed source, catalogue or Fabric Environment.

## 2. Deploy and refresh

```bash
weaver check .
weaver build . --item SemanticModel/ParcelSummary --workspace-config workspace-dev.yml
weaver load SemanticModel/ParcelSummary --workspace-config workspace-dev.yml
```

Inspect `Parcel_Summary_Dev` through a supported native model-definition tool. Its Delivery partition contains three rows, and Delivery Count evaluates to 2 after refresh. Check validates local shape, not M evaluation or service eligibility. Delete only the new model for cleanup.

## 3. Generate from a managed source only when needed

A table without an authored partition can obtain its columns and partition from managed-source metadata. This is a different route with additional prerequisites: a compatible catalogue, built/loaded supported Lakehouse or Warehouse source, resolved endpoints/metadata, and permissions and connections for the model's chosen mode.

Begin with the [Fabric integration fixture](../../basics/power-bi/fabric-integration.md) in its own directory. Build and Load its Warehouse first. Then create `PowerBI/Parcel/ParcelSummary.tmdl`:

```tmdl
model Model
    defaultMode: import

table Delivery
    annotation 'Weaver.Source' = Warehouse/Operations/Parcel.Delivery
    measure 'Delivery Count' = SUM(Delivery[Delivered])
        formatString: 0
```

Add `SemanticModel/ParcelSummary: Parcel_Summary_Dev` under that fixture's `targets`, then select only this new model:

```bash
weaver check .
weaver build . --item SemanticModel/ParcelSummary --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/ParcelSummary --workspace-config workspace-dev.yml
```

Inspect the generated native Delivery columns/Import partition and resolved source expression. Delivery Count should be 2 after source Load and model refresh. Weaver uses an existing supported connection, not newly created credentials.

With `defaultMode: import`, generation supplies an M navigation partition. Otherwise this generation path supplies Direct Lake entity partitions, which retain their source, service and capacity prerequisites. Source housekeeping audit/signature columns are omitted unless explicitly authored. Native descriptions win over source metadata; unsupported source types fail.

A table **with** an authored partition retains that partition and its authored column types. Adding `Weaver.Source` to it is lineage/refinement, not permission to overwrite its query or generate all columns. Use the ordinary integration task for that case.

Build deploys the native definition while leaving the authored TMDL in the project unchanged.

## Related tasks

- [Look up source generation and annotation boundaries](../../reference/power-bi/annotations.md#weaversource).
- [Reuse models through composition](model-composition.md).
- [Look up native layout](../../reference/power-bi/project-layout.md).
