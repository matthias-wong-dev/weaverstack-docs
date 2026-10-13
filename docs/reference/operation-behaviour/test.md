# Test behaviour

Test evaluates Tests and Assumptions. Installed runs use catalogue definitions; source/file runs parse and execute selected source validations without installing or recording them. This includes model-owned DAX and Python validation documents, not only one SQL file.

## Selection

Logical items may be positional or use the repeatable legacy `--item` option. Naming none selects every installed item; naming an uninstalled item is an error. See [Shared selection and identity](shared-selection-and-identity.md) for item and validation-name forms.

An installed item-wide run selects every installed Test and Assumption owned by those items. Their data dependencies identify what they inspect; they do not add data objects, validations or other items. Validations are independent, not a data dependency pipeline; findings and node evaluation errors do not stop the rest. Installed runs use configured run-resource limits. Source/file mode is serial by default and uses scheduled execution when `--concurrency N` is supplied; that total cap and resource limits both apply.

Repeatable `--name` values are case-insensitive whole-name regular expressions over `Schema.Object`; every pattern must match. Matches are deduplicated and refer to logical validations, not procedures/modules. Several matching items can contribute validations. Targeted matches collect diagnostic rows; item-wide runs normally collect counts.

Repeatable `--file` selects files, directories or quoted glob patterns and forces source/file mode. `--name` may filter those files. Project-declared files retain their owning items; external single files require exactly one named item. Selected files must belong within any explicit item boundary. Warehouse SQL, Lakehouse Python/Spark SQL and semantic DAX are supported according to item/dialect rules. No catalogue is needed for source/file mode: physical names resolve from configured targets or logical names. `--source` supplies the project folder (current directory/Notebook Resources by default); without a catalogue all selected project validations run in file mode. With a catalogue, `--source` alone does not override installed mode.

## Planning and host requirements

Installed planning reads the catalogue before acquiring target execution capabilities. A declared validation whose generated procedure or module is absent is selected but becomes `invalid` when it cannot run; it is not treated as a pass.

Warehouse validation executes over TDS and does not require a Fabric Environment. A non-dry-run Lakehouse validation started from a desktop requires a configured Fabric Environment with Weaver installed; this check occurs after item bindings are read and before dispatch. Inside a Fabric session, Test uses that session. Dry runs require no Environment.

A source/file run parses the project/selected files before dispatch. Warehouse SQL runs as a generated batch without leaving a procedure behind; Lakehouse source mode also supports Python validation classes. Semantic DAX Assumptions query the model; DAX Tests also read their supported Expected Warehouse/Lakehouse. Those sources and permissions remain required in file mode. See [DAX validations](../power-bi/validations.md).

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

The Python operation returns completed failed/invalid reports as well as passing ones; inspect `succeeded`, `status` and node errors. No `strict` parameter is supported. Planning, configuration or required catalogue-write failures still raise. The CLI renders the returned report and exits `1` for failed/invalid outcomes or command errors; `passed` and `planned` exit `0`.

Diagnostic rows are collected only for `--name` and `--file`. They remain on the local report object and targeted CLI output; they are excluded from the ordinary durable/transported report mapping. No compatibility guarantee is made for the current JSON shape.

## Current state, history and reruns

An executed installed run appends one Log row and updates current TestStatus for every selected validation, then flushes those writes before returning. TestStatus records the validation kind, result, workflow and available failure count. A failed Test records missing plus unexpected rows; a failed Assumption records violations; an invalid validation records an error without presenting a failure count.

Build sets rebuilt validations to pending. Health reports a never-rerun validation or a previously passing validation whose managed data dependency was established later as Amber. Test has no stale-selection mode: item-wide and named runs execute what was selected regardless of current Green, Amber or Red state. A rerun replaces current TestStatus for reached validations and appends new history; untouched validations retain their earlier current state.

Source/file and dry-run invocations write no installed TestStatus or Log evidence. Test publishes no definitions or certification.

Test does not provide a transaction across validations or rollback authored side effects. If validation SQL or Python changes external state before failing, Test does not undo that work; it still records the installed validation outcome when recording succeeds. A catalogue flush failure is an operation failure and may follow completed validation execution.

See [`weaver test`](../cli/test.md), [Test documents](../weaver-documents/test.md), [Assumption documents](../weaver-documents/assumption.md), [Health](health.md), and [Catalogue schema](../catalogue-schema.md).
