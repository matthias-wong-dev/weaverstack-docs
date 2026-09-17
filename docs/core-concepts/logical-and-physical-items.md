# Logical and physical items

A Weaver project names **logical items**. Workspace configuration binds each logical item to a **physical item** in Microsoft Fabric.

```text
logical item                 physical target
Lakehouse/Landing      →     Lakehouse/Landing_Dev
Warehouse/Operations   →     Warehouse/Operations_Dev
```

The logical identity belongs to the project. The physical target belongs to one Fabric workspace. This separation lets the same project describe development and production without putting environment-specific Fabric names into declaration files.

See [Projects and estates](projects-and-estates.md) for the desired-versus-installed-state model and [How Weaver works](how-weaver-works.md#physical-bindings) for the lifecycle around a binding.

## A Workspace supplies the physical context

A Weaver **Workspace** configuration identifies the Fabric workspace used by an operation. It can also name the catalogue Warehouse, Environment, execution settings and logical-to-physical target bindings.

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue

targets:
  Lakehouse/Landing: Landing_Dev
  Warehouse/Operations: Operations_Dev
```

Here `Parcel Development` is the Fabric workspace. `Warehouse/Catalogue` is the Warehouse that holds Weaver's installed and operational state. `Landing_Dev` and `Operations_Dev` are physical Fabric item names.

A Workspace does not change the identities in the project. `Lakehouse/Landing` remains `Lakehouse/Landing` wherever it is installed.

## A logical item owns project resources

A logical item identity is its kind and name:

```text
Lakehouse/Landing
Warehouse/Operations
```

The kind is part of the identity. A Lakehouse and a Warehouse may therefore both be named `Shared`; `Lakehouse/Shared` and `Warehouse/Shared` are different items.

Resources are owned by their logical item. For example:

```text
Lakehouse/Landing/Tables/Parcel.Event
Warehouse/Operations/Parcel.Event
```

These can share the object name `Parcel.Event` without becoming the same resource. Their item ownership and, for the Lakehouse, the `Tables` area distinguish them. [Resources and artefacts](resources-and-artefacts.md) explains resource identities in more detail.

## A physical target is an existing or selected Fabric item

A physical target is identified by its Fabric item kind and name within the configured workspace. A binding answers where Build should realise one logical item.

Bindings preserve item kind:

- a logical Lakehouse must target a physical Lakehouse;
- a logical Warehouse must target a physical Warehouse.

The short values in `workspace-config.yml`, such as `Landing_Dev`, inherit their kind from the logical key. An explicit command-line binding writes both sides:

```bash
weaver build ./parcel-ops \
  --item Lakehouse/Landing=Lakehouse/Landing_Scratch
```

Weaver rejects a Lakehouse-to-Warehouse or Warehouse-to-Lakehouse binding. It also keeps ordinary logical items isolated: two logical items cannot be installed to the same physical target.

The catalogue Warehouse is separate from these ordinary targets. It records the installed estate; it is not an implicit destination for a project's Warehouse resources.

## Bindings make projects portable

Development and production can use different configuration files for the same source:

```yaml
# workspace-dev.yml
workspace: Parcel Development
catalogue: Warehouse/Catalogue_Dev

targets:
  Lakehouse/Landing: Landing_Dev
  Warehouse/Operations: Operations_Dev
```

```yaml
# workspace-prod.yml
workspace: Parcel Production
catalogue: Warehouse/Catalogue

targets:
  Lakehouse/Landing: Landing
  Warehouse/Operations: Operations
```

The declaration paths and logical identities do not change. Select the environment by selecting its workspace configuration:

```bash
weaver build ./parcel-ops \
  --workspace-config workspace-dev.yml
```

Build reads the configured bindings and records the resolved installed bindings. Load, Test and Health then use the installed bindings from the catalogue rather than reinterpreting a changed `targets:` mapping. Rebuild an item when its binding should change.

## Item selection is a boundary

Commands select logical items even though the work runs against physical targets:

```bash
weaver build --item Lakehouse/Landing
weaver load Lakehouse/Landing
weaver test Warehouse/Operations
weaver health --item Warehouse/Operations
```

Naming no item has command-specific meaning. Build selects every configured item; Load and Test select every installed item. Build uses repeatable `--item` options because its positional argument is the source, while Load and Test take item identities positionally. The [CLI reference](../reference/cli.md#item-and-target-selection) owns the complete grammar.

An item selection is also an execution boundary. A dependency on a resource in another item does not silently add that item to a Load run. Select both items when both should run:

```bash
weaver load Lakehouse/Landing Warehouse/Operations
```

Within that selected scope, Weaver orders installed work by its dependencies. Name-level selection is a narrower operator override. The [Load contract](../contracts/load.md#inputs-and-selection) defines both behaviours.

Continue with [Resources and artefacts](resources-and-artefacts.md) for the contents of an item, or use the [Lakehouse](../guides/lakehouse-pipeline.md) and [Warehouse](../guides/warehouse-pipeline.md) guides to author one.
