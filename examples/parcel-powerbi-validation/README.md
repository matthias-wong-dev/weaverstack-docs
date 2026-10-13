# Validate the delivery count

**Weaver source target:** `74b4d15ee65ed2740593af1f4d459771b801b132`. Use a Weaver build containing these interfaces. The older PyPI `0.9.0` package is not the acceptance target.

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

Copy the supplied complete failing overlay into the model's optional overlay path:

```bash
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

The overlay sets Delivery Count to -1. Expect a `failed` node with one violating row, `DeliveryCount = -1`, not an execution error. The CLI exits 1 for a failed finding or an invalid validation, and 0 for a passing run. Inspect the node outcome to distinguish a violated Assumption from a query that could not run. The Python API returns the validation report rather than turning a finding into a strict-mode exception.

Remove only the overlay you just copied and redeploy:

```bash
rm PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver test SemanticModel/Parcel --name 'Parcel[.]PositiveDeliveryCount' --source . --workspace-config workspace-dev.yml
```

Expect `passed` again. `expected-results.json` separates empty pass rows, deliberate violation rows and the error case. None of the supplied offline results is a live DAX execution.

## Cleanup

In the service, delete only the model and Report names listed in this fixture's chosen configuration, and only if you created them in your disposable workspace. Delete Reports before their model. Do not delete an existing workspace or another project's items. No Wipe is needed. Keep any original definitions if you chose to update existing items instead of creating new ones.
