# Session and workspace helpers

A Session carries workspace resolution, credentials and acquired Fabric execution resources across operation calls. Constructing one resolves configuration but does not resolve Fabric items, start Livy or open a TDS connection. Capabilities are acquired when an operation asks for them.

Use it as a context manager:

```python
import weaver

with weaver.session(
    workspace="Parcel Operations",
    catalogue="Warehouse/Weaver",
    environment="Weaver",
) as opened:
    build_result = weaver.build(".", session=opened)
    load_report = weaver.load("Lakehouse/Parcels", session=opened)
    validation_report = weaver.test("Lakehouse/Parcels", session=opened)
```

The Session closes on leaving the block. Each operation leaves a supplied Session open; an operation-created Session closes at the end of that call. A closed Session does not reopen.

`workspace_config` reads the same workspace configuration used by the CLI. Explicit `workspace`, `catalogue` and `environment` values override values read from that file. A resolved workspace object can be passed as `workspace`, but not together with `workspace_config`.

`current_workspace()` discovers `workspace-config.yml` from the current project first, then the current Fabric notebook workspace. Outside those contexts, pass a workspace name or configuration explicitly.

The [Sessions and workflows guide](../../basics/sessions-and-workflows.md) covers interactive command composition. The [`weaver session` reference](../cli/session.md) documents the terminal prompt.

## Lakehouse locations

`Lakehouse` represents a resolved Lakehouse destination for authored code. It provides table and folder paths and qualifies object names against its Spark destination.

`default_lakehouse(spark)` resolves the Lakehouse attached to the supplied Fabric Spark session. It requires an attached Lakehouse and its workspace address.

`lakehouse_for(resolver, item)` resolves a named Lakehouse with the supplied resolver. Use the returned `Lakehouse` rather than retaining session-scoped mounted paths; `spark_root` is its durable OneLake identity.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

### `weaver.Lakehouse`

Kind: class

### `weaver.current_workspace`

```python
weaver.current_workspace() -> Workspace
```

### `weaver.default_lakehouse`

```python
weaver.default_lakehouse(spark: Any) -> Lakehouse
```

### `weaver.lakehouse_for`

```python
weaver.lakehouse_for(resolver: Any, item: ItemRef | str) -> Lakehouse
```

### `weaver.session`

```python
weaver.session(*, workspace: Any=None, catalogue: str | None=None, environment: str | None=None, workspace_config: Any=None, credential: Any=None)
```

<!-- END GENERATED PYTHON -->
