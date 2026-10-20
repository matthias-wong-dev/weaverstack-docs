# Deploy a native semantic model

Deploy native PBIP/TMDL, query a measure, then hide relationship foreign keys with one modelling rule. Weaver applies the rule to the deployed definition without editing the native files.

## Native files first

A PBIP project contains the model’s native TMDL and its Report definitions. You can also author a model directly in a named TMDL file; [native project layout](../reference/power-bi/project-layout.md) describes both forms.

## Before you start

[Install Weaver](../getting-started/installation.md). This exercise begins in [Power BI-only mode, without a Catalogue](index.md#power-bi-only-without-a-catalogue). Use an existing disposable Power BI service workspace with licensing and permissions to deploy, read and refresh Import Semantic Models, and to edit the linked Report for the field-list check. Use existing permissions; this exercise does not require changing tenant settings. [Service requirements](../reference/power-bi/requirements-and-compatibility.md#runtime-and-service-access) cover the licensing and API boundaries.

Parcel includes Delivery and Depot tables, a relationship and a Delivery Count measure. Its ParcelStatus table has the same `Parcel ID`, `Status` and `Depot` columns as the Warehouse data, with two sample rows to start. The model needs no Lakehouse or source Warehouse workload. If you already have a `parcel` project from the Fabric tasks, run the command from inside it with `--project-folder .` instead; Initialise keeps your data items and adds the models.

## 1. Choose the destination

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --semantic-model Parcel \
  --example Parcel
cd parcel
```

Initialise asks you to confirm (choose `1`), then writes the native model and linked Report under `PowerBI/Parcel/`, a workspace configuration and supporting project files. It creates no Catalogue Warehouse or Fabric Environment. Build creates the Power BI items; building and refreshing this inline model do not require Spark. You can later [add Fabric data workloads and a Catalogue](managed-sources.md) to this same project without replacing its native definitions or existing bindings.

Open `PowerBI/Parcel/Parcel.pbip` in Desktop to inspect the native project. Open `PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl` in your editor. The generated table includes the sample partition and measure:

<!-- initialise:PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl -->
```tmdl
/// Three parcel events, including two delivered parcels.
table Delivery
	measure 'Delivery Count' = SUM(Delivery[Delivered])
		formatString: 0
	measure InternalCost = 7
		formatString: 0.00
	column ParcelId
		dataType: int64
		sourceColumn: ParcelId
		summarizeBy: none
	column DepotId
		dataType: int64
		sourceColumn: DepotId
		summarizeBy: none
	column Delivered
		dataType: int64
		sourceColumn: Delivered
		summarizeBy: sum
	partition Delivery = m
		mode: import
		source =
			let
			    Source = #table(type table [ParcelId = Int64.Type, DepotId = Int64.Type, Delivered = Int64.Type], {{1, 10, 1}, {2, 10, 1}, {3, 20, 0}})
			in
			    Source
```
<!-- /initialise -->

`ParcelStatus.tmdl`, in the same native tables folder, carries the Warehouse-shaped sample. Later, [add `Weaver.Source`](managed-sources.md#connect-the-existing-native-model) to connect that table to the Warehouse without changing its columns or the linked Report.

`workspace-config.yml` already binds `SemanticModel/Parcel` and `Report/Parcel` to their physical names. Keep any existing source bindings. [Environment mappings](../estate/environments.md) covers choosing other physical destinations without changing the source.

## 2. Check the project

```bash
weaver check
```

Check reads local declarations and definitions. It does not execute M/DAX, deploy items or test service permissions.

## 3. Deploy the native model

```bash
weaver build --item SemanticModel/Parcel
```

<!-- cli-capture: {"id": "82-native-catalogue-free-build", "title": "Build · native model without a Catalogue"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · native model without a Catalogue">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel


Build

    Create SemanticModel/Parcel                                                                           20.7s
  Create Power BI items                                                                                   20.7s
  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/Parcel                                                                           0.0s
  Read target inventories                                                                                  0.2s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1

→   SemanticModel/Parcel · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Deploy semantic definitions · 1 action                                         21.3s</span>
→   SemanticModel/Parcel · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Verify deployed semantic definitions · 1 action                                20.5s</span>
  Install                                                                                                 41.8s
<span class="terminal-status-green">✓ Build                                                                                                   1m02s</span>

Installation
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  01a374b67d8eb3b7035bf9ecbd1bb768e263e59c19cbf07741169e18d6b83a5f
</code></pre>
</figure>
<!-- /cli-capture -->

This selects **only the inline semantic model**, even if your project also has source-backed models. Find `Parcel` in your workspace. The Report stays local until you [deploy it](../reports/deploy.md).

## 4. Refresh and inspect the model

```bash
weaver load SemanticModel/Parcel
```

<!-- cli-capture: {"id": "83-native-catalogue-free-refresh", "title": "Load · refresh the inline model"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · refresh the inline model">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Resolve semantic models                                                                                  0.5s
  Read catalogue                                                                                           0.0s
Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel

  Build run graph                                                                                          0.0s
→   Load SemanticModel/Parcel
<span class="terminal-status-green">✓   Load SemanticModel/Parcel                                                                              5.0s</span>
  Execute                                                                                                  5.0s
<span class="terminal-status-green">✓ Load                                                                                                     5.6s</span>

<span class="terminal-status-green">load succeeded: SemanticModel/Parcel</span>

Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
</code></pre>
</figure>
<!-- /cli-capture -->

In the workspace, open the deployed **Parcel** semantic model and choose **Write DAX queries**. Run:

```dax
EVALUATE
ROW("DeliveryCount", [Delivery Count])
```

The live query returned **DeliveryCount = 2**. [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view) needs model write permission and the workspace’s existing web modelling setting. If it is unavailable, connect Power BI Desktop to the published Parcel semantic model using a live connection and run the query in Desktop’s DAX query view with Read and Build permission. Do not query the local PBIP instead: you are checking the deployed model.

Use the linked Report already generated by Initialise for the field-list check below; there is no need to create another Report.

<span id="hide-relationship-foreign-keys"></span>

## AutoHideForeignKeys: hide relationship foreign keys

### Add the same-name overlay

Create `PowerBI/Parcel/Parcel.tmdl`:

```tmdl
model Model
    annotation 'Weaver.AutoHideForeignKeys' = true
```

The filename matches `Parcel.SemanticModel`, so it refines that model rather than declaring another one.

### Deploy and inspect

Build the model and its existing linked Report together. Without a Catalogue, the linked model must be selected in the same Build:

```bash
weaver check
weaver build --item SemanticModel/Parcel --item Report/Parcel
```

<!-- cli-capture: {"id": "85-native-annotation-and-report-build", "title": "Build · apply the rule and bind the linked Report"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · apply the rule and bind the linked Report">
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

```bash
weaver load SemanticModel/Parcel
```

<!-- cli-capture: {"id": "86-native-annotation-refresh", "title": "Load · refresh after the modelling rule"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · refresh after the modelling rule">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Resolve semantic models                                                                                  0.5s
  Read catalogue                                                                                           0.0s
Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Parcel

  Build run graph                                                                                          0.0s
→   Load SemanticModel/Parcel
<span class="terminal-status-green">✓   Load SemanticModel/Parcel                                                                              7.3s</span>
  Execute                                                                                                  7.3s
<span class="terminal-status-green">✓ Load                                                                                                     7.8s</span>

<span class="terminal-status-green">load succeeded: SemanticModel/Parcel</span>

Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
</code></pre>
</figure>
<!-- /cli-capture -->

In the Power BI service, open the generated **Parcel** Report in **Edit** mode and expand Delivery and Depot in the **Data** pane. `Delivery[DepotId]` is gone from the field list; `Depot[DepotId]` is still there. Reading the deployed definition back confirms the change:

| Check | Before the rule | After the rule |
| --- | --- | --- |
| `Delivery[DepotId]` | Visible | Hidden |
| `Depot[DepotId]` | Visible | Visible |
| Delivery Count | 2 | 2 |

The native files and inline data remain in place. Desktop does not execute Weaver annotations when opening the local PBIP; inspect the service-connected model for the change. Hidden fields are not a security policy or RLS/OLS.

To stop requesting the transformation, remove the annotation and rebuild. Setting it to `false` is a no-op, not an instruction to undo an independently authored native hide.

<details markdown="1">
<summary>Inspect the native relationship</summary>

### Inspect the relationship the rule uses

Open `PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl`:

<!-- initialise:PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl -->
```tmdl
relationship Delivery_Depot
	fromColumn: Delivery.DepotId
	toColumn: Depot.DepotId
	fromCardinality: many
	toCardinality: one
	crossFilteringBehavior: oneDirection
```
<!-- /initialise -->

The rule hides the many-side key from the field list, not the one-side key.

</details>

## Carry the convention to the next model

When this convention belongs on several models, [share it in `PowerBI/policy.tmdl`](shared-policy.md). The next task keeps Parcel and its local overlay, adding common formatting and a calculation group.

[Validate the model](validation.md) to check its number, or [connect a managed Fabric source](managed-sources.md) by adding a source-backed model alongside this inline model. [Weaver documents](../core-concepts/weaver-documents.md#native-models-overlays-and-annotations) explains how overlays fit beside native definitions.
