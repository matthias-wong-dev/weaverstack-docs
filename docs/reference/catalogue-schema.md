# Catalogue schema

The Weaver catalogue is a set of Warehouse tables in schema `_`. This page records the current physical inspection surface: table names, public column names, keys, nullability, types, and meanings.

It is a read-only integration boundary. Query these tables for inspection and reporting; do not insert, update, delete, truncate, rebuild, or add application-owned objects under `_`. Build and runtime operations own their rows and lifecycle.

This is not a versioned database schema. The catalogue has no schema-version table or compatibility number, and this page makes no promise that a later Weaver release preserves these columns. Weaver checks the tables and columns it needs when it opens a catalogue and rejects missing or incompatible state rather than offering a general schema migration contract.

## Reading the tables

Public Warehouse column names contain spaces and use title case, so quote them with brackets:

```sql
select
    [Item type],
    [Item name],
    [Target name]
from [_].[Installation];
```

In the definitions below, **key** lists the current logical key in order. `required` means Weaver declares the column non-null; `nullable` means null is part of the current representation. Keys are identity definitions even where Fabric Warehouse does not enforce a relational constraint.

Every table also has these required `datetime2(6)` audit columns:

- `Row insert datetime` — when Weaver inserted the row;
- `Row update datetime` — when Weaver last updated the row; and
- `Row delete datetime` — the soft-delete audit field; a live row uses Weaver's maximum-date sentinel rather than null.

## Projected catalogue tables

Build reconciles these tables from authored project state. Every projected row has a required `Signature` (`varchar(128)`) used to detect changes.

### `_.Installation`

One row per logical item installation, mapping it to its physical target.

**Key:** `Item type`, `Item name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Target name` | `varchar(128)` | required | Physical Fabric item currently bound to the installation. |
| `Weaver version` | `varchar(128)` | required | Weaver version that last reconciled the installation. |
| `Signature` | `varchar(128)` | required | Content hash of the Item declaration. |

### `_.Registry`

Objects certified as installed. Build writes Registry after the object and its dependencies succeed.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Object type` | `varchar(128)` | required | `Folder`, `Table`, `View`, `File`, `Stored procedure`, or `Schema`. |
| `Object role` | `varchar(128)` | required | `Data`, `Load`, `Test`, `Assumption`, `Shortcut`, or `Programmable`. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file. |
| `Build datetime` | `datetime2(6)` | nullable | Publication time shared by all Registry rows written by one completed build. |

### `_.SchemaDictionary`

Declared schemas and their descriptions.

**Key:** `Item type`, `Item name`, `Schema name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Declared schema. |
| `Description` | `varchar(4000)` | nullable | Authored schema description. |
| `Description reference` | `varchar(128)` | nullable | `$Schema.Object` from which the description was copied. |
| `Signature` | `varchar(128)` | required | Content hash of the schema declaration. |

### `_.TableDictionary`

Declared Tables and Views. These rows describe authored documents, not a physical inventory.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Object type` | `varchar(128)` | required | Authored object type: Table or View. |
| `Description` | `varchar(4000)` | nullable | Authored object description. |
| `Description reference` | `varchar(128)` | nullable | `$Schema.Object` supplying the description. |
| `Lineage` | `varchar(4000)` | nullable | Authored statement of where the data comes from. |
| `Lineage reference` | `varchar(128)` | nullable | `$Schema.Object` supplying the lineage. |
| `Primary key` | `varchar(1000)` | nullable | Primary-key columns in declared order. |
| `Not null columns` | `varchar(1000)` | nullable | Declared non-null columns beyond the primary key. |
| `Identity column` | `varchar(128)` | nullable | Weaver-managed surrogate column, when declared. |
| `Comparison columns` | `varchar(1000)` | nullable | Columns whose change drives an upsert. |
| `Is incremental` | `bit` | nullable | Whether Load accumulates rows rather than replacing them. |
| `Is static` | `bit` | nullable | Whether the object loads once rather than being refreshed. |
| `Prohibit rebuild` | `bit` | nullable | Whether Build may drop and recreate the object. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file. |

### `_.FolderDictionary`

Managed Folders and the file patterns their reconciliation owns.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Folder schema. |
| `Object name` | `varchar(128)` | required | Folder object name. |
| `Description` | `varchar(4000)` | nullable | Authored folder description. |
| `Description reference` | `varchar(128)` | nullable | `$Schema.Object` supplying the description. |
| `Lineage` | `varchar(4000)` | nullable | Authored data origin. |
| `Lineage reference` | `varchar(128)` | nullable | `$Schema.Object` supplying the lineage. |
| `File key` | `varchar(1000)` | nullable | Managed glob patterns in declared order. |
| `Is incremental` | `bit` | nullable | Whether Load accumulates files or rows. |
| `Is static` | `bit` | nullable | Whether the Folder loads once. |
| `Prohibit rebuild` | `bit` | nullable | Whether Build may drop and recreate it. |
| `Signature` | `varchar(128)` | required | Content hash of the source file. |

### `_.ColumnDictionary`

Authored column descriptions and Weaver-managed surrogate columns. It is not an inventory of every physical column.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`, `Column name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Column name` | `varchar(128)` | required | Authored or managed column. |
| `Description` | `varchar(4000)` | nullable | Authored column description. |
| `Description reference` | `varchar(128)` | nullable | `$Schema.Object` supplying the description. |
| `Is identity` | `bit` | nullable | Whether this is Weaver's managed surrogate column. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file. |

### `_.KeyDictionary`

Declared logical primary and alternate keys. Weaver does not build or enforce them as database constraints.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`, `Key type`, `Column set`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Key type` | `varchar(128)` | required | `Primary key` or `Unique`. |
| `Column set` | `varchar(1000)` | required | Key columns, comma-separated in declared order. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file. |

### `_.ForeignKeyDictionary`

Declared relationships, not database constraints. A row is an unnamed edge, and the primary side includes logical item identity for cross-item relationships.

**Key:** `Item type`, `Item name`, `Foreign schema name`, `Foreign object name`, `Foreign column set`, `Primary item type`, `Primary item name`, `Primary schema name`, `Primary object name`, `Primary column set`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Referencing logical item type. |
| `Item name` | `varchar(128)` | required | Referencing logical item name. |
| `Foreign schema name` | `varchar(128)` | required | Schema declaring the relationship. |
| `Foreign object name` | `varchar(128)` | required | Object declaring the relationship. |
| `Foreign column set` | `varchar(1000)` | required | Foreign columns in declared order. |
| `Primary item type` | `varchar(128)` | required | Referenced logical item type. |
| `Primary item name` | `varchar(128)` | required | Referenced logical item name. |
| `Primary schema name` | `varchar(128)` | required | Referenced schema. |
| `Primary object name` | `varchar(128)` | required | Referenced object. |
| `Primary column set` | `varchar(1000)` | required | Primary columns paired in order with foreign columns. |
| `Signature` | `varchar(128)` | required | Content hash of the declaring object's source file. |

### `_.TestDictionary`

Declared Tests and Assumptions, rather than the procedures or modules they compile to.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Validation schema. |
| `Object name` | `varchar(128)` | required | Validation name. |
| `Test type` | `varchar(128)` | required | `Test` or `Assumption`. |
| `Description` | `varchar(4000)` | nullable | Authored validation description. |
| `Description reference` | `varchar(128)` | nullable | `$Schema.Object` supplying the description. |
| `Primary key` | `varchar(1000)` | nullable | Test correlation key in declared order; null when undeclared and for Assumptions. |
| `Signature` | `varchar(128)` | required | Content hash of the validation source. |

### `_.Dependency`

Resolved dependency edges and their authored references, scoped to the referencing item. Cross-item and cross-engine edges are represented as Shortcuts.

**Key:** `Item type`, `Item name`, `Referencing schema name`, `Referencing object name`, `Dependency reference`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Referencing logical item type. |
| `Item name` | `varchar(128)` | required | Referencing logical item name. |
| `Referencing schema name` | `varchar(128)` | required | Schema declaring the dependency. |
| `Referencing object name` | `varchar(128)` | required | Object declaring the dependency. |
| `Dependency reference` | `varchar(1000)` | required | Reference exactly as the document wrote it. |
| `Referenced item type` | `varchar(128)` | nullable | Resolved referenced item type. |
| `Referenced item name` | `varchar(128)` | nullable | Resolved referenced item name. |
| `Referenced schema name` | `varchar(128)` | nullable | Resolved referenced schema. |
| `Referenced object name` | `varchar(128)` | nullable | Resolved referenced object. |
| `Signature` | `varchar(128)` | required | Content hash of the owning object's source file. |

### `_.Shortcut`

Declared cross-item, cross-engine, and cross-workspace edges. Logical targets remain logical; `_.Installation` supplies their physical binding.

**Key:** `Item type`, `Item name`, `Shortcut ID`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Destination logical item type. |
| `Item name` | `varchar(128)` | required | Destination logical item name. |
| `Shortcut ID` | `varchar(128)` | required | Authored shortcut identity, such as `Logistics.Parcel` or a schema name. |
| `Schema name` | `varchar(128)` | required | Schema in which this item presents the shortcut. |
| `Object name` | `varchar(128)` | nullable | Presented object; null for a schema shortcut. |
| `Shortcut type` | `varchar(128)` | required | `Table`, `Schema`, `Folder`, or `View`. |
| `Target type` | `varchar(128)` | required | `Logical` or `Physical`. |
| `Target item type` | `varchar(128)` | required | Target item type. |
| `Target item name` | `varchar(128)` | required | Target item name. |
| `Target schema name` | `varchar(128)` | required | Target schema or path. |
| `Target object name` | `varchar(128)` | nullable | Target object; null for a schema or path. |
| `Target workspace name` | `varchar(128)` | nullable | Explicit target workspace; null for logical targets and local physical targets. |
| `Signature` | `varchar(128)` | required | Content hash of the shortcut declaration. |

## Runtime tables

Runtime operations maintain these tables. `_.Log` and `_.LoadStatistic` are append-only history. `_.Bookmark`, `_.LoadStatus`, and `_.TestStatus` represent current object state and are invalidated when the owning incarnation is rebuilt.

### `_.Log`

One row per settled unit of Weaver work.

**Key:** `Log SK`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Log SK` | `varchar(128)` | required | Immutable writer-generated surrogate. |
| `Workflow ID` | `varchar(128)` | required | Correlates rows produced by one workflow. |
| `Task type` | `varchar(128)` | required | Kind of work that settled. |
| `Target type` | `varchar(128)` | nullable | Physical target type. |
| `Target name` | `varchar(128)` | nullable | Physical target name. |
| `Schema name` | `varchar(128)` | nullable | Object schema. |
| `Object name` | `varchar(128)` | nullable | Object name. |
| `Result` | `varchar(128)` | required | `Pending`, `Skipped`, `Succeeded`, `Failed`, `Error`, `Blocked`, or `Rejected`. |
| `Started datetime` | `datetime2(6)` | nullable | Work start. |
| `Completed datetime` | `datetime2(6)` | nullable | Work settlement. |
| `Duration milliseconds` | `bigint` | nullable | Elapsed milliseconds. |
| `Message` | `varchar(4000)` | nullable | Human-readable task summary. |
| `Details` | `varchar(4000)` | nullable | Task-specific structured detail serialized as JSON. |

### `_.Bookmark`

UTC instant immediately before each loadable object's latest clean load began. Views have no bookmark row.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Bookmark datetime` | `datetime2(6)` | required | UTC cursor instant, or `1900-01-01 00:00:00.000000` before a clean load. |

### `_.LoadStatus`

Current load state for each managed Table, Folder, and View.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Workflow ID` | `varchar(128)` | nullable | Workflow that produced this state; joins operationally to `_.Log`. |
| `Result` | `varchar(128)` | required | `Pending`, `Skipped`, `Succeeded`, `Failed`, `Error`, `Blocked`, or `Rejected`. |
| `Started datetime` | `datetime2(6)` | nullable | Load start. |
| `Completed datetime` | `datetime2(6)` | nullable | Load settlement. |
| `Duration milliseconds` | `bigint` | nullable | Elapsed milliseconds. |

### `_.LoadStatistic`

Append-only counts for each load. Rebuild does not delete this history.

**Key:** `Load statistic SK`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Load statistic SK` | `varchar(128)` | required | Immutable writer-generated surrogate. |
| `Workflow ID` | `varchar(128)` | required | Correlates rows produced by one workflow. |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Object schema. |
| `Object name` | `varchar(128)` | required | Object name. |
| `Started datetime` | `datetime2(6)` | nullable | Load start. |
| `Completed datetime` | `datetime2(6)` | nullable | Load settlement. |
| `Duration milliseconds` | `bigint` | nullable | Elapsed milliseconds. |
| `Rows read` | `bigint` | nullable | Rows produced by the source. |
| `Rows inserted` | `bigint` | nullable | Rows added to the target. |
| `Rows updated` | `bigint` | nullable | Target rows changed. |
| `Rows deleted` | `bigint` | nullable | Target rows removed. |
| `Rows rejected` | `bigint` | nullable | Incoming rows refused and retained in the reject table. |
| `Is reload` | `bit` | nullable | Whether the load reread an already-read window. |
| `Is static skip` | `bit` | nullable | Whether a Static object was skipped after a clean load for this incarnation. |

### `_.TestStatus`

Current result of each Test and Assumption.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical item type. |
| `Item name` | `varchar(128)` | required | Logical item name. |
| `Schema name` | `varchar(128)` | required | Validation schema. |
| `Object name` | `varchar(128)` | required | Validation name. |
| `Test type` | `varchar(128)` | nullable | `Test` or `Assumption`. |
| `Workflow ID` | `varchar(128)` | nullable | Workflow that produced this state; joins operationally to `_.Log`. |
| `Result` | `varchar(128)` | required | `Pending`, `Skipped`, `Succeeded`, `Failed`, `Error`, or `Blocked`. |
| `Started datetime` | `datetime2(6)` | nullable | Validation start. |
| `Completed datetime` | `datetime2(6)` | nullable | Validation settlement. |
| `Duration milliseconds` | `bigint` | nullable | Elapsed milliseconds. |
| `Failure count` | `bigint` | nullable | Test discrepancies or contradicting Assumption rows; set only when evaluated. |

## Borrowed-state table

### `_.Mirror`

`_.Mirror` records installed objects whose data comes from another target. It is created on the first borrowed-state write rather than by the built-in catalogue documents, so it may be absent in a catalogue that has never held mirrored state. It is still protected and part of the current readable catalogue surface when present.

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Local logical item type. |
| `Item name` | `varchar(128)` | required | Local logical item name. |
| `Schema name` | `varchar(128)` | required | Local object schema. |
| `Object name` | `varchar(128)` | required | Local object name. |
| `Source workspace name` | `varchar(128)` | required | Workspace from which data is read. |
| `Source target name` | `varchar(128)` | required | Physical source item. |
| `Source schema name` | `varchar(128)` | required | Source schema. |
| `Source object name` | `varchar(128)` | required | Source object. |
| `Physical type` | `varchar(128)` | required | Local physical form: a Warehouse View or Lakehouse Table/Folder shortcut; current vocabulary also contains the general object-type values. |

Weaver removes a Mirror row when that object is built locally.

## Standard item surface

For each installed Warehouse, Weaver projects `_.Installation`, `_.Log`, `_.Bookmark`, `_.LoadStatus`, `_.LoadStatistic`, and `_.TestStatus` as catalogue views. For each installed Lakehouse, it exposes the same standard surface through OneLake shortcuts. The catalogue Warehouse remains the owner of these records; the per-item surface is for inspection and runtime access, not an independent writable copy.
