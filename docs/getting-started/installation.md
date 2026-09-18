# Installation

## Before you start

You need:

- Python 3.11 or later;
- a Microsoft Fabric workspace you can modify;
- permission to create or reuse two Warehouses and a Fabric Environment in that workspace;
- a Fabric credential available through a configured service principal, an existing Azure CLI sign-in or browser sign-in.

The first project also creates or reuses a Fabric Environment, but its Warehouse-only code does not use or publish that Environment.

## Install Weaver

Install the published package into your Python environment:

```bash
python -m pip install weaverstack
```

**Expected result:** the installation completes and provides both the `weaver` command and the importable `weaver` Python package.

Confirm that the command is available:

```bash
weaver --version
weaver --help
```

**Expected result:** the first command prints the installed version, the second lists Weaver commands and both exit successfully.

## Check access to Fabric

Replace the workspace name below with your own:

```bash
weaver doctor --workspace "Parcel Development"
```

Weaver first tries a configured service principal, then an existing Azure CLI sign-in, then browser sign-in. Complete the browser sign-in if it opens.

**Expected result:** Doctor confirms authentication and workspace visibility and exits successfully. A connection that does not apply because the workspace has no corresponding Lakehouse or Warehouse may be reported as not tested.

You are ready to [create the first project](first-project.md). Authentication options, unattended execution and Fabric topology are covered in [Automation and execution contexts](../advanced/automation-and-execution-contexts.md) and the [CLI reference](../reference/cli.md).
