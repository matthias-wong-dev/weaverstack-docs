# Weaver catalogue

The Weaver catalogue is a configured Fabric Warehouse that records the estate Weaver has installed and the results of operating it. It is the shared state behind Build, Load, Test and Health.

Project source and catalogue state answer different questions:

- project source declares what the estate should be;
- the catalogue records what Weaver installed, where it installed it and what later runs did.

[How Weaver works](how-weaver-works.md) places both in the normal lifecycle. [Projects and estates](projects-and-estates.md) explains the wider project and workspace boundary.

## State you can rely on

For installed logical items, the catalogue records enough public state for Weaver to recover:

- the logical item and its physical Fabric target;
- installed objects and their kinds;
- declaration signatures and Build timestamps;
- resolved dependencies and shortcuts;
- installed Load, Test and Assumption work;
- current Load and Test outcomes, run activity and bookmarks;
- which objects are borrowed through a mirror.

Logical identity remains item-aware. Two items may bind to one physical target without sharing ownership, and a Lakehouse Folder and Table with the same `Schema.Object` remain distinct. See [Logical and physical items](logical-and-physical-items.md) and [Resources and artefacts](resources-and-artefacts.md).

The catalogue does not claim ownership of every object found in a Lakehouse or Warehouse. A physical object can exist without being part of Weaver's installed estate. Conversely, catalogue state can become stale when a target is changed outside Weaver; Build reconciles relevant recorded claims with the target before relying on them.

## Repository intent becomes an installed projection

A parsed project can describe all of its intended metadata, dependencies and resources without knowing a physical target. Build adds the selected bindings, compares that intent with the current installed and physical state, and applies the required structural changes.

Only the selected, successfully installed result becomes the new catalogue projection. An omitted item is outside that Build's scope. A declaration that has changed in source does not change Load or Test until Build installs it.

This distinction is visible in the [First project](../get-started/first-project.md): Build installs the Table and Test definitions, then Load and Test use those installed definitions. The [Lakehouse pipeline](../guides/lakehouse-pipeline.md) and [Warehouse pipeline](../guides/warehouse-pipeline.md) show the same boundary for larger items.

## How commands use the catalogue

### Build

Build reads catalogue state for the selected logical items, compares it with project intent and the relevant Fabric targets, and publishes the resulting installed state. The first successful Build creates the catalogue structures when they are absent.

Dependencies affect Build ordering and change impact, but they do not widen item selection. See [Dependencies](dependencies.md) and the [CLI reference](../reference/cli.md#build-and-install).

### Load

Load resolves logical items to their installed targets, selects installed loadable objects and orders item-wide work from the installed dependencies. It does not reopen project source.

The [Load contract](../contracts/load.md) defines the resulting selection, ordering, bookmarks and recorded outcomes.

### Test

Test selects installed Tests and Assumptions for the requested logical items and runs their installed forms. A declared validation whose runnable form is missing is an execution failure, not a pass and not an item to skip silently.

### Health

Health combines installed state with current Load and Test state. It reports on the targets bound to the selected logical items and can compare the catalogue's claims with physical inventory unless that check is disabled.

A Green report therefore means the selected installed estate is current and successful according to the checks Health performed. It does not mean that every unregistered object in the same physical Fabric item belongs to Weaver.

The [CLI reference](../reference/cli.md#load-test-and-health-selection) defines selection and exit behaviour for Load, Test and Health.

## Treat the catalogue as read-only

Do not insert, update or delete catalogue state by hand. Use Build and the runtime commands as its writers, and use the Weaver CLI to inspect outcomes.

Manual edits can make an object appear installed, move a logical item to the wrong target, remove dependency ordering or separate an outcome from the run that produced it. The catalogue's storage layout is not a public extension API; the public contract is the behaviour Weaver exposes through Build, Load, Test, Health, mirror and wipe.

Configure a separate catalogue Warehouse or allow it to share a Warehouse with application schemas. In either case, Weaver's catalogue state remains separate from the project's materialised output. The [First project](../get-started/first-project.md#1-initialise-the-project) shows the catalogue and project Warehouse as separate items, while [How Weaver works](how-weaver-works.md#physical-bindings) explains the binding.

## Mirrors preserve installed meaning

A mirror creates a destination estate from another catalogue's installed state. The destination catalogue records which objects remain borrowed from the source, while local bindings identify where the mirrored logical items live.

That record has operational consequences:

- an unchanged project can Build against the mirrored estate without rebuilding borrowed objects;
- when Build materialises a changed borrowed object locally, that object stops being borrowed;
- Health consults the configured source catalogue for current operational state when selected objects still depend on it.

A mirror is therefore not a replacement for project source and not an invitation to edit catalogue records. It is another installed projection, tied to a named source and destination. Inspect the destructive scope before running it; the [CLI reference](../reference/cli.md#destructive-commands) describes mirror and wipe responsibilities.
