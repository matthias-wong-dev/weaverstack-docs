# `weaver doctor`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver doctor [-h] [--json] --workspace WORKSPACE [--non-interactive]
```

## Options

`-h, --help`
: show this help message and exit

`--json`
: Emit the result as JSON.

`--workspace WORKSPACE`
: Fabric workspace to check.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->

## Responsibility and selection

Probe authentication and Microsoft Fabric connectivity for the workspace named by `--workspace`. Doctor does not read project or workspace configuration.

The probe checks authentication and Fabric REST access. When the workspace contains applicable items, it also checks OneLake through a Lakehouse, TDS through a Warehouse, and Livy through a Lakehouse. An absent item is reported as not tested rather than as a failed endpoint.

## Execution

The command resolves the named workspace and runs the applicable probes. A Lakehouse probe starts a Fabric Spark session and can take about a minute.

## Interaction

Interactive credential selection may fall back from Azure CLI credentials to browser sign-in. `--non-interactive` prevents browser sign-in and other prompts.

## Output and exit behaviour

Human output lists each check with `OK`, `NOT TESTED`, `FAILED`, or `ERROR`, plus available details. Authentication output includes only recognised identity fields.

`--json` emits the current complete doctor report as one JSON document. Its fields are not presented here as a compatibility contract.

The command exits `0` when every applicable check passes. A missing workspace, failed check, or probe error exits `1`. Argument errors exit through `argparse`.

## Examples

```bash
weaver doctor --workspace "Parcel Development"
```

For unattended diagnostics:

```bash
weaver doctor \
  --workspace "Parcel Development" \
  --non-interactive \
  --json
```
