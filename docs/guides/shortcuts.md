# Connect parcel items with Shortcuts

This guide presents a Table owned by `Lakehouse/Tracking` inside `Lakehouse/Reporting` and `Warehouse/Dispatch`. The logical Shortcuts retain the Weaver document identity, so Build can record a cross-item dependency instead of treating the source as an unrelated Fabric location.

## Prerequisites

- [Install Weaver](../get-started/installation.md) and confirm `weaver --version` works.
- Create or reuse a project whose workspace configuration binds `Lakehouse/Tracking`, `Lakehouse/Reporting` and `Warehouse/Dispatch` to Fabric items.
- Publish the project's Fabric Environment before loading the Python Table in `Lakehouse/Reporting`.

The checked logical fixture is `examples/parcel-shortcuts/logical/`. The separate physical declaration is under `examples/parcel-shortcuts/physical/` so it can be checked without requiring an external Fabric item.

## Add the source Table

Create this project structure:

```text
Lakehouse/
├── Tracking/
│   └── Tables/
│       └── Parcel.Event.sql
└── Reporting/
    ├── shortcuts.py
    └── Tables/
        └── Parcel__EventSummary.py
Warehouse/
└── Dispatch/
    └── shortcuts.yml
```

Create `Lakehouse/Tracking/Tables/Parcel.Event.sql`:

```sql
/*
Table ID: Parcel.Event

Description: One row per parcel tracking event.

Lineage: A carrier event feed represented by this example.

Dependencies: []

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: string
  Event sequence: integer
  Status: string
*/
select *
from values
    ('P-1001', 1, 'Accepted'),
    ('P-1001', 2, 'In transit'),
    ('P-1002', 1, 'Delivered')
as event(`Parcel ID`, `Event sequence`, `Status`);
```

`Parcel.Event` belongs to the logical `Lakehouse/Tracking` item. The next declarations refer to that logical identity rather than a workspace-specific Lakehouse name.

## Present the Table in another Lakehouse

Create `Lakehouse/Reporting/shortcuts.py`:

```python
from weaver import Shortcut

Parcel__Event = Shortcut(
    shortcut_type="table",
    target_type="logical",
    target="Lakehouse/Tracking/Tables/Parcel.Event",
)
```

The symbol names the destination: `Lakehouse/Reporting/Tables/Parcel.Event`. The `target` names the source Weaver document. A logical Shortcut cannot name `workspace`; workspace configuration supplies the physical bindings for both logical items.

Create `Lakehouse/Reporting/Tables/Parcel__EventSummary.py`:

```python
"""
Table ID: Parcel.EventSummary

Description: Tracking events read through the local Shortcut destination.

Lineage: $Parcel.Event

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: string
  Event sequence: integer
  Status: string
"""

from shortcuts import Parcel__Event

from weaver import Table


class Parcel__EventSummary(Table):
    def read(self):
        return Parcel__Event(self).dataframe().select(*self.columns())
```

Import from `shortcuts`, not from the authored `weaver.Shortcut` declaration. Build deploys a runtime `shortcuts` module whose reader opens the local destination in `Lakehouse/Reporting`. The import also tells Weaver that `Parcel.EventSummary` depends on `Lakehouse/Tracking/Tables/Parcel.Event` through the Shortcut.

## Present the same Table in a Warehouse

Warehouse Shortcuts use a YAML mapping. Create `Warehouse/Dispatch/shortcuts.yml`:

```yaml
logical:
  "Warehouse/Dispatch/Parcel.Event": "Lakehouse/Tracking/Tables/Parcel.Event"
```

The mapping is destination to target. Build creates the Warehouse destination as a local View over the source. It is not separate Load work; queries against `Parcel.Event` in the Dispatch Warehouse read through that View.

The Lakehouse and Warehouse forms express the same logical relationship on different authoring surfaces. Lakehouse declarations choose `table`, `folder` or a physical `schema` destination in `shortcuts.py`. Warehouse declarations create Views and group mappings under `logical` or `physical` in `shortcuts.yml`. Use the [Reference](../reference/index.md) for the full accepted syntax rather than extrapolating from this task.

## Check and build all participating items

Run the local check:

```bash
weaver check
```

A successful check confirms that the logical target exists in this project, the destination names are valid and the imported Shortcut resolves to its source. It does not contact Fabric or prove that OneLake can create the destination.

For the first installation, select every participating item:

```bash
weaver build \
  --item Lakehouse/Tracking \
  --item Lakehouse/Reporting \
  --item Warehouse/Dispatch
```

Build uses the logical dependency to order selected work and to include affected selected descendants when the source changes. Selection remains the boundary: naming `Lakehouse/Reporting` does not silently add `Lakehouse/Tracking`, and leaving `Warehouse/Dispatch` unselected leaves its installed View unchanged. On a first build, select the producer and consumers together.

After Build succeeds, the [catalogue](../core-concepts/catalogue.md) records the Shortcut and resolved dependency. Fabric should contain:

- `Tables/Parcel/Event` as a OneLake Shortcut in the Reporting Lakehouse;
- `Parcel.Event` as a View in the Dispatch Warehouse.

These are Fabric checkpoints. `weaver check` cannot observe either physical destination.

## Load the producer before its Lakehouse consumer

Publish the Environment, preview the selected items and then load them:

```bash
weaver fabric environment publish \
  --path Environment/Weaver.Environment
weaver load Lakehouse/Tracking Lakehouse/Reporting --dry-run
weaver load Lakehouse/Tracking Lakehouse/Reporting
```

The dry run should place the Tracking source before `Tables/Parcel.EventSummary`. Cross-item dependency does not widen Load selection, so name both items when both should run. The Warehouse Shortcut is a View and has no separate load step.

After the Fabric load succeeds, query `Parcel.EventSummary` in the Reporting Lakehouse and `Parcel.Event` in the Dispatch Warehouse. Each should expose the three source rows. Those outcomes depend on Fabric execution and are not established by local parsing.

## Use a physical Shortcut for an external location

A physical Shortcut names a Fabric location directly. It is appropriate when the source is outside the managed Weaver estate. For example, the independently checked `examples/parcel-shortcuts/physical/Lakehouse/Reporting/shortcuts.py` contains:

```python
from weaver import Shortcut

Parcel__Milestone = Shortcut(
    shortcut_type="table",
    target_type="physical",
    target="Lakehouse/Carrier/Tables/Parcel.Milestone",
    workspace="Carrier Shared",
)
```

Here `Lakehouse/Carrier` is a physical item in the named workspace, not a logical item from this project. `weaver check` validates the declaration shape without contacting that workspace. Build must resolve the workspace and source item and Fabric must permit the Shortcut creation.

A physical Shortcut is a dependency boundary: Weaver does not infer a managed producer or Build order from the external address. Its runtime reader can read the local destination, but source bookmark and Folder change-history methods require logical metadata and therefore are unavailable. If the source is another Weaver document, use a logical Shortcut instead.

## Troubleshooting and next action

If `weaver check` cannot resolve a logical target, correct the exact `ItemType/ItemName/Area/Schema.Object` identity or add the missing source document. If Build reports that the source has no installation, include the source item in the first Build or install it before rebuilding the consumer. If Fabric reports a conflict at the destination, remove or rename the existing object; do not place a Weaver document at the same destination as a Shortcut.

Use [Weaver documents](../core-concepts/weaver-documents.md) for Shortcut ownership, [Dependencies](../core-concepts/dependencies.md) for cross-item ordering and selection, and [Weaver operations](../core-concepts/weaver-operations.md) for the Build/Load boundary. [Development cycle](../core-concepts/development-cycle.md) explains how Shortcut changes materialise in a mirrored estate. Command forms are in the [CLI reference](../reference/cli.md), and Load selection behaviour is in the [Load contract](../contracts/load.md).
