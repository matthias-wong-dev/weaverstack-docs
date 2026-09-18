# Dependencies contract

A dependency records that one Weaver document reads another managed document. Weaver uses that relationship to determine Build order and change impact. Load and Test use the installed graph for their own execution rules; a dependency is not a request to operate on every item it reaches.

## Inferred and declared dependencies

When a document does not declare dependencies, Weaver can infer managed references from supported Python imports and SQL relation references. Discovery is static: Weaver does not execute authored Python or SQL to find edges.

A declared dependency list replaces inferred dependencies for that document. It does not add to them. An explicitly empty list declares no managed dependencies. Document forms that require an explicit list are invalid without one.

A two-part SQL relation or a supported item-object Python import resolves in the document's logical item. A logical Shortcut can resolve that local name to a producer owned by another item. Qualified physical SQL names and physical Shortcuts remain physical references: Weaver records that the consumer reads them but does not invent a managed project producer or Build edge.

Metadata text references and foreign-key metadata are not execution dependencies unless the document also declares or exposes a dependency through the rules above.

## Validation and failure

Every managed dependency must resolve to exactly one document or logical Shortcut using its declared spelling and area. A missing object, missing Shortcut, ambiguous identity, wrong-case spelling or invalid import form fails project discovery. Weaver does not silently discard or retarget the edge.

Tests and Assumptions may depend on data objects. They cannot be dependency targets because they validate data rather than produce data for another document.

The managed document graph and the cross-item graph must be acyclic. A cycle has no valid Build order and is rejected; source-file or directory order is not used to break it.

## Build impact and selection

Build selection starts with documents and installed work owned by the selected logical items. Dependencies do not add an unselected item to the Build.

Within that boundary:

- new selected objects are selected for installation;
- selected objects whose installed declaration or generated work differs are changed;
- an existing selected descendant of a changed object is impacted, even if its own source is unchanged;
- impact crosses a logical Shortcut when both producer and consumer items are selected;
- a descendant in an unselected item is deferred until that item is built;
- changed and impacted work is ordered so managed producers precede their consumers.

A logical Shortcut is a distinct installed hop between producer and consumer. Changing what it points to changes the Shortcut; an unchanged installed Shortcut is not replaced merely because it was considered during planning.

These are Build rules. They describe which installed definitions may need reconciliation. They do not mean that a later Load or Test run automatically executes the same affected subgraph.

## Load dependencies

An item-wide Load starts from the installed objects in the selected items and uses their installed dependencies for execution order. Upstream selected load work precedes downstream selected load work.

A dependency outside the selected items does not widen the run. A named-object Load is narrower still: it executes only the named installed objects and does not expand or order that selection through dependencies. The [Load contract](load.md) defines its failure and fault-tolerance behaviour.

## Test dependencies

Test selects installed Tests and Assumptions owned by the requested items. Their data dependencies identify what they inspect, but do not add data objects or other items to the Test run. Validations do not form a producer chain: they run in stable identity order rather than dependency order among validations.

## Item and run boundaries

An item boundary controls what Build may reconcile and what Load or Test may execute. A dependency can cross that boundary for resolution and ordering without granting write or execution authority over the other item.

To operate on both sides of a cross-item relationship, select both items. Selecting only the consumer can read an already installed producer through its Shortcut; it does not rebuild, load or test the producer as a side effect.

## Defined behaviour

The Dependencies contract specifies that Weaver:

1. infers supported imports and SQL relation references only when no dependency list is declared;
2. treats a declared list, including an empty list, as the complete managed dependency set for that document;
3. distinguishes managed logical edges from unresolved physical references;
4. rejects invalid managed references, validation targets and cycles;
5. expands Build impact through selected existing descendants without adding unselected items;
6. orders selected Build work from producer to consumer;
7. keeps Load selection within its item or named-object boundary; and
8. uses Test dependencies as inspected-data relationships, not as execution expansion or validation ordering.
