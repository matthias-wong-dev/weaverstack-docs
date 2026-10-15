# Catalogue and Health

What happened after the last run? Read Health to find the data work, validation or installation that needs attention. The catalogue keeps installed definitions and operation results together, so a source Table, its model refresh and a DAX validation can be judged against the same dependency history.

Continue the [mapped Landing/Operations project](environments.md#bind-the-project-to-fabric), using the same `workspace-development.yml`. Keep its installed state; inspecting it does not require another Load or Test:

```bash
weaver health --workspace-config workspace-development.yml
```

If you added models and Reports through [the estate mapping](environments.md#a-model-and-report-variation), keep the same `workspace-development.yml`; their installed refresh and validation results appear in this Health report. For a different working project, use its own configuration consistently. No return to the Warehouse starter is required.

Without an item selector, Health covers the whole managed installed estate. It reads recorded state and, by default, compares installed claims with physical inventory. It does not read unbuilt source, load data or execute validations.

## Find the work that needs attention

Health separates three questions:

| Section | What to look for | Usual next action |
| --- | --- | --- |
| Load | Installed Tables/Folders or registered model refreshes that are pending, stale, rejected, failed or blocked | Correct the condition, then Load the intended work |
| Tests | Installed Tests and Assumptions that have not passed against their current inputs | Correct data or validation, then Test again |
| Build | Installed claims that are inconsistent or absent in the inspected physical form | Inspect bindings and installation, then reconcile with Build |

Green means the assessed subjects have no current finding. Amber identifies work that needs attention without a current failure, such as an unrun Table, rejected input or stale Test. Red identifies a recorded failure or inconsistent installation. The overall colour is the worst section colour; act on its named findings, not on colour alone.

A successful model refresh can later become stale because its source was loaded afterward. A passing DAX Test becomes stale when the model it reads changes. Reports have installation/model-dependency claims, but no independent data refresh or Test health. Health is not a Report rendering check.

Age and dependency freshness are different. `load --stale` uses Load-health assessment to select non-Green work; it does not select every Green prerequisite. The optional freshness cutoff is documented in [Health behaviour](../reference/operation-behaviour/health.md). [State and health](../core-concepts/state-and-health.md) explains stale versus failed state and installed Build consistency.

## Follow a finding into the catalogue

The configured catalogue Warehouse exposes queryable state in the `_` schema. These records answer different questions:

| Question | Inspect |
| --- | --- |
| Which physical targets hold the installed logical items? | `_.Installation` |
| Which objects did Build certify, and what did it declare? | `_.Registry`, the schema/Table/Folder/column/key dictionaries, `_.Dependency` and `_.Shortcut` |
| What model source, measure, relationship or DAX validation was installed? | `_.SemanticModel`, its Table/Column/Measure/Relationship records and `_.SemanticModelTest` |
| What is the current Load or validation outcome? | `_.LoadStatus`, `_.TestStatus` |
| Where does the next incremental read begin? | `_.Bookmark`, the consuming object’s latest clean processing boundary |
| What happened during earlier work? | `_.Log` and `_.LoadStatistic`, correlated with the operation’s workflow identifier |
| Which objects still borrow source-owned data after Mirror? | `_.Mirror`, when borrowed state exists |

Use read-only queries against the catalogue’s SQL endpoint when the report is not enough:

```sql
select * from [_].[Installation];
select * from [_].[LoadStatus];
select * from [_].[TestStatus];
```

Interpret current status separately from history. A blocked Load can have a current status without a row-movement statistic because no data work ran. Build establishes fresh current state for changed installed objects; earlier history remains. Do not edit catalogue rows by hand: use the operations that reconcile definitions, bindings and results together.

The [catalogue tour](../core-concepts/catalogue.md) groups every table by the question it answers. The [Catalogue schema reference](../reference/catalogue-schema.md) owns exact columns, keys and stored values. The catalogue records resolved managed lineage, not every external connection.

Catalogue-free Power BI deployment/refresh and source/file-mode Test return reports without persisted Weaver status/history. They are separate supported modes, not another installed estate for this Health command. In an optional mixed mirrored estate, borrowed data’s current Load state comes from its source catalogue while local work uses the destination.

When the findings match the intended starting state, use [the development cycle](development-cycle.md) for the next source change. If an installed operation failed, [recover that work](recovery.md) instead of rebuilding or resetting everything.
