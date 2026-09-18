# View

A View installs a SQL query as a Lakehouse or Warehouse view. Shared source-header, identity and metadata rules are in [Common metadata](common-metadata.md).

## Location and authored form

| Target | Location | Dialect |
| --- | --- | --- |
| Lakehouse | `Lakehouse/<Item>/Tables/<Schema>.<Object>.sql` | Spark SQL |
| Warehouse | `Warehouse/<Item>/<Schema>.<Object>.sql` | T-SQL |

`View ID: Schema.Object` and the filename must agree exactly. A View is SQL-only; a Python class inheriting `View` is not a repository authoring form. The public runtime `View` class and `dataframe()` method are documented under [Python authored objects](../python/objects.md).

## Metadata

A View accepts the [shared keys](common-metadata.md#shared-metadata-keys) plus every key below.

| Key | Required | Accepted value | Default and effect |
| --- | --- | --- | --- |
| `View ID` | Yes | `Schema.Object` | No default. |
| `Column notes` | No | Non-empty mapping of result-column name to prose or one metadata reference | Empty. Names are checked against the built result shape. |
| `Primary key` | No | One comma-separated, ordered, non-empty column set | Empty. Logical metadata only. |
| `Unique keys` | No | Non-empty YAML list; each entry is one comma-separated, ordered column set | Empty. Logical metadata only; an entry cannot repeat the primary key or another unique key. |
| `Foreign keys` | No | Non-empty YAML list of `child columns: target[parent columns]` mappings | Empty. `target` is `Schema.Object`, `Files/Schema.Object` or an item-qualified logical identity, without `$`. Logical metadata only; child and parent sets must have equal length. |

A View cannot declare `Schema`, `Not null`, `Identity`, `Comparison columns`, `Incremental`, `Has load procedure` or stability thresholds. It stores no rows and has no Load definition. Its keys and relationships describe the result; they do not create indexes, constraints or dependencies.

Because the result shape is always inferred, Build checks every local column named by `Column notes`, `Primary key`, `Unique keys` and `Foreign keys` against the query result with exact case. Foreign-key parent columns describe the parent and are not checked against the View shape.

`Static` is accepted as shared build metadata and defaults to `false`, but a View has no Load gate for it to control. `Prohibit rebuild: true` is consequential: Build retains an existing protected View instead of replacing it when replacement would otherwise be required.

## SQL body

The body after the opening metadata block is the View query. It must contain one SQL statement and produce one result set where static analysis can determine that count. Do not write `CREATE VIEW`; Build wraps the body in the target-specific create statement. The target engine validates SQL syntax and any behaviour source analysis cannot establish.

Spark SQL Views must explicitly declare `Dependencies`; use `Dependencies: []` for a query with no project dependencies. T-SQL Views may omit the key and use inferred two-part relation references. An explicit declaration replaces inferred dependencies in either dialect.

## Complete examples

Spark SQL, `Lakehouse/Logistics/Tables/Parcel.Active.sql`:

```sql
/*
View ID: Parcel.Active

Description: Parcels still in transit.

Lineage: Parcel status feed.

Dependencies: []
*/
select 'P-001' as parcel_id, 'in_transit' as status;
```

T-SQL, `Warehouse/Reporting/Parcel.Active.sql`:

```sql
/*
View ID: Parcel.Active

Description: Parcels still in transit.

Lineage: Reporting intake.
*/
select cast('P-001' as varchar(32)) as [parcel_id],
       cast('in_transit' as varchar(32)) as [status];
```

## Build, Load, Test and managed state

Build installs or replaces the View and validates deferred result-column references. A View does not participate in Load and has no bookmark, load status, reject relation, row audit, row signature or identity column. Test does not execute the View itself; installed Tests and Assumptions may query it.

Build records the declaration in `_.TableDictionary`, notes in `_.ColumnDictionary`, keys in `_.KeyDictionary`, relationships in `_.ForeignKeyDictionary`, dependencies in `_.Dependency`, and certification in `_.Registry`. See the [catalogue schema](../catalogue-schema.md) for exact columns and [Build](../operation-behaviour/build.md) for protected-rebuild behaviour.
