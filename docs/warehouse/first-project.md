# A first Warehouse Table and View

Keep the transformation as a T-SQL SELECT. A metadata comment tells Weaver which Table to maintain; Build generates its load work, and Load applies the rows and records the result. Here, three parcel events feed a View showing each parcel's latest status.

Use the [documented Weaver installation](../getting-started/installation.md) and a Fabric workspace where you can create or modify Warehouses. The example uses `Parcel Development`; substitute your workspace name. All shell commands after setup run from the project root.

## Give the SQL a home

Initialise the Parcel example:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --catalogue Catalogue \
  --environment Weaver \
  --warehouse Operations \
  --example Parcel
cd parcel
```

<!-- cli-capture: {"id": "10-warehouse-initialise", "title": "Initialise \u00b7 Parcel Warehouse", "start": "  Catalogue    Catalogue", "end": "Next:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Initialise · Parcel Warehouse">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>  Catalogue    Catalogue   already exists
  Environment  Weaver      already exists
  Warehouse    Operations  created
  Environment publication: deferred

Weaver project ready in ./parcel.

</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/10-warehouse-initialise.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

Initialise creates or reuses the named items and writes the SQL Table, View and validations below. This Warehouse-only project needs no Spark runtime or Environment publication. Open the generated files rather than copying these declarations.

These live captures use a built development wheel from runtime `bf908f47` in the disposable **Weaver Example** trial workspace. They do not establish published-PyPI availability. Use your workspace name; timings vary. [Capture provenance](../assets/cli-captures/manifest.json).

<details markdown="1">
<summary>See the generated workspace bindings</summary>

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
environment: Weaver

targets:
  Warehouse/Operations: Operations
```

`Warehouse/Operations` is the logical item; `Operations` is its physical Warehouse. Use your actual workspace name.

</details>

## Inspect the event Table {#write-the-event-table}

Open `Warehouse/Operations/Parcel.StatusEvent.sql`:

<!-- initialise:Warehouse/Operations/Parcel.StatusEvent.sql -->
```sql
/*
Table ID: Parcel.StatusEvent

Description: One row per parcel status event.

Lineage: A deterministic carrier feed represented by this example.

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: varchar(20)
  Event sequence: int
  Status: varchar(30)
  Depot: varchar(50)
*/
select v.[Parcel ID]
     , v.[Event sequence]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 1, 'Accepted', 'North'),
    ('P-1001', 2, 'In transit', 'Central'),
    ('P-1002', 1, 'Delivered', 'South')
) as v ([Parcel ID], [Event sequence], [Status], [Depot]);
```
<!-- /initialise -->

The key identifies one event. Keep the SQL as a SELECT; the declaration describes the Table that should receive it.

## Read the latest event through a View

Open `Warehouse/Operations/Parcel.CurrentStatus.sql`:

<!-- initialise:Warehouse/Operations/Parcel.CurrentStatus.sql -->
```sql
/*
View ID: Parcel.CurrentStatus

Description: The latest recorded status for each parcel.

Lineage: Parcel status events ordered by event sequence.
*/
with ranked as (
    select [Parcel ID]
         , [Status]
         , [Depot]
         , row_number() over (
               partition by [Parcel ID]
               order by [Event sequence] desc
           ) as [Event rank]
    from [Parcel].[StatusEvent]
)
select [Parcel ID]
     , [Status]
     , [Depot]
from ranked
where [Event rank] = 1;
```
<!-- /initialise -->

The View reads the event Table and keeps the most recent row for each parcel.

## Install the definitions, then load the rows

**Use disposable targets.** Build manages the selected item and may prune undeclared co-located content. Keep irreplaceable sources in a separate physical item; [target ownership](schema-and-protection.md#keep-the-source-outside-the-managed-target) explains the boundary.

```bash
weaver check
```

<!-- cli-capture: {"id": "11-warehouse-check", "title": "Check \u00b7 local project"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Check · local project">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Project valid.
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/11-warehouse-check.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

Install the definitions:

```bash
weaver build --item Warehouse/Operations
```

<!-- cli-capture: {"id": "12-warehouse-build", "title": "Build \u00b7 first Warehouse installation", "start": "Installation", "full": true} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · first Warehouse installation">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Installation
<span class="terminal-status-green">   18 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  9b8429565c5101b39fdec126ffe26eb858fc30d94f6c2e0af1a0d80bad9055c9
</code></pre>
<details><summary>Show the complete capture</summary><pre tabindex="0" aria-label="Captured terminal output"><code>Workspace  Weaver Example
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

Build

  Check target occupancy                                                                                   0.0s

  Resolve semantic data sources                                                                            0.0s

  Read catalogue                                                                                           6.1s

    Read Warehouse/Operations inventory                                                                    0.9s

    Read Warehouse/Catalogue inventory                                                                     0.2s

  Read target inventories                                                                                  1.1s

  Read semantic sources                                                                                    0.0s

  Prepare bundle                                                                                           0.2s

Install selection
  Warehouse/Operations
    new                     13
    selected for build      13

→   Warehouse/Catalogue · Upgrade catalogue identity and semantic keys · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Upgrade catalogue identity and semantic keys · 1 action                         16.2s</span>

→   Warehouse/Catalogue · Removing superseded catalogue entries · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Removing superseded catalogue entries · 1 action                                 3.9s</span>

→   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action                          2.0s</span>

→   Warehouse/Operations · Creating schemas · 2 actions

→   Warehouse/Catalogue · Removing unmanaged objects · 2 actions

→   Warehouse/Operations · Building objects · 1 action

<span class="terminal-status-green">✓   Warehouse/Operations · Creating schemas · 2 actions                                                    0.5s</span>

→   Warehouse/Operations · Creating shortcuts · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Removing unmanaged objects · 2 actions                                           0.5s</span>

<span class="terminal-status-green">✓   Warehouse/Operations · Creating shortcuts · 1 action                                                   0.1s</span>

→   Warehouse/Operations · Installing load and test artefacts · 5 actions

<span class="terminal-status-green">✓   Warehouse/Operations · Building objects · 1 action                                                     1.6s</span>

→   Warehouse/Operations · Building objects · 1 action

<span class="terminal-status-green">✓   Warehouse/Operations · Building objects · 1 action                                                     0.0s</span>

<span class="terminal-status-green">✓   Warehouse/Operations · Installing load and test artefacts · 5 actions                                  1.1s</span>

→   Warehouse/Catalogue · Recording created Views · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Recording created Views · 1 action                                               0.5s</span>

→   Warehouse/Catalogue · Updating catalogue definitions · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Updating catalogue definitions · 1 action                                        7.8s</span>

→   Warehouse/Catalogue · Finalising catalogue · 1 action

<span class="terminal-status-green">✓   Warehouse/Catalogue · Finalising catalogue · 1 action                                                  0.6s</span>

  Install                                                                                                 32.7s

<span class="terminal-status-green">✓ Build                                                                                                   52.9s</span>

Installation
<span class="terminal-status-green">   18 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  9b8429565c5101b39fdec126ffe26eb858fc30d94f6c2e0af1a0d80bad9055c9
</code></pre></details><p class="terminal-source"><a href="../../assets/cli-captures/12-warehouse-build.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

Load the event rows:

```bash
weaver load Warehouse/Operations
```

<!-- cli-capture: {"id": "13-warehouse-load", "title": "Load \u00b7 first event rows", "start": "Load summary", "end": "  Workflow:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · first event rows">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code>Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   3
    inserted               3
    updated                0
    deleted                0
    rejected               0

</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/13-warehouse-load.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

Run the generated validations, then inspect the installed result:

```bash
weaver test Warehouse/Operations
```

<!-- cli-capture: {"id": "14-warehouse-test", "title": "Test \u00b7 generated validations", "start": "test passed", "end": "  Workflow:"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · generated validations">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code><span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    2 passed</span>
    0 failed
</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/14-warehouse-test.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->

```bash
weaver health --item Warehouse/Operations
```

<!-- cli-capture: {"id": "15-warehouse-health", "title": "Health \u00b7 loaded and tested Warehouse", "start": "Weaver Health", "end": "Slowest loads"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · loaded and tested Warehouse">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Captured terminal output"><code><span class="terminal-status-green">Weaver Health  Green</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 0m ago
<span class="terminal-status-green">  1 succeeded</span>

<span class="terminal-status-green">Tests   Green</span>
<span class="terminal-status-green">  2 succeeded</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (10 objects)

</code></pre>
<p class="terminal-source"><a href="../../assets/cli-captures/15-warehouse-health.txt">Sanitised transcript</a> · <a href="../../assets/cli-captures/manifest.json">Capture details</a> · Transcript excerpt · Live CLI capture; progress redraws omitted.</p>
</figure>
<!-- /cli-capture -->


In a SQL query connected to **Operations**, read the View:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

## What happened around the SELECT

Build created the physical Table, generated its loading procedure and installed the dependent View. The SQL reference supplied the dependency; `Lineage` is descriptive. Load staged the query result, matched keys and reconciled changed values according to the Table’s policy. It also recorded the row changes and processing state for Health. You wrote neither an INSERT/MERGE procedure nor a second load-order definition.

The View now gives you one row per parcel, but a successful Load does not prove that it chose the right event. [Testing Warehouse data](tests.md) runs the generated independent expected result and check for unknown statuses to this same project, without initialising another one.

If you edit either SQL document, Check and Build install the changed definition before another Load. [The development cycle](../estate/development-cycle.md) covers that loop; [Table reference](../reference/weaver-documents/table.md) owns the exact authoring and load contract.
