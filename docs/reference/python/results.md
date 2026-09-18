# Python result and report types

Operations return frozen result and report values. Import every type on this page from `weaver`; nested implementation types named in annotations are not additional public import paths.

The constructors below describe the returned shape and are useful in tests. Normal application code receives these values from the corresponding operation. `to_mapping()` methods produce the operation's current machine representation, but this page does not promise a version-independent JSON schema. See [Build, Load and Test](../../core-concepts/build-load-and-test.md) for lifecycle semantics and the operation's [CLI reference](../cli.md) for command behaviour.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

- `weaver.BuildResult` — class
- `weaver.ExampleOutcome` — class
- `weaver.FabricItemOutcome` — class
- `weaver.HealthFinding` — class
- `weaver.HealthReport` — class
- `weaver.HealthSection` — class
- `weaver.InitialiseReport` — class
- `weaver.LoadActivity` — class
- `weaver.LoadMessage` — class
- `weaver.LoadNodeReport` — class
- `weaver.LoadResult` — class
- `weaver.LoadRunReport` — class
- `weaver.MirrorPlan` — class
- `weaver.MirrorResult` — class
- `weaver.ValidationNodeReport` — class
- `weaver.ValidationRunReport` — class
- `weaver.WipeItemResult` — class
- `weaver.WipePlan` — class
- `weaver.WipeReport` — class
- `weaver.WipeResult` — class

<!-- END GENERATED PYTHON -->

## Initialisation

### `FabricItemOutcome`

```python
FabricItemOutcome(
    role: str,
    name: str,
    status: str,
    action: str | None = None,
)
```

One requested Fabric item's role, name, observed status, and optional action. `to_mapping()` returns those four fields.

### `ExampleOutcome`

```python
ExampleOutcome(generated: bool = False)
```

Records whether initialisation generated the example source files. `to_mapping()` returns `generated`.

### `InitialiseReport`

```python
InitialiseReport(
    project_folder: str,
    workspace: str,
    resources: tuple[FabricItemOutcome, ...] = (),
    files: tuple[str, ...] = (),
    example: ExampleOutcome = ExampleOutcome(),
    dry_run: bool = False,
    environment_publication: str = "deferred",
    environment_definition: str = "written",
)
```

Returned by `initialise()`. `resources` reports requested Fabric items; `files` lists generated or planned project paths. `created` contains `Role/Name` strings for created resources. `succeeded` is always `True` for a returned report because initialisation raises instead of returning a failed report. `next_commands` supplies the standard workflow, build, load, test, and health commands. `to_mapping()` includes these derived fields.

See [`weaver initialise`](../cli/initialise.md) for creation and dry-run behaviour.

## Build

### `BuildResult`

```python
BuildResult(
    source: str,
    items: tuple[str, ...],
    bundle_id: str,
    installation: bool,
    bundle_path: str | None,
    status: str,
    errors: tuple[BuildFailure, ...] = (),
    selection: Any = None,
    installation_report: Any = None,
)
```

Returned by `build()`. `installation` distinguishes an installed build from a bundle-only build. `bundle_path` is populated for a retained bundle and otherwise `None`. `succeeded` is true only when `status == "succeeded"`.

Each value in `errors` exposes `action_id`, `error_type`, `message`, `artefact`, and `source_path`. `selection` and `installation_report` retain detailed in-memory evidence but are omitted by `to_mapping()`; the mapping contains source, selected items, bundle identity, installation mode, bundle path, status, and mapped errors.

See [`weaver build`](../cli/build.md) and [Build bundles and controlled installation](../../advanced/build-bundles-and-controlled-installation.md).

## Mirror

### `MirrorPlan`

```python
MirrorPlan(
    workspace: Workspace,
    source: CatalogueRef,
    destination: CatalogueRef,
    items: tuple[str, ...] = (),
)
```

Returned by `plan_mirror()`. It is a resolved, non-executed request. `target` is the destination `Warehouse/<name>` string; `mapping` is `(target, source)`; `str(plan)` renders `<source> into <destination>`. Passing the plan to `check_mirror()` validates it against the source catalogue; passing it to `mirror()` validates and executes it.

### `MirrorResult`

```python
MirrorResult(
    workspace: str,
    source_catalogue: str,
    destination_catalogue: str,
    wiped: tuple[str, ...],
    copied: Mapping[str, int] = {},
    uncopied: tuple[str, ...] = (),
    items: tuple[str, ...] = (),
    mirrored: Mapping[str, Mapping] = {},
    status: str = "succeeded",
)
```

Returned after `mirror()` completes. `wiped` names emptied destinations in execution order. `copied` maps catalogue table names to copied row counts, and `rows` is their sum. `uncopied` names historical catalogue tables rebuilt without copied rows. `items` names mirrored logical items; `mirrored` carries each item's source, target, and operation-specific counts. `to_mapping()` converts tuples and mappings to transport shapes.

See [`weaver mirror`](../cli/mirror.md) and [Development cycle](../../basics/development-cycle.md).

## Wipe

### `WipePlan`

```python
WipePlan(
    workspace: Workspace,
    targets: tuple[WipeTarget, ...],
    catalogue: str | None,
    catalogue_action: str,
    unbound: tuple[str, ...] = (),
)
```

Returned by `plan_wipe()`. `targets` is already in execution order; when the catalogue is removed, it is last. `empties_the_catalogue` states whether the catalogue is among those targets. `is_catalogue(target)` checks one target. `describe()` renders the settled action, and `to_mapping()` returns its machine form.

### `WipeReport`

```python
WipeReport(
    target: str,
    location: Location,
    removed: tuple[str, ...],
    dry_run: bool = False,
)
```

Per-area removal detail retained beneath a wipe result. `count` is `len(removed)`. `to_mapping()` serialises `location` as its string value.

### `WipeItemResult`

```python
WipeItemResult(
    target: str,
    outcome: str,
    is_catalogue: bool = False,
    unbound: bool = False,
    counts: Mapping[str, int] = None,
    reports: tuple[WipeReport, ...] = (),
)
```

One physical item's outcome. `counts` defaults to an empty mapping and may contain `entries` and `shortcuts`. `reports` retains per-area detail but is omitted from `to_mapping()`. `describe()` returns one console-oriented summary line.

### `WipeResult`

```python
WipeResult(
    workspace: str,
    items: tuple[WipeItemResult, ...] = (),
    reports: tuple[WipeReport, ...] = (),
    unbound: Mapping | None = None,
    plan: WipePlan | None = None,
    dry_run: bool = False,
)
```

Returned by `wipe()`. `items` is the item-level result; `reports` is the lower-level removal detail. `emptied` lists emptied physical targets in execution order. `unbound` contains the catalogue update result when claims were removed. `to_mapping()` includes the plan and item outcomes but not the lower-level `reports` tuple.

See [`weaver wipe`](../cli/wipe.md) and [Recovery](../../basics/recover-failed-work.md) before using the destructive operation.

## Load

### `LoadResult`

```python
LoadResult(
    succeeded: bool,
    rows_read: int = 0,
    rows_inserted: int = 0,
    rows_updated: int = 0,
    rows_deleted: int = 0,
    rows_rejected: int = 0,
    error_message: str | None = None,
    bookmark_datetime: datetime | None = None,
    is_static_skip: bool = False,
)
```

One load primitive's outcome. `bookmark_datetime` is the UTC instant captured before a clean load read its source. `is_static_skip` distinguishes a load-once skip from an empty read.

```python
from weaver import LoadResult

result = LoadResult(succeeded=True, rows_read=12, rows_inserted=12)
row = result.as_row()
assert LoadResult.from_row(row) == result
```

`failure(message, **counts)` constructs a failed result while preserving supplied counts. `rejected(message)` copies a result with `succeeded=False` and the supplied error. `as_row()` serialises the bookmark as ISO text; `from_row(row)` reconstructs the value and treats a zone-less timestamp as UTC.

### `LoadMessage`

```python
LoadMessage(
    severity: str,
    code: str,
    message: str,
    detail: str | None = None,
    source: str | None = None,
    executor: str | None = None,
)
```

A structured finding about a load node or the run. `severity`, `code`, and `message` are required. `detail`, `source`, and `executor` add available context. `to_mapping()` and `from_mapping(payload)` round-trip the transport form.

### `LoadNodeReport`

```python
LoadNodeReport(
    node_id: str,
    logical_id: str | None,
    physical_target: str,
    primitive_kind: str,
    dispatch_location: str | None,
    status: str,
    executed: bool = False,
    messages: tuple[LoadMessage, ...] = (),
    result: LoadResult | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
)
```

One planned or executed node. `executed` is true only when work touched the target. `succeeded` is true for `succeeded` and dry-run `validated` statuses; a `succeeded_with_rejects` node is not cleanly successful. `result` carries row counts when a load primitive returned them. `to_mapping()` and `from_mapping(payload)` round-trip the report shape.

### `LoadRunReport`

```python
LoadRunReport(
    requested: tuple[str, ...],
    status: str,
    dry_run: bool,
    fault_tolerant: bool,
    reload: bool = False,
    nodes: tuple[LoadNodeReport, ...] = (),
    edges: tuple[tuple[str, str], ...] = (),
    order: tuple[str, ...] = (),
    messages: tuple[LoadMessage, ...] = (),
    workflow_id: str | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
    workspace: str | None = None,
)
```

Returned by `load()`. `requested` preserves the requested item strings. `nodes`, `edges`, and `order` describe the settled run graph. `by_node` maps node IDs to reports. `succeeded` is true for `succeeded` and `succeeded_with_rejects` run statuses. Dry runs use the same shape, with `dry_run=True` and no execution evidence. `to_mapping()` and `from_mapping(payload)` round-trip the report.

See [`weaver load`](../cli/load.md), [Incremental data processing](../../advanced/incremental-data-processing.md), and [Fault tolerance](../../core-concepts/fault-tolerance.md).

## Validation

### `ValidationNodeReport`

```python
ValidationNodeReport(
    logical_id: str,
    kind: str,
    physical_target: str,
    primitive_kind: str,
    dispatch_location: str | None,
    status: str,
    executed: bool = False,
    messages: tuple[str, ...] = (),
    result: Any = None,
    started_at: str | None = None,
    finished_at: str | None = None,
    diagnostics: Any = None,
)
```

One Test or Assumption outcome. `result` carries Test discrepancy counts or an Assumption violation count. `diagnostics` contains rows only when the caller requested one validation by name or file; it is excluded from comparison, representation, and `to_mapping()`. `succeeded` is true for `passed` and dry-run `planned` statuses. `from_mapping(payload)` reconstructs the count-bearing result but not diagnostic rows.

### `ValidationRunReport`

```python
ValidationRunReport(
    status: str,
    nodes: tuple[ValidationNodeReport, ...] = (),
    workflow_id: str | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
)
```

Returned by `test()`. `succeeded` is true for `passed` and `planned`. `failed_nodes` and `invalid_nodes` filter the two unsuccessful status classes. `node(name)` performs a case-insensitive lookup by the trailing logical `Schema.Object` and raises `KeyError` when absent. `totals()` returns planned, executed, passed, failed, and invalid node counts plus missing, unexpected, and violation totals. `to_mapping()` includes those totals; `from_mapping(payload)` reconstructs the report.

See [`weaver test`](../cli/test.md) and [Add Tests and Assumptions](../../basics/tests-and-assumptions.md).

## Health

### `HealthFinding`

```python
HealthFinding(
    area: str,
    code: str,
    severity: str,
    message: str,
    object_id: str | None = None,
    target: str | None = None,
    status: str | None = None,
    workflow_id: str | None = None,
    started_at: datetime | None = None,
    completed_at: datetime | None = None,
    failure_count: int | None = None,
)
```

One health finding. `severity` is `green`, `amber`, or `red`; `status` is the underlying runtime status when available. `sort_key` orders worse findings first, then by code, target, and object. `to_mapping()` emits ISO datetime strings.

### `HealthSection`

```python
HealthSection(
    area: str,
    findings: tuple[HealthFinding, ...] = (),
    counts: Mapping[str, int] = {},
    subjects: int = 0,
)
```

The Load, Tests, or Build section. `status` is the worst finding severity, defaulting to `green` when there are no findings. `subjects` is the number assessed. `to_mapping()` returns status, subjects, sorted counts, and findings.

### `LoadActivity`

```python
LoadActivity(
    object_id: str,
    target: str | None,
    workflow_id: str,
    started_at: datetime | None = None,
    completed_at: datetime | None = None,
    duration_ms: int | None = None,
    rows_read: int = 0,
    rows_inserted: int = 0,
    rows_updated: int = 0,
    rows_deleted: int = 0,
    rows_rejected: int = 0,
    is_reload: bool = False,
    is_static_skip: bool = False,
)
```

One object's recorded load activity in the report window. `to_mapping()` serialises timestamps and all row counts.

### `HealthReport`

```python
HealthReport(
    generated_at: datetime,
    as_of: datetime,
    load: HealthSection,
    tests: HealthSection,
    build: HealthSection,
    targets: tuple[str, ...] = (),
    current_load: CurrentLoad | None = None,
    load_activity: tuple[LoadActivity, ...] = (),
)
```

Returned by `health()`. `sections` is `(load, tests, build)`. `status` is their worst severity, `findings` flattens their findings, and `is_healthy` is true only when status is `green`. `slowest(limit=5)` returns timed activity by descending duration; `moved(limit=5)` returns activity by descending inserted, updated, and deleted rows. Both use object ID as the tie-breaker.

`current_load` summarises the workflow IDs, time range, and status counts behind the estate's current load state. `to_mapping()` emits the health format version, sections, this current-load summary, and load activity.

See [`weaver health`](../cli/health.md) and [Run and inspect an estate](../../basics/run-and-inspect-estate.md).
