# Add Tests and Assumptions

A Test compares expected rows with actual rows. An Assumption returns rows that violate a condition. Build installs both kinds of validation, Test executes them and Health reads their current recorded outcomes.

> **Design background:** [Principles of Data Engineering distinguishes tests from monitored assumptions](https://principlesofdataengineering.org/docs/quality-reliability/tests-and-assumptions/): tests compare independently calculated results, while Assumptions surface monitored violating records for attention rather than automatically invalidating the whole pipeline. Weaver still records an Assumption that returns rows as a failed validation under the Test operation semantics described below.

This guide adds one Test and one Assumption to a small Warehouse pipeline.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Use a Fabric workspace where you can create or modify a catalogue Warehouse and a target Warehouse.

## 1. Initialise the project

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

## 2. Add data to validate

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

## 3. Add a Test

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

## 4. Add an Assumption

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

## 5. Check, build and load

Validate the complete project, install it and populate the Table:

```bash
weaver check
weaver build
weaver load Warehouse/Operations
```

Check prints `Project valid.` Build should report no failed actions and installs the Table, Test and Assumption; it does not execute either validation. Load should report `Parcel.Status` as succeeded with two rows.

## 6. Run the validations

Execute every installed validation in the item, then inspect the current state:

```bash
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

Test should report `Parcel.StatusMatches` and `Parcel.StatusIsKnown` as passed. The Test has `0 missing, 0 unexpected`; the Assumption has `0 violations`. Health should show Green Build, Load and Tests sections.

A failed validation did run: it found discrepancies or violating rows. A validation reported as unable to run did not produce a valid result and is not a pass.

## 7. Diagnose one deliberate failure

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
  --name Parcel.StatusMatches
```

The Test should fail for `P-1002` with one missing row (`In transit`) and one unexpected row (`Delivered`). The command exits non-zero, and Health records the Test section as Red until a later installed run passes.

Restore the complete passing Test from step 3, then install and run all validations again:

```bash
weaver check
weaver build
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

The item returns to Green. Editing the source without Build would leave Test running the previously installed definition. Exact validation and diagnostic behaviour is in the [Test operation reference](../reference/operation-behaviour/test.md).
