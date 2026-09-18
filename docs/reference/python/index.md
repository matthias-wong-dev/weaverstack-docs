# Python API

The public Python surface is the set of names exported by `weaver.__all__`. Import these names from `weaver`; importable internal modules are not part of this reference.

Use [operations](operations.md) to run lifecycle work and [Session and workspace helpers](session.md) to share a workspace context across calls. The remaining pages own the public types:

- [Authored objects](objects.md)
- [Validation objects](validation.md)
- [Results and reports](results.md)
- [Exceptions](errors.md)

The [CLI reference](../cli.md) covers equivalent command-line entry points. [Build, Load and Test](../../core-concepts/build-load-and-test.md) explains the lifecycle boundaries rather than repeating them here.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

- `weaver.__version__` — value

<!-- END GENERATED PYTHON -->

Signatures on these pages are generated from the public export authority and source declarations. Class entries identify the exported type without synthesising a constructor signature from dataclass fields or runtime behaviour.
