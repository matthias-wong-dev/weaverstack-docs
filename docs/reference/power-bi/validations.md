# DAX Tests and Assumptions

A semantic-model Assumption returns violating DAX rows. A semantic-model Test compares DAX actual rows with SQL expected rows from a supported Warehouse or Lakehouse. Both are model-owned validation documents, separate from the deployed model definition.

## Location and body

Use `PowerBI/<project>/assumptions/<Model>/<Schema.Object>.dax` or `tests/<Model>/<Schema.Object>.dax`. The model must be an exact local definition; filename, metadata identity and directory kind must agree. Variants own their validations and do not inherit a base model's validations.

Start with a native block-comment YAML header. After it the body must be a DAX query beginning with `EVALUATE` or `DEFINE` (comments and whitespace may precede it).

```dax
/*
Assumption ID: Parcel.PositiveCount
Description: Delivery count is not negative.
*/
EVALUATE
FILTER(ROW("Delivery count", [Delivery count]), [Delivery count] < 0)
```

This file's location is `PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveCount.dax` and assumes an existing `[Delivery count]` measure. Zero result rows pass; non-zero rows are findings, not a service-execution failure.

## Metadata

| Key | Required/default | Accepted form and meaning |
| --- | --- | --- |
| `Test ID` / `Assumption ID` | exactly one required | `Schema.Object`, equal to the filename; correct directory kind |
| `Description` | required/non-empty | Text or supported description reference; see [common metadata](../weaver-documents/common-metadata.md) |
| `Notes` | optional/empty | Non-empty free text |
| `Revision notes` | optional/empty | Non-empty dated YAML note list |
| `Dependencies` | optional/inferred | List of `Schema.Object` reads in the Expected source for a Test; explicit list replaces inference, `[]` declares none |
| `Primary key` | optional/empty, Test only | Comma-separated column names correlating discrepancy diagnostics |
| `Expected source` | required for DAX Test | `Warehouse/<item>` or `Lakehouse/<item>`; no arbitrary external database type |
| `Expected SQL` | required for DAX Test | Non-empty SQL text producing exactly one expected relation in that source's dialect |

An Assumption has no Expected side and must not declare `Primary key`, `Expected source` or `Expected SQL`. A DAX Assumption reads its owning model; non-empty explicit `Dependencies` are refused. Data-object metadata such as `Schema`, `Incremental`, `Static`, stability thresholds or load controls does not apply. Unknown/duplicate keys fail.

```dax
/*
Test ID: Parcel.CountMatches
Description: Delivery count agrees with the operations Warehouse.
Expected source: Warehouse/Operations
Expected SQL: |-
  SELECT COUNT(*) AS [Delivery count] FROM Parcel.Deliveries;
*/
EVALUATE ROW("Delivery count", [Delivery count])
```

This Test belongs under `PowerBI/Parcel/tests/Parcel/Parcel.CountMatches.dax`. Expected reads resolve in `Warehouse/Operations`. If that source is in the project, references must name its declared objects; cross-item physical spellings in Expected SQL do not create a different source. Warehouse uses T-SQL over TDS; Lakehouse uses addressed Spark SQL. Validation queries do not automatically Load sources or refresh models first.

## Comparison

The two sides are sets of rows compared by column position. Both must supply column metadata and the same number of columns. DAX labels such as `Table[Column]` or `[Measure]` normalize to their bracketed column name; duplicate normalized names fail. Diagnostics use expected-side names. Order projected columns deliberately; matching label text alone does not reorder values.

Numeric values compare by value, text exactly, dates as midnight datetimes and zoned datetimes in UTC. Duplicate rows are collapsed for set comparison. A primary key does not change the pass rule, but must be present at matching positions on both sides and uniquely identify populated rows; null/blank or duplicate keys invalidate the comparison. `_weaver_side` and `_weaver_sk` are reserved diagnostic column names and are refused. If the two sides return the same set of column names in different orders, the comparison refuses the reordered shape rather than silently realigning it. A Test result with no column metadata is invalid, including an empty DAX/SQL result that transports no schema; it is not silently passed.

A Test passes only when `missing_count` and `unexpected_count` are both zero. Expected-only/different rows count as missing; actual-only/different rows count as unexpected. An Assumption passes only when `violation_count` is zero. Query, permission, shape, key and definition-version errors are `invalid`, not zero-count passes.

## File and catalogue modes

```bash
weaver test SemanticModel/Parcel --source . --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --file PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveCount.dax --source . --workspace-config workspace-dev.yml
```

Without a catalogue Test reads project validations and records no Weaver history. Supplying `--file` also selects source/file mode when a catalogue is configured. Project files run against their owning models; configured `targets` supplies physical names, otherwise the logical name is used. Directories and quoted glob patterns can select several files. External single files require exactly one named item. `--name` is repeatable case-insensitive whole-name regex filtering and may filter file selections too. Every supplied pattern must match.

With a catalogue and no `--file`, Test runs installed validation definitions against recorded targets, writes TestStatus/Log and does not reread edited files. `--source` supplies project context for Power BI selectors; it does not itself force source mode. Build the model again to install a changed validation. Source/file mode still needs the Expected source and permissions for a reconciliation Test; it removes recording, not remote dependencies.

Targeted name/file runs collect diagnostic rows; item-wide runs normally collect counts. All completed runs return a Python report, including findings and invalid outcomes. Inspect `succeeded`, `status` and nodes. The CLI returns `1` for failed/invalid results, `0` for passed/planned; no `strict=True` parameter is supported by `weaver.test`.

A dry run parses/resolves without dispatching DAX/SQL or writing Log/TestStatus. It does not prove query permissions or deployed data correctness. See [Test behaviour](../operation-behaviour/test.md), [mode requirements](requirements-and-compatibility.md) and [machine output](../machine-readable-output.md).
