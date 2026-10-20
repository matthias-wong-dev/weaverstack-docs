---
hide:
  - toc
---

# Catalogue Dashboard

The Catalogue Dashboard is a Power BI semantic model and Report over a Weaver catalogue. One command deploys it beside the catalogue. Its seven pages show Health, the Orchestration graph, when each run started and finished, recent workflows as a Gantt chart, an ER diagram with a metadata browser, and a bus matrix for each semantic model.

The model reads the catalogue's tables over Direct Lake, so each page shows what the catalogue records as work is processed. The Dashboard only reads the catalogue. Nothing about it is recorded there, and Initialise, Build, Wipe and Mirror never touch it.

It is an ordinary semantic model and Report. Change it to fit your needs, or build your own over the catalogue.

## The HTML Content visual

Each page is drawn by the HTML Content custom visual (the Regular edition, from AppSource). Where a tenant allows only certified visuals, a Fabric administrator must add HTML Content as an organisational visual before the pages render. The semantic model works without it.

The Report is best effort. We aim to replace or supplement it with Fabric Apps.

## Deploy the Dashboard

The catalogue must have been built into by Weaver 0.10.0 or later, which records the lineage the Dashboard reads. Continuing the [Parcel estate](catalogue-and-health.md), name the Dashboard and deploy it:

```bash
weaver catalogue-dashboard --name "Catalogue Dashboard" --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "152-catalogue-dashboard", "title": "Catalogue Dashboard · deploy over the Parcel catalogue"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Catalogue Dashboard · deploy over the Parcel catalogue">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Catalogue Dashboard

  Check the source catalogue                                                                               1.8s
  Resolve the Dashboard&#x27;s items                                                                           21.3s
Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Catalogue Dashboard
  Report/Catalogue Dashboard


Build

    Resolve semantic data sources                                                                          0.3s
      Resolve SemanticModel/Catalogue Dashboard                                                            0.0s
      Resolve Report/Catalogue Dashboard                                                                   0.0s
    Read target inventories                                                                                0.2s
    Read semantic sources                                                                                  5.1s
    Prepare bundle                                                                                         0.4s
Install selection
  SemanticModel/Catalogue Dashboard
    changed                 1
    selected for build      1
  Report/Catalogue Dashboard
    changed                 1
    selected for build      1

→     SemanticModel/Catalogue Dashboard · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓     SemanticModel/Catalogue Dashboard · Deploy semantic definitions · 1 action                          22.6s</span>
→     SemanticModel/Catalogue Dashboard, Report/Catalogue Dashboard · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓     SemanticModel/Catalogue Dashboard, Report/Catalogue Dashboard · Verify deployed semantic definitions · 1 action   20.6s</span>
→     Report/Catalogue Dashboard · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓     Report/Catalogue Dashboard · Deploy Report definitions · 1 action                                   20.4s</span>
→     Report/Catalogue Dashboard · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓     Report/Catalogue Dashboard · Verify deployed Report definitions · 1 action                          20.9s</span>
    Install                                                                                               1m24s
<span class="terminal-status-green">✓ Build                                                                                                   1m30s</span>

  Refresh the Dashboard model                                                                             13.6s
<span class="terminal-status-green">✓ Catalogue Dashboard                                                                                     2m08s</span>

Catalogue Dashboard  Catalogue Dashboard  in Parcel Development
  Reads  Parcel Development/Warehouse/Catalogue  (21 tables)
  SemanticModel Catalogue Dashboard  updated
  Report        Catalogue Dashboard  updated
</code></pre>
</figure>
<!-- /cli-capture -->

The command creates or updates a SemanticModel and a Report with that name in the catalogue's workspace, then refreshes the model. It reads the catalogue named by `catalogue:` in the workspace configuration; `--catalogue Warehouse/Name` names another. To deploy without naming it each time, add the name to the configuration:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
catalogue_dashboard: Catalogue Dashboard
```

- The Dashboard deploys into the workspace of the catalogue it reads. A catalogue in another workspace is refused.
- A name that `targets:` deploys a model or Report to is refused, and so is an existing model or Report of that name that is not a Catalogue Dashboard.
- `--dry-run` resolves the catalogue and the Dashboard's items and changes nothing.
- Run the command again after upgrading Weaver. It replaces the model and Report definitions, so save your own changes under another name.
- To remove the Dashboard, delete its SemanticModel and Report in Fabric.

## What it reads

The model reads these catalogue tables over Direct Lake: `Installation`, `Registry`, `LineageNode`, `LineageEdge`, `Dependency`, `LoadStatus`, `TestStatus`, `Log`, `LoadStatistic`, the dictionary tables and the `SemanticModel` tables. The [catalogue schema](../reference/catalogue-schema.md) describes each one.

Each page sends the visual only what it shows. The Gantt and Overview read workflows from the last 7 days, and Performance reads up to 30 days. The catalogue keeps the full history for your own queries.

The first page view after a load, or after the model has been idle, can take several seconds while Direct Lake loads the columns it needs.

## The pages

The pages below are the Dashboard's own renderer over a generated estate of 133 objects, recorded at a fixed time. Search, select, drag and zoom as you would in Power BI.

Times show in the time zone of your browser, with the zone named, for example `AEDT`. The **Times** control in the page header switches the page to UTC and back. The catalogue holds UTC and the Dashboard converts it as it draws, so a time in the table is the same instant in either zone.

### Marks

Each object carries a mark for its kind, in lists, chips, the graph and the Gantt and Performance tables. Hover a mark for its name.

| Mark | Kind |
| --- | --- |
| Filled blue circle | Table |
| Blue ring with a dot | View |
| Green folder | Folder |
| Amber diamond | Shortcut |
| Filled violet triangle | Test |
| Outlined violet triangle | Assumption |
| Dark blue hexagon | Semantic model |
| Dark blue outlined square | Report |

### Overview

Installed items by kind, with their object counts, a status bar and when work was last processed. The tiles summarise Load, Tests and Build health and the workflows of the last 7 days; significant findings are listed below.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/overview.html" title="Catalogue Dashboard demo: Overview" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Overview full size](../assets/catalogue-dashboard/overview.html){ target="_blank" }</p>

### Health

The Load, Tests and Build findings, filtered by area and severity, including green rows. This page assesses what the catalogue records about itself. Physical inventory and unresolved references need [`weaver health`](catalogue-and-health.md).

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/health.html" title="Catalogue Dashboard demo: Health" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Health full size](../assets/catalogue-dashboard/health.html){ target="_blank" }</p>

### Orchestration

The installed dependency graph across Lakehouses, Warehouses and semantic models, coloured by each object's last outcome or by kind. The tiles count objects that are current, ready to load, waiting on a dependency or failed.

- Search for an object and press Enter to select it. Shift adds to the selection.
- A term containing `*` adds every match: `Parcel.*` selects every object in the `Parcel` schema. Terms combine.
- **Up** and **Down** set how many dependency levels to show either side of the selection. `‹‹ N` and `N ››` markers expand the neighbours not shown.
- Drag nodes, zoom, and use ⤢ to fill the page. The side panel shows the selected object's last load, readiness, findings, validations, and what it reads and is read by.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/orchestration.html" title="Catalogue Dashboard demo: Orchestration" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Orchestration full size](../assets/catalogue-dashboard/orchestration.html){ target="_blank" }</p>

### Performance

Did the run finish in time. Each workflow is one vertical bar in a column for its day, from the time it started at the bottom to the time it finished at the top, with the time of day up the side in the page's time zone. The bar is drawn in blue for the Load part and violet for the Test part, and outlined in red when a record failed. Runs that overlap are never added together. Set a deadline, an hour of that zone, to see which runs ended after it.

Choose a window of 24 hours, 7 days or 30 days, a task and an item. Select a run, in the chart or its table, to list its longest object records, Loads first and then Tests. Select an object in that list to see that load's own row counts, read, inserted, updated, deleted and rejected, with the same object's loads in the runs around it, one row each. A Test shows its result and message with the executions around it. Counts are never added across loads.

The Loads and Tests tables give each object's number of loads or executions over the window. Select one to see its latest loads or executions one by one. The largest loads of the last 7 days are listed each by its own counts.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/performance.html" title="Catalogue Dashboard demo: Performance" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Performance full size](../assets/catalogue-dashboard/performance.html){ target="_blank" }</p>

### Gantt

One workflow from the last 7 days, each record a bar on its timeline, with the object's mark, its item as `Type/Name` and its task, Load or Test. The tiles give elapsed time, summed task time, peak concurrency and failures. Click a row for the object and the record's outcome. Hold Ctrl or ⌘ and scroll to zoom time; drag to pan; double-click to reset.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/gantt.html" title="Catalogue Dashboard demo: Gantt" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Gantt full size](../assets/catalogue-dashboard/gantt.html){ target="_blank" }</p>

### Entity dictionary

An ER diagram of Lakehouse and Warehouse tables, drawn from their declared `Primary key` and `Foreign keys`. Select a table and set how many levels of **Parents** (the primary key side) and **Children** (the foreign key side) to follow. Tables with no relationship are shown too. Boxes can be dragged.

Below it, the dictionary lists every item, Table, View, Folder, Shortcut, Test, Assumption and column, filtered by name, kind or description.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/entities.html" title="Catalogue Dashboard demo: Entity dictionary" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Entity dictionary full size](../assets/catalogue-dashboard/entities.html){ target="_blank" }</p>

### Semantic model

One deployed semantic model: its last refresh, DAX validations, and a bus matrix of fact tables against dimension tables showing each relationship's cardinality, filter direction and whether it is active. Its tables, columns, measures and the managed sources they read follow.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/semantic.html" title="Catalogue Dashboard demo: Semantic model" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Semantic model page full size](../assets/catalogue-dashboard/semantic.html){ target="_blank" }</p>
