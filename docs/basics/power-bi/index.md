# Semantic models and Reports

Native semantic models and Reports belong in the same project as their Lakehouse and Warehouse sources. Build deploys the definitions, Load refreshes models, Test evaluates DAX validations, and Health includes their recorded state in the managed estate report.

The ordinary authoring flow is in [Basics](../index.md), alongside Lakehouse and Warehouse tasks:

- [Deploy semantic models and Reports with PBIP](deploy-pbip.md).
- [Connect a semantic model to source data](fabric-integration.md).
- [Choose environment targets](environments.md).
- [Validate a semantic model](validate.md).
- [Hide relationship foreign keys](modelling-rule.md).

For shared standards and model variants, use the [Semantic models tasks in Advanced](../../advanced/index.md#semantic-models). Exact native layout, TMDL, annotations and DAX rules belong in [Reference](../../reference/power-bi/index.md).

Model and Report deployment can also run without a catalogue in an existing Power BI service workspace. The deployment task supplies that smaller setup; licence, model-mode and permission requirements are in the [compatibility reference](../../reference/power-bi/requirements-and-compatibility.md).
