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
<figure class="project-overview-dag" aria-labelledby="parcel-dependencies">
<figcaption class="project-overview-label" id="parcel-dependencies">How the work connects</figcaption>
<div class="project-diagram-scroll" tabindex="0" role="region" aria-label="Parcel dependency diagram; scroll horizontally on narrow screens">
<svg class="parcel-diagram" viewBox="0 0 960 340" role="img" aria-labelledby="parcel-docs-title parcel-docs-desc">
<title id="parcel-docs-title">A Parcel project across Fabric items</title>
<desc id="parcel-docs-desc">Parcel.Events feeds Parcel.Event. Event branches to Lakehouse CurrentStatus and a Warehouse logical Shortcut, which feeds LakehouseCurrentStatus. The Warehouse source connects to the Parcel semantic model through Weaver.Source, and the model binds to the Parcel Report.</desc>
<defs><marker id="parcel-docs-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="var(--pv-blue)"/></marker></defs>
<g data-project-band="Lakehouse" class="parcel-band band-0">
<rect x="1" y="1" width="358" height="332" rx="10"/>
<text class="parcel-band-title" x="16" y="32">Lakehouse</text>
<text class="parcel-band-sub" x="16" y="56">Landing · Parcel</text>
</g>
<g data-project-band="Warehouse" class="parcel-band band-1">
<rect x="371" y="1" width="268" height="332" rx="10"/>
<text class="parcel-band-title" x="386" y="32">Warehouse</text>
<text class="parcel-band-sub" x="386" y="56">Operations · Parcel</text>
</g>
<g data-project-band="Semantic Model" class="parcel-band band-2">
<rect x="651" y="1" width="143" height="332" rx="10"/>
<text class="parcel-band-title" x="666" y="28">Semantic<tspan x="666" dy="22"> Model</tspan></text>
<text class="parcel-band-sub" x="666" y="78">Parcel</text>
</g>
<g data-project-band="Report" class="parcel-band band-3">
<rect x="806" y="1" width="143" height="332" rx="10"/>
<text class="parcel-band-title" x="821" y="32">Report</text>
<text class="parcel-band-sub" x="821" y="56">Parcel</text>
</g>
<path class="parcel-edge" data-project-edge="folder|event" d="M116 164 H132" marker-end="url(#parcel-docs-arrow)"/>
<path class="parcel-edge" data-project-edge="event|current" d="M232 164 H240 V108 H248" marker-end="url(#parcel-docs-arrow)"/>
<path class="parcel-edge" data-project-edge="event|shortcut" d="M232 164 H386" marker-end="url(#parcel-docs-arrow)"/>
<path class="parcel-edge" data-project-edge="shortcut|consumer" d="M498 164 H514" marker-end="url(#parcel-docs-arrow)"/>
<path class="parcel-edge" data-project-source="consumer|model" d="M626 164 H666" marker-end="url(#parcel-docs-arrow)"/>
<path class="parcel-edge parcel-binding" data-project-binding="model|report" d="M778 164 H821" marker-end="url(#parcel-docs-arrow)"/>
<g class="parcel-node parcel-file" data-project-node="folder" data-logical-id="Lakehouse/Landing/Files/Parcel.Events">
<rect x="16" y="132" width="100" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:18px" x="66.0" y="156">Events</text>
<text class="parcel-node-sub" x="66.0" y="179">Python</text>
<text class="parcel-node-sub" x="66.0" y="197">Folder</text>
</g>
<g class="parcel-node parcel-table" data-project-node="event" data-logical-id="Lakehouse/Landing/Tables/Parcel.Event">
<rect x="132" y="132" width="100" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:18px" x="182.0" y="156">Event</text>
<text class="parcel-node-sub" x="182.0" y="179">Python</text>
<text class="parcel-node-sub" x="182.0" y="197">Table</text>
</g>
<g class="parcel-node parcel-table" data-project-node="current" data-logical-id="Lakehouse/Landing/Tables/Parcel.CurrentStatus">
<rect x="248" y="76" width="96" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:18px" x="296.0" y="101">Current</text>
<text class="parcel-node-title" style="font-size:18px" x="296.0" y="120">Status</text>
<text class="parcel-node-sub" x="296.0" y="139">Spark SQL</text>
</g>
<g class="parcel-node parcel-shortcut" data-project-node="shortcut" data-logical-id="Warehouse/Operations/Parcel.LakehouseEvent">
<rect x="386" y="132" width="112" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:17px" x="442.0" y="157">Lakehouse</text>
<text class="parcel-node-title" style="font-size:18px" x="442.0" y="176">Event</text>
<text class="parcel-node-sub" x="442.0" y="195">Shortcut</text>
</g>
<g class="parcel-node parcel-table" data-project-node="consumer" data-logical-id="Warehouse/Operations/Parcel.LakehouseCurrentStatus">
<rect x="514" y="132" width="112" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:17px" x="570.0" y="151">Lakehouse</text>
<text class="parcel-node-title" style="font-size:18px" x="570.0" y="168">Current</text>
<text class="parcel-node-title" style="font-size:18px" x="570.0" y="185">Status</text>
<text class="parcel-node-sub" x="570.0" y="201">T-SQL</text>
</g>
<g class="parcel-node parcel-model" data-project-node="model" data-logical-id="SemanticModel/Parcel">
<rect x="666" y="132" width="112" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:18px" x="722.0" y="156">Parcel</text>
<text class="parcel-node-sub" x="722.0" y="179">Native</text>
<text class="parcel-node-sub" x="722.0" y="197">TMDL</text>
</g>
<g class="parcel-node parcel-report" data-project-node="report" data-logical-id="Report/Parcel">
<rect x="821" y="132" width="112" height="76" rx="8"/>
<text class="parcel-node-title" style="font-size:18px" x="877.0" y="156">Parcel</text>
<text class="parcel-node-sub" x="877.0" y="179">Native</text>
<text class="parcel-node-sub" x="877.0" y="197">Report</text>
</g>
</svg>
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
