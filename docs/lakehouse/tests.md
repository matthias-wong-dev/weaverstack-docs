# Testing Lakehouse data

Check that CurrentStatus returns the expected parcels, and that every event uses a recognised status. These validations live beside the same Folder and Tables; Build installs them, and Test runs them separately from Load.

Continue from [Working with Spark SQL](spark-sql.md). For direct entry, the [Lakehouse document snapshot](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-lakehouse) lists the Python, SQL and validation checkpoints. Use the earlier project's bindings and matching published runtime; no new item or catalogue is needed.

## Compare CurrentStatus with an independent result

Create `Lakehouse/Landing/tests/Parcel.CurrentStatusMatches.sql`:

```sql
/*
Test ID: Parcel.CurrentStatusMatches

Description: Current statuses match the carrier export's expected latest events.

Primary key: Parcel ID
*/
select *
from values
    ('P-1001', 'In transit', 'Central'),
    ('P-1002', 'Delivered', 'South')
as expected(`Parcel ID`, `Status`, `Depot`);

select `Parcel ID`, `Status`, `Depot`
from Parcel.CurrentStatus;
```

The first query is the expected result from the small carrier export; the second reads the installed Table. It does not repeat CurrentStatus's window calculation. Both return `Parcel ID`, `Status` and `Depot` in the same order. `Primary key` pairs diagnostic rows for a parcel; it does not change the comparison.

## Find unknown event statuses

Create `Lakehouse/Landing/assumptions/Parcel.EventStatusIsKnown.sql`:

```sql
/*
Assumption ID: Parcel.EventStatusIsKnown

Description: Every parcel event has a recognised status.
*/
select `Parcel ID`, `Event sequence`, `Status`
from Parcel.Event
where `Status` is null
   or `Status` not in ('Accepted', 'In transit', 'Delivered');
```

An Assumption returns the rows that contradict its statement. This one passes only when that query returns no rows. SQL validations infer their managed dependencies from relation references; unlike Spark SQL Tables, they do not require an explicit `Dependencies` field.

## Run both validations

From the same project root:

```bash
weaver check
weaver build --item Lakehouse/Landing
weaver load Lakehouse/Landing --stale
weaver test Lakehouse/Landing
weaver health --item Lakehouse/Landing
```

Check should accept both documents. Build installs them but does not evaluate them. The stale Load catches up any data work made stale by Build; Test does not load its dependencies for you. With the original export, Test should record `Succeeded` for both validations, with zero missing/unexpected rows and zero assumption violations. Inspect the Test section of Health rather than treating a successful Load as a quality result.

To run these source files before installing a validation edit:

```bash
weaver test Lakehouse/Landing \
  --file Lakehouse/Landing/tests/Parcel.CurrentStatusMatches.sql \
  --file Lakehouse/Landing/assumptions/Parcel.EventStatusIsKnown.sql
```

File mode reads the deployed Tables but records no catalogue Test state. Use the installed-mode command above when you want Health to reflect the result.

## Diagnose one mismatch

In the Test's expected query only, change P-1001's status from `In transit` to `Delivered`. Leave the Folder, Event and CurrentStatus unchanged. Check and Build the validation edit, then select that installed Test with a whole-name regex:

```bash
weaver check
weaver build --item Lakehouse/Landing
weaver test Lakehouse/Landing --name '^Parcel\.CurrentStatusMatches$'
weaver health --item Lakehouse/Landing
```

The selected Test should fail and return diagnostic rows showing the expected `Delivered` and actual `In transit`. Health should show the failed validation. There is no Load here because the data declarations and their intended data have not changed. Restore the expected value, Check and Build again, then rerun the selected Test; it should succeed.

The small fixed export made the expected rows explicit. A changing carrier feed needs processing state as well as tests: [Loading changes and bookmarks](incremental.md) shows a complete mutable-source variation, where updating or removing a file changes CurrentStatus without rebuilding its code.

[Tests](../reference/weaver-documents/test.md), [Assumptions](../reference/weaver-documents/assumption.md) and [Test behaviour](../reference/operation-behaviour/test.md) own the exact comparison, diagnostic and recording rules. Python validations use the same data: a `Test` implements `expected()` and `actual()` returning Spark DataFrames, while an `Assumption` implements `read()` returning violations; their complete forms are in those references.
