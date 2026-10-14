# Semantic models

Keep the native PBIP and TMDL you already author. Weaver deploys the model and applies optional conventions without rewriting those source files.

[Deploy a native model](native-tmdl.md), then add one overlay to hide relationship foreign keys. If the convention belongs on several models, [share it as policy](shared-policy.md) instead of repeating it.

[Connect a managed Fabric source](managed-sources.md) when the model needs Warehouse or Lakehouse data; [validate the model](validation.md) when a successful refresh is not enough to establish the right number.

Go further with [custom annotations](custom-annotations.md), [model variants](composition.md) or [authoring directly from TMDL](from-tmdl.md). [Reports](../reports/index.md) covers their native deployment and bindings.
