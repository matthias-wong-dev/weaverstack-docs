# Wipe behaviour

Wipe empties named or catalogue-discovered physical Lakehouses/Warehouses, including unmanaged contents, and normally empties a resolved catalogue last. Semantic-model-only named Wipe instead resets those model definitions, retains the catalogue and removes their claims. No Fabric item is deleted. Reports cannot be wiped; use [Unbind](unbind.md) to remove their catalogue claims without changing the Reports.

## Physical target selection

Named targets are physical `Lakehouse/Name`, `Warehouse/Name` or `SemanticModel/Name`, not logical project items. They deduplicate in request order; dependencies add no targets. Partial areas such as `Lakehouse/Name/Files` are unsupported.

Without targets, Wipe discovers the estate from catalogue Installation records. When configuration has `targets`, every recorded installation must still be bound to the same physical target there, otherwise unscoped Wipe refuses and asks for named targets. With no configured targets, catalogue records supply the scope. Reports in the discovered estate are retained and shown as left rather than physically emptied. With neither explicit targets nor a catalogue, planning fails.

Lakehouse Wipe removes entries/shortcuts in Files and Tables while retaining area roots and the Fabric-owned `dbo` table directory. Shortcut removal retains source data. Warehouse Wipe removes user objects while keeping Fabric system schemas. Unmanaged content within these selected boundaries is in scope.

## Catalogue disposition

| Plan value | Effect | Ordinary route |
| --- | --- | --- |
| `remove` | Empty selected/discovered eligible targets, then the resolved catalogue | Default with a catalogue except a named semantic-only selection |
| `unbind` | Empty/reset targets, keep catalogue and remove their claims | `--unbind`, or default named semantic-only selection with a catalogue |
| `leave` | Empty explicit targets without reading/updating a catalogue | No catalogue resolves |
| `physical-only` | Internal/Python disposition for exactly named physical targets without claims | Not a CLI choice; not the ordinary retirement route |

`remove` appends the catalogue once and acts on it last; naming a single Warehouse while a catalogue resolves still empties that catalogue unless `--unbind` is selected. `unbind` requires a catalogue and named non-catalogue targets, and cannot include the catalogue as a target. A named semantic-only selection refuses explicit catalogue removal. A mixed named source/model selection retains the normal destructive catalogue default unless `--unbind` is used. The settled plan states the disposition; inspect it, not only the positional list.

## Semantic-model reset and source preservation

Semantic Wipe retains the model item and replaces its native definition with an empty model, preserving the existing culture. It does not wipe source data, gateways or shared connections. Registry/current runtime claims are withdrawn before the REST reset; remaining dictionary claims are removed after verified readback in the unbind path. A failed reset/readback cannot report the model as emptied or restore prior certification.

`--preserve-data-source` keeps one supported source in a hidden, columnless/measureless `__WeaverSource` table with one native partition. Supported forms are Automatic SQL/Direct Lake, retaining deployed shared expressions, or explicitly bound ShareableCloud SQL/Import with literal SQL database and one relation navigation, no shared expression. Import partitions must reach the same physical source as the bound connection. Unsupported/multiple source or connection forms refuse before any selected target mutates. No external source gives an ordinary empty reset. The flag requires at least one semantic target; it is frozen in the plan, not a credential migration or preservation of the full model.

## Preview and authorisation

`plan_wipe()` settles scope and disposition. `wipe(plan=...)` refuses additional planning arguments; `session` and `dry_run` can still accompany a plan. The CLI displays and executes the settled plan. Review and confirm if correct, or decline if not.

`--dry-run` reports scope without executing removal or claim deletion and needs no `--yes`. It does not prove later execution or enumerate a universal detailed object inventory. Execution requires `--yes` or affirmative terminal confirmation; declining Wipe exits `1`. JSON, non-interactive or no-prompt execution requires `--yes`. `--non-interactive` disables input/browser sign-in but does not authorise destruction.

## Ordering, failure and results

Targets are frozen into mutation actions. Independent targets can execute under configured resource limits; do not assume serial list-order execution or that failure on one prevents another from already running. Lakehouse shortcut detachment/path release precedes its content sweep. Catalogue removal or final claim deletion depends on settlement of the required target actions; it is not an operation-wide transaction.

Successful target outcomes are `emptied`; a retained catalogue in an unbind result is `preserved` with `unbound: true`. Lakehouse reports describe removed entries/shortcuts. A failure or uncertain action raises a command error rather than a completed successful Wipe result. Earlier/independent mutations remain, a failing target can be partially changed, and missing certification may already have been withdrawn. Inspect the remaining physical/catalogue state before retrying; do not automatically replay an uncertain destructive action. Wipe has no rollback.

See [`weaver wipe`](../cli/wipe.md), [Unbind](unbind.md), [Python operations](../python/operations.md) and [machine output](../machine-readable-output.md).
