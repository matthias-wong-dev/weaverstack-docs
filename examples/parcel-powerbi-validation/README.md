# Validate the delivery count

Install Weaver from PyPI using the [installation guide](../../docs/getting-started/installation.md).

## Journey checkpoint

This is the direct-entry snapshot for [Validate a semantic model](../../docs/semantic-models/validation.md). Continuing readers add only its DAX file to the already deployed native Parcel model; keep the existing foreign-key overlay and workspace configuration. The snapshot itself has no initial overlay. Warehouse-backed reconciliation continues the separate [managed-source checkpoint](../../docs/semantic-models/managed-sources.md), not this inline model.

## Before you run

Use existing disposable development and production-labelled workspaces, with the names in `workspace-dev.yml` and `workspace-prod.yml`, or edit those two files to your own disposable names. The production-labelled file is not permission to use a production workspace. You need the appropriate Power BI service licence, item creation/update rights, model refresh rights and permission to view the Report. Sign in through Weaver's supported authentication route. No catalogue, Lakehouse, Spark session, Fabric Environment or external data credentials are needed for these inline Import partitions.

`PowerBI/Parcel/Parcel.pbip` opens the native project. Its model contains three parcel rows, two depots and a many-to-one relationship. The Report has a visible Delivery Count card. Refresh should show **2**.

## Check and deploy

Run from this example directory, not its parent:

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Check validates project discovery and definitions locally. Build and Load contact the service. In the development workspace, verify `Parcel_Dev` and `Parcel_Report_Dev` exist, the Report is connected to that model, and the card displays 2 after refresh. A zero exit status is not a visual or binding check.

## Run the Assumption from source

The model owns `PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax`. An Assumption returns violating rows, not a single boolean result. This query returns no rows when Delivery Count is positive.

You need DAX query access to the model (Read and Build permissions), and the tenant's Execute Queries setting must permit your identity. A query permission or execution error produces an **invalid** validation node in source/file mode, not a passing result.

```bash
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

The validation node should be `passed`, with zero violations. Source mode does not write catalogue Test history.

## Deliberately fail, then correct

Save any existing overlay before changing the measure. Use an unused backup filename and keep the same shell through restoration:

```bash
test ! -e Parcel.tmdl.saved || exit 1
had_overlay=false
if test -f PowerBI/Parcel/Parcel.tmdl; then
  had_overlay=true
  cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
fi
```

Set Delivery Count to `-1` in `PowerBI/Parcel/Parcel.tmdl`, using `failure/Parcel.tmdl` as the declaration. Retain all other overlay declarations. Edit an existing Delivery/measure declaration rather than adding a duplicate. With the native rule-only overlay, add the failure's Delivery section below the existing rule; with this snapshot's absent overlay, create the complete failure file.

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

The overlay sets Delivery Count to -1. Expect a `failed` node with one violating row, `DeliveryCount = -1`, not an execution error. The CLI exits 1 for a failed finding or an invalid validation, and 0 for a passing run. Inspect the node outcome to distinguish a violated Assumption from a query that could not run. The Python API returns the validation report rather than turning a finding into a strict-mode exception.

Restore the original overlay even if a command failed. A deliberately failed Test exits 1; do not chain restoration behind `&&` or automatic exit-on-error:

```bash
if test "$had_overlay" = true; then
  mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
else
  rm PowerBI/Parcel/Parcel.tmdl
fi
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect `passed` again. `expected-results.json` separates empty pass rows, deliberate violation rows and the error case. None of the supplied offline results is a live DAX execution.

## Cleanup

In the service, delete only the model and Report names listed in this fixture's chosen configuration, and only if you created them in your disposable workspace. Delete Reports before their model. Do not delete an existing workspace or another project's items. No Wipe is needed. Keep any original definitions if you chose to update existing items instead of creating new ones.
