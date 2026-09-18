# `weaver fabric notebook`


---

## `weaver fabric notebook`

<!-- BEGIN GENERATED CLI -->

## `weaver fabric notebook push`

### Synopsis

```text
weaver fabric notebook push [-h] [--name NAME] [--description DESCRIPTION] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] source
```

### Positional arguments

`source`
: Local .py or .ipynb notebook source.

### Options

`-h, --help`
: show this help message and exit

`--name NAME`
: Fabric display name. Defaults to the filename.

`--description DESCRIPTION`
: No description is provided by the parser.

`--json`
: No description is provided by the parser.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

## `weaver fabric notebook run`

### Synopsis

```text
weaver fabric notebook run [-h] [--lakehouse LAKEHOUSE] [--no-wait] [--timeout TIMEOUT] [--poll-interval POLL_INTERVAL] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] name
```

### Positional arguments

`name`
: Fabric Notebook display name.

### Options

`-h, --help`
: show this help message and exit

`--lakehouse LAKEHOUSE`
: Default Lakehouse for the notebook session.

`--no-wait`
: No description is provided by the parser.

`--timeout TIMEOUT`
: No description is provided by the parser.

`--poll-interval POLL_INTERVAL`
: No description is provided by the parser.

`--json`
: No description is provided by the parser.

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

---

## Push and run a Fabric notebook

Use the notebook commands to deploy a local `.py` or `.ipynb` definition and start it as a Fabric Spark job. The run receives an explicit default Lakehouse and Fabric Environment.

This route manages the Notebook item itself. It does not Build Weaver documents, publish an Environment or move a local notebook's Resources.

## Prerequisites

- A Fabric workspace containing the default Lakehouse.
- A published Fabric Environment available to the workspace running the notebook.
- A local `.py` or `.ipynb` notebook definition.
- Credentials that can create or update Notebook items and start notebook jobs.

Bind the workspace, Lakehouse and Environment in a workspace configuration:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
environment: ParcelRuntime

targets:
  Lakehouse/Landing: ParcelLandingDev
```

The catalogue is not used as the notebook's default Lakehouse. `fabric notebook run` uses `--lakehouse` when supplied; otherwise it selects the one configured Lakehouse only when the configuration contains exactly one.

If `ParcelRuntime` does not yet exist or its definition changed, publish it before the notebook run. [Configure workspaces and Fabric Environments](../../basics/workspace-and-python-runtime.md) covers that boundary.

## Push the notebook definition

Deploy a local Python notebook:

```bash
weaver fabric notebook push notebooks/ParcelRefresh.py \
  --name ParcelRefresh \
  --description "Refresh parcel landing data" \
  --workspace-config workspace-development.yml
```

The filename stem becomes the Fabric display name when `--name` is omitted. If that name does not exist, Weaver creates the Notebook and applies the optional description. If it exists, Weaver replaces the notebook definition; it does not update that item's existing description.

Push transports only the `.py` or `.ipynb` definition. Local notebook Resources are not included. Put required Python packages in the attached Environment and make other inputs available through Fabric items or services the notebook can access.

The command reports whether it created or updated the item, its Fabric ID and the local source path. Treat a successful push as deployment evidence, not execution evidence.

## Run and wait for the result

Start the deployed notebook with an explicit Lakehouse when the configuration could be ambiguous:

```bash
weaver fabric notebook run ParcelRefresh \
  --workspace-config workspace-development.yml \
  --lakehouse ParcelLandingDev \
  --timeout 3600 \
  --poll-interval 15
```

Weaver resolves the Notebook and default Lakehouse in `Parcel Operations`, resolves `ParcelRuntime`, submits a Spark notebook job and polls until Fabric reports a terminal result. A successful waited run prints the terminal status and job URL, plus the notebook exit value when Fabric returns one.

`--timeout` limits how long the CLI waits; it does not set a notebook runtime limit or cancel the remote job. If waiting times out, use the reported Fabric context to inspect the job before starting another run.

A failed or cancelled terminal result makes the command fail and includes the provider's reported reason when one is available. Correct the notebook, Lakehouse, Environment, permissions or capacity condition named by that result, push a changed definition when necessary, and start a new run.

## Submit without waiting

For an external scheduler that tracks the Fabric job URL, submit and return after Fabric accepts it:

```bash
weaver fabric notebook run ParcelRefresh \
  --workspace-config workspace-development.yml \
  --lakehouse ParcelLandingDev \
  --no-wait \
  --non-interactive \
  --json
```

`--no-wait` reports acceptance, not completion. The command can exit successfully while the remote job later fails or is cancelled. Persist the returned job URL and add a separate completion check in the scheduler; do not treat process exit alone as the notebook outcome.

`--non-interactive` prevents browser sign-in. It does not supply credentials, change the Lakehouse or publish the Environment. Configure an unattended credential path before using the command from a scheduler.

## Use an Environment from another workspace

An Environment binding can be qualified as `Workspace/Environment`:

```yaml
environment: Shared Runtimes/ParcelRuntime
```

The notebook and its default Lakehouse still run in the workspace selected for the command. Fabric must allow the consumer workspace to attach the qualified Environment, and the caller needs access to both workspaces. Qualifying the Environment does not make the Notebook or Lakehouse cross-workspace.

See [`weaver fabric notebook`](fabric-notebook.md) for complete options and output behaviour. See the [Host-behaviour contract](../operation-behaviour/session-runtime.md) for attached-workspace and cross-workspace execution rules.
