# Weaver catalogue

The Weaver catalogue is a configured Fabric Warehouse that records the installed estate and its operational state. Its tables live in the `_` schema.

Project source, workspace configuration and catalogue state answer different questions:

- project source declares what should exist;
- workspace configuration says where Build should install logical items;
- the catalogue records what Build installed and what Load and Test did afterwards.

Load, Test and Health use catalogue state rather than interpreting the project again. A source edit therefore does not affect those operations until a successful Build installs it.

## How to read the `_` schema

Catalogue rows use logical item identity so state remains attached to project concepts even when physical target names differ. `_.Installation` connects each logical item to its physical target.

The tables answer four groups of questions:

1. What did Build install and declare?
2. What is the current operational state?
3. What happened in earlier operations?
4. Which installed objects still borrow data from another estate?

The tour below covers every catalogue table. See [Catalogue schema reference](../reference/catalogue-schema.md) for exact columns, keys, types and stored values.

## Installed and declaration state

Build reconciles these tables for the logical items it installs.

| Table | What it tells you | Inspect it when |
| --- | --- | --- |
| `_.Installation` | Which physical Fabric target holds each logical item and which item declaration is installed there. | You need to connect logical catalogue rows to a physical target. |
| `_.Registry` | Which objects Build certified as installed, their physical kind and their role in the estate. | You need to separate Weaver-installed objects from unrelated objects or see whether source differs from the installed generation. |
| `_.SchemaDictionary` | Which schemas the installed declarations use and how those schemas are described. | You need installed schema-level documentation. |
| `_.TableDictionary` | The installed declarations for Tables and Views, including their descriptive, key and load metadata. | You need to understand what an installed Table or View is meant to represent or how it loads. |
| `_.FolderDictionary` | The installed declarations for managed Folders and the file scope each declaration owns. | You need to understand a Folder's purpose or managed file boundary. |
| `_.ColumnDictionary` | Authored column descriptions and Weaver-managed surrogate columns. It is not a physical column inventory. | You need installed column documentation or need to identify a managed identity column. |
| `_.KeyDictionary` | Declared primary and unique keys as logical metadata. | You need to understand how rows are identified; the rows do not imply physical indexes or constraints. |
| `_.ForeignKeyDictionary` | Declared relationships between column sets, including cross-item relationships. | You need to trace relationship metadata; the rows do not imply database constraints. |
| `_.TestDictionary` | Which Tests and Assumptions Build installed and the descriptive metadata for each. | You need to inventory validations or distinguish their kinds. |
| `_.Dependency` | Authored dependency references and the logical objects to which Weaver resolved them. | You need to explain Build impact or Load and Test ordering. |
| `_.Shortcut` | Installed logical and physical Shortcut declarations and their targets. | You need to trace how an item presents data owned elsewhere. |

`_.Registry` is the certification boundary: a physical object may exist without being part of the installed estate. Interpret a Registry row together with its `_.Installation` binding.

## Current operational state

These tables answer what is true for the current installed incarnation of an object. Rebuilding that object resets or replaces the applicable current state.

| Table | What it tells you | Inspect it when |
| --- | --- | --- |
| `_.Bookmark` | The incremental read boundary established by a loadable object's latest clean Load. | You need to understand where the next incremental read begins or whether a clean Load has completed. |
| `_.LoadStatus` | The current Load outcome for each managed Table, Folder and View. | You need the Load state used by Health. |
| `_.TestStatus` | The current outcome and finding count for each installed Test and Assumption. | You need the validation state used by Health. |

A rebuilt loadable object or validation begins with fresh current state for its new installed incarnation. These tables answer “what is the result now?”, not “what has ever happened?”.

## Operational history

History remains after an object is rebuilt.

| Table | What it tells you | Inspect it when |
| --- | --- | --- |
| `_.Log` | A history of settled Weaver work, correlated by workflow. | You need to reconstruct a run or investigate a failed or blocked unit of work. |
| `_.LoadStatistic` | The row counts and timing recorded for each Load. | You need to understand what a Load moved or compare activity across runs. |

`_.LoadStatus` gives the current outcome. `_.LoadStatistic` gives the activity for a particular Load. A blocked Load can have current status without a load statistic because no data work ran.

## Mirrored and borrowed state

Mirror establishes a development catalogue from another installed estate. Selected data can remain borrowed while changed objects are built locally.

| Table | What it tells you | Inspect it when |
| --- | --- | --- |
| `_.Mirror` | Which installed objects still borrow data, where that data comes from and what presents it at the development target. | You need to distinguish borrowed objects from locally materialised objects or trace borrowed data to its source. |

`_.Mirror` is created when borrowed state is first recorded, so an estate that has never borrowed data may not contain it. A development catalogue can describe a mixed estate: a Registry object with a corresponding Mirror row is borrowed; an installed object without one is local. Building a changed borrowed object locally removes its borrowed-state row after the installation succeeds.

Current Load state for borrowed data remains with the source estate; work performed locally is recorded in the development catalogue. [Mirrors](mirrors.md) explains the user model.

## Inspect the catalogue; change it through Weaver

Query the `_` schema to inspect an estate, but do not edit catalogue rows by hand. Use Build, Load, Test, Mirror and Wipe for state changes. Manual writes can detach recorded state from the installed objects and bindings it describes.

Use Health and command reports for normal operation, and read-only catalogue queries when you need more detail. Exact publication boundaries and schema definitions are in [Catalogue schema reference](../reference/catalogue-schema.md).
