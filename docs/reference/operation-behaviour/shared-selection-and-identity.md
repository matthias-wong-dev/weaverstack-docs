# Shared selection and identity

Weaver keeps authored identity separate from physical Fabric placement. An operation's argument position decides whether `Lakehouse/Name` denotes a logical item or a physical target.

This page defines the shared names and selection grammars. The individual operation pages define planning, state changes, outcomes and failure handling.

## Project identity

A parsed project's identity is the basename of its selected source directory. Build and Check select a project by path, not by a declared key inside the project.

```bash
weaver check ./parcel-project
weaver build ./parcel-project
```

The project name must be one non-empty logical name with no surrounding whitespace and no `/`, `\\`, `.` or `:`. Project source defaults are operation-specific:

- `weaver check` defaults to the current directory;
- desktop `weaver build` defaults to the current directory;
- Build inside a Fabric session defaults to Notebook Resources and may also accept an `abfss://` directory.

Workspace configuration is discovered from the process's current working directory, not from the selected project source path.

## Logical item identity

A logical item is exactly:

```text
Lakehouse/ItemName
Warehouse/ItemName
```

`Lakehouse` and `Warehouse` are the only item kinds and use that spelling. The kind is part of identity, so `Lakehouse/Shared` and `Warehouse/Shared` are different items.

An item component is a non-empty, exact-case logical name with no surrounding whitespace and no `/`, `\\`, `.` or `:`. Internal spaces are permitted. Parsers do not infer a missing kind or trim logical components.

`Warehouse/_weaver` is Weaver's built-in catalogue item and cannot be authored by a project.

## Schema and document identity

Schemas and documents are item-qualified. Their canonical forms are:

| Declaration | Canonical identity | Example |
| --- | --- | --- |
| Schema | `ItemType/ItemName/Schema` | `Warehouse/Operations/Parcel` |
| Lakehouse Table or View | `Lakehouse/ItemName/Tables/Schema.Object` | `Lakehouse/Landing/Tables/Parcel.Status` |
| Lakehouse Folder | `Lakehouse/ItemName/Files/Schema.Object` | `Lakehouse/Landing/Files/Parcel.Events` |
| Lakehouse Test or Assumption | `Lakehouse/ItemName/Schema.Object` | `Lakehouse/Landing/Parcel.StatusIsKnown` |
| Warehouse Table, View, Test or Assumption | `Warehouse/ItemName/Schema.Object` | `Warehouse/Operations/Parcel.Status` |
| Deployed Lakehouse file | `Lakehouse/ItemName/file:Path/Name.ext` | `Lakehouse/Landing/file:_/Load/lib/rules.py` |
| Warehouse programmable | `Warehouse/ItemName/procedure:Schema/Object` | `Warehouse/Operations/procedure:Parcel/Refresh Status` |

A Lakehouse's `Tables` or `Files` area is part of a data document's identity. A Table and Folder may therefore share one `Schema.Object`. Lakehouse validations have no area because they materialise no data, so a validation may also share its `Schema.Object` with an area-qualified data declaration.

A Warehouse has no area syntax. Its relations and validations use one `Schema.Object` namespace and cannot reuse the same identity.

For ordinary schema and object components, `.` separates `Schema` from `Object`; it is not allowed inside either component. Python filenames and class names encode that separator as `__`, while SQL filenames use `.`. Those are authored spellings, not alternative canonical identities. Deployed-file paths and programmable names have the specialised forms shown above.

The schema `_` is reserved for Weaver-managed definitions in every item. Names that merely begin with an underscore, such as `_Control`, are ordinary logical names.

## Case, lookup and collisions

Canonical authored identity preserves case. Within one logical namespace:

- an exact duplicate is rejected;
- identities that differ only by case are also rejected;
- no source file, generated layer or composition source wins a collision;
- a Shortcut destination cannot collide with a native declaration;
- a Test and Assumption cannot share one validation identity; and
- explicit and implied schemas that differ only by case collide.

Logical item selection uses the canonical item spelling. Installed `--name` lookup for Load and Test is case-insensitive, but the result and catalogue retain the canonical installed identity. Case-insensitive selector lookup does not permit case-only declarations to coexist.

## Physical Fabric identities

A whole physical item is written:

```text
Lakehouse/PhysicalName
Warehouse/PhysicalName
```

A Fabric item name is trimmed and must not be empty, consist only of dots, or contain `/`, `\\`, `:`, `*`, `?`, `"`, `<`, `>` or `|`.

Workspace configuration omits the physical kind in a target value because the logical mapping key supplies it:

```yaml
targets:
  Lakehouse/Landing: ParcelLandingDev
  Warehouse/Operations: ParcelOperationsDev
```

Build and Mirror command selectors include both kinds in an explicit binding:

```text
LOGICAL_ITEM=PHYSICAL_TARGET
```

Both sides must have the same kind. The right side changes the destination for that request; it does not rename the logical item. Physical targets are names within the resolved workspace and cannot carry another workspace qualifier.

The catalogue is a separate physical Warehouse binding. It never becomes an implicit target for a logical Warehouse.

## Selector summary

| Operation | Item or target grammar | Omitted selection | Narrower selector |
| --- | --- | --- | --- |
| Check | positional project directory | current directory | none |
| Build | repeatable `--item ITEM[=TARGET]` | every configured target, in logical identity order | none |
| Load | positional `ITEM ...`; repeatable `--item ITEM` is the legacy equivalent | every item installed in the catalogue, in logical identity order | repeatable `--name NAME` |
| Test | positional `ITEM ...`; repeatable `--item ITEM` is the legacy equivalent | every item installed in the catalogue, in logical identity order | one of `--name Schema.Object` or `--file PATH` |
| Health | repeatable `--item ITEM` | the complete installed estate | none |
| Wipe | positional physical `TARGET ...` | the physical estate recorded by the catalogue | none |
| Mirror | repeatable `--item ITEM[=TARGET]` | every configured target, in logical identity order | `--no-item` selects the catalogue only |
| Install | positional build-bundle path | — | selection is fixed by the bundle |
| Workflow | positional workflow name | — | each entry keeps its command's grammar |
| Session | no operation selection of its own | — | each entered command keeps its grammar |

## Build selection

`SOURCE` selects the complete project snapshot to parse. Repeatable `--item` values select the logical items Build may reconcile:

```bash
weaver build ./parcel \
  --item Lakehouse/Landing \
  --item Warehouse/Operations=Warehouse/OperationsDev
```

The left side of each binding must identify an item in project source. Without `=TARGET`, the selected workspace configuration must provide that item's target. With `=TARGET`, the physical target must have the same kind and overrides the configured target for that request.

Naming no item selects every key in the configuration's `targets` mapping. An empty mapping does not mean every project item; Build then requires explicit items with explicit or configured destinations.

Build has no object-name selector. It reads the whole project for validation and dependency resolution, but selected logical items remain its installation boundary. Selecting the same logical item twice is rejected rather than deduplicated. Two ordinary selected items of the same kind cannot use one physical target.

## Load selection

Load combines positional items followed by legacy `--item` values. Items use logical `Lakehouse/Name` or `Warehouse/Name` syntax. Repeated items are deduplicated in first-requested order. `ITEM=TARGET` is rejected because Load reads the installed physical binding from the catalogue.

```bash
weaver load Lakehouse/Landing Warehouse/Operations
weaver load Lakehouse/Landing --name Tables/Parcel.Status
```

`--name` is repeatable. Inside the selected items, it accepts:

```text
Tables/Schema.Object   # Lakehouse Table
Files/Schema.Object    # Lakehouse Folder
Schema.Object           # Warehouse object, or one unambiguous Lakehouse object
```

Lookup is case-insensitive. A bare Lakehouse `Schema.Object` is rejected when both `Tables/...` and `Files/...` match. A selector matching the same installed node more than once is deduplicated in first-resolved order. A name matching the same identity in more than one selected item is ambiguous; select one item.

Named Load selection runs exactly the resolved installed objects. It does not add their dependencies or dependency-order edges. Item-wide and stale selection use the installed graph, but traversal never adds an unselected item.

## Test selection

Test combines and deduplicates positional and legacy `--item` values in the same way as Load. It rejects `ITEM=TARGET` and reads targets from the catalogue.

Without a narrower selector, Test selects all installed Tests and Assumptions owned by the selected items. Data dependencies do not select additional validations, objects or items.

`--name Schema.Object` selects one installed Test or Assumption inside the item boundary. Lookup is case-insensitive. The selector is ambiguous if the same `Schema.Object` exists in more than one selected item, so select one item. Validation names never use Lakehouse `Tables/` or `Files/` prefixes.

`--file PATH` selects one source Test or Assumption without installing it. It requires exactly one installed item to supply the target and dialect. `--file` and `--name` are mutually exclusive. The path is a source-file selector, not a document identity or physical target.

## Health selection

Health accepts repeatable `--item ITEM` values. Repeated logical items are deduplicated in request order. Naming none selects the complete estate recorded by the catalogue.

Health maps selected logical items to their installed physical targets and deduplicates targets when several selected items resolve to the same target. It has no document, source-file or physical-target selector. Dependency ancestry may still be read to assess selected subjects; it does not add reported item scope.

## Wipe selection

Wipe's positional values are physical targets:

```bash
weaver wipe Lakehouse/ParcelLandingDev Warehouse/ParcelOperationsDev
```

They are not logical item selectors, even when a logical and physical item share a name. Repeated identical typed targets are deduplicated in first-requested order. Wipe does not inspect project source or traverse dependencies to add targets.

Naming no target reads distinct physical targets from the catalogue's installation records. `--unbind` still requires at least one named target because it preserves the catalogue while removing its claims for exactly those targets.

## Mirror selection

Mirror uses Build's `ITEM[=TARGET]` grammar for destination bindings:

```bash
weaver mirror \
  --item Lakehouse/Landing=Lakehouse/ParcelLandingDev \
  --item Warehouse/Operations=Warehouse/ParcelOperationsDev
```

The logical item must have an installation in the source catalogue. Without `=TARGET`, its destination comes from the selected workspace configuration. Naming no item selects every configured target; it does not select every item installed in the source catalogue.

`--no-item` selects no physical item and forks only the catalogue. It is mutually exclusive with `--item`.

Mirror does not accept object names or Wipe-style positional targets. A logical item selected twice is rejected after binding resolution. Destination physical identity includes kind and name: a Lakehouse and Warehouse may share a display name, but two selected items of the same kind cannot share one destination. The source catalogue, destination catalogue, source item targets and destination item targets must all be usable within the one resolved workspace; workspace-qualified Mirror configuration does not widen this boundary.

## Selection and dependency boundary

A selected logical item grants authority over work owned by that item. A managed dependency may:

- order selected Build or item-wide Load work;
- carry Build impact to a selected descendant; or
- supply ancestry used by Health.

It does not select an unselected item. To operate on both sides of a cross-item relationship, select both items. Named Load intentionally omits graph expansion and ordering, while Test dependencies describe inspected data rather than a producer chain.

See [Workspace configuration](../configuration-files/workspace-config.md) for physical binding precedence and the individual [operation behaviour](index.md) pages for state and failure boundaries.
