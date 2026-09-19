# Connect data with Shortcuts

A logical Shortcut connects two parts of the Weaver project. A physical Shortcut marks the boundary where the Weaver project connects to something it does not own.

```text
managed producer → logical Shortcut → managed consumer
```

```text
external physical data → physical Shortcut → managed work
```

Choose the target type from who owns the source:

| Target | Use it when | Consequence |
| --- | --- | --- |
| `logical` | Another Weaver document owns the source. | The target is a full Weaver identity. Weaver manages the dependency and records the relationship in the catalogue. |
| `physical` | A Fabric item outside the project owns the source. | The target is a physical Fabric address. Weaver manages the local Shortcut, but the external source has no managed producer, Build producer or project graph edge. |

The sections below show one complete logical path and one ordinary physical declaration. Use the [Shortcut reference](../reference/weaver-documents/shortcut.md) for every accepted Table, Folder, Schema and View form.

## Connect managed items with a logical Shortcut

This tutorial presents a Table owned by `Lakehouse/Tracking` as a View in `Warehouse/Dispatch`. The declaration keeps the source's Weaver identity, so it can follow different physical bindings while Build manages the cross-item relationship.

### Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Use a Fabric workspace where you can create or modify a catalogue Warehouse, a Lakehouse and a second Warehouse.

### 1. Initialise both items

Create a project containing the producer and consumer:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-shortcut \
  --catalogue Catalogue \
  --lakehouse Tracking \
  --warehouse Dispatch \
  --no-example
cd parcel-shortcut
```

Replace `Parcel Development` with your workspace. Weaver writes bindings for `Lakehouse/Tracking` and `Warehouse/Dispatch` to `workspace-config.yml`. The command ends with `Weaver project ready in .../parcel-shortcut.`

### 2. Add the source Table

Create `Lakehouse/Tracking/Tables/Parcel.Event.sql`:

```sql
/*
Table ID: Parcel.Event

Description: One row per parcel tracking event.

Lineage: A deterministic carrier feed represented by this example.

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

The source is a Spark SQL Table, so it explicitly declares that it has no managed dependencies.

### 3. Present it in the Warehouse

Create `Warehouse/Dispatch/shortcuts.yml`:

```yaml
logical:
  "Warehouse/Dispatch/Parcel.Event": "Lakehouse/Tracking/Tables/Parcel.Event"
```

The mapping reads from destination to target. Build creates `Parcel.Event` in the Dispatch Warehouse as a View over the Table owned by the Tracking Lakehouse. Because the target is logical, Weaver adds a managed dependency from `Warehouse/Dispatch` to `Lakehouse/Tracking` and records the Shortcut relationship in the catalogue.

The target must remain the full Weaver identity `Lakehouse/Tracking/Tables/Parcel.Event`, not a Fabric item name. That declaration can stay unchanged while workspace configurations bind `Lakehouse/Tracking` to `ParcelTrackingDev` in development and `ParcelTracking` in production:

```yaml title="workspace-development.yml"
targets:
  Lakehouse/Tracking: ParcelTrackingDev
  Warehouse/Dispatch: ParcelDispatchDev
```

```yaml title="workspace-production.yml"
targets:
  Lakehouse/Tracking: ParcelTracking
  Warehouse/Dispatch: ParcelDispatch
```

The selected configuration supplies the physical source and destination. [Configure a workspace and Python runtime](workspace-and-python-runtime.md) shows complete configuration files and how to select one.

### 4. Check and build the relationship

Validate the declarations, then install all configured items:

```bash
weaver check
weaver build
```

Check prints `Project valid.` It confirms that the logical target exists and that both Shortcut identities are valid without contacting Fabric. Build should report no failed actions and install the Tracking Table before the Dispatch Shortcut View.

For selected work, Build follows this order:

```text
source document → logical Shortcut → consuming document
```

A changed source can select the Shortcut and affected downstream consumers within the requested Build boundary. Dependencies order and affect selected work; they do not add an unselected item. Select every item whose installed state should change.

### 5. Load the producer

Run the loadable work in the source item and read both items' state:

```bash
weaver load Lakehouse/Tracking
weaver health \
  --item Lakehouse/Tracking \
  --item Warehouse/Dispatch
```

Load should report `Tables/Parcel.Event` as succeeded with three rows. The Shortcut View has no separate Load step. Health should show the installed relationship without a failed Build or Load finding.

When both sides have loadable work, select both items in an item-wide Load. Weaver then uses the installed dependency relationship to order the producer before the consumer. Dependencies do not widen Load selection, and deliberately naming individual documents does not apply dependency ordering.

### 6. Query through the Shortcut

Query the Dispatch Warehouse SQL endpoint:

```sql
select [Parcel ID], [Event sequence], [Status]
from [Parcel].[Event]
order by [Parcel ID], [Event sequence];
```

The View returns the three rows stored in `Lakehouse/Tracking/Tables/Parcel.Event`. The physical Lakehouse and Warehouse names remain in the selected workspace configuration; the Shortcut declaration keeps logical project identities.

After changing the source declaration, Build the affected items and use `weaver load Lakehouse/Tracking --stale` for post-Build catch-up. [Dependencies](../core-concepts/dependencies.md) explains cross-item ordering and selection boundaries.

## Connect external data with a physical Shortcut

Use a physical Shortcut when Fabric data has no owning Weaver document in this project. Keep the source in a separate physical item that is not bound as a managed target. For example, `ParcelSourceArchive` may hold externally owned files while `Lakehouse/Tracking` is bound to the managed `ParcelTracking` Lakehouse.

Create `Lakehouse/Tracking/shortcuts.py`:

```python
from weaver import Shortcut


Parcel__StatusSource = Shortcut(
    shortcut_type="folder",
    target_type="physical",
    target="Lakehouse/ParcelSourceArchive/Files/parcel-status",
)
```

Build manages the local `Lakehouse/Tracking/Files/Parcel.StatusSource` Shortcut and records its external target. It does not manage or build `ParcelSourceArchive`, and the declaration adds no producer or edge to the project dependency graph. Do not add the source Lakehouse as another managed target: Build may prune undeclared co-located content inside every selected managed item.

Installed Python code imports the generated local destination and uses its public reader interface:

```python
from shortcuts import Parcel__StatusSource

source_root = Parcel__StatusSource(self).path()
```

`path()` returns a mounted `pathlib.Path` for ordinary Python file access. `spark_path()` returns a string for Spark readers; do not treat that Spark URI as a `pathlib.Path`.

A physical target without `workspace` uses the configured workspace. Add `workspace="Carrier Shared"` to a Lakehouse Shortcut when the source belongs to that other workspace. A Warehouse physical View Shortcut is restricted to the configured workspace because `shortcuts.yml` has no workspace field. Keep the complete target grammar, destination rules, and compatibility combinations in the [Shortcut reference](../reference/weaver-documents/shortcut.md).
