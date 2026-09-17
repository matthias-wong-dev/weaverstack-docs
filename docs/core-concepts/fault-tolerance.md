# Fault tolerance

Fault tolerance determines how much remaining work Weaver attempts after one piece of work fails. It does not change the result of the failed work, undo work that already completed or make the operation a transaction.

The boundary differs across [Build, Load and Test](weaver-operations.md). A failure policy from one operation does not carry into the next.

## Build stops before later installation work

Build has no fault-tolerant execution mode. It records an outcome for every planned installation action. Once Build reaches a failure barrier, remaining work is skipped.

A failed Build can therefore leave physical changes from work that completed before the barrier. Later catalogue publication does not certify a failed rebuild. Build does not roll those changes back as one transaction. After correcting the declaration or platform condition, another Build reconciles the estate it finds rather than resuming the failed work.

## Load can continue after a settled failure

A normal item-wide Load stops scheduling otherwise-ready work after its first execution failure. Dependent work is blocked; independent work that was not reached remains pending.

A fault-tolerant Load keeps scheduling selected work. Independent branches continue. Downstream work can also run after an upstream execution failure, using the state that exists at that point; the failed upstream work is not treated as a successful update.

That continuation applies only to work that resolved and then failed during execution. If Weaver cannot resolve or validate selected work before execution, its descendants remain blocked while unrelated branches continue. A dependency cycle is invalid rather than a failure to continue past.

The final Load result still contains every outcome. A run with both completed and failed or blocked work is partially successful; fault tolerance does not convert it to success.

## Row rejection is a second Load boundary

For Tables and Folders, fault tolerance also controls recoverable incoming-row or incoming-file rejection. When continuation is selected, Weaver excludes rejected input and publishes the accepted input. The load records rejects and does not advance its bookmark because it did not consume a clean source window.

This does not tolerate every invalid change. A change that would leave the target invalid, or one refused by a stability threshold, still fails without modifying the target through that load path. These checks are separate from whether other work continues.

## Test evaluates each validation

An installed Test run attempts every selected Test and Assumption. A failed validation is a finding about its data; a validation that cannot run is recorded separately. Neither outcome stops another selected validation.

Test does not expose Load's fault-tolerance choice. Its validations are independent consumers of data, not producers ordered through one another. A source-file Test is a single direct evaluation, so there is no remaining validation set to continue.

## Workflows stop between commands

A workflow runs commands in order and stops when a command returns failure or raises a Weaver error. It does not continue to a later command because an earlier command preserved some independent progress.

Fault tolerance remains local to a command inside the workflow. For example, a fault-tolerant Load may finish additional work, but its failed or partially successful result still stops the following workflow commands. Commands that completed before the failure remain applied; the workflow does not roll them back.

## Reports and catalogue state describe partial work

Build reports the outcome of its planned installation actions. Load records each settled piece of work in the catalogue, including failed, blocked and pending outcomes. Installed Test runs record each validation outcome. Load statistics exist only for work that executed, and bookmarks advance only after a clean successful load. Direct source-file Tests do not publish estate evidence. Load and Test records created inside one workflow share its workflow identifier.

Fault tolerance does not retry failed Build actions, Load work, validations or workflow commands. A later attempt is a new operation against the state left by the previous one. Exact statuses, options, output fields and persistence guarantees belong in Reference and Contracts; the [Load contract](../contracts/load.md) defines the current Load surface.
