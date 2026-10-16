# Author a model from TMDL

A standalone named TMDL file can supply a model without a native `.SemanticModel` directory. Choose this when you want to author the definition directly; existing PBIP projects do not need to convert.

## 1. Write one complete model

Continue the [generated Parcel project](native-tmdl.md) and add `PowerBI/Parcel/ParcelSummary.tmdl`. Keep its existing native model and Report:

```tmdl
model Model
    culture: en-US
    defaultMode: import

table Delivery
    measure 'Delivery Count' = SUM(Delivery[Delivered])
        formatString: 0
    measure InternalCost = 7
        formatString: 0.00
    column Delivered
        dataType: int64
        sourceColumn: Delivered
        summarizeBy: sum
    partition Delivery = m
        mode: import
        source =
            let
                Source = #table(type table [Delivered = Int64.Type], {{1}, {1}, {0}})
            in
                Source
```

The filename declares `SemanticModel/ParcelSummary`. There is no Report in this example. If a same-name native `ParcelSummary.SemanticModel` exists, this file instead overlays it; do not mistake that for two independent definitions.

Add this binding under `targets` in the existing `workspace-config.yml`, keeping all existing entries:

```yaml title="Add under targets"
  SemanticModel/ParcelSummary: ParcelSummary
```

Use the [ordinary service licensing and permissions](native-tmdl.md). The inline Import partition needs no managed source, catalogue or Fabric Environment.

## 2. Deploy and refresh

```bash
weaver check
weaver build --item SemanticModel/ParcelSummary
weaver load SemanticModel/ParcelSummary
```

<!-- cli-capture: {"id": "95a-summary-build", "title": "Build · a model authored as one TMDL file"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · a model authored as one TMDL file">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/ParcelSummary


Build

    Create SemanticModel/ParcelSummary                                                                    20.6s
  Create Power BI items                                                                                   20.6s
  Resolve semantic data sources                                                                            0.0s
    Resolve SemanticModel/ParcelSummary                                                                    0.0s
  Read target inventories                                                                                  0.2s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.0s
Install selection
  SemanticModel/ParcelSummary
    changed                 1
    selected for build      1

→   SemanticModel/ParcelSummary · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelSummary · Deploy semantic definitions · 1 action                                  21.0s</span>
→   SemanticModel/ParcelSummary · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓   SemanticModel/ParcelSummary · Verify deployed semantic definitions · 1 action                         20.5s</span>
  Install                                                                                                 41.5s
<span class="terminal-status-green">✓ Build                                                                                                   1m02s</span>

Installation
<span class="terminal-status-green">    2 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  adfdbe93e8e0f0fafa41c2439baf189510670bd6c74ac0ae45008dd9eda4afb1
</code></pre>
</figure>
<!-- /cli-capture -->

After refresh, the Delivery table has three rows and Delivery Count = 2. Check validates local shape, not M evaluation or service eligibility.

If the project has a [shared policy](shared-policy.md), it applies here too: ParcelSummary gains the Display calculation group. The standalone file is the model's own layer, so its explicit `formatString: 0` wins over the policy's `#,##0`, just as a same-name overlay would.

## 3. Generate from a managed source only when needed

A table without an authored partition can obtain its columns and partition from managed-source metadata. This is a different route with additional prerequisites: a compatible catalogue, built/loaded supported Lakehouse or Warehouse source, resolved endpoints/metadata, and permissions and connections for the model's chosen mode.

Keep the same project and the loaded source from [Managed sources](managed-sources.md). Direct entrants complete that source setup once. Instead of replacing ParcelSummary’s inline table, add a distinctly named `PowerBI/Parcel/ParcelSourceSummary.tmdl`:

```tmdl
model Model
    defaultMode: import
    annotation 'Weaver.BaseSemanticModels' = Parcel

table CurrentStatus
    annotation 'Weaver.Source' = Warehouse/Operations/Parcel.CurrentStatus
    measure 'Managed Parcel Count' = COUNTROWS(CurrentStatus)
```

Add `SemanticModel/ParcelSourceSummary: ParcelSourceSummary` under the existing targets. Select only this new model:

```bash
weaver check
weaver build --item SemanticModel/ParcelSourceSummary --bind-data-sources
weaver load SemanticModel/ParcelSourceSummary
```

Inspect its generated CurrentStatus columns, Import partition and resolved source expression. Managed Parcel Count should be 2 after source Load and model refresh. The inline Parcel and ParcelSummary models remain independent. Weaver uses an existing supported connection, not new credentials.

With `defaultMode: import`, generation supplies an M navigation partition. Otherwise this generation path supplies Direct Lake entity partitions, which retain their source, service and capacity prerequisites. Source housekeeping audit/signature columns are omitted unless explicitly authored. Native descriptions win over source metadata; unsupported source types fail.

A table **with** an authored partition retains that partition and its authored column types. Adding `Weaver.Source` to it is lineage/refinement, not permission to overwrite its query or generate all columns. Use the [managed-source task](managed-sources.md) to add source-backed functionality without changing the original partition.

Build deploys the native definition while leaving the authored TMDL in the project unchanged.

## Related tasks

- [Look up source generation and annotation boundaries](../reference/power-bi/annotations.md#weaversource).
- [Reuse models through composition](composition.md).
- [Look up native layout](../reference/power-bi/project-layout.md).
