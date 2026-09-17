# Core concepts

Core concepts explain the mental model needed to understand and operate Weaver. They describe public behaviour and its consequences, not the internal arrangement of the source code.

The model begins with [How Weaver works](how-weaver-works.md):

```text
Project declarations
        ↓
Physical bindings
        ↓
Build
        ↓
Load / Test
        ↓
Operational state
        ↓
Health
```

Read the model in layers:

- [Projects and estates](projects-and-estates.md) separates project source, installed state and operational state.
- [Logical and physical items](logical-and-physical-items.md) explains how stable project identities bind to Fabric targets.
- [Resources and artefacts](resources-and-artefacts.md) separates what you author from what Weaver installs and runs.
- [Dependencies](dependencies.md) explains ordering, change impact and item-selection boundaries.
- [The Weaver catalogue](catalogue.md) describes the shared installed and operational state behind Build, Load, Test and Health.

Later pages will cover workflows, fault tolerance, local and Fabric execution, and mirrors in more depth.
