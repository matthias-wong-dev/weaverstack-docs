# Reference

Use Reference to look up current public interfaces, exact representations and operation behaviour. For a worked task, start with [Lakehouse](../lakehouse/index.md), [Warehouse](../warehouse/index.md), [Semantic models](../semantic-models/index.md), [Reports](../reports/index.md) or [Coordinate your estate](../estate/index.md).

## Find the definition for your item

| Item | Authored definitions and relevant interfaces |
| --- | --- |
| Lakehouse | [Python and Spark SQL Tables](weaver-documents/table.md), [Folders](weaver-documents/folder.md), [Shortcuts](weaver-documents/shortcut.md), [Python authoring](python/objects.md) and [runtime requirements](operation-behaviour/session-runtime.md#fabric-environment-qualification). |
| Warehouse | [T-SQL Tables](weaver-documents/table.md#t-sql), [Views](weaver-documents/view.md), [schema metadata](weaver-documents/schema-metadata.md) and [programmables](weaver-documents/warehouse-programmable.md). |
| Semantic models | [Native layout](power-bi/project-layout.md#model-discovery-and-identity), [TMDL merging](power-bi/tmdl.md), [annotations](power-bi/annotations.md), [extension API](python/semantic-models.md) and [DAX validations](power-bi/validations.md). |
| Reports | [Discovery and local model association](power-bi/project-layout.md#report-discovery-and-association), [deployment binding](power-bi/requirements-and-compatibility.md#report-binding) and [target mappings](configuration-files/workspace-config.md#targets). |

For Lakehouse and Warehouse validation declarations, use [Test](weaver-documents/test.md), [Assumption](weaver-documents/assumption.md) and [Python validation objects](python/validation.md). [Test behaviour](operation-behaviour/test.md) distinguishes installed definitions and recorded results from source/file execution. Reports have no Load or Test; refresh and validate their semantic model.

## Look up a shared operation

[Selection and identity](operation-behaviour/shared-selection-and-identity.md) defines item and document names. [Load selection](operation-behaviour/load.md#selection) defines whole-name regular expressions and ancestor/descendant expansion; [reload](operation-behaviour/load.md#reload) defines the destructive scope. [Workspace execution settings](configuration-files/workspace-config.md#execution) defines resource ceilings alongside the invocation caps in [Build](cli/build.md), [Load](cli/load.md) and [Test](cli/test.md).

[Model source mappings and connections](power-bi/requirements-and-compatibility.md#source-mapping-and-connections) are distinct from destination names and credentials. [Build behaviour](operation-behaviour/build.md#inputs-and-selection) defines the separate source-item and model/Report Build calls. For recorded estate evidence, use [Health behaviour](operation-behaviour/health.md) and the [catalogue schema](catalogue-schema.md).

## Complete reference areas

| Area | Use it to look up |
| --- | --- |
| [Weaver documents](weaver-documents/overview.md) | Authored locations, forms and metadata. |
| [Semantic models and Reports](power-bi/index.md) | Native project layout, TMDL policy/composition, annotations, DAX validations and compatibility modes. |
| [Python API](python/index.md) | Public exports, call shapes and result types. |
| [CLI](cli.md) | Commands, options and shared CLI behaviour. |
| [Configuration files](configuration-files/index.md) | Workspace, workflow and Fabric Environment definitions. |
| [Operation behaviour](operation-behaviour/index.md) | Selection, state changes, outcomes and failure boundaries. |
| [Catalogue schema](catalogue-schema.md) | Public `_` tables, columns, types and keys. |
| [Build bundle format](build-bundle-format.md) | Manifest, payload and destination-bound installation handoff. |
| [Machine-readable output](machine-readable-output.md) | Command-specific CLI JSON documents and exit outcomes. |

For options in an installed CLI version, run:

```bash
weaver <command> --help
```

These pages record current formats where no separate compatibility policy exists. They do not make every machine shape or stored column a stable cross-version contract.
