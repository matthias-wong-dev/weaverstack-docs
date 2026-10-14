# Deploy a native semantic model

Deploy the PBIP/TMDL you already author, then hide relationship foreign keys with one built-in rule. The native files stay unchanged; Weaver applies the rule to the model definition it deploys.

## Native files first

A PBIP project contains the model’s native TMDL and its Report definitions. You can also author a model directly in a named TMDL file; [native project layout](../reference/power-bi/project-layout.md) describes both forms. Weaver does not require you to add an annotation before it can deploy the model.

## Before you start

[Install Weaver](../getting-started/installation.md). Use an existing Power BI service workspace and an identity allowed to create/update, read and refresh the model. Its licence and capacity must support the model mode.

The example contains inline Import data and works in an existing standalone Power BI workspace. No catalogue or source Warehouse is needed. [Managed Fabric sources](managed-sources.md) adds source coordination later.

Download or clone the [complete parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/main/examples/parcel-powerbi) and work from `examples/parcel-powerbi`. `PowerBI/Parcel/Parcel.pbip` opens the native project. Its model has three parcel rows, two depots, a relationship and a Delivery Count measure. Its Report has a Delivery Count card.

For an existing Fabric project, copy the `PowerBI/` directory and add the shown targets to its configuration, retaining the workspace and catalogue settings.

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
weaver build . --item SemanticModel/Parcel --workspace-config workspace-dev.yml
```

This selects **only the semantic model**. Build deploys and verifies `Parcel_Dev`; the Report stays local until you [deploy the linked Report](../reports/deploy.md).

## 4. Refresh and inspect the model

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Find `Parcel_Dev` in the workspace. After refresh, query **Delivery Count: it should be 2**. A model-definition tool or the service’s Get Definition API should show Delivery, Depot, their Import partitions and the many-to-one relationship.

You now have a deployed native model. Add the rule below to change its field list without editing the native columns.

<span id="hide-relationship-foreign-keys"></span>

## AutoHideForeignKeys: hide relationship foreign keys

### Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model instead of declaring another one.

### Deploy and inspect

```bash
weaver check .
weaver build . --item SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed native definition through a supported model-definition tool or the service's Get Definition API. `Delivery[DepotId]` should have `isHidden = true`; `Depot[DepotId]` and unrelated columns should stay visible. The relationship and both partitions should remain. You do not need a Report query to verify that transformation.

The local native column is not rewritten. Desktop does not execute Weaver annotations; the visibility change is applied to the deployment definition. Hidden columns are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild from source. A declaration of `false` is a no-op, not an instruction to undo an independently authored native hide.

<details markdown="1">
<summary>Inspect the native relationship</summary>

### Inspect the relationship the rule uses

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

</details>

## Carry the convention to the next model

You now have the native Parcel model and one local rule, with Delivery and Depot unchanged apart from field visibility. When that convention belongs on several models, [share it in `PowerBI/policy.tmdl`](shared-policy.md). The next task keeps this model and adds common formatting and a native calculation group; it does not ask you to start deployment again.

[Validate the model](validation.md) to check its number, or [connect a managed Fabric source](managed-sources.md) when Delivery comes from a Warehouse rather than inline data. [Weaver documents](../core-concepts/weaver-documents.md#native-models-overlays-and-annotations) explains where overlays fit beside normal native definitions.
