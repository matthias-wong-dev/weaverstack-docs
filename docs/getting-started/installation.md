# Installation

Install Weaver, configure Fabric access, then use the first project to build and operate a small estate. Lakehouse and Warehouse work, semantic models and Reports use the same project with permissions appropriate to each item.

## Install the documented snapshot

!!! warning "Private documentation preview"
    These pages describe Weaver revision `74b4d15ee65ed2740593af1f4d459771b801b132`. The published PyPI package `0.9.0` does not contain all of these interfaces. Public publication is held until its matching package is available. For this preview, use the exact source target below rather than an unqualified package install.

Use Python 3.11 or later and Git. In a Python environment:

```bash
python -m pip install "weaverstack @ git+https://github.com/matthias-wong-dev/weaverstack.git@74b4d15ee65ed2740593af1f4d459771b801b132"
weaver --version
weaver --help
```

The installation provides the `weaver` command and importable `weaver` package. The snapshot has a derived development version; it is not a new named release. The help should include Build `--dry-run`, Load recursive selection, invocation concurrency and Unbind.

Check an existing project without service access:

```bash
weaver check .
```

Check parses declarations and native project files. It does not deploy, run DAX, execute SQL or establish workspace permissions.

## Configure Fabric access

For the first Warehouse tutorial, use a Fabric workspace on suitable running capacity and permission to create or reuse the named catalogue and target Warehouse. Its Initialise step also creates or reuses a Fabric Environment, but the Warehouse-only work does not publish or execute that runtime.

Python Lakehouse work needs Spark and Weaver available in the relevant runtime. Warehouse T-SQL does not need Spark. Spark-backed Build requires a compatible Weaver runtime; the Lakehouse task supplies its publication steps.

Doctor can check the relevant existing workspace:

```bash
weaver doctor --workspace "Parcel Development"
```

Doctor’s general probes can acquire Spark. For a model-specific readiness check, use its semantic-model route as described in the [CLI reference](../reference/cli/doctor.md).

## Model and Report access

When adding a semantic model and its linked Report to the project:

- use a service workspace that supports the model’s mode;
- have the appropriate Power BI licence and workspace rights for the operation; creation needs Contributor or greater access and the API's required delegated scopes;
- provide native PBIP/TMDL model and Report definitions in the supported layout;
- have refresh and query access for steps that need them. DAX query access has its own service and tenant requirements.

An Import model with inline data can run in an existing Power BI workspace without a Weaver catalogue. The deployment example uses that small setup to demonstrate native files. A model reading managed Lakehouse or Warehouse data uses the project’s source mappings and existing service connections; Direct Lake retains its capacity requirements.

Use [Deploy semantic models and Reports with PBIP](../basics/power-bi/deploy-pbip.md) to add their definitions to the project. [Requirements and compatibility](../reference/power-bi/requirements-and-compatibility.md) owns supported modes, bindings and permission boundaries. Microsoft documents [model creation rights](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model) and [licences/workspace types](https://learn.microsoft.com/en-us/fabric/enterprise/licenses).

## When the preview needs a hosted runtime

A Lakehouse tutorial that publishes `--dev` needs a checkout-backed installation so Weaver can build the exact local wheel. Use this alternative to the direct Git package install above:

```bash
git clone https://github.com/matthias-wong-dev/weaverstack.git
git -C weaverstack checkout 74b4d15ee65ed2740593af1f4d459771b801b132
python -m pip install -e "./weaverstack[dev]"
```

Keep that checkout at the documented revision, return to the tutorial project directory, and use its Environment publication step. Do not overlay an unpublished development version from PyPI. A notebook already running in Fabric needs the matching package and dependencies in its attached runtime; it does not need a second remote session merely to run in that workspace.

## Sign in for the operation

The desktop CLI uses supported configured credentials, an existing Azure CLI sign-in or interactive browser sign-in. Do not assume every call requires the same credential path. Unattended `--non-interactive` commands must already have usable non-browser credentials. The Python library accepts caller-supplied credentials through its supported Session/API; its defaults are not the CLI's credential policy.

Continue with [your first Fabric project](first-project.md). [Basics](../basics/index.md) adds Lakehouse and Warehouse work, semantic models and Reports. [Automation](../advanced/automation-and-execution-contexts.md) owns unattended execution details.
