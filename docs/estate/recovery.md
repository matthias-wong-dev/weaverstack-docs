# Recover failed work

Recovery is a new operation against the state that remains. Correct the cause, choose the smallest operation that expresses the intended result, and verify the estate afterward. Build, Load, Test and workflows do not roll back completed work when a later step fails.

Use the same project and configuration as the run that failed. The examples use the Parcel estate and `workspace-development.yml`; if you only have the Warehouse project, use `workspace-config.yml` instead. Named examples use `Parcel.StatusEvent`, the Operations Table; Views have no Load of their own.

Start with Health. It shows source data, model refreshes and validations together:

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
weaver build --workspace-config workspace-development.yml
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
weaver load Warehouse/Operations --name 'Parcel[.]StatusEvent' --descendants --dry-run --workspace-config workspace-development.yml
```

Remove only `--dry-run` if the selection is correct. This is a whole-name regex, not an exact-name shortcut. Expansion stays inside named items, and a descendant's omitted sibling prerequisite is not automatically refreshed. [Run part of an estate](selective-runs.md) gives the deterministic example and both directions. This command does not request reconstruction.

## Reconstruct a Table

Reload **empties each reached selected Table and resets its bookmark/progress before loading it**. Use it only when reconstruction from empty is intended:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]StatusEvent' --reload --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "130-reload-preview", "title": "Reload preview · one Table"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Reload preview · one Table">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           2.7s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
  Execute                                                                                                  0.0s
<span class="terminal-status-green">✓ Load (dry run)                                                                                           2.7s</span>

<span class="terminal-status-green">plan (reload) succeeded: Warehouse/Operations</span>

    validated                load:Warehouse/Operations/Parcel.StatusEvent

Plan
    1 selected
</code></pre>
</figure>
<!-- /cli-capture -->

The preview names exactly the Tables that will be emptied. Then run it:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]StatusEvent' --reload --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "131-reload", "title": "Reload · reconstruct StatusEvent from empty"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Reload · reconstruct StatusEvent from empty">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.7s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
→   Load Warehouse/Operations/Parcel.StatusEvent
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +3 ~0 -0 !0)                                    2.5s</span>
  Execute                                                                                                  3.2s
  Record what the run did                                                                                  0.4s
<span class="terminal-status-green">✓ Load                                                                                                     6.3s</span>

<span class="terminal-status-green">load (reload) succeeded: Warehouse/Operations</span>

Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   3
    inserted               3
    updated                0
    deleted                0
    rejected               0

  Workflow: e0d44df3ceb54cb48ac6f0446ab371f7
</code></pre>
</figure>
<!-- /cli-capture -->

The three events were inserted into an empty Table (`+3`), each with a new `Row insert datetime`, and the Table's bookmark restarted from that Load.

Plain named Reload follows its matching selection without expansion. Ancestors/descendants can deliberately enlarge the reached set and therefore enlarge the destructive scope. Folders cannot be reloaded; stale and reload cannot be combined. If execution fails after the reset or emptying step, the previous Table contents are not restored automatically.

## Continue partial work only when its output is usable

`--fault-tolerant` lets independent work continue and can publish valid rows/files alongside retained rejects. It does not turn failures into success. A descendant may run after an upstream execution failure settles and read whatever state that failure left; invalid or unresolved upstream work still blocks descendants. Review node outcomes before using partial output. Rejecting loads do not establish a clean bookmark boundary.

```bash
weaver load Warehouse/Operations --stale --fault-tolerant --workspace-config workspace-development.yml
```

A delete/update stability-threshold breach still refuses the change without modifying the target. Fault tolerance changes how that refusal is returned, not whether it is applied. If the large change is intended, review it and explicitly waive those thresholds for this invocation:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]StatusEvent' --ignore-stability-threshold --workspace-config workspace-development.yml
```

This flag does not waive null or unique-key checks, change definitions or reset bookmarks. An incremental merge violating an existing unique key is fatal even with fault tolerance. See [rejected data and thresholds](../advanced/partial-failures-rejected-data-and-thresholds.md) and [Load failure policy](../reference/operation-behaviour/load.md#outcomes-and-failure-policy) before choosing continuation.

## Rerun validation

Correct the data, runtime or validation condition. Build edits before catalogue-mode Test; source/file-mode Test can use the edited validation without recording installed history. For the installed route:

```bash
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Test has no rollback step. A failed validation remains the current finding until a later run records another outcome.

## Recover a model or Report

Keep this same project. If you added the [native and source-backed models](../semantic-models/managed-sources.md), use their existing bindings in `workspace-development.yml`; do not replace the independent pipelines or native model.

A semantic-model refresh is Load work. Fix its source, connection or refresh condition, then rerun Load. A DAX finding is validation work: correct the model, data or query, then rerun Test. Their installed results appear in the same Health report as Lakehouse and Warehouse work.

A definition or binding change needs Build instead. Select the model and linked Report through their project, after any source-data Build:

```bash
weaver build --item PowerBI/Parcel --workspace-config workspace-development.yml
weaver load SemanticModel/Parcel --workspace-config workspace-development.yml
weaver test SemanticModel/Parcel --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

These commands assume the Parcel model and Report are in the project and configured. Reports have no separate Load or Test; inspect the Report’s binding and rendering after recovering its model. See [Deploy models and Reports](../reports/deploy.md) and [Connect a model to source data](../semantic-models/managed-sources.md).

## Refresh a mirrored baseline

Re-mirror **empties and reconstructs the destination catalogue and every selected destination target**, replacing local materialisations in that boundary. The source items remain untouched. Use it only to replace a mirrored development estate with a fresh source baseline. Run it with the mirror configuration from [Develop using Mirror](mirror.md), not the estate's own configuration:

```bash
weaver mirror --workspace-config workspace-mirror.yml
```

<!-- cli-capture: {"id": "142-remirror", "title": "Mirror · replace the development baseline"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Mirror · replace the development baseline">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Mirror

Workspace              Parcel Development
Source catalogue       Warehouse/Catalogue
Destination catalogue  Warehouse/CatalogueDev
Targets
  Warehouse/Operations → Warehouse/OperationsDev

Empty these targets? This cannot be undone. [y/N] y

Mirror

  Planning the mirror                                                                                      1.5s
→   Wipe Warehouse/CatalogueDev · 1 action
→   Wipe Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Wipe Warehouse/CatalogueDev · 1 action                                                                 1.2s</span>
→   Warehouse/CatalogueDev · Catalogue: creating schemas · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: creating schemas · 1 action                                        0.0s</span>
→   Warehouse/CatalogueDev · Catalogue: building objects · 24 actions
<span class="terminal-status-green">✓   Wipe Warehouse/OperationsDev · 1 action                                                                1.3s</span>
→   Reconstruct Warehouse/OperationsDev · 2 actions
→   Recreate views over other items in Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Reconstruct Warehouse/OperationsDev · 2 actions                                                        0.2s</span>
<span class="terminal-status-green">✓   Recreate views over other items in Warehouse/OperationsDev · 1 action                                  0.5s</span>
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: building objects · 24 actions                                      5.8s</span>
→   Warehouse/CatalogueDev · Catalogue: updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: updating catalogue definitions · 1 action                          4.4s</span>
→   Warehouse/CatalogueDev · Catalogue: finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: finalising catalogue · 1 action                                    0.7s</span>
→   Recreate catalogue views in Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Recreate catalogue views in Warehouse/OperationsDev · 1 action                                         0.1s</span>
→   Copy procedures and functions into Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Copy procedures and functions into Warehouse/OperationsDev · 1 action                                  0.3s</span>
→   Warehouse/CatalogueDev · Forking the catalogue and binding items · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Forking the catalogue and binding items · 1 action                            7.9s</span>
  Mirroring                                                                                               20.5s
<span class="terminal-status-green">✓ Mirror                                                                                                  23.4s</span>

Mirror complete
  Catalogue  Warehouse/Catalogue → Warehouse/CatalogueDev
  1 item mirrored
  2 destinations emptied
</code></pre>
</figure>
<!-- /cli-capture -->

Mirror shows the source catalogue, destination catalogue and target bindings before it asks. Confirm only if that boundary is correct. It has no dry-run mode; declining leaves the destinations unchanged.

Any object that had become local in OperationsDev is borrowed again, so its development-only changes are gone. Run Health against the mirror configuration, then Build any project changes that should become local again:

```bash
weaver health --item Warehouse/Operations --workspace-config workspace-mirror.yml
```

## Wipe only when the desired state is empty

Wipe is not rollback and is not the normal response to a failed Build or Load. It empties selected Lakehouse/Warehouse contents, including unmanaged content, and **normally also empties the resolved catalogue even when only one Warehouse is named**. No Fabric item is deleted. Use it only when that complete resolved boundary should end empty; Reports cannot be wiped.

To empty this physical target while retaining the catalogue and removing that target’s claims, request `--unbind` explicitly and inspect the full settled plan:

```bash
weaver wipe Warehouse/Operations --unbind --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "150-wipe-preview", "title": "Wipe preview · one Warehouse, catalogue kept"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Wipe preview · one Warehouse, catalogue kept">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Wipe on Parcel Development

Empty
  Warehouse/Operations

Catalogue
  Warehouse/Catalogue   preserved; claims for Warehouse/Operations unbound

Nothing was changed.
</code></pre>
</figure>
<!-- /cli-capture -->

If the plan is the empty state you want, run it without `--dry-run` and confirm:

```bash
weaver wipe Warehouse/Operations --unbind --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "151-wipe", "title": "Wipe · empty Operations and remove its claims"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Wipe · empty Operations and remove its claims">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Wipe on Parcel Development

Empty
  Warehouse/Operations

Catalogue
  Warehouse/Catalogue   preserved; claims for Warehouse/Operations unbound

Empty 1 item(s)? This cannot be undone. [y/N] y

Wipe

→   Wipe Warehouse/Operations · 1 action
<span class="terminal-status-green">✓   Wipe Warehouse/Operations · 1 action                                                                   1.6s</span>
→   Unbind catalogue claims in Warehouse/Catalogue · 1 action
<span class="terminal-status-green">✓   Unbind catalogue claims in Warehouse/Catalogue · 1 action                                              6.1s</span>
  Emptying Warehouse/Operations                                                                            7.8s
<span class="terminal-status-green">✓ Wipe                                                                                                     9.9s</span>

Wipe complete

  Warehouse/Operations        emptied
  Warehouse/Catalogue         catalogue preserved, claims unbound
</code></pre>
</figure>
<!-- /cli-capture -->

Operations is now an empty Warehouse with no Weaver claims; the catalogue still holds Landing and any other items. To bring it back, Build and Load it as on first deployment:

```bash
weaver build --item Warehouse/Operations --workspace-config workspace-development.yml
weaver load Lakehouse/Landing Warehouse/Operations --workspace-config workspace-development.yml
```

The first Build into a just-emptied Warehouse can fail with a Fabric `Snapshot isolation transaction failed` error while the service settles its metadata. Rerun the Build; it reconciles from the state that remains.

Wipe target arguments are physical Fabric items, not logical Weaver item identities. Naming no target selects the physical estate recorded by the catalogue and retains the normal catalogue-removal default; preview that full boundary before authorising it. Semantic-model-only named Wipe instead resets the selected model definitions and retains the catalogue while removing their claims; it does not empty their sources or shared connections. Wipe is not transactional: completed or independent mutations remain after failure. Inspect remaining state before retrying uncertain destructive work.

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
