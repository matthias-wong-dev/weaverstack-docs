# Test behaviour

Test evaluates Tests and Assumptions. Installed runs use catalogue definitions; file runs compile and execute one source validation without installing it.

## Selection

Logical items may be positional or use the repeatable legacy `--item` option. Naming none selects every installed item; naming an uninstalled item is an error. See [Shared selection and identity](shared-selection-and-identity.md) for item and validation-name forms.

An installed item-wide run selects every installed Test and Assumption owned by those items. Their data dependencies identify what they inspect; they do not add data objects, validations or other items. Validations run independently in stable logical-identity order rather than dependency order, so one failure or execution error does not stop the rest.

`--name Schema.Object` selects one installed Test or Assumption inside the item boundary. It names the logical validation, not its generated procedure or module. If that name occurs in more than one selected item, restrict the request to one item. A named run executes the validation once and returns its diagnostic rows; an item-wide run requests counts without collecting those rows.

`--file PATH` is mutually exclusive with `--name` and requires exactly one installed item to supply the physical target and dialect. The file must declare a SQL Test or Assumption valid for that target. Python source files are rejected; import the class and call its validation interface instead. A file run does not replace or publish an installed validation.

## Planning and host requirements

Installed planning reads the catalogue before acquiring target execution capabilities. A declared validation whose generated procedure or module is absent is selected but becomes `invalid` when it cannot run; it is not treated as a pass.

Warehouse validation executes over TDS and does not require a Fabric Environment. A non-dry-run Lakehouse validation started from a desktop requires a configured Fabric Environment with Weaver installed; this check occurs after item bindings are read and before dispatch. Inside a Fabric session, Test uses that session. Dry runs require no Environment.

A source-file run parses and compiles the file before reporting or dispatch. Warehouse SQL runs as a generated batch without leaving a procedure behind. Lakehouse file mode accepts Spark SQL and runs it through the same comparison path as installed validation; it does not accept Python source.

## Validation semantics

A Test compares expected and actual relations:

- `missing_count` is rows present on the expected side and absent or different on the actual side;
- `unexpected_count` is rows present on the actual side and absent or different on the expected side; and
- the Test passes only when both counts are zero.

An optional primary key correlates diagnostic rows between the two sides; it does not change the pass rule.

An Assumption returns rows that violate one condition. It passes when `violation_count` is zero and fails when it is non-zero. It has no expected/actual pair and cannot declare a primary key.

A validation that cannot be evaluated is `invalid`, not a failed data finding and not a zero-count pass. The report retains the execution error.

## Dry run

`--dry-run` resolves installed validations without dispatching them. File dry-run still reads, parses and compiles the selected file. A resolved node is `planned` with `executed` false; a report containing planned nodes exits successfully.

Dry runs do not create Log or TestStatus records and do not collect diagnostics. A planning or compilation error is a command error rather than a fabricated planned node.

## Outcomes, reports and process status

Each validation is:

- `passed` — it ran and found no discrepancy or violation;
- `failed` — it ran and found discrepancy or violation rows;
- `invalid` — it could not be evaluated; or
- `planned` — dry-run resolution completed without execution.

The run takes the worst selected outcome: `invalid` outranks `failed`, which outranks `passed`; an all-planned run is `planned`. An empty installed selection is `passed`. Counts aggregate Tests and Assumptions separately.

The Python operation returns failed and invalid reports by default. `strict=True` raises `ValidationError` only after all selected validations have run and the completed report has been assembled; the exception carries the report. The CLI uses strict mode, renders that report, and exits `1` for `failed`, `invalid` or command errors. `passed` and `planned` exit `0`.

Diagnostic rows are collected only for `--name` and `--file`. They remain on the local report object and targeted CLI output; they are excluded from the ordinary durable/transported report mapping. No compatibility guarantee is made for the current JSON shape.

## Current state, history and reruns

An executed installed run appends one Log row and updates current TestStatus for every selected validation, then flushes those writes before returning or raising strict failure. TestStatus records the validation kind, result, workflow and available failure count. A failed Test records missing plus unexpected rows; a failed Assumption records violations; an invalid validation records an error without presenting a failure count.

Build sets rebuilt validations to pending. Health reports a never-rerun validation or a previously passing validation whose managed data dependency was established later as Amber. Test has no stale-selection mode: item-wide and named runs execute what was selected regardless of current Green, Amber or Red state. A rerun replaces current TestStatus for reached validations and appends new history; untouched validations retain their earlier current state.

File and dry-run invocations write no installed TestStatus or Log evidence. Test publishes no definitions or certification.

Test does not provide a transaction across validations or rollback authored side effects. If validation SQL or Python changes external state before failing, Test does not undo that work; it still records the installed validation outcome when recording succeeds. A catalogue flush failure is an operation failure and may follow completed validation execution.

See [`weaver test`](../cli/test.md), [Test documents](../weaver-documents/test.md), [Assumption documents](../weaver-documents/assumption.md), [Health](health.md), and [Catalogue schema](../catalogue-schema.md).
