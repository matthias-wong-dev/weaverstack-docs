# Development and production Reports

Use the same native Report and model in both workspaces. The selected workspace configuration changes their physical names and the Report's deployed model binding; it does not change their logical names or authored files.

Continue from [Deploy a native Report](deploy.md) in the same `parcel` project. If you are starting here, that page generates and deploys the pair. Keep your model overlays and source bindings.

## Select the two destinations

Create `workspace-dev.yml` and `workspace-prod.yml` for two existing disposable workspaces using the minimal configurations below. These inline-model destinations need no source workload. For an estate with Lakehouse or Warehouse items, copy the working configuration instead, retain its catalogue, runtime and source bindings, and change only the intended destinations. A production-labelled example is not a reason to use a real production workspace.

```yaml title="workspace-dev.yml"
workspace: Parcel BI Development
targets:
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
```

```yaml title="workspace-prod.yml"
workspace: Parcel BI Production
targets:
  SemanticModel/Parcel: Parcel
  Report/Parcel: Parcel_Report
```

`SemanticModel/Parcel` and `Report/Parcel` remain the logical items in both files. The Report's native `definition.pbir` still contains the [same `byPath`](deploy.md#start-with-the-linked-pair) to `../Parcel.SemanticModel`.

## Build and check each binding

Use an identity with model/Report create or update and readback rights in each workspace. Build updates existing selected items, so choose names you own.

```bash
weaver check .
weaver build . --item SemanticModel/Parcel --item Report/Parcel --workspace-config workspace-dev.yml
weaver build . --item SemanticModel/Parcel --item Report/Parcel --workspace-config workspace-prod.yml
```

If the development pair is already deployed, only the production Build is new work. Both commands select the linked model with the Report, as required for this catalogue-free project.

Check each Report's actual service binding, including the workspace, not just the displayed item names:

| Configuration | Workspace | Report | Linked semantic model |
| --- | --- | --- | --- |
| `workspace-dev.yml` | Parcel BI Development | `Parcel_Report_Dev` | `Parcel_Dev` |
| `workspace-prod.yml` | Parcel BI Production | `Parcel_Report` | `Parcel` |

In each workspace’s **lineage view**, follow the deployed Report’s semantic-model link. Confirm both its name and workspace against the table above. The production Report must link to the production model, not to the development one. The source `byPath` remains unchanged.

For a viewing check, refresh each model with refresh permission, then open each Report with view/query permission:

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-prod.yml
```

Both Delivery Count cards should show **2**. Model refresh and Report rendering are separate checks from Build and binding; there is no Report Load or Test.

An unrelated authored `byConnection` with no local model association stays as authored. Weaver does not reverse-map that external connection to a development or production model. The linked-pair behaviour above applies to the local association; [Report binding rules](../reference/power-bi/requirements-and-compatibility.md#report-binding) also describe same-name model precedence and the catalogue-backed Report-only case.

The Report now follows its model into each workspace without a source edit. When you also need to move its Lakehouse or Warehouse sources, use [workspace and environment mappings](../estate/environments.md) for the whole project. Destination names alone do not change source expressions or credentials. For changes to the model itself, return to [native TMDL and overlays](../semantic-models/native-tmdl.md).

## Remove only the example items

If you created disposable pairs for this exercise, delete their Reports before their models. Keep both workspaces and any pre-existing items; if you updated an existing item, retain its original definition rather than treating deletion as cleanup.
