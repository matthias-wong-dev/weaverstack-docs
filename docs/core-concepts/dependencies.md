# Dependencies

A dependency states that one Weaver document reads another. Across the [Weaver operations](weaver-operations.md), that relationship determines Build impact and the order of item-wide work. It does not widen the items selected for an operation.

## Weaver discovers or reads dependencies from documents

Depending on the document form, Weaver can discover dependencies from Python imports and SQL relation references. A document can instead declare its dependencies explicitly in metadata.

An explicit dependency list replaces discovery rather than extending it. An explicitly empty list states that the document has no managed dependencies. Spark SQL data documents require an explicit list because a query may read paths or other sources that static SQL relation discovery cannot represent completely.

Weaver determines these relationships without executing authored Python or SQL. Exact import forms, metadata keys and SQL rules belong with each document type in Reference.

## Logical shortcuts connect items

A short object name resolves within the document's owning logical item. To represent a managed read across logical items, declare a logical Shortcut in the consuming item. The Shortcut identifies both the document presented to the consumer and the document that owns the data.

A physical reference can name a Fabric object outside the logical estate, but Weaver cannot infer a managed project dependency from that physical name.

## Build uses dependencies for order and change impact

Build installs upstream documents before selected documents that depend on them. If an upstream declaration changes, selected downstream documents may also need to be rebuilt even when their own files are unchanged.

Selection remains the boundary. If a downstream document belongs to an unselected item, Build leaves that item unchanged. Select every item that should participate in the Build.

A dependency cycle has no valid Build order. Project checking and Build reject cycles rather than using file order to break them.

## Load orders selected work

An item-wide Load uses the dependencies recorded by Build. Within the selected items, upstream load work runs before downstream load work.

A dependency on an unselected item does not add that item to the run. Select both items when both should load.

A named Load is a narrower operator selection: it runs exactly the named installed documents without adding or ordering their dependencies. The Load contract owns the detailed selection and failure behaviour.

## Test reads dependencies but does not sequence validations

Tests and Assumptions can depend on the data they inspect. Nothing can depend on a Test or Assumption: validations consume data and do not produce data for another document.

Test selects installed validations from the requested items. Their dependencies do not add items to the Test run, and Tests and Assumptions run in stable identity order rather than dependency order among validations.

Declare relationships in documents and Shortcuts, not through filenames or directory order. The [development cycle](development-cycle.md) shows where dependency impact enters the edit, Build, Load and Test loop. [Fault tolerance](fault-tolerance.md) explains how each operation proceeds after work fails.
