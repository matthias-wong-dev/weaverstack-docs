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
SemanticModel/ItemName
Report/ItemName
```

`Lakehouse`, `Warehouse`, `SemanticModel` and `Report` are the item kinds and use that spelling. The kind is part of identity, so `Lakehouse/Shared` and `Warehouse/Shared` are different items.

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
SemanticModel/PhysicalName
Report/PhysicalName
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
| Build | repeatable `--item ITEM[=TARGET]`, item type or `PowerBI[/project]` | every configured target | no object selector |
| Load | positional `ITEM ...`; repeatable `--item ITEM` is the legacy equivalent | every item installed in the catalogue, in logical identity order | repeatable `--name NAME` |
| Test | positional `ITEM ...`, `PowerBI[/project]`; legacy `--item` | installed items, or project validations in catalogue-free file mode | repeated regex `--name`, repeated `--file` paths/directories/globs |
| Health | repeatable `--item ITEM` | the complete installed estate | none |
| Wipe | positional physical Lakehouse/Warehouse/SemanticModel targets | eligible recorded estate, with configuration guard | no Report wipe |
| Unbind | explicit physical `TARGET ...`, including Report | error | claim removal only |
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

Build has no object-name selector. It reads the whole project for validation and dependency resolution, but selected logical items remain its installation boundary. Repeated identical selections deduplicate; conflicting exact bindings for the same item fail. An exact binding overrides an overlapping type/project selector. Two ordinary selected items of the same kind cannot use one physical target.

Build also accepts exact type selectors `Lakehouse`, `Warehouse`, `SemanticModel`, `Report` and `PowerBI`/`PowerBI/<project>`. Type selectors expand known source/configured items; Power BI groups expand their native model/Report definitions. Unknown/empty groups fail. These are not wildcard or regex item selectors. Source items and Power BI items cannot be built in one mixed call. Build destinations still require explicit/configured bindings for each expanded item.

## Load selection

Positional and legacy `--item` values combine and deduplicate in requested order. Use exact `Lakehouse/Name`, `Warehouse/Name` or `SemanticModel/Name`; `PowerBI`/`PowerBI/<project>` selects models discovered at `--source` (default current directory/Notebook Resources). Reports cannot Load. `ITEM=TARGET` is refused. Installed runs use recorded targets; catalogue-free refresh uses configuration or model names and requires explicit models/project selectors.

Repeat `--name` for case-insensitive whole-name regular expressions. Patterns match `Schema.Object` in Warehouses, `Tables/Schema.Object` or `Files/Schema.Object` in Lakehouses and installed model refresh names. A bare Lakehouse match is refused if both areas match in one item. The same matching name in several selected items is a set of matches, not automatically an ambiguity. Every pattern must match and invalid regex fails. Regex is neither glob nor substring syntax; use `[.]` for a literal dot.

```bash
weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --descendants --dry-run
weaver load Lakehouse/Landing --name 'Tables/Parcel[.]Status' --dry-run
```

Without expansion, named matches are an unordered operator override without inferred barriers. `--ancestors` and `--descendants` each traverse from the original selected seeds within requested installed items; their union has dependency ordering and required endpoint/publication barriers. It does not recursively add ancestors of newly reached descendants. No flag builds changed source or adds an unnamed item. Catalogue-free refresh rejects installed-graph name/stale/reload/recursive selection. See [Load behaviour](load.md).

## Test selection

Test combines/deduplicates positional and legacy items and rejects Build binding syntax. `PowerBI[/project]` expands only semantic models from `--source`; Reports cannot Test. Catalogue mode runs installed definitions against recorded targets. Without a catalogue, or when `--file` is supplied, source/file mode runs project validations against configured targets or logical names.

Repeated `--name` patterns match the complete logical `Schema.Object`, ignoring case; each must match. Validation names have no Lakehouse area prefix. Data dependencies do not add data work or more validations.

Repeated `--file` values select files, project directories or quoted glob patterns. Declared files keep their owning items, which must be inside an explicit item scope. An external single file requires exactly one named item; an external directory is refused. Files can be filtered by names; the options are not mutually exclusive. An unmatched file glob, no-validation directory or unmatched regex fails, not an empty pass. Source/file runs do not install or record definitions. See [Test behaviour](test.md) and [DAX validations](../power-bi/validations.md).

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

It does not select an unselected item. To operate on both sides of a cross-item relationship, select both items. Unexpanded named Load intentionally omits graph expansion and ordering, while Test dependencies describe inspected data rather than a producer chain.

See [Workspace configuration](../configuration-files/workspace-config.md) for physical binding precedence and the individual [operation behaviour](index.md) pages for state and failure boundaries.
