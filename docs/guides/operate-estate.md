# Operate an installed estate

This guide covers the routine inspect, plan, run and inspect loop after Build has installed a Weaver estate. Build, Load and Test retain the meanings defined by [Weaver operations](../core-concepts/weaver-operations.md); this page concentrates on operator checkpoints.

## Prerequisites

- [Install Weaver](../get-started/installation.md) and confirm `weaver --version` works.
- Use a workspace configuration that names the intended workspace and catalogue. Keep that same file on every command in one operating loop.
- Build the logical items at least once. Load and Test select installed work from the catalogue; they do not read project source.
- Have permission to read the catalogue and target items and to run the selected work.

The examples use an installed parcel estate and `workspace-production.yml`:

```yaml
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

Replace these physical names with your own. The command selections remain logical item names.

## 1. Inspect the starting state

Run Health over the installed estate:

```bash
weaver health \
  --workspace-config workspace-production.yml
```

Health reports one estate verdict and separate Load, Tests and Build sections. Green exits `0`; Amber or Red exits `1`. Findings name the affected logical object and the condition to investigate.

By default, Health compares certified objects with physical inventory. Keep that check for routine operation. Use `--no-inventory` only when you deliberately need a catalogue-only read:

```bash
weaver health \
  --workspace-config workspace-production.yml \
  --no-inventory
```

A catalogue-only result does not establish that certified objects still exist in Fabric.

Scope the report when one item is the operating boundary:

```bash
weaver health \
  --item Warehouse/Operations \
  --workspace-config workspace-production.yml
```

Naming no item reports the whole installed estate. Health is read-only: it does not Build, Load or Test anything.

## 2. Preview Load selection

Preview the installed Load work before executing it:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-production.yml \
  --dry-run
```

The plan lists selected work and its validation outcome without running authored work, moving a bookmark or recording a Load run. Confirm that:

- the requested logical items are the intended boundary;
- each expected Table or Folder appears;
- dependency order is plausible;
- no node is `invalid` or `blocked`.

Dependencies order work within the selected items; they do not add an unselected item. A named selection is narrower still and does not add or order dependencies:

```bash
weaver load Warehouse/Operations \
  --name Parcel.Status \
  --workspace-config workspace-production.yml \
  --dry-run
```

Use a named Load only when running exactly that installed object is intentional. [Dependencies](../core-concepts/dependencies.md) explains the difference between item-wide and named selection.

For a routine catch-up, preview only non-Green loadable objects:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --stale \
  --dry-run \
  --workspace-config workspace-production.yml
```

`--stale` uses the same Load-health assessment as Health. By default, a non-static successful load older than 24 hours is stale. To use another threshold, give both commands the same zoned instant:

```bash
weaver health \
  --as-of 2026-09-18T00:00:00+10:00 \
  --workspace-config workspace-production.yml

weaver load Lakehouse/Landing Warehouse/Operations \
  --stale \
  --as-of 2026-09-18T00:00:00+10:00 \
  --dry-run \
  --workspace-config workspace-production.yml
```

`--as-of` is valid on Load only with `--stale`. A stale plan that selects nothing succeeds and changes nothing.

## 3. Run Load and inspect its outcome

Run the selection already reviewed:

```bash
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-production.yml
```

The report shows an outcome for each selected loadable object, row counts where the work supplied them, a summary and a workflow identifier. A successful run exits `0`. Failed, blocked and pending work is visible in a non-zero result; do not treat partial completion as rollback.

The default Load stops scheduling after its first execution failure. Add `--fault-tolerant` only when continuing independent branches—and allowing downstream work to read the state left by a settled upstream failure—is the intended policy. [Fault tolerance](../core-concepts/fault-tolerance.md) defines that boundary.

## 4. Preview and run installed validations

Preview Test selection:

```bash
weaver test Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-production.yml \
  --dry-run
```

Then run the same selection:

```bash
weaver test Lakehouse/Landing Warehouse/Operations \
  --workspace-config workspace-production.yml
```

Test attempts every selected installed Test and Assumption. A failed validation found discrepancies or violations. A validation that could not run is a separate outcome. Either makes the command exit non-zero.

For one known validation and its diagnostic rows:

```bash
weaver test Warehouse/Operations \
  --name Parcel.StatusMatches \
  --workspace-config workspace-production.yml
```

Changing a Test source file does not affect these commands until Build installs the change.

## 5. Confirm the resulting estate

Repeat Health after Load and Test:

```bash
weaver health \
  --workspace-config workspace-production.yml
```

A Green estate has Green Load, Tests and Build sections at the report's freshness threshold. Amber commonly means pending or stale work. Red identifies failed validation, failed load or inconsistent installed state. Use the finding rather than the overall colour to choose the next action.

If source changed during diagnosis, validate it locally and Build the affected items before rerunning Load or Test:

```bash
weaver check
weaver build . \
  --item Warehouse/Operations \
  --workspace-config workspace-production.yml
```

Build has no dry-run option. It installs project source and can leave completed physical work in place if a later action fails. Keep its selection to the logical items that should be reconciled, then inspect Health again. See the [Development cycle](../core-concepts/development-cycle.md) for the edit-and-Build loop.

## Automate the settled loop with a workflow

Use a workflow after its individual selections and failure policy are understood. Create `workflow.yml`:

```yaml
workflows:
  parcel-daily:
    - load Lakehouse/Landing Warehouse/Operations --workspace-config workspace-production.yml
    - test Lakehouse/Landing Warehouse/Operations --workspace-config workspace-production.yml
    - health --workspace-config workspace-production.yml
```

Run it with:

```bash
weaver workflow parcel-daily --file workflow.yml
```

Weaver displays the sequence before running it and uses one Session and one workspace. It stops when a command fails. Commands that completed before the failure remain applied; a workflow is not a transaction.

For unattended execution, use both the interaction policy and explicit workflow authorisation:

```bash
weaver workflow parcel-daily \
  --file workflow.yml \
  --non-interactive \
  --yes
```

`--non-interactive` only prevents input, retry prompts and browser sign-in. It does not authorise anything. `--yes` authorises the displayed workflow and its commands; it does not select an estate, make failures successful or change operation semantics.

## Inspect the catalogue when the report is not enough

Use Health first. Query the catalogue's `_` schema read-only when you need the installed record behind a finding:

| Question | Catalogue table |
| --- | --- |
| Which physical target is bound to this logical item? | `_.Installation` |
| Which object and source generation did Build certify? | `_.Registry` |
| What dependencies and Shortcuts were installed? | `_.Dependency`, `_.Shortcut` |
| Is this object still borrowed from a mirrored estate? | `_.Mirror` |
| What is its current Load or Test result? | `_.LoadStatus`, `_.TestStatus` |
| What settled work belongs to the reported workflow? | `_.Log` |
| What rows moved in a completed Load? | `_.LoadStatistic` |

Do not edit catalogue rows. The [Catalogue](../core-concepts/catalogue.md) defines each table and its state boundary.

For automation, commands that expose `--json` emit one JSON document on stdout:

```bash
weaver health \
  --workspace-config workspace-production.yml \
  --json
```

Health's JSON includes a format version, overall status, sections and findings. Build, Load and Test also expose `--json`, but their fields are command-specific; do not infer one command's schema from another. Consult the [CLI reference](../reference/cli.md) and [Contracts](../contracts/index.md) before binding automation to an output contract.

Local checks and dry runs establish parsing and selection only. Build, Load, Test, inventory Health and catalogue queries produce live Fabric evidence only when run against the intended workspace.