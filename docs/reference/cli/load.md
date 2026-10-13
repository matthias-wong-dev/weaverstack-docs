# `weaver load`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver load [-h] [--item ITEM] [--name NAME] [--source SOURCE] [--concurrency N] [--ancestors] [--descendants] [--fault-tolerant] [--reload] [--ignore-stability-threshold] [--stale] [--as-of DATETIME] [--dry-run] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [ITEM ...]
```

## Positional arguments

`ITEM`
: Weaver items to load, as Lakehouse/Name, Warehouse/Name or SemanticModel/Name. PowerBI or PowerBI/<project> names the semantic models of the project folder. Naming none loads every installed item.

## Options

`-h, --help`
: show this help message and exit

`--item ITEM`
: Legacy spelling for a positional Weaver item.

`--name NAME`
: Select installed objects whose whole name matches this regular expression: Tables/Schema.Object or Files/Schema.Object in a Lakehouse, Schema.Object in a Warehouse. A bare Schema.Object is accepted where it names one object. Repeat to select more.

`--source SOURCE`
: Project folder, or an abfss location inside a Fabric session. Defaults to the current directory or Notebook Resources.

`--concurrency N`
: Limit total simultaneous execution for this invocation; retain resource limits.

`--ancestors`
: Include recursive upstream loads within the selected items.

`--descendants`
: Include recursive downstream loads within the selected items.

`--fault-tolerant`
: Continue independent branches after a failure.

`--reload`
: Rebuild each selected table: reset its bookmark, empty it, then load. Does not affect unselected tables.

`--ignore-stability-threshold`
: Waive the declared delete and update limits for this load. Row checks, fault tolerance and selection are unchanged.

`--stale`
: Select the objects whose load health is not green.

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

Load runs installed Table/Folder work or refreshes semantic models. Reports do not Load. Positional items and repeatable legacy `--item` define a hard scope. With a catalogue omission selects installed items except Reports; without a catalogue name semantic models explicitly or use `PowerBI[/project]` with source context.

Repeat `--name` for case-insensitive whole-name regular expressions, not globs/substrings; every pattern must match. Use `[.]` for literal dots. In Lakehouses qualify ambiguous names with `Tables/` or `Files/`. Plain named selection is an unordered operator override without inferred dependency/barrier edges.

`--ancestors`/`--descendants` recursively expand original seeds separately inside requested installed items; the union restores dependency ordering and required barriers. Newly reached descendants do not add all their other ancestors. Select both items explicitly for cross-item expansion. These are Load options, not Build/Test options.

`--stale` selects non-Green work; `--as-of` requires it and a zoned ISO-8601 cutoff (default 24 hours before the run). `--reload` and `--stale` conflict. Catalogue-free refresh offers no installed name/stale/reload/recursive selection and records no Weaver history. `--source` supplies project context for Power BI group selectors, not changed source Load code.

## Execution and warnings

`--dry-run` resolves the plan without dispatch, endpoint refresh or catalogue writes. `--reload` empties each reached selected Table and resets progress before loading. It is destructive; expansion can enlarge its scope. Folders cannot reload. Static Tables run again after reload. A reached failed reconstruction is not rolled back.

`--fault-tolerant` continues independent work under the Load policy; final failures still fail the run. `--ignore-stability-threshold` waives only declared delete/update gates for that invocation, not null/unique checks, selection or failure policy. Use it only when the large change is intended. `--concurrency N` caps total simultaneous scheduled nodes alongside per-resource limits.

## Interaction and outcomes

Supported interactive load failures can offer retry. JSON/non-interactive invocations make one attempt; non-interactive also disables browser sign-in. Human output lists nodes/status/counts; JSON emits the report or error with available partial report. Exit is `0` for succeeded/succeeded-with-rejects, `1` for partial/failed/invalid or command failures, `2` for parser usage errors. Model refresh has no invented row counts.

## Examples

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --descendants --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --descendants --concurrency 2 --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --stale --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

These commands assume the relevant definitions/targets already exist. See [Load behaviour](../operation-behaviour/load.md) for exact selection/failure state and [shared selection](../operation-behaviour/shared-selection-and-identity.md).
