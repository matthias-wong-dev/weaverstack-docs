# Core concepts

Core concepts explain the mental model needed to understand and operate Weaver. They describe public behaviour and its consequences, not the internal arrangement of the source code.

The model begins with [How Weaver works](how-weaver-works.md):

```text
Weaver documents
        ↓
Build → Load → Test
        ↓
Catalogue state
        ↓
Development cycle
```

Read the model in layers:

- [Projects and estates](projects-and-estates.md) separates project source, installed state and operational state.
- [Logical and physical items](logical-and-physical-items.md) explains how stable project identities bind to Fabric targets.
- [Weaver documents](weaver-documents.md) explains how paths, document types and metadata declare the estate.
- [Weaver operations](weaver-operations.md) explains how Build, Load and Test turn those documents into an installed and operating estate.
- [The Weaver catalogue](catalogue.md) describes the installed and operational state behind Build, Load, Test and Health.
- [The development cycle](development-cycle.md) shows how a configuration switch and mirror establish a development estate from production.
- [Dependencies](dependencies.md) explains ordering, change impact and item-selection boundaries.
- [Fault tolerance](fault-tolerance.md) explains what each operation attempts after work fails.

This order follows the user's work: author documents, operate them, inspect the resulting catalogue state, and repeat the cycle. Dependencies and fault tolerance explain how that work is ordered and how it proceeds after failure.
