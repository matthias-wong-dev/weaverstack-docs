# The development cycle

Use a mirrored development estate to keep the project's logical identities while working against development catalogues and physical targets. Establish the baseline once, then iterate without re-mirroring it on every change.

## Phase 1: establish the development baseline

Choose the development workspace configuration. It should bind the project to the development catalogue and targets and name the source catalogue in `mirror`.

Before changing anything, run Mirror once:

```bash
weaver mirror --workspace-config workspace-development.yml
```

Review the displayed source catalogue, destination catalogue and every destination target. Confirm if that boundary is correct; decline if it is not. Mirror has no dry-run mode, and declining leaves the destinations unchanged.

Mirror empties and reconstructs the displayed destination catalogue and targets from the source estate. Unchanged objects begin as borrowed source data. The destination catalogue records that state, while the project's logical items and Weaver documents remain unchanged.

Inspect the baseline:

```bash
weaver health --workspace-config workspace-development.yml
```

See [Mirrors](../core-concepts/mirrors.md) for borrowed and local data. Exact Mirror selection, authorisation and failure boundaries are in [Mirror operation behaviour](../reference/operation-behaviour/mirror.md).

## Phase 2: edit and iterate

Use this loop after the baseline exists:

```text
edit
  → check
  → build
  → load --stale
  → test
  → health
  → repeat
```

Run it against the same development configuration:

```bash
weaver check

weaver build . \
  --workspace-config workspace-development.yml

weaver load \
  --stale \
  --workspace-config workspace-development.yml

weaver test \
  --workspace-config workspace-development.yml

weaver health \
  --workspace-config workspace-development.yml
```

Check validates project source locally. Build compares that source with the mirrored installed state. Changed borrowed objects and affected descendants inside the Build selection become local; unchanged objects remain borrowed.

Build resets changed loadable work to a non-Green state. `load --stale` selects the installed loadable objects that now need work while leaving Green objects alone. Test runs the installed validations, and Health shows the resulting Load, Tests and Build state.

Run the loop item-wide by default. Use `--name` only for deliberate targeting, diagnosis or Table reconstruction; named Load does not add dependencies. The [Load operation behaviour](../reference/operation-behaviour/load.md) defines that narrower boundary.

Re-mirror only when the intended result is a fresh source baseline. It replaces local materialisations inside the displayed destination boundary; it is a reset, not an iteration step.
