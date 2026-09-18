# Contracts

A contract states Weaver's specified public behaviour precisely enough to guide use, implementation and acceptance testing. Contracts cover selection, ordering, execution boundaries, state changes, outcomes and failures; they do not turn internal implementation choices or observed formats into promises.

## Project and identity

- [Project](project.md) — project boundaries, source discovery and Check/Build consumption.
- [Weaver documents](documents.md) — supported authored families, placement and agreement rules.
- [Identity and naming](identity-and-naming.md) — logical identities, physical bindings, reserved namespaces and collisions.
- [Configuration](configuration.md) — workspace configuration, precedence, target bindings and estate switching.

## Planning and installed state

- [Catalogue](catalogue.md) — ownership, publication, certification, runtime state and read boundaries.
- [Dependencies](dependencies.md) — inferred and declared relationships, Build impact and execution boundaries.
- [Signatures and change detection](signatures-and-change-detection.md) — installed equality, physical reconciliation, pruning and certification.
- [Selection](selection.md) — logical items, installed names, physical targets and operation-specific boundaries.

## Lifecycle operations

- [Build](build.md) — source snapshots, selection, planning, bundles, installation and certification.
- [Load](load.md) — selection, dependencies, execution, outcomes, bookmarks and fault tolerance.
- [Test](test.md) — installed and source-file validation, outcomes, strict mode and recording.
- [Workflow](workflow.md) — command composition, shared Session, confirmation and stop-on-failure behaviour.

Read [Fault tolerance](fault-tolerance.md) with an operation contract when failure or partial work matters; continuation and blocking differ by operation.

## State and long-running work

- [State and health](state-and-health.md) — current evidence, freshness, findings and Green/Amber/Red status.
- [Fault tolerance](fault-tolerance.md) — operation-specific failure barriers, continuation and partial work.
- [Incremental processing](incremental-processing.md) — bookmarks, keyed changes, Folder history, stability and reload.
- [History](history.md) — current state, append-only records, workflow correlation and retention boundaries.
- [Mirror](mirror.md) — estate copying, rebinding, borrowed forms, localisation and destructive boundaries.

## Schema, runtime and interfaces

- [Schema](schema.md) — columns, keys, inference, managed columns and validation boundaries.
- [Runtime](runtime.md) — installed execution, Session context, engine boundaries and result publication.
- [Host behaviour](host-behaviour.md) — desktop, attached-notebook and cross-workspace execution positions.
- [CLI behaviour](cli-behaviour.md) — parsing, interaction, authorisation, streams, status and interruption.

Use [Reference](../reference/index.md) for exact command syntax and current machine formats. A reference example illustrates behaviour but does not enlarge a contract.