# Validate a semantic model

A successful refresh says the model ran, not that its measure is right. Add an Assumption to the working Parcel model, then reconcile the additional source-backed model with independent Warehouse SQL.

In [Power BI-only mode, without a Catalogue](index.md#two-ways-to-use-weaver-with-power-bi), DAX validations run directly against the selected model using source/file mode. Results return to the caller; Weaver records no installed Test history.

With a Catalogue, Build can install authored validations. Installed Test runs record results in the Catalogue, and Health assesses them alongside other managed work. Source/file mode remains a deliberate option in Catalogue-backed projects too; the commands below distinguish the two.

<span id="choose-your-working-checkpoint"></span>

## Choose the model you are checking

- **ParcelWarehouse already reads the managed Warehouse:** go straight to [Compare DAX with source SQL](#compare-dax-with-source-sql). Keep the source and model you just loaded; no inline-data setup or new provisioning is needed.
- **You are checking the native inline Parcel model:** [add the DAX Assumption](#start-from-the-model-you-already-deployed) to that existing model and retain your overlay.

## Start from the model you already deployed

For the Assumption, continue the [native model](native-tmdl.md): Parcel has inline Import data, Delivery Count evaluates to 2, and its same-name overlay hides the relationship foreign key. Keep that overlay and your existing workspace configuration. You add one DAX file, not another project or deployment setup.

If you are starting here, generate and deploy the [native Parcel example](native-tmdl.md#before-you-start), then add the Assumption below. Keep any existing overlay.

DAX queries need model Read and Build permissions and an identity permitted by the tenant’s Execute Queries setting. Reconciliation also needs SELECT access to the Warehouse source. Use existing permissions; do not change tenant settings for this exercise.

## 1. Add the DAX Assumption

Create `PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax`:

```dax
/*
Assumption ID: Parcel.PositiveDeliveryCount
Description: The delivery count is positive.
*/
EVALUATE FILTER(ROW("DeliveryCount", [Delivery Count]), [DeliveryCount] <= 0)
```

The filename, metadata ID and `assumptions` directory agree. `Parcel` in the directory is the local logical model name, not the physical `Parcel_Dev`. An Assumption returns violating rows; zero rows passes. [DAX validation reference](../reference/power-bi/validations.md) owns the complete metadata rules.

## 2. Run the authored query

```bash
weaver check .
weaver test SemanticModel/Parcel --source . --file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax'
```

<!-- cli-capture: {"id": "84-native-source-dax-validation", "title": "Test · source DAX against the deployed model"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · source DAX against the deployed model">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read validations                                                                                         0.5s
  Execute                                                                                                  0.7s
<span class="terminal-status-green">✓ Test                                                                                                     1.3s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    1 passed</span>
    0 failed
</code></pre>
</figure>
<!-- /cli-capture -->

The Assumption passed with zero violations and exit 0. You do not need Build merely to edit a source query: this run evaluates the new file against the already deployed model.

The file is evaluated against the model you already deployed. This source run does not install a validation or write catalogue history. [Test modes](../reference/cli/test.md) explains installing a validation when you want recorded estate results.

<details markdown="1">
<summary>Optional: make the measure fail, then restore your model</summary>

## 3. Produce a finding without losing your overlay

Use this declaration for the optional failure exercise:

```tmdl
table Delivery
	measure 'Delivery Count' = -1
```

Back up the existing same-name overlay first; it may contain the foreign-key rule, policy overrides or your own conventions. Use an unused `Parcel.tmdl.saved` filename and keep the same shell for correction:

```bash
test ! -e Parcel.tmdl.saved || exit 1
had_overlay=false
if test -f PowerBI/Parcel/Parcel.tmdl; then
  had_overlay=true
  cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
fi
```

Edit `PowerBI/Parcel/Parcel.tmdl` to set Delivery Count to `-1`, using the failure declaration above. Keep every other declaration in the overlay. If `table Delivery` or its measure already exists, edit that declaration rather than pasting a second one: duplicate declarations are refused. In the native rule-only checkpoint, add the Delivery section beneath the existing `model Model` annotation. If you have no overlay, create the file with the complete failure declaration.

Deploy that changed measure and run the same source Assumption:

```bash
weaver check .
weaver build . --item SemanticModel/Parcel
weaver load SemanticModel/Parcel
weaver test SemanticModel/Parcel --source . --file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax'
```

<!-- cli-capture: {"id": "91-native-failed-source-dax", "title": "Test · deliberately wrong measure"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · deliberately wrong measure">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read validations                                                                                         0.6s
  Execute                                                                                                  1.0s
<span class="terminal-status-red">✗ Test                                                                                                     1.6s</span>

<span class="terminal-status-red">test failed</span>

<span class="terminal-status-red">  failed     Assumption  SemanticModel/Parcel/Parcel.PositiveDeliveryCount  (1 violation)</span>

Test summary
    0 passed
<span class="terminal-status-red">    1 failed</span>

  SemanticModel/Parcel/Parcel.PositiveDeliveryCount:
    {&#x27;DeliveryCount&#x27;: -1}
</code></pre>
</figure>
<!-- /cli-capture -->

Test returned one violating row, `DeliveryCount = -1`, and exit 1. This is a finding, not a query failure. A permission or execution failure produces an `invalid` node and also exits 1. Python returns the validation report: inspect `succeeded`, node `status` and diagnostics rather than using a retired `strict=` argument.

## 4. Restore the prior model and rerun

Run the restoration even if Check, Build, Load or Test failed. A deliberate failed Test exits 1, so do not put restoration behind `&&` or a shell’s automatic exit-on-error:

```bash
if test "$had_overlay" = true; then
  mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
else
  rm PowerBI/Parcel/Parcel.tmdl
fi
weaver check .
weaver build . --item SemanticModel/Parcel
weaver load SemanticModel/Parcel
weaver test SemanticModel/Parcel --source . --file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax'
```

<!-- cli-capture: {"id": "94-native-restored-source-dax", "title": "Test · restore the saved overlay"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · restore the saved overlay">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read validations                                                                                         0.6s
  Execute                                                                                                  0.8s
<span class="terminal-status-green">✓ Test                                                                                                     1.5s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    1 passed</span>
    0 failed
</code></pre>
</figure>
<!-- /cli-capture -->

The Assumption passed again. The existing overlay is restored byte for byte, including its foreign-key convention. Only the direct-entry case that had no overlay removes the file created by this exercise. If the shell was interrupted, restore `Parcel.tmdl.saved` manually before deploying again.


`--file` explicitly selects source/file mode even when the configuration contains a catalogue. `--source .` identifies the project; it does not force file mode by itself. Without a configured catalogue, `--source .` alone uses source mode. Source/file mode records no installed `_.TestStatus` or Test history. Repeat `--file` for paths/directories/globs and `--name` for case-insensitive whole-validation regex seeds; each supplied name pattern must match.

To install this Assumption in a catalogue-backed project, Build the changed model declarations, then run Test without `--file`. Installed mode reads the catalogue’s validation definition and records results. Do not assume an edited local DAX file changed that installed definition.

</details>

## Compare DAX with source SQL

Use the already loaded [managed-source model](managed-sources.md) in this same project. **ParcelWarehouse** reads Operations’ CurrentStatus View; the native **Parcel** model remains inline. Do not compare the inline Delivery data with an unrelated Warehouse result.

Add a measure to the existing `CurrentStatus` declaration in `PowerBI/Parcel/ParcelWarehouse.tmdl`. Its complete contents become:

```tmdl
model Model
    culture: en-US
    defaultMode: import
    annotation 'Weaver.BaseSemanticModels' = Parcel

table CurrentStatus
    annotation 'Weaver.Source' = Warehouse/Operations/Parcel.CurrentStatus
    measure 'Managed Parcel Count' = COUNTROWS(CurrentStatus)
```

Create `PowerBI/Parcel/tests/ParcelWarehouse/Parcel.CurrentStatusReconciles.dax`:

```dax
/*
Test ID: Parcel.CurrentStatusReconciles
Description: Model parcel count agrees with the managed Warehouse View.
Expected source: Warehouse/Operations
Expected SQL: |
  SELECT COUNT_BIG(*) AS ParcelCount FROM [Parcel].[CurrentStatus]
*/
EVALUATE ROW("ParcelCount", [Managed Parcel Count])
```

Build installs this model’s measure and Test; refresh it, then compare the model count with independent SQL. Both should return 2:

```bash
weaver check
weaver build --item SemanticModel/ParcelWarehouse --bind-data-sources
weaver load SemanticModel/ParcelWarehouse
weaver test SemanticModel/ParcelWarehouse --name 'Parcel[.]CurrentStatusReconciles'
```

<!-- review-todo: dax-sql -->
!!! warning "TODO — capture Parcel.CurrentStatusReconciles Test output"
    This exact Test has not run because ParcelWarehouse refresh is blocked by its missing credentialled connection. Capture its passing result after refresh, then exercise and restore the optional discrepancy below. Native DAX validation above is already verified.
<!-- /review-todo -->

```bash
weaver health
```

<details markdown="1">
<summary>Inspect the recorded model and validation evidence</summary>

This is installed mode. Inspect CurrentStatus under logical `SemanticModel/ParcelWarehouse` in `_.SemanticModelTable`, and the `_.Dependency` row whose authored `Dependency reference` is `Warehouse/Operations/Parcel.CurrentStatus`. Source mode/access belongs in the table metadata; source identity belongs in Dependency. This generated Import partition uses SQL access.

Inspect the installed validation in `_.SemanticModelTest` and its result in `_.TestStatus`. Model refresh and Test results sit beside Warehouse state in the same catalogue. With no item selector, Health covers the managed estate, not arbitrary workspace items.

</details>

<details markdown="1">
<summary>Optional: inspect a DAX-to-SQL discrepancy and restore it</summary>

### Produce and correct a discrepancy

Save `PowerBI/Parcel/ParcelWarehouse.tmdl` to an unused `ParcelWarehouse.tmdl.saved` file. In the existing measure declaration, change `COUNTROWS(CurrentStatus)` to `COUNTROWS(CurrentStatus) + 1`. Keep the source annotation and the rest of the file.

```bash
weaver build --item SemanticModel/ParcelWarehouse --bind-data-sources
weaver load SemanticModel/ParcelWarehouse
weaver test SemanticModel/ParcelWarehouse --name 'Parcel[.]CurrentStatusReconciles'
```

Expect a discrepancy: actual 3 against SQL expected 2. Restore your saved file even if a command fails, then repeat the three commands. The corrected Test should pass. Do not put restoration behind `&&` or automatic exit-on-error: a deliberate failed Test exits 1.

This edits the additional model’s measure, not Warehouse data or the native Parcel model. Access/query errors are invalid validations, not discrepancies; installed `_.TestStatus` records execution errors as `Error`. Binding uses an existing approved connection, not new credentials.

</details>

## Read the estate result

In a catalogue-backed project, `weaver test` without item selectors runs installed Lakehouse, Warehouse and model validations. [Run and inspect the estate](../estate/operate.md) combines those outcomes with source loads and model refreshes. Exact diagnostics and recording boundaries belong in [Test behaviour](../reference/operation-behaviour/test.md).

For cleanup, delete only example-created Reports/models, Reports first. Retire the example’s Operations Warehouse only through a scoped approved procedure; retain shared catalogues, workspaces and connections. Do not use unscoped Wipe.
