# The development cycle

Edit a working definition, check it, inspect the Build preview, install the change, catch up data and validate the result. Use the same configuration throughout so each report describes the estate you changed.

```text
edit → check → Build preview → Build → Load → Test → Health → repeat
```

Keep the project and configuration you just inspected. The leading commands continue [Landing → Dispatch](connected-items.md) with `workspace-development.yml`, as selected on the mapping and Health pages. Edit a Landing declaration while leaving its logical names and Dispatch connection intact. Use the [connection task](connected-items.md) if those items are not yet installed.

For another source-data estate, select its actual changed items in the same loop. A Warehouse-only reader can use `--item Warehouse/Operations` with the [StatusEvent project](../warehouse/tests.md). If you chose the managed Parcel variation, stay with it and use [the model-inclusive loop](#include-semantic-models-and-reports) below, rather than returning to either source-data example.

## Edit and iterate

After editing the source, check it locally and preview the intended installed change:

```bash
weaver check .
weaver build . --item Lakehouse/Landing --item Warehouse/Dispatch --dry-run --workspace-config workspace-development.yml
```

Check catches declaration errors without contacting Fabric. Build preview reads existing targets and shows selected work and destructive consequences without installing or changing catalogue/runtime state. It is not a retained executable bundle, does not prove runtime compatibility, and cannot provision missing selected Power BI targets. Use ordinary Build for first deployment.

If the preview is the intended change, install and operate that selection:

```bash
weaver build . --item Lakehouse/Landing --item Warehouse/Dispatch --workspace-config workspace-development.yml
weaver load --stale --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Build reconciles source against installed state, including changed definitions and affected descendants inside its selected items. Changed loadable work begins with non-Green current state. `load --stale` selects installed loadables needing work; it leaves omitted Green producers alone. Test runs installed validations, then Health shows Load, Tests and Build together.

Load and catalogue-mode Test use installed definitions, not your edited source files. A data-only source change needs Load, not another Build; a declaration change must cross Build first. Source/file Tests are an alternative authoring check and do not write installed Test history.

Use an item-wide run by default. Plain named Load does not add or order dependencies. [Run part of an estate](selective-runs.md) teaches deliberate seed expansion and a preview when item-wide work is too broad. Completed work is not rolled back after a later failure; follow [Recovery](recovery.md) against the state that remains.

## Include semantic models and Reports

For the [managed-source Parcel project](../semantic-models/managed-sources.md), keep its Operations Delivery source, model and Report in one project with `workspace-dev.yml`. Its model reads Operations Delivery; keep that source and its existing connection.

Build source-data definitions first, then changed model/Report definitions separately:

```bash
weaver check .
weaver build . --item Warehouse/Operations --dry-run --workspace-config workspace-dev.yml
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --dry-run --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load --stale --workspace-config workspace-dev.yml
weaver test --workspace-config workspace-dev.yml
weaver health --workspace-config workspace-dev.yml
```

This loop assumes the project’s model and Report already exist, its native source mapping is configured and its supported service connection is available. Preview each changed Build before applying it. `--bind-data-sources` requests binding to an existing connection; it creates no credentials. Build deploys the model before its linked Report. Estate Load coordinates selected source data and model refreshes; a source change can make the model stale even if its definition did not change. DAX validations are part of Test. **Reports have only a Build/deployment lifecycle, not Load or Test.** Inspect their actual binding and rendering through the [Report task](../reports/deploy.md).

## Optional: establish a mirrored development baseline

Once the ordinary loop works, [develop using Mirror](mirror.md) if development should borrow existing source data rather than load every unchanged object locally. It requires existing source and destination items in the same workspace and empties the destination catalogue plus selected targets. Re-mirror only for a fresh baseline, not for each edit.

[Run, test and inspect the estate](operate.md) is the installed-state path when no source change needs Build. [Build, Load and Test](../core-concepts/build-load-and-test.md) explains the operation boundaries behind both paths.
