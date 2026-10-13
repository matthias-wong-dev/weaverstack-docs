# Run a selected part of a parcel estate

**Weaver source target:** `74b4d15ee65ed2740593af1f4d459771b801b132`. Use a Weaver build containing these interfaces. The older PyPI `0.9.0` package is not the acceptance target.

## Resources and starting directory

Run from this directory. Use an existing disposable Fabric workspace on capacity that supports Warehouses, a compatible Weaver catalogue Warehouse, and two empty Warehouses named by the chosen configuration. Edit `workspace-dev.yml` and `workspace-prod.yml` to your disposable workspace/catalogue names. The production-labelled file is not permission to use production. You need catalogue read/write access and rights to create/alter and load objects in both Warehouses. This SQL-only fixture does not need Spark or a published Fabric Environment for its Warehouse work.

The core Operations graph contains five tables:

```text
Parcel.RawEvents → Parcel.Events → Parcel.Daily → Parcel.Summary
                                      ↑
                               Reference.Depot
```

An independent `Reference.Service` table supplies a third runnable root for the concurrency example. Reporting's `Parcel.DashboardInput` reads the Operations Summary through the explicit logical declaration in `Warehouse/Reporting/shortcuts.yml`. These are seven authored loadable tables, not a performance-sized estate.

## Build and preload everything

```bash
weaver check .
weaver build . --item Warehouse/Operations --item Warehouse/Reporting --workspace-config workspace-dev.yml
weaver load Warehouse/Operations Warehouse/Reporting --workspace-config workspace-dev.yml
```

Verify all seven tables loaded. Summary and DashboardInput should each have `DeliveryCount = 1`; Depot and Service each have one row. Preload before demonstrating a partial run: omitted producers, particularly Reference.Depot, must already be current.

## Choose a seed and inspect the selection

These are case-insensitive **whole-name regular expressions**. `[.]` makes the dot literal. A plain named override adds no dependency ordering, even when several names match.

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --descendants --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --descendants --dry-run --workspace-config workspace-dev.yml
```

Expected selected sets are in `expected-results.json`: plain selects Events; ancestors selects RawEvents and Events; descendants selects Events, Daily and Summary; both selects RawEvents, Events, Daily and Summary. Expanded selections retain their dependency order.

**Both directions start from the original Events seed. Their union does not add Reference.Depot**, even though Daily reads it. Neither Reference.Service nor the unrequested Reporting item is added. Expansion is over installed dependencies inside requested items; it does not Build changed source or refresh every producer of a newly reached descendant.

Run the inspected combined selection by removing only `--dry-run`:

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --descendants --workspace-config workspace-dev.yml
```

Inspect the Load report: only those four table loads should have run. Omitted tables keep their existing data and progress.

## Expand across the second item

```bash
weaver load Warehouse/Operations Warehouse/Reporting --name 'Parcel[.]Events' --descendants --dry-run --workspace-config workspace-dev.yml
```

This selects Events, Daily, Summary and Reporting/DashboardInput, because both item scopes were named. The Warehouse-to-Warehouse path uses a native logical view over the other Warehouse; this fixture has no Lakehouse endpoint/publication barrier to demonstrate. A Lakehouse crossing can introduce readiness barriers and requires its own resources.

## Regex failures and repeated patterns

```bash
weaver load Warehouse/Operations --name 'parcel[.]events' --name 'Reference[.]Service' --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Missing' --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name 'Parcel[.]Events' --name 'Parcel[.]Missing' --dry-run --workspace-config workspace-dev.yml
weaver load Warehouse/Operations --name '[' --dry-run --workspace-config workspace-dev.yml
```

The first command selects Events and Service as an unordered override. Each supplied pattern must match; the next two refuse Missing before dispatch, even when the other pattern matches. The last refuses an invalid regex. A substring such as `Events` does not match `Parcel.Events`.

Lakehouse names have areas. In a Lakehouse estate with both a Table and Folder named `Parcel.Events`, use `--name 'Tables/Parcel[.]Events'` or `--name 'Files/Parcel[.]Events'`; the bare name is ambiguous. This is a separate identity illustration, not a runnable Lakehouse deployment command for this Warehouse fixture.

## Limit one run

```bash
weaver load Warehouse/Operations Warehouse/Reporting --concurrency 2 --workspace-config workspace-dev.yml
```

RawEvents, Depot and Service are independent roots. The invocation cap applies across the run while Warehouse-specific limits and dependencies still apply. It is not a cluster-size setting and does not edit the configuration. Leave it unset when you do not need a cap.

## Python preview

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

Ordinary item-wide Load keeps its graph. `--stale` chooses outdated installed work; it is not a synonym for `--reload`. **Reload destructively reconstructs every reached selected table and resets its progress.** Expansion can enlarge that destructive scope. Always preview first; stale and reload cannot be combined. `--fault-tolerant` changes continuation policy, not selection. Recursive flags belong to Load, not Build or Test.

## Cleanup

Prefer deleting only the two empty-before-this-example Warehouses after verifying they contain no other work. Remove their catalogue registrations through your approved scoped retirement procedure. Retain the shared catalogue and workspace. Do not delete Warehouses you did not create for this fixture, and do not use an unscoped Wipe.
