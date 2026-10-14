# Run and inspect an estate

Use the same configuration and operations across the managed estate. Health brings Lakehouse and Warehouse state together with registered model refreshes and validations; Load and Test operate that work without a second set of model-specific procedures.

Continue from a successful item Build using its existing configuration; no fresh setup or rerun is needed to inspect state. Direct entrants can use the complete [Warehouse checkpoint](../warehouse/tests.md) or [managed-source model checkpoint](../semantic-models/managed-sources.md). The latter contains Operations Delivery and the Parcel model, not the first Warehouse StatusEvent/View pair. Run these commands from the directory containing the intended `workspace-config.yml`; if you kept a named file such as `workspace-dev.yml`, add `--workspace-config workspace-dev.yml` to each command.

## 1. Inspect the starting state

```bash
weaver health
```

Without an item selector, Health covers the whole installed estate. It is read-only and reports Load, Tests and Build state as Green, Amber or Red, naming findings that need attention. By default it also compares installed claims with physical inventory.

Use the findings to decide whether the estate needs data work, validation or Build recovery. Health does not read unbuilt source or run Load or Test for you.

For changed definitions, [Check, preview and Build](development-cycle.md) before this installed-state sequence. Source-data and model/Report definitions require separate Build calls. Reports participate in Build only; they have no independent Load or Test.

## 2. Run installed data work

For the normal item-wide run:

```bash
weaver load
```

Load selects the installed Table and Folder work and registered semantic-model refreshes. Managed dependencies order selected source work before model refreshes. Reports use the model’s data rather than having their own Load. Load reads installed definitions and bindings from the catalogue. It does not read edited project source; run Build first when source has changed.

For routine catch-up after Build or when Health reports pending or stale load work, narrow the run to non-Green loadable objects:

```bash
weaver load --stale
```

`--stale` uses the same Load-health assessment as Health. It preserves dependency ordering among selected item-wide work but does not pull Green upstream work into the run. An empty stale selection succeeds without changing the estate.

A Load can leave partial state when work fails. Completed work is not rolled back. Use its per-object outcomes and then follow [Recover failed work](recovery.md).

## 3. Run installed validations

```bash
weaver test
```

Test runs the installed Tests and Assumptions across Lakehouse Python/Spark SQL, Warehouse SQL and semantic-model DAX. A model-owned Test can compare its measure with SQL calculated independently from the source. A failed validation found data discrepancies or violations; a validation that could not run is an execution problem. In catalogue mode, edited validation source takes effect after Build installs it. Source/file mode reads authored validations and records no catalogue status/history.

## 4. Inspect the resulting state

```bash
weaver health
```

Green means the assessed Load, Tests and Build subjects have no current finding. Amber identifies work that is pending, stale or otherwise needs attention without a current failure. Red identifies a recorded failure or inconsistent installed state. Act on the finding rather than the overall colour alone.

For a complete source-and-model example, follow [Connect a semantic model to source data](../semantic-models/managed-sources.md).

Use [Troubleshooting](../basics/troubleshooting.md) when the final report is not Green. If an item-wide run is broader than the intended work, [run part of an estate](selective-runs.md). To cap simultaneous scheduled work for one invocation, [control concurrency](concurrency.md). Both are optional controls, not prerequisites for normal operation. See [Operation behaviour](../reference/operation-behaviour/index.md) and the [CLI reference](../reference/cli.md) for selection, freshness, inventory controls, named execution and machine-readable output.
