# Identity and naming contract

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

Python filenames and class names encode the schema/object separator as `__`; SQL filenames use `.`. Those are authored spellings of the same `Schema.Object` identity, not alternative runtime identities. The [Weaver documents contract](documents.md) defines their agreement rules.

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
