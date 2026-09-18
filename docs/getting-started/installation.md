# Installation

## Prerequisites

- Python 3.11 or later.
- Access to a Microsoft Fabric workspace for commands that inspect or change Fabric.
- A service principal, an Azure CLI sign-in, or permission to complete browser sign-in.

The [first project](first-project.md) also requires permission to create or reuse two Warehouses and the default Fabric Environment.

## Install Weaver

Install the published package into your Python environment:

```bash
python -m pip install weaverstack
```

The distribution installs both the `weaver` command and the importable `weaver` Python package.

Check the installation:

```bash
weaver --version
weaver --help
```

`weaver --version` prints the installed package version. `weaver --help` lists the available commands. Both commands should exit with status `0`.

## Authenticate to Fabric

The desktop CLI tries these credential paths in order when a command first reaches Fabric:

1. a service principal configured with `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and either `AZURE_CLIENT_SECRET` or `AZURE_CLIENT_CERTIFICATE_PATH`;
2. an existing Azure CLI sign-in;
3. browser sign-in, unless the command uses `--non-interactive`.

For local development, sign in with the Azure CLI and check the workspace:

```bash
az login
weaver doctor --workspace "Parcel Development"
```

`doctor` checks authentication, workspace visibility, and the applicable Fabric connections. A failed applicable check returns a non-zero status. A connection that cannot be tested because the workspace has no corresponding Lakehouse or Warehouse is reported as not tested.

`--non-interactive` prevents prompts, keypress waits, and browser sign-in. It does not authorise destructive work; those commands also require `--yes` when no person is available to confirm them. See [Interaction and automation](../reference/cli.md#interaction-and-automation) for the shared CLI rules.

## Know when to publish an Environment

`weaver initialise` writes a local Fabric Environment definition and creates or reuses the named Environment. Creation and publication are separate operations.

Publish the generated definition before running project work that imports Weaver-authored Python in Fabric:

```bash
weaver fabric environment publish \
  --path Environment/Weaver.Environment \
  --workspace "Parcel Development"
```

Warehouse-only SQL work does not require Environment publication. The first project therefore leaves publication deferred. The [CLI reference](../reference/cli.md) lists the command responsibilities and workspace options.

## Next action

[Create the Warehouse-only first project](first-project.md).
