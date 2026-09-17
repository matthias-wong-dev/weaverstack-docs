# Development cycle

A development estate can start from production's installed state without maintaining a second set of Weaver documents. The selected workspace configuration changes the catalogue and physical targets; the project keeps the same logical item identities and declarations.

This page assumes the mirror and Session/workflow models. It applies the [Build, Load and Test lifecycle](weaver-operations.md) to a mirrored development estate rather than repeating the operation model or command syntax. See the [CLI reference](../reference/cli.md) for command forms and options.

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

The mirror supplies a development baseline. Build then materialises changed borrowed objects and affected descendants where the edited project requires local state. Unchanged objects continue to read production data through their local Views or shortcuts.

## Configuration is the environment switch

A production and development configuration can bind the same project to different physical items. A real project uses these two files in the same project directory.

Production configuration:

```yaml
workspace: Data Without Guessing
environment: dwg-environment
catalogue: Warehouse/Catalogue

targets:
  Lakehouse/T1_DWG: T1_DWG
  Warehouse/T2_DWG: T2_DWG
```

Development configuration:

```yaml
workspace: Data Without Guessing
environment: dwg-environment
catalogue: Warehouse/DEV_Catalogue
mirror: Warehouse/Catalogue

targets:
  Lakehouse/T1_DWG: DEV_T1_DWG
  Warehouse/T2_DWG: DEV_T2_DWG
```

The project and logical item keys are unchanged:

- `Lakehouse/T1_DWG`
- `Warehouse/T2_DWG`

The selected configuration changes their physical targets from `T1_DWG` and `T2_DWG` to `DEV_T1_DWG` and `DEV_T2_DWG`. It also changes the catalogue from `Warehouse/Catalogue` to `Warehouse/DEV_Catalogue` and names the production catalogue as the mirror source.

These names are one project's convention, not a required production/development naming pattern. The mechanism is the selected configuration. Separate document trees or Git branches are not what makes an operation target production or development.

## Start from the production estate

Production must first have an installed estate: item bindings, Registry certifications, declaration dictionaries and current operational state in its catalogue. Mirror reads that installed projection rather than rebuilding production documents into the development targets.

Select the development configuration before planning the mirror. In that configuration:

- `catalogue` is the destination catalogue;
- `mirror` is the source catalogue;
- `targets` bind the same logical items to their development items.

Mirror replaces the selected destination catalogue and target contents, copies installed and current state, and creates local borrowed forms for production data. Warehouse relations are exposed as Views over their source. Lakehouse Tables and Folders are exposed through shortcuts, while source Views use local wrapper Views. The destination catalogue records each borrowed relation in `_.Mirror`.

Operational history remains with the estate where it happened: `_.Log` and `_.LoadStatistic` are not copied. Inspect the settled mirror plan before applying it because mirroring empties the destination catalogue and selected development targets.

## Change the project, then Build

Edit the ordinary Weaver documents under `Lakehouse/T1_DWG` or `Warehouse/T2_DWG`. Their logical identities match the Registry rows copied from production, so Build can compare the edited declarations with the mirrored baseline.

For an unchanged borrowed object, the installed signature still matches and the local View or shortcut remains in place. For a changed borrowed object selected by Build:

1. Build replaces the borrowed representation with the declared local object;
2. affected local descendants are rebuilt or refreshed according to the dependency graph;
3. the object's `_.Mirror` row is removed after it is materialised;
4. unchanged objects retain their `_.Mirror` rows and continue to borrow production data.

The result is a mixed development estate. Some objects still read production; changed objects hold local data in the configured development targets. `_.Registry` continues to describe the logical installed object, while `_.Mirror` identifies which of those objects remain borrowed.

## Load, Test and Health the mixed estate

Load runs the installed work for locally materialised objects and records local bookmarks, status, statistics and logs. Borrowed data remains owned and loaded at its source rather than being written through the development pointer.

Test runs the installed Tests and Assumptions against the resulting estate. A validation can therefore exercise local changes while unchanged dependencies still resolve to production data.

Health combines both sides:

- installed and operational state for local objects comes from `Warehouse/DEV_Catalogue`;
- current Load state for objects still listed in `_.Mirror` comes from `Warehouse/Catalogue`;
- physical inventory is checked against the borrowed form recorded for each mirrored object and the local form of each materialised object.

Continue with another edit, Build, Load, Test and Health cycle. Re-mirror when development needs a fresh production baseline; that starts again by replacing the configured development destinations.

The [Catalogue](catalogue.md) explains the state that changes through this loop. [Weaver operations](weaver-operations.md) explains the lifecycle boundary between authored, installed and operational state. Exact workspace-configuration fields, precedence, mirror selection and command grammar belong in Reference.
