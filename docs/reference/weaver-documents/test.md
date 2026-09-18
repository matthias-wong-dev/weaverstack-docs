# Test

A Test compares an expected relation with an actual relation. It passes when their two-way set difference is empty. An optional primary key correlates diagnostic rows; it does not change the comparison.

## Location and identity

| Item | Location | Filename | Authored form |
| --- | --- | --- | --- |
| Lakehouse | `Lakehouse/<Item>/tests/` | `Schema__Object.py` | Python |
| Lakehouse | `Lakehouse/<Item>/tests/` | `Schema.Object.sql` | Spark SQL |
| Warehouse | `Warehouse/<Item>/tests/` | `Schema.Object.sql` | T-SQL |

The file must sit directly under `tests/`. `Test ID: Schema.Object`, filename and Python class name must agree exactly, including case. Each identity component is one logical name: no forward slash, backslash, dot, colon or surrounding whitespace. A Test and Assumption share one validation namespace. In a Warehouse that namespace also collides with Tables and Views of the same `Schema.Object`; a Lakehouse validation identity has no `Tables/` area and may share a local name with a Table.

## Metadata

| Key | Required | Value and default |
| --- | --- | --- |
| `Test ID` | Yes | One non-empty `Schema.Object`; the file contains no other ID key. |
| `Description` | Yes | Non-empty prose or one metadata reference. |
| `Primary key` | No | One comma-separated, ordered column set. Default: no correlation key. |
| `Dependencies` | No | YAML list of item-relative `Schema.Object` names. Absent: infer; present: replace inference; `[]`: none. |
| `Notes` | No | Non-empty free text. |
| `Revision notes` | No | Non-empty YAML list of dated notes using one accepted date spelling throughout the document; see [Common metadata](common-metadata.md). |

Only these keys are accepted. `Lineage`, `Schema`, `Column notes`, `Unique keys`, `Foreign keys`, `Not null`, `Identity`, `Comparison columns`, `Incremental`, `Static`, `Prohibit rebuild`, `File key`, `Has load procedure`, `Delete percentage threshold`, `Update percentage threshold` and `Stability row threshold` are incompatible with a Test.

`Primary key` columns must be returned by both sides. At runtime each key must be non-null, non-blank and unique on each side. `_weaver_side` and `_weaver_sk` are reserved diagnostic column names and must not be returned by either side.

Dependencies are inferred from Python object imports or SQL relation references when `Dependencies` is absent. This includes Spark SQL Tests; the explicit-dependency requirement for Spark SQL Tables and Views does not apply to validations. Declared dependencies replace inferred references and cannot name the Test itself or another Test or Assumption. Item graphs remain acyclic.

## Python body

The module declares exactly one Weaver class directly inheriting `weaver.Test`. Its name equals the filename stem. It implements one synchronous `expected()` and one synchronous `actual()` method and must not override `read()`.

Both methods return Spark DataFrames with the same number of positionally compatible columns. If both sides use the same column names, they must use the same order; Weaver refuses a reordered copy of the same names rather than silently changing comparison semantics. A declared primary key must exist on both sides and only pairs expected and actual diagnostic rows for the same entity.

```python
"""
Test ID: Parcel.CountsMatch

Description: Expected and actual parcel counts match.

Primary key: Depot
"""

from weaver import Test


class Parcel__CountsMatch(Test):
    def expected(self):
        return self.spark.createDataFrame([("CBR", 2)], "Depot string, Count long")

    def actual(self):
        return self.spark.createDataFrame([("CBR", 2)], "Depot string, Count long")
```

Path: `Lakehouse/Quality/tests/Parcel__CountsMatch.py`.

## SQL body

Setup statements that return no rows may precede the contract queries. All setup must finish before the first result-producing query. The body then produces exactly two result sets:

1. expected rows;
2. actual rows.

Both result sets obey the same shape and optional primary-key rules as Python Tests.

Spark SQL example:

```sql
/*
Test ID: Parcel.CountsMatch

Description: Expected and actual parcel counts match.

Primary key: Depot
*/
select 'CBR' as Depot, 2 as Count;

select 'CBR' as Depot, 2 as Count;
```

Path: `Lakehouse/Quality/tests/Parcel.CountsMatch.sql`.

Warehouse T-SQL example:

```sql
/*
Test ID: Parcel.CountsMatch

Description: Expected and actual parcel counts match.

Primary key: Depot
*/
select cast('CBR' as varchar(20)) as Depot, cast(2 as bigint) as Count;

select cast('CBR' as varchar(20)) as Depot, cast(2 as bigint) as Count;
```

Path: `Warehouse/Quality/tests/Parcel.CountsMatch.sql`.

## Operations and managed state

- **Check** parses metadata, identity, class/method structure, SQL program shape, dependencies and cycles without running the Test.
- **Build** installs the declaration and its runnable form. Lakehouse Python is deployed as a module; Lakehouse Spark SQL is compiled to a module; Warehouse T-SQL is compiled to a stored procedure. Build does not evaluate the Test. A rebuilt Test receives current status `Pending`.
- **Load** does not run Tests.
- **Test** runs the installed definition after its data dependencies and records `Succeeded`, `Failed`, `Error` or `Blocked`. Missing and unexpected counts form the failure count. Diagnostic rows are returned to an interactive caller when requested but are not persisted.

`_.TestDictionary` records the logical item, `Schema.Object`, test type, resolved description and its reference, optional primary key and source signature. `_.Registry` records the compiled module or procedure with role `Test`, not a physical object at the logical Test ID. `_.Dependency` records resolved edges. `_.TestStatus` records the logical identity, test type, workflow, result, timing and current failure count; `_.Log` keeps execution history.
