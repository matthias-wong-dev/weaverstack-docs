# Core concepts

Core concepts explain the mental model needed to understand and operate Weaver. They describe public behaviour and its consequences, not the internal arrangement of the source code.

The model begins with [How Weaver works](how-weaver-works.md):

```text
Weaver documents
        ↓
Logical estate + workspace bindings
        ↓
Build → Load → Test
        ↓
Catalogue state → Health
```

Read the model in layers:

- [Projects and estates](projects-and-estates.md) separates project source, installed state and operational state.
- [Logical and physical items](logical-and-physical-items.md) explains how stable project identities bind to Fabric targets.
- [Weaver documents](weaver-documents.md) explains how paths, document types and metadata declare the estate.
- [Dependencies](dependencies.md) explains ordering, change impact and item-selection boundaries.
- [The Weaver catalogue](catalogue.md) describes the installed and operational state behind Build, Load, Test and Health.
- [The development cycle](development-cycle.md) shows how a configuration switch and mirror establish a development estate from production.

Build, Load and Test form the central lifecycle. Mirrors, Sessions and workflows compose that lifecycle into normal development and operation.
