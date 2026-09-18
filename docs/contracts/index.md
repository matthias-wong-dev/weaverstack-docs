# Contracts

A contract specifies public behaviour precisely enough to guide use, implementation and acceptance testing without turning internal implementation choices into promises.

Contracts include syntax and interfaces, but they also cover behavioural semantics: selection, ordering, state changes, outcomes, failure boundaries and host-specific qualifications.

The contract surface includes:

- projects, Weaver documents, identity and naming;
- configuration, catalogue state and dependencies;
- signatures and change detection;
- build, load, test and workflow behaviour;
- selection, state and health;
- schema, runtime and host behaviour;
- fault tolerance, incremental processing and history;
- mirrors and CLI behaviour;
- machine-readable interfaces.

## Contracts

- [Project](project.md) — project boundaries, source discovery and Check/Build consumption.
- [Weaver documents](documents.md) — supported authored families, placement and agreement rules.
- [Identity and naming](identity-and-naming.md) — logical identities, physical bindings, reserved namespaces and collisions.
- [Configuration](configuration.md) — workspace configuration, precedence, target bindings and estate switching.
- [Catalogue](catalogue.md) — ownership, publication, certification, runtime state and read boundaries.
- [Dependencies](dependencies.md) — inferred and declared relationships, Build impact and execution boundaries.
- [Signatures and change detection](signatures-and-change-detection.md) — installed equality, physical reconciliation, pruning and certification.
- [Load](load.md) — selection, dependencies, execution, outcomes, bookmarks and fault tolerance.

A contract states only behaviour supported by current source and tests. Examples may illustrate that behaviour, but an example does not enlarge the guarantee.
