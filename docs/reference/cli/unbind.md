# `weaver unbind`

Unbind removes the catalogue's claims for named physical items without changing their definitions, data, refresh state, connections or existence in Fabric. It requires a catalogue. Use it to stop managing an item, including a Report, or to forget an item already removed outside Weaver.

The arguments are physical targets, not logical project items. For `Report/Parcel: Parcel_Report_Dev` in configuration, name `Report/Parcel_Report_Dev`.

```bash
weaver unbind Report/Parcel_Report_Dev --dry-run --workspace-config workspace-dev.yml
weaver unbind Report/Parcel_Report_Dev --workspace-config workspace-dev.yml
```

The settled plan shows the logical claims removed, each physical target's presence and the preserved catalogue. Review it and confirm if correct; decline otherwise. Confirmation is required when any selected target still exists. Removing only claims for absent targets needs no confirmation. `--non-interactive` disables prompts; `--yes` supplies authorisation. A dry run changes nothing.

The catalogue itself cannot be unbound. An unclaimed target is an error. Claim removal does not make a later Build adopt the retained physical definition or data.

See [Unbind behaviour](../operation-behaviour/unbind.md) and [Wipe](wipe.md) for physical emptying rather than claim removal.

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver unbind [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--catalogue CATALOGUE] [--dry-run] [--yes] [--json] [--non-interactive] TARGET [TARGET ...]
```

## Positional arguments

`TARGET`
: Physical items to unbind: Lakehouse/Name, Warehouse/Name, SemanticModel/Name or Report/Name.

## Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

`--dry-run`
: Show what this would unbind.

`--yes`
: Unbind items that still exist without asking.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->
