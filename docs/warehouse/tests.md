# Testing Warehouse data

The [first Table and View](first-project.md) produce two current parcel statuses from three events. Keep that project and add two SQL validations: a Test compares the View with an independent expected result, and an Assumption finds events whose status is unknown.

Start from its loaded `Warehouse/Operations` checkpoint. For direct entry, use the [complete journey snapshot](https://github.com/matthias-wong-dev/weaverstack-docs/tree/main/examples/parcel-warehouse-journey) and follow the first page's setup, Build and Load once. It contains the same `Parcel.StatusEvent` Table and `Parcel.CurrentStatus` View, with both passing validations below. Run all commands from the project root.

## Check the result without repeating the ranking query

Create `Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql`:

```sql
/*
Test ID: Parcel.CurrentStatusMatches

Description: Latest parcel status matches the independently expected rows.

Primary key: Parcel ID
*/
select v.[Parcel ID]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 'In transit', 'Central'),
    ('P-1002', 'Delivered', 'South')
) as v ([Parcel ID], [Status], [Depot]);

select [Parcel ID]
     , [Status]
     , [Depot]
from [Parcel].[CurrentStatus];
```

The first result is expected; the second is actual. The expected rows state what the sample events mean instead of repeating the View's window function. A defect in that function can therefore produce a discrepancy.

A row only in expected is missing; a row only in actual is unexpected. A changed row produces one of each. The optional `Primary key` correlates the diagnostic rows without changing that comparison. The actual query establishes the dependency on `Parcel.CurrentStatus`.

## Find events outside the accepted vocabulary

Create `Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql`:

```sql
/*
Assumption ID: Parcel.StatusIsKnown

Description: Every recorded parcel event has a recognised status.
*/
select [Parcel ID]
     , [Event sequence]
     , [Status]
from [Parcel].[StatusEvent]
where [Status] is null
   or [Status] not in ('Accepted', 'In transit', 'Delivered');
```

Every returned row violates the description. No returned rows means the Assumption passes. This check reads all events, including those hidden by the latest-status View, and its relation reference establishes the dependency on `Parcel.StatusEvent`.

## Install and run the validations

```bash
weaver check
weaver build --item Warehouse/Operations
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

Build installs the new validations; it does not execute them. With the Table and View source unchanged, this addition does not require another data Load. Test should report `Parcel.CurrentStatusMatches` as passed with `0 missing, 0 unexpected`, and `Parcel.StatusIsKnown` as passed with `0 violations`. Health should show Green Build, Load and Tests sections.

A failed validation ran and found a discrepancy or violation. An unable-to-run result is neither a finding nor a pass. [Test behaviour](../reference/operation-behaviour/test.md) owns the exact outcome and recording rules.

## Make one discrepancy visible

Replace `Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql` with this complete version. It deliberately expects the wrong status for `P-1002`:

```sql
/*
Test ID: Parcel.CurrentStatusMatches

Description: Latest parcel status matches the independently expected rows.

Primary key: Parcel ID
*/
select v.[Parcel ID]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 'In transit', 'Central'),
    ('P-1002', 'In transit', 'South')
) as v ([Parcel ID], [Status], [Depot]);

select [Parcel ID]
     , [Status]
     , [Depot]
from [Parcel].[CurrentStatus];
```

Install the edited Test and select it for diagnostics:

```bash
weaver check
weaver build --item Warehouse/Operations
weaver test Warehouse/Operations --name 'Parcel[.]CurrentStatusMatches'
weaver health --item Warehouse/Operations
```

The expected finding is one missing row (`P-1002`, `In transit`, `South`) and one unexpected row (`P-1002`, `Delivered`, `South`). Test exits non-zero; Health records Tests as Red. The selector is a case-insensitive whole-name regular expression, so `[.]` matches the literal dot.

Restore the passing Test shown above, then install and rerun it:

```bash
weaver check
weaver build --item Warehouse/Operations
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

Both validations should pass and the item should return to Green.

To try edited SQL against deployed data before installing it, use file mode:

```bash
weaver test Warehouse/Operations --source . --file 'Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql'
```

`--file` selects file mode even with a catalogue configured. It records no installed Test status or history; `--source` alone does not select file mode. [Test CLI](../reference/cli/test.md) covers repeatable file and name selectors. [Test](../reference/weaver-documents/test.md) and [Assumption](../reference/weaver-documents/assumption.md) define the complete SQL forms.

These checks now describe the result you expect, but the event feed is still a constant in a SQL file. [Loading changes](incremental.md) uses a complete mutable-source variation: the same parcels arrive through an external Warehouse, and a keyed Table consumes updates and cancellations without rebuilding its definition.
