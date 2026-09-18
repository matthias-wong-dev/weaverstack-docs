# Wipe behaviour


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
