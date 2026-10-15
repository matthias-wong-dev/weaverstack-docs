# Deploy a native Report

Keep your native `.Report` beside its semantic model. Build deploys the model first, then binds the Report to that deployed model without rewriting the local `definition.pbir`.

## Start with the linked pair

Continue the [native Parcel model](../semantic-models/native-tmdl.md) in the same project, keeping its overlays. Initialise has already written its linked Report. If you are starting here, [install Weaver](../getting-started/installation.md) and generate the pair:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --semantic-model Parcel \
  --example Parcel
cd parcel
```

Open `PowerBI/Parcel/Parcel.pbip` in Desktop to inspect the Report. Its association is authored in `PowerBI/Parcel/Parcel.Report/definition.pbir`:

<!-- initialise:PowerBI/Parcel/Parcel.Report/definition.pbir -->
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../Parcel.SemanticModel"
    }
  }
}
```
<!-- /initialise -->

The path is relative to the `.Report` directory. Keep the complete native Report payload as well as this file; the example includes its page and card definitions. [Native project layout](../reference/power-bi/project-layout.md#report-discovery-and-association) describes discovery for your own project.

The inline model needs no source Lakehouse or Warehouse workload. Initialise sets up the project catalogue and Environment; this Report/model Build does not need Spark. The [standalone Power BI setup](../reference/power-bi/requirements-and-compatibility.md) also supports an existing workspace without a catalogue.

## Choose the destination and Build

Use the generated `workspace-config.yml`. It already binds `SemanticModel/Parcel` and `Report/Parcel` to their physical items in Parcel Development. Keep any Lakehouse or Warehouse bindings in that file.

Build can create missing selected models and Reports or update existing ones. Choose item names you own. Sign in with an identity allowed to create/update and read back both items; the service licence and capacity must support the model mode. [Service requirements](../reference/power-bi/requirements-and-compatibility.md#runtime-and-service-access) give the platform boundaries.

Run from the example directory:

```bash
weaver check .
weaver build . --item SemanticModel/Parcel --item Report/Parcel
```

Check validates local definitions, not service access. These two selectors deploy the inline model and its linked Report without selecting any additional source-backed models. Build deploys and verifies `Parcel` before deploying the Parcel Report, then verifies the Report definition and its actual model binding. The deployed payload uses the resolved service workspace/model IDs; your authored `byPath` and native files stay unchanged.

Without a catalogue, a linked Report must include its local model in the same Build. In a catalogue-backed project, a Report-only Build can use an already certified installed model whose recorded binding matches the resolved destination and source requirements. See [Report binding](../reference/power-bi/requirements-and-compatibility.md#report-binding) before selecting only `Report/Parcel`.

## Inspect the Report

In the service workspace, find the Parcel Report and check that its linked model is `Parcel` in **Parcel Development**. Open the workspace’s **lineage view** and follow the Report’s model link. Confirm it points to the Parcel semantic model in this workspace, not a similarly named model in another destination.

To view the generated Report’s card after loading its inline data, refresh the **model** with an identity allowed to refresh it:

```bash
weaver load SemanticModel/Parcel
```

With permission to view the Report and query its model, open the card: **Delivery Count should be 2**. This is a separate viewing check, not a Report deployment requirement. Reports have no separate Load, Test or refresh operation; data refresh and validation belong to the model. Build success alone does not establish refresh access or card rendering.

The development Report now has a destination-specific model binding while the source still names `../Parcel.SemanticModel`. [Use the same Report in development and production](environments.md) by selecting a second configuration, not editing that path.
