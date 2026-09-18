# Wipe behaviour

Wipe empties whole physical Fabric items. It is not scoped to Weaver-managed objects inside those items.

## Physical target selection

Positional targets are physical `Lakehouse/Name` or `Warehouse/Name` identities. They are not logical Weaver items. A Lakehouse target includes its Files and Tables areas; partial targets such as `Lakehouse/Name/Files` are not accepted by the public operation.

Naming targets selects exactly those physical items, deduplicated in request order. Wipe does not traverse project or installed dependencies.

Naming no target discovers the physical installed estate from distinct target type/name pairs in the selected catalogue's `_.Installation` rows. It does not use the targets currently declared in workspace configuration. With neither named targets nor a resolvable catalogue, planning fails.

A Lakehouse wipe removes all entries and shortcuts from its Files and Tables areas while keeping the area roots and the Fabric-owned `dbo` table directory. Removing a shortcut does not remove its source data. A Warehouse wipe removes user objects while retaining Fabric system schemas. Unmanaged content in the selected item is in scope.

## Catalogue disposition

The settled `WipePlan.catalogue_action` has these current values:

| Value | Behaviour | Public CLI route |
| --- | --- | --- |
| `remove` | Empty named or discovered targets and empty the resolved catalogue last. | Default when a catalogue resolves. |
| `unbind` | Empty named targets, preserve the catalogue, then remove its claims for those targets. | `--unbind`; requires a catalogue and at least one named non-catalogue target. |
| `leave` | Empty named targets with no catalogue to read or update. | Result when no catalogue resolves; it cannot be requested over a resolved catalogue. |
| `physical-only` | Empty exactly named targets without catalogue discovery or claim changes. | Python/internal operation route; not exposed as a CLI option. Mirror uses it for its own destinations. |

`remove`, `unbind` and `leave` are the catalogue dispositions visible through ordinary Wipe planning. `physical-only` is public in the Python operation vocabulary but is not a Wipe command-line choice.

For `remove`, the catalogue is appended once even when it was discovered or named earlier, and is always last. This keeps `_.Installation` readable while other targets are processed. For `unbind`, the catalogue cannot also be a target; claim removal happens only after all named targets have been emptied.

## Plan, preview and authorisation

`plan_wipe()` resolves target selection and catalogue disposition before mutation. Passing a settled plan to `wipe()` forbids additional planning arguments; `session` and `dry_run` may still accompany it. The CLI displays and executes the same plan without rediscovery.

`--dry-run` returns or renders the settled item-level plan and changes nothing. It does not enumerate the objects inside each item. At the public operation level, Warehouse targets are previewed without executing Warehouse wipe SQL, and Lakehouse removal reports are marked as dry-run.

A non-dry-run CLI invocation requires `--yes` or an affirmative terminal confirmation. Declining confirmation returns failure for Wipe and changes nothing. JSON mode, `--non-interactive`, and an invocation without a prompt never ask; without `--yes` they fail before mutation. `--non-interactive` also disables browser sign-in, but it is not destructive authorisation.

## Ordering, results and failure

Targets execute serially in plan order. With `remove`, the catalogue executes last. With `unbind`, claim removal executes after every target. Each completed item result is `emptied`; a kept catalogue added to an unbind result is `preserved` with `unbound: true`. Lakehouse results count removed `entries` and `shortcuts`; Warehouse results currently expose no object count.

Wipe stops when a target operation or final unbind fails. Targets already emptied remain empty; a failing target may be partially changed according to Fabric or storage behaviour; later targets are not attempted. If unbinding fails, every selected target is already empty and the catalogue may still contain some or all prior claims. Wipe has no rollback and does not return a completed `WipeResult` for a raised operation failure.

A later Wipe is a new operation against the remaining physical and catalogue state. See [Machine-readable interfaces](../machine-readable-output.md) for the current plan and result fields.
