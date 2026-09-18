# Schemas, keys and managed columns

A Weaver Table has two column layers:

- the **business schema** comes from an authored `Schema` or from the query shape Build establishes; and
- **managed columns** are added by Weaver for identity, row auditing and keyed change comparison.

Keys and column metadata apply to the business schema. They describe row identity and relationships without promising a physical index or enforced database constraint.

## Declared schema and inferred schema

Python Tables must declare `Schema`. Spark SQL and Warehouse Tables may either declare it or let Build infer their business columns from the query result shape. Views always take their columns from their query.

With a declared schema:

- authored names, case, order and types define the installed business shape;
- a SQL query must return every declared business column and no undeclared one;
- query order may differ because declared order wins; and
- Python code must return values the target engine can write as the declared types—Weaver does not coerce an arbitrary frame into shape.

With an inferred SQL schema, Build obtains business names and physical types from the target engine. Column-referencing metadata remains authored. A primary key, comparison column, column note or nullability declaration must still name an inferred column exactly, so Build can reject a reference only after it has the query shape.

Inference does not derive Weaver metadata from SQL constraints, indexes, Spark attributes or sample data. Changing a physical query shape also does not update the installed contract until Build installs the changed document.

## Primary keys identify rows for Load

A primary key is an ordered, non-empty set of business columns. Its columns are implicitly non-null. An incremental Table requires one because updates and explicit deletes must identify existing rows.

For a keyed Load, the primary key decides whether a staged row is an insert or a match. It is also the required shape of an explicit incremental delete claim. Key order is preserved, so a composite key is not an unordered set.

Declaring a key does not promise that Fabric creates an index or enforces a relational constraint. Weaver uses the logical key in generated and runtime Load work and records it in the catalogue.

## Unique keys and foreign keys add logical rules

Unique keys are ordered lists of ordered column sets. They cannot duplicate the primary key or one another. Load uses their declaration order while handling incoming duplicate rows, and an incremental merge that would leave the target non-unique fails rather than publishing that invalid state.

Foreign keys pair this Table's ordered columns with equally sized ordered columns on another logical object. They record a relationship, including across logical items, but they do not by themselves:

- create an execution dependency;
- create or name a database constraint;
- build an index; or
- enforce referential integrity in the target engine.

Use authored imports, relation references or explicit `Dependencies` for execution order. [Dependencies](../core-concepts/dependencies.md) explains that separate graph.

## Nullability is authored

Business columns are nullable unless they are in the primary key or named under `Not null`. Primary-key columns must not be repeated under `Not null`; they are already non-null by definition.

For a declared schema, Check can validate these references locally. For an inferred SQL shape, Build performs the reference check after the engine exposes the result columns. Load then applies the installed nullability contract to returned rows under its normal rejection and fault-tolerance rules.

Managed audit, signature and identity columns are physically non-null and do not belong under authored `Not null`.

## Comparison columns decide whether a matched row changed

A keyed Table compares matched rows using its comparison columns. By default, that set is every business column outside the primary key. `Comparison columns` can narrow the set when another business column should not cause an update.

Weaver computes and stores a managed row signature over that set. A matching key with a different signature is an update; changing a column excluded from the comparison set does not make the row an update. The primary key and Weaver-managed columns are not part of the digest.

The signature is local bookkeeping for one physical Table. Lakehouse and Warehouse representations need not contain the same bytes, and applications should not compare, author or populate it.

## Identity is a managed surrogate

`Identity` requests a managed, engine-generated `bigint` surrogate outside the business schema. Authored staging data does not supply it.

The identity name must not also appear under `Schema`, collide with an inferred query column or name the primary key. The primary key must come from source data so a later Load can match an existing row; an engine-generated identity cannot serve that purpose.

`Table.columns()` and `Table.dataframe()` omit the identity along with the other managed columns. It remains part of the physical Table and its installed metadata.

## Audit and signature columns are not business columns

Weaver adds three row-audit timestamps to Tables for insertion, update and delete lifecycle state. Live rows use a maximum-date sentinel for the non-null delete value. Python code can opt into those audit columns with `dataframe(row_audit_columns=True)`; the row signature is never exposed through that projection.

A keyed loadable Table also carries the managed row signature. An unkeyed Table replaces its target wholesale and does not need one. Folders have neither Table row-audit columns nor a row signature.

Managed names are reserved in both their Lakehouse and Warehouse spellings. Check rejects authored columns that collide with them.

## Physical representation follows the engine

The logical model is shared, but its physical form is engine-specific:

| Concern | Lakehouse Delta | Fabric Warehouse |
| --- | --- | --- |
| Business types | Spark/Delta types | T-SQL types |
| Audit names | lower snake case | spaced public names |
| Audit timestamp type | Spark `timestamp` | `datetime2(6)` |
| Row signature | SHA-256 hex text stored as `string` | SHA-256 bytes stored as `varbinary(32)` |
| Identity | engine-generated `bigint` | engine-generated `bigint` |

Those representations support the same Weaver behaviour; they are not a portable cross-engine row format. A declaration should use the type vocabulary for its target and should not return managed columns from authored code or queries.

Use [Table reference](../reference/weaver-documents/table.md) and [Common metadata](../reference/weaver-documents/common-metadata.md) for exact authoring fields and accepted forms. [Catalogue schema](../reference/catalogue-schema.md) owns the exact catalogue column inventory, and [Python authored objects](../reference/python/objects.md) defines author-facing projections.
