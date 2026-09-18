# Workflow behaviour

A Workflow is an ordered list of ordinary Weaver CLI command lines executed through one Session. It is not a shell, a second operation language or a transaction.

## Discovery and YAML shape

`weaver workflow NAME` reads `./workflow.yml` relative to the process working directory. `--file PATH` selects another file; Weaver does not search parent directories or alternate filenames.

The YAML document must be a top-level mapping containing `workflows`. `workflows` must map names to non-empty lists, and every entry in the selected list must be a non-empty string.

```yaml
workflows:
  refresh:
    - build . --item Warehouse/Operations
    - load Warehouse/Operations
    - test Warehouse/Operations
```

A missing file, malformed YAML, missing or non-mapping `workflows`, unknown name, empty sequence, non-string entry or empty entry fails before execution.

## Command parsing

Each entry is tokenised as one command line and parsed by the ordinary Weaver parser. A leading `weaver` is optional. Shell quoting is honoured, but shell operators, redirection, environment expansion, command substitution and chaining are rejected. Non-Weaver programs fail parser validation.

`session` and `workflow` entries are forbidden: a Workflow already owns its Session, and Workflows cannot nest.

Every entry is parsed before the sequence is displayed, confirmed or run. One invalid command or option therefore prevents the first command from running.

## One workspace and one Session

Outer `--workspace`, `--workspace-config`, `--catalogue` and `--environment` values form the Workflow's default workspace context. If neither the outer command nor an entry names one, normal workspace discovery may use `workspace-config.yml` in the working directory. An entry's ordinary explicit values still apply within that context.

All explicitly resolved entry configurations must equal the Workflow's resolved `Workspace`. If more than one distinct configuration is named, the Workflow fails before execution. One Workflow cannot switch Fabric workspace.

A caller-supplied open Session is reused and left open. Otherwise the Workflow creates one Session and closes it after the sequence. Before the first command it may prepare the union of declared capabilities and known physical Lakehouse attachments for all entries. Preparation changes acquisition timing only; each command retains its own selection and capability requirements.

All executed entries share one workflow identifier for Load and Test catalogue evidence.

## Confirmation

After parsing and workspace resolution, the CLI displays the selected file and complete numbered sequence.

Without `--yes`, an interactive run asks once about that sequence. Declining runs nothing and returns success because execution was cancelled by an answered prompt. If no prompt is available, missing `--yes` is an error and returns failure.

The one Workflow confirmation sets authorisation for every entry, including Mirror and Wipe, so nested commands do not prompt again. Outer `--non-interactive` propagates to every entry and can only make an entry stricter; it disables input, keypress waits and browser sign-in but does not imply authorisation. Unattended execution therefore needs `--non-interactive --yes` when those policies are required.

## Execution and failure

Entries run in file order with their ordinary parsed arguments. The Workflow stops at the first handler that returns a non-zero status or raises a Weaver error. It reports that entry and does not run later entries. A successful Workflow reports the number of completed commands; `--timings` reports Session timings after success or failure.

Each command keeps its own selection, dry-run, fault-tolerance, strictness, publication and result semantics. A Workflow does not retry failed work. State changed by completed commands and partial state left by the failing command remain. There is no Workflow rollback; recovery follows the failed operation's behaviour and starts a new command or Workflow against the remaining state.
