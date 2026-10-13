# Python operations

Call operations as functions on `weaver`. Each call resolves one workspace and returns a result or report object. Pass `session=` to reuse an open Session; without it, the operation opens and closes the Session it needs. A supplied Session remains open after the call.

A Session fixes the Fabric workspace. Operation arguments may supply a catalogue or Environment within that workspace, but cannot move the Session to another workspace. See [Session and workspace helpers](session.md) for reuse and discovery.

## Lifecycle calls

- `initialise` validates and creates a project and its requested Fabric items. Environment publication is optional.
- `build` reads project source and normally deploys it. `dry_run=True` returns the canonical read-only preview with no retained bundle; `bundle_only=True` retains a destination-bound bundle without installation. They cannot be combined. Build sources and Power BI items in separate calls.
- `load` runs installed Table/Folder work and semantic-model refresh. `items` is a hard boundary; `names` is whole-name case-insensitive regex selection. Optional `ancestors`/`descendants` expand the original seeds separately within that boundary. Without a catalogue only explicit semantic-model refresh is available.
- `test` runs installed validations or source/file validations with `files=` or no catalogue. `names=` filters by repeated whole-name regex; `source=` supplies project context. It returns the completed report even for findings or invalid validations; inspect `succeeded` and `status`.
- `health` reads catalogue and physical state. `inventories=False` omits physical inventory reads.

The operation model and state transitions are in [Build, Load and Test](../../core-concepts/build-load-and-test.md). For command output, interaction policy and exit status, use the [CLI reference](../cli.md).

## Plan before changing state

`plan_mirror` resolves source, destination and item selection without reading Fabric. `check_mirror` checks that plan against the source catalogue without changing Fabric. `mirror` executes a checked plan, emptying destination targets before copying or rebinding state.

`plan_wipe` settles target order and catalogue disposition. It reads the catalogue when no targets are named and estate discovery is required. `wipe` executes the settled plan; `dry_run=True` reports the work without emptying targets.

`plan_unbind` reads installed claims and physical presence; `unbind` removes those claims without changing physical items. It requires explicit physical targets and a catalogue.

Build, Load and Test accept positive integer `concurrency=` as a total invocation cap, in addition to configured resource limits. `load(ignore_stability_threshold=True)` waives only declared delete/update thresholds for that call, not key checks, failure policy or selection.

Keep a reviewed plan object when approval and execution happen in separate code paths. Passing a settled wipe plan together with new planning arguments is rejected.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

### `weaver.build`

```python
weaver.build(source=None, *, items: str | Sequence[str] | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, data_sources=None, bind_data_sources: bool=False, dry_run: bool=False, bundle_only: bool=False, bundle_path: str | Path | None=None, concurrency: int | None=None, session=None) -> BuildResult
```

### `weaver.check_mirror`

```python
weaver.check_mirror(plan: MirrorPlan, *, session=None) -> ResolvedMirror
```

### `weaver.health`

```python
weaver.health(items: str | Sequence[str] | None=None, *, as_of: str | datetime | None=None, workspace: str | None=None, catalogue: str | None=None, workspace_config: str | Path | None=None, inventories: bool=True, session=None) -> HealthReport
```

### `weaver.initialise`

```python
weaver.initialise(project_folder, *, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, lakehouse: str | None=None, warehouse: str | None=None, semantic_model: str | None=None, example: bool=False, publish_environment: bool=False, install_weaver: bool | None=None, dry_run: bool=False, session=None, client=None) -> InitialiseReport
```

### `weaver.load`

```python
weaver.load(items: str | Sequence[str] | None=None, *, names: str | Sequence[str] | None=None, ancestors: bool=False, descendants: bool=False, source=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, fault_tolerant: bool=False, dry_run: bool=False, reload: bool=False, ignore_stability_threshold: bool=False, stale: bool=False, as_of: str | datetime | None=None, concurrency: int | None=None, session=None) -> LoadRunReport
```

### `weaver.mirror`

```python
weaver.mirror(items: str | Sequence[str] | None=None, *, no_item: bool=False, plan: MirrorPlan | ResolvedMirror | None=None, workspace: str | None=None, catalogue: str | None=None, mirror: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, session=None) -> MirrorResult
```

### `weaver.plan_mirror`

```python
weaver.plan_mirror(items: str | Sequence[str] | None=None, *, no_item: bool=False, workspace: str | None=None, catalogue: str | None=None, mirror: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, session=None) -> MirrorPlan
```

### `weaver.plan_unbind`

```python
weaver.plan_unbind(targets: str | Iterable[str], *, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, session=None) -> UnbindPlan
```

### `weaver.plan_wipe`

```python
weaver.plan_wipe(targets: str | Iterable[str]=(), *, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, unbind: bool=False, catalogue_action: str | None=None, preserve_data_source: bool=False, session=None) -> WipePlan
```

### `weaver.test`

```python
weaver.test(items: str | Sequence[str] | None=None, *, names: str | Sequence[str] | None=None, files: str | Path | Sequence[str | Path] | None=None, source=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, dry_run: bool=False, concurrency: int | None=None, session=None) -> ValidationRunReport
```

### `weaver.unbind`

```python
weaver.unbind(targets: str | Iterable[str]=(), *, plan: UnbindPlan | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, dry_run: bool=False, session=None) -> UnbindResult
```

### `weaver.wipe`

```python
weaver.wipe(targets: str | Iterable[str]=(), *, plan: WipePlan | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, unbind: bool=False, catalogue_action: str | None=None, preserve_data_source: bool | None=None, dry_run: bool=False, session=None) -> WipeResult
```

<!-- END GENERATED PYTHON -->
