# Mirror behaviour

Mirror reconstructs a destination catalogue from another installed catalogue. It can also replace selected destination items with borrowed representations of their source installations.

## Source and destination

`mirror` / `--mirror` names the source catalogue. `catalogue` / `--catalogue` names the destination when a mirror source is configured or both values are supplied explicitly. Explicit values override the corresponding configuration values.

Without a configured `mirror`, configured `catalogue` is the source and a separate destination is required. With both configured, `mirror` is the source and `catalogue` is the destination.

Source and destination must resolve to distinct Warehouses in the operation's workspace. A workspace-qualified source or destination in another workspace is refused. Mirror does not copy between resolved workspaces.

The source must contain the catalogue tables required by this Weaver revision. A missing, unreadable or incompatible source fails before any destination is emptied.

## Item selection

Repeatable `--item ITEM[=TARGET]` selects logical items. `ITEM` uses its configured destination; `ITEM=TARGET` supplies or overrides it. Naming no item selects every configured target. `--no-item` selects no item and copies only the catalogue; it is mutually exclusive with `--item`.

Each selected item must have a source installation. Selected logical items cannot repeat. Destination identities are type plus name: two selected outputs cannot share one physical target, collide with the destination catalogue, or overlap any source catalogue or item read by the same run.

A source catalogue containing `_.Mirror` rows may be copied in catalogue-only mode. Selected items cannot be rebound from it: borrowed state records one source hop, so a second hop is refused.

Recorded logical Shortcuts are resolved against the run's final bindings before mutation. Physical Shortcuts retain their recorded workspace and item. Selected producers precede selected consumers where a logical Shortcut requires that order; an unorderable selected cycle is refused.

## Preflight and authorisation

The public operation has three boundaries:

1. `plan_mirror()` resolves workspace, catalogue roles and written item selection without reading Fabric.
2. `check_mirror()` proves the source, resolves source installations and final destinations, and checks borrowed relations, deployed work and recreatable Shortcuts without mutation.
3. `mirror()` executes the settled plan. An unresolved `MirrorPlan` is checked first; a `ResolvedMirror` is executed as supplied.

The CLI completes both planning and checking, displays the source, destination and selected mappings, then asks about that settled plan. Mirror has no dry-run mode.

An interactive CLI run requires confirmation unless `--yes` is present. JSON mode, a non-interactive run, or a run without a prompt requires `--yes`; otherwise nothing is changed. `--non-interactive` disables prompts and browser sign-in but does not authorise destruction.

Authorisation covers the destination catalogue and every displayed destination target. Existing contents in that scope are not preserved.

## Catalogue copy

Execution first empties and rebuilds the destination catalogue, then copies installed projection and current state from the source. The copied state includes source item bindings, Registry certification, declaration dictionaries, dependencies, Shortcuts, bookmarks, and current Load and Test status. The destination keeps its own built-in catalogue installation.

`_.Log` and `_.LoadStatistic` are rebuilt empty rather than copied. In catalogue-only mode, existing `_.Mirror` rows are copied. Unselected logical items retain the copied source bindings.

## Selected item state

Each selected destination target is emptied before its borrowed forms are created.

| Destination | Borrowed data | Local execution state |
| --- | --- | --- |
| Warehouse | Views over source Tables and Views; supported recorded Shortcuts become local Views | Required procedures and functions are copied into the destination |
| Lakehouse | OneLake shortcuts for Tables and Folders; source Views use local wrapper Views; recorded Shortcuts are recreated | The deployed Load and Test file tree is copied into the destination |

`_.Mirror` records each borrowed relation's source and physical form. The selected item's installation binding changes to the destination only after its borrowed forms and deployed work have been created. Copied code is local because execution is dispatched from the destination; it does not make borrowed data locally owned or loadable there.

A later Build compares project source with copied Registry certification and destination inventory. An unchanged borrowed object keeps its borrowed form and `_.Mirror` row. A changed or affected selected object has its recorded borrowed form removed, is installed locally, and loses its `_.Mirror` row after the physical work. The estate can therefore contain borrowed and local objects together.

## Failure, partial effects and re-mirroring

Planning and checking failures leave all destinations intact. Once execution starts, effects are not transactional:

1. the destination catalogue is emptied, rebuilt and populated;
2. selected targets are then emptied and reconstructed in settled order; and
3. each selected binding changes last for that item.

A failure in catalogue rebuild or copy, target emptying, borrowed-form creation, deployed-work copy, Shortcut recreation, mirror recording or binding publication stops the operation. Earlier destructive and completed effects remain. No successful `MirrorResult` is returned for an incomplete run, and Weaver performs no operation-wide rollback.

Running Mirror again is a new reconstruction from the selected source. It empties the same settled destination scope again, so local materialisation inside that scope is replaced by a fresh borrowed baseline. This is a reset, not rollback or continuation of the earlier run.

A successful result reports `status: succeeded`, the workspace and catalogue pair, emptied destinations, copied and uncopied catalogue tables, selected logical items, and kind-specific work counts. See [Machine-readable interfaces](../machine-readable-output.md) for the current unversioned JSON shape.
