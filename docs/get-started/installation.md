# Installation

## Requirements

- Python 3.11 or later.
- Access to a Microsoft Fabric workspace for commands that inspect or change Fabric.

Install the published package:

```bash
python -m pip install weaverstack
```

Confirm that the command is available:

```bash
weaver --version
weaver --help
```

The package installs the `weaver` command and the importable `weaver` Python package.

## Authentication

Weaver chooses credentials when a command first reaches Fabric, in this order:

1. a service principal configured with `AZURE_CLIENT_ID`, `AZURE_TENANT_ID` and either `AZURE_CLIENT_SECRET` or `AZURE_CLIENT_CERTIFICATE_PATH`;
2. an existing Azure CLI sign-in;
3. interactive browser sign-in, unless `--non-interactive` was passed.

For local development, an Azure CLI session is the simplest non-browser path:

```bash
az login
weaver doctor --workspace "Parcel Development"
```

`doctor` checks authentication, workspace visibility and connectivity to the Fabric services Weaver needs. A missing Lakehouse or Warehouse leaves the corresponding check not tested; a failed applicable check returns a non-zero exit status.

In unattended execution, pass `--non-interactive`. It prevents prompts and browser sign-in; it does not authorise destructive work. Destructive commands also require `--yes` when no person is available to confirm them.

## Fabric Environments

Current versions of `weaver initialise` write a local Fabric Environment definition. Environment creation and publication are separate operations. Publish the generated definition before a load or test that runs Weaver-authored Python in Fabric:

```bash
weaver fabric environment publish \
  --path Environment/Weaver.Environment \
  --workspace "Parcel Development"
```

Warehouse-only work does not need the Environment to be published. Commands that execute Weaver-authored Python in Fabric do.

Next: [create a first project](first-project.md).
