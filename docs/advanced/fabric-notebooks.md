# Push and run a Fabric notebook

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

If `ParcelRuntime` does not yet exist or its definition changed, publish it before the notebook run. [Configure workspaces and Fabric Environments](../guides/environments.md) covers that boundary.

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

See [`weaver fabric notebook`](../reference/cli/fabric-notebook.md) for complete options and output behaviour. See the [Host-behaviour contract](../contracts/host-behaviour.md) for attached-workspace and cross-workspace execution rules.
