# Test contract

Test evaluates Weaver Tests and Assumptions against an installed item. It normally runs installed validation definitions from the catalogue; a targeted source-file run compiles and evaluates one uninstalled validation without publishing it.

## Installed selection

An installed run selects logical items as `Lakehouse/Name` or `Warehouse/Name`:

```bash
weaver test Warehouse/Operations
weaver test Lakehouse/Landing --name Parcel.EventKeys
weaver test
```

Naming no item selects every item recorded in `_.Installation`. Naming an uninstalled item is an error. Item selection includes installed Tests and Assumptions owned by those items; data dependencies identify what each validation reads but do not add data objects, validations or other items to the run.

Without `--name`, selected validations run in stable logical-identity order. They are independent: one failed or invalid validation does not stop the others.

`--name Schema.Object` selects one installed Test or Assumption inside the item boundary. The identity is the authored validation name, not the name of its installed executable. A targeted installed run returns the diagnostic rows produced by that validation; an item-wide run returns counts but does not collect diagnostic rows.

## Source-file selection

`--file PATH` compiles and runs one source Test or Assumption without installing it:

```bash
weaver test Warehouse/Operations \
  --file Warehouse/Operations/tests/Parcel.StatusMatches.sql
```

A file run requires exactly one installed item to supply the target and dialect. The file must be a supported Test or Assumption declaration for that item. `--file` and `--name` are mutually exclusive.

A source-file run does not replace the installed validation, update `_.TestStatus` or append installed-estate validation evidence. It returns diagnostic rows for the invocation itself. The source path is a test selector only; other lifecycle operations continue to use installed definitions.

## Test and Assumption results

A Test compares expected and actual relations. It passes when both discrepancy counts are zero and fails with separate missing and unexpected counts otherwise. A Test may declare a primary key to correlate its two sides.

An Assumption identifies rows that contradict a condition. It passes when its violation count is zero and fails when the count is non-zero. An Assumption has no expected/actual pair and cannot declare a primary key.

A validation that cannot be evaluated is `invalid`, not passed and not a failed data finding. Its report carries the execution error rather than presenting zero discrepancies or violations.

## Dry runs

`--dry-run` resolves installed validations without executing them. A source-file dry run still reads and compiles the declaration but does not execute it on the target. Every valid selected validation is `planned` and has `executed` set to false.

A report containing only planned validations is successful. Dry runs do not create `_.Log` or `_.TestStatus` records.

## Outcomes and strict mode

Each validation is:

- `passed` — it ran and found no discrepancies or violations;
- `failed` — it ran and found discrepancies or violations;
- `invalid` — it could not be evaluated;
- `planned` — a dry run resolved it without execution.

The run status is the worst selected outcome: `invalid` takes precedence over `failed`, which takes precedence over `passed`; a dry run is `planned`. The report aggregates passed, failed and invalid counts plus Test discrepancy and Assumption violation counts.

The Python operation returns failed and invalid reports by default. With `strict=True`, it raises `ValidationError` after the completed report has been assembled; the exception carries that report. The CLI uses strict mode, renders the report and exits non-zero for failed or invalid outcomes. Passing and planned reports exit zero.

Strict mode changes how an unsuccessful report reaches the caller. It does not stop remaining validations, discard their outcomes or change validation semantics.

## Catalogue recording

An executed installed run appends one `_.Log` record and updates `_.TestStatus` for every selected validation. The current status records whether the declaration was a Test or Assumption, its result, its failure count where one exists and the workflow identifier.

A failed Test records total missing and unexpected rows. A failed Assumption records violations. An invalid validation records an error with no failure count. Diagnostic rows are returned only for a targeted invocation and are not written as catalogue evidence or included in the durable report representation.

Weaver flushes installed validation records before returning or raising for strict mode. Source-file and dry-run invocations write no installed validation state.

## Defined behaviour

The Test contract specifies that Test:

1. selects installed Tests and Assumptions inside the logical item boundary;
2. does not expand selection through inspected-data dependencies;
3. runs all selected installed validations independently in stable identity order;
4. distinguishes installed name selection from uninstalled source-file execution;
5. applies the separate Test discrepancy and Assumption violation semantics;
6. reports inability to evaluate as `invalid`, not as a passing zero count;
7. lets strict mode raise only after preserving the completed report;
8. records every executed installed validation before reporting completion; and
9. keeps dry-run and source-file outcomes out of installed catalogue state.

See [`weaver test`](../cli/test.md), [Validation objects](../python/validation.md), and [Catalogue](../catalogue-schema.md).