# Troubleshoot an estate

Start from the symptom the operator can observe. Keep the selected workspace configuration beside every remote command so diagnosis does not cross estates accidentally.

## Prerequisites

- [Install Weaver](../get-started/installation.md) and confirm `weaver --version` works.
- Know the workspace-configuration file used by the failing command.
- Preserve the complete command report, exit status and workflow identifier when one is printed.
- Use read-only access to the catalogue Warehouse for deeper investigation. Do not repair catalogue rows manually.

The examples use `workspace-production.yml`, `Lakehouse/Landing` and `Warehouse/Operations` from a neutral parcel estate.

## `weaver check` rejects the project

Run Check from the project root before investigating Fabric:

```bash
weaver check
```

Check parses Weaver documents, identities, metadata, SQL validation shapes and dependency relationships without contacting Fabric. A success prints `Project valid.`. A failure is therefore a project-source problem, not proof of a workspace outage.

Use the first reported file, identity or dependency error as the correction boundary. Common tasks are:

- make a path agree with its declared `Schema.Object` identity;
- correct an unsupported or misspelled metadata key;
- add a missing logical Shortcut target or correct its full logical identity;
- remove a dependency cycle;
- correct the result-query shape of a SQL Test or Assumption.

Rerun Check after each correction. Do not proceed to Build until it succeeds. Check does not execute authored Python or SQL and cannot prove remote imports, permissions or object creation.

For machine-readable reporting:

```bash
weaver check --json
```

JSON changes output form, not validation scope.

## The workspace cannot be reached or authentication fails

Probe the workspace independently of the project:

```bash
weaver doctor --workspace "Parcel Operations"
```

Doctor requires an explicit workspace name. It does not read `workspace-production.yml`, a catalogue binding or an Environment binding. It reports authentication, Fabric REST and the available TDS, OneLake and Livy probes. Checking a workspace with a Lakehouse can start a Fabric Spark session and take about a minute.

Interpret the boundary that failed:

- **Authentication**: confirm the intended credential path. Interactive CLI use can fall back to browser sign-in; `--non-interactive` omits browser sign-in.
- **Fabric REST**: confirm the workspace spelling, tenant and permission to discover it.
- **Warehouse TDS**: confirm SQL endpoint availability and permission on the Warehouse Doctor names.
- **OneLake**: confirm storage access to the Lakehouse Doctor names.
- **Fabric Spark / Livy**: confirm the capacity and workspace can start a Spark session.

A successful Doctor report proves only the probes it ran against the named workspace. It does not prove that a later command selected the intended workspace configuration, catalogue, targets or Environment.

## The command uses the wrong workspace, catalogue or target

Repeat the failing command with an explicit configuration path:

```bash
weaver health \
  --workspace-config workspace-production.yml
```

Then inspect:

1. `workspace`, `catalogue` and `targets` in that file;
2. any explicit `--workspace`, `--catalogue`, `--environment` or Build `ITEM=TARGET` override;
3. `_.Installation` for the logical item and its installed physical target.

Build reads physical target bindings from workspace configuration. Load, Test and Health read installed bindings from the selected catalogue. A physical Fabric item name is not a Load or Test item selection. Correct the configuration or Build binding rather than renaming logical project directories to match a physical target.

Use one configuration consistently through Check, Build, Load, Test and Health. Check itself is local and does not read that binding, but keeping the command sequence explicit makes an estate switch visible.

## Load or Test says an item or object is not installed

Confirm installation state:

```bash
weaver health \
  --item Warehouse/Operations \
  --workspace-config workspace-production.yml
```

Inspect `_.Installation` for the logical item and `_.Registry` for the object. If the item has never been installed, select it in Build:

```bash
weaver check
weaver build . \
  --item Warehouse/Operations \
  --workspace-config workspace-production.yml
```

If a consumer uses a logical Shortcut, the source document must resolve locally and the source item must have an installation when Build needs its physical binding. On a first installation, Build the producer and consumer items together. Dependencies do not widen Build selection.

Do not write `_.Installation` or `_.Registry` by hand. Build is the reconciliation operation that publishes those claims.

## Build fails or leaves the estate inconsistent

Read the Build report in order. Completed actions may already have changed physical objects; later actions can be failed or skipped. Build does not roll the operation back and does not certify a failed rebuild as successful.

Separate three questions:

1. **Did Check pass?** If not, correct source first.
2. **Did preflight find the configured Fabric items?** Confirm the catalogue and each selected target exist with the expected Fabric item kind.
3. **Which Build action first failed?** Correct that declaration, permission or Fabric condition rather than acting on the skipped remainder.

Then rerun the same selected Build:

```bash
weaver build . \
  --item Warehouse/Operations \
  --workspace-config workspace-production.yml
```

The next Build reconciles the state it finds; it does not resume the previous report. Follow it with Health. If Health says the catalogue is incomplete or incompatible, preserve the report and inspect the named catalogue table. Do not use a scoped Build or manual SQL writes as an assumed repair for damaged catalogue state.

## Load reports failed, blocked or pending work

Preview the same boundary before retrying:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-production.yml \
  --dry-run
```

Use the per-object outcomes:

- **failed**: the selected work or its dispatch failed; correct the reported data, code, permission or runtime condition;
- **blocked**: inspect the named upstream failure or unresolved dependency first;
- **pending**: the work did not execute, commonly because fail-fast scheduling stopped after another failure;
- **succeeded with rejects**: inspect the rejection evidence and row counts; the bookmark does not advance after a load with rejects.

A retry is a new Load against the state left by the previous run. Without `--fault-tolerant`, scheduling stops after the first execution failure. With it, independent branches continue and downstream work may read the state left by a settled upstream failure. Choose that policy deliberately; it does not turn partial work into success.

Use `_.LoadStatus` for the current outcome, `_.Log` for settled work under the workflow identifier and `_.LoadStatistic` for recorded data movement. A blocked object can have status without a load statistic because its data work did not run.

## Test fails or could not run

A failed validation ran and found discrepancies or violations. A validation that could not run is an execution problem. Both exit non-zero, but they require different actions.

Run one installed validation for diagnostic rows:

```bash
weaver test Warehouse/Operations \
  --name Parcel.StatusMatches \
  --workspace-config workspace-production.yml
```

For a failure, inspect the missing, unexpected or violation rows and correct either the data-producing work or the validation expectation. For a validation that could not run, correct the reported query, permission, binding or runtime condition.

If the validation source changed, Check and Build it before rerunning Test. Installed Test does not read the edited source file. `test --file` is a direct source-file evaluation and does not install the validation or publish estate evidence.

Use `_.TestStatus` for the current installed outcome and `_.Log` for settled execution detail. `_.TestDictionary` answers what Build installed; it does not hold the latest result.

## Python work reports an Environment or import problem

First identify whether the selected installed work uses Python in Fabric:

- Warehouse T-SQL work does not need a Fabric Environment;
- Lakehouse Spark SQL can use the workspace's default Spark runtime;
- Python Table, Folder, Test and Assumption work needs a configured, published Fabric Environment containing Weaver.

For Python work, verify all three controls:

1. the selected workspace configuration names `environment`;
2. that Environment exists in the intended workspace or is fully qualified as `Workspace/Environment`;
3. its latest definition was published successfully.

Publish or republish it when needed:

```bash
weaver fabric environment publish \
  --path Environment/ParcelRuntime.Environment \
  --workspace-config workspace-production.yml
```

Then rerun the failed Load or Test. Publication does not resume it. A successful local Check does not prove that Fabric attached the Environment or imported Weaver; only live execution establishes that outcome. See [Workspaces and Environments](environments.md) for the full boundary.

## Health is Amber because work is pending or stale

Run Health and a matching stale dry run:

```bash
weaver health \
  --workspace-config workspace-production.yml

weaver load Lakehouse/Landing Warehouse/Operations \
  --stale \
  --dry-run \
  --workspace-config workspace-production.yml
```

A rebuilt loadable object returns to Pending until a clean Load settles. A non-static successful load older than Health's freshness threshold is stale. `load --stale` selects loadable objects whose Load health is not Green; it does not select Views as work or rerun Tests.

If Test state is Pending because its validation was rebuilt, run Test for the owning item. If Health says a validation has a stale dependency, Load the affected data first, then rerun Test. To change freshness, pass the same zoned `--as-of` instant to Health and to `load --stale`.

## A Shortcut or mirrored object points somewhere unexpected

Establish whether the object is local, a declared Shortcut or borrowed mirror state:

- `_.Shortcut` records installed logical and physical Shortcut edges;
- `_.Dependency` records the relationship Build resolved;
- `_.Mirror` records objects still borrowed from a mirror source;
- no matching `_.Mirror` row means the installed object is local.

For a logical Shortcut, correct the source Weaver identity and Build every selected producer or consumer that should change. For a physical Shortcut, verify the external workspace, item and Fabric permission; Weaver has no managed producer to order from that address.

In a mirrored development estate, unchanged borrowed objects continue to read the source estate. Build materialises changed borrowed objects and affected selected descendants locally, then removes their `_.Mirror` rows. If the intended recovery is a fresh source baseline rather than a local Build, use the mirror-refresh procedure in [Recovery](recovery.md); it replaces the destination boundary.

Never delete a Shortcut's source to repair its local destination. Wiping, pruning or replacing a local Shortcut is not authority to mutate the referenced object.

## Decide between the catalogue and logs

Use the narrowest evidence surface:

| Question | Inspect |
| --- | --- |
| What is installed and where? | `_.Installation`, `_.Registry`, declaration dictionaries |
| What is the current Load or Test result? | `_.LoadStatus`, `_.TestStatus` |
| What settled during one reported workflow? | `_.Log` filtered by the workflow identifier |
| What data movement was recorded? | `_.LoadStatistic` |
| Is the object borrowed or connected through a Shortcut? | `_.Mirror`, `_.Shortcut` |
| Did parsing, planning, authentication or preflight fail before work settled? | The command's stderr or JSON report |

The catalogue records installed and settled operational state; it is not a copy of every terminal message. Preserve command output for failures that occur before a catalogue write.

Use [Weaver operations](../core-concepts/weaver-operations.md) to identify the lifecycle stage, [Catalogue](../core-concepts/catalogue.md) for table meanings, [Development cycle](../core-concepts/development-cycle.md) for mirrored estates, [Dependencies](../core-concepts/dependencies.md) for selection and ordering, [Fault tolerance](../core-concepts/fault-tolerance.md) for partial work, the [CLI reference](../reference/cli.md) for exact options and [Contracts](../contracts/index.md) for defined behaviour.