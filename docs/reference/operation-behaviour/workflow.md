# Workflow contract

A Workflow is a named sequence of Weaver CLI commands. It composes existing commands in one Session and workspace; it does not introduce a second operation language or a transaction around the sequence.

## Workflow file

The default file is `./workflow.yml`. `--file PATH` selects another YAML file. The document must contain a top-level `workflows` mapping, and the requested name must map to a non-empty list of strings:

```yaml
workflows:
  refresh:
    - build ./parcel --item Warehouse/Operations
    - load Warehouse/Operations
    - test Warehouse/Operations
```

Each string is one ordinary Weaver command line. A leading `weaver` is optional, and quoted arguments are preserved:

```yaml
workflows:
  refresh:
    - weaver build . --workspace-config "parcel development.yml"
```

Every entry is parsed by the normal Weaver command parser before anything runs. An invalid command or option fails the Workflow before its first entry.

A Workflow is not a shell. Pipes, redirection, command substitution, environment expansion, command chaining and non-Weaver programs are rejected. `session` is excluded because the Workflow already owns a Session, and `workflow` is excluded so Workflows cannot nest.

## Shared workspace and Session

Every entry runs in one Session and one Fabric workspace. Outer `--workspace`, `--workspace-config`, `--catalogue` and `--environment` values provide defaults inherited by entries that do not set them. An entry may resolve to the same workspace configuration, but entries cannot select different workspaces.

If the caller supplies an open Session, the Workflow joins it and leaves it open. Otherwise the Workflow opens one Session for the complete sequence. Entries share one workflow identifier, which correlates catalogue evidence produced by Load and Test.

The Workflow prepares the union of capabilities and known Lakehouse attachments required by its entries before running the first command. This reuse does not alter the individual operation contracts or permit an entry to move to another workspace.

## Validation, display and confirmation

Weaver loads the named sequence, parses every entry and resolves the shared workspace before displaying or executing it. It displays the workflow file and the complete numbered sequence.

Without `--yes`, an interactive invocation asks once whether to execute that displayed sequence. Declining runs nothing and is not an execution failure. If confirmation is required but no prompt is available, the Workflow fails and names `--yes` as the required action.

Confirmation authorises the complete displayed sequence, including destructive entries, so individual commands do not ask again. `--non-interactive` is inherited by every entry and can only make interaction stricter; it prevents input, keypress waits and browser sign-in but does not imply approval. Unattended execution therefore requires `--non-interactive --yes`.

## Ordered execution and failure

Entries run in file order with their ordinary parsed arguments. The Workflow stops at the first entry that returns a failure status or raises a Weaver error. The failing entry is reported, and later entries do not run.

A Workflow is not transactional. State changed by completed entries, and partial state left by the failing entry under that operation's own contract, remains in place. Weaver does not roll earlier Build, Load, Test, Mirror or Wipe effects back when a later entry fails. Recovery is the recovery procedure for the operation that failed, followed by rerunning an appropriate sequence.

Each entry retains its own selection, dry-run, fault-tolerance, strictness, confirmation and result semantics. Workflow composition changes only Session reuse, shared workspace resolution, one-time confirmation, correlation and stop-on-first-failure behaviour.

## Outcome

A Workflow succeeds only when every entry succeeds. It reports the number of completed commands. On failure it identifies the first unsuccessful entry and returns a non-zero status. `--timings` reports Session timings after either success or failure.

A user who declines an available confirmation receives a zero status because no execution was attempted. Missing non-interactive authorisation is a failure and returns non-zero.

## Defined behaviour

The Workflow contract specifies that Workflow:

1. reads one named, non-empty sequence from the selected YAML file;
2. accepts ordinary Weaver command lines and rejects shell language and nested sessions or Workflows;
3. parses every entry and resolves one shared workspace before execution;
4. runs entries in file order through one supplied or managed Session;
5. applies outer interaction and workspace values as inherited defaults without allowing a workspace change;
6. displays and confirms the complete sequence once;
7. stops at the first failed status or Weaver error; and
8. leaves completed and partial operation state in place rather than rolling the sequence back.

See [`weaver workflow`](../cli/workflow.md), [Session and workspace helpers](../python/session.md), and the contracts for each command placed in the sequence.