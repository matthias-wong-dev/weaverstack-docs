# Hide relationship foreign keys

Keep relationship keys available to the model without presenting every many-side key in the field list. One native annotation applies that convention.

Use a fresh copy of the [ordinary parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi) and its [deployment prerequisites](deploy-pbip.md). No shared policy or custom Python is needed.

## 1. Inspect the native relationship

The model relates `Delivery[DepotId]` on the many side to `Depot[DepotId]` on the one side. The authored columns are visible. A model without a relationship would give this rule nothing to hide.

## 2. Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model instead of declaring another one.

## 3. Deploy and inspect

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed native definition through a supported model-definition tool or the service's Get Definition API. `Delivery[DepotId]` should have `isHidden = true`; `Depot[DepotId]` and unrelated columns should stay visible. The relationship and partitions remain, and the Report still shows Delivery Count = 2.

The local native column is not rewritten. Desktop does not execute Weaver annotations; the visibility change is applied to the deployment definition. Hidden columns are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild from source. A declaration of `false` is a no-op, not an instruction to undo an independently authored native hide.

For cleanup, delete only this example's newly created Report/model, Reports first.

## Related tasks

- [Share native modelling standards](../../advanced/power-bi/shared-policy.md).
- [Look up all built-in annotations](../../reference/power-bi/annotations.md).
- [Understand source overlays](../../reference/power-bi/tmdl.md).
