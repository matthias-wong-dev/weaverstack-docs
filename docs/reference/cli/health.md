# `weaver health`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver health [-h] [--item ITEM] [--as-of DATETIME] [--no-inventory] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--catalogue CATALOGUE]
```

## Options

`-h, --help`
: show this help message and exit

`--item ITEM`
: Weaver item to report on, as Lakehouse/Name or Warehouse/Name. Repeat to select more than one. Naming none reports on the whole installed estate.

`--as-of DATETIME`
: ISO-8601 instant with a zone. A load settled before it reads as stale. Defaults to 24 hours ago.

`--no-inventory`
: Skip the physical inventory check for certified objects.

`--json`
: Emit the report as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

<!-- END GENERATED CLI -->

## Responsibility and selection

Report load, test and build health for the installed estate. Repeat `--item` with `Lakehouse/Name` or `Warehouse/Name` to restrict the report; naming none selects the whole installed estate.

`--as-of` sets the load freshness threshold and must be an ISO-8601 instant with a time zone. It defaults to 24 hours before the report. `--no-inventory` skips checking certified objects against physical inventory.

## Execution

Health reads the catalogue and, unless disabled, physical inventory. It runs no authored code and accepts no Environment option. Lakehouse inventory uses OneLake rather than a Spark session.

The report assesses load freshness and outcomes, validation outcomes, and consistency between installed catalogue state and physical inventory.

## Interaction

Health does not prompt for report choices. Interactive credential selection may use browser sign-in; `--non-interactive` prevents browser sign-in and other prompts.

## Output and exit behaviour

Human output gives the overall `Green`, `Amber`, or `Red` verdict, then load, test and build sections with counts and findings. It can also show recent load activity and slowest loads. Plain redirected output does not depend on terminal colour for meaning.

`--json` emits the current complete health report as one JSON document. The current payload carries its own format version, but this page does not declare compatibility between format versions.

The command exits `0` only for a Green report. Amber, Red, or a command error exits `1`. Argument errors exit through `argparse`.

## Examples

```bash
weaver health --workspace-config workspace-config.yml
```

Check selected items at a fixed freshness threshold without inventory reads:

```bash
weaver health \
  --item Lakehouse/Landing \
  --item Warehouse/Operations \
  --as-of 2026-09-05T00:00:00Z \
  --no-inventory \
  --workspace-config workspace-config.yml
```
