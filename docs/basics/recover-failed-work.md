# Recover failed work

Recovery is a new operation against the state that remains. Correct the cause, choose the smallest operation that expresses the intended result, and verify the estate afterward. Build, Load, Test and workflows do not roll back completed work when a later step fails.

Start with one Health report for the managed estate, using the failed command’s workspace configuration. It combines source-data state with registered model refreshes and validations:

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

## Include related work deliberately

After correcting the cause, preview a seed and its downstream work:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Status' --descendants --dry-run --workspace-config workspace-development.yml
```

Remove only `--dry-run` if the selection is correct. This is a whole-name regex, not an exact-name shortcut. Expansion stays inside named items, and a descendant's omitted sibling prerequisite is not automatically refreshed. [Run part of an estate](../advanced/run-part-of-an-estate.md) gives the deterministic example and both directions. This command does not request reconstruction.

## Reconstruct a Table

Use reload only when the intended result is to empty and rebuild a specific installed Table from its initial bookmark:

```bash
weaver load Warehouse/Operations \
  --name 'Parcel[.]Status' \
  --reload \
  --dry-run \
  --workspace-config workspace-development.yml

weaver load Warehouse/Operations \
  --name 'Parcel[.]Status' \
  --reload \
  --workspace-config workspace-development.yml
```

Plain named Reload follows its matching selection without expansion. Ancestors/descendants can deliberately enlarge the reached set and therefore enlarge the destructive scope. Folders cannot be reloaded; stale and reload cannot be combined. If execution fails after the reset or emptying step, the previous Table contents are not restored automatically.

## Rerun validation

Correct the data, runtime or validation condition. Build edits before catalogue-mode Test; source/file-mode Test can use the edited validation without recording installed history. For the installed route:

```bash
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Test has no rollback step. A failed validation remains the current finding until a later run records another outcome.

## Recover a model or Report

A semantic-model refresh is Load work. Fix its source, connection or refresh condition, then rerun Load. A DAX finding is validation work: correct the model, data or query, then rerun Test. Their installed results appear in the same Health report as Lakehouse and Warehouse work.

A definition or binding change needs Build instead. Select the model and linked Report through their project, after any source-data Build:

```bash
weaver build . --item PowerBI/Parcel --workspace-config workspace-development.yml
weaver load SemanticModel/Parcel --workspace-config workspace-development.yml
weaver test SemanticModel/Parcel --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

These commands assume the Parcel model and Report are in the project and configured. Reports have no separate Load or Test; inspect the Report’s binding and rendering after recovering its model. See [Deploy models and Reports](power-bi/deploy-pbip.md) and [Connect a model to source data](power-bi/fabric-integration.md).

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

## Remove a claim without emptying the item

Unbind removes the catalogue's ownership claims for the resolved physical items; it does not delete those physical items or contents. It is not Wipe, rollback or a way to repair rows by hand. Review the exact scope and confirmation in the [Unbind reference](../reference/operation-behaviour/unbind.md).

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
