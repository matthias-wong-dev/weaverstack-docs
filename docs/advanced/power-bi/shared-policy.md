# Share native modelling standards

Apply the same formatting and calculation structure to several models without copying the convention into each native project. Shared policy is TMDL; custom Python is not required.

Start with a fresh [ordinary parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi) and its [deployment prerequisites](../../basics/power-bi/deploy-pbip.md). The independent [standards fixture](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-standards) contains the completed policy plus the separate custom annotation example.

## 1. Add the shared policy

Create `PowerBI/policy.tmdl`:

```tmdl
model Model
	discourageImplicitMeasures

table Delivery
	measure 'Delivery Count'
		formatString: #,##0
	measure InternalCost
		formatString: #,##0.00

table Display
	calculationGroup
		precedence: 10
		calculationItem Current = SELECTEDMEASURE()
	column Calculation
		dataType: string
		sourceColumn: Name
		summarizeBy: none
```

The policy applies to all final models in this project and declares no physical model of its own. Here it sets two measure formats and adds a native Display calculation group with a Current calculation item. The calculation group is native TMDL, not an invented built-in annotation.

## 2. Override one convention locally

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true

table Delivery
    measure 'Delivery Count'
        formatString: 0 "deliveries"
```

The effective definition merges the native source, then shared policy, then this model's same-name overlay. The overlay's Delivery Count format wins; InternalCost retains `#,##0.00`. Omission is not general deletion. [TMDL reference](../../reference/power-bi/tmdl.md) owns exact merge and replacement rules.

## 3. Deploy and inspect

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed native definition. It should contain Display/Current, `discourageImplicitMeasures`, the two intended formats and the hidden many-side Delivery[DepotId]. Original partitions and the relationship remain. The Report's Delivery Count should display `2 deliveries`.

Authored native files still contain the declarations, not the transformed definition. Use the service's Get Definition API or a supported native inspection tool to inspect deployment; no public compiled-TMDL export is supplied by this workflow.

Delete only the fixture-created Report/model for cleanup, Reports first.

## Related tasks

- [Add a custom annotation](custom-annotations.md).
- [Reuse a base model in variants](model-composition.md).
- [Look up policy and overlay precedence](../../reference/power-bi/tmdl.md).
