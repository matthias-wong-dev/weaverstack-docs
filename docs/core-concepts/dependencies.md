# Dependencies

Weaver normally discovers dependencies from authored imports and relation references. These relationships connect the documents that produce data to the documents that read it, without requiring a separate graph to be maintained by hand.

A document can declare `Dependencies` when deliberate control is needed. An explicit declaration **replaces** inference; it does not add to the relationships Weaver discovered. An explicit empty list therefore means that the document has no managed dependencies.

Spark SQL data documents are the exception to inference-first authoring: they still require an explicit `Dependencies` declaration, including an empty declaration when they depend on no managed object. Weaver can extract relation references from Spark SQL, but the current document contract still requires the explicit field.

## Document dependencies

A document dependency says that one Weaver document reads another. Weaver can infer these relationships from supported Python imports and SQL relation references without executing the authored code.

Within a logical item, dependencies establish the document graph. Build uses that graph to install producers before consumers and to find downstream documents affected by a changed declaration. Load uses the installed form of the graph to order selected data-producing work.

Physical relation names can point outside the managed project estate. Weaver preserves such references, but they do not identify a managed producer that Build can select or Load can order.

## Item dependencies

When a relationship crosses logical items, it also creates an item dependency. Item dependencies determine a valid order for a multi-item Build and for item-wide Load work when both items are selected.

The item graph must be acyclic. A project in which two items depend on each other has no valid Build order and is rejected. Explicit dependencies are not a way to enable a circular item graph.

Document and item graphs answer different questions. The document graph identifies the affected and ordered work. The item graph ensures that physical item boundaries are crossed in a valid order.

## Logical Shortcuts carry managed relationships across items

A logical Shortcut gives a consumer a local logical name for data owned by another item. Dependencies that resolve through it still point to the source document, while the Shortcut remains an installation step between source and consumer:

```text
source document → logical Shortcut → consuming document
```

That extra step lets Build materialise the Shortcut after its source and before consumers. It also lets Load preserve the managed producer-consumer order across physical engines when both sides are in scope.

A physical Shortcut or directly qualified physical relation has no managed project producer. Weaver cannot infer project ordering from that external address.

## Dependencies do not widen selection

Dependencies order and affect work inside the requested boundary; they do not silently add another logical item to an operation.

For Build, selecting an item can rebuild changed documents and affected descendants in that item, while dependent documents in an unselected item remain unchanged. Select every item whose installed state should change.

For an item-wide Load, Weaver orders the selected loadable documents using the installed graph. An upstream object in an unselected item is not added to the run. Deliberately named Load selection is narrower still: it runs the named installed documents without dependency expansion or dependency ordering.

Test uses dependencies to understand what each validation reads and whether a previous result is stale. Dependencies do not turn data producers into additional Test work.

See [Shared selection and identity](../reference/operation-behaviour/shared-selection-and-identity.md) for exact inference forms, declaration syntax and operation-specific selection rules. [Build, Load and Test](build-load-and-test.md) explains where each graph enters the lifecycle.
