# Compose two model variants

Reuse a source foundation without deploying it as a physical base model. Give each output its own additions, Report and validations.

## Before you start

Continue the [native Parcel project](native-tmdl.md), keeping its working model, Report and overlays. Add a **copy** named ParcelBase as the source foundation for two audience variants. Nothing renames or removes Parcel.

From the project root, make the local source copies below. Existing destinations cause `copytree` to refuse rather than overwrite them:

```python title="prepare-variants.py"
import json
import shutil
from pathlib import Path

root = Path("PowerBI/Parcel")
shutil.copytree(root / "Parcel.SemanticModel", root / "ParcelBase.SemanticModel")
for name in ("ParcelOperations", "ParcelExecutive"):
    report = root / f"{name}.Report"
    shutil.copytree(root / "Parcel.Report", report)
    path = report / "definition.pbir"
    definition = json.loads(path.read_text())
    definition["datasetReference"] = {"byPath": {"path": f"../{name}.SemanticModel"}}
    path.write_text(json.dumps(definition, indent=2) + "\n")
```

Run `python prepare-variants.py` once. ParcelBase retains Delivery, Depot, their inline partitions and relationship. Add `PowerBI/Parcel/ParcelBase.tmdl` to supply the internal-cost table used by this example:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true

table InternalCosts
    column Amount
        dataType: int64
        sourceColumn: Amount
    partition InternalCosts = m
        mode: import
        source = #table(type table [Amount = Int64.Type], {{7}})
```

The output TMDL files below compose that local foundation. They are not precompiled, independently populated Desktop models. Their Reports use ordinary native Report definitions and Build resolves each same-name model association.

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

Each output owns its validations. Create the following file under **both** `PowerBI/Parcel/assumptions/ParcelOperations/` and `PowerBI/Parcel/assumptions/ParcelExecutive/`, named `Parcel.PositiveDeliveryCount.dax`:

```dax
/*
Assumption ID: Parcel.PositiveDeliveryCount
Description: The delivery count is positive.
*/
EVALUATE FILTER(ROW("DeliveryCount", [Delivery Count]), [DeliveryCount] <= 0)
```

Composition does not copy a base’s validations. Under `targets` in the existing `workspace-config.yml`, add:

```yaml title="Add under targets"
  SemanticModel/ParcelOperations: ParcelOperations
  Report/ParcelOperations: ParcelOperations
  SemanticModel/ParcelExecutive: ParcelExecutive
  Report/ParcelExecutive: ParcelExecutive
```

Keep the existing Parcel and source bindings. No ParcelBase target is needed because this task deploys only the two outputs.

## 2. Select only the outputs

From the same project root:

```bash
weaver check .
weaver build . --item SemanticModel/ParcelOperations --item Report/ParcelOperations --item SemanticModel/ParcelExecutive --item Report/ParcelExecutive
weaver load SemanticModel/ParcelOperations SemanticModel/ParcelExecutive
weaver test SemanticModel/ParcelOperations SemanticModel/ParcelExecutive --source .
```

<!-- review-todo: composition -->
!!! warning "TODO — capture both variants’ Build, Load and Test results"
    Run the commands immediately above for ParcelOperations and ParcelExecutive. Capture their terminal results and verify each Report binding and model query; the composition and preservation checks so far are offline.
<!-- /review-todo -->

Do not replace that Build selection with `PowerBI/Parcel`: the broad project selector includes the base. This configuration deliberately has no base target, so that broader request refuses. Source composition does not itself select a base for deployment.

## 3. Inspect the outputs

Verify both configured models and Reports exist, each Report binds to its own model, both cards show 2 and both model-owned Assumptions pass. Inspect native definitions: Operations has Delivery Rate and InternalCosts; Executive omits InternalCosts but retains Delivery Count and the relationship. No new physical ParcelBase item should exist.

For a second environment, create its configuration using [workspace mappings](../estate/environments.md), repeat the explicit four-item Build selection with that configuration, then refresh the two models. Do not edit the base merely to change destination names.

## 4. Diagnose a missing base

```bash
cp PowerBI/Parcel/ParcelExecutive.tmdl ParcelExecutive.tmdl.saved
# In your editor, change ParcelBase to MissingBase in the Executive annotation.
# Save the edited PowerBI/Parcel/ParcelExecutive.tmdl, then run Check.
weaver check .
mv ParcelExecutive.tmdl.saved PowerBI/Parcel/ParcelExecutive.tmdl
weaver check .
```

The failing overlay names MissingBase. The first Check refuses it in the local project scope; restoring the file makes discovery valid again. Bases must be local to the same Power BI group. Composition recursively merges raw local bases before final policy and overlays, then applies handlers once to the final model. Cycles and repeated ancestors are refused, not silently deduplicated. A base contributes source, not another selected deployment or copied validations.

Delete only the two example-created Reports and output models for cleanup, Reports first. Keep any pre-existing base or workspace.

## Related tasks

- [Look up exact composition and policy precedence](../reference/power-bi/tmdl.md).
- [Add validations to an output](validation.md).
- [Author a standalone TMDL model](from-tmdl.md).
