# Connect items and dependencies

What should a Warehouse read when the data comes from a Lakehouse? Name the existing producer in a logical Shortcut. Weaver installs the connection in order and keeps its dependency with the project.

You need both items in the same `parcel` project. If you followed the Warehouse and Lakehouse tasks in order, you already have them: [adding Landing](../lakehouse/python.md#create-the-project) also generated the Warehouse files below. Otherwise, add the item you are missing from inside `parcel`:

=== "Started with the Lakehouse"

    ```bash
    weaver initialise --workspace "Parcel Development" --project-folder . --warehouse Operations --example Parcel
    ```

=== "Started with the Warehouse"

    ```bash
    weaver initialise --workspace "Parcel Development" --project-folder . --lakehouse Landing --example Parcel
    ```

    Then publish the Environment and Build Landing as in the [first Lakehouse task](../lakehouse/python.md#check-build-and-load).

Initialise reads the existing bindings and keeps every file you already have. If you have authored a `shortcuts.yml`, such as the [incremental task's](../warehouse/incremental.md) physical mapping, Initialise adds its logical mapping beside yours.

Operations keeps its own seeded `Parcel.StatusEvent` Table, CurrentStatus View and validations. The cross-item additions have distinct names. Open `Warehouse/Operations/shortcuts.yml`:

<!-- initialise:Warehouse/Operations/shortcuts.yml -->
```yaml
logical:
  Warehouse/Operations/Parcel.LakehouseEvent: Lakehouse/Landing/Tables/Parcel.Event
```
<!-- /initialise -->

The mapping reads from destination to source. Build presents Landing’s Event Table through the logical `Parcel.LakehouseEvent` Shortcut View. This does not replace StatusEvent.

Open `Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql` to see the additional loadable Table:

<!-- initialise:Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql -->
```sql
/*
Table ID: Parcel.LakehouseCurrentStatus

Primary key: Parcel ID

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
  Depot: varchar(50)

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
    from [Parcel].[LakehouseEvent]
)
select [Parcel ID]
     , [Status]
     , [Depot]
from ranked
where [Event rank] = 1;
```
<!-- /initialise -->

The SQL reference connects this new Table to Landing. Build orders the selected source and Shortcut; Load waits for the supported SQL-endpoint readiness boundary before the Warehouse reads the Lakehouse.

```bash
weaver check
weaver build --item Lakehouse/Landing --item Warehouse/Operations
```

<!-- cli-capture: {"id": "51-cross-item-build", "title": "Build · connect the two managed items"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Build · connect the two managed items">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing
  Warehouse/Operations


Build

  Check target occupancy                                                                                   0.0s
  Resolve semantic data sources                                                                            0.0s
  Read catalogue                                                                                           2.9s
    Read Warehouse/Operations inventory                                                                    0.8s
    Read Warehouse/Catalogue inventory                                                                     0.1s
    Read Lakehouse/Landing inventory  (32.4s waiting for Spark)                                           40.1s
  Read target inventories                                                                                 41.0s
  Resolve physical shortcut targets                                                                        0.2s
  Read semantic sources                                                                                    0.0s
  Prepare bundle                                                                                           0.1s
Install selection
  Lakehouse/Landing         up to date
  Warehouse/Operations
    new                     3
    selected for build      3

→   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Reconcile runtime state before physical work · 1 action                          1.0s</span>
→   Warehouse/Operations · Creating shortcuts · 2 actions
<span class="terminal-status-green">✓   Warehouse/Operations · Creating shortcuts · 2 actions                                                  0.2s</span>
→   Warehouse/Operations · Building objects · 1 action
<span class="terminal-status-green">✓   Warehouse/Operations · Building objects · 1 action                                                     1.1s</span>
→   Warehouse/Operations · Installing load and test artefacts · 1 action
<span class="terminal-status-green">✓   Warehouse/Operations · Installing load and test artefacts · 1 action                                   0.1s</span>
→   Warehouse/Catalogue · Updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Updating catalogue definitions · 1 action                                        3.8s</span>
→   Warehouse/Catalogue · Finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/Catalogue · Finalising catalogue · 1 action                                                  0.5s</span>
  Install                                                                                                  6.6s
<span class="terminal-status-green">✓ Build                                                                                                   52.6s</span>

Installation
<span class="terminal-status-green">    7 succeeded</span>
    0 failed
    0 skipped
  Report  [local-path]
  Bundle  e55d88243fcd6225d6ab1d0b3d670524b56c5aee49e04210edcf4cfb1ed51255
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver load Lakehouse/Landing Warehouse/Operations
```

<!-- cli-capture: {"id": "52-cross-item-load", "title": "Load · Lakehouse producer and Warehouse consumer"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · Lakehouse producer and Warehouse consumer">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           3.1s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing
  Warehouse/Operations

  Build run graph                                                                                          0.0s
  Wait for Spark session                                                                                  39.5s
→   Load Lakehouse/Landing/Files/Parcel.Events
→   Load Warehouse/Operations/Parcel.LiveStatus
→   Load Warehouse/Operations/Parcel.StatusEvent
→   Load Lakehouse/Landing/Files/Parcel.StatusFiles
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Files/Parcel.Events  (read 1, +0 ~0 -0 !0)                                      2.8s</span>
→   Load Lakehouse/Landing/Tables/Parcel.Event
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Files/Parcel.StatusFiles  (read 1, +0 ~0 -0 !0)                                 2.9s</span>
→   Load Lakehouse/Landing/Tables/Parcel.LiveStatus
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.LiveStatus  (read 0, +0 ~0 -0 !0)                                 0.2s</span>
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LiveStatus  (read 0, +0 ~0 -0 !0)                                     5.0s</span>
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.StatusEvent  (read 3, +0 ~0 -0 !0)                                    5.0s</span>
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +0 ~0 -0 !0)                                     12.8s</span>
→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus
→   Refresh Lakehouse/Landing SQL endpoint
<span class="terminal-status-green">✓   Refresh Lakehouse/Landing SQL endpoint                                                                 0.8s</span>
→   Load Warehouse/Operations/Parcel.LakehouseCurrentStatus
<span class="terminal-status-green">✓   Load Warehouse/Operations/Parcel.LakehouseCurrentStatus  (read 2, +2 ~0 -0 !0)                         2.0s</span>
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +0 ~0 -0 !0)                              7.6s</span>
  Execute                                                                                                 21.3s
  Record what the run did                                                                                  0.0s
<span class="terminal-status-green">✓ Load                                                                                                    1m13s</span>

<span class="terminal-status-green">load succeeded: Lakehouse/Landing, Warehouse/Operations</span>

Load summary
<span class="terminal-status-green">    8 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                  12
    inserted               2
    updated                0
    deleted                0
    rejected               0

  Workflow: 46cba535cdd3454fadece85ceefbaf3c
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver health --item Lakehouse/Landing --item Warehouse/Operations
```

<!-- cli-capture: {"id": "53-cross-item-health", "title": "Health · loaded data needs current validations"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · loaded data needs current validations">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           2.8s
  Check installed items                                                                                    0.2s
  Read installed objects                                                                                   3.2s
<span class="terminal-status-green">✓ Health                                                                                                   6.1s</span>

<span class="terminal-status-amber">Weaver Health  Amber</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 0m ago
<span class="terminal-status-green">  8 succeeded</span>

<span class="terminal-status-amber">Tests   Amber</span>
<span class="terminal-status-green">  4 succeeded</span>
<span class="terminal-status-amber">  Amber  Lakehouse/Landing/Parcel.CurrentStatusMatches</span>
<span class="terminal-status-green">          Lakehouse/Landing/Files/Parcel.Events has been loaded since this validation passed</span>
<span class="terminal-status-amber">  Amber  Lakehouse/Landing/Parcel.EventStatusIsKnown</span>
<span class="terminal-status-green">          Lakehouse/Landing/Files/Parcel.Events has been loaded since this validation passed</span>
<span class="terminal-status-amber">  Amber  Warehouse/Operations/Parcel.CurrentStatusMatches</span>
<span class="terminal-status-green">          Warehouse/Operations/Parcel.StatusEvent has been loaded since this validation passed</span>
<span class="terminal-status-amber">  Amber  Warehouse/Operations/Parcel.StatusIsKnown</span>
<span class="terminal-status-green">          Warehouse/Operations/Parcel.StatusEvent has been loaded since this validation passed</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (29 objects)

Slowest loads
  Lakehouse/Landing/Tables/Parcel.Event          12.8s
  Lakehouse/Landing/Tables/Parcel.CurrentStatus  7.6s
  Warehouse/Operations/Parcel.StatusEvent        5.0s
  Warehouse/Operations/Parcel.LiveStatus         5.0s
  Lakehouse/Landing/Files/Parcel.StatusFiles     2.9s

Largest changes
  Warehouse/Operations/Parcel.LakehouseCurrentStatus  read 2  +2 ~0 -0 !0
</code></pre>
</figure>
<!-- /cli-capture -->

Load and Build are Green. Tests are Amber even though their previous runs succeeded: the source data was loaded after those runs. [Run the installed validations](operate.md#3-run-installed-validations) before treating those results as current. Health exits non-zero while it reports these findings; that is not a failed Load.

In Operations’s SQL query editor:

```sql
SELECT [Parcel ID], [Status], [Depot]
FROM Parcel.LakehouseCurrentStatus
ORDER BY [Parcel ID];
```

Expect P-1001 / In transit / Central and P-1002 / Delivered / South. `Parcel.CurrentStatus` still reads Operations’s independent seeded StatusEvent Table. `Parcel.LakehouseCurrentStatus` reads Landing’s managed data. Their names keep those meanings separate.

The source identity in `shortcuts.yml` stays unchanged when [workspace mappings](environments.md) choose different physical destinations.

## Order selected work, not every related item

Python imports and supported Warehouse SQL references normally supply document dependencies without a second authored graph. An explicit `Dependencies` declaration replaces inference, including an empty list. Spark SQL data documents still require that field explicitly. The item graph must be acyclic.

For a connection with loadable work on both sides, select both logical items in an item-wide Load. Weaver orders selected producers before consumers and inserts supported OneLake-publication and SQL-endpoint readiness barriers where the installed cross-engine path requires them. The Shortcut View has no separate Load, but its consuming LakehouseCurrentStatus Table does. Name both Landing and Operations when you want that selected cross-item work ordered together.

Dependencies never add an unnamed item. Build changes affected descendants only inside selected items; item-wide Load orders only its selected work. Plain `--name` Load is an operator override without inferred dependency ordering or readiness barriers. [Run part of an estate](selective-runs.md) shows how deliberate ancestor/descendant expansion restores ordering within the requested boundary.

A physical Shortcut or a directly qualified external relation is different: it identifies data outside this project’s ownership, not a managed producer that Weaver can Build or order. See [Shortcuts and existing data](../lakehouse/shortcuts.md) for that boundary and [Dependencies](../core-concepts/dependencies.md) for the complete reasoning.

## Extend the same coordination to a model

A semantic model’s `Weaver.Source` annotation can connect its Table to a managed source. Estate Load then places selected source work before model refresh, and Health can show a model behind its source. A linked Report depends on the model for deployment, but has no data Load or Test of its own.

Add `--semantic-model Parcel --example Parcel` with Initialise against this same folder to generate the independent inline model and Report plus separately named `ParcelLakehouse` and `ParcelWarehouse` models. Build source items before source-backed models, using an existing approved service connection. [Connect a managed Fabric source](../semantic-models/managed-sources.md) explains the additional models; it never replaces the native Delivery partition.

Once the connections work, [map development and production](environments.md) without changing those logical source identities. [How Weaver works](../core-concepts/how-weaver-works.md) follows the source into installed operations; [Design philosophy](../core-concepts/design-philosophy.md) explains the choices behind keeping native authoring and queryable state.
