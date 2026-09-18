# Python operations

Call operations as functions on `weaver`. Each call resolves one workspace and returns a result or report object. Pass `session=` to reuse an open Session; without it, the operation opens and closes the Session it needs. A supplied Session remains open after the call.

A Session fixes the Fabric workspace. Operation arguments may supply a catalogue or Environment within that workspace, but cannot move the Session to another workspace. See [Session and workspace helpers](session.md) for reuse and discovery.

## Lifecycle calls

- `initialise` validates and creates a project and its requested Fabric items. Environment publication is optional.
- `build` reads project source, prepares a build bundle and installs it unless `bundle_only=True`.
- `load` runs installed data work. `items` is a hard item boundary; `names` selects work inside that boundary without dependency expansion.
- `test` runs installed validations, or one uninstalled source file when `file=` is supplied. `strict=True` raises `ValidationError` for failed or invalid validation outcomes.
- `health` reads catalogue and physical state. `inventories=False` omits physical inventory reads.

The operation model and state transitions are in [Build, Load and Test](../../core-concepts/build-load-and-test.md). For command output, interaction policy and exit status, use the [CLI reference](../cli.md).

## Plan before changing state

`plan_mirror` resolves source, destination and item selection without reading Fabric. `check_mirror` checks that plan against the source catalogue without changing Fabric. `mirror` executes a checked plan, emptying destination targets before copying or rebinding state.

`plan_wipe` settles target order and catalogue disposition. It reads the catalogue when no targets are named and estate discovery is required. `wipe` executes the settled plan; `dry_run=True` reports the work without emptying targets.

Keep a reviewed plan object when approval and execution happen in separate code paths. Passing a settled wipe plan together with new planning arguments is rejected.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

### `weaver.build`

```python
weaver.build(source=None, *, items: str | Sequence[str] | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, bundle_only: bool=False, bundle_path: str | Path | None=None, session=None) -> BuildResult
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
weaver.initialise(project_folder, *, workspace: str | None=None, catalogue: str=DEFAULT_CATALOGUE, environment: str=DEFAULT_ENVIRONMENT, lakehouse: str | None=None, warehouse: str | None=None, example: bool=False, publish_environment: bool=False, install_weaver: bool | None=None, dry_run: bool=False, session=None, client=None) -> InitialiseReport
```

### `weaver.load`

```python
weaver.load(items: str | Sequence[str] | None=None, *, names: str | Sequence[str] | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, fault_tolerant: bool=False, dry_run: bool=False, reload: bool=False, stale: bool=False, as_of: str | datetime | None=None, session=None) -> LoadRunReport
```

### `weaver.mirror`

```python
weaver.mirror(items: str | Sequence[str] | None=None, *, no_item: bool=False, plan: MirrorPlan | ResolvedMirror | None=None, workspace: str | None=None, catalogue: str | None=None, mirror: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, session=None) -> MirrorResult
```

### `weaver.plan_mirror`

```python
weaver.plan_mirror(items: str | Sequence[str] | None=None, *, no_item: bool=False, workspace: str | None=None, catalogue: str | None=None, mirror: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, session=None) -> MirrorPlan
```

### `weaver.plan_wipe`

```python
weaver.plan_wipe(targets: str | Iterable[str]=(), *, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, unbind: bool=False, catalogue_action: str | None=None, session=None) -> WipePlan
```

### `weaver.test`

```python
weaver.test(items: str | Sequence[str] | None=None, *, name: str | None=None, file: str | Path | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, dry_run: bool=False, strict: bool=False, session=None) -> ValidationRunReport
```

### `weaver.wipe`

```python
weaver.wipe(targets: str | Iterable[str]=(), *, plan: WipePlan | None=None, workspace: str | None=None, catalogue: str | None=None, environment: str | None=None, workspace_config: str | Path | None=None, unbind: bool=False, catalogue_action: str | None=None, dry_run: bool=False, session=None) -> WipeResult
```

<!-- END GENERATED PYTHON -->
