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

If your shell is already in the project, use `--project-folder .` and stay there. A Power BI-only project has no Environment yet, so Initialise asks for one: choose an existing Environment or let it create `Weaver`. Press Enter to skip the optional Lakehouse, then confirm. If Operations is already in the project, this is a rerun that changes nothing.

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

## 3. Create the connection

An Import model over a Fabric Warehouse refreshes through an explicit cloud connection with credentials. Weaver binds an existing one; it does not create credentials. In Fabric, open **Settings** → **Manage connections and gateways** → **New**, choose **Cloud** and **SQL Server**, and enter:

- **Server:** the Operations Warehouse's SQL connection string (Warehouse **Settings** → **SQL endpoint**);
- **Database:** `Operations`;
- **Authentication:** OAuth 2.0 with your account, or **Workspace identity**. Workspace identity needs the workspace to have an identity (workspace **Settings** → **Workspace identity**) with Contributor access to the workspace.

If someone else owns a suitable connection, ask them to share it with you instead.

## 4. Bind and refresh the model

<span id="3-bind-and-refresh-the-model"></span>

```bash
weaver build --item SemanticModel/ParcelWarehouse --bind-data-sources
```

<!-- cli-capture: {"id": "113-managed-model-bind-build", "title": "Build · install the managed model and bind its connection"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · install the managed model and bind its connection">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  SemanticModel/ParcelWarehouse


Build

  Check target occupancy                                                                                   0.0s
  Resolve semantic data sources                                                                            0.6s
  Read catalogue                                                                                           9.8s
    Resolve SemanticModel/ParcelWarehouse                                                                  0.0s
    Read Warehouse/Catalogue inventory                                                                   0.3s
  Read target inventories                                                                                  0.3s
  Read semantic sources                                                                                    1.2s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/ParcelWarehouse
    dependency impacts      1
    selected for build      1

→   Warehouse/Catalogue · Removing superseded catalogue entries · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Removing superseded catalogue entries · 1 action                               3.4s</span>
→   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action                        0.6s</span>
→   SemanticModel/ParcelWarehouse · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelWarehouse · Deploy semantic definitions · 1 action                                23.3s</span>
→   Warehouse/Catalogue · Publish deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Publish deployed semantic definitions · 1 action                              24.6s</span>
→   Warehouse/Catalogue · Updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Updating catalogue definitions · 1 action                                      0.5s</span>
→   Warehouse/Catalogue · Finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Finalising catalogue · 1 action                                                0.5s</span>
  Install                                                                                                 52.9s
SemanticModel/ParcelWarehouse data sources bound: [warehouse-endpoint];operations

<span class="terminal-status-green">✓ Build                                                                                                   1m20s</span>

Installation
<span class="terminal-status-green">    6 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  891699408c263599e0ee16d53f9416f22760f53e9b3089fffe84c7ebf1716f53
</code></pre>
</figure>
<!-- /cli-capture -->

Build generated CurrentStatus from the Warehouse View, deployed the model, bound it to the connection whose server and database match, and recorded it in the catalogue. Without a matching connection, Build still deploys but warns `no connection has that path`, and refresh later fails with "uses a default data connection without explicit connection credentials". If more than one connection reaches the same endpoint, Build refuses and names them; keep one.

Refresh the source and model together:

```bash
weaver load Warehouse/Operations SemanticModel/ParcelWarehouse
```

<!-- cli-capture: {"id": "114-managed-source-and-model-load", "title": "Load · Warehouse source, then the model refresh"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · Warehouse source, then the model refresh">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           3.1s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations
  SemanticModel/ParcelWarehouse

  Build run graph                                                                                          0.0s
→   Load Warehouse/Operations/Parcel.StatusEvent
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +0 ~0 -0 !0)                                  4.4s</span>
→   Load SemanticModel/ParcelWarehouse
<span class="terminal-status-green">✓   Load SemanticModel/ParcelWarehouse                                                                     7.4s</span>
  Execute                                                                                                 11.9s
  Record what the run did                                                                                  0.5s
<span class="terminal-status-green">✓ Load                                                                                                    15.5s</span>

<span class="terminal-status-green">load succeeded: Warehouse/Operations, SemanticModel/ParcelWarehouse</span>

Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   3
    inserted               0
    updated                0
    deleted                0
    rejected               0

  Workflow: ada9ebe7e6804230a0354a8b19ad37ec
</code></pre>
</figure>
<!-- /cli-capture -->

The Warehouse Table loaded before the model refreshed. Open **ParcelWarehouse** in the service, choose Write DAX queries (or use the [Desktop live-connection route](native-tmdl.md#4-refresh-and-inspect-the-model)), and run:

```dax
EVALUATE
CurrentStatus
```

The model returns the same two rows as the Warehouse View: P-1001 / In transit / Central and P-1002 / Delivered / South.

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

Build the changed model, then refresh it after its source:

```bash
weaver build --item SemanticModel/Parcel --bind-data-sources
```

<!-- cli-capture: {"id": "120-native-source-build", "title": "Build · connect the native model's ParcelStatus"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · connect the native model&#x27;s ParcelStatus">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  SemanticModel/Parcel


Build

  Check target occupancy                                                                                   0.0s
  Resolve semantic data sources                                                                            0.4s
  Read catalogue                                                                                           2.8s
    Resolve SemanticModel/Parcel                                                                           0.0s
    Read Warehouse/Catalogue inventory                                                                   0.1s
  Read target inventories                                                                                  0.1s
  Read semantic sources                                                                                    0.5s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/Parcel
    changed                 1
    selected for build      1

→   Warehouse/Catalogue · Removing superseded catalogue entries · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Removing superseded catalogue entries · 1 action                               2.0s</span>
→   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action                        0.6s</span>
→   SemanticModel/Parcel · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/Parcel · Deploy semantic definitions · 1 action                                         22.1s</span>
→   Warehouse/Catalogue · Publish deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Publish deployed semantic definitions · 1 action                              23.9s</span>
→   Warehouse/Catalogue · Updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Updating catalogue definitions · 1 action                                      1.3s</span>
→   Warehouse/Catalogue · Finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Finalising catalogue · 1 action                                                0.5s</span>
  Install                                                                                                 50.4s
SemanticModel/Parcel data sources bound: [warehouse-endpoint];operations

<span class="terminal-status-green">✓ Build                                                                                                   56.0s</span>

Installation
<span class="terminal-status-green">    6 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  e7c89bef423d5b6ca034168a8d4b81f75af2d66a04232251c3067aef808260f0
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load Warehouse/Operations SemanticModel/Parcel
```

<!-- cli-capture: {"id": "121-native-source-load", "title": "Load · source, then the native model"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · source, then the native model">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.9s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations
  SemanticModel/Parcel

  Build run graph                                                                                          0.0s
→   Load Warehouse/Operations/Parcel.StatusEvent
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +0 ~0 -0 !0)                                  3.9s</span>
→   Load SemanticModel/Parcel
<span class="terminal-status-green">✓   Load SemanticModel/Parcel                                                                              7.2s</span>
  Execute                                                                                                 11.3s
  Record what the run did                                                                                  0.5s
<span class="terminal-status-green">✓ Load                                                                                                    14.7s</span>

<span class="terminal-status-green">load succeeded: Warehouse/Operations, SemanticModel/Parcel</span>

Load summary
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   3
    inserted               0
    updated                0
    deleted                0
    rejected               0

  Workflow: 05881cbbd216434fb5638533587c92e4
</code></pre>
</figure>
<!-- /cli-capture -->

With the sample partition removed, `Weaver.Source` supplies the Warehouse partition at Build: the deployed ParcelStatus partition now navigates to `Parcel.CurrentStatus` in Operations. The columns, the Delivery data and the Report's binding to **Parcel** stay the same.

[Compare DAX with source SQL](validation.md#compare-dax-with-source-sql) to validate a source-backed model in the same project. [Run and inspect the estate](../estate/operate.md) combines source Load, model refresh, Test and Health.
