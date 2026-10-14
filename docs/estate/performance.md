# Investigate performance and scale

First establish what the run is doing. Work that moves rows, waits for a service and repeats setup needs different remedies.

## 1. Keep the comparison fixed

Record the Weaver revision/package, capacity, selected items, source and target state, run mode and resource limits. Compare the same workload before changing one setting. Separate a first Load, an unchanged Load and incremental change; they answer different questions.

Use normal operation reports to identify attempted, succeeded, failed and blocked work. A short run that omitted necessary work is not a performance improvement.

## 2. Separate work, waits and overhead

Use a Session or workflow's Fabric access timings:

```bash
weaver session --workspace-config workspace-dev.yml --timings
```

Inside the Session, run the operation you are investigating, then exit to see its access timings. The accepted `verify` sequence from [workflows](automation-and-deployment.md#turn-the-accepted-sequence-into-a-workflow) can report timings with:

```bash
weaver workflow verify --workspace-config workspace-dev.yml --timings
```

Review the workflow's commands and confirmation before running it. `--timings` belongs to Session and Workflow, not an invented Load flag. For catalogue-backed work, inspect the per-node report, `_.Log` and `_.LoadStatistic` alongside current status. History is not the same as current health.

Ask where time went:

| Observation | Check next |
| --- | --- |
| Long row-processing nodes | Change volume, incremental query shape, source access and target reconciliation |
| Ready work waiting for a lane | Dependency shape and resource/total concurrency ceilings |
| Long endpoint/readiness waits | The tables actually read through that endpoint and current service readiness |
| Many tiny nodes with little row movement | Repeated session, metadata, storage and scheduling overhead |
| A node failed or was blocked | Correct that condition before treating its short runtime as evidence |

## 3. Adjust the work, not just the lane count

Independent work can run concurrently, but its source dependencies and service limits still govern admission. More lanes do not shorten a serial chain or repair a slow source query. Use [Control concurrency](concurrency.md) to set a total invocation cap or resource limits for the item that is constrained.

Weaver shares repeated setup, batches supported access and coordinates endpoint readiness with the Tables actually needed downstream. For a model refresh, check both the upstream source load and the model’s service refresh: the run report puts them in the same graph.

## A measured estate

An observed synthetic workload of around 3,000 objects on F64, with one Lakehouse and two Warehouses, completed its first Load in about an hour. The later measured incremental Loads completed in under 15 minutes. The workload inserted about 4 billion rows across its layers; those are estate insertions, not distinct source records. These observations are not a service SLA or a duration promised for another workload.

Use that as context, then measure your own project with its data shape, source access and capacity. Keep first-load and incremental timings separate when comparing changes.

## Related tasks

- [Limit simultaneous work](concurrency.md).
- [Run only the relevant part](selective-runs.md).
- [Inspect row auditing and operational history](../advanced/row-auditing-and-operational-history.md).
