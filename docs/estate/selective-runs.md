# Run part of an estate

Can you rerun only this Table and the work it affects? Start with a named Load preview, then add upstream or downstream work when that is the intended scope.

Keep the [Landing → Operations project](connected-items.md) and its `workspace-development.yml` from [workspace mappings](environments.md). Landing’s Folder supplies Event, which feeds CurrentStatus. Operations exposes Event through a Shortcut and loads the additional LakehouseCurrentStatus Table.

## Preview one Table

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "60-named-load-preview", "title": "Preview \u00b7 one installed Table", "start": "    validated"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · one installed Table">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>    validated                load:Lakehouse/Landing/Tables/Parcel.Event

Plan
    1 selected
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/60-named-load-preview.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

The plan selects only `Tables/Parcel.Event`. No data is loaded by `--dry-run`. Read the selected identities before running; plain named Load does not add producers or infer their ordering. The `[.]` matches a literal dot in this whole-name selector; `Tables/` identifies the Table rather than a Folder.

## Include the work before or after it

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --ancestors --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "61-ancestor-load-preview", "title": "Preview \u00b7 include the producer", "start": "    validated"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · include the producer">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>    validated                load:Lakehouse/Landing/Files/Parcel.Events
    validated                load:Lakehouse/Landing/Tables/Parcel.Event
                             after load:Lakehouse/Landing/Files/Parcel.Events

Plan
    2 selected
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/61-ancestor-load-preview.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --dry-run --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "62-descendant-load-preview", "title": "Preview \u00b7 include the consumer", "start": "    validated"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · include the consumer">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>    validated                load:Lakehouse/Landing/Tables/Parcel.Event
    validated                load:Lakehouse/Landing/Tables/Parcel.CurrentStatus
                             after load:Lakehouse/Landing/Tables/Parcel.Event

Plan
    2 selected
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/62-descendant-load-preview.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
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

<!-- cli-capture: {"id": "63-descendant-load", "title": "Load \u00b7 the inspected downstream selection", "start": "\u2192   Load", "end": "  Execute", "full": true} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · the inspected downstream selection">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>→   Load Lakehouse/Landing/Tables/Parcel.Event

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +0 ~0 -0 !0)                                     16.0s</span>

→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +0 ~0 -0 !0)                              7.9s</span>

</code></pre>
<details><summary>Show the complete capture</summary><pre tabindex="0" aria-label="Captured terminal output"><code>Load

  Read catalogue                                                                                           2.0s

Workspace  Weaver Example
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s

  Wait for Spark session                                                                                  32.0s

→   Load Lakehouse/Landing/Tables/Parcel.Event

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +0 ~0 -0 !0)                                     16.0s</span>

→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus

<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +0 ~0 -0 !0)                              7.9s</span>

  Execute                                                                                                 23.4s

  Record what the run did                                                                                  0.0s

<span class="terminal-status-green">✓ Load                                                                                                    1m08s</span>

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

  Workflow: [run-id]
</code></pre></details><p class="terminal-source"><a href="../../assets/cli-captures/63-descendant-load.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

Event ran before CurrentStatus. Inspect each outcome; attempted is not the same as succeeded. With the original three-event feed, CurrentStatus should still show the two parcel statuses from the Lakehouse task. Operations is outside this invocation; its additional cross-item Table is not reloaded by this Landing-only selection. Next, [limit simultaneous work](concurrency.md) on this same estate.

## Diagnose an unmatched name

A misspelt selection is an error, not an empty successful run. For example, in unattended mode:

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]DoesNotExist' --dry-run --workspace-config workspace-development.yml --non-interactive
```

<!-- cli-capture: {"id": "68-no-match-unattended-preview", "title": "Preview \u00b7 no installed name matches", "start": "error:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Preview · no installed name matches">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code><span class="terminal-status-red">error: no installed loadable object in the requested items matches &#x27;Tables/Parcel[.]DoesNotExist&#x27;. Installed: Files/Parcel.Events, Tables/Parcel.CurrentStatus, Tables/Parcel.Event</span>
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/68-no-match-unattended-preview.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

Check the installed names and item scope. In an interactive terminal, Esc leaves the error prompt; Enter retries the same request.

## Explore a larger branching selection

<details markdown="1">
<summary>Optional: sibling prerequisites and a second Warehouse</summary>

Extend the same project with these additional declarations. Keep its original pipelines and validations. Create or reuse a separate disposable Reporting Warehouse in your workspace and add `Warehouse/Reporting: Reporting` under the working configuration’s `targets`. Then create the following files; their names do not replace StatusEvent, CurrentStatus or the Lakehouse integration.

```sql title="Warehouse/Operations/Parcel.Daily.sql"
/*
Table ID: Parcel.Daily
Description: Small parcel example table.
Lineage: $Parcel.Events
*/
SELECT e.DepotId, SUM(e.Delivered) AS DeliveryCount FROM [Parcel].[Events] AS e JOIN [Reference].[Depot] AS d ON e.DepotId = d.DepotId GROUP BY e.DepotId
```

```sql title="Warehouse/Operations/Parcel.Events.sql"
/*
Table ID: Parcel.Events
Description: Small parcel example table.
Lineage: $Parcel.RawEvents
*/
SELECT ParcelId, DepotId, Delivered FROM [Parcel].[RawEvents]
```

```sql title="Warehouse/Operations/Parcel.RawEvents.sql"
/*
Table ID: Parcel.RawEvents
Description: Small parcel example table.
Lineage: Constant
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
Description: Small parcel example table.
Lineage: $Parcel.Daily
*/
SELECT SUM(DeliveryCount) AS DeliveryCount FROM [Parcel].[Daily]
```

```sql title="Warehouse/Operations/Reference.Depot.sql"
/*
Table ID: Reference.Depot
Description: Small parcel example table.
Lineage: Constant
Schema:
  DepotId: int
  DepotName: varchar(20)
*/
SELECT CAST(10 AS int) AS DepotId, CAST('Central' AS varchar(20)) AS DepotName
```

```sql title="Warehouse/Operations/Reference.Service.sql"
/*
Table ID: Reference.Service
Description: Small parcel example table.
Lineage: Constant
Schema:
  ServiceId: int
  ServiceName: varchar(20)
*/
SELECT CAST(1 AS int) AS ServiceId, CAST('Standard' AS varchar(20)) AS ServiceName
```

```sql title="Warehouse/Reporting/Parcel.DashboardInput.sql"
/*
Table ID: Parcel.DashboardInput
Description: Small parcel example table.
Lineage: $Parcel.Summary
*/
SELECT DeliveryCount FROM [Parcel].[Summary]
```

```yaml title="Warehouse/Reporting/shortcuts.yml"
logical:
  Warehouse/Reporting/Parcel.Summary: Warehouse/Operations/Parcel.Summary
```

<!-- review-todo: branching -->
!!! warning "TODO — capture the larger Warehouse/Reporting selection results"
    Landing selections earlier on this page are verified. This optional extended graph has only passed offline checks: capture its Build/Load and the branching previews below before filling in their terminal results.
<!-- /review-todo -->

Install and preload the extended graph using the same estate configuration:

```bash
weaver check
weaver build --item Warehouse/Operations --item Warehouse/Reporting --workspace-config workspace-development.yml
weaver load Warehouse/Operations Warehouse/Reporting --workspace-config workspace-development.yml
```

Use its installed graph below. The guide uses this installed graph in `Warehouse/Operations`:

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

**Both directions start from the original seeds separately. Their union does not add `Reference.Depot`, even though Daily reads it.** An omitted producer is not automatically refreshed. Expanded work runs in dependency order within the selected graph, including required supported barriers; unrelated sibling prerequisites do not become selected data work.

## 5. Run the selection you inspected

Remove only the preview flag:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --workspace-config workspace-development.yml
```

The report should show RawEvents and Events as attempted, with Events ordered after RawEvents. Daily, Summary, Depot and the Reporting item were not requested by that invocation. Inspect outcomes: an attempted node is not necessarily a successful one.

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

This selects Events, Daily and Summary in Operations, then DashboardInput in Reporting. It still omits RawEvents and Depot. Keep both current before that run. A Lakehouse-to-Warehouse equivalent may also need OneLake publication and SQL endpoint readiness; these are ordered by the supported installed graph, not replaced with an arbitrary delay.

## 7. Match several names and diagnose a refusal

Repeat `--name` to take the union of matching seeds. Every supplied pattern must match at least one loadable object inside the requested scope:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --name 'Reference[.]Depot' --descendants --dry-run --workspace-config workspace-development.yml
weaver load Warehouse/Operations --name 'Parcel[.]DoesNotExist' --dry-run --workspace-config workspace-development.yml
```

The second command is a no-match error, not an empty successful run. Check installed spelling and item scope. `Parcel.Events` leaves its dot as a regex wildcard; `[.]` expresses the literal identity.

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
