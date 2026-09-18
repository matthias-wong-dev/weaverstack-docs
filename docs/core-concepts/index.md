# Core concepts

Core concepts explain the public model needed to design and operate a Weaver estate.

Begin with [How Weaver works](how-weaver-works.md) for the complete model, then read [Design philosophy](design-philosophy.md) for the principles behind it. Follow the sequence behind the work:

```text
Weaver documents
        ↓
Build → Load → Test
        ↓
Catalogue and health state
        ↓
Dependencies and fault tolerance
```

## Establish the estate boundary

- [Projects and estates](projects-and-estates.md) separates version-controlled source, installed Fabric definitions and operational catalogue state.
- [Logical and physical items](logical-and-physical-items.md) explains how stable project identities bind to environment-specific Fabric targets.
- [Weaver documents](weaver-documents.md) explains how paths, document types and metadata declare the estate.

## Follow authored work into operation

- [Build, Load and Test](build-load-and-test.md) explains how authored work becomes installed definitions, data and validation outcomes.
- [Catalogue](catalogue.md) describes the recorded state behind Build, Load, Test and Health.
- [State and health](state-and-health.md) explains the current estate view.
- [Mirrors](mirrors.md) explains borrowed and locally materialised state.
- [Sessions and workflows](sessions-and-workflows.md) explains shared execution context and ordered command composition.

## Reason about ordering and failure

- [Dependencies](dependencies.md) explains operation order, change impact and item-selection boundaries.
- [Fault tolerance](fault-tolerance.md) explains what each operation attempts after work fails.

Use [Basics](../basics/index.md) to complete normal work and [Reference](../reference/index.md) to look up exact interfaces and behaviour.
