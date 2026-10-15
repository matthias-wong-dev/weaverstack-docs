# Deploy a native semantic model

Deploy the PBIP/TMDL you already author, then hide relationship foreign keys with one built-in rule. The native files stay unchanged; Weaver applies the rule to the model definition it deploys.

## Native files first

A PBIP project contains the model’s native TMDL and its Report definitions. You can also author a model directly in a named TMDL file; [native project layout](../reference/power-bi/project-layout.md) describes both forms. Weaver does not require you to add an annotation before it can deploy the model.

## Before you start

[Install Weaver](../getting-started/installation.md). Use an existing Power BI service workspace and an identity allowed to create/update, read and refresh the model. Its licence and capacity must support the model mode.

The example contains inline Import data and works in an existing standalone Power BI workspace. No catalogue or source Warehouse is needed. [Managed Fabric sources](managed-sources.md) adds source coordination later.

Download and extract the [complete parcel project](../assets/examples/parcel-powerbi.zip) and work from `examples/parcel-powerbi`. `PowerBI/Parcel/Parcel.pbip` opens the native project. Its model has three parcel rows, two depots, a relationship and a Delivery Count measure. Its Report has a Delivery Count card.

Save the `parcel-powerbi.zip` download in an empty working directory, then extract its repository-relative paths and enter the project:

```bash
python -m zipfile -e parcel-powerbi.zip .
cd examples/parcel-powerbi
```

For an existing Fabric project, copy the `PowerBI/` directory and add the shown targets to its configuration, retaining the workspace and catalogue settings.

## 1. Choose the destination

Edit `workspace-dev.yml` to name your existing disposable workspace:

```yaml
workspace: Parcel BI Development
targets:
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
```

Logical names stay in the project; this file chooses physical names. Build may create missing selected models and Reports, or update existing ones. Choose names you own. Do not run `weaver initialise` for this route: it also provisions a catalogue Warehouse and Fabric Environment.

## 2. Check the project

Before the first Build, record hashes of the authored native model files. Run from the example project root; the same-name Weaver overlay is outside this directory:

```bash
python -c 'import hashlib,json; from pathlib import Path; r=Path("PowerBI/Parcel/Parcel.SemanticModel"); Path("native-source.sha256.json").write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(r.rglob("*")) if p.is_file()}))'
```

```bash
weaver check .
```

Check reads local declarations and definitions. It does not execute M/DAX, deploy items or test service permissions. In your own project, use the supported `PowerBI/<project>/` layout with native `.SemanticModel` and `.Report` definitions. A PBIP entrypoint is optional for discovery.

## 3. Deploy the native model

```bash
weaver build . --item SemanticModel/Parcel --workspace-config workspace-dev.yml
```

This selects **only the semantic model**. Build deploys and verifies `Parcel_Dev`; the Report stays local until you [deploy the linked Report](../reports/deploy.md).

## 4. Refresh and inspect the model

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Find `Parcel_Dev` in the workspace. Save the following as `query-model.py` beside `workspace-dev.yml`, then run `python query-model.py` from that directory. It uses the installed Weaver package and the same authentication and workspace configuration as the CLI:

```python title="query-model.py"
import weaver

with weaver.session(workspace_config="workspace-dev.yml") as opened:
    deployed = opened.semantic_model("Parcel_Dev")
    rows = deployed.query_dax('EVALUATE ROW("DeliveryCount", [Delivery Count])')
    print(rows)
```

The returned row should have **DeliveryCount = 2**. This calls the Power BI Execute Queries API: the identity needs model Read and Build permissions and must be allowed by the tenant's Execute Queries setting. Use existing permissions; do not change tenant settings for the exercise. This query checks the deployed model, not a locally opened PBIP file.

You now have a deployed native model. Add the rule below to change its field list without editing the native columns.

<span id="hide-relationship-foreign-keys"></span>

## AutoHideForeignKeys: hide relationship foreign keys

### Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model instead of declaring another one.

### Deploy and inspect

```bash
weaver check .
weaver build . --item SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
```

Read the deployed definition through Fabric's Get Definition API using the same Session. Save this as `inspect-model.py` beside the configuration and run `python inspect-model.py`:

```python title="inspect-model.py"
import base64
import hashlib
import json
from pathlib import Path

import weaver
from weaver.semantic_models import TmdlDefinition

with weaver.session(workspace_config="workspace-dev.yml") as opened:
    definition = opened.semantic_model("Parcel_Dev").get_definition(format="TMDL")
parts = {
    part["path"]: base64.b64decode(part["payload"], validate=True)
    for part in definition["parts"]
    if part["payloadType"] == "InlineBase64"
}
model = TmdlDefinition(parts).model
assert model.tables["Delivery"].columns["DepotId"].isHidden is True
assert model.tables["Depot"].columns["DepotId"].isHidden is not True
relationship = model.relationships["Delivery_Depot"]
assert relationship.fromColumn == "Delivery.DepotId"
assert relationship.toColumn == "Depot.DepotId"
assert relationship.fromCardinality == "many"
assert relationship.toCardinality == "one"
assert relationship.crossFilteringBehavior == "oneDirection"
root = Path("PowerBI/Parcel/Parcel.SemanticModel")
authored = TmdlDefinition({
    path.relative_to(root).as_posix(): path.read_bytes()
    for path in root.rglob("*") if path.is_file()
}).model
for name in ("Delivery", "Depot"):
    partition = model.tables[name].partitions[name]
    assert partition.mode == "import"
    assert partition.source == authored.tables[name].partitions[name].source
after = {
    str(path): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(root.rglob("*")) if path.is_file()
}
assert after == json.loads(Path("native-source.sha256.json").read_text())
print("Visibility, relationship, Import partitions and authored file hashes checked")
```

A successful run verifies the deployed many-side key is hidden, the one-side key is visible, the relationship and both Import partitions remain, and all authored native model bytes match the pre-Build baseline. An omitted native `isHidden` property also means visible. Get Definition needs model-definition read access; Build already uses definition readback. These are read-only inspection calls, not a Report rendering test.

The local native column is not rewritten. Desktop does not execute Weaver annotations; the visibility change is applied to the deployment definition. Hidden columns are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild from source. A declaration of `false` is a no-op, not an instruction to undo an independently authored native hide.

<details markdown="1">
<summary>Inspect the native relationship</summary>

### Inspect the relationship the rule uses

The native `definition/relationships.tmdl` relates the many-side Delivery key to Depot. Both authored columns are visible:

```tmdl
relationship Delivery_Depot
	fromColumn: Delivery.DepotId
	toColumn: Depot.DepotId
	fromCardinality: many
	toCardinality: one
	crossFilteringBehavior: oneDirection
```

The rule hides the many-side key from the field list, not the one-side key.

</details>

## Carry the convention to the next model

You now have the native Parcel model and one local rule, with Delivery and Depot unchanged apart from field visibility. When that convention belongs on several models, [share it in `PowerBI/policy.tmdl`](shared-policy.md). The next task keeps this model and adds common formatting and a native calculation group; it does not ask you to start deployment again.

[Validate the model](validation.md) to check its number, or [connect a managed Fabric source](managed-sources.md) when Delivery comes from a Warehouse rather than inline data. [Weaver documents](../core-concepts/weaver-documents.md#native-models-overlays-and-annotations) explains where overlays fit beside normal native definitions.
