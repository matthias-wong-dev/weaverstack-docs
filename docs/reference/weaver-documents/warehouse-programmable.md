# Warehouse programmable

A Warehouse programmable is an authored stored procedure managed by Build. No other programmable kind is accepted on this authoring surface.

## Location and identity

The file is UTF-8 T-SQL at:

```text
Warehouse/<Item>/programmables/<Schema>.<Procedure>.sql
```

It sits directly under `programmables/`; nested directories and Lakehouse programmables are not supported. The filename has exactly one schema and procedure component. Its managed identity is the owning Warehouse plus `Schema.Procedure`.

The file contains exactly one declaration matching:

```sql
CREATE OR ALTER PROCEDURE <Schema>.<Procedure>
```

Bracketed T-SQL identifiers are accepted. Statement and filename agreement is case-insensitive; the managed identity retains the filename spelling. Plain `CREATE PROCEDURE`, a second procedure declaration, a mismatched name and an authored procedure in Weaver's reserved `_` schema are rejected.

Programmables have no Weaver metadata block, metadata keys, dependency declaration, Python class, required method or return form. Weaver runs the complete file verbatim during installation. References inside the procedure body are not inferred into the project dependency graph.

```sql
create or alter procedure Parcel.RefreshSummary
as
begin
    set nocount on;
    select count(*) as ParcelCount
    from Parcel.Current;
end;
```

Path: `Warehouse/Reporting/programmables/Parcel.RefreshSummary.sql`.

## Operations and managed state

- **Check** validates location, suffix, filename shape, UTF-8 text, the single `CREATE OR ALTER PROCEDURE` declaration, name agreement and reserved schema.
- **Build** creates a new procedure, replaces one whose source changed, leaves an unchanged one alone and drops a removed managed procedure. It is installed as managed Warehouse structure with role `Programmable`.
- **Load** and **Test** do not invoke authored programmables. Their callers execute them outside Weaver's Load/Test scheduler.

`_.Registry` records the procedure identity, physical type `Stored procedure`, role `Programmable`, source signature and Build publication state. There is no separate programmable dictionary, Load status, Test status or Weaver-managed result column for its body.
