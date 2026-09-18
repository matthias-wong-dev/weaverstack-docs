# Core concepts

Core concepts explain the public model needed to design and operate a Weaver estate. They describe consequences visible to a user, not the internal arrangement of the source code.

Begin with [How Weaver works](how-weaver-works.md) for the complete model, then follow the sequence behind the work:

```text
Weaver documents
        ↓
Build → Load → Test
        ↓
Catalogue state
        ↓
Development cycle
        ↓
Dependencies and fault tolerance
```

## Establish the estate boundary

- [Projects and estates](projects-and-estates.md) separates version-controlled source, installed Fabric definitions and operational catalogue state.
- [Logical and physical items](logical-and-physical-items.md) explains how stable project identities bind to environment-specific Fabric targets.

Read these first when one project must address development and production estates without changing its logical identities.

## Follow authored work into operation

- [Weaver documents](weaver-documents.md) explains how paths, document types and metadata declare the estate.
- [Weaver operations](weaver-operations.md) explains how Build, Load and Test turn those documents into installed definitions, data and validation outcomes.
- [The Weaver catalogue](catalogue.md) describes the recorded state behind Build, Load, Test and Health.
- [The development cycle](development-cycle.md) shows how a configuration switch and Mirror establish a development estate from production.

## Reason about ordering and failure

- [Dependencies](dependencies.md) explains operation order, change impact and item-selection boundaries.
- [Fault tolerance](fault-tolerance.md) explains what each operation attempts after work fails.

Concepts explain why the system behaves this way. Use [Guides](../guides/index.md) to complete a task, [Reference](../reference/index.md) to look up an interface and [Contracts](../contracts/index.md) for precise behavioural boundaries.