# Weaver documents

Source-data Weaver documents declare Tables, Folders and related work. Read those documents as four parts:

```text
path + kind + metadata + authored body
```

- **Path** identifies the owning logical item and, for Lakehouse data, the `Files` or `Tables` area.
- **Kind** says what the document declares: a Table, Folder, View, Test, Assumption, Shortcut, Warehouse programmable or schema description.
- **Metadata** names the declaration and describes properties such as schema, keys, dependencies and load behaviour.
- **Authored body** contains the SQL, Python or mapping that implements the declaration.

For example, in `Warehouse/Operations/Parcel.Status.sql`, the path assigns the document to `Warehouse/Operations`, `Table ID` makes it a Table named `Parcel.Status`, the remainder of the comment carries its metadata, and the query is the body Build installs as data work.

Weaver checks that placement, filename, kind and declared identity agree. Exact paths, metadata fields, defaults and body requirements are in [Weaver documents reference](../reference/weaver-documents/overview.md).

## Native Power BI definitions

PBIP projects, `.SemanticModel` directories, `.Report` directories and named TMDL definitions use native files under `PowerBI/<project>`. They do not require a SQL/Python metadata header. Optional policy, overlays and annotations add conventions without making source generation a prerequisite. DAX validations have their own metadata and model-owned directories. See [Power BI layout](../reference/power-bi/project-layout.md).

## Documents that hold or present data

### Table

A Table declares stored tabular data and, when it has authored load work, how that data is produced. Tables can belong to Lakehouses or Warehouses. Lakehouse Tables live in the item's `Tables` area.

### Folder

A Folder declares files managed beneath a Lakehouse item's `Files` area. Its body produces or reads the files within the declared scope.

### View

A View declares a query-defined relation. Build installs its query as a definition; View creation is not a separate Load step.

## Documents that validate data

### Test

A Test compares expected and actual rows.

### Assumption

An Assumption returns rows that contradict a stated condition. It passes when that result is empty.

Build installs validations for later catalogue-mode Test. Source/file mode can read authored validations directly and run them against deployed objects without persistent catalogue records.

## Documents that connect or describe the estate

### Shortcut

A Shortcut presents data from another location inside an item. A logical Shortcut names another Weaver document and therefore carries a managed cross-item relationship. A physical Shortcut names an external Fabric location directly.

### Warehouse programmable

A Warehouse programmable declares a stored procedure in a Warehouse. Build installs it, but it is not independently loadable.

### Schema metadata

Schema metadata describes a schema or declares one before another document implies it. Tables, Views and other object identities already imply their schemas, so a separate schema document is needed only for that additional declaration.

## Supporting files travel with an item

An item can contain supporting Python modules and other files used by its documents. Build can package those files with installed work, but their presence does not make them independently selectable Weaver documents.

Next, [Build, Load and Test](build-load-and-test.md) explains how authored documents become an operating estate.
