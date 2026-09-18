# Development cycle

A development estate can start from production's installed state without maintaining a second set of Weaver documents. Mirror is the state transition into that estate, not merely a command that copies data. The selected workspace configuration changes the catalogue and physical targets; the project keeps the same logical item identities and declarations.

This page applies the [Build, Load and Test lifecycle](../core-concepts/build-load-and-test.md) to a mirrored development estate. See the [CLI reference](../reference/cli.md) for command forms and options.

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

The [Catalogue](../core-concepts/catalogue.md) explains the state that changes through this loop. [Weaver operations](../core-concepts/build-load-and-test.md) explains the lifecycle boundary between authored, installed and operational state. The [Mirror contract](../reference/operation-behaviour/mirror.md) defines the destructive transition, copied state and localisation boundary; exact command grammar remains in Reference.
