# Fault-tolerance contract

Fault tolerance controls how much selected work is attempted after a failure. It does not change a failed outcome, retry work, widen selection, undo completed changes or make an operation transactional.

Failure barriers differ by operation. A continuation rule for Load does not apply to Build, Test or a workflow.

## Build barriers

Build has no fault-tolerant mode. Installation is divided by ordered barriers. When an action fails, that sequence fails, every planned action receives a reported outcome and later installation work is skipped. Catalogue certification that depends on failed physical work is not published as successful.

Actions completed before the barrier remain applied. Build does not roll them back as one operation. A later Build reads the project, catalogue and inventory again and reconciles the state it finds; it does not resume the earlier report.

A Build result reports failure and preserves its per-action evidence. Preflight failures that occur before installation runs leave the plan unexecuted rather than producing successful action outcomes.

## Load barriers

An item-wide Load uses the installed dependency graph. There are two distinct kinds of upstream problem.

A **resolved execution failure** occurs after Weaver resolved the node and attempted its installed work. Without fault tolerance, the first such failure stops later scheduling, blocks its dependants and leaves otherwise independent nodes that were not reached pending. With fault tolerance:

- independent selected branches continue; and
- a selected dependant may run after the failed upstream node has settled.

The dependant reads the state left by that failed execution. The upstream node is not treated as successful.

An **unresolved or invalid node** cannot be dispatched as valid installed work. Its descendants remain blocked under either policy. Fault tolerance still permits unrelated valid branches to run. A dependency cycle is invalid before this continuation rule can apply.

Name selection remains an override: it contains only the named installed objects and has no dependency expansion or dependency ordering to continue through.

The final report retains failed, blocked and pending outcomes. Fault tolerance can therefore produce more completed work, but a mixed report is still partially successful and exits non-zero. When no requested branch completes, or fail-fast stops the run, the run fails.

## Rejected input and invalid target state

For a Table or Folder, fault tolerance also controls recoverable incoming-row or incoming-file rejection. Without it, rejected input stops that object's load before the target is modified through the reconciliation path. With it, rejected input is excluded and accepted input can be published; the result records rejects and does not advance the bookmark.

Fault tolerance does not permit a change that would leave a declared unique key invalid. It also does not waive a stability threshold. Those conditions fail the object without applying the proposed target change through that path. A separate explicit threshold waiver applies only to the Table load that receives it.

## Test barriers

An installed Test run evaluates every selected Test and Assumption. A failed validation is a completed finding; a validation that cannot run is an invalid outcome. Neither blocks another selected validation because validations are independent consumers, not a producer chain.

Test therefore uses continuation internally but exposes no Load fault-tolerance switch. A one-file source Test has one selected validation and publishes no installed-estate status or history.

## Workflow barriers

A workflow parses and settles its sequence before execution, then runs commands in file order. It stops at the first command that returns failure or raises a Weaver error. Later commands do not run.

Fault tolerance remains local to a nested Load. If that Load finishes with a failed or partially successful report, the workflow stops even though the Load attempted additional branches. Commands completed earlier in the workflow remain applied.

An interactive Session has a different boundary: a failed command returns to its prompt, allowing a later command to be issued as a new operation. If an acquired execution capability fails, Weaver does not replace it part-way through the failed operation; a later operation may attempt to reacquire it.

## Recording partial work

Build reports each planned installation action as succeeded, failed or skipped. Load and installed Test runs record settled node outcomes with their workflow identifier. A blocked Load records current status and log evidence but no Load statistic because no data work ran. Bookmarks advance only for clean successful loads.

A workflow shares one workflow identifier across recorded Load and Test work that actually ran. The failed command and earlier commands can therefore be correlated; later commands have no outcomes because they were not executed.

No operation in this contract retries failed work automatically. A later attempt is a new operation against the state left behind.

## Defined behaviour

The Fault-tolerance contract specifies that Weaver:

1. stops Build at its installation barrier and skips later planned work;
2. stops ordinary Load scheduling after an execution failure while reporting every planned node;
3. lets fault-tolerant Load continue independent work and descendants of settled execution failures;
4. keeps descendants of unresolved or invalid Load work blocked;
5. keeps row-rejection continuation separate from target-validity and stability checks;
6. evaluates selected validations independently;
7. stops a workflow after its first unsuccessful command; and
8. preserves completed effects and evidence without operation-wide rollback or automatic retry.
