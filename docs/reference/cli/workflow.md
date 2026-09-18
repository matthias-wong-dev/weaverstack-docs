# `weaver workflow`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver workflow [-h] [--file PATH] [--timings] [--yes] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] name
```

## Positional arguments

`name`
: Workflow name in workflow.yml.

## Options

`-h, --help`
: show this help message and exit

`--file PATH`
: Workflow file. Defaults to ./workflow.yml.

`--timings`
: Report Fabric access timings after the workflow.

`--yes`
: Authorise the workflow and all its commands.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

<!-- END GENERATED CLI -->

## Responsibility and selection

`workflow` runs one named, non-empty list under the top-level `workflows` mapping in a YAML file. The default file is `./workflow.yml`; `--file` selects another path.

Each list entry is one Weaver command line. The leading `weaver` is optional and quoted arguments are preserved. Shell operators, expansion, redirection and commands other than Weaver commands are rejected. A workflow cannot contain `session` or another `workflow`.

All entries must resolve to one workspace. The outer workspace options provide a shared default; an entry may name the same workspace but not a different one.

## Execution

Weaver reads and parses every entry, resolves the shared workspace and displays the complete sequence before execution. The commands then run in file order in one Session and share one workflow identifier. Reusable resources required by the sequence are prepared before the first command.

Execution stops at the first command that returns a failure status or raises a Weaver error. Later entries do not run. `--timings` reports Session timings after success or failure.

## Interaction

Without `--yes`, Weaver asks once before running the displayed sequence. Confirming the sequence authorises all entries, including destructive commands, so they do not ask again. Declining an interactive prompt runs nothing.

`--non-interactive` propagates to every entry and prevents input, keypress waits and browser sign-in. It does not authorise the sequence: unattended execution requires both `--non-interactive` and `--yes`.

## Output and exit behaviour

Before execution, output names the workflow file and numbers every command. During execution, each entry is introduced with its position in the sequence. Success reports the number of completed commands; failure identifies the entry where execution stopped.

The command exits `0` when all entries succeed or an operator declines the confirmation. It exits `1` when confirmation is required but unavailable, or when an entry fails. File, YAML, parser and conflicting-workspace errors are command errors.

## Example

```yaml
workflows:
  refresh:
    - build ./parcel-operations --item Warehouse/Operations
    - load Warehouse/Operations
    - test Warehouse/Operations
```

```bash
weaver workflow refresh \
  --workspace-config workspace-development.yml \
  --non-interactive \
  --yes
```
