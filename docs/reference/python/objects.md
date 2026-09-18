# Python authored objects

These classes are the public Python surface for Lakehouse object modules and authored shortcut declarations. Import them from `weaver`; modules below the top-level package are implementation details.

Python object classes are not the YAML metadata, SQL document, or CLI forms of the same concepts. See [Weaver documents](../../core-concepts/weaver-documents.md) for the document model, [Lakehouse pipeline](../../basics/lakehouse-python.md) for an end-to-end authoring path, and [Shortcuts](../../basics/shortcuts.md) for shortcut target forms.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

- `weaver.Folder` — class
- `weaver.Shortcut` — class
- `weaver.SparkSqlTable` — class
- `weaver.Table` — class
- `weaver.View` — class
- `weaver.WeaverObject` — class

<!-- END GENERATED PYTHON -->

## `WeaverObject`

```python
WeaverObject(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Base class shared by `Folder`, `Table`, `View`, `Test`, and `Assumption`. Application code normally subclasses one of those concrete classes instead.

`spark` is either a Spark session or another `WeaverObject`. Passing another object reuses its Spark session, resolved Lakehouse, and catalogue anchor. `lakehouse` must be a resolved `Lakehouse`, not a name. `catalogue` may be a `Warehouse/<name>` reference or an already-read catalogue value returned by Weaver.

Principal attributes and methods:

- `spark`, `lakehouse`, and `spark_root` expose the resolved runtime context.
- `identity` is the `(schema, object)` pair derived from the class name. `Parcel__Event` becomes `("Parcel", "Event")`.
- `object_id` is the resulting `Schema.Object` string.
- `installed` is the installed catalogue identity, or `None` for a freestanding object.
- `with_catalogue(catalogue, identity=None) -> WeaverObject` anchors an existing instance and returns it.
- `bookmark()` returns the timezone-aware UTC instant immediately before the object's last clean load began. It requires a catalogue anchor.
- `read()` is the authored read contract and raises `NotImplementedError` on the base class.

Construction fails when there is no Spark session, the Lakehouse value is unresolved, or the class name does not contain exactly one schema/object boundary written as `__`. Operations that need catalogue state also fail for a freestanding object.

```python
from weaver import Table


class Parcel__CurrentStatus(Table):
    def read(self):
        return source_frame.select(*self.columns())


status = Parcel__CurrentStatus(spark, catalogue="Warehouse/Catalogue")
assert status.object_id == "Parcel.CurrentStatus"
```

The module-level metadata attached to an authored class remains part of the Python document. See [Build a Lakehouse pipeline with Python](../../basics/lakehouse-python.md) for a complete document and [Incremental data processing](../../advanced/incremental-data-processing.md) for return forms across changed and unchanged inputs.

## `Folder`

```python
Folder(spark: Any, **kwargs: Any)
```

Subclass `Folder` for files managed beneath a Lakehouse `Files` area. Implement `read()` to write into and return `self.staging_folder()`. An incremental folder may instead return `(staging_folder, files_to_delete)`.

Public methods:

```python
path() -> Path
spark_path() -> str
files_since(bookmark: datetime) -> dict[Path, datetime]
latest_files() -> dict[Path, datetime]
deleted_since(bookmark: datetime) -> dict[Path, datetime]
staging_folder() -> StagingFolder
load(fault_tolerant: bool = False, reload: bool = False) -> LoadResult
```

`path()` is the mounted Python path; `spark_path()` is its `abfss://` address. `files_since()` and `deleted_since()` use a timezone-aware bookmark and apply a strict “after” boundary. `latest_files()` returns current files from the newest change that left files in place.

A standalone `read()` gets a temporary staging directory. A recorded load gets the fixed sibling staging directory for that invocation. Returning a different staging value fails the load. `reload=True` is not supported for folders.

```python
from weaver import Folder


class Parcel__ManifestExport(Folder):
    def read(self):
        staging = self.staging_folder()
        write_manifests(staging.path)
        return staging
```

## `Table`

```python
Table(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Subclass `Table` for rows materialised as a Delta table or Warehouse table. `read()` returns a staging frame. An incremental table may return `(staging_frame, delete_keys)`; a non-incremental table must return only the staging frame.

Public methods:

```python
columns() -> tuple[str, ...]
primary_key_columns() -> tuple[str, ...]
dataframe(row_audit_columns: bool = False) -> Any
empty_dataframe(row_audit_columns: bool = False) -> Any
load(
    fault_tolerant: bool = False,
    ignore_stability_threshold: bool = False,
    reload: bool = False,
) -> LoadResult
```

`columns()` returns business columns in declaration order. `primary_key_columns()` returns the declared key or `()`. `dataframe()` reads the resolved Delta path and omits Weaver's row signature; setting `row_audit_columns=True` appends the three row-audit columns. `empty_dataframe()` returns the same shape with no rows and requires the physical table to exist.

`load()` requires a catalogue anchor and records the outcome before returning. `reload=True` resets the selected table's bookmark and load state, empties the target, then calls `read()`. `ignore_stability_threshold=True` waives declared delete and update limits for that invocation.

See [Incremental data processing](../../advanced/incremental-data-processing.md) for bookmark, delete-claim, and reload behaviour.

## `SparkSqlTable`

```python
SparkSqlTable(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Runtime class generated from an authored Spark SQL table document. Its `sql: str` attribute contains the program, and `read()` executes that program to produce staging and optional delete keys.

Do not subclass `SparkSqlTable` in repository Python. Author a `.sql` document; Build generates the class. [Build a Lakehouse pipeline with Spark SQL](../../basics/lakehouse-spark-sql.md) shows the authored form.

## `View`

```python
View(
    spark: Any,
    *,
    lakehouse: Lakehouse | None = None,
    catalogue: str | Catalogue | None = None,
)
```

Represents a declared SQL view. A View has no `read()` implementation.

```python
dataframe() -> Any
```

`dataframe()` reads the view by its qualified catalogue name through `spark.table(...)`.

## `Shortcut`

```python
Shortcut(
    shortcut_type: str,
    target_type: str,
    target: str,
    workspace: str | None = None,
)
```

Frozen declaration value used in an item's authored `shortcuts.py`. Its attributes preserve the four constructor arguments.

An authored `Shortcut` declares what Build should create; it is not a data reader. Calling it raises a Weaver error. Runtime object code reads a deployed shortcut by importing the generated name from the deployed `shortcuts` module and calling that generated value with the owning object.

```python
from weaver import Shortcut

Parcel__Events = Shortcut(
    shortcut_type="table",
    target_type="logical",
    target="Lakehouse/Landing/Tables/Parcel.Events",
)
```

The accepted shortcut types, target grammar, and logical/physical distinction are documented in [Shortcuts](../../basics/shortcuts.md). They are not interchangeable with workspace YAML target bindings or CLI item selection.
