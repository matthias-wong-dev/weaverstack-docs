# Python validation objects

Python validations are Weaver documents implemented as classes. Import the four public classes on this page from `weaver`.

This page documents their Python call shape. SQL validation files have a different program shape, and CLI Test selects installed or source-file validations rather than constructing these classes. See [Validate an installed estate](../../basics/tests-and-assumptions.md) for those workflows and [Weaver documents](../../core-concepts/weaver-documents.md) for Test and Assumption semantics.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

- `weaver.Assumption` — class
- `weaver.SparkSqlAssumption` — class
- `weaver.SparkSqlTest` — class
- `weaver.Test` — class

<!-- END GENERATED PYTHON -->

All four classes share this constructor through `WeaverObject`:

```python
(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

A validation may be freestanding for `read()`, `expected()`, or `actual()` calls. `run()` requires a catalogue anchor because it records the result before returning. Passing another `WeaverObject` as `spark` reuses that object's runtime context.

## `Test`

```python
Test(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Subclass `Test` and implement both sides:

```python
expected()
actual()
read()
run()
```

`expected()` returns the required relation; `actual()` returns the relation under test. `read()` is supplied by `Test` and returns their symmetric difference. Do not override it. Defining `read()` on a `Test` subclass fails when the subclass is created.

When the declaration has a primary key, diagnostic rows include correlation data for the two sides. The key does not change which rows are compared. An empty difference passes. `run()` returns a result carrying `missing_count`, `unexpected_count`, and `error_message`.

```python
from weaver import Test

from Parcel__ExpectedStatus import Parcel__ExpectedStatus
from Parcel__CurrentStatus import Parcel__CurrentStatus


class Parcel__StatusReconciles(Test):
    def expected(self):
        return Parcel__ExpectedStatus(self).dataframe()

    def actual(self):
        return Parcel__CurrentStatus(self).dataframe()
```

If either side cannot be evaluated, `run()` records an Error outcome and re-raises the exception. It does not turn an evaluation error into zero discrepancies.

## `Assumption`

```python
Assumption(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Subclass `Assumption` and implement:

```python
read()
run()
```

`read()` returns rows that contradict the statement. No rows means the Assumption holds. An Assumption cannot declare a primary key because it returns one evidence relation rather than two relations to correlate. `run()` returns a result carrying `violation_count` and `error_message`.

```python
from weaver import Assumption

from Parcel__CurrentStatus import Parcel__CurrentStatus


class Parcel__StatusIsKnown(Assumption):
    def read(self):
        return Parcel__CurrentStatus(self).dataframe().where(
            "Status is null or Status not in ('Accepted', 'In transit', 'Delivered')"
        )
```

As with `Test`, an evaluation error is recorded and re-raised rather than reported as a passing result.

## `SparkSqlTest`

```python
SparkSqlTest(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Runtime class generated from a Spark SQL Test document. Its `sql: str` attribute contains the program. After optional setup statements, the first result query is the expected relation and the second is the actual relation. `expected()`, `actual()`, `read()`, and `run()` expose the same semantics as `Test`.

Do not subclass `SparkSqlTest` in repository Python. Author the SQL validation file described in [Validate an installed estate](../../basics/tests-and-assumptions.md); Build generates this class.

## `SparkSqlAssumption`

```python
SparkSqlAssumption(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Runtime class generated from a Spark SQL Assumption document. Its `sql: str` attribute contains the program. After optional setup statements, one result query returns the violating rows. `read()` and `run()` expose the same semantics as `Assumption`.

Do not subclass `SparkSqlAssumption` in repository Python. The authored form is the SQL validation document, not this generated class.
