# Connect a managed Fabric source

Extend the existing Parcel project from [Power BI-only operation into a Catalogue-managed Fabric estate](index.md#two-ways-to-use-weaver-with-power-bi). Add a Warehouse, then use `Weaver.Source` to connect its data to a model. The walkthrough below creates a separate model; you can also [connect the existing native model](#connect-the-existing-native-model) and keep its linked Report.

## Before you start

Continue the [native Parcel project](native-tmdl.md) in the same workspace, retaining its configuration and overlays. That starting path has no Catalogue; adding the Warehouse below introduces one. The workspace now needs Fabric capacity that supports Warehouse work, Warehouse create/alter/load and SELECT rights, Catalogue access, and model deployment, refresh and query permissions. Source-backed Import refresh also needs an existing supported service connection with SQL access. Weaver can bind a matching connection; adding a Catalogue does not create credentials or administer gateways.

## 1. Configure destination and source separately

From the directory containing `parcel`, extend the project:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --warehouse Operations \
  --example Parcel
cd parcel
```

If your shell is already in the project, use `--project-folder .` and stay there. Omitted existing items are retained. If Operations is already present, this is an idempotent rerun, not a request to replace it.

Initialise adds the Operations Warehouse with its independent [Table and View](../warehouse/first-project.md), their validations, and a **separate** `ParcelWarehouse` model. It introduces the required Catalogue and Environment support for the data project. It retains `Parcel.SemanticModel`, the Report and previously authored files, including any same-name Parcel overlay. New target bindings are added to `workspace-config.yml` without changing existing physical bindings. This extends the same installation; it does not replace the inline Delivery partition or change the original model’s meaning.

Open `PowerBI/Parcel/ParcelWarehouse.tmdl`:

<!-- initialise:PowerBI/Parcel/ParcelWarehouse.tmdl -->
```tmdl
model Model
	culture: en-US
	defaultMode: import
	annotation 'Weaver.BaseSemanticModels' = Parcel

table CurrentStatus
	annotation 'Weaver.Source' = Warehouse/Operations/Parcel.CurrentStatus
```
<!-- /initialise -->

The additional model composes the native Parcel foundation, so existing modelling policy still has its original Delivery/Depot tables to refine. `Weaver.Source` asks Build to generate this model’s CurrentStatus table from the managed Warehouse View. Its Import partition and columns are generated from the resolved source metadata. This is an additional model: it does not substitute a Warehouse partition into the native Delivery table. [Author from TMDL](from-tmdl.md#3-generate-from-a-managed-source-only-when-needed) explains source generation in detail.

The project’s `targets` choose physical items. Optional `data_sources` mappings can independently choose which supported physical source a logical expression reads; see [workspace mappings](../estate/environments.md). Neither setting grants SQL access or creates a service connection.

## 2. Build and load the Warehouse first

```bash
weaver check
weaver build --item Warehouse/Operations
weaver load Warehouse/Operations
```

In a SQL query connected to Operations, inspect the source:

```sql
SELECT [Parcel ID], [Status], [Depot]
FROM Parcel.CurrentStatus
ORDER BY [Parcel ID];
```

Expect P-1001 / In transit / Central and P-1002 / Delivered / South. The Warehouse’s StatusEvent Table and CurrentStatus View remain the same independent pipeline introduced in the Warehouse journey.

## 3. Bind and refresh the model

```bash
weaver build --item SemanticModel/ParcelWarehouse --bind-data-sources
```

<!-- cli-capture: {"id": "113-managed-model-bind-build", "title": "Build · install and verify the managed model"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · install and verify the managed model">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Weaver Example
Catalogue  Warehouse/Catalogue
Targets
  SemanticModel/ParcelWarehouse

Build

    Create SemanticModel/ParcelWarehouse                                                                  20.7s

  Create Power BI items                                                                                   20.7s

  Check target occupancy                                                                                   0.0s

  Resolve semantic data sources                                                                            0.3s

  Read catalogue                                                                                           1.6s

    Resolve SemanticModel/ParcelWarehouse                                                                  0.0s

    Read Warehouse/Catalogue inventory                                                                     0.0s

  Read target inventories                                                                                  0.0s

  Read semantic sources                                                                                    0.6s

  Prepare bundle                                                                                           0.1s

Install selection
  SemanticModel/ParcelWarehouse
    changed                 1
    selected for build      1

→   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action                          1.6s</span>

→   SemanticModel/ParcelWarehouse · Deploy semantic definitions · 1 action

<span class="terminal-status-green">✓   SemanticModel/ParcelWarehouse · Deploy semantic definitions · 1 action                                21.0s</span>

→   Warehouse/Catalogue · Publish deployed semantic definitions · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Publish deployed semantic definitions · 1 action                                24.1s</span>

→   Warehouse/Catalogue · Updating catalogue definitions · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Updating catalogue definitions · 1 action                                        2.3s</span>

→   Warehouse/Catalogue · Finalising catalogue · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Finalising catalogue · 1 action                                                  0.6s</span>

  Install                                                                                                 49.6s

<span class="terminal-status-amber">warning: SemanticModel/ParcelWarehouse reads [warehouse-endpoint];operations, and no connection has that path. Create a connection for it in Fabric before refreshing.</span>

<span class="terminal-status-green">✓ Build                                                                                                   1m14s</span>

Installation
<span class="terminal-status-green">    5 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  f804e31e3ca885c39ee691d2a4f205f8992398b1d8ed70bf550c8f6a10e81385
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load Warehouse/Operations SemanticModel/ParcelWarehouse
```

<!-- cli-capture: {"id": "114-managed-source-and-model-load", "title": "Load · source succeeded, model refresh failed"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · source succeeded, model refresh failed">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.4s

Workspace  Weaver Example
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations
  SemanticModel/ParcelWarehouse

  Build run graph                                                                                          0.0s

→   Load Warehouse/Operations/Parcel.StatusEvent

→   Load Warehouse/Operations/Parcel.LakehouseCurrentStatus

→   Load Warehouse/Operations/Parcel.LiveStatus

<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LiveStatus  (read 0, +0 ~0 -0 !0)                                     2.9s</span>

<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +0 ~0 -0 !0)                                    4.4s</span>

→   Load SemanticModel/ParcelWarehouse

<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LakehouseCurrentStatus  (read 2, +0 ~0 -0 !0)                         4.6s</span>

<span class="terminal-status-amber">warning: SemanticModel/ParcelWarehouse reads [warehouse-endpoint];operations, and no connection has that path. If the refresh fails, create a connection for it.</span>

<span class="terminal-status-red">✗   Load SemanticModel/ParcelWarehouse                                                                     6.0s</span>

  Execute                                                                                                 10.6s

  Record what the run did                                                                                  0.7s

<span class="terminal-status-red">✗ Load                                                                                                    13.7s</span>

load partially_succeeded: Warehouse/Operations, SemanticModel/ParcelWarehouse

<span class="terminal-status-red">  ✗ failed                   load:SemanticModel/ParcelWarehouse</span>
<span class="terminal-status-red">      error: load:SemanticModel/ParcelWarehouse failed: Semantic model refresh [item-id] ended with status &#x27;Failed&#x27;: We cannot refresh this semantic model because this semantic model uses a default data connection without explicit connection credentials. Please replace the default data connection in the semantic model settings with an explicit cloud or gateway data connection.; (Premium_ASWL_Error, ModelRefresh_ShortMessage_ProcessingError, ModelRefresh_DataSourceErrorLabel) No connection has the path [warehouse-endpoint];operations. Create a connection for it in Fabric, then load again.</span>

Load summary
<span class="terminal-status-green">    3 succeeded</span>
<span class="terminal-status-red">    1 failed</span>
    0 blocked
  Rows
    read                   5
    inserted               0
    updated                0
    deleted                0
    rejected               0

  Workflow: [run-id]
<span class="terminal-status-red">error: REST reported: Load failed for SemanticModel/ParcelWarehouse: load:SemanticModel/ParcelWarehouse failed: Semantic model refresh [item-id] ended with status &#x27;Failed&#x27;: We cannot refresh this semantic model because this semantic model uses a default data connection without explicit connection credentials. Please replace the default data connection in the semantic model settings with an explicit cloud or gateway data connection.; (Premium_ASWL_Error, ModelRefresh_ShortMessage_ProcessingError, ModelRefresh_DataSourceErrorLabel) No connection has the path [warehouse-endpoint];operations. Create a connection for it in Fabric, then load again.; Load summary: 3 succeeded, 1 failed</span>
  Workflow: [run-id]
</code></pre>
</figure>
<!-- /cli-capture -->

<!-- review-todo: managed-refresh -->
!!! warning "TODO — capture a successful ParcelWarehouse refresh"
    The Load above failed because Operations has no explicit cloud or gateway connection with credentials. Bind an approved connection, rerun this Load and replace this TODO with its successful terminal result.
<!-- /review-todo -->

The capture’s source Loads succeeded, but the model refresh failed: the service had no explicit cloud or gateway connection with credentials for Operations. Build success verifies the deployed definition, not the credentials needed to refresh it. Select an existing approved connection with the connection’s owner before rerunning Load.

Build the source and model in separate requests. `--bind-data-sources` uses an existing matching supported connection. Resolve missing or ambiguous connections with the connection’s owner; do not change tenant settings to make the example run.

The selected Warehouse work precedes the additional model’s refresh. After refresh succeeds, open **ParcelWarehouse** in the service, choose Write DAX queries (or use the [Desktop live-connection route](native-tmdl.md#4-refresh-and-inspect-the-model)), and run:

```dax
EVALUATE
CurrentStatus
```

The model should expose the same two current-status rows.

Adding a Lakehouse works the same way: Initialise retains both pipelines and adds `ParcelLakehouse` over Landing’s CurrentStatus Table. With Lakehouse and Warehouse selected, separately named Warehouse integration objects also connect the Lakehouse Event Table without replacing StatusEvent or changing the original View. [Connect items and dependencies](../estate/connected-items.md) follows that path.

## Connect the existing native model

The native Parcel model already has a ParcelStatus table with the same `Parcel ID`, `Status` and `Depot` columns. To connect that model instead of creating a separate variant:

1. In `PowerBI/Parcel/Parcel.SemanticModel/definition/tables/ParcelStatus.tmdl`, remove only the `partition ParcelStatus = m` block and its sample rows. Retain the table and its columns.
2. Add this declaration to the existing `PowerBI/Parcel/Parcel.tmdl` overlay. Keep the modelling rules already there.

<!-- parcel-native-source -->
```tmdl
table ParcelStatus
	annotation 'Weaver.Source' = Warehouse/Operations/Parcel.CurrentStatus
```
<!-- /parcel-native-source -->

If you followed [Connect items and dependencies](../estate/connected-items.md), use `Warehouse/Operations/Parcel.LakehouseCurrentStatus` here to continue the Lakehouse-to-Warehouse flow. Both sources have the same columns.

After building and loading the source, build the changed model and refresh it:

```bash
weaver build --item SemanticModel/Parcel --bind-data-sources
weaver load Warehouse/Operations SemanticModel/Parcel
```

<!-- review-todo: parcel-native-source-refresh -->
!!! warning "TODO — capture the connected Parcel model's refresh"
    The same-schema source replacement is checked offline. The original-model Build and refresh shown here still need live capture with an approved Operations connection, just as the ParcelWarehouse refresh above does.
<!-- /review-todo -->

With the sample partition removed, `Weaver.Source` supplies the Warehouse partition at Build. The columns and the Report's binding to **Parcel** stay the same. Query ParcelStatus through the deployed model to inspect the connected data.

[Compare DAX with source SQL](validation.md#compare-dax-with-source-sql) to validate a source-backed model in the same project. [Run and inspect the estate](../estate/operate.md) combines source Load, model refresh, Test and Health.
