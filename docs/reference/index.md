# Reference

Use Reference to look up current public interfaces, exact representations and operation behaviour.

| Area | Use it to look up |
| --- | --- |
| [Weaver documents](weaver-documents/overview.md) | Authored locations, forms and metadata. |
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
