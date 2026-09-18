# Reference

Reference pages describe current public interfaces tersely and precisely. Use them to look up syntax and shapes; use [Guides](../guides/index.md) for complete tasks and [Contracts](../contracts/index.md) for behavioural guarantees.

## Invoke Weaver

- [CLI reference](cli.md) — shared options, selection grammar and a generated page for every executable command.
- [Python API](python/index.md) — every public top-level export, its call shape and returned result types.

For options in an installed CLI version, run:

```bash
weaver <command> --help
```

## Exchange and publish definitions

- [Fabric Environment definition](environment-definition.md) — accepted directory parts, package overlays and publication boundaries.
- [Build bundle](build-bundle.md) — current manifest, payload and installation handoff.

## Inspect machine state

- [Machine-readable interfaces](machine-readable-interfaces.md) — current CLI JSON documents and exit outcomes.
- [Catalogue schema](catalogue-schema.md) — current public `_` tables, columns and keys.

These pages record current formats where no separate compatibility policy exists. They do not make every machine shape or stored column a stable cross-version contract. For specified operation semantics, continue to the [Contracts index](../contracts/index.md).