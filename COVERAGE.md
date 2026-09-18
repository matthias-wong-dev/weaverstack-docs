# Internal documentation coverage map

This maintainer-only map records what the public site does not yet explain. It lives outside `docs/` and is not rendered on `docs.weaverstack.dev`. A named path is an ownership decision, not a claim that the page or contract already exists.

## Concepts

The accepted Core sequence now covers the public mental model: Weaver documents, operations, catalogue state, the development cycle, dependencies and fault tolerance. Task-specific detail belongs in Guides; precise behavioural commitments belong in Contracts. Do not create extra concept pages merely to mirror source modules.

The foundation, lifecycle and interface contracts now own identity, source discovery, change detection, schema, runtime, host, CLI, validation, state and health. The final integration pass should remove conceptual repetition rather than create matching Core pages.

## Guides

The mapped authoring, operating and automation tasks now have substantive guides. Remaining work is integration: connect them to new contracts and reference pages, remove repetition, and check the complete reader journeys during Batch 12.

## CLI commands

The generated CLI reference owns all 17 current parser leaves across 15 pages. `tools/generate_cli_reference.py` rejects unassigned, duplicate and retired commands and detects checked-in generated-block drift.

The machine-readable-interface reference records the current command-specific JSON shapes and exit outcomes. It does not turn unversioned output into a compatibility promise.

## Python API

The generated Python reference owns all 51 names in `weaver.__all__` across seven pages. `tools/generate_python_reference.py` rejects unassigned, duplicate and retired exports and detects checked-in generated-block drift.

The reference distinguishes public top-level exports from importable internal modules. It does not claim compatibility for nested implementation types or current machine mappings.

## Contracts

Foundation, lifecycle and interface behaviour is covered through Build, Load, Test, Workflow, selection, state and health, schema, runtime, host behaviour, CLI behaviour, fault tolerance, incremental processing, history and Mirror. Current Environment, build-bundle, machine-output and catalogue shapes are recorded under Reference where no compatibility policy exists.

The following authored-format contracts remain optional post-launch depth rather than gaps in the accepted public model:

| Possible contract | Current authority | Future authoritative home | Required precision |
| --- | --- | --- | --- |
| Python-authored objects | Object base classes and repository AST validation | `contracts/python-authoring.md` | Required class names/methods, static restrictions, runtime context and return contracts. |
| SQL-authored objects | SQL program readers and tests | `contracts/sql-authoring.md` | Metadata blocks, statement structure, dialect-specific constraints, inferred versus declared schema and load/delete queries. |
| Shortcut declarations | Shortcut readers and tests | `contracts/shortcuts.md` | Exact Python/YAML schema, target grammar and unsupported combinations. |

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

Those claims remain withheld until the product establishes and tests them precisely.
