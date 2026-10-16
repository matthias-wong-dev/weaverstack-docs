# Compose two independently deployed model variants

Install Weaver from PyPI using the [installation guide](../../docs/getting-started/installation.md).

## Journey checkpoint

[Compose two model variants](../../docs/semantic-models/composition.md) deliberately changes the single Parcel output into a local ParcelBase foundation and two audience outputs. This complete snapshot supports direct entry; it is not a silent rename of the native model checkpoint. Delivery/Depot remain the foundation, while each output has its own Report and validation. Only the two outputs deploy; the base remains source.

## Before you run

Use two existing disposable Power BI workspaces and edit the two configuration files to their names. You need model/Report creation or update rights, refresh and view permissions, the appropriate service licence, and DAX query Read/Build access. This fixture does not require a catalogue, Fabric Environment or external source credentials.

`ParcelBase.SemanticModel` is the complete native source foundation, with inline Import data and a relationship. `ParcelOperations.tmdl` and `ParcelExecutive.tmdl` each declare `Weaver.BaseSemanticModels = ParcelBase`. Their small native model packages provide output properties; Weaver composes the effective definitions before deployment. The authored output project is not a precompiled, independently populated Desktop model.

Operations adds Delivery Rate. Executive excludes the InternalCosts **table** and overrides Delivery Count formatting. Each has its own `assumptions/<Model>/Parcel.PositiveDeliveryCount.dax` and a full Report with a Delivery Count card. The base has neither a Report nor a copied validation. Excluding objects is not RLS/OLS or an access-control policy.

## Select only the outputs

Run from this directory:

```bash
weaver check .
weaver build . --item SemanticModel/ParcelOperations --item Report/ParcelOperations --item SemanticModel/ParcelExecutive --item Report/ParcelExecutive --workspace-config workspace-dev.yml
weaver load SemanticModel/ParcelOperations SemanticModel/ParcelExecutive --workspace-config workspace-dev.yml
weaver test SemanticModel/ParcelOperations SemanticModel/ParcelExecutive --source . --workspace-config workspace-dev.yml
```

Do not select `PowerBI/Parcel`: it includes the base in the requested selection. These configurations deliberately omit a base target, so that broader request refuses before deployment. Keep the explicit four-item selection above. Reusing the base source does not require deploying a physical `ParcelBase` model. Verify the four configured output items exist, each Report binds to its own output model, both cards show 2, both model-owned Assumptions pass, and no new `ParcelBase` item was created.

Inspect the deployed native definitions: Operations contains Delivery Rate and InternalCosts; Executive has no InternalCosts but retains Delivery Count and the relationship. `expected-results.json` lists the intended additions, exclusions and outputs. To deploy the same outputs to the second disposable workspace, repeat the explicit four-item Build command with `workspace-prod.yml`, then refresh the two models with that configuration.

## Deliberate composition failure

```bash
cp PowerBI/Parcel/ParcelExecutive.tmdl ParcelExecutive.tmdl.saved
cp failure/ParcelExecutive.tmdl PowerBI/Parcel/ParcelExecutive.tmdl
weaver check .
mv ParcelExecutive.tmdl.saved PowerBI/Parcel/ParcelExecutive.tmdl
weaver check .
```

The first Check must refuse `MissingBase` in the local project scope. Restore the overlay before proceeding.

## Cleanup

Delete only the two Reports and two output models named in the chosen configuration, and only if this fixture created them in your disposable workspace. Delete Reports first. Do not delete a pre-existing base or workspace. No unscoped Wipe is needed.
