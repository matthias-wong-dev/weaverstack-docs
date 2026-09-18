# Mirrors


---

## Development cycle

A development estate can start from production's installed state without maintaining a second set of Weaver documents. Mirror is the state transition into that estate, not merely a command that copies data. The selected workspace configuration changes the catalogue and physical targets; the project keeps the same logical item identities and declarations.

This page applies the [Build, Load and Test lifecycle](build-load-and-test.md) to a mirrored development estate. See the [CLI reference](../reference/cli.md) for command forms and options.

## The loop

```text
production estate
        ↓
select development workspace configuration
        ↓
mirror production into development
        ↓
change Weaver documents
        ↓
build
        ↓
changed borrowed objects become local
        ↓
load → test → health
        ↖         ↓
          repeat
```

The mirror supplies a development baseline. Build then materialises changed borrowed objects and affected descendants in the selected Build scope. Unchanged objects continue to read production data through their local Views or shortcuts.

## Configuration is the environment switch

A production and development configuration can bind the same project to different physical items. A real project uses these two files in the same project directory.

Production configuration:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

Development configuration:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
mirror: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

The project and logical item keys are unchanged:

- `Lakehouse/Landing`
- `Warehouse/Operations`

The selected configuration changes their physical targets from `ParcelLanding` and `ParcelOperations` to `ParcelLandingDev` and `ParcelOperationsDev`. It also changes the catalogue from `Warehouse/ParcelCatalogue` to `Warehouse/ParcelCatalogueDev` and names the production catalogue as the mirror source.

These names are illustrative, not a required production/development naming pattern. The mechanism is the selected configuration. Separate document trees or Git branches are not what makes an operation target production or development.

## Start from the production estate

Production must first have an installed estate: item bindings, Registry certifications, declaration dictionaries and current operational state in its catalogue. Mirror reads that installed projection rather than rebuilding production documents into the development targets.

Select the development configuration before planning the mirror. In that configuration:

- `catalogue` is the destination catalogue;
- `mirror` is the source catalogue;
- `targets` bind the same logical items to their development items.

Mirror empties and rebuilds the destination catalogue, then empties each selected destination target. It copies installed and current state, changes the selected items' physical bindings to their development targets, and creates local borrowed forms for production data. Warehouse relations are exposed as Views over their source. Lakehouse Tables and Folders are exposed through shortcuts, while source Views use local wrapper Views. The destination catalogue records each borrowed relation in `_.Mirror`.

Operational history remains with the estate where it happened: `_.Log` and `_.LoadStatistic` are not copied. Inspect the settled mirror plan before applying it: its destination catalogue and listed development targets are the destructive replacement boundary.

## Change the project, then Build

Edit the ordinary Weaver documents under `Lakehouse/Landing` or `Warehouse/Operations`. Their logical identities match the Registry rows copied from production, so Build can compare the edited declarations with the mirrored baseline.

For an unchanged borrowed object, the installed signature still matches and the local View or shortcut remains in place. For a changed borrowed object, Build follows dependencies within its selected scope:

1. the changed object and affected descendants are selected for local installation;
2. Build replaces each selected borrowed representation with its declared local form;
3. Build removes their `_.Mirror` rows after physical work and before catalogue publication;
4. unchanged objects retain their `_.Mirror` rows and continue to borrow production data.

The result is a mixed development estate. Some objects still read production; changed objects and affected descendants hold local data in the configured development targets. `_.Registry` continues to describe the logical installed object, while `_.Mirror` identifies which of those objects remain borrowed.

## Load, Test and Health the mixed estate

Load runs the installed work for locally materialised objects and records local bookmarks, status, statistics and logs. Borrowed data remains owned and loaded at its source rather than being written through the development pointer.

Test runs the installed Tests and Assumptions against the resulting estate. A validation can therefore exercise local changes while unchanged dependencies still resolve to production data.

Health combines both sides:

- installed and operational state for local objects comes from `Warehouse/ParcelCatalogueDev`;
- current Load state for objects still listed in `_.Mirror` comes from `Warehouse/ParcelCatalogue`;
- physical inventory is checked against the borrowed form recorded for each mirrored object and the local form of each materialised object.

Continue with another edit, Build, Load, Test and Health cycle. Re-mirror when development needs a fresh production baseline. It repeats the transition: the destination catalogue and selected development targets are emptied and reconstructed from the source, replacing local materialisations in that boundary.

The [Catalogue](catalogue.md) explains the state that changes through this loop. [Weaver operations](build-load-and-test.md) explains the lifecycle boundary between authored, installed and operational state. The [Mirror contract](../reference/operation-behaviour/mirror.md) defines the destructive transition, copied state and localisation boundary; exact command grammar remains in Reference.

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
