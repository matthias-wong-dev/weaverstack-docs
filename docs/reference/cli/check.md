# `weaver check`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver check [-h] [--json] [--non-interactive] [PROJECT_FOLDER]
```

## Positional arguments

`PROJECT_FOLDER`
: Project folder. Defaults to the current directory.

## Options

`-h, --help`
: show this help message and exit

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->

## Responsibility and selection

Parse and validate a Weaver project without contacting Fabric. The positional folder defaults to the current directory.

Check discovers the recognised Weaver project trees, validates declarations and dependency structure, and does not execute authored Python. Unrelated files inside item directories are ignored by project discovery.

## Execution

The command reads the project from disk. It requests no Fabric session, workspace, catalogue, Environment, or credentials.

## Interaction

After a project error in an interactive terminal, Weaver can offer to retry so an edited project is read again. `--non-interactive` and `--json` return after one attempt without prompting.

## Output and exit behaviour

A valid project prints `Project valid.`. A project error is written to stderr and the command exits `1`.

`--json` emits one document. Success currently contains `status` and the resolved `project_folder`; failure contains `status` and an error message. These fields are current output, not a declared compatibility contract.

The command exits `0` for a valid project and `1` for project discovery, metadata, identity, or graph errors. Argument errors exit through `argparse`.

## Examples

```bash
weaver check
weaver check ./parcel --non-interactive
weaver check ./parcel --json
```
