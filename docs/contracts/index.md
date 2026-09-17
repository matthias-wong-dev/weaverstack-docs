# Contracts

Contracts are machine-consumed or compatibility-sensitive public surfaces. They need exact field, type, versioning and failure rules rather than narrative examples.

The current site establishes these boundaries:

- a project is organised by logical `Lakehouse/<name>` and `Warehouse/<name>` items;
- `workspace-config.yml` binds those items to Fabric and `workflow.yml` stores ordered CLI command lines;
- build freezes source interpretation into a bundle before installation;
- `--json` commands emit one JSON document on stdout;
- the catalogue in Warehouse schema `_` is Weaver-managed installed and operational state.

Dedicated references are still required for:

- every recognised project document and metadata field;
- workspace and workflow configuration schemas;
- shortcut declarations;
- build bundle layout and compatibility;
- command JSON schemas and exit codes;
- catalogue tables and supported read contracts;
- Python operation signatures, result types and exceptions.

These are mapped to future pages in the [coverage gap map](../gaps.md). Until those pages exist, do not infer a stable field from an internal dataclass or a single example.
