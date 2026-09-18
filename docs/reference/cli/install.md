# `weaver install`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver install [-h] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] BUNDLE
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

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

<!-- END GENERATED CLI -->

## Responsibility and selection

Install a deployment bundle created by `weaver build --bundle-only`. `BUNDLE` is a bundle directory or `.weaver.zip` archive.

Install accepts a Fabric workspace directly or through workspace configuration. The bundle already contains the planned deployment, so this command accepts neither a catalogue nor an Environment override.

## Execution

The command opens the selected workspace, validates and reads the frozen bundle, and executes its installation actions. It does not reopen project source or recalculate build selection.

## Interaction

Install does not ask for deployment choices. Interactive credential selection may use browser sign-in; `--non-interactive` prevents browser sign-in and other prompts.

## Output and exit behaviour

Human output reports succeeded, failed, and skipped action counts followed by the bundle identifier.

`--json` emits the current installation report as one JSON document. Its fields and bundle format are not presented here as compatibility contracts.

The command exits `0` when the installation report succeeds and `1` when it reports failure or raises a command error. Argument errors exit through `argparse`.

## Examples

```bash
weaver install ./dist/parcel-bundle \
  --workspace-config workspace-config.yml
```

```bash
weaver install ./dist/parcel-bundle.weaver.zip \
  --workspace "Parcel Production" \
  --non-interactive \
  --json
```
