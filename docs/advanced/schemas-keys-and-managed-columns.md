# Schema contract

A Weaver schema declaration describes the business columns a Table is expected to expose: their names, order, data types and authored nullability. Primary, unique and foreign keys add logical row and relationship expectations. The declaration does not expose Weaver's parser objects or intermediate schema model as an API.

## Declared columns

A `Schema` mapping preserves authored column order. Column names are exact-case. A declared Table is installed in that order even when a SQL query returns the same columns in another order.

The declared data type is the installed type. A business column is nullable unless it is named by `Not null` or belongs to the primary key. Primary-key columns are therefore not nullable without also being repeated under `Not null`.

Python Table documents must declare `Schema`. Spark SQL and Warehouse Table documents may declare it. When they do, it is authoritative: the query must return every declared business column, no undeclared business column, and the exact declared spelling. A mismatch fails Build rather than silently dropping, adding or renaming a query column.

A schema declaration does not coerce an authored Python result into shape. Authored code must return the declared columns with values the target engine can write as the declared types.

## Inferred columns

A Spark SQL or Warehouse Table may omit `Schema`. Its business column names and physical types are then obtained from the result shape established by the target engine during Build. A View also takes its columns from its query rather than a `Schema` mapping.

Inference supplies only facts available from that result shape. Authored metadata still controls primary keys, unique keys, foreign keys, comparison columns, column notes, nullability and any managed identity column. Every such metadata reference must match an inferred business column exactly.

This boundary is deliberate:

- declared schema decides names, order, types and authored nullability;
- inferred schema takes names and types from the built query shape;
- metadata is not inferred from SQL constraints, indexes, Spark attributes or source data;
- later physical changes do not rewrite the installed declaration without Build.

## Keys and relationships

`Primary key` is an ordered, non-empty set of business columns. It is required for incremental Table processing. The primary key identifies rows for comparison, update and explicit deletion, and its columns are not nullable.

`Unique keys` is an ordered list of ordered column sets. Declaration order is significant when Load evaluates incoming duplicates. A unique key must not duplicate the primary key or another unique key.

`Foreign keys` pair an ordered set of this object's columns with an equally sized ordered set on another logical object. They record a relationship. They do not add a dependency by themselves and do not require Weaver to create or enforce a physical database constraint.

Keys are logical Weaver metadata even where an installed engine representation includes a non-enforced key declaration. Do not treat them as a promise of an index, engine-enforced referential integrity or a particular constraint name.

## Weaver-managed columns

Weaver can add columns that are not part of the authored business schema:

- row-audit columns record insert, update and delete lifecycle times for Tables;
- a row-signature column supports change comparison for keyed loadable Tables;
- an authored `Identity` name requests a Weaver-managed, engine-generated surrogate value outside the business schema.

Managed names are reserved. An authored business column, key or identity declaration that collides with a reserved managed name is invalid. An identity column must not also be declared under `Schema`, returned by the query or used as the primary key.

`Table.columns()` and ordinary `Table.dataframe()` expose business columns. The public row-audit option adds the audit columns. The row signature remains managed state rather than an authored projection. Exact method signatures are in [Python authored objects](../reference/python/objects.md).

Managed-column spellings, physical encodings and generated statements can differ between Lakehouse and Warehouse targets. Those implementation forms are not an additional authoring surface.

## Validation and failure points

Validation occurs at the earliest boundary that has the required evidence.

**Project discovery** rejects malformed schema values, duplicate or case-colliding columns, unknown metadata keys, missing required schemas, invalid key shapes, key or nullability references outside a declared schema, repeated keys and reserved-name collisions. Check reaches this boundary without contacting Fabric.

**Build** validates deferred references after an inferred result shape is available. It rejects missing or extra columns for a declared SQL schema, metadata references absent from an inferred shape, case mismatches, ambiguous case-only query columns and identity collisions. These failures do not turn the inferred result into new source metadata.

**Load** validates returned data against the installed contract. Missing required values, duplicate incoming keys and incompatible rows are reported under Load's fault-tolerance rules. A proposed incremental merge that would leave a declared unique key invalid fails without accepting the invalid target state. Target-engine type or expression errors remain execution failures.

The same declaration is used after installation. Load does not reopen the project to discover a newer schema, and a source edit has no runtime effect until Build installs it.

## Defined behaviour

The Schema contract specifies that Weaver:

1. preserves authored business-column names, order, types and declared nullability;
2. treats primary-key columns as non-null and keeps ordered primary, unique and foreign-key sets;
3. uses a declared SQL schema as authoritative and otherwise obtains business names and types from the built query shape;
4. keeps authored metadata authoritative when business columns are inferred;
5. treats keys and relationships as logical metadata rather than a promise of physical enforcement;
6. keeps managed audit, signature and identity columns outside the authored business schema;
7. rejects declaration errors during discovery and deferred shape errors during Build; and
8. executes Load against the installed schema contract rather than unbuilt source.

See [Weaver documents](../reference/weaver-documents/overview.md), [Build](../reference/operation-behaviour/build.md), [Load](../reference/operation-behaviour/load.md), and [Python authored objects](../reference/python/objects.md).
