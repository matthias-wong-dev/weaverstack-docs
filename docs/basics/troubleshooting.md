# Troubleshooting

Use the same workspace configuration as the failed command. Preserve its report, exit status and workflow identifier, and do not edit catalogue rows to repair state.

## Check fails

Run Check from the project root:

```bash
weaver check
```

Check is local. Correct the first reported path, identity, metadata, SQL shape or dependency error, then rerun it. Do not proceed to Build until Check succeeds.

A successful Check proves that Weaver can parse the project. It does not execute authored code or prove Fabric access, permissions or remote Python imports.

## Build fails

Read the Build report in action order. Completed actions may already have changed physical objects; Build does not roll them back when a later action fails.

1. Run `weaver check` and correct source errors.
2. Confirm that the selected configuration names the intended catalogue and targets.
3. Correct the first failed declaration, permission or Fabric condition.
4. Rerun the same Build selection.
5. Run Health.

```bash
weaver build . --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

The rerun reconciles the state it finds; it does not resume the previous report. If Health reports an incomplete or incompatible catalogue, preserve the evidence rather than writing catalogue tables manually or using Wipe as an ordinary Build repair.

## Load fails

Use the report to distinguish failed, blocked and pending work. Correct the reported data, code, runtime or permission condition, then preview and rerun the intended item boundary:

```bash
weaver load \
  --dry-run \
  --workspace-config workspace-development.yml

weaver load \
  --workspace-config workspace-development.yml
```

A retry is a new Load against the state left by the previous run. If source changed during the correction, Build it first. Without fault tolerance, the first execution failure stops new scheduling; completed work remains applied. See [Recover failed work](recover-failed-work.md) for stale catch-up and deliberate Table reconstruction.

## Test cannot run

A validation that could not run is different from a validation that ran and found bad data. Correct the reported query, binding, permission or runtime condition.

If the Test or Assumption source changed, Check and Build its owning item before rerunning Test:

```bash
weaver check
weaver build . --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
```

Test executes installed validations, not edited source files. A validation that ran and failed is a data finding; investigate the diagnostic rows and the data-producing work, then rerun Test after correction.

## Health is Amber

Amber usually means work is pending or stale rather than failed. Run Health, catch up non-Green Load work, run validations and inspect again:

```bash
weaver health --workspace-config workspace-development.yml
weaver load --stale --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

A rebuilt Table or Folder remains Pending until Load settles. A rebuilt validation remains Pending until Test runs. If a validation is stale because its inputs changed, Load the data first and then rerun Test.

## Health is Red

Read the section and finding that caused Red:

- **Load**: correct the failed or blocked work, then rerun the intended Load boundary.
- **Tests**: correct the data or validation expectation, then rerun Test.
- **Build**: reconcile the source and physical installation with Build; missing or contradictory catalogue state is not repaired by Load or Test.

Run Health again after the recovery operation. Red is not cleared by a successful unrelated command.

## Runtime or authentication fails

Probe the named workspace independently of the project:

```bash
weaver doctor --workspace "Parcel Development"
```

Doctor reports the authentication and Fabric capabilities it could probe. It does not read workspace configuration or prove that a later command selected the intended catalogue, targets or Environment.

For authentication failures, confirm the credential path and workspace permission. Non-interactive execution does not fall back to browser sign-in.

For Python Load or Test work, confirm that the selected workspace configuration names an Environment, that the Environment exists, and that its latest definition was published successfully:

```bash
weaver fabric environment publish \
  --path Environment/ParcelRuntime.Environment \
  --workspace-config workspace-development.yml
```

Then rerun the failed Load or Test; publication does not resume it. Warehouse T-SQL work does not require a Fabric Environment, and Spark SQL can use the workspace's default Spark runtime. See [Configure a workspace and Python runtime](workspace-and-python-runtime.md).

For exact command outcomes and catalogue evidence, use [Operation behaviour](../reference/operation-behaviour/index.md) and [Catalogue](../core-concepts/catalogue.md).
