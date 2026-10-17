# Control concurrency

Can this run use less simultaneous work? Add `--concurrency 2` to limit it to two scheduled nodes. Leave the setting out when the normal configured limits are appropriate.

## Limit one run

Continue the Landing/Operations project from [selective runs](selective-runs.md), keeping `workspace-development.yml`. Cap its Landing Load at two scheduled nodes:

```bash
weaver load Lakehouse/Landing --concurrency 2 --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "64-concurrency-two-load", "title": "Load · invocation capped at two nodes"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Load · invocation capped at two nodes">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Load

  Read catalogue                                                                                           2.5s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
  Wait for Spark session                                                                                  35.9s
→   Load Lakehouse/Landing/Files/Parcel.Events
→   Load Lakehouse/Landing/Files/Parcel.StatusFiles
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Files/Parcel.Events  (read 1, +0 ~0 -0 !0)                                      3.0s</span>
→   Load Lakehouse/Landing/Tables/Parcel.Event
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Files/Parcel.StatusFiles  (read 1, +0 ~0 -0 !0)                                 3.1s</span>
→   Load Lakehouse/Landing/Tables/Parcel.LiveStatus
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.LiveStatus  (read 0, +0 ~0 -0 !0)                                 0.2s</span>
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.Event  (read 3, +0 ~0 -0 !0)                                     14.4s</span>
→   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus
<span class="terminal-status-green">✓   Load Lakehouse/Landing/Tables/Parcel.CurrentStatus  (read 2, +0 ~0 -0 !0)                              7.1s</span>
  Execute                                                                                                 22.8s
  Record what the run did                                                                                  0.0s
<span class="terminal-status-green">✓ Load                                                                                                    1m09s</span>

<span class="terminal-status-green">load succeeded: Lakehouse/Landing</span>

Load summary
<span class="terminal-status-green">    5 succeeded</span>
    0 failed
    0 blocked
  Rows
    read                   7
    inserted               0
    updated                0
    deleted                0
    rejected               0

  Workflow: 64a5966c5760456093c5c15975f95fe3
</code></pre>
</figure>
<!-- /cli-capture -->

The dependency chain still ran in order. A cap of two permits two ready nodes; it does not make this chain parallel.

Build and Test accept the same positive-integer option:

```bash
weaver build --item Lakehouse/Landing --concurrency 2 --workspace-config workspace-development.yml
weaver test Lakehouse/Landing --concurrency 2 --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "66-concurrency-two-test", "title": "Test · two independent validations"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · two independent validations">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read catalogue                                                                                           2.9s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing

  Build run graph                                                                                          0.0s
  Wait for Spark session                                                                                  38.9s
→   Test Lakehouse/Landing/Parcel.CurrentStatusMatches
→   Test Lakehouse/Landing/Parcel.EventStatusIsKnown
<span class="terminal-status-green">✓   Test Lakehouse/Landing/Parcel.EventStatusIsKnown                                                      11.2s</span>
<span class="terminal-status-green">✓   Test Lakehouse/Landing/Parcel.CurrentStatusMatches                                                    13.8s</span>
  Execute                                                                                                 12.7s
  Record what the run did                                                                                  0.0s
<span class="terminal-status-green">✓ Test                                                                                                    1m02s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    2 passed</span>
    0 failed
  Workflow: cee836b15e044193b9d0f2ed606bb84b
</code></pre>
</figure>
<!-- /cli-capture -->

Here both validations started before either finished. The cap applies across the invocation, not separately to each item. With two Warehouses and a total cap of two, there are still at most two simultaneous scheduled nodes, not four. Dependencies and resource ceilings can keep actual concurrency lower.

The option does not change workspace configuration, retarget a bundle or rewrite its plan. Omission keeps the configured/default behaviour. It does not set Spark capacity, executor count or cluster size, and does not limit every nested HTTP request.

## Use the same cap in Python

```python
import weaver

workspace = weaver.current_workspace(workspace_config='workspace-development.yml').workspace
result = weaver.build(
    '.',
    workspace=workspace,
    items='Lakehouse/Landing',
    concurrency=2,
    workspace_config='workspace-development.yml',
)
if not result.succeeded:
    raise RuntimeError(result.errors)
result.to_mapping()
```

In a Fabric notebook, pass the supported project source location and let Weaver discover the notebook context, or reuse an established Session:

```python
import weaver

workspace = weaver.current_workspace(workspace_config='workspace-development.yml').workspace
report = weaver.load('Lakehouse/Landing', workspace=workspace, workspace_config='workspace-development.yml', concurrency=2)
if not report.succeeded:
    raise RuntimeError('Inspect the failed nodes in the Load report')
report.to_mapping()
```

Workspace selection and runtime prerequisites still apply. The invocation cap does not provision compute or make otherwise unavailable work runnable.

Source/file-mode Tests are serial by default. Explicit concurrency lets them use the run scheduler, subject to their resource limits. A cap limits scheduled work, not the number of DAX queries a single validation contains.

## Tune persistent resource limits only when needed

Build limits and run limits are separate. This is a **reference illustration of the defaults**, not configuration every project must paste:

```yaml
execution:
  build:
    warehouse_concurrency: 2
    spark_concurrency: 4
    onelake_concurrency: 8
    shortcut_concurrency: 2
  run:
    spark_concurrency: 4
    warehouse_concurrency: 4
```

Warehouse limits apply per Warehouse. Spark run lanes can use separate Spark sessions within one Spark application; they are not a newly provisioned cluster for each table. Build's other ceilings govern storage and shortcut work. An invocation cap remains the overall ceiling on top of those limits.

There is no `execution.test`, target-level `parallel_workers` setting or `--spark-concurrency` CLI flag. Use [workspace configuration](../reference/configuration-files/workspace-config.md) for accepted keys and precedence.

## Measure before increasing a limit

Use enough independent work for the cap to matter. A single dependency chain will not become parallel merely because the number increases.

Compare a fixed workload, record waits, outcomes and resource usage, and change one setting at a time. More concurrency can increase contention or throttling. The historical F64 benchmark used 24 Spark lanes and 12 per Warehouse; these are not defaults, small-capacity recommendations or hard maxima.

## Related tasks

- [Investigate performance and scale](performance.md).
- [Run part of an estate](selective-runs.md).
- [Look up Build, Load and Test options](../reference/cli.md).
