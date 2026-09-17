# Recover an estate

Recovery in Weaver is reconciliation: correct the cause, choose the smallest supported operation and run it against the state that remains. Build, Load, Test and workflows are not operation-wide transactions. Completed work is not rolled back when later work fails.

## Prerequisites

- Preserve the failed command report, exit status and workflow identifier.
- Run Health against the same workspace configuration to identify current installed and operational state.
- Correct project source with `weaver check` before using Build.
- Preview selection with `--dry-run` wherever the operation supports it.
- Use read-only catalogue inspection. Do not repair `_.Registry`, status, bookmark or mirror rows manually.

The examples use `workspace-development.yml`, `Lakehouse/Landing` and `Warehouse/Operations` in a parcel estate.

## Choose the recovery operation

| State to recover | Supported action | What it does not do |
| --- | --- | --- |
| Source or Build condition corrected | Rerun Build for the affected logical items | Resume or roll back the failed Build |
| Load failed or remained pending | Dry-run and rerun the intended item or named selection | Reinstall edited source |
| Selected Table must restart from empty | Use `load --reload` for that Table | Reload Folders or downstream objects |
| Only non-Green Load work should run | Use `load --stale` | Rerun Tests or widen item selection |
| Validation failed or could not run | Correct data, runtime or validation; rerun Test | Rebuild an edited validation automatically |
| Development needs a fresh source baseline | Re-mirror after inspecting the settled destination plan | Preserve local destination materialisations |
| Physical targets must be deliberately emptied | Use Wipe after a dry run | Provide normal Build/Load iteration or rollback |

Start with [Fault tolerance](../core-concepts/fault-tolerance.md) when a report contains mixed outcomes. A later attempt is a new operation against partial state, not continuation of the old operation.

## Reconcile a failed Build

A Build failure can leave physical changes from completed actions while later work is skipped. Correct the source or Fabric condition, then validate locally:

```bash
weaver check
```

Build only the logical items whose installed estate should be reconciled:

```bash
weaver build . \
  --item Warehouse/Operations \
  --workspace-config workspace-development.yml
```

Select every item that should participate in dependency impact. A dependency does not add an unselected item. Build reads the current project and installed estate again, determines affected work and publishes certification only for successful installation work.

Build has no dry-run switch. Keep the selection narrow, preserve the previous report and inspect the result:

```bash
weaver health \
  --item Warehouse/Operations \
  --workspace-config workspace-development.yml
```

Do not use Wipe to turn an ordinary failed Build into a clean slate. Rerun Build so it can reconcile the state it finds. If the catalogue itself is reported incomplete or incompatible, stop and preserve evidence rather than assuming that a scoped Build can reconstruct state owned by other installations.

## Rerun failed or pending Load work

After correcting the data, runtime or permission condition, preview the same logical-item boundary:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-development.yml \
  --dry-run
```

Then rerun it:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-development.yml
```

This uses the work last installed by Build. If source changed during the correction, Build it first.

For one object, use an exact named selection:

```bash
weaver load Warehouse/Operations \
  --name Parcel.Status \
  --workspace-config workspace-development.yml \
  --dry-run

weaver load Warehouse/Operations \
  --name Parcel.Status \
  --workspace-config workspace-development.yml
```

A named Load runs exactly the named installed object without adding or ordering its dependencies. Confirm upstream state yourself before choosing it.

## Reconstruct selected Tables with reload

Use reload when the selected Table must be emptied and rebuilt from the beginning, including a reset bookmark. Preview it first:

```bash
weaver load Warehouse/Operations \
  --name Parcel.Status \
  --reload \
  --dry-run \
  --workspace-config workspace-development.yml
```

Apply the reviewed selection:

```bash
weaver load Warehouse/Operations \
  --name Parcel.Status \
  --reload \
  --workspace-config workspace-development.yml
```

Reload is destructive for each selected Table: it resets the bookmark, marks Load state Pending, empties the Table and runs its installed Load work. It does not affect unselected Tables or add downstream objects. Folders cannot be reloaded with this option.

If execution fails after the reset or emptying step, there is no automatic restoration of the previous Table contents. Correct the cause and rerun the reload or restore data through a separately managed backup process. Weaver does not promise an operation-wide rollback.

## Run only non-Green Load work

Health and stale selection share the same Load assessment. Inspect and preview:

```bash
weaver health \
  --workspace-config workspace-development.yml

weaver load Lakehouse/Landing Warehouse/Operations \
  --stale \
  --dry-run \
  --workspace-config workspace-development.yml
```

Apply the same selection:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --stale \
  --workspace-config workspace-development.yml
```

This selects installed loadable objects in the named items whose Load health is not Green, including failed, blocked, rejected, pending or stale work. Green upstream work is not pulled into the selection merely because a selected descendant reads it. Dependency ordering remains between selected item-wide work.

To use a specific freshness threshold, repeat the same zoned instant on Health, dry run and Load:

```bash
weaver load Warehouse/Operations \
  --stale \
  --as-of 2026-09-18T00:00:00+10:00 \
  --dry-run \
  --workspace-config workspace-development.yml
```

`--reload` and `--stale` cannot be combined. Choose reconstruction of explicitly selected Tables or health-based catch-up, not both.

## Recover validation state

If a Test or Assumption source changed, Check and Build its owning item first. Then preview and rerun installed validations:

```bash
weaver test Warehouse/Operations \
  --dry-run \
  --workspace-config workspace-development.yml

weaver test Warehouse/Operations \
  --workspace-config workspace-development.yml
```

For one validation and diagnostic rows:

```bash
weaver test Warehouse/Operations \
  --name Parcel.StatusMatches \
  --workspace-config workspace-development.yml
```

Test attempts all validations in an item-wide selection even when one fails. It has no retry or rollback switch. A rebuilt validation is Pending until Test runs it; a failed validation remains a data finding until a later run records another outcome.

## Refresh a mirrored development baseline

Re-mirror only when the intended recovery is to replace the development baseline from its configured source. Mirror empties and reconstructs the destination catalogue and selected destination targets, replacing local materialisations in that boundary.

Mirror does not expose `--dry-run`. Do not invent one. To inspect its settled plan without mutation, run it without `--yes` in non-interactive mode:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --non-interactive
```

Weaver resolves and displays the source catalogue, destination catalogue and selected target bindings, then refuses to mutate because authorisation is absent. A non-zero exit is expected for this preview. Check every destination named in that plan.

After review, rerun the same request with explicit authorisation:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --non-interactive \
  --yes
```

`--non-interactive` does not authorise the mirror. `--yes` authorises emptying the displayed destinations; it does not make the request non-interactive, change the selection or preserve destination data.

After Mirror completes, inspect Health. Changed project documents still require Build before their borrowed representations become local. See the [Development cycle](../core-concepts/development-cycle.md) for the resulting mixed estate and [Catalogue](../core-concepts/catalogue.md) for `_.Mirror` state.

## Wipe only when emptying is the intended recovery

Wipe is not the normal development loop. Use Build to reconcile declarations, reload to reconstruct selected Tables and mirror to refresh a development baseline. Use Wipe only when the intended result is an empty physical target or estate.

Preview exact physical targets:

```bash
weaver wipe Warehouse/ParcelOperationsDev \
  --workspace-config workspace-development.yml \
  --dry-run
```

The dry run displays the settled target boundary and changes nothing. It does not enumerate every object inside each item.

If that boundary is correct, authorise the same command:

```bash
weaver wipe Warehouse/ParcelOperationsDev \
  --workspace-config workspace-development.yml \
  --non-interactive \
  --yes
```

Named targets are physical Fabric items, not logical Weaver item names. With named targets, Wipe empties exactly those items and includes the resolved catalogue according to the displayed plan. To preserve the catalogue while removing its claims for named emptied targets, use `--unbind`; it requires a catalogue and at least one target:

```bash
weaver wipe Warehouse/ParcelOperationsDev \
  --unbind \
  --workspace-config workspace-development.yml \
  --dry-run
```

Naming no target selects the whole estate recorded by the catalogue and empties the catalogue last. Always dry-run that form first:

```bash
weaver wipe \
  --workspace-config workspace-development.yml \
  --dry-run
```

`--non-interactive` only prevents prompts and browser sign-in. It never grants permission. `--yes` authorises the settled removal and nothing else. Neither option changes the target boundary or supplies rollback.

## Verify recovery

After the selected recovery operation:

1. rerun Health with physical inventory enabled;
2. inspect the operation report and workflow identifier;
3. query `_.LoadStatus` or `_.TestStatus` for current state when needed;
4. use `_.Log` and `_.LoadStatistic` for settled historical evidence;
5. rerun Test when recovered data changes validation inputs.

```bash
weaver health \
  --workspace-config workspace-development.yml
```

A successful command is not proof that every business expectation is restored. Health reports installed and operational consistency; Tests and domain queries establish data expectations.

Use [Weaver operations](../core-concepts/weaver-operations.md) for lifecycle meaning, [Dependencies](../core-concepts/dependencies.md) for affected selection, [Fault tolerance](../core-concepts/fault-tolerance.md) for partial work, the [Load contract](../contracts/load.md) for reload and stale guarantees, the [CLI reference](../reference/cli.md) for exact options and [Contracts](../contracts/index.md) for other defined boundaries.