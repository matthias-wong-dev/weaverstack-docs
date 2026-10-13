# Add Tests and Assumptions

A Test compares expected rows with actual rows. An Assumption returns rows that violate a condition. The same rules apply to Lakehouse Python/Spark SQL, Warehouse SQL and semantic-model DAX. Build installs validations; Test runs them and records results for Health.

Keep the validation beside the data or model it checks. An independent calculation can catch a defect that a check repeating the original transformation would miss.

> **Design background:** [Tests and Assumptions](https://principlesofdataengineering.org/docs/quality-reliability/tests-and-assumptions/) distinguishes comparison with an independent result from monitoring rows that violate a condition. Weaver runs both through Test.

## Choose the validation form

- Lakehouse validations use Python or Spark SQL; [Test](../reference/weaver-documents/test.md) and [Assumption](../reference/weaver-documents/assumption.md) define those forms.
- [Warehouse validations](#warehouse-validations) below provide a complete SQL example.
- [Semantic-model validations](#semantic-model-validations) use DAX against a native model.
- [Compare DAX with source SQL](#compare-dax-with-source-sql) to check a measure against its managed source independently.

These examples are independent. Use the one for the item you are working on; a model validation does not require you to complete the Warehouse example first.

## Warehouse validations

### Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Use a Fabric workspace where you can create or modify a catalogue Warehouse and a target Warehouse.

### 1. Initialise the project

Create a project containing `Warehouse/Operations`:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-validation \
  --catalogue Catalogue \
  --warehouse Operations \
  --no-example
cd parcel-validation
```

Replace `Parcel Development` with your workspace. Weaver writes `workspace-config.yml` and an empty `Warehouse/Operations` directory. The command ends with `Weaver project ready in .../parcel-validation.`

### 2. Add data to validate

Create `Warehouse/Operations/Parcel.Status.sql`:

```sql
/*
Table ID: Parcel.Status

Description: Current parcel status in the validation example.

Lineage: A deterministic parcel feed represented by this example.

Primary key: Parcel ID

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
*/
select v.[Parcel ID]
     , v.[Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v ([Parcel ID], [Status]);
```

Load will materialise two rows for the validations to read.

### 3. Add a Test

Create `Warehouse/Operations/tests/Parcel.StatusMatches.sql`:

```sql
/*
Test ID: Parcel.StatusMatches

Description: Current parcel status matches the expected rows.

Primary key: Parcel ID
*/
select v.[Parcel ID]
     , v.[Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v ([Parcel ID], [Status]);

select [Parcel ID]
     , [Status]
from [Parcel].[Status];
```

The first result is expected; the second is actual. The Test passes when both contain the same rows. A row found only in expected is missing, and a row found only in actual is unexpected. A changed row therefore produces one missing row and one unexpected row.

`Primary key` is optional. It correlates diagnostic rows from the two sides; it does not change what counts as a discrepancy. Weaver infers the dependency on `Parcel.Status` from the actual query.

### 4. Add an Assumption

Create `Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql`:

```sql
/*
Assumption ID: Parcel.StatusIsKnown

Description: Every parcel has a status recognised by this example.
*/
select [Parcel ID]
     , [Status]
from [Parcel].[Status]
where [Status] is null
   or [Status] not in ('Accepted', 'In transit', 'Delivered');
```

Every returned row violates the statement in the description. The Assumption passes when the query returns no rows. Weaver infers its dependency from the query as well.

### 5. Check, build and load

Validate the complete project, install it and populate the Table:

```bash
weaver check
weaver build
weaver load Warehouse/Operations
```

Check prints `Project valid.` Build should report no failed actions and installs the Table, Test and Assumption; it does not execute either validation. Load should report `Parcel.Status` as succeeded with two rows.

### 6. Run the validations

Execute every installed validation in the item, then inspect the current state:

```bash
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

Test should report `Parcel.StatusMatches` and `Parcel.StatusIsKnown` as passed. The Test has `0 missing, 0 unexpected`; the Assumption has `0 violations`. Health should show Green Build, Load and Tests sections.

A failed validation did run: it found discrepancies or violating rows. A validation reported as unable to run did not produce a valid result and is not a pass.

### 7. Diagnose one deliberate failure

Replace `Warehouse/Operations/tests/Parcel.StatusMatches.sql` with this complete failing version:

```sql
/*
Test ID: Parcel.StatusMatches

Description: Current parcel status matches the expected rows.

Primary key: Parcel ID
*/
select v.[Parcel ID]
     , v.[Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'In transit')
) as v ([Parcel ID], [Status]);

select [Parcel ID]
     , [Status]
from [Parcel].[Status];
```

Install the edited Test, then target it deliberately so the report includes diagnostic rows:

```bash
weaver check
weaver build
weaver test Warehouse/Operations \
  --name 'Parcel[.]StatusMatches'
```

The Test should fail for `P-1002` with one missing row (`In transit`) and one unexpected row (`Delivered`). The command exits non-zero, and Health records the Test section as Red until a later installed run passes.

Restore the complete passing Test from step 3, then install and run all validations again:

```bash
weaver check
weaver build
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

The item returns to Green. Editing the source without Build would leave Test running the previously installed definition. To test edited source directly against the deployed Warehouse:

```bash
weaver test Warehouse/Operations --source . --file 'Warehouse/Operations/tests/Parcel.StatusMatches.sql'
```

`--file` selects file mode even with a catalogue configured. `--source` identifies the project; it does not force file mode on its own. Repeat `--file` for files/directories/glob patterns and `--name` for case-insensitive whole-validation regex seeds. Each supplied name pattern must match. File mode records no `TestStatus` or installed history. Python uses `names=` and `files=` and returns a report for findings; inspect `succeeded`, `status` and node diagnostics rather than using a retired `strict=` argument.

## Semantic-model validations

Add a DAX Assumption to the Parcel model. Its result is evaluated by the same Test operation and pass rule used above.

### Before you start

Use the independent [validation project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-validation). Work from its directory, edit `workspace-dev.yml` to your disposable workspace, and use the [ordinary deployment prerequisites](power-bi/deploy-pbip.md).

You also need model Read and Build permissions for DAX queries and an identity allowed by the tenant's Execute Queries setting. Do not change tenant settings simply to run the example. The supplied example uses source validation. For installed model validation and shared Health state, use the [managed-source task](power-bi/deploy-pbip.md#use-a-managed-source).

### 1. Deploy and refresh

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

The Delivery Count card should show 2. The model owns `PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax`:

```dax
/*
Assumption ID: Parcel.PositiveDeliveryCount
Description: The delivery count is positive.
*/
EVALUATE FILTER(ROW("DeliveryCount", [Delivery Count]), [DeliveryCount] <= 0)
```

The filename, metadata ID and `assumptions` directory agree. The model name in the path is the local logical name, not `Parcel_Dev`.

### 2. Run the source Assumption

```bash
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect a `passed` validation node with zero violations and CLI exit 0. `--source .` reads the edited validation file; no Build is needed merely to change that query. Without a catalogue this uses source/file mode. With a configured catalogue, add `--file 'PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax'` when you deliberately want that mode rather than installed validation recording. `--file` takes a path; it is not a bare flag.

### 3. Produce a finding

The supplied `failure/Parcel.tmdl` is a complete optional overlay:

```tmdl
table Delivery
	measure 'Delivery Count' = -1
```

Copy it into the model's overlay path and deploy the changed measure:

```bash
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect `failed` with one violating row, `DeliveryCount = -1`, and CLI exit 1. Inspect the returned diagnostics. A query/permission failure instead produces an `invalid` node and also exits 1; it is neither a finding nor a pass. Python returns the validation report, so inspect its outcomes rather than adding an obsolete `strict=` option.

### 4. Correct it

Remove only the overlay copied in the previous step, then redeploy and rerun:

```bash
rm PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect `passed` again. For cleanup, delete only this example's newly created Report/model, Reports first.

## Compare DAX with source SQL

Use the separate [managed-source parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-fabric). Work from that example directory and first [build its Warehouse, model and Report](power-bi/deploy-pbip.md#use-a-managed-source). This is not the inline-data project used in the previous example.

The identity needs DAX query Read/Build access and permission under the tenant’s Execute Queries setting, plus SELECT access to the Warehouse source. Use existing permissions; do not change tenant settings for this exercise.

The supplied model-owned Test evaluates Delivery Count and compares it with the Warehouse's sum of Delivered. Both should return 2:

```bash
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
weaver health --workspace-config workspace-dev.yml
```

Inspect Delivery's metadata row under logical `SemanticModel/Parcel` in `_.SemanticModelTable`, and its `_.Dependency` row whose authored `Dependency reference` is `Warehouse/Operations/Parcel.Delivery`. Source mode/access belongs in the table metadata; source identity belongs in Dependency. A null `Source access` is valid for this retained authored partition and does not mean its mapping failed.

The Test result and the model’s refresh state appear beside Warehouse state in the same catalogue. Inspect the installed validation in `_.SemanticModelTest` and its result in `_.TestStatus`. With no item selector, Health covers the managed estate.

### Produce and correct a discrepancy

The fixture's failing overlay makes the model measure one greater than the source calculation:

```bash
cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]DeliveryReconciles' --workspace-config workspace-dev.yml
```

Expect a failed finding, actual 3 versus expected 2, then a pass after correction. Restore the original overlay even if a command fails. Access/query errors are `invalid` validation nodes, not discrepancies; installed TestStatus records them as `Error`. Failed/invalid CLI Tests exit 1.

For cleanup, delete only fixture-created Reports/models, then retire its Operations Warehouse through a scoped approved procedure. Keep the shared catalogue, workspace and connections. Do not use unscoped Wipe.

## Read the estate result

In a catalogue-backed project, `weaver test` without item selectors runs the installed Lakehouse, Warehouse and model validations. `weaver health` brings their current outcomes together with source loads and model refreshes. Source/file-mode tests read authored queries without recording installed history.

See [Run and inspect the estate](run-and-inspect-estate.md) for the normal operating flow. Exact metadata, diagnostics and exit behaviour belong in the [Test reference](../reference/operation-behaviour/test.md) and [DAX validation reference](../reference/power-bi/validations.md).
