# A first Warehouse Table and View

Keep the transformation as a T-SQL SELECT. A metadata comment tells Weaver which Table to maintain; Build generates its load work, and Load applies the rows and records the result. Here, three parcel events feed a View showing each parcel's latest status.

You need [Weaver installed](../getting-started/installation.md) and a Fabric workspace on running capacity where you can create Warehouses. The example uses a workspace called `Parcel Development`; substitute your own. Use a disposable workspace for the tutorials: Build owns the Warehouses it manages and removes objects you did not declare there.

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

<!-- cli-capture: {"id": "10-warehouse-initialise", "title": "Initialise · Parcel Warehouse"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Initialise · Parcel Warehouse">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Set up a Weaver project.

Lakehouse (optional)
Use a Lakehouse for files and Python/Delta tables.
Press Enter if this project does not need one.
Examples: Landing, Bronze
Lakehouse:

Project

  Project folder  ./parcel
  Workspace       Parcel Development
  Catalogue       Catalogue
  Environment     Weaver
  Lakehouse       None
  Warehouse       Operations
  Example         Parcel
  Semantic Model  None

1. Continue
2. Change an answer
3. Cancel
Choose [1/2/3]: 1
Publishing a Fabric Environment can take about 5 minutes.
Publish the Environment now? [y/N]: n

Setting up the Weaver project

  Checking the workspace                                                                                   0.3s
  Reading the Environment                                                                                  0.0s
  Checking the project files                                                                               0.1s
  Creating the Catalogue Catalogue                                                                        11.6s
  Creating the Warehouse Operations                                                                        5.1s
  Writing the project files                                                                                0.0s
  Creating the Environment Weaver                                                                         21.2s
<span class="terminal-status-green">✓ Setting up the Weaver project                                                                           38.4s</span>

  Catalogue    Catalogue   created
  Environment  Weaver      created
  Warehouse    Operations  created
  Environment publication: deferred

Weaver project ready in [local-path]/parcel.

Next:

  cd [local-path]/parcel

Environment publication deferred.
Publish it before the first load that runs Python.

  weaver fabric environment publish --path Environment/Weaver.Environment
  weaver workflow full

Or run individually:
  weaver build
  weaver load
  weaver test
  weaver health

You can set this up again with:

  weaver initialise --workspace &#x27;Parcel Development&#x27; --project-folder ./parcel --catalogue Catalogue --environment Weaver --warehouse Operations --example Parcel --non-interactive
</code></pre>
</figure>
<!-- /cli-capture -->

The Terminal wizard asks one question you did not answer on the command line: press Enter to skip the Lakehouse, choose `1` to continue, and answer `n` to publishing the Environment. A Warehouse-only project runs no Python in Fabric, so it needs no published Environment yet, even though the closing hint mentions one.

Initialise created the Catalogue and Operations Warehouses and wrote the SQL Table, View and validations below. Run every later command from the `parcel` folder. Open the generated files as you read; you do not need to copy them.

<details markdown="1">
<summary>See the generated workspace bindings</summary>

```yaml title="workspace-config.yml"
workspace: Parcel Development
environment: Weaver
catalogue: Warehouse/Catalogue

targets:
  Warehouse/Operations: Operations
```

`Warehouse/Operations` is the logical item your project names; `Operations` is the physical Warehouse it deploys to. `catalogue` is the Warehouse where Weaver records what it installed and ran.

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

Check the project locally first. It reads the declarations and their dependencies without contacting Fabric:

```bash
weaver check
```

<!-- cli-capture: {"id": "11-warehouse-check", "title": "Check · local project"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Check · local project">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Project valid.
</code></pre>
</figure>
<!-- /cli-capture -->

Build installs the definitions. Because Build owns `Operations`, keep data you cannot recreate in a separate item; [target ownership](schema-and-protection.md#keep-the-source-outside-the-managed-target) explains why.

```bash
weaver build --item Warehouse/Operations
```

<!-- cli-capture: {"id": "12-warehouse-build", "title": "Build · first Warehouse installation"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · first Warehouse installation">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations


Build

  Check target occupancy                                                                                   0.0s
  Resolve semantic data sources                                                                            0.0s
  Read catalogue                                                                                           0.0s
    Read Warehouse/Operations inventory                                                                    0.8s
    Read Warehouse/Catalogue inventory                                                                     0.2s
  Read target inventories                                                                                  1.1s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.5s
Install selection
  Warehouse/Operations
    new                     13
    selected for build      13

→   Warehouse/Catalogue · Creating schemas · 1 action
→   Warehouse/Operations · Creating schemas · 2 actions
→   Warehouse/Operations · Building objects · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Creating schemas · 1 action                                                      0.0s</span>
→   Warehouse/Catalogue · Building objects · 24 actions
<span class="terminal-status-green">✓   Warehouse/Operations · Creating schemas · 2 actions                                                    0.7s</span>
<span class="terminal-status-green">✓   Warehouse/Operations · Building objects · 1 action                                                     4.9s</span>
→   Warehouse/Operations · Building objects · 1 action
<span class="terminal-status-green">✓   Warehouse/Operations · Building objects · 1 action                                                     0.0s</span>
<span class="terminal-status-green">✓   Warehouse/Catalogue · Building objects · 24 actions                                                   10.9s</span>
→   Warehouse/Operations · Creating shortcuts · 1 action
<span class="terminal-status-green">✓   Warehouse/Operations · Creating shortcuts · 1 action                                                   0.2s</span>
→   Warehouse/Operations · Installing load and test artefacts · 5 actions
<span class="terminal-status-green">✓   Warehouse/Operations · Installing load and test artefacts · 5 actions                                  0.3s</span>
→   Warehouse/Catalogue · Recording created Views · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Recording created Views · 1 action                                               3.5s</span>
→   Warehouse/Catalogue · Updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Updating catalogue definitions · 1 action                                        8.3s</span>
→   Warehouse/Catalogue · Finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Finalising catalogue · 1 action                                                  0.7s</span>
  Install                                                                                                 24.1s
<span class="terminal-status-green">✓ Build                                                                                                   28.9s</span>

Installation
<span class="terminal-status-green">   38 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  6be8993fb78d73585788794aaf4c7638d5811b025da54dbc0df9df3117975d19
</code></pre>
</figure>
<!-- /cli-capture -->

Load the event rows:

```bash
weaver load Warehouse/Operations
```

<!-- cli-capture: {"id": "13-warehouse-load", "title": "Load · first event rows"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · first event rows">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           3.5s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
→   Load Warehouse/Operations/Parcel.StatusEvent
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +3 ~0 -0 !0)                                    4.9s</span>
  Execute                                                                                                  5.0s
  Record what the run did                                                                                  0.7s
<span class="terminal-status-green">✓ Load                                                                                                     9.2s</span>

<span class="terminal-status-green">load succeeded: Warehouse/Operations</span>

Load summary
<span class="terminal-status-green">    1 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   3
    inserted               3
    updated                0
    deleted                0
    rejected               0

  Workflow: 117a9e4b54d34e759857595f1a0ac3a8
</code></pre>
</figure>
<!-- /cli-capture -->

Run the two generated validations, then read Health, Weaver's summary of what is installed and what ran:

```bash
weaver test Warehouse/Operations
```

<!-- cli-capture: {"id": "14-warehouse-test", "title": "Test · generated validations"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · generated validations">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read catalogue                                                                                           3.0s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Warehouse/Operations

  Build run graph                                                                                          0.0s
→   Test Warehouse/Operations/Parcel.CurrentStatusMatches
→   Test Warehouse/Operations/Parcel.StatusIsKnown
<span class="terminal-status-green">✓   Test Warehouse/Operations/Parcel.StatusIsKnown                                                         1.7s</span>
<span class="terminal-status-green">✓   Test Warehouse/Operations/Parcel.CurrentStatusMatches                                                  7.7s</span>
  Execute                                                                                                  7.9s
  Record what the run did                                                                                  0.9s
<span class="terminal-status-green">✓ Test                                                                                                    11.8s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    2 passed</span>
    0 failed
  Workflow: 487b69ed9b984916b74bdc7e3243fcd7
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver health --item Warehouse/Operations
```

<!-- cli-capture: {"id": "15-warehouse-health", "title": "Health · loaded and tested Warehouse"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · loaded and tested Warehouse">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           3.7s
  Check installed items                                                                                    0.1s
  Read installed objects                                                                                   0.6s
<span class="terminal-status-green">✓ Health                                                                                                   4.5s</span>

<span class="terminal-status-green">Weaver Health  Green</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 0m ago
<span class="terminal-status-green">  1 succeeded</span>

<span class="terminal-status-green">Tests   Green</span>
<span class="terminal-status-green">  2 succeeded</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (10 objects)

Slowest loads
  Warehouse/Operations/Parcel.StatusEvent     4.9s

Largest changes
  Warehouse/Operations/Parcel.StatusEvent     read 3  +3 ~0 -0 !0
</code></pre>
</figure>
<!-- /cli-capture -->


In the Fabric portal, open the **Operations** Warehouse, choose **New SQL query** and read the View:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | In transit | Central |
| P-1002 | Delivered | South |

P-1001 has two events; the View keeps the later one.

## What happened around the SELECT

Build created the physical Table, generated its loading procedure and installed the dependent View. The SQL reference supplied the dependency; `Lineage` is descriptive. Load staged the query result, matched keys and reconciled changed values according to the Table’s policy. It also recorded the row changes and processing state for Health. You wrote neither an INSERT/MERGE procedure nor a second load-order definition.

The View now gives you one row per parcel. [Testing Warehouse data](tests.md) explains the two validations you just ran and shows what a failing one looks like.

If you edit either SQL document, Check and Build install the changed definition before another Load. [The development cycle](../estate/development-cycle.md) covers that loop; [Table reference](../reference/weaver-documents/table.md) owns the exact authoring and load contract.
