# `weaver build`

Deploy Lakehouse and Warehouse definitions, then native semantic models and Reports, from the same project and workspace configuration. Build changes definitions; use Load to run data work or refresh a model.

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver build [-h] [--item ITEM[=TARGET]] [--data-source EXPRESSION=KIND/NAME] [--bind-data-sources] [--dry-run] [--bundle-only] [--bundle-path PATH] [--concurrency N] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [SOURCE]
```

## Positional arguments

`SOURCE`
: Project folder, or an abfss location inside a Fabric session. Defaults to the current directory or Notebook Resources.

## Options

`-h, --help`
: show this help message and exit

`--item ITEM[=TARGET]`
: Weaver item to build. Its physical target comes from workspace configuration; use ITEM=TARGET to supply or override it. Repeat to select multiple items. Naming none builds every configured item.

`--data-source EXPRESSION=KIND/NAME`
: Substitute a shared M source expression with a Warehouse or Lakehouse.

`--bind-data-sources`
: After deploying a semantic model, bind each of its SQL data sources to the connection that reaches it.

`--dry-run`
: Inspect the Build plan without changing target state.

`--bundle-only`
: Create a deployment bundle without installing it.

`--bundle-path PATH`
: Directory to write a bundle created with --bundle-only.

`--concurrency N`
: Limit total simultaneous execution for this invocation; retain resource limits.

`--json`
: Emit the result as JSON.

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

Build snapshots and validates project source, prepares a destination-bound plan and normally installs it. `SOURCE` defaults to the current directory on a desktop or Notebook Resources in Fabric; Fabric also accepts an `abfss` source.

Repeat `--item ITEM[=TARGET]` for exact logical bindings, item-type selectors or `PowerBI/<project>`. Omission selects configured targets. Explicit binding targets must match the item kind. Build Lakehouse/Warehouse source items and Power BI items in separate calls.

## Execution modes

- Normal Build deploys selected changes and can create missing selected model/Report targets. Selected semantic models deploy/verify even when unchanged; source-item fixed points and catalogue-backed Report-only fixed points differ.
- `--dry-run` reads state and returns the canonical preview without mutations, target creation or a retained bundle. Suitable existing targets are required.
- `--bundle-only` retains a frozen executable bundle without installing. `--bundle-path` requires this mode and an absent/empty destination. It does not provision missing targets.

Dry run and bundle-only are mutually exclusive. Install executes retained input without reopening source or replanning/retargeting. `--concurrency N` caps total scheduled actions alongside configured resource limits; it does not edit configuration. `--data-source Expression=Warehouse/Name` overrides supported typed shared-expression mappings; `--bind-data-sources` requests existing connection binding, not credentials creation.

## Interaction and outcomes

Interactive source-discovery/metadata/identity/graph errors may offer edit-and-retry within the Session. Configuration/service failures are not source-edit retries. JSON/non-interactive runs make one attempt. Installation is not an operation-wide transaction; earlier physical/current-state changes can remain after failure.

Human output presents selection/action outcomes, warnings and retained bundle/report paths as applicable. JSON emits the current result, including preview evidence in dry-run mode. CLI exit is `0` for a succeeded result and `1` for failed operations/results; parser usage errors exit `2`.

## Examples

```bash
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --dry-run --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --concurrency 2 --workspace-config workspace-dev.yml
weaver build . --item Warehouse/Operations --bundle-only --bundle-path ./dist/parcel-bundle --workspace-config workspace-dev.yml
```

Use [Build behaviour](../operation-behaviour/build.md) for reconciliation/protection/failure rules, [shared selection](../operation-behaviour/shared-selection-and-identity.md) for grammar and [Power BI requirements](../power-bi/requirements-and-compatibility.md) for modes/bindings.

## Build source items, then models and Reports

For a project containing `Warehouse/Operations` and `PowerBI/Parcel`, with both configured:

```bash
weaver build . --item Warehouse/Operations --workspace-config workspace-config.yml
weaver build . --item PowerBI/Parcel --workspace-config workspace-config.yml
```

The first call installs source definitions. The second can read their metadata, deploys the model before its linked Report, and registers them in the same catalogue. Source-data and Power BI definitions use separate Build calls; a workflow can sequence both. See [Connect a semantic model to source data](../../semantic-models/managed-sources.md).
