# Deploy an existing PBIP

Deploy a native semantic model and its linked Report, then refresh the model and open the Report. Keep authoring in Power BI Desktop and TMDL; Weaver supplies the deployment configuration.

## Before you start

[Install the documented snapshot](../../getting-started/installation.md). Use an existing Power BI service workspace and an identity with model/Report create or update rights, refresh rights and permission to view the Report. The service licence and model mode must support those operations. Free Desktop alone is not a deployment environment.

This route needs no Weaver catalogue, Lakehouse, Spark session or Fabric Environment. The example uses inline Import data, so it also needs no external source connection. Your own project's partitions may have separate credential requirements.

Download or clone the [complete parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi) and work from `examples/parcel-powerbi`. `PowerBI/Parcel/Parcel.pbip` opens the native project. Its model has three parcel rows, two depots, a relationship and a Delivery Count measure. Its Report has a Delivery Count card.

## 1. Choose the destination

Edit `workspace-dev.yml` to name your existing disposable workspace:

```yaml
workspace: Parcel BI Development
targets:
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
```

Logical names stay in the project; this file chooses physical names. Build may create missing selected models and Reports, or update existing ones. Choose names you own. Do not run `weaver initialise` for this route: it also provisions a catalogue Warehouse and Fabric Environment.

## 2. Check the project

```bash
weaver check .
```

Check reads local declarations and definitions. It does not execute M/DAX, deploy items or test service permissions. In your own project, use the supported `PowerBI/<project>/` layout with native `.SemanticModel` and `.Report` definitions. A PBIP entrypoint is optional for discovery.

## 3. Deploy the model and linked Report

```bash
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
```

The project selector includes both items. Weaver deploys and verifies the model before its linked Report, resolving the Report to `Parcel_Dev`. It changes the deployment payload, not your authored `definition.pbir`.

Without a catalogue, do not select only a linked Report: include its local model. [Report binding requirements](../../reference/power-bi/requirements-and-compatibility.md#report-binding) explain the separate certified-model case with a catalogue.

## 4. Refresh and view the result

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Open the service workspace. Find `Parcel_Dev` and `Parcel_Report_Dev`, confirm the Report is connected to that model, and open its card. After refresh, **Delivery Count is 2**. Inspect the refresh result if the card cannot query its data. A successful Build does not establish refresh access or Report rendering.

Reports have definitions, not a data Load. Refresh their semantic model. There is no catalogue status/history on this route.

## Cleanup

In the service, delete only the Report and model you created for this example, Reports first. Keep existing workspaces and other items. If you updated existing items, retain their original definitions rather than treating deletion as cleanup.

## Related tasks

- [Deploy the same source to another environment](environments.md).
- [Add a DAX Assumption](validate.md).
- [Look up supported native layout and formats](../../reference/power-bi/project-layout.md).
