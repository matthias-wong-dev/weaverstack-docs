# Build behaviour

Build turns one snapshot of project source into a deployment bundle and, unless `--bundle-only` is set, installs that bundle.

## Inputs and selection

`SOURCE` is a project directory. It defaults to the current directory on a desktop and to the process working tree exposed as Notebook Resources inside a Fabric session. An `abfss` source is accepted only inside a Fabric session.

Repeatable `--item ITEM[=TARGET]` selects logical items and may supply or override each physical binding. Naming no item selects every target in workspace configuration; an empty selection is an error. See [Shared selection and identity](shared-selection-and-identity.md) for the accepted forms and item boundary.

Build copies the complete source directory to a temporary snapshot before parsing. Later edits to, removal of, or additions under the original directory do not change that Build. The snapshot is removed after success or failure.

## Validation, preflight and planning

Before installation, Build:

1. parses and validates the complete project snapshot, including identities, dependencies and cycles;
2. validates the selected items and bindings;
3. on a desktop, verifies the workspace, catalogue, Environment when named, and all selected physical targets in one Fabric inventory read before opening Spark; this REST preflight is skipped inside a Fabric session;
4. reads the installed catalogue and selected physical inventories; and
5. compares source, installed certification and physical state to prepare a bundle.

Source validation reads the whole project, but selected items are the reconciliation boundary. Dependencies do not add an unselected item. Within the boundary, planning classifies new and changed work, selected existing descendants affected by a change, protected work, and installed work removed from source. Producers precede consumers; removal uses the reverse dependency boundary. Cross-item impact reaches a consumer only when both items are selected.

Installed signatures are equality tokens, not public content digests. Build also checks physical presence and form: a matching signature does not make a missing or differently typed object unchanged. Uncertified physical objects are not adopted merely because their names match. `Prohibit rebuild` retains an existing protected data object when replacement would otherwise be required; it does not prevent first installation.

## Bundle-only mode

Every Build prepares a self-contained deployment bundle before installation. The bundle contains the frozen plan and payloads, not project source.

`--bundle-only` writes the bundle and stops before installation. It still validates source and reads the destination catalogue and inventories because the plan is destination-state-specific. `--bundle-path` is valid only with `--bundle-only` and must name a new or empty directory; without it, Weaver creates a temporary-directory path and returns that path. Build has no `--dry-run` mode: bundle-only mode writes a bundle but changes no installed objects or catalogue state.

`weaver install` accepts a local bundle directory or `.weaver.zip` archive. It validates the plan and payload checksums before any action, then executes that frozen plan without reopening source or replanning against destination state. Bundle representation and identity are current formats, not compatibility guarantees; see [Build bundle format](../build-bundle-format.md).

## Installation barriers and certification

Installation executes plan sequences in order. Actions in a batch run serially. If an action fails, the remaining actions already in that batch still receive their actual results; later batches in that sequence and every later sequence are `skipped`. Every planned action therefore ends as `succeeded`, `failed` or `skipped`.

Runtime-state reconciliation occurs before physical rebuild work. A selected loadable being rebuilt is set to pending and its bookmark is reset to the initial boundary; a selected Test or Assumption is set to pending. Removed declarations lose their current-state rows. Operational history in Log and LoadStatistic is retained, and unchanged or unselected objects keep their current state. A failed later action does not restore an earlier reset.

Physical work and runtime artefacts precede catalogue publication. Dictionaries and item bindings are published before Registry certification, and Registry is a final barrier. Physical work can therefore exist without matching certification if a later publication action fails; Build health reports that inconsistency. A Lakehouse SQL-endpoint refresh that the current host cannot perform is recorded as `skipped` and does not by itself fail installation.

A report status is `succeeded` when no action failed, including a plan containing supported host skips, and `failed` otherwise. Installation writes `install-report.yml` beside the bundle plan; a direct Build also returns that report, although its internal temporary bundle is removed.

## Failures, partial state and reruns

Source, request, desktop preflight, state-read and bundle-validation errors stop before installation and produce no installation report. During installation, failures are captured in the report; the CLI renders the result and exits `1`. A successful or bundle-only Build exits `0`.

Build has no operation-wide transaction or rollback. Runtime-state resets, removals, physical changes and catalogue writes completed before a later failure remain. Rerunning Build takes a new source snapshot and replans from the catalogue and physical state that remain; an unchanged settled rerun selects no physical or catalogue work.

Build may remove obsolete Weaver-certified objects and catalogue claims inside selected items. It does not reconcile or remove state outside that boundary.

See [`weaver build`](../cli/build.md), [`weaver install`](../cli/install.md), [Catalogue schema](../catalogue-schema.md), and [Shared selection and identity](shared-selection-and-identity.md).
