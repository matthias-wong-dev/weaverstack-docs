# Partial failures, rejected data and stability thresholds

A Load can encounter failure at three different levels: one execution node, work ordered around that node, and the estate state left after the run. Treating them as one all-or-nothing result hides the decisions that matter for continuation and recovery.

## A node failure does not erase completed work

An item-wide Load runs the installed dependency graph. When a node fails after its work has been resolved and dispatched, the target and catalogue may already contain effects from that attempt. Earlier nodes also remain completed. Weaver does not roll the operation back as one transaction.

The execution policy decides what is attempted next:

- fail-fast execution stops scheduling otherwise-ready nodes;
- fault-tolerant execution continues independent selected branches; and
- fault-tolerant execution may attempt a selected descendant after an upstream execution failure has settled.

That last case is deliberate. The descendant reads the state the failed execution left; Weaver does not pretend that the upstream node succeeded. Use it only when downstream work can produce useful evidence or useful partial output from that state.

A node that cannot be resolved or validated before dispatch has a different boundary. Its descendants remain blocked because Weaver has no valid installed work to continue through. Fault tolerance can still run unrelated valid branches.

Selection remains in force throughout. Continuation does not add another item, infer extra named work or repair an invalid installed graph. See [Fault tolerance](../core-concepts/fault-tolerance.md) for the conceptual model and [Load behaviour](../reference/operation-behaviour/load.md) for exact selection and outcomes.

## Rejected input is local to one load

For supported keyed Tables, Weaver can separate unusable incoming rows from rows eligible for reconciliation. Folder loads similarly separate staged files that do not match the Folder's file key.

Without fault tolerance, any such reject refuses that object's reconciliation before its target is modified through that path. Reject evidence remains available for diagnosis. With fault tolerance, Weaver excludes the rejected rows or files and can publish the accepted input. A tolerated reject does not make the input valid; it records that only part of the proposed input was applied.

This object-level policy and graph continuation use the same fault-tolerance choice but answer different questions:

- **input tolerance** decides whether accepted input from one node may be published alongside rejects;
- **graph continuation** decides which other selected nodes may be attempted after a node failure.

A tolerated reject does not block a downstream node. An intolerant reject is a node failure and follows the graph policy.

## Stability thresholds guard target-wide change

A keyed Table can declare limits for the percentage of established target rows that one load would delete or update, together with the target size at which those limits begin to apply. Weaver calculates the proposed change before target mutation. A change over an active limit is refused without applying the proposed target change through that path.

Stability checks are not row-rejection rules. Fault tolerance does not waive them, and an incremental change that would leave a declared unique key invalid is also refused regardless of the fault-tolerance setting. The Table API has a separate, explicit one-run stability waiver for an intended large change; it applies only to that Table load.

> **Design background:** [Load mechanics](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/load-mechanics/) frames staging, comparison with the current target, rejects and stability thresholds as separate controls over proposed change. Weaver applies those ideas through the reject and threshold behaviours described here; the reference pages define its exact mechanics.

Keep thresholds aligned with the scale and expected churn of each Table. A threshold low enough to catch an accidental replacement may also stop a legitimate backfill, while a high threshold may add no useful guard. Review the proposed change and use the explicit waiver only when the large update or deletion is the intended operation. See the [Table reference](../reference/weaver-documents/table.md) and [Python API](../reference/python/index.md) for exact metadata keys, defaults and API arguments.

## Read the estate as partial state

After a mixed run, inspect each affected branch rather than reading only the top-level result:

1. identify work that completed and may have changed data;
2. distinguish execution failures from work that could not be resolved;
3. find dependants that were blocked and independent work that was never scheduled;
4. inspect reject evidence and target contents for nodes that accepted only part of their input; and
5. use Health and catalogue history to decide what is failed, stale or still established.

Bookmarks advance only after clean successful loads. A tolerated reject can publish accepted data without advancing the bookmark, so a later run still starts from the last clean boundary. A failed or blocked node likewise leaves its recorded state available for recovery.

Recovery is a new operation against this partial estate. Correct the source, declaration, credentials or platform condition, then rerun the appropriate scope. Weaver does not resume an invisible transaction or automatically undo useful work from independent branches. See [Fault and outcome vocabulary](../reference/operation-behaviour/fault-and-outcome-vocabulary.md) for the exact node and run terms used in reports.
