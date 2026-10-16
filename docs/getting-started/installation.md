# Installation

Use Python 3.11 or later. Install Weaver in your Python environment and check the version:

<span id="install-the-documented-snapshot"></span>

## Install Weaver

```bash
python -m pip install --upgrade weaverstack
weaver --version
```

The package provides the `weaver` command and Python library. `weaver --help` lists the commands.

## Configure Fabric access

Choose the item you want to work on:

- [Lakehouse: a CSV file into a Delta Table](../lakehouse/python.md).
- [Warehouse: a SQL Table and View](../warehouse/first-project.md).
- [Semantic model: deploy native TMDL and add a modelling rule](../semantic-models/native-tmdl.md).
- [Report: deploy a native Report with its model](../reports/deploy.md).

Each task gives its workspace rights, capacity and setup requirements where you need them.

## Model and Report access

Start with Semantic Models and Reports in an existing, suitably licensed Power BI service workspace without setting up a Fabric Warehouse, Lakehouse or Catalogue. This is distinct from the capacity needed for Fabric data workloads. See the [two operating modes](../semantic-models/index.md#two-ways-to-use-weaver-with-power-bi) and [model and Report requirements](../reference/power-bi/requirements-and-compatibility.md).

<span id="when-the-preview-needs-a-hosted-runtime"></span>

## Publish the Fabric runtime

Lakehouse Spark work needs the same Weaver version locally and in its published Fabric Environment. The [first Python task](../lakehouse/python.md#check-build-and-load) shows that publication step before Build. Warehouse-only SQL does not need it.

## Sign in for the operation

The desktop CLI can use configured credentials, existing Azure CLI sign-in or interactive browser sign-in. Start with the normal interactive commands in the tutorials. [Unattended execution](../estate/automation-and-deployment.md) explains configured non-browser credentials and `--non-interactive` when you need a job rather than a desktop session.
