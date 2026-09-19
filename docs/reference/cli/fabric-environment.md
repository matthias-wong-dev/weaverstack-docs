# `weaver fabric environment`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver fabric environment publish [-h] [--path DIRECTORY] [--dev] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [ENVIRONMENT]
```

## Positional arguments

`ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

## Options

`-h, --help`
: show this help message and exit

`--path DIRECTORY`
: Local <Name>.Environment definition directory. It names the Environment and supplies the complete definition.

`--dev`
: Supply Weaver as a wheel built from this checkout.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

<!-- END GENERATED CLI -->

## Responsibility and selection

`fabric environment publish` supplies Weaver to a Fabric Environment. Choose exactly one source:

- `ENVIRONMENT` names an existing Environment. An unqualified name needs `--workspace` or workspace configuration; `Workspace/Environment` supplies its owner.
- `--path DIRECTORY` names a local `<Name>.Environment` directory. The directory name selects the Environment, and `--workspace` or workspace configuration selects its workspace.

`ENVIRONMENT` and `--path` cannot be combined.

## Execution

With `ENVIRONMENT`, Weaver updates only its own staged libraries and preserves the Environment's other libraries and settings. The Environment must already exist.

With `--path`, Weaver reads the complete local definition, overlays the Weaver libraries, and creates or updates the named Environment. The complete definition includes the Environment settings and libraries represented by that directory.

By default, the Environment receives the released Weaver requirement. `--dev` builds a wheel from the current Weaver checkout and supplies that wheel with its Fabric runtime dependencies. An already matching, successfully published Environment is left unchanged. Otherwise the command waits for publication to settle and fails if Fabric reports an unsuccessful result.

## Interaction

The command has no destructive confirmation and does not accept `--yes`. `--non-interactive` prevents browser sign-in; configured unattended credentials must then be sufficient.

## Output and exit behaviour

Progress is written to stderr. Stdout always contains one JSON result document, including the selected Environment, publication mode, action, status and timings. There is no separate `--json` option. Treat the document as command output, not as a versioned schema guarantee.

The command exits `0` when publication succeeds or no update is needed. Invalid source selection, a missing existing Environment, wheel-build failure, authentication failure, publication failure or timeout produces a non-zero status.

## Examples

Publish released Weaver libraries into an existing Environment:

```bash
weaver fabric environment publish ParcelRuntime \
  --workspace "Parcel Development" \
  --non-interactive
```

Publish a complete local definition:

```bash
weaver fabric environment publish \
  --path Environment/ParcelRuntime.Environment \
  --workspace "Parcel Development"
```

## Pre-release source checkout

Use the commands above without `--dev` for a released Weaver installation. `--dev` is only for testing an unreleased source checkout in Fabric: it builds that checkout as a wheel and publishes the wheel with its Fabric runtime dependencies.

Install the checkout in editable mode so the `weaver` executable and imported module both resolve to that source tree, then invoke that executable:

```bash
git clone https://github.com/matthias-wong-dev/weaverstack.git
cd weaverstack
python -m venv .venv
.venv/bin/python -m pip install -e .

.venv/bin/weaver fabric environment publish \
  --path ../parcel-ops/Environment/ParcelRuntime.Environment \
  --workspace "Parcel Development" \
  --dev
```

On Windows, use `.venv\Scripts\python.exe` and `.venv\Scripts\weaver.exe`. The package declares the wheel builder needed by `--dev`. The command finds the checkout from the installed `weaver` module, not from an unrelated `pyproject.toml` in the current directory. A released installation should continue to use normal publication rather than `--dev`.
