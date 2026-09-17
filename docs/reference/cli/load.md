# `weaver load`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver load [-h] [--item ITEM] [--name NAME] [--fault-tolerant] [--reload] [--stale] [--as-of DATETIME] [--dry-run] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [ITEM ...]
```

## Positional arguments

`ITEM`
: Weaver items to load, as Lakehouse/Name or Warehouse/Name. Naming none loads every installed item.

## Options

`-h, --help`
: show this help message and exit

`--item ITEM`
: Legacy spelling for a positional Weaver item.

`--name NAME`
: Load one installed object, as Tables/Schema.Object or Files/Schema.Object in a Lakehouse and Schema.Object in a Warehouse. A bare Schema.Object is accepted where it names one object. Repeat to select more than one.

`--fault-tolerant`
: Continue independent branches after a failure.

`--reload`
: Rebuild each selected table: reset its bookmark, empty it, then load. Does not affect unselected tables.

`--stale`
: Load only the objects whose load health is not green.

`--as-of DATETIME`
: ISO-8601 instant with a zone, used as the health freshness threshold when selecting objects. Defaults to 24 hours ago. Only valid with --stale.

`--dry-run`
: Show the load plan without running it.

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

Run installed loadable objects for selected logical items. Positional items use `Lakehouse/Name` or `Warehouse/Name`; naming none selects every installed item. The repeatable `--item` spelling is retained for existing invocations, and its values follow positional values in the request.

Repeat `--name` to bypass graph selection and run exact installed objects. In a Lakehouse use `Tables/Schema.Object` or `Files/Schema.Object`; a bare `Schema.Object` is accepted when it identifies one object. Warehouse names use `Schema.Object`.

`--stale` selects objects whose load health is not Green. `--as-of` must be an ISO-8601 instant with a time zone, is valid only with `--stale`, and defaults to 24 hours before the run. `--reload` and `--stale` cannot be combined.

## Execution

The normal run resolves installed bindings from the catalogue, plans dependency order, and executes selected load nodes. `--fault-tolerant` allows independent branches to continue after a failure; the final report still fails if any selected work fails.

`--reload` resets the bookmark and empties each selected table before loading it. It does not affect unselected tables. `--dry-run` returns the selected plan without executing it.

## Interaction

After a load error in an interactive terminal, Weaver can offer to retry while keeping the Session open. `--non-interactive` and `--json` return after one attempt without prompting. Non-interactive mode also prevents browser sign-in.

## Output and exit behaviour

Human output lists each node, its status and available row counts, then totals load statuses and row movement. Dry-run output reports the selected plan. An intolerant failure prints its partial report when one is available.

`--json` emits the current report as one document. On an intolerant failure with a partial report, the document includes the error and report. These fields are not presented here as a compatibility contract.

The command exits `0` when the report succeeds, including an empty successful plan, and `1` when the report or operation fails. Argument errors exit through `argparse`.

## Examples

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-config.yml
```

Preview stale selection at a fixed instant:

```bash
weaver load Lakehouse/Landing \
  --stale \
  --as-of 2026-09-05T00:00:00Z \
  --dry-run \
  --workspace-config workspace-config.yml
```

Reload one installed table:

```bash
weaver load Lakehouse/Landing \
  --name Tables/Parcel.CurrentStatus \
  --reload \
  --workspace-config workspace-config.yml
```
