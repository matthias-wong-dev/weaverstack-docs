# Catalogue schema

The Weaver catalogue is a set of Warehouse tables in schema `_`. This page records the current physical inspection surface: table names, public column names, keys, nullability, types, and meanings.

It is a read-only integration boundary. Query these tables for inspection and reporting; do not insert, update, delete, truncate, rebuild, or add application-owned objects under `_`. Build and runtime operations own their rows and lifecycle.

The catalogue schema is unversioned: it has no schema-version table or compatibility number. Weaver checks the tables and columns it needs when opening a catalogue and rejects missing or incompatible state.

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

## What to inspect

| Question | Tables |
| --- | --- |
| Which logical items are installed, and where? | `_.Installation`, including resolved `Workspace name`, `Workspace GUID`, `Target name` and `Target item GUID` |
| What is certified and what source contributed it? | `_.Registry`; `Object type` includes Semantic model, Report and Source artifact; `Object role` includes Source |
| What did authored data and validation declare? | Schema/Table/Folder/Column/Key/ForeignKey/Test dictionaries, `_.Dependency` and `_.Shortcut` |
| What did model readback record? | `_.SemanticModel`, `_.SemanticModelTable`, `_.SemanticModelColumn`, `_.SemanticModelMeasure`, `_.SemanticModelRelationship` |
| Which DAX validation definition was installed? | `_.SemanticModelTest`, separate from `_.TestDictionary` and current `_.TestStatus` |
| What has loaded or passed, and where is progress? | `_.Bookmark`, `_.LoadStatus`, `_.TestStatus` |
| What happened over time? | Append-oriented `_.Log` and `_.LoadStatistic`; not the same thing as current state |
| What is borrowed in a Mirror? | Optional `_.Mirror`, created on the first borrowed-state write; no built-in SQL document declares it |

Semantic metadata is projected from deployed readback, not a claim to discover all unmanaged workspace models. Report registrations live in Installation/Registry; there is no separate Report dictionary table. A catalogue-free deployment/refresh or file-mode Test adds no rows here. Signatures are equality tokens for reconciliation, not a public cross-version hash algorithm.

`_.Mirror` records local object identity and physical source/form. It is removed when an object becomes local. Protected mirror materialisation retains data/bookmarks under its specific Build rules; ordinary replacement and Wipe have different boundaries.

The generated inventory includes every physical column, including audit columns. Keys are shown in stored order. Vocabulary spellings are recorded in the checked-in manifest; they do not imply relational constraints or a versioned migration policy.

<!-- BEGIN GENERATED CATALOGUE REFERENCE -->

## Physical table declarations

### `_.Bookmark`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Bookmark datetime` | `datetime2(6)` | required | The UTC instant immediately before the most recent clean load began, or 1900-01-01 00:00:00.000000 for an object that has not had one. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.ColumnDictionary`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`, `Column name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Column name` | `varchar(128)` | required | The column. |
| `Description` | `varchar(4000)` | nullable | What this column is. |
| `Description reference` | `varchar(128)` | nullable | The $Schema.Object this description was copied from, if any. |
| `Is identity` | `bit` | nullable | Whether this is Weaver's managed surrogate column. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.Dependency`

**Key:** `Item type`, `Item name`, `Referencing schema name`, `Referencing object name`, `Dependency reference`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Referencing schema name` | `varchar(128)` | required | The schema of the object declaring the dependency. |
| `Referencing object name` | `varchar(128)` | required | The name of the object declaring the dependency. |
| `Dependency reference` | `varchar(1000)` | required | The dependency exactly as the owning document wrote it. |
| `Referenced item type` | `varchar(128)` | nullable | The referenced item's type, when the edge resolved. |
| `Referenced item name` | `varchar(128)` | nullable | The referenced item's name, when the edge resolved. |
| `Referenced schema name` | `varchar(128)` | nullable | The referenced schema, when the edge resolved. |
| `Referenced object name` | `varchar(128)` | nullable | The referenced object, when the edge resolved. |
| `Signature` | `varchar(128)` | required | Content hash of the owning object's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.FolderDictionary`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Description` | `varchar(4000)` | nullable | What this folder is. |
| `Description reference` | `varchar(128)` | nullable | The $Schema.Object this description was copied from, if any. |
| `Lineage` | `varchar(4000)` | nullable | Where this object's data comes from. |
| `Lineage reference` | `varchar(128)` | nullable | The $Schema.Object the lineage was copied from, if any. |
| `File key` | `varchar(1000)` | nullable | The glob patterns Weaver manages, in declared order. |
| `Is incremental` | `bit` | nullable | Whether load accumulates rows rather than replacing them. |
| `Is static` | `bit` | nullable | Whether the object is loaded once rather than refreshed. |
| `Prohibit rebuild` | `bit` | nullable | Whether build may drop and recreate this object. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.ForeignKeyDictionary`

**Key:** `Item type`, `Item name`, `Foreign schema name`, `Foreign object name`, `Foreign column set`, `Primary item type`, `Primary item name`, `Primary schema name`, `Primary object name`, `Primary column set`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Foreign schema name` | `varchar(128)` | required | The schema of the object declaring the relationship. |
| `Foreign object name` | `varchar(128)` | required | The name of the object declaring the relationship. |
| `Foreign column set` | `varchar(1000)` | required | The foreign columns, comma-separated in declared order. |
| `Primary item type` | `varchar(128)` | required | The primary item's type. |
| `Primary item name` | `varchar(128)` | required | The primary item's name. |
| `Primary schema name` | `varchar(128)` | required | The primary schema. |
| `Primary object name` | `varchar(128)` | required | The primary object. |
| `Primary column set` | `varchar(1000)` | required | The primary columns, paired in order with the foreign ones. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.Installation`

**Key:** `Item type`, `Item name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Workspace name` | `varchar(128)` | required | The resolved Fabric workspace display name. |
| `Workspace GUID` | `varchar(128)` | required | The resolved Fabric workspace GUID. |
| `Target name` | `varchar(128)` | required | The resolved Fabric target display name. |
| `Target item GUID` | `varchar(128)` | required | The resolved Fabric target item GUID. |
| `Weaver version` | `varchar(128)` | required | The Weaver version that last reconciled this installation. |
| `Signature` | `varchar(128)` | required | Content hash of the Item declaration, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.KeyDictionary`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`, `Key type`, `Column set`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Key type` | `varchar(128)` | required | Primary key or Unique. |
| `Column set` | `varchar(1000)` | required | The key's columns, comma-separated in declared order. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.LineageEdge`

**Key:** `Item type`, `Item name`, `Downstream node ID`, `Upstream node ID`, `Edge kind`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Downstream node ID` | `varchar(1000)` | required | The node that reads. |
| `Upstream node ID` | `varchar(1000)` | required | The node read. For an External edge, the reference as its author wrote it. |
| `Edge kind` | `varchar(128)` | required | Dependency, Shortcut, Validation or External. |
| `Through node ID` | `varchar(1000)` | nullable | The shortcut the read passed through, if any. |
| `Downstream node key` | `varchar(12)` | required | The downstream node's key. |
| `Upstream node key` | `varchar(12)` | required | The upstream node's key, or the hash of an External reference. |
| `Through node key` | `varchar(12)` | nullable | The key of the shortcut the read passed through, if any. |
| `Signature` | `varchar(128)` | required | Content hash of the edge's row, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.LineageNode`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Node ID` | `varchar(1000)` | required | The node's installed identity, as LineageEdge names it. |
| `Node key` | `varchar(12)` | required | A short hash of the node ID, as LineageEdge's keys name it. |
| `Node kind` | `varchar(128)` | required | What the node is. |
| `Label` | `varchar(1000)` | required | The node's display name. |
| `Item label` | `varchar(1000)` | required | The node's item, as Type/Name. |
| `Description` | `varchar(4000)` | nullable | The declared description, if any. |
| `Search text` | `varchar(4000)` | required | Label, item and description in lower case, for search. |
| `Is internal` | `bit` | required | Whether the node is part of the Weaver catalogue. |
| `Can load` | `bit` | required | Whether Weaver loads the node in this estate. |
| `Is static` | `bit` | required | Whether the node is loaded once rather than refreshed. |
| `Is mirrored` | `bit` | required | Whether another catalogue's estate supplies the node's data. |
| `Is installed` | `bit` | required | Whether the node's runnable artefact or definition is installed. |
| `Signature` | `varchar(128)` | required | Content hash of the node's row, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.LoadStatistic`

**Key:** `Load statistic SK`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Load statistic SK` | `varchar(128)` | required | An immutable surrogate generated by the writer. Fabric Warehouse tables have no identity columns, and sessions may append concurrently. |
| `Workflow ID` | `varchar(128)` | required | Correlates every row one workflow produced. |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Started datetime` | `datetime2(6)` | nullable | When the load started. |
| `Completed datetime` | `datetime2(6)` | nullable | When the load settled. |
| `Duration milliseconds` | `bigint` | nullable | How long the load took, in milliseconds. |
| `Rows read` | `bigint` | nullable | What the source produced. |
| `Rows inserted` | `bigint` | nullable | Rows the target gained. |
| `Rows updated` | `bigint` | nullable | Rows the target changed. |
| `Rows deleted` | `bigint` | nullable | Rows the target lost. |
| `Rows rejected` | `bigint` | nullable | Incoming rows the load refused, kept in the reject table. |
| `Is reload` | `bit` | nullable | Whether this object was reset for this reload attempt. A failed attempted reload is still marked as a reload. |
| `Is static skip` | `bit` | nullable | Whether a Static object was skipped because a clean load had already run for this incarnation. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.LoadStatus`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Workflow ID` | `varchar(128)` | nullable | The workflow whose load produced this state, so the row can be read alongside the evidence in _.Log. |
| `Result` | `varchar(128)` | required | How the work ended. |
| `Started datetime` | `datetime2(6)` | nullable | When the work started. |
| `Completed datetime` | `datetime2(6)` | nullable | When the work settled. |
| `Duration milliseconds` | `bigint` | nullable | How long the work took, in milliseconds. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.Log`

**Key:** `Log SK`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Log SK` | `varchar(128)` | required | An immutable surrogate generated by the writer. Fabric Warehouse tables have no identity columns, and sessions may append concurrently. |
| `Workflow ID` | `varchar(128)` | required | Correlates every row one workflow produced. A composed run shares one value across its operations. |
| `Task type` | `varchar(128)` | required | The kind of work that settled. |
| `Target type` | `varchar(128)` | nullable | The physical target's type. |
| `Target name` | `varchar(128)` | nullable | The physical target's name. |
| `Schema name` | `varchar(128)` | nullable | The object's schema. |
| `Object name` | `varchar(128)` | nullable | The object's name. |
| `Result` | `varchar(128)` | required | How the work ended. A load may also be Rejected, meaning it completed with rejected rows. |
| `Started datetime` | `datetime2(6)` | nullable | When the work started. |
| `Completed datetime` | `datetime2(6)` | nullable | When the work settled. |
| `Duration milliseconds` | `bigint` | nullable | How long the work took, in milliseconds. |
| `Message` | `varchar(4000)` | nullable | Human-readable task summary. |
| `Details` | `varchar(4000)` | nullable | Structured task-specific detail, as JSON. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.Mirror`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Source workspace name` | `varchar(128)` | required | The workspace the data is read from. |
| `Source target name` | `varchar(128)` | required | The physical item the data is read from. |
| `Source schema name` | `varchar(128)` | required | The schema the data is read from. |
| `Source object name` | `varchar(128)` | required | The object the data is read from. |
| `Physical type` | `varchar(128)` | required | What stands at the local address: a Warehouse View or a Lakehouse Table or Folder shortcut. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.Registry`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Object type` | `varchar(128)` | required | The installed physical type. |
| `Object role` | `varchar(128)` | required | The object's role. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file, so a change can be detected. |
| `Build datetime` | `datetime2(6)` | nullable | When this row was published, shared by every row one completed build wrote. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SchemaDictionary`

**Key:** `Item type`, `Item name`, `Schema name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The schema. |
| `Description` | `varchar(4000)` | nullable | What this schema is. |
| `Description reference` | `varchar(128)` | nullable | The $Schema.Object this description was copied from, if any. |
| `Signature` | `varchar(128)` | required | Content hash of the schema declaration, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SemanticModel`

**Key:** `Item type`, `Item name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Description` | `varchar(max)` | nullable | The native semantic description. |
| `Signature` | `varchar(128)` | required | Content hash of the effective semantic model, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SemanticModelColumn`

**Key:** `Item type`, `Item name`, `Table name`, `Column name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Table name` | `varchar(128)` | required | The owning semantic table. |
| `Column name` | `varchar(128)` | required | The native column name. |
| `Description` | `varchar(max)` | nullable | The native semantic description. |
| `Data type` | `varchar(128)` | nullable | The native semantic data type. |
| `Column type` | `varchar(128)` | nullable | The native column kind. |
| `Source column` | `varchar(128)` | nullable | The source column name. |
| `Expression` | `varchar(max)` | nullable | The calculated column expression. |
| `Signature` | `varchar(128)` | required | Content hash of the effective semantic model, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SemanticModelMeasure`

**Key:** `Item type`, `Item name`, `Table name`, `Measure name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Table name` | `varchar(128)` | required | The measure's home table. |
| `Measure name` | `varchar(128)` | required | The native measure name. |
| `Description` | `varchar(max)` | nullable | The native semantic description. |
| `Expression` | `varchar(max)` | nullable | The DAX expression. |
| `Format string` | `varchar(max)` | nullable | The authored format string. |
| `Signature` | `varchar(128)` | required | Content hash of the effective semantic model, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SemanticModelRelationship`

**Key:** `Item type`, `Item name`, `Relationship name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Relationship name` | `varchar(128)` | required | The native relationship name. |
| `From table` | `varchar(128)` | nullable | The source table. |
| `From column` | `varchar(128)` | nullable | The source column. |
| `To table` | `varchar(128)` | nullable | The destination table. |
| `To column` | `varchar(128)` | nullable | The destination column. |
| `From cardinality` | `varchar(128)` | nullable | The source cardinality. |
| `To cardinality` | `varchar(128)` | nullable | The destination cardinality. |
| `Cross filtering behavior` | `varchar(128)` | nullable | The native cross-filter direction. |
| `Is active` | `bit` | nullable | Whether the relationship is active. |
| `Signature` | `varchar(128)` | required | Content hash of the effective semantic model, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SemanticModelTable`

**Key:** `Item type`, `Item name`, `Table name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Table name` | `varchar(128)` | required | The native table name, matching Dependency's referencing object name. |
| `Table ordinal` | `bigint` | nullable | One-based effective TMDL declaration order. |
| `Description` | `varchar(max)` | nullable | The native semantic description. |
| `Source mode` | `varchar(128)` | nullable | The storage mode of the partition reading the managed source. |
| `Source access` | `varchar(128)` | nullable | How that partition reads the source: sql or lakehouse. |
| `Signature` | `varchar(128)` | required | Content hash of the effective semantic model, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.SemanticModelTest`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Definition` | `varchar(max)` | required | Versioned JSON: the DAX query and, for a Test, its logical Expected source and Expected SQL. |
| `Signature` | `varchar(128)` | required | Content hash of the validation's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.Shortcut`

**Key:** `Item type`, `Item name`, `Shortcut ID`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Shortcut ID` | `varchar(128)` | required | The shortcut as its author declared it: 'Sales.Customer' for a table or folder, 'Reference' for a schema. |
| `Schema name` | `varchar(128)` | required | The schema this item presents the shortcut in. |
| `Object name` | `varchar(128)` | nullable | The object this item presents. Null for a schema shortcut, which presents a namespace rather than an object. |
| `Shortcut type` | `varchar(128)` | required | What the shortcut is. |
| `Target type` | `varchar(128)` | required | Whether the target is a logical item or a physical item. |
| `Target item type` | `varchar(128)` | required | The target's item type. |
| `Target item name` | `varchar(128)` | required | The target's item name. |
| `Target schema name` | `varchar(128)` | required | The schema or path the target sits in. |
| `Target object name` | `varchar(128)` | nullable | The target object. Null for a schema or path. Together, the four target columns preserve a logical producer's identity. |
| `Target workspace name` | `varchar(128)` | nullable | The workspace the target is in. Null for a logical target, which is bound, and for a physical one in this workspace. |
| `Signature` | `varchar(128)` | required | Content hash of the shortcut declaration, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.TableDictionary`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Object type` | `varchar(128)` | required | Table or View. |
| `Description` | `varchar(4000)` | nullable | What this object is. |
| `Description reference` | `varchar(128)` | nullable | The $Schema.Object this description was copied from, if any. |
| `Lineage` | `varchar(4000)` | nullable | Where this object's data comes from. |
| `Lineage reference` | `varchar(128)` | nullable | The $Schema.Object the lineage was copied from, if any. |
| `Primary key` | `varchar(1000)` | nullable | The primary key's columns, in declared order. |
| `Not null columns` | `varchar(1000)` | nullable | Columns declared not null, beyond the primary key. |
| `Identity column` | `varchar(128)` | nullable | Weaver's managed surrogate column, when one is declared. |
| `Comparison columns` | `varchar(max)` | nullable | Columns an author named to drive an upsert. Null where none were named, which is every eligible non-key column. |
| `Is incremental` | `bit` | nullable | Whether load accumulates rows rather than replacing them. |
| `Is static` | `bit` | nullable | Whether the object is loaded once rather than refreshed. |
| `Prohibit rebuild` | `bit` | nullable | Whether build may drop and recreate this object. |
| `Signature` | `varchar(128)` | required | Content hash of the object's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.TestDictionary`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Test type` | `varchar(128)` | required | Test compares an expected relation with an actual one; Assumption returns the rows that contradict it. |
| `Description` | `varchar(4000)` | nullable | What this validation is. |
| `Description reference` | `varchar(128)` | nullable | The $Schema.Object this description was copied from, if any. |
| `Primary key` | `varchar(1000)` | nullable | A Test's correlation key, comma-separated in declared order. Null when undeclared and for every Assumption. |
| `Signature` | `varchar(128)` | required | Content hash of the validation's source file, so a change can be detected. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

### `_.TestStatus`

**Key:** `Item type`, `Item name`, `Schema name`, `Object name`

| Column | Type | Null | Meaning |
| --- | --- | --- | --- |
| `Item type` | `varchar(128)` | required | Logical Weaver item type. |
| `Item name` | `varchar(128)` | required | Logical Weaver item name. |
| `Schema name` | `varchar(128)` | required | The object's schema. |
| `Object name` | `varchar(128)` | required | The object's name. |
| `Test type` | `varchar(128)` | nullable | Test or Assumption. |
| `Workflow ID` | `varchar(128)` | nullable | The workflow whose run produced this state, so the row can be read alongside the evidence in _.Log. |
| `Result` | `varchar(128)` | required | How the work ended. |
| `Started datetime` | `datetime2(6)` | nullable | When the work started. |
| `Completed datetime` | `datetime2(6)` | nullable | When the work settled. |
| `Duration milliseconds` | `bigint` | nullable | How long the work took, in milliseconds. |
| `Failure count` | `bigint` | nullable | Discrepancy rows for a Test or contradicting rows for an Assumption. Set only when evaluated. |
| `Row insert datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row update datetime` | `datetime2(6)` | required | UTC row audit timestamp |
| `Row delete datetime` | `datetime2(6)` | required | UTC row audit timestamp |

<!-- END GENERATED CATALOGUE REFERENCE -->

## Ownership and relationships

The configured catalogue Warehouse owns schema `_`; neighbouring schemas remain application-owned. Project source is desired state. These tables record only the generation Build installed, its bindings and later operation state. Editing source does not change them.

Build reconciles projected rows for selected logical items. It publishes dictionaries and `_.Installation` before certifying installed objects in `_.Registry`; rows for unselected items are outside that Build's write scope. Load owns bookmarks, load status, load statistics and load log entries. Test owns test status and its log entries. Mirror writes borrowed state, and Wipe removes the state in its settled scope.

Keys on this page are Weaver's row-identity rules, not declared Warehouse primary-key or foreign-key constraints. Relationships follow the stored identities:

- the leading `Item type`, `Item name` columns scope projected and object-current rows to a logical item;
- `_.Installation` resolves that item to its current physical target;
- `_.Registry`, the dictionary tables, `_.Bookmark`, `_.LoadStatus`, `_.TestStatus`, and `_.Mirror` identify an object within that item; the applicable object keys align, but no database foreign key enforces the join;
- `_.Dependency` records an authored reference and its resolved producer columns; `_.ForeignKeyDictionary` records a declared relationship; neither creates a physical database constraint;
- `Workflow ID` associates status and statistic rows with operational evidence in `_.Log`; it is an operational join, not a declared key relationship; and
- a matching `_.Mirror` row supplements a `_.Registry` certification with the borrowed source and local physical form.

`_.Bookmark`, `_.LoadStatus`, and `_.TestStatus` are current state for the object as installed. Rebuilding the corresponding loadable object, data node, or validation invalidates that object's applicable rows. `_.Log` and `_.LoadStatistic` are append-only history and are not invalidated by Build. `_.Mirror` is borrowed state: it remains until the object is materialised locally or Mirror replaces the borrowed scope.

A physical object is not installed state without its Registry certification and item binding. Build reconciles those claims against physical inventory. A selected item remains bound even when a successful Build certifies no objects.

A successful operation includes its required catalogue publication. Build certifies only materialised objects; Load and Test settle their required catalogue writes before reporting successful completion. There is no operation-wide rollback of earlier physical or catalogue effects after a later action fails.

## Standard item surface

For each installed Warehouse, Weaver projects `_.Installation`, `_.Log`, `_.Bookmark`, `_.LoadStatus`, `_.LoadStatistic`, and `_.TestStatus` as views. For each installed Lakehouse, it exposes the same tables as OneLake shortcuts. The catalogue Warehouse remains the owner; these per-item objects are inspection and runtime access paths, not writable copies.

## Read and format boundary

Read-only SQL over `_` is the supported inspection path. Direct writes, triggers, replacement procedures, or dependencies on Weaver's statement ordering are not supported.

The catalogue has no schema-version row. Weaver checks the tables, columns, and stored vocabulary needed by an operation. A missing catalogue can be bootstrapped; state that cannot be interpreted or reconciled within the operation's authority is rejected. Some specifically introduced tables can be added by Build, but there is no general migration or cross-version compatibility promise for the inventory documented here.
