# Table

A Table materialises rows in a Lakehouse Delta table or Warehouse table. Shared source-header, identity and metadata rules are in [Common metadata](common-metadata.md).

## Location and authored form

| Target | Location | Form |
| --- | --- | --- |
| Lakehouse | `Lakehouse/<Item>/Tables/<Schema>__<Object>.py` | Python class inheriting `Table` |
| Lakehouse | `Lakehouse/<Item>/Tables/<Schema>.<Object>.sql` | Spark SQL program |
| Warehouse | `Warehouse/<Item>/<Schema>.<Object>.sql` | T-SQL program |

`Table ID: Schema.Object`, the filename and, for Python, class `Schema__Object` must agree exactly. A Python Table implements one synchronous `read()` method. Do not author a `SparkSqlTable` subclass; Build generates that runtime class from a Spark SQL document. Runtime constructors and helper signatures are in [Python authored objects](../python/objects.md).

## Metadata

A Table accepts the [shared keys](common-metadata.md#shared-metadata-keys) plus every key below.

| Key | Required | Accepted value | Default and effect |
| --- | --- | --- | --- |
| `Table ID` | Yes | `Schema.Object` | No default. |
| `Schema` | Python only | Non-empty mapping of exact-case column name to non-empty target-engine type text | Required for Python; optional for Spark SQL and T-SQL. Authored order is preserved. |
| `Column notes` | No | Non-empty mapping of column name to prose or one metadata reference | Empty. Names must match the declared or built business shape exactly. |
| `Primary key` | Conditional | One comma-separated, ordered, non-empty column set | Empty. Required when `Incremental: true`. Key columns are implicitly not null. |
| `Unique keys` | No | Non-empty YAML list; each entry is one comma-separated, ordered column set | Empty. Entries and columns cannot repeat; an entry cannot equal the primary key. |
| `Foreign keys` | No | Non-empty YAML list of `child columns: target[parent columns]` mappings | Empty. `target` is `Schema.Object`, `Files/Schema.Object` or an item-qualified logical identity, without `$`. Child and parent sets must have equal length. Relationships are logical metadata, not dependencies or physical constraints. |
| `Not null` | No | YAML list of distinct column names | Empty. Do not repeat primary-key columns. |
| `Identity` | No | One column name | Absent. Adds a Weaver-managed, engine-generated, not-null `bigint` surrogate outside `Schema` and query output. |
| `Comparison columns` | No | One comma-separated, ordered column set | Every non-key business column. With an inferred SQL shape, the runtime derives that default from the built target. Requires a primary key and cannot include key columns. |
| `Incremental` | No | Boolean | `false`. `true` requires a primary key. |
| `Has load procedure` | No | Boolean | `true`. `false` is accepted only for Spark SQL and T-SQL Tables; Weaver installs structure but no generated load or row-signature column. |
| `Delete percentage threshold` | No | Whole integer from `0` through `100` | `5`. |
| `Update percentage threshold` | No | Whole integer from `0` through `100` | `20`. |
| `Stability row threshold` | No | Whole integer of at least `0` | `1000000`. |

A `Schema` declaration is authoritative. A SQL query must return every declared business column, no extra business column and the exact declared spelling; query order may differ. Without `Schema`, Spark SQL and T-SQL take business names and types from the staging query during Build. Key, nullability, comparison and note references are then checked against that inferred shape with exact case. Type strings are passed to the target representation; Check does not establish that the engine accepts them. A business column is nullable unless it is in `Primary key` or `Not null`.

Primary, unique and foreign column sets preserve declaration order. Unique-key declaration order also controls the order in which Load rejects incoming duplicates.

The stability percentages are strict upper bounds checked before writes on keyed targets at or above `Stability row threshold`. They do not apply to empty targets or unkeyed wholesale replacement. A value of `100` disables that percentage gate. A load invocation may explicitly waive both gates; see [Python authored objects](../python/objects.md) and [Load](../operation-behaviour/load.md).

### Incompatible combinations

- `Incremental: true` without `Primary key`.
- `Comparison columns` without a primary key, or containing a primary-key column.
- A `Not null` entry that repeats a primary-key column.
- An `Identity` that appears in `Schema`, is the primary key, appears in the query result, or collides with a Weaver-managed audit or signature name.
- An authored business column colliding case-insensitively with a managed audit or signature name.
- `Has load procedure: false` on a Python Table.
- A non-incremental body or Python return that supplies explicit deletes.

When `Schema` is declared, all locally named columns in keys, `Not null`, `Comparison columns` and `Column notes` must exist. With an inferred SQL shape, Build performs the same check. Duplicate or case-only query columns are invalid.

## Body and return contract

### Python

`read()` returns a Spark DataFrame containing the business columns.

- Non-incremental: return the staging DataFrame. A tuple or `None` is invalid; an empty snapshot is an empty DataFrame.
- Incremental: return the staging DataFrame, `(staging, delete_keys)`, `None` for no work, or `(None, delete_keys)` for deletion-only work. `delete_keys` is a DataFrame containing the primary-key columns.

Incremental omission does not delete a target row; only explicit delete keys do. A non-incremental keyed load treats absent source rows as deleted. An unkeyed Table replaces the target wholesale.

### Spark SQL

Every statement, including the final one, ends with `;`. Setup statements may precede result queries. The first result query supplies staging rows. An optional second result query supplies delete keys and therefore requires `Incremental: true` and a primary key. Zero result queries or more than two are invalid.

### T-SQL

Setup may precede the top-level result query; semicolons are optional. The first top-level `SELECT` supplies staging rows. An optional second supplies delete keys and therefore requires `Incremental: true` and a primary key. Zero visible result queries or more than two are invalid. `GO` is not accepted. If dynamic SQL prevents static result analysis, the Warehouse endpoint remains the authority when Build or Load executes the generated work.

## Complete examples

Python, `Lakehouse/Logistics/Tables/Parcel__Current.py`:

```python
"""
Table ID: Parcel.Current

Description: Current state of each parcel.

Lineage: Parcel event stream.

Primary key: parcel_id

Schema:
  parcel_id: string
  status: string
"""

from weaver import Table


class Parcel__Current(Table):
    def read(self):
        return self.spark.createDataFrame([], "parcel_id string, status string")
```

Spark SQL, `Lakehouse/Logistics/Tables/Parcel.StatusCount.sql`:

```sql
/*
Table ID: Parcel.StatusCount

Description: Parcel count by status.

Lineage: Parcel status feed.

Dependencies: []
*/
select 'in_transit' as status, cast(0 as bigint) as parcel_count;
```

T-SQL, `Warehouse/Reporting/Parcel.StatusCount.sql`:

```sql
/*
Table ID: Parcel.StatusCount

Description: Parcel count by status.

Lineage: Reporting intake.
*/
select cast('in_transit' as varchar(32)) as [status],
       cast(0 as bigint) as [parcel_count];
```

## Build, Load, Test and managed state

Build installs the Table structure and, when enabled, its load definition. It obtains an inferred SQL shape at Build time; it does not call Python `read()`. Load runs the installed definition. Test does not execute a Table, although Tests and Assumptions may read it.

Every Table has three not-null row-audit columns. Delta uses `row_insert_datetime`, `row_update_datetime` and `row_delete_datetime` of type `timestamp`; Warehouse uses spaced names of type `datetime2(6)`. A keyed Table with a load also has a not-null row signature: `row_signature` as `string` in Delta or `Row signature` as `varbinary(32)` in Warehouse. `Identity`, when declared, is a leading managed `bigint`; the audit columns and then row signature follow the business shape. These managed columns are not authored in `Schema` or returned by the source query.

Build records the declaration in `_.TableDictionary`, authored notes and managed identity in `_.ColumnDictionary`, keys in `_.KeyDictionary`, relationships in `_.ForeignKeyDictionary`, dependencies in `_.Dependency`, and installed certification in `_.Registry`. Loadable Tables use current load state and bookmarks and contribute Load history/statistics. See the [catalogue schema](../catalogue-schema.md) for exact columns and [Schemas, keys and managed columns](../../advanced/schemas-keys-and-managed-columns.md) for the processing model.
