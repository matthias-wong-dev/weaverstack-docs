# Weaver catalogue

The Weaver catalogue is a configured Fabric Warehouse that records the installed estate and its operational state. Its tables live in the `_` schema. [Weaver operations](weaver-operations.md) explains how Build publishes installed state, Load and Test update runtime state, and Health reads both.

Project source and catalogue state answer different questions:

- project source declares what should exist;
- workspace configuration says where logical items should be installed;
- the catalogue records what Build installed and what later operations did.

A change to a Weaver document does not change catalogue state until a successful Build includes that logical item. Load and Test use the installed definitions recorded by Build rather than reopening the project source.

## How to read the `_` schema

Most catalogue rows are scoped by logical item type and name. Object-level tables add schema and object identity. `_.Installation` connects that logical scope to a physical Fabric target.

The tables fall into four groups:

1. installed and declaration state, reconciled by Build;
2. current operational state for the installed generation;
3. append-only operational history;
4. borrowed state created by a mirror.

The tour below explains what each table means and when it is useful to inspect. Exact columns, keys, stored vocabularies and compatibility rules belong in [Reference](../reference/index.md).

## Installed and declaration state

Build reconciles these tables from the selected project declarations. Rows for logical items outside the Build selection remain outside that reconciliation.

| Table | What it records | Inspect it when |
| --- | --- | --- |
| `_.Installation` | Each logical item's physical target, the Weaver version that last reconciled it and the item declaration signature. | You need to confirm where a logical item is installed or which installation a catalogue row belongs to. |
| `_.Registry` | Objects certified as installed, including their physical kind, role, source signature and Build time. Certification is published after the object and its dependencies have succeeded. | You need to distinguish installed objects from unrelated objects in the same Fabric item, or compare an installed signature with project source. |
| `_.SchemaDictionary` | Declared schemas and their authored descriptions. | You need the installed schema-level documentation for an item. |
| `_.TableDictionary` | Declared Tables and Views, including descriptions, lineage, keys used by loading, nullability metadata and load behaviour. It describes Weaver documents rather than inventorying arbitrary physical relations. | You need to understand the installed declaration for a Table or View. |
| `_.FolderDictionary` | Managed Folders, their lineage and load behaviour, and the file patterns that bound Weaver's management of their contents. | You need to inspect a Folder's installed load contract or managed file scope. |
| `_.ColumnDictionary` | Authored column descriptions and Weaver-managed surrogate columns. It is not a complete physical-column inventory. | You need installed column documentation or need to identify a managed identity column. |
| `_.KeyDictionary` | Declared primary and unique keys. These are logical metadata; the catalogue does not imply that Weaver built database indexes or constraints for them. | You need to see the keys used to identify rows or describe uniqueness. |
| `_.ForeignKeyDictionary` | Declared relationships between column sets, including relationships across logical items. These are relationship metadata, not database constraints. | You need to inspect installed relationship metadata or trace a cross-item relationship. |
| `_.TestDictionary` | Declared Tests and Assumptions, their descriptions and a Test's correlation key. It describes validations, not their latest outcomes. | You need to see which validations Build installed or distinguish a Test from an Assumption. |
| `_.Dependency` | Authored dependency references and the logical object identities to which they resolved. | You need to explain Build impact or the ordering of installed Load and Test work. |
| `_.Shortcut` | Declared cross-item, cross-engine and cross-workspace edges, including their logical or physical targets. | You need to trace how one installed item reaches an object owned elsewhere. |

`_.Registry` is the certification boundary. A physical object can exist without a Registry row, and a Registry row is meaningful only in the context of its `_.Installation` binding. Health can compare these claims with physical inventory; Build compares them with project declarations and the selected targets.

## Current operational state

Current-state rows describe the present installed generation. Rebuilding the corresponding object invalidates or resets that state.

| Table | What it records | Inspect it when |
| --- | --- | --- |
| `_.Bookmark` | The UTC instant immediately before a loadable object's latest clean load began. A rebuild or reload resets the bookmark; Views have no bookmark row. | You need to explain the next incremental read boundary or whether an object has completed a clean load. |
| `_.LoadStatus` | The current Load result and timing for each managed Table, Folder and View, with the workflow that produced it. Rebuilt loadable objects return to Pending; built Views start Succeeded. | You need the current Load outcome used by Health. |
| `_.TestStatus` | The current result, timing and failure count for each installed Test and Assumption, with the workflow that produced it. Rebuilding a validation sets it to Pending. | You need the current validation outcome used by Health. |

These tables are keyed by logical object identity rather than by a physical target name. `_.Installation` supplies the target binding. The workflow identifier connects a current result with its supporting entries in `_.Log` and, for loads, `_.LoadStatistic`.

## Operational history

History records what happened. Rebuilding an object does not remove it.

| Table | What it records | Inspect it when |
| --- | --- | --- |
| `_.Log` | One appended row for each settled unit of Weaver work, with workflow identity, target, result, timing, message and task-specific detail. | You need to reconstruct a run, correlate work from one workflow or investigate a failure. |
| `_.LoadStatistic` | Append-only counts and timing for each Load, including rows read, inserted, updated, deleted and rejected, plus reload and static-skip indicators. | You need the activity behind a Load outcome or a historical record of data movement. |

`_.LoadStatus` answers “what is the current result?” while `_.LoadStatistic` answers “what did that Load move?”. A blocked Load can have current status without a statistic because no data work ran.

## Mirrored and borrowed state

Mirror is an estate transition. It creates a development catalogue whose installed state starts from another catalogue, rebinds selected logical items to development targets and records which relations still read from the source estate.

| Table | What it records | Inspect it when |
| --- | --- | --- |
| `_.Mirror` | Installed objects whose data is still borrowed: the source workspace and object, and the physical form at the destination address. A Warehouse relation is a local View. A Lakehouse Table or Folder is a shortcut, while a source View is exposed through a local wrapper View. | You need to distinguish borrowed data from locally materialised data, find the source relation or explain the physical type Build and Health should expect. |

`_.Mirror` is created when borrowed state is first recorded; an estate that has never borrowed an object need not contain the table. The resulting catalogue can describe a mixed estate. `_.Installation` binds each logical item to its destination target. `_.Registry` retains the installed logical type, role and signature. A matching `_.Mirror` row overrides the expected physical form and names the source; no matching row means the Registry object is local.

The destination starts with copied declaration and current-state rows. `_.Log` and `_.LoadStatistic` remain in the catalogue where the work happened. For an object still in `_.Mirror`, Health reads current Load state from the configured source catalogue; for a local object, it reads destination state.

Build compares Registry signatures with the selected project documents. A changed borrowed object and affected descendants selected by Build are installed locally. After the physical work, Build removes their `_.Mirror` rows before publishing the resulting catalogue state. Unchanged objects keep their borrowed forms and rows.

## Inspect, but do not write

The `_` schema is a queryable public surface, not a write extension point. Do not insert, update or delete catalogue rows by hand. Manual writes can separate logical identity from its target, certify an object that Build did not install, alter dependency ordering or detach a result from the workflow that produced it.

Use Build, Load, Test, mirror and wipe as writers. Use Health, command output and read-only queries for inspection. Generated procedures and Weaver's internal write order are implementation details rather than additional catalogue contracts. The [Catalogue contract](../contracts/catalogue.md) defines publication and certification boundaries; the [Catalogue schema reference](../reference/catalogue-schema.md) records the current columns and keys without promising compatibility. The [Load contract](../contracts/load.md) defines Load's execution and recording boundary.
