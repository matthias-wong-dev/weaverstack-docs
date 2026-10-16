# Deploy a native Report

Keep your native `.Report` beside its semantic model. Build deploys the model first, then binds the Report to that deployed model without rewriting the local `definition.pbir`.

## Start with the linked pair

Continue the [native Parcel model](../semantic-models/native-tmdl.md) in the same project, keeping its overlays. Initialise has already written its linked Report. If you are starting here, [install Weaver](../getting-started/installation.md) and generate the pair:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --semantic-model Parcel \
  --example Parcel
cd parcel
```

Open `PowerBI/Parcel/Parcel.pbip` in Desktop to inspect the Report. Its association is authored in `PowerBI/Parcel/Parcel.Report/definition.pbir`:

<!-- initialise:PowerBI/Parcel/Parcel.Report/definition.pbir -->
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../Parcel.SemanticModel"
    }
  }
}
```
<!-- /initialise -->

The path is relative to the `.Report` directory. Keep the complete native Report payload as well as this file; the example includes its page and card definitions. [Native project layout](../reference/power-bi/project-layout.md#report-discovery-and-association) describes discovery for your own project.

This starts in [Power BI-only mode, without a Catalogue](../semantic-models/index.md#power-bi-only-without-a-catalogue). Native-only Initialise writes the linked pair, workspace configuration and supporting local project files; it creates no Catalogue Warehouse or Fabric Environment by default. This inline model and Report need no Lakehouse, Warehouse workload or Spark runtime. Use an existing, suitably licensed Power BI service workspace with the permissions described below.

## Choose the destination and Build

Use the generated `workspace-config.yml`. It already binds `SemanticModel/Parcel` and `Report/Parcel` to their physical items in Parcel Development. Keep any Lakehouse or Warehouse bindings in that file.

Build can create missing selected models and Reports or update existing ones. Choose item names you own. Sign in with an identity allowed to create/update and read back both items; the service licence and capacity must support the model mode. [Service requirements](../reference/power-bi/requirements-and-compatibility.md#runtime-and-service-access) give the platform boundaries.

Run from the example directory:

```bash
weaver check
weaver build --item SemanticModel/Parcel --item Report/Parcel
```

<!-- cli-capture: {"id": "85-native-annotation-and-report-build", "title": "Build · deploy and verify the linked pair"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · deploy and verify the linked pair">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel
  Report/Parcel


Build

    Create Report/Parcel                                                                                  20.6s
  Create Power BI items                                                                                   20.6s
  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel                                                                           0.0s
    Resolve Report/Parcel                                                                                  0.0s
  Read target inventories                                                                                  0.2s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1
  Report/Parcel
    changed                 1
    selected for build      1

→   SemanticModel/Parcel · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Deploy semantic definitions · 1 action                                         21.0s</span>
→   SemanticModel/Parcel, Report/Parcel · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel, Report/Parcel · Verify deployed semantic definitions · 1 action                 20.5s</span>
→   Report/Parcel · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓   Report/Parcel · Deploy Report definitions · 1 action                                                  20.4s</span>
→   Report/Parcel · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓   Report/Parcel · Verify deployed Report definitions · 1 action                                         20.9s</span>
  Install                                                                                                 1m22s
<span class="terminal-status-green">✓ Build                                                                                                   1m43s</span>

Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  ca0aeddd18fafaf4a715693285d9d933b0dd6b057bb7feb7588e13780e3e8f21
</code></pre>
</figure>
<!-- /cli-capture -->

Check validates local definitions, not service access. These two selectors deploy the inline model and its linked Report without selecting any additional source-backed models. Build deploys and verifies `Parcel` before deploying the Parcel Report, then verifies the Report definition and its actual model binding. The deployed payload uses the resolved service workspace/model IDs; your authored `byPath` and native files stay unchanged.

Without a catalogue, a linked Report must include its local model in the same Build. In a catalogue-backed project, a Report-only Build can use an already certified installed model whose recorded binding matches the resolved destination and source requirements. See [Report binding](../reference/power-bi/requirements-and-compatibility.md#report-binding) before selecting only `Report/Parcel`.

## Inspect the Report

In the service workspace, find the Parcel Report and check that its linked model is `Parcel` in **Parcel Development**. Open the workspace’s **lineage view** and follow the Report’s model link. Confirm it points to the Parcel semantic model in this workspace, not a similarly named model in another destination.

To view the generated Report’s card after loading its inline data, refresh the **model** with an identity allowed to refresh it:

```bash
weaver load SemanticModel/Parcel
```

<!-- review-todo: report-rendering -->
!!! warning "TODO — check the rendered Parcel Delivery Count card"
    Open the deployed Report after the model Load and confirm its card shows 2. Deployment, the Report-to-model binding and the DAX value (2) are verified through the APIs; Report export is not available on the capture capacity and the service UI was not signed in.
<!-- /review-todo -->

With permission to view the Report and query its model, open the card: **Delivery Count should be 2**. Reports have no separate Load, Test or refresh operation; data refresh and validation belong to the model.

The development Report now has a destination-specific model binding while the source still names `../Parcel.SemanticModel`. [Use the same Report in development and production](environments.md) by selecting a second configuration, not editing that path.
