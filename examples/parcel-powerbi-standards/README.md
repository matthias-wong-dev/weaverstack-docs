# Apply model standards without changing the native project

**Weaver source target:** `74b4d15ee65ed2740593af1f4d459771b801b132`. Use a Weaver build containing these interfaces. The older PyPI `0.9.0` package is not the acceptance target.

## Journey checkpoint

This complete direct-entry snapshot finishes [shared modelling standards](../../docs/semantic-models/shared-policy.md) and [custom annotations](../../docs/semantic-models/custom-annotations.md). It preserves the native Parcel model’s Delivery, Depot, partitions and relationship. Continuing readers add policy first, then the handler and its measure annotation; they keep their existing project and configuration. The shared foreign-key policy variation is shown on the policy page; this snapshot retains that rule locally.

## Before you run

Use existing disposable development and production-labelled workspaces, with the names in `workspace-dev.yml` and `workspace-prod.yml`, or edit those two files to your own disposable names. The production-labelled file is not permission to use a production workspace. You need the appropriate Power BI service licence, item creation/update rights, model refresh rights and permission to view the Report. Sign in through Weaver's supported authentication route. No catalogue, Lakehouse, Spark session, Fabric Environment or external data credentials are needed for these inline Import partitions.

`PowerBI/Parcel/Parcel.pbip` opens the native project. Its model contains three parcel rows, two depots and a many-to-one relationship. The Report has a visible Delivery Count card. Refresh should show **2**.


## Read the three rules

- `PowerBI/Parcel/Parcel.tmdl` applies `Weaver.AutoHideForeignKeys` to the actual Delivery → Depot relationship. The authored many-side `Delivery[DepotId]` is visible; its effective native definition is hidden. `Depot[DepotId]` and unrelated columns stay visible.
- `PowerBI/policy.tmdl` adds a native `Display` calculation group with a `Current = SELECTEDMEASURE()` item, discourages implicit measures, and formats measures. The same-name overlay overrides the policy's Delivery Count format with `0 "deliveries"`. `InternalCost` keeps the policy format `#,##0.00`.
- `PowerBI/annotations/Parcel__DisplayFolder.py` declares one `Annotation` subclass. `Parcel.DisplayFolder` at measure scope sets the named measure's native `displayFolder` property to `Parcel metrics`.

**Annotation files are trusted local Python.** Weaver executes them during parsing/compilation; do not Check or Build an untrusted project. They are not sandboxed metadata. This subclass runs in the default `post_schema` phase and reports an empty value with the declaration's file and line. Power BI Desktop itself does not execute Weaver annotations.

## Deploy and inspect the native result

From this directory:

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Inspect the deployed model through a supported native model-definition tool, or the service's Get Definition API. Verify the many-side hide, calculation group/item, the two measure formats and display folder recorded in `expected-results.json`. Confirm the Delivery and Depot partitions and relationship still exist. In the Report, the card should display `2 deliveries`.

This is inspection of a deployed native model, not a Weaver compiled-TMDL export. The native project files remain unchanged by compilation; they still contain the rule declarations rather than the transformed many-side property.

## See a custom-rule diagnostic

Back up the normal overlay, then replace it with the supplied empty-value case:

```bash
cp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved
cp failure/Parcel.tmdl PowerBI/Parcel/Parcel.tmdl
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
mv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl
```

Compilation refuses the empty folder with a file/line diagnostic. Restore the normal overlay even if Build fails. The shared calculation group is native TMDL, not an invented built-in annotation.

## Cleanup

In the service, delete only the model and Report names listed in this fixture's chosen configuration, and only if you created them in your disposable workspace. Delete Reports before their model. Do not delete an existing workspace or another project's items. No Wipe is needed. Keep any original definitions if you chose to update existing items instead of creating new ones.
