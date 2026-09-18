# Internal documentation coverage map

This maintainer-only map records what the public site does not yet explain. It lives outside `docs/` and is not rendered on `docs.weaverstack.dev`. A named path is an ownership decision, not a claim that the page or contract already exists.

## Concepts

The accepted Core sequence now covers the public mental model: Weaver documents, operations, catalogue state, the development cycle, dependencies and fault tolerance. Task-specific detail belongs in Guides; precise behavioural commitments belong in Contracts. Do not create extra concept pages merely to mirror source modules.

The foundation and lifecycle contracts now own identity, source discovery, change detection, validation, state and health. The final integration pass should remove conceptual repetition rather than create matching Core pages.

## Guides

The mapped authoring, operating and automation tasks now have substantive guides. Remaining work is integration: connect them to new contracts and reference pages, remove repetition, and check the complete reader journeys during Batch 12.

## CLI commands

The generated CLI reference owns all 17 current parser leaves across 15 pages. `tools/generate_cli_reference.py` rejects unassigned, duplicate and retired commands and detects checked-in generated-block drift.

Compatibility promises for JSON shapes and exit-code taxonomy remain withheld pending the interface decisions recorded below.

## Python API

The generated Python reference owns all 51 names in `weaver.__all__` across seven pages. `tools/generate_python_reference.py` rejects unassigned, duplicate and retired exports and detects checked-in generated-block drift.

The reference distinguishes public top-level exports from importable internal modules. It does not claim compatibility for nested implementation types or current machine mappings.

## Contracts

Foundation and lifecycle behaviour is covered through Build, Load, Test, Workflow, selection, state and health, fault tolerance, incremental processing, history and Mirror. The remaining contracts are exact authored formats and machine/host interfaces whose compatibility boundaries require care.

| Missing contract | Current authority | Future authoritative home | Required precision |
| --- | --- | --- | --- |
| Python-authored objects | Object base classes and repository AST validation | `contracts/python-authoring.md` | Required class names/methods, static restrictions, runtime context and return contracts. |
| SQL-authored objects | SQL program readers and tests | `contracts/sql-authoring.md` | Metadata blocks, statement structure, dialect-specific constraints, inferred versus declared schema and load/delete queries. |
| Shortcut declarations | Shortcut readers and tests | `contracts/shortcuts.md` | Exact Python/YAML schema, target grammar and unsupported combinations. |
| Build bundle | Build bundle model, serializer and invariant tests | `contracts/build-bundle.md` | Directory/archive layout, manifest and payload hashes, identity, compatibility and validation errors. |
| CLI JSON | Renderers and representation tests | `contracts/cli-json.md` | Per-command schemas, format versions, nullability, partial reports and error envelope. |
| Exit codes | CLI handlers and interaction tests | `contracts/exit-codes.md` | Success, domain failure, health status, refusal, parser failure and interruption. |
| Catalogue compatibility | Catalogue table declarations and compatibility tests | existing `contracts/catalogue.md` or a generated schema reference | Decide whether columns, keys and schema versions form a supported consumer interface beyond the established table purposes and read-only boundary. |
| Environment definition | Environment definition parser and publication tests | `contracts/environment.md` | Directory parts, package overlay ownership, local/remote authority and preservation guarantees. |

## Explicitly withheld claims

The site does not claim:

- compatibility guarantees for bundle or catalogue formats beyond current source behaviour;
- stability for internal Python modules;
- a complete compatibility contract for every authored metadata key;
- a universal authentication prerequisite beyond the implemented credential chain;
- that all Fabric workspaces expose every Doctor probe;
- that an Environment is required for Warehouse-only work;
- that workflow files are a general orchestration language;
- that `--json` schemas are stable where no format/version contract is documented;
- that source design documents are themselves a supported public API.

Those claims remain withheld until the mapped contract or reference page can state and test them precisely.
