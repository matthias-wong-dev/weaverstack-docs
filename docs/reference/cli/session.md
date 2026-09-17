# `weaver session`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver session [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] [--catalogue CATALOGUE] [--timings]
```

## Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

`--catalogue CATALOGUE`
: Where the Weaver catalogue lives, for example Warehouse/Weaver.

`--timings`
: Report Fabric access timings when the session ends.

<!-- END GENERATED CLI -->

## Responsibility and selection

`session` opens a command prompt backed by one persistent Session. It accepts lifecycle commands with normal CLI syntax; the leading `weaver` is optional. `help` or `?` prints command help, and `exit` or `quit` closes the prompt.

An explicit workspace or a discovered `workspace-config.yml` fixes the Session's workspace. Commands may override its catalogue or Environment, but cannot switch to another workspace. Without a default workspace, each command must supply its own.

Fabric management, project initialisation and another `session` cannot run inside the prompt. Other accepted commands use the same parser as standalone invocations.

## Execution

Commands run in order and reuse the Session and any prepared connections. A pasted multiline block ignores blank lines and lines beginning with `#`. Its first failed command stops the rest of that block; the prompt remains open for the next command.

`Ctrl-C` while editing abandons the current input. Interrupting or failing a command also leaves the prompt open. `--timings` reports accumulated Fabric access timings when the Session closes.

## Interaction

This is an interactive command. Individual commands retain their own confirmation rules, including the distinction between `--non-interactive` and `--yes`.

## Output and exit behaviour

The banner names the default workspace, if one was resolved, and lists the lifecycle commands available at the prompt. Command output is unchanged. Command errors are written to stderr without closing the Session.

`exit`, `quit` and end-of-file close the Session with status `0`. A failed command does not become the process exit status because the prompt continues.

## Example

```console
$ weaver session --workspace-config workspace-development.yml --timings
weaver> build ./parcel-operations
weaver> load Warehouse/Operations
weaver> test Warehouse/Operations
weaver> exit
```
