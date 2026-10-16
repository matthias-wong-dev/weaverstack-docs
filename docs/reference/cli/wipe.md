# `weaver wipe`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver wipe [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [--unbind] [--preserve-data-source] [--dry-run] [--yes] [--json] [--non-interactive] [TARGET ...]
```

## Positional arguments

`TARGET`
: Physical items to empty: Lakehouse/Name, Warehouse/Name or SemanticModel/Name. Naming none empties the estate the catalogue records.

## Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

`--unbind`
: Keep the catalogue and remove its claims for the named targets. Requires a catalogue and at least one target.

`--preserve-data-source`
: Retain one Automatic SQL / Direct Lake source in a hidden columnless table.

`--dry-run`
: Show the estate this would empty.

`--yes`
: Authorise the removal without asking.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->

## Responsibility and selection

`wipe` empties the named physical Fabric items and, when a catalogue resolves, empties that catalogue last. `--unbind` instead preserves the catalogue and removes its claims for the named targets.

Each positional `TARGET` is a physical `Lakehouse/Name`, `Warehouse/Name` or `SemanticModel/Name`, not a logical Weaver item. Named targets select exactly those items. With no targets, Weaver reads the estate recorded by the resolved catalogue. `--unbind` requires a resolved catalogue and at least one target. A named semantic-model-only selection retains the catalogue and removes model claims by default. Reports cannot be wiped; use standalone [Unbind](unbind.md). An unscoped wipe with configured targets refuses installations not bound there to the same physical items.

## Execution

Weaver resolves one plan before asking for confirmation and executes that same plan without rediscovering the estate. A Lakehouse wipe removes its selected physical contents; a Warehouse wipe empties the selected Warehouse. A semantic-model wipe retains the service item and resets its native definition. `--preserve-data-source` retains a supported hidden source shell, not the whole model, source data or credentials. This operation has no rollback; independent targets may already have changed when one fails. See [Wipe behaviour](../operation-behaviour/wipe.md) for accepted source-preservation forms and catalogue scope.

`--dry-run` resolves and displays the plan without emptying or unbinding anything. It does not require `--yes`.

## Interaction

Without `--yes`, an interactive invocation displays the plan and asks for confirmation. `--yes` authorises removal but does not suppress the human-readable plan.

`--non-interactive` prevents prompts and browser sign-in; it does not approve removal. An unattended wipe requires `--non-interactive --yes`. JSON mode never prompts and also requires `--yes` unless `--dry-run` is used.

## Output and exit behaviour

Human dry-run output describes the physical targets and states that nothing changed. Human execution output shows the plan before mutation, then reports one outcome per physical item.

`--json --dry-run` writes one plan document to stdout. `--json --yes` writes one result document that includes the plan and item outcomes. Treat these as command output, not as a versioned schema guarantee.

The command exits `0` after a dry run or completed wipe. Missing or declined confirmation exits `1` and changes nothing. Planning, validation, authentication and Fabric failures also produce a non-zero status.

## Examples

Preview named physical targets:

```bash
weaver wipe \
  Lakehouse/ParcelLanding_Dev \
  Warehouse/ParcelOperations_Dev \
  --workspace "Parcel Development" \
  --dry-run
```

Run the settled plan unattended:

```bash
weaver wipe Warehouse/ParcelOperations_Dev \
  --workspace "Parcel Development" \
  --non-interactive \
  --yes
```

Preserve the catalogue while emptying and unbinding one target:

```bash
weaver wipe Lakehouse/ParcelLanding_Dev \
  --workspace-config workspace-development.yml \
  --unbind \
  --yes
```
