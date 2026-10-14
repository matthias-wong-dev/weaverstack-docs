# Installation

Install Weaver, then choose the item you want to work with. Lakehouse, Warehouse, semantic-model and Report tasks give their own access requirements; a Warehouse starter is optional.

<span id="install-the-documented-snapshot"></span>

## Install Weaver

Use Python 3.11 or later. In your Python environment:

```bash
python -m pip install --upgrade weaverstack
weaver --version
```

The package provides the `weaver` command and the importable `weaver` Python library. Use `weaver --help` to see the available commands.

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

Use [Deploy a native model](../semantic-models/native-tmdl.md) to add their definitions to the project. [Requirements and compatibility](../reference/power-bi/requirements-and-compatibility.md) owns supported modes, bindings and permission boundaries. Microsoft documents [model creation rights](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model) and [licences/workspace types](https://learn.microsoft.com/en-us/fabric/enterprise/licenses).

<span id="when-the-preview-needs-a-hosted-runtime"></span>

## Publish the Fabric runtime

Lakehouse work needs the same Weaver version in your local Python environment and the Fabric Environment used by Spark. After the [first Lakehouse task](../lakehouse/python.md) creates the local Environment definition, publish it from the project directory:

```bash
weaver fabric environment publish --path Environment/Weaver.Environment
```

Normal publication adds the installed Weaver release to the Environment's package requirements and waits for Fabric to finish publishing. Selecting an Environment in workspace configuration does not publish it. [Running Python in Fabric](../lakehouse/runtime.md) explains the runtime checks and when to republish. Warehouse-only work does not need this Spark runtime.

## Sign in for the operation

The desktop CLI uses supported configured credentials, an existing Azure CLI sign-in or interactive browser sign-in. Do not assume every call requires the same credential path. Unattended `--non-interactive` commands must already have usable non-browser credentials. The Python library accepts caller-supplied credentials through its supported Session/API; its defaults are not the CLI's credential policy.

Choose [Lakehouse](../lakehouse/index.md), [Warehouse](../warehouse/index.md), [Semantic models](../semantic-models/index.md) or [Reports](../reports/index.md). [Workflows and controlled deployment](../estate/automation-and-deployment.md) owns the route to unattended execution.
