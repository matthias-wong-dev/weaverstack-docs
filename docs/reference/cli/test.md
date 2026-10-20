# `weaver test`

Run Lakehouse Python/Spark SQL, Warehouse SQL and semantic-model DAX validations through one Test operation. Installed results share the catalogue and appear together in Health.

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver test [-h] [--item ITEM] [--name PATTERN] [--file PATH] [--source SOURCE] [--concurrency N] [--dry-run] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [ITEM ...]
```

## Positional arguments

`ITEM`
: Weaver items to validate, as Lakehouse/Name, Warehouse/Name or SemanticModel/Name. PowerBI or PowerBI/<project> names the semantic models of the project folder. Naming none validates every item.

## Options

`-h, --help`
: show this help message and exit

`--item ITEM`
: Legacy spelling for a positional Weaver item.

`--name PATTERN`
: Run only validations whose whole Schema.Object matches this regular expression, with their diagnostic rows. Repeat to select more.

`--file PATH`
: Run validations from source in file mode: a file, a directory or a glob. A file outside the project folder runs against the one item named. Repeat to select more.

`--source SOURCE`
: Project folder, or an abfss location inside a Fabric session. Defaults to the current directory or Notebook Resources.

`--concurrency N`
: Limit total simultaneous execution for this invocation; retain resource limits.

`--dry-run`
: Show the test plan without running it.

`--json`
: Emit the report as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

<!-- END GENERATED CLI -->

## Responsibility and selection

Test evaluates Tests/Assumptions and returns a report. Positional/legacy items define scope. With a catalogue and no files it uses installed definitions. `--file` selects source/file mode even with a catalogue; without a catalogue Test reads project validations. Source/file mode records no installed TestStatus/Log. Reports cannot Test; validate their model.

Repeat `--name` for whole-name case-insensitive regex filtering; every pattern must match. Repeat `--file` for source files, project directories or quoted glob patterns. The selectors can be combined. Project-declared files keep their owners; an external single file requires exactly one named item. `--source` supplies project context (default current directory/Notebook Resources); it alone does not force file mode when a catalogue exists. PowerBI/project selectors expand semantic models.

Supported source forms include Warehouse SQL, Lakehouse Python/Spark SQL and model-owned DAX. DAX reconciliation still requires its Expected Lakehouse/Warehouse and query permissions. Name/file-targeted runs collect diagnostics; item-wide runs normally report counts. `--dry-run` parses/resolves without evaluating queries or recording state.

## Execution and outcomes

Validations are independent: findings and node evaluation errors do not prevent later selected validations. Installed runs use configured resource limits. Source/file mode is serial by default; explicit `--concurrency N` uses scheduled execution with a total cap alongside resource ceilings. It does not Load data dependencies or refresh a model first.

No edit-and-retry loop is offered. Non-interactive mode disables prompts/browser sign-in. Human output/JSON distinguish `passed`, `failed`, `invalid`, `planned`, with missing/unexpected Test counts, Assumption violations and available diagnostic rows. Python returns completed reports including findings; `weaver.test` has no strict-mode argument. CLI exits `0` for passed/planned, `1` for failed/invalid or command error, `2` for parser usage errors.

## Examples

```bash
weaver test Warehouse/Operations --name 'Parcel[.]StatusMatches' --workspace-config workspace-dev.yml
weaver test Warehouse/Operations --file Warehouse/Operations/tests --source . --concurrency 2 --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --source . --workspace-config workspace-dev.yml
```

The last command uses file mode only when that configuration has no catalogue; with a catalogue it selects installed validations. Add `--file PowerBI/Parcel/assumptions/Parcel` to explicitly choose source mode.

See [Test behaviour](../operation-behaviour/test.md), [DAX validations](../power-bi/validations.md) and [machine output](../machine-readable-output.md).

## Validate source data and semantic models together

With the source and model validations installed:

```bash
weaver test --workspace-config workspace-config.yml
```

The same report contains Lakehouse/Warehouse validations and model-owned DAX validations. A DAX Test can compare a measure with SQL calculated independently over its managed source. To inspect one model, select `SemanticModel/Parcel`; Reports have no separate Test. See [Validate a semantic model](../../semantic-models/validation.md) and [Compare DAX with source SQL](../../semantic-models/validation.md#compare-dax-with-source-sql).
