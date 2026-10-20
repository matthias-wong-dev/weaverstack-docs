# `weaver catalogue-dashboard`

Catalogue Dashboard creates or updates the Catalogue Dashboard's SemanticModel and Report, both under one name, in the workspace of the catalogue it reads. It refreshes the model after deployment. The catalogue is only read, and nothing about the Dashboard is recorded in it.

```bash
weaver catalogue-dashboard --name "Catalogue Dashboard" --workspace-config workspace-development.yml
```

`--catalogue` defaults to `catalogue:` and `--name` to `catalogue_dashboard:` in workspace configuration. A catalogue in another workspace, a name that `targets:` deploys a model or Report to, and an existing model or Report of that name that is not a Catalogue Dashboard are refused. A catalogue that Weaver 0.10.0 or later has not built into is refused before any change. A dry run changes nothing.

See [Catalogue Dashboard](../../estate/catalogue-dashboard.md) for what the pages show and the HTML Content requirement.

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver catalogue-dashboard [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--catalogue REFERENCE] [--name NAME] [--dry-run] [--json] [--non-interactive]
```

## Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--catalogue REFERENCE`
: The catalogue Warehouse to read, as Workspace/Warehouse/Name or Warehouse/Name. Defaults to catalogue: in workspace configuration.

`--name NAME`
: The SemanticModel and Report to deploy to. Defaults to catalogue_dashboard: in workspace configuration.

`--dry-run`
: Resolve the source and the Dashboard's items without changing them.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->
