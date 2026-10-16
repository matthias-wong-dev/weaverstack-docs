# Development and production Reports

Use the same native Report and model in both workspaces. The selected workspace configuration changes their physical names and the Report's deployed model binding; it does not change their logical names or authored files.

Continue from [Deploy a native Report](deploy.md) in the same `parcel` project. If you are starting here, that page generates and deploys the pair. Keep your model overlays and source bindings.

## Select the two destinations

Create `workspace-development.yml` and `workspace-production.yml` for two existing disposable workspaces. If you already have these files from the [estate pages](../estate/environments.md), add the two targets to each instead. These inline-model destinations need no source workload. For an estate with Lakehouse or Warehouse items, copy the working configuration instead, retain its catalogue, runtime and source bindings, and change only the intended destinations. A production-labelled example is not a reason to use a real production workspace.

```yaml title="workspace-development.yml"
workspace: Parcel Development
targets:
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
```

```yaml title="workspace-production.yml"
workspace: Parcel Production
targets:
  SemanticModel/Parcel: Parcel_Production
  Report/Parcel: Parcel_Report_Production
```

`SemanticModel/Parcel` and `Report/Parcel` remain the logical items in both files. The Report's native `definition.pbir` still contains the [same `byPath`](deploy.md#start-with-the-linked-pair) to `../Parcel.SemanticModel`.

## Build and check each binding

Use an identity with model/Report create or update and readback rights in each workspace. Build updates existing selected items, so choose names you own.

```bash
weaver check
weaver build --item SemanticModel/Parcel --item Report/Parcel --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "100-report-development-build", "title": "Build · development pair and binding"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · development pair and binding">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel → SemanticModel/Parcel_Dev
  Report/Parcel → Report/Parcel_Report_Dev


Build

  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel_Dev                                                                       0.0s
    Resolve Report/Parcel_Report_Dev                                                                       0.0s
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

→   SemanticModel/Parcel_Dev · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel_Dev · Deploy semantic definitions · 1 action                                     21.5s</span>
→   SemanticModel/Parcel_Dev, Report/Parcel_Report_Dev · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel_Dev, Report/Parcel_Report_Dev · Verify deployed semantic definitions · 1 action   20.5s</span>
→   Report/Parcel_Report_Dev · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓   Report/Parcel_Report_Dev · Deploy Report definitions · 1 action                                       20.4s</span>
→   Report/Parcel_Report_Dev · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓   Report/Parcel_Report_Dev · Verify deployed Report definitions · 1 action                              21.2s</span>
  Install                                                                                                 1m23s
<span class="terminal-status-green">✓ Build                                                                                                   1m23s</span>

Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  d4da8e0cdf80545685fe83c06a61f3362febf0fdb2eb4bca4d3d7d46794c8e72
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver build --item SemanticModel/Parcel --item Report/Parcel --workspace-config workspace-production.yml
```

<!-- cli-capture: {"id": "101-report-production-build", "title": "Build · production pair in its own workspace"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · production pair in its own workspace">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Production
Catalogue  none
Targets
  SemanticModel/Parcel → SemanticModel/Parcel_Production
  Report/Parcel → Report/Parcel_Report_Production


Build

    Create SemanticModel/Parcel_Production                                                                20.7s
    Create Report/Parcel_Report_Production                                                                20.7s
  Create Power BI items                                                                                   41.4s
  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel_Production                                                                0.0s
    Resolve Report/Parcel_Report_Production                                                                0.0s
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

→   SemanticModel/Parcel_Production · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel_Production · Deploy semantic definitions · 1 action                              21.1s</span>
→   SemanticModel/Parcel_Production, Report/Parcel_Report_Production · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel_Production, Report/Parcel_Report_Production · Verify deployed semantic definitions · 1 action   20.7s</span>
→   Report/Parcel_Report_Production · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓   Report/Parcel_Report_Production · Deploy Report definitions · 1 action                                20.4s</span>
→   Report/Parcel_Report_Production · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓   Report/Parcel_Report_Production · Verify deployed Report definitions · 1 action                       21.4s</span>
  Install                                                                                                 1m23s
<span class="terminal-status-green">✓ Build                                                                                                   2m05s</span>

Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  60e0d5ff7a64ba24ad9343689bb3d21e20e64d604f85edf1fe5817076faaa6f0
</code></pre>
</figure>
<!-- /cli-capture -->

Each Build ran in its own workspace and selected the linked model with the Report, as a catalogue-free project requires. If the development pair is already deployed, only the production Build is new work.

Check each Report's actual service binding, including the workspace, not just the displayed item names:

| Configuration | Workspace | Report | Linked semantic model |
| --- | --- | --- | --- |
| `workspace-development.yml` | Parcel Development | `Parcel_Report_Dev` | `Parcel_Dev` |
| `workspace-production.yml` | Parcel Production | `Parcel_Report_Production` | `Parcel_Production` |

In each workspace’s **lineage view**, follow the deployed Report’s semantic-model link. Confirm both its name and workspace against the table above. The production Report must link to `Parcel_Production`, not to the development model. The source `byPath` remains unchanged.

For a viewing check, refresh each model with refresh permission, then open each Report with view/query permission:

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-development.yml
weaver load SemanticModel/Parcel --workspace-config workspace-production.yml
```

<!-- cli-capture: {"id": "103-report-production-refresh", "title": "Load · refresh the production model"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · refresh the production model">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Resolve semantic models                                                                                  0.5s
  Read catalogue                                                                                           0.0s
Workspace  Parcel Production
Catalogue  none
Targets
  SemanticModel/Parcel → SemanticModel/Parcel_Production

  Build run graph                                                                                          0.0s
→   Load SemanticModel/Parcel
<span class="terminal-status-green">✓   Load SemanticModel/Parcel                                                                              7.7s</span>
  Execute                                                                                                  7.7s
<span class="terminal-status-green">✓ Load                                                                                                     8.2s</span>

<span class="terminal-status-green">load succeeded: SemanticModel/Parcel</span>

Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
</code></pre>
</figure>
<!-- /cli-capture -->

Each model returns Delivery Count = 2, so open each Report and its card shows **2**. Model refresh and Report rendering are separate checks from Build and binding; there is no Report Load or Test.

An unrelated authored `byConnection` with no local model association stays as authored. Weaver does not reverse-map that external connection to a development or production model. The linked-pair behaviour above applies to the local association; [Report binding rules](../reference/power-bi/requirements-and-compatibility.md#report-binding) also describe same-name model precedence and the catalogue-backed Report-only case.

The Report now follows its model into each workspace without a source edit. When you also need to move its Lakehouse or Warehouse sources, use [workspace and environment mappings](../estate/environments.md) for the whole project. Destination names alone do not change source expressions or credentials. For changes to the model itself, return to [native TMDL and overlays](../semantic-models/native-tmdl.md).

## Remove only the example items

When you are done, delete the example Reports and models from both workspaces.
