# Develop using Mirror

Borrow an installed estate’s data for development, then materialise only the objects your changes need. Keep the same project documents and logical identities while the development configuration selects different physical targets.

Use Mirror only after the [ordinary development loop](development-cycle.md) is understood. **It empties and reconstructs the destination catalogue and every selected destination target**, including local materialisations there. Source items remain untouched. It is a baseline reset, not an iteration command.

## Prepare existing destinations in the same workspace

Mirror works between existing Fabric items in one workspace. Here the source is the estate you have been building: the `Catalogue` Warehouse and the `Operations` Warehouse it records. Mirror needs an empty destination for each, and it does not create Fabric items.

1. In the Fabric portal, create two Warehouses in `Parcel Development`: `CatalogueDev` and `OperationsDev`.
2. Add a separate configuration beside the project. Keep `workspace-development.yml` as it is; this file describes the mirrored copy:

```yaml title="workspace-mirror.yml"
workspace: Parcel Development
catalogue: Warehouse/CatalogueDev
mirror: Warehouse/Catalogue

targets:
  Warehouse/Operations: OperationsDev
```

`mirror` names the source catalogue; `catalogue` and `targets` name the destinations. The source physical item, `Operations`, comes from the source catalogue's recorded binding, not from this file. Only the items listed under `targets` are rebound to development copies.

Run Mirror:

```bash
weaver mirror --workspace-config workspace-mirror.yml
```

Weaver shows the source catalogue, destination catalogue and each target mapping, then asks once before emptying the destinations. Compare the plan with the names above; answer `y` only if they match. Declining changes nothing, and Mirror has no dry-run mode.

<!-- cli-capture: {"id": "140-mirror", "title": "Mirror · fork the catalogue into development"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Mirror · fork the catalogue into development">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Mirror

Workspace              Parcel Development
Source catalogue       Warehouse/Catalogue
Destination catalogue  Warehouse/CatalogueDev
Targets
  Warehouse/Operations → Warehouse/OperationsDev

Empty these targets? This cannot be undone. [y/N] y

Mirror

  Planning the mirror                                                                                      1.8s
→   Wipe Warehouse/CatalogueDev · 1 action
→   Wipe Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Wipe Warehouse/CatalogueDev · 1 action                                                                 0.7s</span>
→   Warehouse/CatalogueDev · Catalogue: creating schemas · 1 action
<span class="terminal-status-green">✓   Wipe Warehouse/OperationsDev · 1 action                                                                0.7s</span>
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: creating schemas · 1 action                                        0.0s</span>
→   Warehouse/CatalogueDev · Catalogue: building objects · 24 actions
→   Reconstruct Warehouse/OperationsDev · 2 actions
→   Recreate views over other items in Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Reconstruct Warehouse/OperationsDev · 2 actions                                                        0.2s</span>
<span class="terminal-status-green">✓   Recreate views over other items in Warehouse/OperationsDev · 1 action                                  0.4s</span>
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: building objects · 24 actions                                      6.9s</span>
→   Warehouse/CatalogueDev · Catalogue: updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: updating catalogue definitions · 1 action                          4.4s</span>
→   Warehouse/CatalogueDev · Catalogue: finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: finalising catalogue · 1 action                                    0.7s</span>
→   Recreate catalogue views in Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Recreate catalogue views in Warehouse/OperationsDev · 1 action                                         0.1s</span>
→   Copy procedures and functions into Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Copy procedures and functions into Warehouse/OperationsDev · 1 action                                  0.3s</span>
→   Warehouse/CatalogueDev · Forking the catalogue and binding items · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Forking the catalogue and binding items · 1 action                            7.8s</span>
  Mirroring                                                                                               20.9s
<span class="terminal-status-green">✓ Mirror                                                                                                  24.4s</span>

Mirror complete
  Catalogue  Warehouse/Catalogue → Warehouse/CatalogueDev
  1 item mirrored
  2 destinations emptied
</code></pre>
</figure>
<!-- /cli-capture -->

Mirror emptied CatalogueDev and OperationsDev and rebuilt them from the source estate. Unchanged objects start as borrowed source data: OperationsDev presents Operations' Tables through local Views, and `_.Mirror` in CatalogueDev lists every borrowed object. The project's logical items and Weaver documents are unchanged.

Inspect the baseline:

```bash
weaver health --workspace-config workspace-mirror.yml
```

<!-- cli-capture: {"id": "141-mirror-health", "title": "Health · the mirrored development estate"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · the mirrored development estate">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           3.4s
  Read the mirrored catalogue                                                                              1.9s
  Check installed items                                                                                    0.2s
  Read installed objects                                                                                  17.1s
<span class="terminal-status-green">✓ Health                                                                                                  22.6s</span>

<span class="terminal-status-amber">Weaver Health  Amber</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 1m ago
<span class="terminal-status-green">  15 succeeded</span>

<span class="terminal-status-amber">Tests   Amber</span>
<span class="terminal-status-green">  4 succeeded</span>
<span class="terminal-status-amber">  Amber  Warehouse/Operations/Parcel.CurrentStatusMatches</span>
<span class="terminal-status-green">          Warehouse/Operations/Parcel.StatusEvent has been loaded since this validation passed</span>
<span class="terminal-status-amber">  Amber  Warehouse/Operations/Parcel.StatusIsKnown</span>
<span class="terminal-status-green">          Warehouse/Operations/Parcel.StatusEvent has been loaded since this validation passed</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (67 objects)

Slowest loads
  Warehouse/Operations/Parcel.LakehouseCurrentStatus  6.6s
  Warehouse/Operations/Parcel.Daily                   4.9s
  Warehouse/Operations/Parcel.LiveStatus              2.5s
  Warehouse/Operations/Parcel.StatusEvent             2.5s
  Warehouse/Operations/Reference.Depot                2.2s

Largest changes
  Warehouse/Operations/Parcel.StatusEvent     read 3  +3 ~0 -0 !0
  Warehouse/Operations/Parcel.Daily           read 1  +1 ~0 -1 !0
  Warehouse/Operations/Parcel.Events          read 1  +1 ~0 -1 !0
  Warehouse/Operations/Parcel.RawEvents       read 1  +1 ~0 -1 !0
  Warehouse/Operations/Parcel.Summary         read 1  +1 ~0 -1 !0
</code></pre>
</figure>
<!-- /cli-capture -->

Health reads borrowed objects' Load state from the source catalogue, so the mirrored estate starts with the source's history and findings.

See [Mirrors](../core-concepts/mirrors.md) for borrowed and local data. Exact Mirror selection, authorisation and failure boundaries are in [Mirror operation behaviour](../reference/operation-behaviour/mirror.md).

## Change only the work that needs to become local

After a successful Mirror, keep the same project source and pass `--workspace-config workspace-mirror.yml` to Build, Load, Test and Health. The [development cycle](development-cycle.md#edit-and-iterate) is unchanged.

Build compares source with copied installed declarations. Unchanged borrowed objects stay borrowed. A changed selected object, or an affected selected descendant, becomes local after successful installation and loses its `_.Mirror` row. Items outside the Build selection do not materialise just because another item changed. Load operates local materialisations; borrowed data continues to be loaded and owned at its source.

For example, if you added the [selection example's](selective-runs.md#explore-a-larger-branching-selection) `Reference.Service`, change its `ServiceName` constant and run:

```bash
weaver build --item Warehouse/Operations --workspace-config workspace-mirror.yml
weaver load Warehouse/Operations --stale --workspace-config workspace-mirror.yml
```

Reference.Service becomes a local Table in OperationsDev and leaves `_.Mirror`. Reference.Depot stays borrowed, and the source Operations Warehouse keeps its original value.

Warehouse borrowed Tables/Views are presented through local Views. Lakehouse stored Tables/Folders use shortcuts, with local wrapper Views for source Views. Health reads borrowed current Load state from the source catalogue and local state from development. A mixed estate is an ordinary result, not evidence that every object has been copied.

Selected changed or impacted protected Tables/Folders use preserving materialisation rather than empty reconstruction: Warehouse CTAS, Delta shallow clone or native recursive Folder copy. That path retains the established bookmark but is not an atomic estate snapshot; shallow clones require source file retention. Protection does not protect against Wipe or deliberate re-mirroring. Keep irreplaceable source data outside ordinary managed target ownership. See [Protecting data](../advanced/protecting-data.md).

## Reset only when a new source baseline is intended

Run Mirror again only when the displayed destination catalogue and selected targets should be replaced. Local work inside that boundary is not preserved as a fallback. Preflight failures leave destinations unchanged; a failure after mutation begins does not restore the old catalogue or targets and does not undo already completed destinations. Inspect remaining state before retrying.

Selective mirroring still copies the destination catalogue, but only selected items are rebound to development targets; unselected copied installations remain source-bound. A catalogue-only Mirror copies installed/current state without emptying an item target, and destination Log/LoadStatistic history starts empty. It is not an isolated writable copy of every source binding. Rebinding from an already mirrored source is refused rather than chaining borrowing hops.

[Mirror and materialisation strategies](../advanced/mirror-and-materialisation-strategies.md) explains these narrower estate shapes. [Mirror behaviour](../reference/operation-behaviour/mirror.md) owns exact selection, binding and failure rules. Once the baseline is in place, return to [ordinary development](development-cycle.md), not another reset.
