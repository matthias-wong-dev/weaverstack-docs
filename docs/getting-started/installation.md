# Installation

Weaver needs Python 3.11 or later. Install it into the Python environment you use for the project, ideally a virtual environment:

<span id="install-the-documented-snapshot"></span>

## Install Weaver

```bash
python -m pip install --upgrade weaverstack
```

```bash
weaver --version
```

The package provides the `weaver` command and the `weaver` Python library. `weaver --help` lists the commands.

<span id="configure-fabric-access"></span>

## Sign in for the operation

The `weaver` command signs in with the first credential that works: a configured service principal, then an existing Azure CLI sign-in, then interactive browser sign-in. On a desktop, either sign in with the Azure CLI first or let the first command open a browser:

```bash
az login
```

The identity needs the workspace rights each task lists. Tasks state their own requirements, such as creating Warehouses, publishing an Environment or refreshing a semantic model, where you need them. [Unattended execution](../estate/automation-and-deployment.md) covers service principals and `--non-interactive` for jobs.

## Model and Report access

Semantic models and Reports can run in an existing, suitably licensed Power BI workspace without a Fabric Warehouse, Lakehouse or Catalogue. Fabric data workloads need Fabric capacity. See the [two operating modes](../semantic-models/index.md#two-ways-to-use-weaver-with-power-bi) and [model and Report requirements](../reference/power-bi/requirements-and-compatibility.md).

<span id="when-the-preview-needs-a-hosted-runtime"></span>

## Publish the Fabric runtime

Lakehouse Python and Spark SQL run in Fabric Spark, so the Fabric Environment needs the same Weaver version you installed locally. The [first Lakehouse task](../lakehouse/python.md#check-build-and-load) publishes it with one command before its first Build. Warehouse T-SQL and Power BI-only work do not need it.

## Next

[Start with a first task](index.md). The [Warehouse Table and View](../warehouse/first-project.md) is the shortest first result.
