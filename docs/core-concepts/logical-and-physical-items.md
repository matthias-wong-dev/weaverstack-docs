# Logical and physical items

A Weaver project names logical items such as `Lakehouse/Landing`, `Warehouse/Operations`, `SemanticModel/Parcel` and `Report/Parcel`. `workspace-config.yml` binds them to physical items of the same type in the selected workspace.

```text
logical item                 physical Fabric item
Lakehouse/Landing      →     Lakehouse/ParcelLandingDev
Warehouse/Operations   →     Warehouse/ParcelOperationsDev
SemanticModel/Parcel   →     SemanticModel/Parcel_Dev
Report/Parcel          →     Report/Parcel_Report_Dev
```

The logical identity belongs to the project. The physical item belongs to a Fabric workspace.

Item kinds remain aligned: a logical Lakehouse binds to a physical Lakehouse, and a logical Warehouse binds to a physical Warehouse.

## Choose one of three ownership cases

| Case | Where the data lives | Weaver's boundary |
| --- | --- | --- |
| Ordinary managed item | In the physical target bound to a logical item | Build reconciles the selected item to project declarations and may prune undeclared co-located content. |
| Protected managed object | In a managed target, with `Prohibit rebuild: true` on the Table, Folder, or View | Weaver still owns the object; the flag only guards replacement during Build. |
| External physical source | In a physical item that is not a managed target, reached through a physical Shortcut | Weaver owns the local Shortcut, not the source item or its contents. |

Do not bind or select an external source item as a managed target merely to make it readable. Keep it outside the Build boundary and expose only the required Table, Folder, or schema through a physical Shortcut. See [Protecting data](../advanced/protecting-data.md) for the recoverability decision.

## Logical identity stays with the source

A logical item identity combines its kind and name. The kind matters: `Lakehouse/Shared` and `Warehouse/Shared` are different logical items.

Every Weaver document belongs to one logical item. That ownership keeps otherwise identical object names distinct across items and gives Build, Load and Test a stable item vocabulary independent of Fabric display names.

Commands select logical items. Build resolves them through the chosen workspace configuration. Catalogue-backed Load and Test use recorded installed bindings. Without a catalogue, model refresh and source/file-mode validation resolve the configured targets; there is no installed binding to consult.

## `workspace-config.yml` supplies an environment

A workspace configuration can name:

- the Fabric workspace;
- the Warehouse containing the Weaver catalogue;
- the physical target for each logical item;
- a Fabric Environment for Python work;
- a source catalogue to mirror when establishing a development estate.

The catalogue is optional for standalone Power BI operations. When configured, its Warehouse stores Weaver state. It is separate from the physical target of a logical Warehouse unless both are deliberately hosted in the same Warehouse.

## One project can bind to development and production

For example, the same Warehouse project can carry these two configurations:

```yaml title="workspace-config.prod.yml"
workspace: Parcel Production
catalogue: Warehouse/ParcelCatalogue

targets:
  Warehouse/Operations: ParcelOperations
```

```yaml title="workspace-config.dev.yml"
workspace: Parcel Development
catalogue: Warehouse/ParcelCatalogueDev

targets:
  Warehouse/Operations: ParcelOperationsDev
```

The project still authors `Warehouse/Operations` in both cases. Selecting the production configuration addresses the production workspace and catalogue and builds into `ParcelOperations`; selecting the development configuration addresses the development workspace and catalogue and builds into `ParcelOperationsDev`.

```text
same logical project + production config → production physical estate
same logical project + development config → development physical estate
```

A configuration's `targets` mapping tells Build where to install. Catalogue-backed Load and Test read the installed binding, so an edited mapping takes effect there only after Build publishes it. Catalogue-free model refresh and file-mode validation instead use configuration. [Power BI environment switching](../basics/power-bi/environments.md) shows target names and linked Report bindings.

A build also refuses to install two logical items into one occupied physical target. The exact configuration keys, discovery order and command-line precedence are in [Workspace configuration reference](../reference/configuration-files/workspace-config.md).

Continue with [Weaver documents](weaver-documents.md) for what the project places inside each logical item.
