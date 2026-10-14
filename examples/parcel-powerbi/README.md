# Deploy a native parcel Power BI project

**Weaver source target:** `74b4d15ee65ed2740593af1f4d459771b801b132`. Use a Weaver build containing these interfaces. The older PyPI `0.9.0` package is not the acceptance target.

## Before you run

Use existing disposable development and production-labelled workspaces, with the names in `workspace-dev.yml` and `workspace-prod.yml`, or edit those two files to your own disposable names. The production-labelled file is not permission to use a production workspace. You need the appropriate Power BI service licence, item creation/update rights, model refresh rights and permission to view the Report. Sign in through Weaver's supported authentication route. No catalogue, Lakehouse, Spark session, Fabric Environment or external data credentials are needed for these inline Import partitions.

`PowerBI/Parcel/Parcel.pbip` opens the native project. Its model contains three parcel rows, two depots and a many-to-one relationship. The Report has a visible Delivery Count card. Refresh should show **2**.

This is the complete direct-entry snapshot for [native Report deployment](../../docs/reports/deploy.md) and [development/production binding](../../docs/reports/environments.md): the local model, Report and both configurations are included. A continuing reader keeps this project and any model overlay already added; the environment task changes only the selected configuration. No modelling tutorial is required to deploy the Report. Build is the Report checkpoint; the model refresh below is a separate viewing check. To compare authored bytes across both destinations, record the hash baseline in the next section **before the first Build**.

## Check and deploy

Run from this example directory, not its parent:

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Check validates project discovery and definitions locally. Build and Load contact the service. In the development workspace, verify `Parcel_Dev` and `Parcel_Report_Dev` exist, the Report is connected to that model, and the card displays 2 after refresh. A zero exit status is not a visual or binding check.

## Reuse the source in another environment

Before deployment, record the authored project hashes from this directory:

```bash
python -c 'import hashlib,json; from pathlib import Path; r=Path("PowerBI"); Path("authored-hashes-before.json").write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(r.rglob("*")) if p.is_file()},indent=2))'
```

After the development Build/refresh above, deploy with the second configuration:

```bash
weaver build . --item PowerBI/Parcel --workspace-config workspace-prod.yml
weaver load SemanticModel/Parcel --workspace-config workspace-prod.yml
python -c 'import hashlib,json; from pathlib import Path; r=Path("PowerBI"); before=json.loads(Path("authored-hashes-before.json").read_text()); after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(r.rglob("*")) if p.is_file()}; assert before==after; print("Authored PowerBI bytes unchanged")'
```

Verify `Parcel` and `Parcel_Report` in the second disposable workspace, with that Report bound to `Parcel`, not `Parcel_Dev`. These mappings change destination names and Report binding; they do not configure source credentials. Both partitions use inline data, so there is no source connection to change.

`expected-results.json` records the logical models, Report association and expected count. Local parsing does not prove service acceptance, refresh, licence eligibility or Report rendering.

## Cleanup

In the service, delete only the model and Report names listed in this fixture's chosen configuration, and only if you created them in your disposable workspace. Delete Reports before their model. Do not delete an existing workspace or another project's items. No Wipe is needed. Keep any original definitions if you chose to update existing items instead of creating new ones.
