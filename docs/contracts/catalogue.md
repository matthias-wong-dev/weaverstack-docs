# Catalogue contract

The Weaver catalogue is the installed record of a Weaver estate. It lives in the configured catalogue Warehouse and owns the `_` schema there. Weaver does not claim ownership of neighbouring schemas or their objects, even when the catalogue shares a Warehouse with application data.

Project source describes the intended estate. The catalogue describes the generation Build installed, its physical bindings and the operational state later recorded by Load and Test. Editing source alone does not alter the catalogue.

## Publication scope and ownership

Catalogue rows are scoped by logical item type and name. A Build reads and reconciles the rows for the items it selects; rows for unselected items are outside its write boundary. A selected item remains bound even when its successful Build certifies no objects.

Build owns publication of installed declarations, item bindings and certifications. Load and Test own their runtime results. Mirror and wipe perform their documented catalogue transitions. The `_` tables are public for read-only inspection, but direct inserts, updates and deletes are not a supported extension point.

A successful catalogue write is part of the operation that reports it. Load and Test do not report successful completion before their required catalogue writes have become durable. A Build publishes only the selected state it installed; it does not certify an omitted or unmaterialised object.

## Public `_` tables

The table names below form the public inspection surface. Their behavioural meanings are:

| Table | Recorded state |
| --- | --- |
| `_.Installation` | The physical target bound to each logical item and the Build that reconciled that binding. |
| `_.Registry` | Objects certified as installed, including their logical identity, physical form, role and installed signature. |
| `_.SchemaDictionary` | Installed schema declarations and descriptions. |
| `_.TableDictionary` | Installed Table and View declarations, including load-related metadata. |
| `_.FolderDictionary` | Installed Folder declarations and managed file scope. |
| `_.ColumnDictionary` | Authored column descriptions and Weaver-managed surrogate-column metadata; not a complete physical-column inventory. |
| `_.KeyDictionary` | Declared primary and unique keys as logical metadata, not physical database constraints or indexes. |
| `_.ForeignKeyDictionary` | Declared relationships as logical metadata, including cross-item relationships; not physical database constraints. |
| `_.TestDictionary` | Installed Test and Assumption declarations, not their latest outcomes. |
| `_.Dependency` | Installed dependency references and their resolved managed producers, where one exists. |
| `_.Shortcut` | Installed logical and physical Shortcut declarations. |
| `_.Bookmark` | The current incremental boundary for a loadable installed object. |
| `_.LoadStatus` | The current Load state of an installed data object. |
| `_.TestStatus` | The current Test or Assumption state. |
| `_.Log` | Append-only records of settled Weaver work. |
| `_.LoadStatistic` | Append-only measurements for completed Load work. |
| `_.Mirror` | Borrowed installed objects and the source and destination physical forms used for them. |

`_.Bookmark`, `_.LoadStatus` and `_.TestStatus` describe the current installed generation. Rebuilding the corresponding loadable object or validation resets the applicable current state; state for objects outside the rebuild remains unchanged. `_.Log` and `_.LoadStatistic` are history and survive a rebuild.

## Binding and certification

`_.Installation` binds logical item identity to a physical target. Object and state rows use logical identity; interpret them through that binding rather than treating a physical target name as their owner.

`_.Registry` is the installation certification boundary. A physical object without a matching certification is not installed merely because it exists. A certification is valid only with its item binding and expected physical inventory. If physical reconciliation disproves a certification, Build removes that installed claim and handles the object according to the selected declaration and physical reconciliation rules.

Shortcut certification depends on the destination item binding because the same logical Shortcut can have different physical forms in a Lakehouse and a Warehouse. An unbound item is not published by guessing that form.

## Mirrored state

A mirror is not the same as a local installation. The destination catalogue carries copied installed declarations and current state, while `_.Mirror` marks objects whose data is still borrowed from the source estate. `_.Registry` continues to describe the installed logical object; a matching `_.Mirror` row supplies its borrowed physical form and source.

A destination can contain both borrowed and local objects. An unchanged borrowed object remains borrowed. When a selected changed object or selected affected descendant is installed locally, its mirror record no longer describes the resulting state. Operational history remains in the catalogue where the work occurred; it is not copied as destination history.

## Read and compatibility boundary

Read-only SQL over `_` is supported for inspection and reporting. Application writes, triggers, replacement procedures and code that depends on Weaver's internal publication sequence are not supported.

Weaver validates catalogue shape and the stored values it must understand before using them. A missing catalogue is a bootstrap case. An incomplete catalogue or one missing required state is rejected when Weaver cannot reconcile it without risking other installations. Weaver can introduce specifically supported newer tables during Build, but this is not a general promise that every older or newer catalogue is automatically migrated.

This contract defines table purpose, ownership, scoping and state transitions. It does not freeze every column, key, data type, stored vocabulary, schema version, transport representation or generated statement. Use the Weaver version that created an incompatible catalogue, or rebuild or repair it with authority over every affected installation.

## Defined behaviour

The Catalogue contract specifies that Weaver:

1. owns only `_` in the configured catalogue Warehouse;
2. separates authored source from installed and runtime state;
3. scopes Build reads and writes to selected logical items;
4. publishes bindings separately from object certification;
5. certifies only installed objects and reconciles certification against physical inventory;
6. resets applicable current state when its installed generation is rebuilt while retaining history;
7. distinguishes borrowed mirror state from local installed state;
8. supports read-only inspection, not direct catalogue mutation; and
9. rejects catalogue state it cannot interpret or reconcile within the requested authority.
