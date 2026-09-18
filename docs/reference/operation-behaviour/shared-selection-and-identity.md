# Shared selection and identity


---

## Identity and naming contract

Weaver identities name authored intent. Physical names identify Fabric items in one workspace. Changing a physical binding does not change a project, item, schema or document identity.

Identity is exact-case. Case is not normalised for lookup, comparison or collision handling.

## Identity levels

| Level | Canonical form | Example |
| --- | --- | --- |
| Project | project-root folder name | `parcel-project` |
| Logical item | `ItemType/ItemName` | `Lakehouse/Landing` |
| Item-owned schema | `ItemType/ItemName/Schema` | `Warehouse/Operations/Parcel` |
| Lakehouse Table or View | `Lakehouse/ItemName/Tables/Schema.Object` | `Lakehouse/Landing/Tables/Parcel.Status` |
| Lakehouse Folder | `Lakehouse/ItemName/Files/Schema.Object` | `Lakehouse/Landing/Files/Parcel.Events` |
| Lakehouse Test or Assumption | `Lakehouse/ItemName/Schema.Object` | `Lakehouse/Landing/Parcel.StatusIsKnown` |
| Warehouse relation or validation | `Warehouse/ItemName/Schema.Object` | `Warehouse/Operations/Parcel.Status` |

Only `Lakehouse` and `Warehouse` are item types, with that exact spelling. The item type is part of identity: `Lakehouse/Shared` and `Warehouse/Shared` are distinct.

A schema or document identity is item-qualified. The same `Schema.Object` in two items is two declarations. A Lakehouse area is also part of data identity, so `Tables/Parcel.Events` and `Files/Parcel.Events` may coexist in one Lakehouse.

A Lakehouse Test or Assumption has no area because it materialises no data. A Warehouse has no area syntax. Consequently, a Warehouse validation cannot reuse the `Schema.Object` identity of a Table or View in the same item, while a Lakehouse validation may use the same `Schema.Object` as a Table or Folder because the data declarations include their areas.

## Logical names

Project, item, schema and object components are non-empty, exact-case logical names without surrounding whitespace. A single logical component cannot contain `/`, `\\`, `.` or `:`. The dot in `Schema.Object` and slashes in qualified identities are separators, not characters inside a component.

Parsers require the complete canonical shape. They do not infer a missing item type, Lakehouse area, schema or object. Extra path components, an unrecognised item type and padded or empty components are identity errors.

Python filenames and class names encode the schema/object separator as `__`; SQL filenames use `.`. Those are authored spellings of the same `Schema.Object` identity, not alternative runtime identities. The [Weaver documents contract](../weaver-documents/overview.md) defines their agreement rules.

## Logical and physical names

A logical item remains stable across workspace configurations:

```text
Lakehouse/Landing → Lakehouse/ParcelLandingDev
Lakehouse/Landing → Lakehouse/ParcelLanding
```

The left side is the project identity. The right side is the typed physical target resolved for one Build. The logical item's type determines the physical target type; a logical Lakehouse cannot bind to a Warehouse, or the reverse.

Workspace configuration writes a target value as a Fabric item name because its logical key already supplies the kind. Fabric names are trimmed and may contain spaces or dots, but may not be empty, consist only of dots, or contain `/`, `\\`, `:`, `*`, `?`, `"`, `<`, `>` or `|`.

The catalogue Warehouse is a separate physical binding. It records installed logical identities and their target bindings; it does not become the implicit target of a logical Warehouse item.

## Reserved namespaces

`Warehouse/_weaver` is Weaver's built-in catalogue item. A project must not author that item.

Within ordinary items, the schema named `_` is reserved for Weaver-managed definitions. An authored Table, View, Folder, validation, schema document or Warehouse programmable cannot claim it. Names that merely begin with an underscore, such as `_Control`, are ordinary logical names.

Other reserved column names and runtime-specific names belong to the contracts for those authored forms. They do not change the project, item, area, schema and object grammar defined here.

## Parsing, lookup and collisions

Canonical identities round-trip without case folding. Lookup requires the declared spelling. A reference with the wrong case does not bind to the matching declaration under another spelling; where possible, the error identifies the declared spelling.

Within one logical namespace:

- declaring the same identity more than once is an error;
- declaring identities that differ only by case is also an error;
- a shortcut destination colliding with a native document is an error;
- a Test and Assumption cannot share one validation identity;
- an explicit schema and an implied schema that differ only by case collide.

No file, declaration source or composition layer wins a collision. The project must contain one exact spelling.

Some namespaces are deliberately separate. The same object name may coexist across different items, across the `Tables` and `Files` areas of one Lakehouse, and between a Lakehouse data declaration and an area-less validation. Warehouse relations and validations are not separate namespaces.

## Failure semantics

Malformed identity values fail at the boundary that reads them:

- project and declaration identities fail project discovery;
- malformed target keys or physical names in workspace YAML fail configuration loading;
- malformed command selections fail command validation;
- unresolved or wrongly cased logical references fail project validation.

Weaver reports these as errors rather than trimming logical names, changing case, guessing a missing component or silently choosing one colliding declaration.

## Defined behaviour

The Identity and naming contract specifies that Weaver:

1. keeps project, item, area, schema and object identity exact and item-qualified;
2. treats a Lakehouse area as part of data identity;
3. keeps logical identity independent of physical Fabric naming;
4. preserves item kind across a binding;
5. reserves `Warehouse/_weaver` and the `_` schema for Weaver-managed definitions;
6. rejects malformed, duplicate and case-only-colliding identities;
7. resolves logical references using exact declared spelling.

---

## Selection contract

Weaver operations share identity forms, but selection is defined by each operation's authority. A logical item, an installed object name and a physical target are different selectors even when their display names happen to match.

## Shared identity forms

### Logical items

A logical item is written as:

```text
Lakehouse/Name
Warehouse/Name
```

The kind and name identify the item in project source and catalogue state. Logical item selection never means “every dependency reachable from this item”. Dependencies can order selected work without widening its item boundary.

### Installed object names

An installed relational or validation name is `Schema.Object`. A Lakehouse data object may be qualified with its area:

```text
Tables/Parcel.Status
Files/Parcel.Events
```

The area distinguishes a Lakehouse Table from a Folder with the same `Schema.Object`. An operation may accept a bare Lakehouse `Schema.Object` only when the installed selection resolves it unambiguously. Warehouse objects and all Test or Assumption names use `Schema.Object` without a Lakehouse area.

An object name is interpreted inside selected logical items. It is not a physical Fabric path and does not grant authority over another item.

### Physical targets

A physical target is also written `Lakehouse/Name` or `Warehouse/Name`, but its position determines that it names a Fabric item rather than a logical Weaver item. Build and Mirror make this distinction explicit with a binding:

```text
LOGICAL_ITEM=PHYSICAL_TARGET
```

Both sides must have the same item kind. The right side supplies or overrides workspace configuration; it does not rename the logical item.

## Build

Build selects logical items with repeatable `--item ITEM[=TARGET]`. `ITEM` is the source and catalogue ownership boundary; optional `TARGET` is its physical destination. Without `=TARGET`, workspace configuration must provide the binding.

Naming no Build item selects every configured target. Build does not accept object-name selection: it reconciles the selected items and computes changed and impacted documents within them. Dependencies can add selected descendants to the Build plan but cannot add an unselected item.

## Load

Load accepts logical items positionally; repeatable `--item ITEM` is a legacy spelling for the same selection. Naming no item selects every installed item from the catalogue, not every configured project target.

Repeatable `--name NAME` selects exact installed Tables or Folders inside that item boundary. Named selection does not expand or order through dependencies. Item-wide and stale selection do use the installed graph for ordering, while still excluding unselected items.

Load does not accept `ITEM=TARGET`: physical bindings come from the installed catalogue.

## Test

Test uses the same positional and legacy `--item` logical-item grammar as Load. Naming no item selects every installed item.

`--name Schema.Object` selects one installed Test or Assumption inside the item boundary. `--file PATH` instead selects one source validation and requires exactly one installed item to provide its target. The selectors are mutually exclusive. Validation dependencies identify inspected data; they do not expand Test selection or order validations as producers and consumers.

Test does not accept physical target overrides or Lakehouse `Tables/` and `Files/` object areas for validation names.

## Health

Health selects installed logical items only through repeatable `--item ITEM`. Naming none assesses the complete installed estate. It has no object-name, source-file or physical-target selector: Load, Test and Build health are assessed together for each selected installed item.

## Wipe

Wipe positional values are physical `Lakehouse/Name` or `Warehouse/Name` targets. They are not logical item identities, even if a target has the same name as its logical item.

Named targets select exactly those physical Fabric items. Naming none derives the installed physical estate from the catalogue. `--unbind` preserves the catalogue while removing claims for named targets and therefore requires at least one target. Wipe does not traverse project or installed dependencies to add targets.

## Mirror

Mirror selects logical items with repeatable `--item ITEM[=TARGET]`. The optional right side is the destination physical target; without it, the destination comes from workspace configuration. Naming no item selects every configured destination target, not every installed item in the source catalogue.

`--no-item` selects no physical item and forks only the catalogue. It is mutually exclusive with `--item`. Mirror maps the selected source installations to settled destination bindings; it does not accept object names or Wipe-style positional physical targets.

## Empty, duplicate and invalid selections

Where an omitted item selection means “all”, the source of “all” remains operation-specific:

| Operation | Omitted item selection |
| --- | --- |
| Build | every configured target |
| Load | every installed item |
| Test | every installed item |
| Health | the complete installed estate |
| Wipe | physical estate recorded by the catalogue |
| Mirror | every configured destination target |

Repeated Load and Test items are deduplicated in request order. Build and Mirror bindings must not select one logical item more than once or bind two ordinary logical items to the same physical target. A named item that is unknown to the relevant project, configuration or installed catalogue is an error; Weaver does not reinterpret it as a physical target or silently reduce the selection.

## Defined behaviour

The Selection contract specifies that Weaver:

1. distinguishes logical items, installed object names, source files and physical targets by their operation and argument position;
2. uses `Lakehouse/Name` and `Warehouse/Name` for typed item identities;
3. uses `ITEM=TARGET` only where Build or Mirror binds a logical item to a same-kind physical target;
4. keeps dependency traversal inside the authority granted by the operation's item selection;
5. preserves exact named-object selection for Load and single-validation selection for Test;
6. treats Wipe targets as physical rather than logical; and
7. resolves omitted selection from configuration, installed state or physical estate according to the operation rather than applying one universal “all” rule.

See [Identity and naming](shared-selection-and-identity.md), [Build](build.md), [Load](load.md), and [Test](test.md).

---

## Dependencies contract

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
