# Work in Sessions and workflows

Open a Session when several commands will run against one Fabric workspace. Once the sequence is accepted, record it as a workflow and run it as one named unit.

## Open one Session

From a project directory containing `workspace-config.yml`, run:

```bash
weaver session --timings
```

At the `weaver>` prompt, run the normal lifecycle:

```text
weaver> build .
weaver> load
weaver> test
weaver> health
weaver> exit
```

The leading `weaver` is optional at the prompt. Each line uses the ordinary CLI parser and keeps its ordinary operation behaviour.

The commands share the Session's workspace and can reuse capabilities already acquired there, including authentication, item resolution, Warehouse connections, OneLake access and Spark context. The Session acquires only what the commands need and releases what it opened on exit. `--timings` reports Fabric access timings when the Session ends.

A failed command returns to the prompt. Correct the cause, inspect Health and rerun the appropriate command without opening another Session. A Session does not combine the commands into a transaction or change their selections.

## Turn the accepted sequence into a workflow

Create `workflow.yml` in the project directory:

```yaml
workflows:
  verify:
    - check .
    - build .
    - load
    - test
    - health
```

A workflow is an ordered list of ordinary Weaver commands. It is not a shell or a second execution language. Each entry retains its normal selection, effects and failure behaviour. Exact YAML grammar and allowed command forms are in [Workflow configuration](../reference/configuration-files/workflow.md).

Run the sequence:

```bash
weaver workflow verify --timings
```

Weaver parses the entries, resolves one workspace, displays the numbered sequence and asks once for confirmation. The entries then run in file order through one Session. Load and Test outcomes from the sequence share a workflow identifier for catalogue correlation.

The workflow stops at the first failed command. Later entries do not run, and completed work is not rolled back. Diagnose the failed operation and rerun an appropriate sequence against the state that remains; a workflow is not a transaction.

For unattended execution, authorise the sequence explicitly and disable all interactive input:

```bash
weaver workflow full --yes --non-interactive
```

`--yes` authorises the displayed workflow and all its entries. `--non-interactive` also prevents prompts, keypress waits and browser sign-in, so the configured unattended credentials must be sufficient. Piping `y` into `weaver workflow full` is not confirmation: when stdin is not a real terminal, Weaver refuses to run unless `--yes` is present.

For unattended policy, authentication and exact confirmation behaviour, see [Workflow operation behaviour](../reference/operation-behaviour/workflow.md) and [Automation and execution contexts](../advanced/automation-and-execution-contexts.md).
