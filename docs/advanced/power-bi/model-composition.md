# Compose two model variants

Reuse a source foundation without deploying it as a physical base model. Give each output its own additions, Report and validations.

## Before you start

Use the independent [variant project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-variants) with the [ordinary Power BI prerequisites](../../basics/power-bi/deploy-pbip.md), plus DAX query rights for its Assumptions. Configure existing disposable workspaces. No catalogue or Fabric Environment is required by this inline Import example.

`ParcelBase.SemanticModel` supplies complete native data, relationships and measures. The two output packages supply native model properties, while their named TMDL files declare composition. An output package by itself is not a precompiled, independently populated Desktop model.

## 1. Read each difference

`PowerBI/Parcel/ParcelOperations.tmdl`:

```tmdl
model Model
	annotation 'Weaver.BaseSemanticModels' = ParcelBase

table Delivery
	measure 'Delivery Rate' = DIVIDE([Delivery Count], COUNTROWS(Delivery))
		formatString: 0.0%
```

Operations adds Delivery Rate and keeps InternalCosts.

`PowerBI/Parcel/ParcelExecutive.tmdl`:

```tmdl
model Model
	annotation 'Weaver.BaseSemanticModels' = ParcelBase

table InternalCosts
	annotation 'Weaver.Exclude' = true

table Delivery
	measure 'Delivery Count'
		formatString: #,##0
```

Executive excludes the InternalCosts **table** and changes Delivery Count formatting. Exclusion is not RLS/OLS or an access-control policy; validate security separately.

Each output owns its own `assumptions/<Model>/Parcel.PositiveDeliveryCount.dax` and a linked Report. Composition does not copy a base's validations.

## 2. Select only the outputs

From the fixture directory:

```bash
weaver check .
weaver build . --item SemanticModel/ParcelOperations --item Report/ParcelOperations --item SemanticModel/ParcelExecutive --item Report/ParcelExecutive --workspace-config workspace-dev.yml
weaver load SemanticModel/ParcelOperations SemanticModel/ParcelExecutive --workspace-config workspace-dev.yml
weaver test SemanticModel/ParcelOperations SemanticModel/ParcelExecutive --source . --workspace-config workspace-dev.yml
```

Do not replace that Build selection with `PowerBI/Parcel`: the broad project selector includes the base. The fixture deliberately has no base target, so that broader request refuses. Source composition does not itself select a base for deployment.

## 3. Inspect the outputs

Verify both configured models and Reports exist, each Report binds to its own model, both cards show 2 and both model-owned Assumptions pass. Inspect native definitions: Operations has Delivery Rate and InternalCosts; Executive omits InternalCosts but retains Delivery Count and the relationship. No new physical ParcelBase item should exist.

For a second environment, repeat the explicit four-item Build selection with `workspace-prod.yml`, then refresh the two models with that configuration. Do not edit the base merely to change destination names.

## 4. Diagnose a missing base

```bash
cp PowerBI/Parcel/ParcelExecutive.tmdl ParcelExecutive.tmdl.saved
cp failure/ParcelExecutive.tmdl PowerBI/Parcel/ParcelExecutive.tmdl
weaver check .
mv ParcelExecutive.tmdl.saved PowerBI/Parcel/ParcelExecutive.tmdl
weaver check .
```

The failing overlay names MissingBase. The first Check refuses it in the local project scope; restoring the file makes discovery valid again. Bases must be local to the same Power BI group. Cycles and repeated ancestors are refused, not silently deduplicated.

Delete only the two fixture-created Reports and output models for cleanup, Reports first. Keep any pre-existing base or workspace.

## Related tasks

- [Look up exact composition and policy precedence](../../reference/power-bi/tmdl.md).
- [Add validations to an output](../../basics/tests-and-assumptions.md#semantic-model-validations).
- [Author a standalone TMDL model](model-from-tmdl.md).
