# Share native modelling standards

Apply the same formatting and calculation structure to several models without copying the convention into each native project. Shared policy is TMDL; custom Python is not required.

Continue the [native Parcel model](native-tmdl.md#hide-relationship-foreign-keys): Delivery, Depot, the relationship and the same-name foreign-key overlay are already working. Add only the policy and format override below, keeping your workspace configuration. Direct entrants can use the complete [standards snapshot](../assets/examples/parcel-powerbi-standards.zip) with the same native model and [deployment prerequisites](native-tmdl.md#before-you-start). That snapshot also contains the optional custom handler from the next task; it is not needed for this policy.

## 1. Add the shared policy

Create `PowerBI/policy.tmdl` with the standards snapshot’s native formatting and calculation policy:

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

To share the foreign-key convention too, move its annotation from the local overlay into the policy’s existing `model Model` section. That section then reads:

```tmdl
model Model
    discourageImplicitMeasures
    annotation 'Weaver.AutoHideForeignKeys' = true
```

Keep the policy’s Delivery and Display sections below it. The local block in the next step retains the same annotation for readers using the unmodified standards snapshot; once policy owns it, you can omit that duplicate local declaration.

## 2. Override one convention locally

Replace the earlier rule-only `PowerBI/Parcel/Parcel.tmdl` with the local format override below. It retains the same foreign-key declaration, so this complete block also works with the unmodified standards snapshot:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true

table Delivery
    measure 'Delivery Count'
        formatString: 0 "deliveries"
```

The effective definition merges the native source, then shared policy, then this model's same-name overlay. The overlay's Delivery Count format wins; InternalCost retains `#,##0.00`. Omission is not general deletion. [TMDL reference](../reference/power-bi/tmdl.md) owns exact merge and replacement rules.

## 3. Deploy and inspect

```bash
weaver check .
weaver build . --item SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed native definition. It should contain Display/Current, `discourageImplicitMeasures`, the two intended formats and the hidden many-side Delivery[DepotId]. Original partitions and the relationship remain. If you deploy the linked Report, its Delivery Count should display `2 deliveries`; the native format properties establish the model result.

Authored native files still contain the declarations, not the transformed definition. Inspect the deployed definition through the service’s Get Definition API or a native model-definition tool.

The same model can now take shared standards and a local exception. If a convention needs logic that TMDL cannot express, [add a custom annotation](custom-annotations.md) without replacing the policy or native project.

## Related tasks

- [Add a custom annotation](custom-annotations.md).
- [Reuse a base model in variants](composition.md).
- [Look up policy and overlay precedence](../reference/power-bi/tmdl.md).
