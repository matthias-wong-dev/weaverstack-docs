---
hide:
  - toc
---

# Catalogue Dashboard

The Catalogue Dashboard is a Power BI semantic model and Report over a Weaver catalogue. One command deploys it beside the catalogue. Its seven pages show Health, the Load orchestration graph, recent workflows as a Gantt chart, load performance, an ER diagram with a metadata browser, and a bus matrix for each semantic model.

The model reads the catalogue's tables over Direct Lake, so each page shows what the catalogue records as work settles. The Dashboard only reads the catalogue. Nothing about it is recorded there, and Initialise, Build, Wipe and Mirror never touch it.

It is an ordinary semantic model and Report. Change it to fit your needs, or build your own over the catalogue.

## The HTML Content visual

Each page is drawn by the HTML Content custom visual (the Regular edition, from AppSource). Where a tenant allows only certified visuals, a Fabric administrator must add HTML Content as an organisational visual before the pages render. The semantic model works without it.

The Report is best effort. We aim to replace or supplement it with Fabric Apps.

## Deploy the Dashboard

The catalogue must have been built into by Weaver 0.10.0 or later, which records the lineage the Dashboard reads. Continuing the [Parcel estate](catalogue-and-health.md), name the Dashboard and deploy it:

```bash
weaver catalogue-dashboard --name "Catalogue Dashboard" --workspace-config workspace-development.yml
```

The command creates or updates a SemanticModel and a Report with that name in the catalogue's workspace, then refreshes the model. It reads the catalogue named by `catalogue:` in the workspace configuration; `--catalogue Warehouse/Name` names another. To deploy without naming it each time, add the name to the configuration:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
catalogue_dashboard: Catalogue Dashboard
```

From Python, the same operation is `weaver.deploy_catalogue_dashboard`:

```python
import weaver

result = weaver.deploy_catalogue_dashboard(
    name="Catalogue Dashboard",
    catalogue="Warehouse/Catalogue",
    workspace="Parcel Development",
)
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

### Overview

Installed items by kind, with their object counts, a status bar and when work last settled. The tiles summarise Load, Tests and Build health and the workflows of the last 7 days; significant findings are listed below.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/overview.html" title="Catalogue Dashboard demo: Overview" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Overview full size](../assets/catalogue-dashboard/overview.html){ target="_blank" }</p>

### Health

The Load, Tests and Build findings, filtered by area and severity, including green rows. This page assesses what the catalogue records about itself. Physical inventory and unresolved references need [`weaver health`](catalogue-and-health.md).

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/health.html" title="Catalogue Dashboard demo: Health" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Health full size](../assets/catalogue-dashboard/health.html){ target="_blank" }</p>

### Load orchestration

The installed dependency graph across Lakehouses, Warehouses and semantic models, coloured by each object's last outcome or by kind. The tiles count objects that are current, ready to load, waiting on a dependency or failed.

- Search for an object and press Enter to select it. Shift adds to the selection.
- A term containing `*` adds every match: `Parcel.*` selects every object in the `Parcel` schema. Terms combine.
- **Up** and **Down** set how many dependency levels to show either side of the selection. `‹‹ N` and `N ››` markers expand the neighbours not shown.
- Drag nodes, zoom, and use ⤢ to fill the page. The side panel shows the selected object's last load, readiness, findings, validations, and what it reads and is read by.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/orchestration.html" title="Catalogue Dashboard demo: Load orchestration" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Load orchestration full size](../assets/catalogue-dashboard/orchestration.html){ target="_blank" }</p>

### Gantt

One workflow from the last 7 days, each record a bar on its timeline. The tiles give elapsed time, summed task time, peak concurrency and failures. Hold Ctrl or ⌘ and scroll to zoom time; drag to pan; double-click to reset.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/gantt.html" title="Catalogue Dashboard demo: Gantt" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Gantt full size](../assets/catalogue-dashboard/gantt.html){ target="_blank" }</p>

### Performance

Load statistics over the last 24 hours, 7 days or 30 days, for every item or one: load count and time, rows read, changed and rejected, throughput, a daily trend, and a table of objects ranked by load time.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/performance.html" title="Catalogue Dashboard demo: Performance" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Performance full size](../assets/catalogue-dashboard/performance.html){ target="_blank" }</p>

### Entity dictionary

An ER diagram of Lakehouse and Warehouse tables, drawn from their declared `Primary key` and `Foreign keys`. Select a table and set how many levels of **Parents** (the primary key side) and **Children** (the foreign key side) to follow. Tables with no relationship are shown too. Boxes can be dragged.

Below it, the dictionary lists every item, Table, View, Folder, Shortcut, Test, Assumption and column, filtered by name, kind or description.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/entities.html" title="Catalogue Dashboard demo: Entity dictionary" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Entity dictionary full size](../assets/catalogue-dashboard/entities.html){ target="_blank" }</p>

### Semantic model

One deployed semantic model: its last refresh, DAX validations, and a bus matrix of fact tables against dimension tables showing each relationship's cardinality, filter direction and whether it is active. Its tables, columns, measures and the managed sources they read follow.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/semantic.html" title="Catalogue Dashboard demo: Semantic model" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Semantic model page full size](../assets/catalogue-dashboard/semantic.html){ target="_blank" }</p>
