# Share native modelling standards

Apply the same formatting and calculation structure to several models without copying the convention into each native project. Shared policy is TMDL; custom Python is not required.

Continue the [native Parcel model](native-tmdl.md#hide-relationship-foreign-keys): Delivery, Depot, the relationship and the same-name foreign-key overlay are already working. Add only the policy and format override below, keeping your workspace configuration. For direct entry, complete the [native model task](native-tmdl.md) first; then add the policy below.

## 1. Add the shared policy

Create `PowerBI/policy.tmdl` with the native formatting and calculation policy below:

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
	partition Display = calculationGroup
		mode: import
```

The policy applies to all final models in this project and declares no physical model of its own. Here it sets two measure formats and adds a native Display calculation group with a Current calculation item. The calculation group is ordinary TMDL, including the `calculationGroup` partition that Power BI Desktop also writes; without it, the service adds its own partition and Build's readback check fails.

To share the foreign-key convention too, move its annotation from the local overlay into the policy’s existing `model Model` section. That section then reads:

```tmdl
model Model
    discourageImplicitMeasures
    annotation 'Weaver.AutoHideForeignKeys' = true
```

Keep the policy’s Delivery and Display sections below it. The next step retains that annotation locally too; once policy owns it, you can omit the duplicate local declaration.

## 2. Override one convention locally

Replace the earlier rule-only `PowerBI/Parcel/Parcel.tmdl` with the local format override below. It retains the same foreign-key declaration, so the foreign-key rule remains in effect:

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
weaver check
weaver build --item SemanticModel/Parcel
```

<!-- cli-capture: {"id": "87b-policy-build", "title": "Build · native model with shared policy"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · native model with shared policy">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel


Build

  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel                                                                           0.0s
  Read target inventories                                                                                  0.1s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1

→   SemanticModel/Parcel · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Deploy semantic definitions · 1 action                                         21.0s</span>
→   SemanticModel/Parcel · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Verify deployed semantic definitions · 1 action                                20.5s</span>
  Install                                                                                                 41.5s
<span class="terminal-status-green">✓ Build                                                                                                   41.9s</span>

Installation
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  ce6f3aefefe56812fc09dd5dc15f4f40a696c13c59ca48ede27a97b34df7d447
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load SemanticModel/Parcel
```

The deployed definition now contains the Display group with its Current item, `discourageImplicitMeasures`, `0 "deliveries"` on Delivery Count (the local override), `#,##0.00` on InternalCost (the policy) and a hidden `Delivery[DepotId]`. The original partitions and relationship are unchanged. Delivery Count still evaluates to 2 and now formats as `2 deliveries`.

Authored native files still contain the declarations, not the transformed definition. Inspect the deployed definition through the service’s Get Definition API or a native model-definition tool.

The same model can now take shared standards and a local exception. If a convention needs logic that TMDL cannot express, [add a custom annotation](custom-annotations.md) without replacing the policy or native project.

## Related tasks

- [Add a custom annotation](custom-annotations.md).
- [Reuse a base model in variants](composition.md).
- [Look up policy and overlay precedence](../reference/power-bi/tmdl.md).
