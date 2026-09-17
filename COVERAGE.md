# Internal documentation coverage map

This maintainer-only map records what the public site does not yet explain. It lives outside `docs/` and is not rendered on `docs.weaverstack.dev`. A named path is an ownership decision, not a claim that the page or contract already exists.

## Concepts

| Missing subject | Current evidence | Future authoritative home | Needed coverage |
| --- | --- | --- | --- |
| Logical identity and naming | Repository parser, identity tests, repository design | `core-concepts/identity.md` | Item, area, schema and object identity; filename rules; logical versus physical names; reserved `_` and `_weaver` names. |
| Repository discovery | Repository reader and discovery tests | `core-concepts/repository.md` | Recognised trees, ignored content, `_ignore`, helper modules, static parsing and source locations. |
| Dependency graph | Declaration graph and build/run graph tests | `core-concepts/dependencies.md` | Inferred and declared dependencies, item layers, cycles, impact propagation and run-scope boundaries. |
| Shortcuts | Shortcut declarations, planner tests and Fabric journeys | `core-concepts/shortcuts.md` | Logical and physical targets, Lakehouse and Warehouse forms, ownership, cross-workspace limits and read semantics. |
| Incremental build | Build selection, Registry and inventory tests | `core-concepts/incremental-build.md` | Signatures, physical reconciliation, changed/impacted selection, prune, prohibited rebuild and certification. |
| Load execution | Runtime graph, load reports and acceptance journeys | `core-concepts/load.md` | Bookmarks, fault tolerance, barriers, reload, stale selection, row statistics and failure boundaries. |
| Tests and Assumptions | Validation source, tests and design | `core-concepts/validation.md` | Test versus Assumption semantics, installed and direct execution, diagnostic-row handling and persisted outcomes. |
| Health model | Health source, representation tests and design | `core-concepts/health.md` | Green/Amber/Red rules, freshness, inventory checks, findings, history bounds and exit status. |
| Sessions and host positions | Session code, desktop/notebook tests and architecture design | `core-concepts/sessions.md` | Desktop versus Fabric execution, resource reuse, lazy Spark startup, workspace scope and supported host-specific behaviour. |
| Catalogue model | Catalogue source, table declarations and design | `core-concepts/catalogue.md` | Certification, installed bindings, runtime state, read-only consumer expectations and upgrade boundaries. |

## Guides

| Missing task | Future authoritative home | Scope |
| --- | --- | --- |
| Create a Lakehouse pipeline | `guides/lakehouse-pipeline.md` | Folder, Python Table and Spark SQL Table declarations; Environment publication; build and load. |
| Create a Warehouse pipeline | `guides/warehouse-pipeline.md` | T-SQL tables/views, keys, load behaviour and programmables. |
| Connect items with shortcuts | `guides/shortcuts.md` | Same-workspace logical shortcuts, physical sources and verification. |
| Write validations | `guides/validation.md` | Python and SQL Tests/Assumptions, installed runs and `--file`. |
| Load incrementally | `guides/incremental-loads.md` | Bookmarks, Folder change history, keyed updates, delete claims and reload. |
| Diagnose a project or workspace | `guides/troubleshooting.md` | `check`, `doctor`, health findings, transport errors and safe retry boundaries. |
| Automate a lifecycle | `guides/automation.md` | Service principals, `--non-interactive`, `--yes`, JSON, workflows and exit codes. |
| Operate multiple environments | `guides/environments.md` | Per-environment bindings, shared Environments and promotion boundaries. |
| Recover and decommission | `guides/recovery.md` | Failed build recovery, dry runs, wipe, unbind and catalogue preservation. |

## CLI commands

The [CLI reference](reference/cli.md) lists every current command and its responsibility. It does not yet provide an option-by-option page with examples, output contracts and failure modes.

| Command family | Future authoritative home | Missing detail |
| --- | --- | --- |
| `initialise` | `reference/cli/initialise.md` | Wizard and unattended requirements, generated files, reuse/conflict rules, dry-run and JSON. |
| `doctor`, `check` | `reference/cli/diagnostics.md` | Probe statuses, exit codes, local validation boundaries and JSON. |
| `build`, `install` | `reference/cli/deployment.md` | Full options, bundle paths, selection reports, retry boundary and installation results. |
| `load` | `reference/cli/load.md` | Name grammar, fault tolerance, reload/stale constraints, dry-run and report schema. |
| `test` | `reference/cli/test.md` | Item/name/file selection, diagnostic rows, exit status and report schema. |
| `health` | `reference/cli/health.md` | Freshness, inventory, status calculation and format version. |
| `wipe` | `reference/cli/wipe.md` | Catalogue dispositions, complete plan/result schemas and destructive ordering. |
| `mirror` | `reference/cli/mirror.md` | Source/destination resolution, item rebinding, confirmation and result schema. |
| `session`, `workflow` | `reference/cli/session-and-workflow.md` | Accepted command language, inheritance, resource reuse, workflow file rules and failure stopping. |
| `fabric environment` | `reference/cli/fabric-environment.md` | Local versus remote authority, released versus development publication and preservation rules. |
| `fabric notebook` | `reference/cli/fabric-notebook.md` | Source formats, naming, default Lakehouse, waiting and timeout behaviour. |
| `fabric capacity` | `reference/cli/fabric-capacity.md` | Azure prerequisites, subscription selection, action results and polling expectations. |

## Python API

`weaver.__all__` defines a substantial import surface, but this site does not yet publish signatures or stability guarantees. Future pages must be generated or checked against that public namespace.

| API group | Public names needing coverage | Future authoritative home |
| --- | --- | --- |
| Operations | `initialise`, `build`, `load`, `test`, `health`, `mirror`, `plan_mirror`, `check_mirror`, `plan_wipe`, `wipe` | `reference/python/operations.md` |
| Session and workspace | `session`, `current_workspace`, `Lakehouse`, `default_lakehouse`, `lakehouse_for` | `reference/python/session.md` |
| Authored objects | `WeaverObject`, `Folder`, `Table`, `View`, `Shortcut`, `SparkSqlTable` | `reference/python/objects.md` |
| Validation objects | `Test`, `Assumption`, `SparkSqlTest`, `SparkSqlAssumption` | `reference/python/validation.md` |
| Result and report types | Initialisation, build, load, validation, health, mirror and wipe result classes exported by `weaver` | `reference/python/results.md` |
| Exceptions | `WeaverError`, `CommandError`, `ConfigError`, `IdentityError`, `ValidationError` | `reference/python/errors.md` |

The API reference must distinguish public exports from importable internal modules. Real projects that import `weaver.catalogue`, `weaver.operations` or other internal paths do not by themselves make those paths supported extensions.

## Contracts

| Missing contract | Current authority | Future authoritative home | Required precision |
| --- | --- | --- | --- |
| Workspace configuration | Config parser and declaration tests | `contracts/workspace-config.md` | All keys, value types, defaults, environment references, target execution settings, precedence and errors. |
| Workflow configuration | CLI workflow parser and tests | `contracts/workflow.md` | File shape, accepted command language, forbidden nesting/shell syntax, confirmation and propagation rules. |
| Project documents | Metadata and repository parsers plus fixtures | `contracts/documents.md` | Supported kinds, paths, headers, keys, defaults, type/nullability grammar and validation errors. |
| Python-authored objects | Object base classes and repository AST validation | `contracts/python-authoring.md` | Required class names/methods, static restrictions, runtime context and return contracts. |
| SQL-authored objects | SQL program readers and tests | `contracts/sql-authoring.md` | Metadata blocks, statement structure, dialect-specific constraints, inferred versus declared schema and load/delete queries. |
| Shortcut declarations | Shortcut readers and tests | `contracts/shortcuts.md` | Exact Python/YAML schema, target grammar and unsupported combinations. |
| Build bundle | Build bundle model, serializer and invariant tests | `contracts/build-bundle.md` | Directory/archive layout, manifest and payload hashes, identity, compatibility and validation errors. |
| CLI JSON | Renderers and representation tests | `contracts/cli-json.md` | Per-command schemas, format versions, nullability, partial reports and error envelope. |
| Exit codes | CLI handlers and interaction tests | `contracts/exit-codes.md` | Success, domain failure, health status, refusal, parser failure and interruption. |
| Catalogue | Catalogue table declarations and compatibility tests | `contracts/catalogue.md` | Supported read surface, columns, keys, meanings, schema/version compatibility and prohibition on manual writes. |
| Environment definition | Environment definition parser and publication tests | `contracts/environment.md` | Directory parts, package overlay ownership, local/remote authority and preservation guarantees. |

## Explicitly withheld claims

The initial site does not claim:

- compatibility guarantees for bundle or catalogue formats beyond current source behaviour;
- stability for internal Python modules;
- a complete list of metadata keys or configuration fields;
- a universal authentication prerequisite beyond the implemented credential chain;
- that all Fabric workspaces expose every Doctor probe;
- that an Environment is required for Warehouse-only work;
- that workflow files are a general orchestration language;
- that `--json` schemas are stable where no format/version contract is documented;
- that source design documents are themselves a supported public API.

Those claims remain withheld until the mapped contract or reference page can state and test them precisely.
