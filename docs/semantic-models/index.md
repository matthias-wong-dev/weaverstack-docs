# Semantic models

Keep the native PBIP and TMDL you already author. Weaver deploys the model and applies optional conventions without rewriting those source files.

## Two ways to use Weaver with Power BI

### Power BI only — without a Catalogue

Use native Power BI Semantic Models and Reports without creating a Fabric Warehouse or Weaver Catalogue. Weaver deploys native definitions, applies shared TMDL conventions, composes model variants and supports DAX validation.

You need an existing Power BI service workspace with appropriate licensing and permissions. Without a Catalogue, Weaver operates directly on the selected models and Reports. It does not maintain centralised installed dependency state, execution history or estate-wide Health.

### Fabric estate — with a Catalogue

If you also use Fabric Lakehouses and Warehouses, configure a Fabric Warehouse as Weaver’s Catalogue. You retain the native Power BI capabilities, while Weaver can coordinate models with their managed data sources.

The Catalogue records installed definitions, dependencies, Load and refresh results, validations and operational state. This enables coordinated execution, recorded testing and Health across the managed estate.

### Start where you are

Both modes use the same Weaver package and native Power BI project files. Start with Power BI alone, then add a Catalogue and managed data sources without replacing your existing model and Report definitions.

The distinction is whether a Catalogue is configured, not which licence you hold. See [requirements and the detailed mode matrix](../reference/power-bi/requirements-and-compatibility.md#mode-matrix) for service, licensing and capability boundaries.

[Deploy a native model](native-tmdl.md), then add one overlay to hide relationship foreign keys. If the convention belongs on several models, [share it as policy](shared-policy.md) instead of repeating it.

[Connect a managed Fabric source](managed-sources.md) when the model needs Warehouse or Lakehouse data; [validate the model](validation.md) when a successful refresh is not enough to establish the right number.

Go further with [custom annotations](custom-annotations.md), [model variants](composition.md) or [authoring directly from TMDL](from-tmdl.md). [Reports](../reports/index.md) covers their native deployment and bindings.
