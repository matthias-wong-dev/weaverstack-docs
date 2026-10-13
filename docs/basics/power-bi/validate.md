# Validate a semantic model

Add a DAX Assumption that returns violating rows. An empty result passes; a returned row is a finding, not a query error.

## Before you start

Use the independent [validation project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi-validation). Work from its directory, edit `workspace-dev.yml` to your disposable workspace, and use the [ordinary deployment prerequisites](deploy-pbip.md).

You also need model Read and Build permissions for DAX queries and an identity allowed by the tenant's Execute Queries setting. Do not change tenant settings simply to run the example. This catalogue-free route records no installed Test history.

## 1. Deploy and refresh

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

The Delivery Count card should show 2. The model owns `PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax`:

```dax
/*
Assumption ID: Parcel.PositiveDeliveryCount
Description: The delivery count is positive.
*/
EVALUATE FILTER(ROW("DeliveryCount", [Delivery Count]), [DeliveryCount] <= 0)
```

The filename, metadata ID and `assumptions` directory agree. The model name in the path is the local logical name, not `Parcel_Dev`.

## 2. Run the source Assumption

```bash
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect a `passed` validation node with zero violations and CLI exit 0. `--source .` reads the edited validation file; no Build is needed merely to change that query. Without a catalogue this uses source/file mode. With a configured catalogue, add `--file` when you deliberately want that mode rather than installed validation recording.

## 3. Produce a finding

The supplied `failure/Parcel.tmdl` is a complete optional overlay:

```tmdl
table Delivery
	measure 'Delivery Count' = -1
```

Copy it into the model's overlay path and deploy the changed measure:

```bash
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect `failed` with one violating row, `DeliveryCount = -1`, and CLI exit 1. Inspect the returned diagnostics. A query/permission failure instead produces an `invalid` node and also exits 1; it is neither a finding nor a pass. Python returns the validation report, so inspect its outcomes rather than adding an obsolete `strict=` option.

## 4. Correct it

Remove only the overlay copied in the previous step, then redeploy and rerun:

```bash
rm PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect `passed` again. For cleanup, delete only this example's newly created Report/model, Reports first.

## Related tasks

- [Compare DAX with managed-source SQL](fabric-integration.md).
- [Look up DAX validation metadata and diagnostics](../../reference/power-bi/validations.md).
- [Recover failed work](../recover-failed-work.md).
