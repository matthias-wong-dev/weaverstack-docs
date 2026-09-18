# Python exceptions

Catch public Weaver exceptions from the top-level package:

```python
from weaver import CommandError, WeaverError

try:
    report = operation()
except CommandError as exc:
    print(exc)
except WeaverError as exc:
    print(exc)
```

`WeaverError` is the common public root. The narrower classes below identify failures callers can usually classify. Other operation-specific subclasses may appear at runtime but are not top-level public imports; catch `WeaverError` when none of the exported categories fits.

These are Python exceptions, not CLI exit-code categories or YAML validation records. For command-line recovery and output, use [Troubleshooting](../../guides/troubleshooting.md), [Automation](../../guides/automation.md), and the [CLI reference](../cli.md).

## `WeaverError`

```python
WeaverError(message: object, *, executor: str | None = None)
```

Base class for Weaver-originated errors and a subclass of `Exception`. `str(exc)` renders `message`. `executor` identifies the execution location when an exception boundary supplied one; otherwise it is `None`.

Catching this class does not catch unrelated Python exceptions such as `KeyError`, `TypeError`, or errors raised directly by user code.

## `CommandError`

```python
CommandError(message: object, *, executor: str | None = None)
```

Raised when an explicitly requested operation is invalid. Examples include incompatible operation arguments, an unresolved requested target, or a destructive plan that violates its preconditions.

Use this class when application control flow distinguishes a rejected request from other Weaver failures.

## `ConfigError`

```python
ConfigError(message: object, *, executor: str | None = None)
```

Raised when workspace configuration or supplied configuration-dependent values are invalid. This category covers configuration parsing and validation, not every missing runtime prerequisite.

See [Workspaces and Environments](../../guides/environments.md) for the configuration boundary.

## `IdentityError`

```python
IdentityError(message: object, *, executor: str | None = None)
```

Raised when a target, item, repository, or location identity is malformed. The message identifies the rejected value or grammar where the parser has that context.

## `ValidationError`

```python
ValidationError(
    message: str,
    *,
    result: object | None = None,
    report: Any | None = None,
)
```

Raised when a Test or Assumption cannot be evaluated, or when strict validation rejects a completed run.

- `result` carries a failed-to-run validation result when one is available.
- `report` carries the completed validation report when strict mode rejects its outcome.

The two attributes default to `None`. `ValidationError` does not accept the `executor` keyword exposed by the other constructors on this page.

A validation that executes and finds discrepancies or violations is represented as a failed validation outcome. An evaluation failure is distinct and must not be interpreted as a passing result. See [Validate an installed estate](../../guides/validation.md).
