# Control concurrency

Can this run use less simultaneous work? Add `--concurrency 2` to limit it to two scheduled nodes. Leave the setting out when the normal configured limits are appropriate.

## Limit one run

Continue the Landing/Operations project from [selective runs](selective-runs.md), keeping `workspace-development.yml`. Cap its Landing Load at two scheduled nodes:

```bash
weaver load Lakehouse/Landing --concurrency 2 --workspace-config workspace-development.yml
```

Build and Test accept the same positive-integer option:

```bash
weaver build . --item Lakehouse/Landing --concurrency 2 --workspace-config workspace-development.yml
weaver test Lakehouse/Landing --concurrency 2 --workspace-config workspace-development.yml
```

The cap applies across the invocation, not separately to each item. With two Warehouses and a total cap of two, there are still at most two simultaneous scheduled nodes, not four. Dependencies and resource ceilings can keep actual concurrency lower.

The option does not change workspace configuration, retarget a bundle or rewrite its plan. Omission keeps the configured/default behaviour. It does not set Spark capacity, executor count or cluster size, and does not limit every nested HTTP request.

## Use the same cap in Python

```python
import weaver

result = weaver.build(
    '.',
    items='Lakehouse/Landing',
    concurrency=2,
    workspace_config='workspace-development.yml',
)
if not result.succeeded:
    raise RuntimeError(result.errors)
```

In a Fabric notebook, pass the supported project source location and let Weaver discover the notebook context, or reuse an established Session:

```python
import weaver

report = weaver.load('Lakehouse/Landing', concurrency=2)
if not report.succeeded:
    raise RuntimeError('Inspect the failed nodes in the Load report')
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
