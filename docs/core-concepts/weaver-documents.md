# Weaver documents

Weaver documents are the files you author to declare a logical estate. Each document belongs to a logical Lakehouse or Warehouse item.

Weaver reads three sources of meaning together:

- **Path** identifies the owning item and, for Lakehouse data, the `Files` or `Tables` area.
- **Document type** identifies what the file declares, such as a Table, View or Test.
- **Metadata** names the declaration and describes properties such as schema, keys, dependencies and load behaviour.

Together they establish the document's logical identity and how Build, Load or Test treats it. Weaver checks that the path, filename, document type and declared identity agree. Exact filenames, metadata keys and language-specific syntax belong in Reference and the authoring guides.

## Data documents

### Table

A Table declares stored tabular data. Its document describes the table's identity and data contract and may define the work that populates it. Build installs the table definition and any load work; Load runs installed load work.

Tables can belong to a Lakehouse or Warehouse. A Lakehouse Table is owned by the item's `Tables` area.

### Folder

A Folder declares managed files under a Lakehouse item's `Files` area. Its document defines the folder identity and the file scope and load behaviour Weaver manages.

Folders are Lakehouse documents. A Folder and Table may use the same `Schema.Object` name because `Files` and `Tables` are separate Lakehouse areas.

### View

A View declares a query-defined relation. Build installs the view after the Tables, Folders or other Views it reads. A View has no separate Load step.

## Validation documents

### Test

A Test compares an expected relation with an actual relation. It passes when their symmetric difference is empty. An optional primary key correlates diagnostic rows; it does not change the comparison count.

### Assumption

An Assumption returns rows that contradict a condition. It passes when the result is empty.

Tests and Assumptions are installed by Build and run by Test. They read the estate but do not materialise data objects.

## Connection and structure documents

### Shortcut

A Shortcut declares a relation from one item to data elsewhere. A logical Shortcut names another Weaver document and carries that relationship across item boundaries. A physical Shortcut names an external Fabric location directly.

Shortcuts participate in Build ordering. A logical Shortcut is also how a document in one logical item declares a managed dependency on data owned by another.

### Warehouse programmable

A Warehouse programmable declares a stored procedure that Build manages in a Warehouse item. It is installed structure rather than a Table or View and has no independent Load step.

### Schema metadata

Schema metadata adds a description to a schema or declares a schema that no Table, View or other document yet implies. Object identities imply the schemas they use, so a separate schema document is optional unless that additional declaration is needed.

## Supporting files

An item can include supporting code and data that travel with its installed work. Those files do not become independently selectable Weaver documents merely because they are beneath the item.

The next concept is [Dependencies](dependencies.md): how documents state what they read and how those relationships affect Build, Load and Test.
