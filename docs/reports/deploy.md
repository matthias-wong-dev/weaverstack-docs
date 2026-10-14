# Deploy a native Report

Keep your native `.Report` beside its semantic model. Build deploys the model first, then binds the Report to that deployed model without rewriting the local `definition.pbir`.

## Start with the linked pair

[Install Weaver](../getting-started/installation.md), then work from the [complete parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/main/examples/parcel-powerbi), in `examples/parcel-powerbi`. It contains the native model and a Report with a Delivery Count card. You do not need to author the model again or complete the semantic-model tutorial first.

If you already deployed this pair in [Deploy a native model](../semantic-models/native-tmdl.md), keep that project, including any overlay you added. This task uses the same Report and model.

Open `PowerBI/Parcel/Parcel.pbip` in Desktop to inspect the Report. Its association is authored in `PowerBI/Parcel/Parcel.Report/definition.pbir`:

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

The path is relative to the `.Report` directory. Keep the complete native Report payload as well as this file; the fixture already includes its page and card definitions. [Native project layout](../reference/power-bi/project-layout.md#report-discovery-and-association) describes discovery for your own project.

This inline Import example also works in an existing standalone Power BI service workspace. It needs no Weaver catalogue, Lakehouse, Warehouse or Fabric Environment. Do not use `weaver initialise` for that setup: it provisions a catalogue and Environment.

## Choose the destination and Build

Edit `workspace-dev.yml` to name an existing disposable workspace:

```yaml
workspace: Parcel BI Development
targets:
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
```

Build can create missing selected models and Reports or update existing ones. Choose item names you own. Sign in with an identity allowed to create/update and read back both items; the service licence and capacity must support the model mode. [Service requirements](../reference/power-bi/requirements-and-compatibility.md#runtime-and-service-access) give the platform boundaries.

Run from the example directory:

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
```

Check validates local definitions, not service access. `PowerBI/Parcel` selects the local model and Report together. Build deploys and verifies `Parcel_Dev` before deploying `Parcel_Report_Dev`, then verifies the Report definition and its actual model binding. The deployed payload uses the resolved service workspace/model IDs; your authored `byPath` and native files stay unchanged.

Without a catalogue, a linked Report must include its local model in the same Build. In a catalogue-backed project, a Report-only Build can use an already certified installed model whose recorded binding matches the resolved destination and source requirements. See [Report binding](../reference/power-bi/requirements-and-compatibility.md#report-binding) before selecting only `Report/Parcel`.

## Inspect the Report

In the service workspace, find `Parcel_Report_Dev` and check that its linked model is `Parcel_Dev` in **Parcel BI Development**. Use the service's lineage view or Report binding readback; when using API readback, compare `datasetId` and `datasetWorkspaceId` with the deployed model and workspace IDs.

To view the fixture's card after loading its inline data, refresh the **model** with an identity allowed to refresh it:

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

With permission to view the Report and query its model, open the card: **Delivery Count should be 2**. This is a separate viewing check, not a Report deployment requirement. Reports have no separate Load, Test or refresh operation; data refresh and validation belong to the model. Build success alone does not establish refresh access or card rendering.

The development Report now has a destination-specific model binding while the source still names `../Parcel.SemanticModel`. [Use the same Report in development and production](environments.md) by selecting a second configuration, not editing that path.
