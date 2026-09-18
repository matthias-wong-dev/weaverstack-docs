# Validate an installed estate

This guide adds one Test and one Assumption to a Warehouse parcel pipeline. Build installs both validations; Test executes them against the installed data.

A Test asks whether expected and actual relations contain the same rows. An Assumption asks whether a query returns any violating rows. Neither validation populates business data.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Access to a Fabric workspace containing a catalogue Warehouse and a target Warehouse you can modify.
- A project root bound to the logical item `Warehouse/Operations`. The complete example is under `examples/parcel-validation/` in the documentation repository.

The example configuration in `workspace-config.yml` is:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue

targets:
  Warehouse/Operations: Operations_Dev
```

Replace the physical names for your workspace. The declarations below keep the logical item and validation identities independent of those names. See [Logical and physical items](../core-concepts/logical-and-physical-items.md) for that boundary.

## Create the parcel Table

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

This Table gives both validations a deterministic installed relation to read. Load must populate it before the validations can pass.

## Add a Test

Create `Warehouse/Operations/tests/Parcel.StatusMatches.sql`:

```sql
/*
Test ID: Parcel.StatusMatches

Description: Current parcel status matches the independently stated expected rows.

Primary key: Parcel ID

Dependencies:
  - Parcel.Status
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

A SQL Test ends with exactly two result queries:

1. the expected relation;
2. the actual relation.

The Test passes when their symmetric difference is empty. A row present only on the expected side is **missing**; a row present only on the actual side is **unexpected**. A changed row therefore contributes one row to each side of the difference.

`Primary key` is optional for a Test. It correlates expected and actual diagnostic rows when present; it does not change the discrepancy count. Key values must be populated and unique on each side for the Test to be evaluated.

`Dependencies` states that this validation reads `Parcel.Status`. A declared list replaces inferred SQL dependencies, so keep it complete. Dependencies place the validation after what it reads during installation and record the relationship in the catalogue; validations cannot themselves be dependency targets. See [Dependencies](../core-concepts/dependencies.md) for the operation-specific effects.

## Add an Assumption

Create `Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql`:

```sql
/*
Assumption ID: Parcel.StatusIsKnown

Description: Every parcel has a status recognised by this example.

Dependencies:
  - Parcel.Status
*/
select [Parcel ID]
     , [Status]
from [Parcel].[Status]
where [Status] is null
   or [Status] not in ('Accepted', 'In transit', 'Delivered');
```

An Assumption ends with one result query. Each returned row violates the stated condition, so this Assumption passes only when the query returns no rows. An Assumption has no Test primary key because it has one relation rather than two sides to correlate.

The paths `tests/` and `assumptions/` identify the validation kind. The filename and declared `Schema.Object` ID must agree. These files are [Weaver documents](../core-concepts/weaver-documents.md), not ad hoc SQL scripts.

## Check declarations locally

From the `parcel-validation` project root, run:

```bash
weaver check
```

A successful local check prints:

```text
Project valid.
```

This proves that Weaver parsed the documents, accepted each validation's result-query shape, matched paths and identities, and resolved the declared dependencies. It does not submit T-SQL, inspect `Operations_Dev`, install a validation or prove that either query returns the intended rows.

## Install and execute the validations

Apply the source and populate the Table before testing it:

```bash
weaver build --item Warehouse/Operations
weaver load Warehouse/Operations
weaver test Warehouse/Operations --dry-run
weaver test Warehouse/Operations
```

Build installs the Table's load work and the Test and Assumption validation procedures. It also publishes their declarations and dependencies to the configured [catalogue](../core-concepts/catalogue.md). Build does not execute either validation.

The Test dry run should list `Parcel.StatusIsKnown` and `Parcel.StatusMatches` as planned without executing them. The real Test run should report both as passed after the example Table loads its two rows. Test attempts every selected validation even if another fails.

For evidence about one validation, run it by installed name:

```bash
weaver test Warehouse/Operations \
  --name Parcel.StatusMatches
```

A named run returns diagnostic rows as well as counts. An item-wide run reports counts without collecting those rows. For this Test, failures report missing and unexpected counts; for the Assumption, failures report a violation count.

A **failed** validation ran and found discrepancies or violations. A validation that could not be evaluated is reported separately as **could not run**; it must not be interpreted as passing. Either outcome makes the CLI exit non-zero, while other selected validations are still attempted. [Fault tolerance](../core-concepts/fault-tolerance.md) places that behaviour in the wider operation model.

## Inspect the recorded outcome

Run:

```bash
weaver health --item Warehouse/Operations
```

After successful Build, Load and Test operations, Health should show Green Build, Load and Tests sections. For read-only investigation, the catalogue separates declaration from outcome:

- `_.TestDictionary` describes the installed Test and Assumption, including the Test's optional correlation key;
- `_.Dependency` records what each validation reads;
- `_.TestStatus` holds the current result and failure count;
- `_.Log` holds the settled work associated with the reported workflow identifier.

Do not edit those tables. Build and Test are their writers.

## Try a failure deliberately

Change `P-1002` in the Test's expected relation from `Delivered` to `In transit`, then run:

```bash
weaver check
weaver build --item Warehouse/Operations
weaver test Warehouse/Operations \
  --name Parcel.StatusMatches
```

The named Test should fail with one missing and one unexpected row for `P-1002`. Revert the expected value, then repeat Check, Build and Test. Editing only the source file is not enough: Test executes the generation last installed by Build. That distinction is the [Weaver operations](../core-concepts/build-load-and-test.md) lifecycle.

For exact command selection and source-file execution, see the [CLI reference](../reference/cli.md). `test --file` compiles and runs one SQL validation directly and does not install it or publish estate evidence; use the Build-and-Test path above for the normal project lifecycle. Continue with the [Development cycle](development-cycle.md) when the same declarations must be validated against a mirrored development estate.
