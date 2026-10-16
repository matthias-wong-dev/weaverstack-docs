# Run part of an estate

Can you rerun only this Table and the work it affects? Start with a named Load preview, then add upstream or downstream work when that is the intended scope.

Keep the [Landing → Operations project](connected-items.md) and its `workspace-development.yml` from [workspace mappings](environments.md). Landing’s Folder supplies Event, which feeds CurrentStatus. Operations exposes Event through a Shortcut and loads the additional LakehouseCurrentStatus Table.

## Preview one Table

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "60-named-load-preview", "title": "Preview · one installed Table"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · one installed Table">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           2.7s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
  Execute                                                                                                  0.0s
<span class="terminal-status-green">✓ Load (dry run)                                                                                           2.7s</span>

<span class="terminal-status-green">plan succeeded: Lakehouse/Landing</span>

    validated                load:Lakehouse/Landing/Tables/Parcel.Event

Plan
    1 selected
</code></pre>
</figure>
<!-- /cli-capture -->

The plan selects only `Tables/Parcel.Event`. No data is loaded by `--dry-run`. Read the selected identities before running; plain named Load does not add producers or infer their ordering. The `[.]` matches a literal dot in this whole-name selector; `Tables/` identifies the Table rather than a Folder.

## Include the work before or after it

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --ancestors --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "61-ancestor-load-preview", "title": "Preview · include the producer"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · include the producer">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           2.6s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
  Execute                                                                                                  0.0s
<span class="terminal-status-green">✓ Load (dry run)                                                                                           2.6s</span>

<span class="terminal-status-green">plan succeeded: Lakehouse/Landing</span>

    validated                load:Lakehouse/Landing/Files/Parcel.Events
    validated                load:Lakehouse/Landing/Tables/Parcel.Event
                             after load:Lakehouse/Landing/Files/Parcel.Events

Plan
    2 selected
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "62-descendant-load-preview", "title": "Preview · include the consumer"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · include the consumer">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           2.6s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
  Execute                                                                                                  0.0s
<span class="terminal-status-green">✓ Load (dry run)                                                                                           2.6s</span>

<span class="terminal-status-green">plan succeeded: Lakehouse/Landing</span>

    validated                load:Lakehouse/Landing/Tables/Parcel.Event
    validated                load:Lakehouse/Landing/Tables/Parcel.CurrentStatus
                             after load:Lakehouse/Landing/Tables/Parcel.Event

Plan
    2 selected
</code></pre>
</figure>
<!-- /cli-capture -->

| Request | Selected Landing work |
| --- | --- |
| Seed alone | Table `Parcel.Event` |
| Ancestors | Folder `Parcel.Events`, then Table `Parcel.Event` |
| Descendants | Table `Parcel.Event`, then Table `Parcel.CurrentStatus` |

Expansion uses the **installed** dependencies, not edited source files. It restores dependency ordering within the selected graph. It never adds an unnamed item: Operations remains outside these requests, and the Shortcut itself has no Load; its consuming Table is selected only when Operations is named. A descendant run omits the Folder, so keep its staged CSV current.

## Run the selection you inspected

Remove only the preview flag when the plan is correct:

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "63-descendant-load", "title": "Load · the inspected downstream selection"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · the inspected downstream selection">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.7s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
  Wait for Spark session                                                                                  35.8s
→   Load Lakehouse/Landing/Tables/Parcel.Event
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +0 ~0 -0 !0)                                     14.0s</span>
→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +0 ~0 -0 !0)                              7.1s</span>
  Execute                                                                                                 19.1s
  Record what the run did                                                                                  0.0s
<span class="terminal-status-green">✓ Load                                                                                                    1m06s</span>

<span class="terminal-status-green">load succeeded: Lakehouse/Landing</span>

Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   5
    inserted               0
    updated                0
    deleted                0
    rejected               0

  Workflow: 22718af73f53453f9d758af309a2809c
</code></pre>
</figure>
<!-- /cli-capture -->

Event ran before CurrentStatus. Inspect each outcome; attempted is not the same as succeeded. With the original three-event feed, CurrentStatus should still show the two parcel statuses from the Lakehouse task. Operations is outside this invocation; its additional cross-item Table is not reloaded by this Landing-only selection. Next, [limit simultaneous work](concurrency.md) on this same estate.

## Diagnose an unmatched name

A misspelt selection is an error, not an empty successful run. For example, in unattended mode:

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]DoesNotExist' --dry-run --workspace-config workspace-development.yml --non-interactive
```

<!-- cli-capture: {"id": "68-no-match-unattended-preview", "title": "Preview · no installed name matches"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · no installed name matches">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           7.4s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
<span class="terminal-status-red">✗ Execute                                                                                                  0.0s</span>
<span class="terminal-status-red">✗ Load (dry run)                                                                                           7.4s</span>

<span class="terminal-status-red">error: no installed loadable object in the requested items matches &#x27;Tables/Parcel[.]DoesNotExist&#x27;. Installed: Files/Parcel.Events, Files/Parcel.StatusFiles, Tables/Parcel.CurrentStatus, Tables/Parcel.Event, Tables/Parcel.LiveStatus</span>
</code></pre>
</figure>
<!-- /cli-capture -->

Check the installed names and item scope. In an interactive terminal, Esc leaves the error prompt; Enter retries the same request.

## Explore a larger branching selection

<details markdown="1">
<summary>Optional: sibling prerequisites and a second Warehouse</summary>

This larger graph shows how expansion treats a sibling prerequisite and a second item. In the Fabric portal, create a Warehouse called **Reporting**, add `Warehouse/Reporting: Reporting` under `targets` in `workspace-development.yml`, then add these files. Their names do not collide with the Parcel pipeline you already have.

```sql title="Warehouse/Operations/Parcel.Daily.sql"
/*
Table ID: Parcel.Daily
Description: Delivered parcels per depot.
Lineage: Parcel.Events joined to the Reference.Depot list.
*/
SELECT e.DepotId, SUM(e.Delivered) AS DeliveryCount FROM [Parcel].[Events] AS e JOIN [Reference].[Depot] AS d ON e.DepotId = d.DepotId GROUP BY e.DepotId
```

```sql title="Warehouse/Operations/Parcel.Events.sql"
/*
Table ID: Parcel.Events
Description: Delivery events used by the daily summary.
Lineage: Copied from Parcel.RawEvents.
*/
SELECT ParcelId, DepotId, Delivered FROM [Parcel].[RawEvents]
```

```sql title="Warehouse/Operations/Parcel.RawEvents.sql"
/*
Table ID: Parcel.RawEvents
Description: One constant delivery event for this selection example.
Lineage: A constant in this file.
Schema:
  ParcelId: int
  DepotId: int
  Delivered: int
*/
SELECT CAST(1 AS int) AS ParcelId, CAST(10 AS int) AS DepotId, CAST(1 AS int) AS Delivered
```

```sql title="Warehouse/Operations/Parcel.Summary.sql"
/*
Table ID: Parcel.Summary
Description: Total delivered parcels.
Lineage: Summed from Parcel.Daily.
*/
SELECT SUM(DeliveryCount) AS DeliveryCount FROM [Parcel].[Daily]
```

```sql title="Warehouse/Operations/Reference.Depot.sql"
/*
Table ID: Reference.Depot
Description: Depots that deliveries are counted against.
Lineage: A constant in this file.
Schema:
  DepotId: int
  DepotName: varchar(20)
*/
SELECT CAST(10 AS int) AS DepotId, CAST('Central' AS varchar(20)) AS DepotName
```

```sql title="Warehouse/Operations/Reference.Service.sql"
/*
Table ID: Reference.Service
Description: Service levels. Nothing in this example reads it.
Lineage: A constant in this file.
Schema:
  ServiceId: int
  ServiceName: varchar(20)
*/
SELECT CAST(1 AS int) AS ServiceId, CAST('Standard' AS varchar(20)) AS ServiceName
```

```sql title="Warehouse/Reporting/Parcel.DashboardInput.sql"
/*
Table ID: Parcel.DashboardInput
Description: Delivered total presented to reporting.
Lineage: Operations Parcel.Summary through a logical Shortcut.
*/
SELECT DeliveryCount FROM [Parcel].[Summary]
```

```yaml title="Warehouse/Reporting/shortcuts.yml"
logical:
  Warehouse/Reporting/Parcel.Summary: Warehouse/Operations/Parcel.Summary
```

Install and preload the extended graph using the same estate configuration:

```bash
weaver check
weaver build --item Warehouse/Operations --item Warehouse/Reporting --workspace-config workspace-development.yml
weaver load Warehouse/Operations Warehouse/Reporting --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "64c-branch-load", "title": "Load · both Warehouses, in dependency order"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · both Warehouses, in dependency order">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           3.0s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations
  Warehouse/Reporting

  Build run graph                                                                                          0.0s
→   Load Warehouse/Operations/Parcel.RawEvents
→   Load Warehouse/Operations/Reference.Depot
→   Load Warehouse/Operations/Parcel.LakehouseCurrentStatus
→   Load Warehouse/Operations/Parcel.LiveStatus
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.RawEvents  (read 1, +1 ~0 -0 !0)                                      2.2s</span>
→   Load Warehouse/Operations/Parcel.Events
<span class="terminal-status-green">✓   Load Warehouse/Operations/Reference.Depot  (read 1, +1 ~0 -0 !0)                                       2.2s</span>
→   Load Warehouse/Operations/Parcel.StatusEvent
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LiveStatus  (read 0, +0 ~0 -0 !0)                                     2.5s</span>
→   Load Warehouse/Operations/Reference.Service
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.Events  (read 1, +1 ~0 -0 !0)                                         1.3s</span>
→   Load Warehouse/Operations/Parcel.Daily
<span class="terminal-status-green">✓   Load Warehouse/Operations/Reference.Service  (read 1, +1 ~0 -0 !0)                                     1.5s</span>
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LakehouseCurrentStatus  (read 2, +0 ~0 -0 !0)                         4.7s</span>
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.Daily  (read 1, +1 ~0 -0 !0)                                          1.8s</span>
→   Load Warehouse/Operations/Parcel.Summary
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +0 ~0 -0 !0)                                    3.5s</span>
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.Summary  (read 1, +1 ~0 -0 !0)                                        1.5s</span>
→   Load Warehouse/Reporting/Parcel.DashboardInput
<span class="terminal-status-green">✓   Load Warehouse/Reporting/Parcel.DashboardInput  (read 1, +1 ~0 -0 !0)                                  2.5s</span>
  Execute                                                                                                  9.4s
  Record what the run did                                                                                  0.5s
<span class="terminal-status-green">✓ Load                                                                                                    12.9s</span>

<span class="terminal-status-green">load succeeded: Warehouse/Operations, Warehouse/Reporting</span>

Load summary
<span class="terminal-status-green">   10 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                  12
    inserted               7
    updated                0
    deleted                0
    rejected               0

  Workflow: 8b0ae5d889cd48d3a3fd852e4f0667f4
</code></pre>
</figure>
<!-- /cli-capture -->

The rest of this section uses this installed graph in `Warehouse/Operations`:

```text
Parcel.RawEvents → Parcel.Events → Parcel.Daily → Parcel.Summary
                                      ↑
                               Reference.Depot
```

`Reference.Depot` must already be current when a partial selection omits it. Expansion reads installed dependencies; it does not Build edited source.

## 1. Choose the item boundary

Name the logical items you intend to run. Dependencies never add an unnamed item. Start with `Warehouse/Operations`; the separate `Warehouse/Reporting` item remains outside this selection.

## 2. Choose the seed

`--name` is a case-insensitive **whole-name regular expression**, not a glob or substring search. Escape a literal dot with `[.]`:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --dry-run --workspace-config workspace-development.yml
```

This selects only `Parcel.Events`. Plain named Load is a deliberate operator override: multiple matches do not imply dependency expansion or ordering between them.

## 3. Inspect the preview

Read the selected identities, dependencies and any required publication/endpoint work in the returned plan. No data is loaded by `--dry-run`. Do not run a command whose selection differs from your intended scope.

## 4. Include upstream or downstream work

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --dry-run --workspace-config workspace-development.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --descendants --dry-run --workspace-config workspace-development.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --descendants --dry-run --workspace-config workspace-development.yml
```

| Request | Selected tables in Operations |
| --- | --- |
| Seed alone | Events |
| Ancestors | RawEvents, Events |
| Descendants | Events, Daily, Summary |
| Both directions | RawEvents, Events, Daily, Summary |

The combined preview returned:

<!-- cli-capture: {"id": "65d-branch-both", "title": "Preview · ancestors and descendants of Parcel.Events"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · ancestors and descendants of Parcel.Events">
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

<span class="terminal-status-green">plan succeeded: Warehouse/Operations</span>

    validated                load:Warehouse/Operations/Parcel.RawEvents
    validated                load:Warehouse/Operations/Parcel.Events
                             after load:Warehouse/Operations/Parcel.RawEvents
    validated                load:Warehouse/Operations/Parcel.Daily
                             after load:Warehouse/Operations/Parcel.Events
    validated                load:Warehouse/Operations/Parcel.Summary
                             after load:Warehouse/Operations/Parcel.Daily

Plan
    4 selected
</code></pre>
</figure>
<!-- /cli-capture -->

**Both directions start from the original seeds separately. Their union does not add `Reference.Depot`, even though Daily reads it.** An omitted producer is not automatically refreshed. Expanded work runs in dependency order within the selected graph, including required supported barriers; unrelated sibling prerequisites do not become selected data work.

## 5. Run the selection you inspected

Remove only the preview flag:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "65e-branch-run-ancestors", "title": "Load · Parcel.Events and its producer"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · Parcel.Events and its producer">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.6s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
→   Load Warehouse/Operations/Parcel.RawEvents
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.RawEvents  (read 1, +1 ~0 -1 !0)                                      2.1s</span>
→   Load Warehouse/Operations/Parcel.Events
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.Events  (read 1, +1 ~0 -1 !0)                                         1.5s</span>
  Execute                                                                                                  3.8s
  Record what the run did                                                                                  0.5s
<span class="terminal-status-green">✓ Load                                                                                                     6.9s</span>

<span class="terminal-status-green">load succeeded: Warehouse/Operations</span>

Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   2
    inserted               2
    updated                0
    deleted                2
    rejected               0

  Workflow: 539f2beac4974f1eacbb765b5a97985a
</code></pre>
</figure>
<!-- /cli-capture -->

RawEvents ran before Events; Daily, Summary, Depot and the Reporting item were not requested. Both Tables have no primary key, so each Load replaces their contents: `+1 ~0 -1` is the old row deleted and the new one inserted.

The equivalent combined Python preview is:

```python
import weaver

preview = weaver.load(
    'Warehouse/Operations',
    names=r'Parcel[.]Events',
    ancestors=True,
    descendants=True,
    dry_run=True,
    workspace_config='workspace-development.yml',
)
print(preview.to_mapping())
```

## 6. Cross an item boundary deliberately

The addition above declares `Warehouse/Reporting/Parcel.DashboardInput`, which consumes Operations' Summary. Selecting Operations alone cannot reach it. To include it, name both items:

```bash
weaver load Warehouse/Operations Warehouse/Reporting --name 'Parcel[.]Events' --descendants --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "65f-branch-cross-item", "title": "Preview · descendants across two Warehouses"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · descendants across two Warehouses">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           2.6s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations
  Warehouse/Reporting

  Build run graph                                                                                          0.0s
  Execute                                                                                                  0.0s
<span class="terminal-status-green">✓ Load (dry run)                                                                                           2.6s</span>

<span class="terminal-status-green">plan succeeded: Warehouse/Operations, Warehouse/Reporting</span>

    validated                load:Warehouse/Operations/Parcel.Events
    validated                load:Warehouse/Operations/Parcel.Daily
                             after load:Warehouse/Operations/Parcel.Events
    validated                load:Warehouse/Operations/Parcel.Summary
                             after load:Warehouse/Operations/Parcel.Daily
    validated                load:Warehouse/Reporting/Parcel.DashboardInput
                             after load:Warehouse/Operations/Parcel.Summary

Plan
    4 selected
</code></pre>
</figure>
<!-- /cli-capture -->

This selects Events, Daily and Summary in Operations, then DashboardInput in Reporting. It still omits RawEvents and Depot. Keep both current before that run. A Lakehouse-to-Warehouse equivalent may also need OneLake publication and SQL endpoint readiness; these are ordered by the supported installed graph, not replaced with an arbitrary delay.

## 7. Match several names and diagnose a refusal

Repeat `--name` to take the union of matching seeds. Every supplied pattern must match at least one loadable object inside the requested scope:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --name 'Reference[.]Depot' --descendants --dry-run --workspace-config workspace-development.yml
weaver load Warehouse/Operations --name 'Parcel[.]DoesNotExist' --dry-run --workspace-config workspace-development.yml
```

The first selects Events and Depot, then Daily, which waits for both, and Summary. The second is a no-match error, not an empty successful run, and lists the installed names:

<!-- cli-capture: {"id": "65h-branch-no-match", "title": "Preview · no installed name matches"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · no installed name matches">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load (dry run)

  Read catalogue                                                                                           2.7s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
<span class="terminal-status-red">✗ Execute                                                                                                  0.0s</span>
<span class="terminal-status-red">✗ Load (dry run)                                                                                           2.7s</span>

<span class="terminal-status-red">error: no installed loadable object in the requested items matches &#x27;Parcel[.]DoesNotExist&#x27;. Installed: Parcel.Daily, Parcel.Events, Parcel.LakehouseCurrentStatus, Parcel.LiveStatus, Parcel.RawEvents, Parcel.StatusEvent, Parcel.Summary, Reference.Depot, Reference.Service</span>
</code></pre>
</figure>
<!-- /cli-capture -->

Check installed spelling and item scope. `Parcel.Events` leaves its dot as a regex wildcard; `[.]` expresses the literal identity.

Lakehouse identities can include `Tables/` or `Files/`. A bare identity can be ambiguous when both areas contain it. Use an area-qualified name, for example:

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --dry-run --workspace-config workspace-development.yml
```

This selects Landing in the same project and development configuration used at the start of this page.


</details>

## Choose the right kind of rerun {#8-choose-the-right-kind-of-rerun}

- Ordinary item-wide Load runs the installed item graph.
- `--stale` selects non-Green work by Load health. It does not refresh every omitted Green prerequisite. `--as-of` supplies its freshness cutoff and requires `--stale`.
- `--reload` **empties reached selected tables and resets their bookmarks/progress before loading them**. Expansion can enlarge that destructive scope. Preview first; the old data is not automatically restored after failure. Reload is not supported for Folders, and cannot be combined with stale selection.
- `--fault-tolerant` changes continuation and reject policy, not the item boundary or source definitions. Read the [failure boundary](../reference/operation-behaviour/load.md) before using partial output.

Ancestors and descendants are Load options, not Build or Test options. Catalogue-free semantic-model refresh does not provide installed-graph name, stale, reload or recursive selection; name the model to refresh instead.

## Related tasks

- [Recover failed work](recovery.md).
- [Limit simultaneous work](concurrency.md).
- [Look up exact selection and identity rules](../reference/operation-behaviour/shared-selection-and-identity.md).
