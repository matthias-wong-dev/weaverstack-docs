# Compose commands with Sessions and workflows

Use a Session while diagnosing or iterating on several commands at a terminal. Put the accepted sequence in a workflow when the same ordered lifecycle should run as one named unit.

## Prerequisites

- [Install Weaver](../get-started/installation.md) and confirm `weaver --version` works.
- Use an existing project and workspace configuration, or copy the checked `examples/parcel-automation/` fixture from this documentation repository.
- Authenticate for the selected Fabric workspace. The fixture uses a Warehouse-only project, so its lifecycle does not require Spark or a published Fabric Environment.

The examples below start in the fixture directory:

```bash
cd examples/parcel-automation
weaver check .
```

A successful check proves that the local project parses. It does not prove a Fabric outcome.

## Iterate in one interactive Session

Open a Session with the workspace configuration:

```bash
weaver session --workspace-config workspace-config.yml --timings
```

At the `weaver>` prompt, run ordinary CLI command lines:

```text
weaver> weaver build . --item Warehouse/Operations
weaver> weaver load Warehouse/Operations
weaver> weaver test Warehouse/Operations
weaver> weaver health --item Warehouse/Operations
weaver> exit
```

The leading `weaver` is optional at the prompt. Quoting and options use the ordinary CLI parser; the Session does not define a second command language.

All commands use one Session and inherit its workspace unless a command supplies a compatible override. One Session cannot switch to another Fabric workspace. Credentials and acquired Fabric execution resources remain available to later commands and are released when the Session exits. The Session starts only the capabilities an operation needs.

A command failure returns to the prompt. Correct the source or command and try the next operation in the same Session. This is different from workflow failure: an interactive Session survives a failed command, while a workflow stops its sequence. `weaver session` is interactive by definition and does not accept `--non-interactive`.

## Author the accepted sequence

Create `workflow.yml` at the project root:

```yaml
workflows:
  verify:
    - weaver check .
    - weaver build . --item Warehouse/Operations --workspace-config workspace-config.yml
    - weaver load Warehouse/Operations --workspace-config workspace-config.yml
    - weaver test Warehouse/Operations --workspace-config workspace-config.yml
    - weaver health --item Warehouse/Operations --workspace-config workspace-config.yml
```

This is the complete checked fixture file. Each entry is one Weaver command line. A workflow is not a shell script: pipes, redirections, command substitution, environment expansion and command chaining are refused. A workflow cannot contain `session` or another `workflow`. Exact file grammar and command options belong in [CLI reference](../reference/cli.md) and [Contracts](../contracts/index.md).

The file order is execution order. Here, Check validates source before Build installs it; Load runs the installed work; Test evaluates the resulting data; Health reads the recorded and physical state. [Weaver operations](../core-concepts/weaver-operations.md) explains these boundaries.

## Review and run interactively

Run the named workflow:

```bash
weaver workflow verify --file workflow.yml --timings
```

Weaver parses every entry before the first one runs, resolves the workflow workspace, then displays a numbered sequence and asks once for confirmation. After confirmation, each command runs in the same Session. The sequence has one workflow identifier, which correlates its recorded Load and Test outcomes in the [Catalogue](../core-concepts/catalogue.md).

Observable checkpoints are:

1. the displayed sequence matches the file;
2. Build reports a successful installation;
3. Load and Test report no failed work;
4. Health reports Green;
5. the command exits zero.

Declining the confirmation cancels the sequence without running it and is not an execution failure.

## Run the workflow unattended

Use both policy options when no operator is present:

```bash
weaver workflow verify \
  --file workflow.yml \
  --non-interactive \
  --yes
```

`--non-interactive` prevents prompts, retries and browser sign-in. It does not grant destructive authorisation. `--yes` authorises the displayed workflow and each nested command; it does not configure unattended interaction or authentication. Without `--yes`, a non-interactive workflow refuses before its first entry. The outer non-interactive policy propagates to every nested command.

## Understand the failure boundary

A workflow stops at the first command that returns failure or raises a Weaver error. It does not retry that command, run later entries or roll back commands that completed. Fault-tolerance options on an individual Load affect work inside that Load only; an unsuccessful final Load result still stops the workflow. See [Fault tolerance](../core-concepts/fault-tolerance.md).

If a command fails:

1. note the number in `Workflow stopped at [N]`;
2. inspect that operation's output and current Health or catalogue state;
3. correct the project, configuration, credentials or Fabric condition;
4. rerun the workflow as a new attempt.

Use the interactive Session first when diagnosis needs several attempts. Use [Run Weaver unattended](automation.md) for runner authentication, logs and machine-readable command output. Use [Promote a bundle](promote-a-bundle.md) when Build planning and installation must happen in separate processes. The [Development cycle](../core-concepts/development-cycle.md) describes how the same logical project moves through a development estate.
