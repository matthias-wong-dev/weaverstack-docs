---
meta_title: Microsoft Fabric data engineering | Weaver docs
description: Build and operate Microsoft Fabric Lakehouses and Warehouses with Weaver using native Python and SQL, dependencies, run state and incremental processing.
social_title: Weaver documentation for Microsoft Fabric data engineering
image_alt: Weaver documentation for Microsoft Fabric data engineering.
---

# Weaver

**Making Fabric easier to use.**

Keep writing Python, SQL and native model definitions. Weaver handles the installation, load work and recorded results around them. Start with the item you are working on.

## A Weaver project at a glance

A Weaver project is ordinary Python, SQL, TMDL and configuration files organised by Fabric item. Start with one item or combine several, as Parcel does here.

<div class="project-overview">
<div class="project-overview-files">
<p class="project-overview-label" id="parcel-files">What you write</p>
<pre class="project-overview-tree" aria-labelledby="parcel-files"><code>parcel/
├── workspace-config.yml
├── workflow.yml
├── Environment/Weaver.Environment/
├── Lakehouse/Landing/
│   ├── Files/Parcel__Events.py
│   ├── Tables/Parcel__Event.py
│   └── Tables/Parcel.CurrentStatus.sql
├── Warehouse/Operations/
│   ├── Parcel.StatusEvent.sql
│   ├── shortcuts.yml
│   ├── Parcel.LakehouseCurrentStatus.sql
│   └── tests/
└── PowerBI/Parcel/
    ├── Parcel.SemanticModel/
    └── Parcel.Report/</code></pre>
</div>
<figure class="project-overview-dag" aria-labelledby="parcel-dependencies" aria-describedby="parcel-edges">
<figcaption class="project-overview-label" id="parcel-dependencies">How the work connects</figcaption>
<p id="parcel-edges" hidden>In Lakehouse Landing, the Parcel.Events Folder feeds the Parcel.Event Table. Event feeds Parcel.CurrentStatus in the Lakehouse and, separately, the Parcel.LakehouseEvent logical Shortcut in Warehouse Operations. That Shortcut feeds Parcel.LakehouseCurrentStatus.</p>
<div class="project-dag-node" data-project-node="folder" data-logical-id="Lakehouse/Landing/Files/Parcel.Events"><strong>Parcel.Events</strong><small>Landing · Python Folder</small></div>
<div class="project-dag-arrow" data-project-edge="folder|event" aria-hidden="true">↓</div>
<div class="project-dag-node" data-project-node="event" data-logical-id="Lakehouse/Landing/Tables/Parcel.Event"><strong>Parcel.Event</strong><small>Landing · Python Table</small></div>
<svg class="project-dag-fork" viewBox="0 0 300 28" aria-hidden="true"><path d="M150 0 V12 M75 24 V12 H225 V24"/><path d="m71 20 4 4 4-4 M221 20 l4 4 4-4"/></svg>
<div class="project-dag-branches">
<div data-project-edge="event|current">
<div class="project-dag-node" data-project-node="current" data-logical-id="Lakehouse/Landing/Tables/Parcel.CurrentStatus"><strong>Parcel.<wbr>CurrentStatus</strong><small>Landing · Spark SQL Table</small></div>
</div>
<div data-project-edge="event|shortcut">
<div class="project-dag-node" data-project-node="shortcut" data-logical-id="Warehouse/Operations/Parcel.LakehouseEvent"><strong>Parcel.<wbr>LakehouseEvent</strong><small>Operations · Logical Shortcut</small></div>
<div class="project-dag-arrow" data-project-edge="shortcut|consumer" aria-hidden="true">↓</div>
<div class="project-dag-node" data-project-node="consumer" data-logical-id="Warehouse/Operations/Parcel.LakehouseCurrentStatus"><strong>Parcel.<wbr>Lakehouse<wbr>CurrentStatus</strong><small>Operations · T-SQL Table</small></div>
</div>
</div>
</figure>
</div>

Dependencies connect the work; Weaver handles building, loading, testing and tracking its state. [Projects and estates](core-concepts/projects-and-estates.md) · [Connect items and dependencies](estate/connected-items.md).

- [Lakehouse](lakehouse/index.md): turn files and Python or Spark SQL into managed Tables.
- [Warehouse](warehouse/index.md): write a SELECT and let Weaver build the Table and its load machinery.
- [Semantic models](semantic-models/index.md): deploy native TMDL, then add modelling conventions and DAX checks.
- [Reports](reports/index.md): deploy native Reports with the right model in each workspace.

When those pieces need to work together, [Coordinate your estate](estate/index.md) covers dependencies, environments, Health and the development loop. Two items are enough to benefit.

New to Weaver? [Start here](getting-started/index.md).

<span id="weaver-documentation"></span>

<span id="build-your-first-project"></span>

<span id="add-work-to-the-project"></span>

<span id="operate-the-estate"></span>
