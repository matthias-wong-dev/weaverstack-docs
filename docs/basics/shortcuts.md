# Connect items with a Shortcut

This guide presents a Table owned by `Lakehouse/Tracking` as a View in `Warehouse/Dispatch`. The logical Shortcut keeps the source's Weaver identity, so Build can manage the cross-item relationship.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Use a Fabric workspace where you can create or modify a catalogue Warehouse, a Lakehouse and a second Warehouse.

## 1. Initialise both items

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

## 2. Add the source Table

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

## 3. Present it in the Warehouse

Create `Warehouse/Dispatch/shortcuts.yml`:

```yaml
logical:
  "Warehouse/Dispatch/Parcel.Event": "Lakehouse/Tracking/Tables/Parcel.Event"
```

The mapping reads from destination to target. Build creates `Parcel.Event` in the Dispatch Warehouse as a View over the Table owned by the Tracking Lakehouse. Because the target is logical, Weaver records a managed dependency from `Warehouse/Dispatch` to `Lakehouse/Tracking`.

This is the normal cross-item form when the source is another document in the same Weaver project. The [Shortcut reference](../reference/weaver-documents/shortcut.md) lists Lakehouse destinations, physical targets and the exact accepted target forms.

## 4. Check and build the relationship

Validate the declarations, then install all configured items:

```bash
weaver check
weaver build
```

Check prints `Project valid.` It confirms that the logical target exists and that both Shortcut identities are valid without contacting Fabric. Build should report no failed actions and install the Tracking Table before the Dispatch View.

## 5. Load the producer

Run the loadable work in the source item and read both items' state:

```bash
weaver load Lakehouse/Tracking
weaver health \
  --item Lakehouse/Tracking \
  --item Warehouse/Dispatch
```

Load should report `Tables/Parcel.Event` as succeeded with three rows. The Shortcut View has no separate Load step. Health should show the installed relationship without a failed Build or Load finding.

Dependencies order selected work but do not widen selection. When both sides contain loadable work, name both items in the item-wide Load command.

## 6. Query through the Shortcut

Query the Dispatch Warehouse SQL endpoint:

```sql
select [Parcel ID], [Event sequence], [Status]
from [Parcel].[Event]
order by [Parcel ID], [Event sequence];
```

The View returns the three rows stored in `Lakehouse/Tracking/Tables/Parcel.Event`. The physical Lakehouse and Warehouse names remain in `workspace-config.yml`; the Shortcut declaration keeps only logical project identities.

After changing the source declaration, Build the affected items and use `weaver load Lakehouse/Tracking --stale` for post-Build catch-up. [Dependencies](../core-concepts/dependencies.md) explains cross-item ordering and selection boundaries.
