# Logical and physical items

A Weaver project names **logical items**. Workspace configuration binds each logical item to a **physical item** in Microsoft Fabric.

```text
logical item                 physical Fabric item
Lakehouse/Landing      →     Lakehouse/Landing_Dev
Warehouse/Operations   →     Warehouse/Operations_Dev
```

The logical identity belongs to the project. The physical item belongs to a Fabric workspace.

## Logical items organise the project

A logical item identity combines its kind and name:

```text
Lakehouse/Landing
Warehouse/Operations
```

The kind is part of the identity. `Lakehouse/Shared` and `Warehouse/Shared` are different logical items even though their names match.

Every Weaver document belongs to a logical item. Lakehouse data documents also belong to either the `Files` or `Tables` area. This ownership allows the same schema and object names to appear in different items without making them the same declaration.

## Physical items are environment-specific

A physical item is a Lakehouse or Warehouse in the configured Fabric workspace. Its display name does not become part of the project's logical identity.

Bindings preserve the item kind: a logical Lakehouse maps to a physical Lakehouse, and a logical Warehouse maps to a physical Warehouse. Two logical items cannot be installed into the same physical target.

Commands select logical items. Build resolves those selections to physical targets before changing Fabric. Load and Test use the bindings recorded by the successful Build.

## Workspace configuration owns the binding

Workspace configuration supplies the physical context for operations. It identifies:

- the Fabric workspace;
- the Warehouse containing the Weaver catalogue;
- the physical target for each logical Lakehouse or Warehouse;
- an optional catalogue to mirror;
- environment and execution settings when required.

The catalogue Warehouse is not an implicit target for a project's Warehouse documents. It stores the installed model, bindings and operational state.

Exact configuration keys and YAML forms belong in Reference. The concept is a mapping from stable project identities to one environment's Fabric items.

## Development and production can bind the same project differently

A project can use one set of logical items in both environments. Its production configuration binds them to production Lakehouse and Warehouse items and records state in `Warehouse/ParcelCatalogue`. Its development configuration keeps those logical item names but binds them to `ParcelLandingDev` and `ParcelOperationsDev`, records state in `Warehouse/ParcelCatalogueDev`, and identifies `Warehouse/ParcelCatalogue` as the catalogue it mirrors.

The mechanism is:

```text
same project + production configuration → production targets and catalogue
same project + development configuration → development targets and catalogue
```

No declaration path changes between those builds. Selecting another workspace configuration changes the physical workspace context, catalogue and target mappings; it does not rename the logical items. The [Identity and naming](../contracts/identity-and-naming.md) and [Configuration](../contracts/configuration.md) contracts define the exact boundaries.

Continue with [Weaver documents](weaver-documents.md) for the files that declare the contents of each logical item.
