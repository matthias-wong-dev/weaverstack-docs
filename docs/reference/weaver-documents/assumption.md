# Assumption

An Assumption returns rows that contradict a statement about the estate. It passes when no rows are returned.

## Location and identity

| Item | Location | Filename | Authored form |
| --- | --- | --- | --- |
| Lakehouse | `Lakehouse/<Item>/assumptions/` | `Schema__Object.py` | Python |
| Lakehouse | `Lakehouse/<Item>/assumptions/` | `Schema.Object.sql` | Spark SQL |
| Warehouse | `Warehouse/<Item>/assumptions/` | `Schema.Object.sql` | T-SQL |

The file must sit directly under `assumptions/`. `Assumption ID: Schema.Object`, filename and Python class name must agree exactly, including case. Each identity component is one logical name: no forward slash, backslash, dot, colon or surrounding whitespace. Tests and Assumptions share one validation namespace. In a Warehouse that namespace also collides with Tables and Views of the same identity; a Lakehouse validation has no `Tables/` area.

## Metadata

| Key | Required | Value and default |
| --- | --- | --- |
| `Assumption ID` | Yes | One non-empty `Schema.Object`; the file contains no other ID key. |
| `Description` | Yes | Non-empty prose or one metadata reference. |
| `Dependencies` | No | YAML list of item-relative `Schema.Object` names. Absent: infer; present: replace inference; `[]`: none. |
| `Notes` | No | Non-empty free text. |
| `Revision notes` | No | Non-empty YAML list of dated notes using one accepted date spelling throughout the document; see [Common metadata](common-metadata.md). |

Only these keys are accepted. `Primary key` is incompatible because an Assumption has no expected/actual pair to correlate. `Lineage`, `Schema`, `Column notes`, `Unique keys`, `Foreign keys`, `Not null`, `Identity`, `Comparison columns`, `Incremental`, `Static`, `Prohibit rebuild`, `File key`, `Has load procedure`, `Delete percentage threshold`, `Update percentage threshold` and `Stability row threshold` are also incompatible.

Dependencies are inferred from Python object imports or SQL relation references when `Dependencies` is absent. Spark SQL Assumptions may use inference; the explicit-dependency requirement for Spark SQL Tables and Views does not apply to validations. A declaration replaces inferred references and cannot name the Assumption itself or any Test or Assumption. Item graphs remain acyclic.

## Python body

The module declares exactly one Weaver class directly inheriting `weaver.Assumption`. Its name equals the filename stem and it implements one synchronous `read()` method. `read()` returns a Spark DataFrame containing the violating rows; any returned row is a failure.

```python
"""
Assumption ID: Parcel.HasDestination

Description: Every parcel has a destination.
"""

from weaver import Assumption


class Parcel__HasDestination(Assumption):
    def read(self):
        return self.spark.createDataFrame([], "ParcelId string, Destination string")
```

Path: `Lakehouse/Quality/assumptions/Parcel__HasDestination.py`.

## SQL body

Setup statements that return no rows may precede the contract query. All setup must finish before the first result-producing query. The body then produces exactly one result set containing violating rows.

Spark SQL example:

```sql
/*
Assumption ID: Parcel.HasDestination

Description: Every parcel has a destination.
*/
select cast(null as string) as ParcelId
where false;
```

Path: `Lakehouse/Quality/assumptions/Parcel.HasDestination.sql`.

Warehouse T-SQL example:

```sql
/*
Assumption ID: Parcel.HasDestination

Description: Every parcel has a destination.
*/
select cast(null as varchar(50)) as ParcelId
where 1 = 0;
```

Path: `Warehouse/Quality/assumptions/Parcel.HasDestination.sql`.

## Operations and managed state

- **Check** parses metadata, identity, class/method structure, SQL program shape, dependencies and cycles without running the Assumption.
- **Build** installs the declaration and its runnable form. Lakehouse Python is deployed as a module; Lakehouse Spark SQL is compiled to a module; Warehouse T-SQL is compiled to a stored procedure. Build does not evaluate it. A rebuilt Assumption receives current status `Pending`.
- **Load** does not run Assumptions.
- **Test** runs the installed definition after its data dependencies. Zero rows records `Succeeded`; returned rows record `Failed`; execution failures record `Error`; unavailable dependencies can record `Blocked`. The violation count is retained, while diagnostic rows are not persisted.

`_.TestDictionary` records the logical item, `Schema.Object`, type `Assumption`, resolved description and its reference, a null primary key and source signature. `_.Registry` records the compiled module or procedure with role `Assumption`, not a physical object at the logical Assumption ID. `_.Dependency` records resolved edges. `_.TestStatus` records the logical identity, test type, workflow, result, timing and current violation count as `Failure count`; `_.Log` keeps execution history.
