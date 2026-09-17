# Contracts

A contract states behaviour a Weaver user can rely on. It is precise enough to guide use, implementation and acceptance testing without turning internal implementation choices into promises.

Contracts include syntax and interfaces, but they also cover behavioural semantics: selection, ordering, state changes, outcomes, failure boundaries and host-specific qualifications.

The contract surface includes:

- projects, resources, identity and naming;
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
