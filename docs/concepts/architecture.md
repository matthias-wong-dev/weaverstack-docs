# Architecture overview

## Repository: the logical estate

A Weaver project represents a Microsoft Fabric workspace as logical items. The first two path segments name an item:

```text
Lakehouse/Landing
Warehouse/Operations
```

Recognised documents beneath those items declare Tables, Views, Folders, Tests, Assumptions, shortcuts, schema metadata and supported Warehouse programmables. The containing item decides whether a SQL document uses Spark SQL or T-SQL. Python and SQL remain executable source rather than templates.

The repository describes intent. It does not have to use the physical Fabric item names for an environment.

## Workspace configuration: physical binding

`workspace-config.yml` names one Fabric workspace, its catalogue Warehouse, an optional Environment and logical-to-physical target mappings:

```yaml
workspace: Parcel Development
environment: Weaver
catalogue: Warehouse/Catalogue

targets:
  Lakehouse/Landing: Landing_Dev
  Warehouse/Operations: Operations_Dev
```

A build binds each selected logical item to a target of the same kind. Later load, test and health commands read installed bindings from the catalogue rather than treating configuration as proof that an item was built.

This separation lets the same repository use different physical names in different environments.

## Build: structure, not business data

Build parses the repository statically, resolves identities and dependencies, reads the catalogue and target inventories, determines the required structural changes, and freezes those changes into a build bundle. The bundle contains ordered actions, payloads, target bindings, hashes and the build selection.

The ordinary `weaver build` command installs that bundle immediately. `--bundle-only` retains it for a later `weaver install`.

Build creates and reconciles structures and installed runtime artefacts. It does not call a Table or Folder's authored `read()` method, move source data or advance a load bookmark. Those are load responsibilities.

The installer executes the frozen bundle. It does not reopen project source, rediscover dependencies or widen destructive scope.

## Load: execute installed data movement

`weaver load` reads installed objects and bindings from the catalogue. For an item-scoped run, the named logical items are a hard boundary: dependencies order work inside that selection but do not add another item.

Load executes the installed Python or T-SQL runtime artefacts, records node outcomes and advances a bookmark only after a clean success. Cross-engine dependencies add the endpoint-refresh or OneLake-publication barriers needed before a consumer can read a producer's result.

## Catalogue: installed and operational state

A configured Warehouse holds Weaver's catalogue in schema `_`. The first ordinary build creates its tables. The catalogue records logical item installations, certified objects, declared metadata, dependencies, shortcuts, bookmarks and load/test outcomes.

A `_.Registry` row certifies that Weaver successfully built an installed object. Physical existence alone is not certification. Before planning, build reconciles catalogue claims with target inventory; after successful installation, catalogue publication and Registry certification occur at the end.

The repository remains authoritative for desired declarations. The catalogue is the installed projection and operational record, not a second authoring surface.

## One lifecycle

```text
project source
    │
    ├── check ─────────────── local validation only
    │
    └── build
          │
          ├── parse and bind logical declarations
          ├── compare catalogue and target inventory
          ├── freeze a build bundle
          └── install structure and certify it
                    │
                    └── load ── execute data movement and record outcomes
                                  │
                                  ├── test
                                  └── health
```

Provisioning is separate. `weaver initialise` creates or adopts the Fabric items a project names and writes project files. A normal build does not create a missing Lakehouse, Warehouse or Environment.

See [First project](../get-started/first-project.md) for the smallest complete path and [CLI reference](../reference/cli.md) for command responsibilities.
