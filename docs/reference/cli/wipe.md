# `weaver wipe`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver wipe [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [--unbind] [--dry-run] [--yes] [--json] [--non-interactive] [TARGET ...]
```

## Positional arguments

`TARGET`
: Physical items to empty, as Lakehouse/Name or Warehouse/Name. Naming none empties the estate the catalogue records.

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

`wipe` empties physical Fabric items. Each positional `TARGET` is a physical `Lakehouse/Name` or `Warehouse/Name`, not a logical Weaver item. Named targets select exactly those items. With no targets, Weaver reads the estate recorded by the resolved catalogue.

The catalogue is part of the plan and is emptied last. `--unbind` instead preserves the catalogue and removes its claims for the named targets; it requires a resolved catalogue and at least one target.

## Execution

Weaver resolves one plan before asking for confirmation and executes that same plan without rediscovering the estate. A Lakehouse wipe removes its selected physical contents; a Warehouse wipe empties the selected Warehouse. This operation cannot be undone.

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
