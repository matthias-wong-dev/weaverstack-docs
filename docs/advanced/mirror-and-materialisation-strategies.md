# Mirror and materialisation strategies


---

## Mirror an estate for specialised development

Mirror starts a destination catalogue from an installed source estate. You can then borrow selected item data, materialise selected items locally, or leave their copied bindings pointing at the source.

This route suits a development estate where most installed state should match an existing estate but one part needs isolated work. Mirror is destructive at every displayed destination and has no dry-run mode.

## Choose the result before running Mirror

For each logical item, choose one of three outcomes:

| Intended result | Action | Resulting binding and data |
| --- | --- | --- |
| Keep using the source item | Do not select it for Mirror or Build | The copied installation continues to name the source target. |
| Borrow source data through a development item | Select it with `weaver mirror --item` | The logical item is rebound to the development target; its data remains source-owned. |
| Own a complete development copy | Fork the catalogue, then select it with `weaver build --item` | Build installs the authored local form in the development target. |

Borrowed Warehouse Tables and Views become local Views over source relations. Borrowed Lakehouse Tables and Folders become OneLake shortcuts; source Views use local wrapper Views. Weaver copies the execution work needed by Load and Test into the destination item, but borrowed objects are not loadable there because their rows remain owned by the source.

A later Build localises a borrowed object only when that selected object changed or is an affected selected descendant. Unchanged borrowed objects remain borrowed, so one destination item can contain both borrowed and local objects.

## Prerequisites

- A source catalogue and destination catalogue in the same Fabric workspace. They must be distinct Warehouses.
- An installed source item for every logical item you intend to mirror.
- Emptyable destination items of the corresponding kind. Mirror empties them; it does not merge their contents.
- A workspace configuration that names the source, destination and development bindings, or the equivalent command options.

For example, create `workspace-development.yml`:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

`mirror` is the catalogue read from. `catalogue` is the catalogue rebuilt. A configuration containing only `catalogue` describes a source estate and cannot also supply the destination for Mirror.

## Inspect the complete destination boundary

Run Mirror interactively before using it in automation:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Lakehouse/Landing \
  --item Warehouse/Operations
```

Omitting `--item` selects every configured target. Use `--no-item` when you intend to fork only the catalogue. Do not combine `--no-item` with item selection.

Before asking for confirmation, Weaver reads and validates the source catalogue, resolves each source installation, settles final bindings and checks the destinations for conflicts. The displayed plan names the destination catalogue and every selected destination item that will be emptied. Decline the prompt if any destination is unexpected.

The preflight rejects a destination that is also read as a source, two selected logical items sharing one physical destination, or an item missing from the source installation. It also refuses to rebind an item from a source catalogue that is already mirrored: borrowed state records one source hop.

## Create a catalogue-only branch

Fork installed and current state without touching an item target:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --no-item
```

After confirmation, the destination catalogue contains copied Registry, declaration, dependency, Shortcut, bookmark, Load-status and Test-status state. Operational log and load-statistic history starts empty. Item bindings remain as recorded in the source catalogue.

Use this route before materialising only one item locally:

```bash
weaver build . \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations
```

Build reads the copied installed state, compares it with project source and installs `Warehouse/Operations` into `Warehouse/ParcelOperationsDev`. Other logical items keep their copied source bindings.

## Borrow selected data into development items

To recreate selected items as borrowed forms at their configured destinations, run:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Lakehouse/Landing \
  --item Warehouse/Operations
```

You may override one configured destination explicitly:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations=Warehouse/ParcelOperationsExperiment
```

Logical Shortcuts are recreated against the final bindings settled for this run. When one selected item points at another, Weaver orders the producer before the consumer. Physical Shortcuts retain their recorded workspace and item.

After Mirror completes, inspect the destination estate:

```bash
weaver health \
  --workspace-config workspace-development.yml \
  --item Lakehouse/Landing \
  --item Warehouse/Operations
```

Health reports the destination estate's installed and operational view. Copied catalogue state is a point-in-time branch, while a borrowed object's Load lifecycle state remains sourced from the catalogue where its data is loaded. Neither is proof that every source object remained unchanged after the mirror.

## Run it unattended only after reviewing the same scope

An unattended mirror needs both interaction policy and destructive authorisation:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations \
  --non-interactive \
  --yes
```

`--non-interactive` prevents prompts and browser sign-in. It does not authorise emptying. `--yes` authorises every destination in the settled plan. Keep the configuration and item selection under change control so the reviewed boundary is the one the job resolves.

## Recover from a failed mirror

Failures during preflight leave destinations unchanged. Once execution starts, Weaver rebuilds the destination catalogue and then processes selected item destinations in settled order. A later failure does not restore earlier contents or roll back completed destinations.

Correct the reported Fabric, copy, Shortcut or binding failure, then run Mirror again against the intended source and selection. A rerun performs a new reconstruction; it is not rollback. Do not run Load against a partially reconstructed destination merely because some targets completed.

See the [Mirror contract](../reference/operation-behaviour/mirror.md) for copied tables, borrowed forms, localisation and failure boundaries. See [`weaver mirror`](../reference/cli/mirror.md) for complete syntax and output behaviour.

---

## Mirror contract

Mirror creates a destination estate from another installed catalogue. It copies installed and current state, optionally rebinds logical items to destination targets, and represents their data as borrowed until a later Build materialises selected work locally.

Mirror is destructive at every displayed destination. It is not a data backup, a dry run or an operation-wide transaction.

## Source, destination and configuration

The mirror source is the catalogue read from. The destination catalogue is emptied and rebuilt.

- `mirror` or `--mirror` names the source.
- `catalogue` or `--catalogue` names the destination when a configured mirror source is present or when both sides are supplied explicitly.
- an explicit source or destination overrides the corresponding configured value.

A configuration that names only `catalogue` describes a source estate; Mirror still requires a separately named destination. Weaver does not infer that one Warehouse is both sides. With both `mirror` and `catalogue` configured, `mirror` is the source and `catalogue` is the destination.

Source and destination catalogues must be distinct Warehouses in the resolved workspace. The source must contain a compatible Weaver catalogue. A missing, unreadable or incompatible source is rejected before any destination is emptied.

Omitting item selection chooses every target declared by the selected workspace configuration. `--item ITEM` uses that logical item's configured destination; `ITEM=TARGET` supplies or overrides it. `--no-item`, or `no_item=True`, copies only the catalogue. Item selection and no-item selection are mutually exclusive.

Each selected logical item must have a source installation. A destination cannot be shared by two selected items, overlap a physical source read by the same run or collide with the destination catalogue. Rebinding items from an already mirrored source is refused because borrowed state records one source hop; a catalogue-only copy may carry that state without adding another hop.

## Planning and checking

The Python operation separates three boundaries:

1. `plan_mirror()` resolves workspace, source, destination and written item selection without reading Fabric.
2. `check_mirror()` reads and validates the source, resolves source installations, destination bindings, borrowable relations, installed work and recreatable Shortcuts, and returns a settled plan without mutation.
3. `mirror()` executes that settled plan. Passing an unresolved plan causes it to be checked first.

All logical-to-physical bindings are settled before any write. Logical Shortcuts use the final bindings from that plan; physical Shortcuts retain their recorded workspace and item. Selected producer items are ordered before selected consumers when recorded logical Shortcuts require it.

The CLI plans and checks before asking for destructive authorisation, displays the settled source, destination and selected target mappings, and executes that same settled plan.

## Destructive authorisation

Mirror has no dry-run mode. In an interactive CLI invocation, withholding or declining confirmation leaves destinations unchanged. In non-interactive or JSON mode, `--yes` is required before mutation. `--non-interactive` prevents prompts and browser sign-in but does not grant authorisation.

Authorisation applies to the destination catalogue and every selected destination target in the displayed plan. It does not change selection or preserve their existing contents.

## Copied catalogue state

Execution empties and rebuilds the destination catalogue, then copies installed projection and current state from the source. This includes source item bindings, Registry certification, declaration dictionaries, dependencies, Shortcuts, bookmarks and current Load and Test status. The destination catalogue keeps its own built-in catalogue installation rather than copying the source catalogue's self-binding.

`_.Log` and `_.LoadStatistic` rows are not copied. Their destination tables are rebuilt empty. An existing `_.Mirror` table is copied for a catalogue-only copy, but a run that rebinds selected items refuses an already mirrored source.

Unselected logical items retain the physical bindings copied from the source. Each selected item's `_.Installation` binding is switched to its settled destination only after its borrowed physical forms and installed execution work have been created. The destination can therefore describe both selected borrowed items and unselected source-bound items.

## Borrowed physical forms

`_.Registry` retains each installed logical object's declared type and signature. `_.Mirror` records the source address and the physical form that represents borrowed data at the destination.

For a Warehouse destination:

- borrowed Tables and Views are local Views over source relations;
- installed procedures and functions needed by Load and Test are copied locally; and
- recorded Shortcuts are recreated as supported local Views using settled bindings.

For a Lakehouse destination:

- borrowed Tables and Folders are OneLake shortcuts;
- a source View is exposed through a local wrapper View;
- the installed Load and Test file tree is copied locally; and
- recorded Shortcuts are recreated against their settled physical sources.

The copied execution work is local because dispatch occurs in the destination item. It does not make borrowed data locally owned. A borrowed object is not loadable at the destination; its current Load state remains sourced from the catalogue where its data is loaded.

## Localisation on Build

An unchanged borrowed object remains in its borrowed form and keeps its `_.Mirror` row. Build compares the copied Registry signature and destination inventory with selected project source.

When a selected borrowed object changes, or is an affected selected descendant, Build:

1. removes the borrowed physical representation using its recorded physical form;
2. installs the authored local form in the configured destination target;
3. removes that object's `_.Mirror` record after physical work; and
4. publishes the resulting local certification.

Unchanged borrowed objects stay borrowed. Unselected items and descendants remain outside that Build. The result may be a mixed estate containing both borrowed and local objects.

## Failure and non-rollback boundaries

Checking the source, item installations, final bindings and recreatable Shortcuts completes before execution begins. These failures leave every destination intact.

Once authorised execution starts, Weaver empties and rebuilds the destination catalogue, then processes selected destination targets in settled order. A later Fabric, copy, Shortcut, installed-work or binding failure does not restore the previous destination catalogue or targets and does not undo earlier completed destinations. No Mirror result is returned as successful unless the complete selected operation finishes.

A later Mirror is a new reconstruction against the source and settled plan. Repeating a successful request converges to the same copied estate, but it is not rollback of an interrupted request.

## Result boundary

A successful result identifies the workspace, source and destination catalogues, emptied destinations, copied catalogue-table counts, historical tables left uncopied, selected logical items and operation-specific counts. These meanings are public; the exact JSON object shape and field ordering are not frozen by this contract.

## Defined behaviour

The Mirror contract specifies that Weaver:

1. resolves source, destination and item bindings without treating one catalogue as both sides;
2. proves and settles the complete read/write boundary before destructive authorisation;
3. requires explicit authorisation and exposes no dry-run mode;
4. rebuilds the destination catalogue from copied installed and current state without copying operational history;
5. rebinds selected logical items while retaining copied source bindings for unselected items;
6. represents borrowed Warehouse data as Views and borrowed Lakehouse data as shortcuts or wrapper Views;
7. keeps installed execution work local while borrowed data remains source-owned;
8. localises changed and affected selected borrowed objects during Build; and
9. preserves completed destructive effects when a later Mirror step fails rather than rolling back the operation.
