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

## Established contract

- [Load](load.md) — selection, dependencies, execution, outcomes, bookmarks and fault tolerance.

A contract states only behaviour supported by current source and tests. Examples may illustrate that behaviour, but an example does not enlarge the guarantee.
