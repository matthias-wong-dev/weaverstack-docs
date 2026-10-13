# `weaver install`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver install [-h] [--json] [--non-interactive] BUNDLE
```

## Positional arguments

`BUNDLE`
: Bundle directory or .weaver.zip archive.

## Options

`-h, --help`
: show this help message and exit

`--json`
: Emit the report as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->

## Responsibility and selection

Install a complete local directory or `.weaver.zip` bundle prepared by Build. The format-5 manifest freezes workspace, targets, catalogue, Environment and any Spark attachment. Install accepts no workspace/configuration, catalogue, Environment, item or target override. It does not reopen source or replan against later destination state.

## Execution and outcomes

The local handoff is validated, including graph, frozen execution context, driver contracts, bundle identity and payload hashes, before actions run. Ready actions execute under their dependency/resource/exclusion rules; presentation sequences are not serial barriers. Earlier and independent effects can remain after a later failure; no operation-wide rollback is provided.

There is no deployment-choice prompt. `--non-interactive` prevents input/browser sign-in without changing the frozen scope. Human output reports action counts and bundle identity; `--json` returns the installation report. CLI exit is `0` when required completion succeeds, `1` for installation/validation failures and `2` for parser usage errors.

```bash
weaver install ./dist/parcel-bundle
weaver install ./dist/parcel-bundle.weaver.zip --non-interactive --json
```

See [Build bundle format](../build-bundle-format.md) for paths/integrity and [Build behaviour](../operation-behaviour/build.md) for plan/state semantics.
