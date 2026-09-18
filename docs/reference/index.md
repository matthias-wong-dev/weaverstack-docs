# Reference

Reference pages describe current public interfaces and exact operation behaviour.

- [Weaver documents](weaver-documents/overview.md) — authored locations, forms and metadata.
- [Python API](python/index.md) — public exports, call shapes and result types.
- [CLI](cli.md) — shared options and generated pages for executable commands.
- [Configuration files](configuration-files/index.md) — workspace, workflow and Fabric Environment definitions.
- [Operation behaviour](operation-behaviour/index.md) — selection, state changes, outcomes and failure boundaries.
- [Catalogue schema](catalogue-schema.md) — public `_` tables, columns and keys.
- [Build bundle format](build-bundle-format.md) — manifest, payload and installation handoff.
- [Machine-readable output](machine-readable-output.md) — current CLI JSON documents and exit outcomes.

For options in an installed CLI version, run:

```bash
weaver <command> --help
```

These pages record current formats where no separate compatibility policy exists. They do not make every machine shape or stored column a stable cross-version contract.
