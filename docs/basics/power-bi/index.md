# Power BI

Start with a native PBIP/TMDL model and its Report. Standalone deployment, model refresh, DAX Assumptions, shared standards and composition do not generally require a Weaver catalogue.

The Power BI service still needs an appropriate licence, workspace access and permissions. "Power BI alone" does not mean free Desktop alone, no tenant or that Direct Lake loses its platform requirements.

## Deploy the project you have

[Deploy an existing PBIP](deploy-pbip.md) uses a small complete Import/calculated-data example with no external source credentials. Then [choose development and production targets](environments.md) through configuration without editing authored model/Report files.

## Add one useful check or convention

[Validate a semantic model](validate.md) adds a DAX Assumption that reports violating rows. [Apply a modelling rule](modelling-rule.md) uses one native annotation to hide many-side relationship keys.

## Connect to Fabric when needed

[Connect a model to a Fabric estate](fabric-integration.md) adds managed-source lineage, installed refresh ordering and persisted results. DAX-to-SQL comparison still needs its supported Warehouse/Lakehouse source and access even when it runs in file mode.

Optional [shared policy](../../advanced/power-bi/shared-policy.md), [custom annotations](../../advanced/power-bi/custom-annotations.md) and [model variants](../../advanced/power-bi/model-composition.md) have separate task pages. [Power BI reference](../../reference/power-bi/index.md) owns complete layout, merge, annotation, validation and compatibility rules.
