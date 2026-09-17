# Run Weaver unattended

This guide runs Weaver from a scheduler or build runner without choosing a CI vendor. The example validates a project locally, then runs its Build, Load, Test and Health sequence against Fabric.

## Prerequisites

- [Install Weaver](../get-started/installation.md) on the runner and confirm `weaver --version` works.
- Give the runner a project and workspace configuration. This documentation repository includes the checked fixture at `examples/parcel-automation/`.
- Authenticate before the job starts. A non-interactive invocation tries a configured Azure service principal, then an existing Azure CLI sign-in. It does not open browser sign-in. For a service principal, configure `AZURE_CLIENT_ID` and `AZURE_TENANT_ID`, plus either `AZURE_CLIENT_SECRET` or `AZURE_CLIENT_CERTIFICATE_PATH`, in the runner's secret store. Do not put credentials in the repository or command line.
- Grant that identity the Fabric and data-plane permissions required by the operations in the job.

Run `weaver doctor --workspace "Parcel Development" --non-interactive --json` in the runner environment when checking authentication and connectivity separately.

## Set the two interaction controls deliberately

`--non-interactive` prevents an invocation from reading standard input, waiting for a keypress, offering a retry or opening browser sign-in. Missing input or authorisation is then an error. It does **not** authorise destructive work.

`--yes` grants authorisation. It does not make an invocation non-interactive, configure credentials or fill missing arguments. An unattended destructive command needs both options:

```bash
weaver wipe Warehouse/ParcelOperationsDev \
  --workspace "Parcel Development" \
  --non-interactive \
  --yes
```

A workflow also requires authorisation before it starts. Pass both options for an unattended workflow even when its listed commands are not individually destructive: `--non-interactive` forbids the confirmation prompt, while `--yes` authorises the displayed sequence and its commands.

## Validate before contacting Fabric

From the fixture directory, run the local parser first:

```bash
cd examples/parcel-automation
mkdir -p .weaver-results
weaver check . \
  --non-interactive \
  --json > .weaver-results/check.json
```

`check` does not contact Fabric. A zero exit status and a JSON document on standard output are the checkpoint. Treat any non-zero status as a failed job and retain standard error with the JSON result directory.

## Run the ordered lifecycle

The fixture's `workflow.yml` contains the whole sequence:

```yaml
workflows:
  verify:
    - weaver check .
    - weaver build . --item Warehouse/Operations --workspace-config workspace-config.yml
    - weaver load Warehouse/Operations --workspace-config workspace-config.yml
    - weaver test Warehouse/Operations --workspace-config workspace-config.yml
    - weaver health --item Warehouse/Operations --workspace-config workspace-config.yml
```

Run it without a terminal:

```bash
weaver workflow verify \
  --file workflow.yml \
  --non-interactive \
  --yes
```

The workflow prints the numbered sequence before execution. It runs the entries in order in one Session and returns non-zero when a command fails. It stops at that command; later entries do not run, and completed work is not rolled back. See [Fault tolerance](../core-concepts/fault-tolerance.md) for the operation-specific failure boundaries.

## Capture machine-readable results

A workflow has no `--json` option. Use its exit status and human log as the run-level record. When automation needs a command's structured result, invoke that command directly with `--json`:

```bash
weaver build . \
  --item Warehouse/Operations \
  --workspace-config workspace-config.yml \
  --non-interactive \
  --json > .weaver-results/build.json

weaver health \
  --item Warehouse/Operations \
  --workspace-config workspace-config.yml \
  --non-interactive \
  --json > .weaver-results/health.json
```

Commands advertise machine-readable output individually. Do not add `--json` to a command whose help does not list it, and do not parse the human renderer as JSON. A report-producing command exits non-zero when its result is unsuccessful; Health exits non-zero for Amber or Red. Preserve standard error separately so an authentication, configuration or parser error is not mistaken for a report.

## Interpret failures

- **The job asks for input or browser sign-in:** the invocation omitted `--non-interactive`, or a wrapper removed it.
- **The job says to pass `--yes`:** authorisation is missing. Add it only after reviewing the exact destructive command or workflow sequence.
- **Credential acquisition fails:** configure a service principal or complete `az login` before the job. `--yes` does not affect authentication.
- **A workflow reports `Workflow stopped at [N]`:** command `N` failed. Inspect that command's error and the [Catalogue](../core-concepts/catalogue.md) or Health state before rerunning. Earlier commands may already have changed Fabric.
- **Local check succeeds but Fabric work fails:** the declarations parsed; the live workspace, permissions or platform operation did not. Local checks are not evidence of a successful Fabric run.

## Next actions

Use [Sessions and workflows](sessions-and-workflows.md) when the sequence itself needs editing or interactive diagnosis. Use [Promote a bundle](promote-a-bundle.md) to separate Build planning from installation. [Weaver operations](../core-concepts/weaver-operations.md), the [Development cycle](../core-concepts/development-cycle.md), the [CLI reference](../reference/cli.md) and [Contracts](../contracts/index.md) define the adjacent lifecycle and command boundaries.
