# Deploy a native semantic model

Deploy the PBIP/TMDL you already author, then hide relationship foreign keys with one built-in rule. The native files stay unchanged; Weaver applies the rule to the model definition it deploys.

## Native files first

A PBIP project contains the model’s native TMDL and its Report definitions. You can also author a model directly in a named TMDL file; [native project layout](../reference/power-bi/project-layout.md) describes both forms. Weaver does not require you to add an annotation before it can deploy the model.

## Before you start

[Install the documented snapshot](../getting-started/installation.md). Use an existing Power BI service workspace and an identity with model/Report create or update rights, refresh rights and permission to view the Report. The service licence and model mode must support those operations.

The example uses inline Import data to isolate deployment from source loading. It can run with just an existing service workspace. It needs no catalogue, Lakehouse, Warehouse or Fabric Environment. This also supports an existing standalone Power BI workspace; [managed Fabric sources](managed-sources.md) add source lineage and recorded estate state later.

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

## 3. Deploy the native model

```bash
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
```

`PowerBI/Parcel` selects the native model and its linked Report. Because this catalogue-free selection includes a linked Report, it also includes that Report’s local model; Weaver deploys the model first. [Deploy a native Report](../reports/deploy.md) owns Report binding and readback. The broader selection deploys both items; it does not make a Report necessary to author or inspect the model.

Without a catalogue, do not select only a linked Report: include its local model. [Report binding requirements](../reference/power-bi/requirements-and-compatibility.md#report-binding) explain the separate certified-model case with a catalogue.

## 4. Refresh and inspect the model

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Find `Parcel_Dev` in the service workspace and inspect its native definition through a supported model-definition tool or the service’s Get Definition API. Delivery and Depot should retain their Import partitions and many-to-one relationship. After refresh, **Delivery Count should evaluate to 2**. That query or the optional Report card is a separate data check; a successful Build does not prove refresh access or Report rendering.

Reports use their semantic model’s data, so refresh the model rather than loading the Report. In a catalogue-backed project, [Health](../reference/cli/health.md) includes the registered model’s refresh state with the rest of the estate. The small catalogue-free example has only the command’s refresh report.

## Hide relationship foreign keys

### 1. Inspect the native relationship

The native `definition/relationships.tmdl` relates the many-side Delivery key to Depot. Both authored columns are visible:

```tmdl
relationship Delivery_Depot
	fromColumn: Delivery.DepotId
	toColumn: Depot.DepotId
	fromCardinality: many
	toCardinality: one
	crossFilteringBehavior: oneDirection
```

The rule hides the many-side key from the field list, not the one-side key.

### 2. Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model instead of declaring another one.

### 3. Deploy and inspect

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed native definition through a supported model-definition tool or the service's Get Definition API. `Delivery[DepotId]` should have `isHidden = true`; `Depot[DepotId]` and unrelated columns should stay visible. The relationship and both partitions should remain. You do not need a Report query to verify that transformation.

The local native column is not rewritten. Desktop does not execute Weaver annotations; the visibility change is applied to the deployment definition. Hidden columns are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild from source. A declaration of `false` is a no-op, not an instruction to undo an independently authored native hide.

## Carry the convention to the next model

You now have the native Parcel model and one local rule, with Delivery and Depot unchanged apart from field visibility. When that convention belongs on several models, [share it in `PowerBI/policy.tmdl`](shared-policy.md). The next task keeps this model and adds common formatting and a native calculation group; it does not ask you to start deployment again.

[Validate the model](validation.md) to check its number, or [connect a managed Fabric source](managed-sources.md) when Delivery comes from a Warehouse rather than inline data. [Weaver documents](../core-concepts/weaver-documents.md#native-models-overlays-and-annotations) explains where overlays fit beside normal native definitions.
