# Common metadata

Table, Folder and View documents share the identity, source-header and metadata rules on this page. Their kind pages list the additional keys and constraints for each document.

## Location, filename and identity

A document belongs to the item named by its path. Lakehouse data documents live directly under an area; Warehouse relations live directly under the item root.

| Kind | Lakehouse path | Warehouse path |
| --- | --- | --- |
| Table | `Lakehouse/<Item>/Tables/<Schema>__<Object>.py` or `Lakehouse/<Item>/Tables/<Schema>.<Object>.sql` | `Warehouse/<Item>/<Schema>.<Object>.sql` |
| Folder | `Lakehouse/<Item>/Files/<Schema>__<Object>.py` | Not supported |
| View | `Lakehouse/<Item>/Tables/<Schema>.<Object>.sql` | `Warehouse/<Item>/<Schema>.<Object>.sql` |

Python filenames use `Schema__Object.py`; SQL filenames use `Schema.Object.sql`. The metadata ID is always `Schema.Object`. Path, filename, ID and case must agree. For Python, the class must also be named `Schema__Object`.

The full logical identity includes the owning item. A Lakehouse identity also includes `Tables` or `Files`, so a Table and Folder may share `Schema.Object`. Documents must be directly under the location above; nested declaration directories are invalid. Exact and case-only identity collisions are invalid. Schema `_` is reserved for Weaver in ordinary items.

Files must be UTF-8 text. A Python document starts with a module docstring containing YAML metadata. A SQL document starts with a `/* ... */` YAML metadata block; the remaining text is its SQL body. The owning item selects Spark SQL for a Lakehouse and T-SQL for a Warehouse.

## Shared metadata keys

Keys are case-sensitive. Unknown and duplicate keys are errors.

| Key | Applies to | Required | Accepted value and default |
| --- | --- | --- | --- |
| `<Kind> ID` | Table, Folder, View | Yes | Exactly one ID key matching the kind and filename; a two-part `Schema.Object` string. |
| `Description` | Table, Folder, View | Yes | Non-empty prose or exactly one metadata reference. Placeholder-only values `not declared`, `n/a`, `tbd` and `todo` are invalid. |
| `Lineage` | Table, Folder, View | Yes | Non-empty prose or exactly one metadata reference. It describes origin; it does not create a dependency. |
| `Notes` | Table, Folder, View | No | Non-empty free text. Dollar signs and placeholder words have no special handling here. Default: absent. |
| `Revision notes` | Table, Folder, View | No | Non-empty YAML list of dated, non-empty notes. Default: empty list. |
| `Dependencies` | Table, Folder, View | Conditional | YAML list of distinct `Schema.Object` names. Default: inferred when the key is absent, except that every Spark SQL object must declare this key. |
| `Static` | Table, Folder, View | No | Boolean. Default: `false`. On a loadable Table or Folder, a clean prior load causes later ordinary loads to skip it; reload can reopen the Table gate. A View has no Load step, so this field creates no View load. |
| `Prohibit rebuild` | Table, Folder, View | No | Boolean. Default: `false`. When `true`, Build retains an existing object that would otherwise be dropped and recreated. It does not prevent first installation. |

A metadata reference is the whole value, not prose containing a reference:

- `$Schema.Object` or `$Schema.Object[Column]` — object in the current item;
- `$Files/Schema.Object` — Folder in the current Lakehouse item;
- `$Lakehouse/<Item>/Tables/Schema.Object`, `$Lakehouse/<Item>/Files/Schema.Object` or `$Warehouse/<Item>/Schema.Object` — item-qualified logical identity.

Use `$$` for a literal dollar sign. Metadata references in `Description`, `Lineage` and column notes are descriptive and do not add graph edges.

Each `Revision notes` entry starts with a date-shaped value in a plausible day/month range and then a note. A document must use one date shape throughout. Accepted shapes are `YYYY-MM-DD`, `YYYY/MM/DD`, `DD/MM/YYYY`, `DD-MM-YYYY` and `DD.MM.YYYY`; slash-separated day-first and month-first dates are not distinguished.

## Dependency inference and override

When `Dependencies` is absent, Weaver infers same-item dependencies from Python object imports and SQL relation references. Python object imports identify their Lakehouse area, for example `Tables.Parcel__Event` or `Files.Parcel__Manifest`. Two-part SQL relation names are candidates for managed objects; physically qualified SQL names and table-valued function calls are recorded as external references, not project graph edges.

When `Dependencies` is present, its list **replaces** inferred dependencies. `Dependencies: []` explicitly declares no graph dependencies even if source analysis finds references. Entries resolve with exact case inside the declaring item and may name a native object or logical Shortcut. Entries cannot repeat, name the document itself, or target a Test or Assumption. Use a Shortcut for a cross-item dependency.

Every Spark SQL Table or View must declare `Dependencies`, including `Dependencies: []` when it has none. T-SQL and Python documents may omit the key and use inference.

Foreign keys, Lineage and other descriptive references do not create dependencies.

## Python and SQL structure

A Python document contains exactly one top-level class that directly inherits the class named by its metadata kind. Helper classes may coexist. The Weaver class name must match the filename, and each required authored method must appear exactly once and must not be `async`. Check and Build parse this source without importing it or calling authored methods.

SQL metadata chooses Table or View; the suffix does not. Weaver checks the body structure statically where it can, but the target engine remains responsible for SQL validity and for behaviour that source analysis cannot establish.

These are Weaver **document-authoring** rules. Constructor parameters, runtime helpers and complete method signatures belong to [Python authored objects](../python/objects.md).

## Complete example

`Lakehouse/Logistics/Tables/Parcel__Event.py`:

```python
"""
Table ID: Parcel.Event

Description: One row per parcel event.

Lineage: Parcel scanner messages.

Notes: Times are recorded in UTC.

Revision notes:
  - 2026-09-18 Added the event type.

Schema:
  parcel_id: string
  event_type: string
"""

from weaver import Table


class Parcel__Event(Table):
    def read(self):
        return self.spark.createDataFrame([], "parcel_id string, event_type string")
```

This example uses dependency inference; it imports no other Weaver document.

## Operation and catalogue boundary

Check validates the complete project statically. Build validates it again, resolves dependencies and installs selected items; Build does not call Python `read()`. Load later executes installed Table and Folder load definitions. Test executes installed Tests and Assumptions, not these data documents. See [Build](../operation-behaviour/build.md), [Load](../operation-behaviour/load.md) and [Test](../operation-behaviour/test.md).

Build records installed identity and signatures in `_.Registry`, declarations in the appropriate dictionary, and resolved graph edges in `_.Dependency`. Exact fields are in the [catalogue schema](../catalogue-schema.md). These tables describe current output; this page does not add a catalogue-format compatibility guarantee.
