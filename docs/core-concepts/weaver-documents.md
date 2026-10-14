# Weaver documents

Weaver adds engineering declarations to the formats you author. For Lakehouse and Warehouse work, a document declares a Table, Folder or related work through four parts:

```text
path + kind + metadata + authored body
```

- **Path** identifies the owning logical item and, for Lakehouse data, the `Files` or `Tables` area.
- **Kind** says what the document declares: a Table, Folder, View, Test, Assumption, Shortcut, Warehouse programmable or schema description.
- **Metadata** names the declaration and describes properties such as schema, keys, dependencies and load behaviour.
- **Authored body** contains the SQL, Python or mapping that implements the declaration.

For example, in `Warehouse/Operations/Parcel.Status.sql`, the path assigns the document to `Warehouse/Operations`, `Table ID` makes it a Table named `Parcel.Status`, the remainder of the comment carries its metadata, and the query is the body Build installs as data work.

Weaver checks that placement, filename, kind and declared identity agree. Exact paths, metadata fields, defaults and body requirements are in [Weaver documents reference](../reference/weaver-documents/overview.md).

## Documents that hold or present data

### Table

A Table declares stored tabular data and, when it has authored load work, how that data is produced. Tables can belong to Lakehouses or Warehouses. Lakehouse Tables live in the item's `Tables` area.

### Folder

A Folder declares files managed beneath a Lakehouse item's `Files` area. Its body produces or reads the files within the declared scope.

### View

A View declares a query-defined relation. Build installs its query as a definition; View creation is not a separate Load step.

## Native models, overlays and annotations

Semantic models use standard TMDL. Reports use their native definitions. Weaver can build those definitions as they are; a PBIP entrypoint opens the project in Desktop.

For Tables and Folders, SQL/Python metadata declares the engineering around the authored code. For semantic models, **TMDL overlays and Weaver annotations play the corresponding authoring role**: add conventions, refinements and managed source relationships to the native model.

An overlay is a partial TMDL file beside a native model. For `Parcel.SemanticModel`, the same-name `Parcel.tmdl` can refine a measure’s format or add an annotation without maintaining a second copy of the model. A shared `PowerBI/policy.tmdl` applies common declarations across models; a model’s local overlay takes precedence.

An annotation requests a modelling rule through normal TMDL syntax:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

That rule hides relationship many-side keys in the deployed model. The authored relationship and native source files remain in place. Other built-ins can identify a managed Table as a model source or apply column visibility conventions.

You can also define a custom annotation as a Python handler and declare it in TMDL. For example, `Parcel.DisplayFolder` can apply a project-specific display-folder convention. Built-in names use the reserved `Weaver` namespace; project handlers use their own namespace. They are executable project code, so Check and Build must only read trusted projects.

Build merges the native definition, shared policy and local overlay, then applies the annotations to the completed model.

[Deploy semantic models and Reports](../semantic-models/native-tmdl.md) shows the native-first workflow and a simple annotation. [Custom annotations](../semantic-models/custom-annotations.md) implements a handler. [TMDL](../reference/power-bi/tmdl.md) and [Annotations](../reference/power-bi/annotations.md) own the exact syntax and precedence.

## Documents that validate data

### Test

A Test compares expected and actual rows using the item’s SQL, Python or DAX validation form.

### Assumption

An Assumption returns rows that contradict a stated condition. It passes when that result is empty. Model-owned DAX validations belong to the same Test/Assumption model; they live beneath the model’s validation directories.

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
