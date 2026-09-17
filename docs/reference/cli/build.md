# `weaver build`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver build [-h] [--item ITEM[=TARGET]] [--bundle-only] [--bundle-path PATH] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [SOURCE]
```

## Positional arguments

`SOURCE`
: Project folder, or an abfss location inside a Fabric session. Defaults to the current directory or Notebook Resources.

## Options

`-h, --help`
: show this help message and exit

`--item ITEM[=TARGET]`
: Weaver item to build. Its physical target comes from workspace configuration; use ITEM=TARGET to supply or override it. Repeat to select multiple items. Naming none builds every configured item.

`--bundle-only`
: Create a deployment bundle without installing it.

`--bundle-path PATH`
: Directory to write a bundle created with --bundle-only.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

<!-- END GENERATED CLI -->

## Responsibility and selection

Read a project, build its objects into named Weaver items, and normally install the resulting deployment bundle.

`SOURCE` is a project folder on the CLI. Inside a Fabric session it may also be an `abfss` location. When omitted, it resolves to the current directory or Notebook Resources according to the host.

Repeat `--item ITEM[=TARGET]` to select logical items. The optional right side supplies or overrides the physical target. Without `--item`, build selects every configured item.

## Execution

Build discovers and validates the project, resolves item bindings, determines the selected changes, creates a bundle, and installs it unless `--bundle-only` is set. `--bundle-path` chooses the retained bundle directory and is valid only with `--bundle-only`; an already populated destination is refused.

`--bundle-only` does not install. The retained directory or archive can be passed to `weaver install` without reopening source or replanning.

## Interaction

After a source discovery, graph, identity, or metadata error in an interactive terminal, Weaver can offer to retry while keeping the Session open. Configuration and Fabric failures are not source-edit retries. `--non-interactive` and `--json` return after one attempt without prompting.

## Output and exit behaviour

A normal build reports installation action counts and the bundle identifier. Bundle-only output reports selected build and removal counts, the bundle identifier, and the path when retained. Source and operation errors are also reported.

`--json` emits the current build result as one JSON document. Its fields and bundle representation are not presented here as compatibility contracts.

The command exits `0` when the build result succeeds and `1` when discovery, planning, bundle creation, or installation fails. Argument errors exit through `argparse`.

## Examples

Build and install every configured item:

```bash
weaver build --workspace-config workspace-config.yml
```

Build selected items with one target override:

```bash
weaver build ./parcel \
  --item Lakehouse/Landing \
  --item Warehouse/Operations=Warehouse/Operations_Dev \
  --workspace-config workspace-config.yml
```

Create a bundle for later installation:

```bash
weaver build ./parcel \
  --bundle-only \
  --bundle-path ./dist/parcel-bundle \
  --workspace-config workspace-config.yml
```
