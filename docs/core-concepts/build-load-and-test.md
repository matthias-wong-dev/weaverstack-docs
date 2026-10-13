# Build, Load and Test

Build deploys definitions, Load performs data work or model refresh, and Test evaluates validations. Catalogue-backed operations record state for Health; standalone Power BI operations return their result without creating that catalogue.

```text
project source
    ↓ Build
installed definitions and work
    ↓ Load
data + current load state
    ↓ Test
current validation state
    ↓ Health
estate assessment
```

The separation is operationally important: source is not installed state, installed work is not the data it produces, and validation results are not the act of loading data.

## Build interprets authored source

Build is the operation that reads Weaver documents. It combines the selected source with workspace configuration, determines the required installation work and applies it to the bound Fabric items.

A catalogue-backed Build records the resulting installed generation. Power BI Build deploys native models and linked Reports, verifying their definitions/bindings; a DAX measure probe during deployment is not a substitute for an authored validation. Different source document kinds contribute different things:

- Tables and Folders contribute stored targets and loadable work;
- Views contribute query-defined relations installed during Build;
- Tests and Assumptions contribute validations for a later Test operation;
- Shortcuts contribute installed connections;
- Warehouse programmables and schema metadata contribute definitions with no separate Load step.

Editing source does not update an installed definition. Build is the point at which an edit becomes part of the operating estate.

## Load runs installed data work

Catalogue-backed Load reads installed items and bindings. It also refreshes registered semantic models in the supported graph. Without a catalogue, Load refreshes explicitly named deployed models using configuration, with no installed-graph name/stale/reload/recursive selection. It runs loadable Tables and Folders in dependency order where applicable, changes their data and records current state and history.

Load does not reopen project source. If a Table document changed after the last Build, Load still runs the previously installed work until another Build succeeds.

Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata do not have their own Load step. They may still supply structure or data used by loadable work. Reports have definitions, not a Load or Test target; refresh and validate their model.

## Test runs installed validations

Test reads the catalogue and executes the installed Tests and Assumptions in its selection.

- A Test compares expected and actual rows.
- An Assumption counts rows that contradict its condition.

Test records each validation's current outcome. It reads estate data but does not install definitions or materialise business data. In catalogue mode, an edited validation takes effect after Build installs it. File mode selects authored validations using `--file` (or runs without a catalogue) and records nothing. `--source` chooses the project folder; it does not by itself force file mode when a catalogue is configured.

## Health reads state

Health assesses installed declarations, current Load and Test state and, by default, physical inventory. It reports Build, Load and Tests as Green, Amber or Red and explains findings that affect that assessment.

Health is not another materialising stage. It runs no authored load or validation code and does not change the installed generation.

## Each operation has its own boundary

Build selects project items and resolves their configured physical targets. Load and Test select from the installed estate and use the bindings recorded by Build. Catalogue-free operations use their documented configuration/source rules instead. Dependencies can determine affected work and execution order, but selection remains an operation-specific boundary. Build source items first, then Power BI items in a separate call; one workflow can contain both steps.

## Sessions and workflows { #a-workflow-composes-ordinary-operations }

A workflow runs ordinary Weaver commands in order through one Session. Each operation keeps its normal boundary and state changes; the sequence is not a transaction.

See [Operation behaviour](../reference/operation-behaviour/index.md) for exact selection, ordering, state changes and failure behaviour. [Sessions and workflows](sessions-and-workflows.md) explains the shared execution context.
