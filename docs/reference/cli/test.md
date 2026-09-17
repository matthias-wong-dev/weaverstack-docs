# `weaver test`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver test [-h] [--item ITEM] [--name Schema.Object | --file PATH] [--dry-run] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [ITEM ...]
```

## Positional arguments

`ITEM`
: Weaver items to validate, as Lakehouse/Name or Warehouse/Name. Naming none validates every installed item.

## Options

`-h, --help`
: show this help message and exit

`--item ITEM`
: Legacy spelling for a positional Weaver item.

`--name Schema.Object`
: Run one installed validation and return diagnostic rows.

`--file PATH`
: Compile and run a source file without installing it.

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

Run installed Tests and Assumptions for selected logical items. Positional items use `Lakehouse/Name` or `Warehouse/Name`; naming none selects every installed item. The repeatable `--item` spelling is retained for existing invocations, and its values follow positional values in the request.

`--name Schema.Object` runs one installed validation. `--file PATH` compiles and runs one source validation without installing it and requires exactly one item. The two selectors are mutually exclusive. Targeted runs collect diagnostic rows; item-wide runs report validation results and counts without diagnostic rows.

## Execution

An installed run reads bindings and validations from the catalogue. Validations are independent, so one finding does not block the remaining selected validations. A source-file run publishes no validation evidence to the installed estate.

`--dry-run` returns the test plan without executing validations.

## Interaction

Test does not offer an edit-and-retry loop. Interactive credential selection may use browser sign-in; `--non-interactive` prevents browser sign-in and other prompts.

## Output and exit behaviour

Human output lists each validation with its status, kind and logical identity. Failed Tests include missing and unexpected counts; failed Assumptions include violation counts. Targeted runs print collected diagnostic rows. The summary reports passed, failed and validations that could not run.

`--json` emits the current report as one document. Targeted JSON includes collected diagnostic rows. Its fields are not presented here as a compatibility contract.

The command exits `0` when all selected validations pass and `1` when a validation fails, cannot run, or the request fails. Argument errors exit through `argparse`.

## Examples

Run all installed validations:

```bash
weaver test --workspace-config workspace-config.yml
```

Run one installed validation and return its diagnostic rows:

```bash
weaver test Warehouse/Operations \
  --name Parcel.StatusMatches \
  --workspace-config workspace-config.yml
```

Compile and run one source validation:

```bash
weaver test Warehouse/Operations \
  --file Warehouse/Operations/tests/Parcel.StatusMatches.sql \
  --workspace-config workspace-config.yml
```
