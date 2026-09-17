# `weaver fabric notebook`

<!-- BEGIN GENERATED CLI -->
## `weaver fabric notebook push`

```text
usage: weaver fabric notebook push [-h] [--name NAME]
                                   [--description DESCRIPTION] [--json]
                                   [--non-interactive] [--workspace WORKSPACE]
                                   [--workspace-config WORKSPACE_CONFIG]
                                   [--environment ENVIRONMENT]
                                   source

positional arguments:
  source                Local .py or .ipynb notebook source.

options:
  -h, --help            show this help message and exit
  --name NAME           Fabric display name. Defaults to the filename.
  --description DESCRIPTION
  --json
  --non-interactive     Do not read stdin, wait for a keypress or open browser
                        sign-in. Missing authorisation or required input is an
                        error.
  --workspace WORKSPACE
                        Fabric Workspace name.
  --workspace-config WORKSPACE_CONFIG
                        Workspace configuration file.
  --environment ENVIRONMENT
                        Fabric Environment name or Workspace/Environment
                        reference.
```

## `weaver fabric notebook run`

```text
usage: weaver fabric notebook run [-h] [--lakehouse LAKEHOUSE] [--no-wait]
                                  [--timeout TIMEOUT]
                                  [--poll-interval POLL_INTERVAL] [--json]
                                  [--non-interactive] [--workspace WORKSPACE]
                                  [--workspace-config WORKSPACE_CONFIG]
                                  [--environment ENVIRONMENT]
                                  [--catalogue CATALOGUE]
                                  name

positional arguments:
  name                  Fabric Notebook display name.

options:
  -h, --help            show this help message and exit
  --lakehouse LAKEHOUSE
                        Default Lakehouse for the notebook session.
  --no-wait
  --timeout TIMEOUT
  --poll-interval POLL_INTERVAL
  --json
  --non-interactive     Do not read stdin, wait for a keypress or open browser
                        sign-in. Missing authorisation or required input is an
                        error.
  --workspace WORKSPACE
                        Fabric Workspace name.
  --workspace-config WORKSPACE_CONFIG
                        Workspace configuration file.
  --environment ENVIRONMENT
                        Fabric Environment name or Workspace/Environment
                        reference.
  --catalogue CATALOGUE
                        Where the Weaver catalogue lives, for example
                        Warehouse/Weaver.
```
<!-- END GENERATED CLI -->

## Responsibility and selection

`fabric notebook push` selects a local `.py` or `.ipynb` file and a Fabric workspace. `--name` overrides the filename stem used as the Fabric display name.

`fabric notebook run` selects a deployed notebook by display name. It requires a default Lakehouse and a Fabric Environment. `--lakehouse` supplies the physical Lakehouse name; when omitted, exactly one configured Lakehouse is selected automatically. The Environment comes from `--environment` or workspace configuration and may be qualified as `Workspace/Environment`.

## Execution

### Push

If the named notebook does not exist, `push` creates it and applies `--description` when supplied. If it exists, `push` replaces its notebook definition; it does not update the existing description. Only the `.py` or `.ipynb` definition is transported, not local notebook Resources.

### Run

`run` starts a Spark notebook job with the selected Lakehouse as its default and the selected Environment attached. By default it polls until Fabric reports a terminal result. `--timeout` sets the maximum wait in seconds, and `--poll-interval` sets the polling interval in seconds.

`--no-wait` returns after Fabric accepts the job. It does not report the eventual notebook result.

## Interaction

Neither command asks for destructive confirmation or accepts `--yes`. `--non-interactive` prevents browser sign-in; configured unattended credentials must then be sufficient.

## Output and exit behaviour

By default, `push` reports whether it created or updated the notebook, plus the notebook ID and local source path. `run` reports the status and job URL, and includes the notebook exit value when Fabric returns one.

`--json` writes one result document to stdout. Treat it as command output, not as a versioned schema guarantee.

`push` exits `0` after Fabric creates or updates the definition. `run` exits `0` after a successful waited result or after job acceptance with `--no-wait`. A failed or cancelled waited job, missing item, invalid source, missing Lakehouse or Environment, timeout, authentication error or Fabric error produces a non-zero status.

## Examples

Create or update a notebook definition:

```bash
weaver fabric notebook push notebooks/ParcelRefresh.py \
  --name ParcelRefresh \
  --workspace "Parcel Development"
```

Run it and wait for completion:

```bash
weaver fabric notebook run ParcelRefresh \
  --workspace-config workspace-development.yml \
  --lakehouse ParcelLanding_Dev \
  --timeout 3600 \
  --poll-interval 15
```
