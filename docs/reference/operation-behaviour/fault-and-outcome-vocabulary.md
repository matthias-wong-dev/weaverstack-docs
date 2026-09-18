# Fault and outcome vocabulary

Status words are operation-specific. The same spelling can appear at different levels, and different operations do not share one report schema, state machine or compatibility contract.

## Build and install

A final installation action is:

- `succeeded` — the action completed;
- `failed` — the action was attempted and failed; or
- `skipped` — the action was not attempted because an earlier installation barrier failed, or the action is a supported host skip.

`pending` and `running` are action/report lifecycle states in the public report types; a completed installation report settles planned actions to the final terms above. An installation report is `succeeded` when no action failed and `failed` otherwise. A supported skipped action does not by itself fail the report.

A Build result uses `succeeded` or `failed`. Pre-installation command errors have no installation report.

## Load

Execution nodes use:

| Node status | Meaning |
| --- | --- |
| `pending` | Selected but not started, including work left unreached by fail-fast scheduling. |
| `running` | Execution has started and has not yet settled. |
| `succeeded` | Executed work established a clean result. |
| `succeeded_with_rejects` | Valid work was published and the primitive reported rejected rows or files. |
| `failed` | The primitive or its dispatch failed. |
| `blocked` | Upstream work could not establish the prerequisite for this node. |
| `skipped` | Execution policy or supported host behaviour omitted the work; dependency failures use `blocked`, not `skipped`. |

Load dry-run nodes instead use `validated`, `invalid` and `blocked`. `validated` means the target and primitive resolved without execution. `invalid` means the node's own primitive or target could not be resolved. Dry-run `blocked` means an upstream prerequisite did not validate.

An execution report is:

- `succeeded` when no executed branch failed or reported rejects;
- `succeeded_with_rejects` when all executable branches completed and at least one reported rejects;
- `partially_succeeded` when at least one branch completed and at least one failed or was blocked; or
- `failed` when no requested branch completed, or fail-fast stopped the task.

A dry-run report is `succeeded` when the plan validates and `invalid` otherwise. An empty execution report is `succeeded`; the current empty dry-run report is `invalid`, except the operation's empty stale selection is returned as a successful no-work run before that generic final-status rule.

## Test

Test node and run reports use the same four terms:

| Status | Meaning |
| --- | --- |
| `passed` | The validation ran and found no discrepancy or violation. |
| `failed` | The validation ran and found discrepancy or violation rows. |
| `invalid` | The validation could not be evaluated. This is not a failed data finding. |
| `planned` | Dry-run resolution completed and the validation did not run. |

A run is `invalid` if any selected node is invalid; otherwise `failed` if any node failed; otherwise `planned` when all selected nodes are planned; otherwise `passed`. An empty installed selection is `passed`.

These are report terms. Persisted `_.TestStatus` uses the catalogue vocabulary below rather than storing `passed` and `invalid` under those spellings.

## Health

Health findings, sections and the overall report use `green`, `amber` and `red`:

- `green` — no worse finding was produced for the assessed subjects;
- `amber` — state is pending, stale, rejected or otherwise not established as current without being a recorded hard failure; and
- `red` — recorded failure, error, blockage or Build inconsistency makes the assessed state failed.

The overall status is the worst section severity. Only `green` is a successful Health CLI result.

## Mirror, Wipe and Workflow

A returned Mirror result currently has `status: succeeded`. Mirror raises on failure rather than returning a partial failed `MirrorResult`.

Each completed Wipe item is `emptied`. A catalogue retained by `unbind` is `preserved` and carries `unbound: true`. A raised Wipe failure has no completed aggregate result for later or partly processed targets.

Workflow has no nested universal outcome vocabulary. It returns success only when all entries return success, or when an available confirmation was explicitly declined before execution. Missing authorisation, a failed command status or a Weaver error returns failure and identifies the first stopped entry. Nested reports retain their own vocabularies.

## Persisted catalogue outcomes

Current Load/Test state and operational Log evidence use these catalogue values:

- `Pending` — no outcome for the current installed incarnation;
- `Skipped` — work was deliberately omitted;
- `Succeeded` — work completed acceptably;
- `Failed` — evaluated work produced an unacceptable result;
- `Error` — work could not be evaluated;
- `Blocked` — an upstream prerequisite prevented execution; and
- `Rejected` — Load completed with rejected input while valid input may have landed.

Capitalisation above is the stored display value; Python constants and report mappings use lowercase spellings. Catalogue terms are not interchangeable with Load report, Test report, Build action or Health terms. For example, Test report `passed` maps to persisted `Succeeded`, Test report `invalid` maps to persisted `Error` or `Blocked` according to cause, and Load report `succeeded_with_rejects` maps to persisted `Rejected`.

## Message severity and compatibility

Load message objects currently use `info`, `warning` and `error` severity. These describe messages, not node or report success.

The terms on this page are the exact current surfaced vocabularies. Their containing fields and JSON documents are command-specific and mostly unversioned. Do not parse one operation's term set as another operation's schema or infer compatibility between them. See [Machine-readable interfaces](../machine-readable-output.md) for current field placement.
