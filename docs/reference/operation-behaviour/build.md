# Build behaviour

Build takes a snapshot of project source, resolves destination bindings and prepares a canonical deployment plan. Normal execution installs it; `--dry-run` only presents it; `--bundle-only` retains executable input without installing.

## Inputs and selection

`SOURCE` defaults to the current directory on a desktop and Notebook Resources inside a Fabric session. An `abfss` source is accepted inside Fabric. The complete source is copied to a temporary snapshot before parsing; later source edits cannot change that invocation. The snapshot is removed after success or failure.

Repeatable `--item ITEM[=TARGET]` selects logical items and may override physical bindings. Naming none selects configured targets; an empty selection fails. Type selectors and `PowerBI/<project>` expand against project/configuration according to [Shared selection](shared-selection-and-identity.md). Parsing checks the complete project, but selected items are the reconciliation boundary; dependencies do not add an unselected item.

Lakehouse/Warehouse sources and Power BI definitions require separate Build calls. Build sources first when a model needs their installed metadata; a Workflow may sequence both calls. Reports have Build definitions, not Load/Test nodes.

## Source-item reconciliation

Before installation Build validates source identities, metadata, dependency cycles, selection and bindings, resolves required targets, then reads catalogue/physical state and plans changes. Desktop preflight uses the Fabric inventory before starting Spark. Source items require a catalogue. Their targets must already exist; ordinary Build can create missing selected Power BI items, not an arbitrary source estate.

Planning classifies new/changed source, affected selected descendants, protected work and managed declarations removed from source. Producers precede consumers and removal respects dependency boundaries. Cross-item impact reaches a consumer only when both items are selected. Signatures are equality tokens, not a public digest algorithm. Physical presence/form also matters; matching source does not certify a missing object or adopt an uncertified object solely by name.

Build owns reconciliation inside each selected physical source item, including pruning undeclared Tables, Views, Schemas and Lakehouse Folders. Keep externally owned or irreplaceable data in a separate physical item reached through a physical Shortcut. Unselected items are outside its reconciliation boundary.

`Prohibit rebuild` retains existing protected data against ordinary replacement; it does not prevent first installation, deliberate Wipe or reload. In a mirrored development destination, edited protected borrowed objects can materialise locally: Warehouse CTAS retains source rows, Lakehouse Folders copy files and Delta Tables use shallow clone after shortcut removal/path release. Source data remains unchanged; retained bookmarks remain, changed Load definitions become Pending and failed materialisation blocks certification. Shallow clones initially depend on source data files/retention, not a deep backup. Unprotected mirror replacement retains reset behaviour.

## Power BI deployment modes

Native models and Reports can deploy without a catalogue. Configured/explicit targets resolve physical destinations; ordinary Build can create selected missing items. Selected semantic models deploy and verify readback even if their source signatures are unchanged. Catalogue-free selections redeploy/verify and record no Weaver fixed point.

With a catalogue, verified model/readback metadata and item registrations are published. Required model properties, removals and invalid-measure checks gate certification. A selected model completes deployment/readback before its linked Reports. Catalogue-backed unchanged Report-only Build can skip work; a linked Report-only update requires a suitable certified installed model. Without a catalogue include its linked model in the same selection. Unrelated authored `byConnection` is not reverse mapped.

`--data-source` / Python `data_sources` overrides supported shared-expression mappings. `--bind-data-sources` asks to bind supported sources to existing connections after deployment. Neither creates credentials. Authored files are not rewritten. See the authoritative [mode matrix and binding rules](../power-bi/requirements-and-compatibility.md).

## Read-only preview

```bash
weaver build . --item PowerBI/Parcel --dry-run --workspace-config workspace-dev.yml
```

Preview uses the same canonical plan construction and reads destination state. It reports selected objects, action classifications, destructive consequences, certification/runtime/validation changes and uncertainty. It performs no target mutation, missing-item provisioning, catalogue publication, endpoint refresh or retained bundle write. It does not prove execution-runtime compatibility, service rights to mutate or later target state. Suitable existing targets are required; a missing selected Power BI target is not created by preview.

`--dry-run` and `--bundle-only` are mutually exclusive. `--bundle-path` requires bundle-only mode. Neither preview nor bundle-only mode uses ordinary missing-target provisioning.

## Retained bundle and installation

`--bundle-only` freezes destination-specific targets, payloads and action dependencies and retains a bundle. It still validates source and reads current catalogue/inventories. `--bundle-path` must be absent or an empty directory; otherwise the returned path is a durable temporary-directory bundle. Install validates local directory/`.weaver.zip` input before dispatch. It does not reopen source, retarget or replan. Generate a new bundle if destination/source/bindings changed. See [Build bundle format](../build-bundle-format.md).

Installation schedules ready actions using success dependencies, settlement ordering, resource limits and physical exclusions. Presentation sequences/batches are not global serial barriers. `--concurrency N` / Python `concurrency=N` adds a total invocation cap without changing resource ceilings or dependency rules. Independent work may continue after a known failure; dependent certification is blocked. Uncertain mutation outcomes are failures, not permission to replay blindly.

Spark-backed execution also requires a compatible Weaver Build runtime before dispatch. Desktop execution probes the published Environment for exact client version, plan format, Delta writer and executor capabilities; notebook execution checks the active runtime. This requirement is independent of whether authored Python `read()` runs. Warehouse-only and standalone Power BI Build do not acquire Spark merely for this check. See [Session runtime qualification](session-runtime.md#fabric-environment-qualification).

## State, outcomes and reruns

Before physical replacement, applicable certification/current-state rows are withdrawn or reset. Ordinary replaced loadables reset their bookmark/current Load state; rebuilt validations become Pending. Removed declarations lose current state. Unchanged/unselected source objects keep state; Log and LoadStatistic history remain. Protected mirror materialisation has the retained-bookmark exception above. Resets completed before a later failure are not restored.

Physical/runtime work precedes successful publication. Item/dictionary publication and final certification depend on required work/readback. Partial physical objects may therefore exist without certification. A direct Build retains its installation report outside the temporary bundle and reports its path and action counts. Reported actions are `succeeded`, `failed` or `skipped`; skipped/blocked prerequisites do not certify dependent work.

Pre-plan source/request/state/capability errors raise without an installation result. Captured installation failures return a failed Build result; CLI exits `1`. A succeeded preview, bundle-only or installation result exits `0`. Build has no operation-wide rollback. Source-item fixed points can plan no work after a settled unchanged rerun; do not apply that rule to selected semantic models, catalogue-free deployment or every Report case. Rerunning normal Build snapshots source and replans against the state remaining after failure.

See [`weaver build`](../cli/build.md), [`weaver install`](../cli/install.md), [Catalogue schema](../catalogue-schema.md) and [outcome vocabulary](fault-and-outcome-vocabulary.md).
