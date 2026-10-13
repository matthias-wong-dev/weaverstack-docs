# Installation

Install Weaver first, then check the prerequisites for the route you need. Power BI deployment and Fabric data engineering have different service requirements.

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

## Route 1: native Power BI

For a model and linked Report:

- use an existing Power BI service workspace, not free Desktop alone;
- have the appropriate Power BI licence and workspace rights for the operation; creation needs Contributor or greater access and the API's required delegated scopes;
- provide native PBIP/TMDL model and Report definitions in the supported layout;
- have refresh and query access for steps that need them. DAX query access has its own service and tenant requirements.

The standalone route does not need a catalogue Warehouse, Lakehouse, Spark session or Fabric Environment. An Import/calculated-data sample avoids an external gateway/credential setup; another model's sources may need their own credentials. Direct Lake still has its platform prerequisites.

Use [Deploy an existing PBIP](../basics/power-bi/deploy-pbip.md) for the first result. [Requirements and compatibility](../reference/power-bi/requirements-and-compatibility.md) owns supported modes, bindings and permission boundaries. Microsoft documents [model creation rights](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model) and [licences/workspace types](https://learn.microsoft.com/en-us/fabric/enterprise/licenses); a licence list is not evidence that your particular service call has succeeded.

## Route 2: a small Fabric pipeline

For the first Warehouse tutorial, use a Fabric workspace on suitable running capacity and permission to create or reuse the named catalogue and target Warehouse. Its Initialise step also creates or reuses a Fabric Environment, but the Warehouse-only work does not publish or execute that runtime.

Python Lakehouse work needs Spark and Weaver available in the relevant runtime. Warehouse T-SQL and Spark-SQL-only work have different runtime needs; do not publish an Environment merely because every tutorial mentions Fabric.

Doctor can check the relevant existing workspace:

```bash
weaver doctor --workspace "Parcel Development"
```

Its general probes can acquire Spark when that probe applies. Do not make a generic Doctor run a compulsory Power BI installation step. An existing model can use Doctor's semantic-model route; see its [CLI reference](../reference/cli/doctor.md).

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

Continue with [your first Fabric project](first-project.md) or [your first Power BI project](../basics/power-bi/deploy-pbip.md). [Automation](../advanced/automation-and-execution-contexts.md) owns unattended execution details.
