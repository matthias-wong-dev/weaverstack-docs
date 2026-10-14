# Workflows and controlled deployment

Reuse one Session while you develop a command sequence, then record the accepted sequence as a workflow. When installation needs a reviewed handoff, plan a destination-specific bundle instead of asking the installer to reopen and reinterpret source.

Continue with your working project and configuration. The examples below use the [managed-source Parcel checkpoint](../semantic-models/managed-sources.md) and its `workspace-dev.yml`: Operations Delivery, the Parcel model and its linked Report. Direct entrants use that complete snapshot; do not combine it with the independent Landing or StatusEvent examples by renaming documents.

## Open one Session

```bash
weaver session --workspace-config workspace-dev.yml --timings
```

At the `weaver>` prompt, run the normal installed-project sequence:

```text
weaver> check .
weaver> build . --item Warehouse/Operations
weaver> build . --item PowerBI/Parcel --bind-data-sources
weaver> load
weaver> test
weaver> health
weaver> exit
```

Source-data and model/Report Build calls remain separate. Reports deploy after their model and have no Load/Test step. Each command uses the ordinary parser and selection rules; the leading `weaver` is optional at the prompt.

The Session belongs to one physical workspace and reuses healthy capabilities it has acquired, such as item resolution, Warehouse connections, OneLake access and Spark context. Unneeded capabilities are not started. A failed command returns to the prompt; completed work remains applied. `--timings` reports Fabric access timings on exit, not a new Load execution mode.

## Turn the accepted sequence into a workflow

Create `workflow.yml` beside the project:

```yaml
workflows:
  verify:
    - check .
    - build . --item Warehouse/Operations
    - build . --item PowerBI/Parcel --bind-data-sources
    - load
    - test
    - health
```

```bash
weaver workflow verify --workspace-config workspace-dev.yml --timings
```

Weaver parses the entries, resolves one workspace, displays the numbered sequence and asks once for confirmation. Review and confirm if correct; decline if not. Commands run in file order through one Session. Load/Test outcomes share a workflow identifier for catalogue correlation.

An execution error stops later entries. Test/Health findings are collected while later commands continue, then make the completed workflow unsuccessful. Completed work is not rolled back. A workflow is an ordered list of Weaver commands, not a shell or a transaction. [Session and workflow concepts](../core-concepts/sessions-and-workflows.md) and [Workflow behaviour](../reference/operation-behaviour/workflow.md) own context reuse and exact continuation rules.

For unattended execution, provide credentials and authorise the settled sequence explicitly:

```bash
weaver workflow verify --workspace-config workspace-dev.yml --yes --non-interactive
```

`--yes` authorises the workflow and entries. `--non-interactive` separately disables input, keypress waits and browser sign-in. Desktop authentication can use a configured service principal or an existing Azure CLI sign-in; the selected identity still needs permissions for every capability. Store secret material in the runner’s secret store, not the project or bundle. Piped `y` is not authorisation when stdin is not a terminal. [Automation and execution contexts](../advanced/automation-and-execution-contexts.md) explains credential selection, host boundaries and machine output.

## Keep the lifecycle in Fabric when that is the execution host

A Fabric notebook can call `weaver.build()`, `weaver.load()`, `weaver.test()` and `weaver.health()` using its attached workspace, runtime and identity. The source-data catalogue remains explicit; discovering the workspace does not invent one. Explicit Session construction is optional for context reuse, not a prerequisite for an ordinary attached-notebook call.

[Portable execution between desktop and Fabric](../advanced/portable-execution-between-desktop-and-fabric.md) provides a separate complete Landing/Operations snapshot, notebook Resources layout and native installed execution examples. That variation contains Landing Event/CurrentStatus and Warehouse StatusEvent/View; it is not this Parcel model fixture. It also shows Fabric Git’s Resources support: `fabric notebook push` transports a notebook definition, not local Resources.

The host still supplies the required capabilities. Desktop Lakehouse Build/Load/Test needs the matching published Weaver runtime; the attached-notebook path uses its active Spark session. [Running Python in Fabric](../lakehouse/runtime.md) owns publication. A local Check or preview does not establish runtime admission. Fabric scheduling, capacity, identity and retries remain host responsibilities, not properties inferred from a successful interactive command.

## Hand off frozen installation work

Use a bundle when the installer should execute reviewed work without reopening the project:

```text
Check source → plan bundle for destination → review and transfer → Install → Load → Test → Health
```

`build --bundle-only` reads the intended destination catalogue and inventory, then freezes targets, ordered actions, generated payloads and integrity hashes. It needs destination access despite not installing. It cannot be combined with `--dry-run`, and neither mode provisions missing Power BI targets as an ordinary first Build can.

Generate a separate bundle for each destination. Changing a configuration does not retarget a retained bundle. Transfer its complete manifest and payload tree without editing them; credentials are not included. Install validates the representation and checksums, then executes frozen actions without rereading source, recalculating impact or substituting targets from another configuration. If source, bindings or relevant destination state changed, plan a new bundle.

A failed installation stops later sequences but does not undo completed physical changes. After installation, operate the destination’s installed definitions with Load, Test and Health. [Build bundles and controlled installation](../advanced/build-bundles-and-controlled-installation.md) explains the handoff; [`build`](../reference/cli/build.md), [`install`](../reference/cli/install.md) and the [bundle format](../reference/build-bundle-format.md) own exact syntax and representation.

For machine consumers, use each command’s advertised structured output and process status together, retaining diagnostics separately. There is no universal JSON envelope or promised long-term compatibility for unversioned output. [Machine-readable output](../reference/machine-readable-output.md) records the command-specific boundary.
