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
		formatString: 0 "delivered"
```

Executive excludes the InternalCosts **table** and gives Delivery Count its own format. Exclusion is not RLS/OLS or an access-control policy; validate security separately.

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
weaver check
weaver build --item SemanticModel/ParcelOperations --item Report/ParcelOperations --item SemanticModel/ParcelExecutive --item Report/ParcelExecutive
```

<!-- cli-capture: {"id": "90b-variants-build", "title": "Build · two variants and their Reports"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · two variants and their Reports">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/ParcelOperations
  Report/ParcelOperations
  SemanticModel/ParcelExecutive
  Report/ParcelExecutive


Build

    Create SemanticModel/ParcelExecutive                                                                  20.7s
    Create SemanticModel/ParcelOperations                                                                 20.6s
    Create Report/ParcelExecutive                                                                         20.6s
    Create Report/ParcelOperations                                                                        20.6s
  Create Power BI items                                                                                   1m22s
  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/ParcelOperations                                                                 0.0s
    Resolve Report/ParcelOperations                                                                        0.0s
    Resolve SemanticModel/ParcelExecutive                                                                  0.0s
    Resolve Report/ParcelExecutive                                                                         0.0s
  Read target inventories                                                                                  0.3s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/ParcelOperations
    changed                 1
    selected for build      1
  Report/ParcelOperations
    changed                 1
    selected for build      1
  SemanticModel/ParcelExecutive
    changed                 1
    selected for build      1
  Report/ParcelExecutive
    changed                 1
    selected for build      1

→   SemanticModel/ParcelExecutive · Deploy semantic definitions · 1 action
→   SemanticModel/ParcelOperations · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelOperations · Deploy semantic definitions · 1 action                               21.0s</span>
→   SemanticModel/ParcelOperations, Report/ParcelExecutive · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelExecutive · Deploy semantic definitions · 1 action                                21.1s</span>
→   SemanticModel/ParcelExecutive · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelOperations, Report/ParcelExecutive · Verify deployed semantic definitions · 1 action   20.5s</span>
→   Report/ParcelOperations · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelExecutive · Verify deployed semantic definitions · 1 action                       20.4s</span>
→   Report/ParcelExecutive · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓   Report/ParcelOperations · Deploy Report definitions · 1 action                                        20.3s</span>
→   Report/ParcelOperations · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓   Report/ParcelExecutive · Deploy Report definitions · 1 action                                         20.3s</span>
→   Report/ParcelExecutive · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓   Report/ParcelExecutive · Verify deployed Report definitions · 1 action                                20.8s</span>
<span class="terminal-status-green">✓   Report/ParcelOperations · Verify deployed Report definitions · 1 action                               20.8s</span>
  Install                                                                                                 1m22s
<span class="terminal-status-green">✓ Build                                                                                                   2m45s</span>

Installation
<span class="terminal-status-green">    8 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  b0841a33f1dc2109ba3070f63cbb77ad57afc5341b2a86fc50cfa98f3ab31ad9
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load SemanticModel/ParcelOperations SemanticModel/ParcelExecutive
weaver test SemanticModel/ParcelOperations SemanticModel/ParcelExecutive --source .
```

<!-- cli-capture: {"id": "90d-variants-test", "title": "Test · each variant's own Assumption"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · each variant&#x27;s own Assumption">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read validations                                                                                         0.1s
  Execute                                                                                                  1.8s
<span class="terminal-status-green">✓ Test                                                                                                     1.9s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    2 passed</span>
    0 failed
</code></pre>
</figure>
<!-- /cli-capture -->

Do not replace that Build selection with `PowerBI/Parcel`: the broad project selector includes the base. This configuration deliberately has no base target, so that broader request refuses. Source composition does not itself select a base for deployment.

## 3. Inspect the outputs

Both models and Reports now exist, and each Report is bound to its own model. Both models return Delivery Count = 2. The deployed definitions differ as declared: ParcelOperations has Delivery Rate and the InternalCosts table; ParcelExecutive has no InternalCosts table and formats Delivery Count as `0 "delivered"`. Shared policy from the [previous task](shared-policy.md) applies to both. No ParcelBase item was deployed.

For a second environment, create its configuration using [workspace mappings](../estate/environments.md), repeat the explicit four-item Build selection with that configuration, then refresh the two models. Do not edit the base merely to change destination names.

## 4. Diagnose a missing base

Save the Executive overlay, change `ParcelBase` to `MissingBase` in its annotation, and Check:

```bash
cp PowerBI/Parcel/ParcelExecutive.tmdl ParcelExecutive.tmdl.saved
weaver check
```

<!-- cli-capture: {"id": "90e-missing-base-check", "title": "Check · a variant names a missing base"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Check · a variant names a missing base">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code><span class="terminal-status-red">error: SemanticModel/ParcelExecutive references missing base &#x27;MissingBase&#x27; in PowerBI/Parcel; bases must be local to this project</span>

Enter to retry, Esc to exit.
</code></pre>
</figure>
<!-- /cli-capture -->

Press Esc at the retry prompt, then restore the file and Check again:

```bash
mv ParcelExecutive.tmdl.saved PowerBI/Parcel/ParcelExecutive.tmdl
weaver check
```

The failing overlay names MissingBase. The first Check refuses it in the local project scope; restoring the file makes discovery valid again. Bases must be local to the same Power BI group. Composition recursively merges raw local bases before final policy and overlays, then applies handlers once to the final model. Cycles and repeated ancestors are refused, not silently deduplicated. A base contributes source, not another selected deployment or copied validations.

## Related tasks

- [Look up exact composition and policy precedence](../reference/power-bi/tmdl.md).
- [Add validations to an output](validation.md).
- [Author a standalone TMDL model](from-tmdl.md).
