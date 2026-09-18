# Run and inspect an estate

After Build installs an estate, use Health to choose the work, run Load and Test, then use Health again to verify the resulting state.

Run these commands from the directory containing the intended `workspace-config.yml`.

## 1. Inspect the starting state

```bash
weaver health
```

Health is read-only. It reports Load, Tests and Build state as Green, Amber or Red and names findings that need attention. By default it also compares installed claims with physical inventory.

Use the findings to decide whether the estate needs data work, validation or Build recovery. Health does not read unbuilt source or run Load or Test for you.

## 2. Run installed data work

For the normal item-wide run:

```bash
weaver load
```

Load reads installed definitions and bindings from the catalogue. It does not read edited project source; run Build first when source has changed.

For routine catch-up after Build or when Health reports pending or stale load work, narrow the run to non-Green loadable objects:

```bash
weaver load --stale
```

`--stale` uses the same Load-health assessment as Health. It preserves dependency ordering among selected item-wide work but does not pull Green upstream work into the run. An empty stale selection succeeds without changing the estate.

A Load can leave partial state when work fails. Completed work is not rolled back. Use its per-object outcomes and then follow [Recover failed work](recover-failed-work.md).

## 3. Run installed validations

```bash
weaver test
```

Test runs the installed Tests and Assumptions. A failed validation found data discrepancies or violations; a validation that could not run is an execution problem. Edited validation source takes effect only after Build installs it.

## 4. Inspect the resulting state

```bash
weaver health
```

Green means the assessed Load, Tests and Build subjects have no current finding. Amber identifies work that is pending, stale or otherwise needs attention without a current failure. Red identifies a recorded failure or inconsistent installed state. Act on the finding rather than the overall colour alone.

Use [Troubleshooting](troubleshooting.md) when the final report is not Green. Exact selection, freshness, inventory controls, named execution and machine-readable output belong in [Operation behaviour](../reference/operation-behaviour/index.md) and the [CLI reference](../reference/cli.md).
