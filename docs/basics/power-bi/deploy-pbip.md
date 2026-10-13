# Deploy semantic models and Reports with PBIP

Weaver works with normal TMDL and native Report definitions. Keep them in the project, use Build to deploy them and Load to refresh the model. Optional TMDL overlays and Weaver annotations add your engineering conventions to those native definitions.

## Native files first

A PBIP project contains the model’s native TMDL and its Report definitions. You can also author a model directly in a named TMDL file; [native project layout](../../reference/power-bi/project-layout.md) describes both forms. Weaver does not require you to add an annotation before it can deploy the model.

## Before you start

[Install the documented snapshot](../../getting-started/installation.md). Use an existing Power BI service workspace and an identity with model/Report create or update rights, refresh rights and permission to view the Report. The service licence and model mode must support those operations.

The example uses inline Import data to isolate deployment from source loading. It can run with just an existing service workspace. The [managed-source example](#use-a-managed-source) below connects a model to Warehouse data in the same project.

Download or clone the [complete parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi) and work from `examples/parcel-powerbi`. `PowerBI/Parcel/Parcel.pbip` opens the native project. Its model has three parcel rows, two depots, a relationship and a Delivery Count measure. Its Report has a Delivery Count card.

If you are adding this model to an existing Fabric project, copy the example’s `PowerBI/` directory into that project. Add the model and Report under your existing configuration’s `targets`; retain its workspace and catalogue settings. The same commands then register the items in the shared catalogue.

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

Reports use their semantic model’s data, so refresh the model rather than loading the Report. In a catalogue-backed project, [Health](../../reference/cli/health.md) includes the registered model’s refresh state with the rest of the estate. The small catalogue-free example has only the command’s refresh report.

## Add an overlay and a Weaver annotation

Once the native project is working, add a convention without maintaining another copy of its model. For example, hide relationship foreign keys from the field list while keeping them available to the relationship.

### Hide relationship foreign keys

#### 1. Inspect the native relationship

The model relates `Delivery[DepotId]` on the many side to `Depot[DepotId]` on the one side. The authored columns are visible. A model without a relationship would give this rule nothing to hide.

#### 2. Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model instead of declaring another one.

#### 3. Deploy and inspect

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed native definition through a supported model-definition tool or the service's Get Definition API. `Delivery[DepotId]` should have `isHidden = true`; `Depot[DepotId]` and unrelated columns should stay visible. The relationship and partitions remain, and the Report still shows Delivery Count = 2.

The local native column is not rewritten. Desktop does not execute Weaver annotations; the visibility change is applied to the deployment definition. Hidden columns are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild from source. A declaration of `false` is a no-op, not an instruction to undo an independently authored native hide.

### Use your own convention

Custom annotations use the same native TMDL declaration mechanism. A project can supply a Python handler for a name such as `Parcel.DisplayFolder`, then use it on a measure to set a project-specific display folder. Built-in names start with `Weaver.`; custom handlers use your project’s namespace.

[Add a custom model annotation](../../advanced/power-bi/custom-annotations.md) gives the complete handler and its TMDL declaration. Start with a built-in when it fits, and use the custom handler when the convention needs code. [Weaver documents](../../core-concepts/weaver-documents.md#native-models-overlays-and-annotations) explains how these declarations fit the authoring model.

## Cleanup

In the service, delete only the Report and model you created for this example, Reports first. Keep existing workspaces and other items. If you updated existing items, retain their original definitions rather than treating deletion as cleanup.

## Use a managed source

The native model can participate in the same dependency graph as its source data. `Weaver.Source` identifies the managed Table; source Load then precedes model refresh, and Health can identify a model that is behind its source.

Use the separate source-backed fixture below, not the inline-data project used above. The two examples have different partitions and workspace configurations.

### Before the source-backed example

Use the [complete Fabric integration project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-fabric) from its example directory. Configure an existing disposable Fabric workspace, compatible Weaver catalogue Warehouse and an empty Operations Warehouse. This SQL/Import route uses no Lakehouse or Spark runtime; Warehouse-only Build does not require a published Fabric Environment.

You need Warehouse create/alter/load and SELECT rights, catalogue read/write, model/Report deployment and refresh/view rights. Import refresh needs an existing supported service connection and credentials with Warehouse SQL access. Weaver does not create credentials. Only request binding to a connection you are permitted to use.

If you do not yet have a catalogue, the [first Fabric project](../../getting-started/first-project.md) supplies the setup route. Do not point this exercise at an existing production estate.

### 1. Configure destination and source separately

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

### 2. Build and load the Warehouse first

```bash
weaver check .
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --workspace-config workspace-dev.yml
```

The source table contains three rows with Delivered values 1, 1, 0. Confirm it is loaded before deploying/refreshing the model.

### 3. Deploy the model and Report

```bash
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Source-data definitions and model/Report definitions use separate Build calls against the same project and configuration. `--bind-data-sources` requests supported binding to an existing matching connection; it does not administer gateways or create credentials. Inspect the model's resolved shared expression and retained partition navigation, its refresh outcome and the Report's actual model binding. The Report card should show 2.

After deployment, [Add Tests and Assumptions](../tests-and-assumptions.md#compare-dax-with-source-sql) checks the model’s DAX result against independent source SQL. [Run and inspect the estate](../run-and-inspect-estate.md) uses the shared Load, Test and Health flow.

For cleanup, delete only this fixture’s newly created Report/model, then retire its disposable Operations Warehouse through a scoped approved procedure. Keep existing shared catalogues, workspaces and connections; do not use unscoped Wipe.

## Related tasks

- [Add Tests and Assumptions](../tests-and-assumptions.md) across data items and models.
- [Configure the workspace](../workspace-and-python-runtime.md) for development and production.
- [Share native model standards](../../advanced/power-bi/shared-policy.md) when a convention applies to several models.
