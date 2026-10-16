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

<!-- review-todo: report-workspaces -->
!!! warning "TODO — repeat these Builds in two authorised workspaces"
    The captures below verify distinct physical pairs in Weaver Example only. Run these development and production configurations in two authorised workspaces and capture each Report’s actual workspace/model binding.
<!-- /review-todo -->

```bash
weaver check .
weaver build . --item SemanticModel/Parcel --item Report/Parcel --workspace-config workspace-dev.yml
```

<!-- cli-capture: {"id": "100-report-development-build", "title": "Build \u00b7 development pair and binding", "start": "Installation", "full": true} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · development pair and binding">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  fdca322af022d22becb26011d253df6e9d1dd198279fb3967138a4f4c26629a7
</code></pre>
<details><summary>Show the complete capture</summary><pre tabindex="0" aria-label="Captured terminal output"><code>Workspace  Weaver Example
Catalogue  none
Targets
  SemanticModel/Parcel → SemanticModel/Parcel_Dev
  Report/Parcel → Report/Parcel_Report_Dev

Build

    Create SemanticModel/Parcel_Dev                                                                       20.6s

    Create Report/Parcel_Report_Dev                                                                       20.6s

  Create Power BI items                                                                                   41.2s

  Resolve semantic data sources                                                                            0.0s

    Resolve SemanticModel/Parcel_Dev                                                                       0.0s

    Resolve Report/Parcel_Report_Dev                                                                       0.0s

  Read target inventories                                                                                  0.2s

  Read semantic sources                                                                                    0.0s

  Prepare bundle                                                                                           0.1s

Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1
  Report/Parcel
    changed                 1
    selected for build      1

→   SemanticModel/Parcel_Dev · Deploy semantic definitions · 1 action

<span class="terminal-status-green">✓   SemanticModel/Parcel_Dev · Deploy semantic definitions · 1 action                                     20.8s</span>

→   SemanticModel/Parcel_Dev, Report/Parcel_Report_Dev · Verify deployed semantic definitions · 1 action

<span class="terminal-status-green">✓   SemanticModel/Parcel_Dev, Report/Parcel_Report_Dev · Verify deployed semantic definitions · 1 action   20.5s</span>

→   Report/Parcel_Report_Dev · Deploy Report definitions · 1 action

<span class="terminal-status-green">✓   Report/Parcel_Report_Dev · Deploy Report definitions · 1 action                                       20.4s</span>

→   Report/Parcel_Report_Dev · Verify deployed Report definitions · 1 action

<span class="terminal-status-green">✓   Report/Parcel_Report_Dev · Verify deployed Report definitions · 1 action                              20.6s</span>

  Install                                                                                                 1m22s

<span class="terminal-status-green">✓ Build                                                                                                   2m03s</span>

Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  fdca322af022d22becb26011d253df6e9d1dd198279fb3967138a4f4c26629a7
</code></pre></details><p class="terminal-source"><a href="../../assets/cli-captures/100-report-development-build.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

```bash
weaver build . --item SemanticModel/Parcel --item Report/Parcel --workspace-config workspace-prod.yml
```

<!-- cli-capture: {"id": "101-report-production-build", "title": "Build \u00b7 production-labelled pair and binding", "start": "Installation", "full": true} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · production-labelled pair and binding">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  2b7649788915c15a48ef067717f36925c5e9a765b6be9e6deff233c2e7c1fe7f
</code></pre>
<details><summary>Show the complete capture</summary><pre tabindex="0" aria-label="Captured terminal output"><code>Workspace  Weaver Example
Catalogue  none
Targets
  SemanticModel/Parcel
  Report/Parcel → Report/Parcel_Report

Build

    Create Report/Parcel_Report                                                                           21.1s

  Create Power BI items                                                                                   21.1s

  Resolve semantic data sources                                                                            0.0s

    Resolve SemanticModel/Parcel                                                                           0.0s

    Resolve Report/Parcel_Report                                                                           0.0s

  Read target inventories                                                                                  0.2s

  Read semantic sources                                                                                    0.0s

  Prepare bundle                                                                                           0.1s

Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1
  Report/Parcel
    changed                 1
    selected for build      1

→   SemanticModel/Parcel · Deploy semantic definitions · 1 action

<span class="terminal-status-green">✓   SemanticModel/Parcel · Deploy semantic definitions · 1 action                                         20.6s</span>

→   SemanticModel/Parcel, Report/Parcel_Report · Verify deployed semantic definitions · 1 action

<span class="terminal-status-green">✓   SemanticModel/Parcel, Report/Parcel_Report · Verify deployed semantic definitions · 1 action          20.4s</span>

→   Report/Parcel_Report · Deploy Report definitions · 1 action

<span class="terminal-status-green">✓   Report/Parcel_Report · Deploy Report definitions · 1 action                                           20.3s</span>

→   Report/Parcel_Report · Verify deployed Report definitions · 1 action

<span class="terminal-status-green">✓   Report/Parcel_Report · Verify deployed Report definitions · 1 action                                  20.7s</span>

  Install                                                                                                 1m22s

<span class="terminal-status-green">✓ Build                                                                                                   1m43s</span>

Installation
<span class="terminal-status-green">    4 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  2b7649788915c15a48ef067717f36925c5e9a765b6be9e6deff233c2e7c1fe7f
</code></pre></details><p class="terminal-source"><a href="../../assets/cli-captures/101-report-production-build.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

If the development pair is already deployed, only the production Build is new work. Both commands select the linked model with the Report, as required for this catalogue-free project.

Check each Report's actual service binding, including the workspace, not just the displayed item names:

| Configuration | Workspace | Report | Linked semantic model |
| --- | --- | --- | --- |
| `workspace-dev.yml` | Parcel BI Development | `Parcel_Report_Dev` | `Parcel_Dev` |
| `workspace-prod.yml` | Parcel BI Production | `Parcel_Report` | `Parcel` |

The [live binding readbacks](../assets/cli-captures/readbacks.json) verified `Parcel_Report_Dev` → `Parcel_Dev` and `Parcel_Report` → `Parcel`. Both captures used the authorised disposable **Weaver Example** workspace, with distinct physical pairs. They demonstrate configuration-specific binding, not access to a second workspace or a real production deployment.

In each workspace’s **lineage view**, follow the deployed Report’s semantic-model link. Confirm both its name and workspace against the table above. The production Report must link to the production model, not to the development one. The source `byPath` remains unchanged.

For a viewing check, refresh each model with refresh permission, then open each Report with view/query permission:

```bash
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-prod.yml
```

<!-- cli-capture: {"id": "103-report-production-refresh", "title": "Load \u00b7 refresh the production-labelled model", "start": "load succeeded:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · refresh the production-labelled model">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code><span class="terminal-status-green">load succeeded: SemanticModel/Parcel</span>

Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/103-report-production-refresh.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

<!-- review-todo: report-cards -->
!!! warning "TODO — check both rendered Delivery Count cards"
    Open Parcel_Report_Dev and Parcel_Report after the refreshes above and confirm each card shows 2. DAX values and bindings are verified; the rendered cards are not.
<!-- /review-todo -->

DAX readback returned 2 from each refreshed model. Both Delivery Count cards should show **2**. Model refresh and Report rendering are separate checks from Build and binding; there is no Report Load or Test.

An unrelated authored `byConnection` with no local model association stays as authored. Weaver does not reverse-map that external connection to a development or production model. The linked-pair behaviour above applies to the local association; [Report binding rules](../reference/power-bi/requirements-and-compatibility.md#report-binding) also describe same-name model precedence and the catalogue-backed Report-only case.

The Report now follows its model into each workspace without a source edit. When you also need to move its Lakehouse or Warehouse sources, use [workspace and environment mappings](../estate/environments.md) for the whole project. Destination names alone do not change source expressions or credentials. For changes to the model itself, return to [native TMDL and overlays](../semantic-models/native-tmdl.md).

## Remove only the example items

If you created disposable pairs for this exercise, delete their Reports before their models. Keep both workspaces and any pre-existing items; if you updated an existing item, retain its original definition rather than treating deletion as cleanup.
