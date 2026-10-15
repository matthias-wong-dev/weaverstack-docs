# Run part of an estate

Can you rerun only this Table and the work it affects? Start with a named Load preview, then add upstream or downstream work when that is the intended scope.

Keep the [Landing → Dispatch project](connected-items.md) and its `workspace-development.yml` from [workspace mappings](environments.md). Landing’s Folder supplies Event, which feeds CurrentStatus. Dispatch’s Shortcut View reads Event directly and has no separate Load.

## Preview one Table

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --dry-run --workspace-config workspace-development.yml
```

The plan should select only `Tables/Parcel.Event`. No data is loaded by `--dry-run`. Read the selected identities before running; plain named Load does not add producers or infer their ordering. The `[.]` matches a literal dot in this whole-name selector; `Tables/` identifies the Table rather than a Folder.

## Include the work before or after it

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --ancestors --dry-run --workspace-config workspace-development.yml
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --dry-run --workspace-config workspace-development.yml
```

| Request | Selected Landing work |
| --- | --- |
| Seed alone | Table `Parcel.Event` |
| Ancestors | Folder `Parcel.Events`, then Table `Parcel.Event` |
| Descendants | Table `Parcel.Event`, then Table `Parcel.CurrentStatus` |

Expansion uses the **installed** dependencies, not edited source files. It restores dependency ordering within the selected graph. It never adds an unnamed item: Dispatch remains outside these requests, and its Shortcut View does not need a data Load anyway. A descendant run omits the Folder, so keep its staged CSV current.

## Run the selection you inspected

Remove only the preview flag when the plan is correct:

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --workspace-config workspace-development.yml
```

The report should show Event attempted before CurrentStatus. Inspect each outcome; attempted is not the same as succeeded. With the original three-event feed, CurrentStatus should still show the two parcel statuses from the Lakehouse task. The Dispatch View continues to read Event without a separate Load. Next, [limit simultaneous work](concurrency.md) on this same estate.

## Explore a larger branching selection

<details markdown="1">
<summary>Optional: sibling prerequisites and a second Warehouse</summary>

Use the [`parcel-load-selection` project](../assets/examples/parcel-load-selection.zip) from the documentation repository. It contains RawEvents, Events, Daily and Summary. Set disposable targets in `workspace-dev.yml`, then run from `examples/parcel-load-selection`:

```bash
weaver check .
weaver build . --item Warehouse/Operations --item Warehouse/Reporting --workspace-config workspace-dev.yml
weaver load Warehouse/Operations Warehouse/Reporting --workspace-config workspace-dev.yml
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
weaver load Warehouse/Operations --name 'Parcel[.]Events' --dry-run --workspace-config workspace-dev.yml
```

This selects only `Parcel.Events`. Plain named Load is a deliberate operator override: multiple matches do not imply dependency expansion or ordering between them.

## 3. Inspect the preview

Read the selected identities, dependencies and any required publication/endpoint work in the returned plan. No data is loaded by `--dry-run`. Do not run a command whose selection differs from your intended scope.

## 4. Include upstream or downstream work

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --descendants --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --descendants --dry-run --workspace-config workspace-dev.yml
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
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --workspace-config workspace-dev.yml
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
    workspace_config='workspace-dev.yml',
)
print(preview.to_mapping())
```

## 6. Cross an item boundary deliberately

The fixture also declares `Warehouse/Reporting/Parcel.DashboardInput`, which consumes Operations' Summary. Selecting Operations alone cannot reach it. To include it, name both items:

```bash
weaver load Warehouse/Operations Warehouse/Reporting --name 'Parcel[.]Events' --descendants --dry-run --workspace-config workspace-dev.yml
```

This selects Events, Daily and Summary in Operations, then DashboardInput in Reporting. It still omits RawEvents and Depot. Keep both current before that run. A Lakehouse-to-Warehouse equivalent may also need OneLake publication and SQL endpoint readiness; these are ordered by the supported installed graph, not replaced with an arbitrary delay.

## 7. Match several names and diagnose a refusal

Repeat `--name` to take the union of matching seeds. Every supplied pattern must match at least one loadable object inside the requested scope:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --name 'Reference[.]Depot' --descendants --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]DoesNotExist' --dry-run --workspace-config workspace-dev.yml
```

The second command is a no-match error, not an empty successful run. Check installed spelling and item scope. `Parcel.Events` leaves its dot as a regex wildcard; `[.]` expresses the literal identity.

Lakehouse identities can include `Tables/` or `Files/`. A bare identity can be ambiguous when both areas contain it. Use an area-qualified name, for example:

```bash
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Event' --descendants --dry-run --workspace-config workspace-development.yml
```

This returns to the Landing project used at the start of this page; select its development configuration, not the Warehouse example’s configuration.


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
