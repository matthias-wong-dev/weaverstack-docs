# Recover failed work

Recovery is a new operation against the state that remains. Correct the cause, choose the smallest operation that expresses the intended result, and verify the estate afterward. Build, Load, Test and workflows do not roll back completed work when a later step fails.

Start with Health against the same workspace configuration used by the failed command:

```bash
weaver health --workspace-config workspace-development.yml
```

## Choose the recovery

| Intended result | Operation |
| --- | --- |
| Reconcile corrected project source | Check, then rerun Build |
| Run failed, pending or stale data work | Rerun Load, normally with `--stale` for non-Green work |
| Reconstruct a selected Table from empty | Named Load with `--reload` |
| Re-evaluate installed validations | Rerun Test |
| Replace development with a fresh source baseline | Re-mirror after reviewing the destination plan |
| Leave selected physical targets or the estate empty | Wipe after a dry run |

## Reconcile corrected source

After correcting source or a Fabric condition:

```bash
weaver check
weaver build . --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Build reads the project and installed estate again and reconciles its selection. It does not resume a failed Build. Completed physical actions from the earlier attempt may still be present, so inspect the new report and Health result.

## Rerun failed or stale Load work

After correcting the data, runtime or permission condition, preview and run non-Green loadable work:

```bash
weaver load \
  --stale \
  --dry-run \
  --workspace-config workspace-development.yml

weaver load \
  --stale \
  --workspace-config workspace-development.yml
```

This uses the definitions last installed by Build. Build first if the correction changed project source. Green upstream work is not added merely because a selected descendant reads it.

## Reconstruct a Table

Use reload only when the intended result is to empty and rebuild a specific installed Table from its initial bookmark:

```bash
weaver load Warehouse/Operations \
  --name Parcel.Status \
  --reload \
  --dry-run \
  --workspace-config workspace-development.yml

weaver load Warehouse/Operations \
  --name Parcel.Status \
  --reload \
  --workspace-config workspace-development.yml
```

Reload follows the exact named selection. It does not add dependencies or downstream work, and Folders cannot be reloaded. If execution fails after the reset or emptying step, the previous Table contents are not restored automatically.

## Rerun validation

Correct the data, runtime or validation condition, Build any edited validation source, then rerun installed validations:

```bash
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Test has no rollback step. A failed validation remains the current finding until a later run records another outcome.

## Refresh a mirrored baseline

Re-mirror only when the intended result is to replace the development baseline with the configured source estate.

```bash
weaver mirror --workspace-config workspace-development.yml
```

Inspect the displayed source catalogue, destination catalogue and target bindings. Confirm if that boundary is correct; decline if it is not. Mirror has no dry-run mode, and declining leaves the destinations unchanged.

Mirror reconstructs the destination catalogue and selected targets. Local materialisations in that boundary are replaced; they are not preserved as a fallback. Run Health after Mirror, then Build any project changes that should become local.

## Wipe only when the desired state is empty

Wipe is not rollback and is not the normal response to a failed Build or Load. Use it only when selected physical targets, or the complete installed estate, should end empty.

Preview the physical target boundary:

```bash
weaver wipe Warehouse/ParcelOperationsDev \
  --dry-run \
  --workspace-config workspace-development.yml
```

If the displayed plan is the desired empty state, rerun without `--dry-run` and confirm it. Wipe target arguments are physical Fabric items, not logical Weaver item identities. Naming no target selects the physical estate recorded by the catalogue, so preview that form before authorising it.

Exact Wipe catalogue handling, unbinding and authorisation rules are in [Wipe operation behaviour](../reference/operation-behaviour/wipe.md).

## Verify the result

After any recovery:

1. inspect the operation report and workflow identifier;
2. rerun Health with its normal physical inventory check;
3. rerun Test when recovered data changes validation inputs; and
4. use read-only catalogue history when the command report is not enough.

```bash
weaver health --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
```

Health establishes Weaver's installed and operational state. Tests and domain queries establish whether the recovered data meets its expectations. See [Fault tolerance](../core-concepts/fault-tolerance.md) for partial-state reasoning and [Operation behaviour](../reference/operation-behaviour/index.md) for exact rerun and destructive boundaries.
