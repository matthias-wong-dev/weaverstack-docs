# Health behaviour

Health reads installed operational state. It does not read project source, execute authored Build, Load or Test work, publish certification, or change the estate.

A Health invocation reads catalogue tables, matching current Load statistics, optional mirrored Load state and optional physical inventories at several points during the invocation. The report is not an atomic snapshot across those sources. `generated_at` is when the operation began; rerunning performs new reads and may produce a different result.

## Selection and evidence

Repeatable `--item ITEM` selects installed logical items. Naming none selects every physical target bound by catalogue installations. A named item without an installation is a command error. Health has no object, file or physical-target selector; see [Shared selection and identity](shared-selection-and-identity.md).

Selection bounds reported subjects and inventory reads. Managed ancestry outside the selection is still read when deciding whether a selected Load or validation is behind its sources.

Health reads:

- catalogue installations, Registry certification, Table, Folder and Test dictionaries, dependencies, Shortcuts and mirror records;
- current LoadStatus and TestStatus;
- only LoadStatistic rows matching the workflow and logical identity in current LoadStatus; and
- by default, physical inventory for selected targets.

Older Log and LoadStatistic rows remain history but are not the current Health activity window. A partial run may leave current objects correlated with different workflows; blocked work can have current status without a LoadStatistic row.

For borrowed objects, current Load state and matching statistics come from the configured source catalogue. The destination catalogue still supplies topology, validation and Build evidence. If borrowed objects exist but the source catalogue is absent or names another workspace, Health fails rather than using copied state as current.

## Inventory and host boundaries

With inventory enabled, Warehouse objects are read over TDS and Lakehouse storage objects through OneLake. Health does not start Spark or Livy and accepts no Environment option. Lakehouse Views are not reported missing merely because storage inventory cannot enumerate them.

`--no-inventory` skips physical reads. Build health can then report catalogue contradictions but cannot establish that certified objects are physically present. Authentication, catalogue, mirror-source and inventory-read failures are command errors; Health does not turn them into Red findings.

## Status aggregation

The severity order is **Green**, **Amber**, **Red**. A section with no findings is Green. Each section is its worst finding, and the overall report is its worst section.

### Load

Installed Tables and Folders are Load subjects. Views and generated runtime artefacts are not, although a View's Build-established time can affect descendants.

- **Green:** the current installed generation settled successfully, is not older than `as_of`, and is not behind a managed ancestor.
- **Amber:** no load has settled since Build; the latest result contains tolerated rejects or another non-failure state; the last clean completion is older than `as_of`; or a managed ancestor has no settled current generation or was established later.
- **Red:** the current result is failed, errored or blocked.

After a static object has established its load-once state, its own age and ancestor-freshness checks are exempt. Its latest lifecycle touch can still affect descendant freshness. A static object that has never loaded is Amber.

### Tests

Installed Tests and Assumptions are Tests subjects.

- **Green:** the latest installed execution passed and no managed data dependency was established later.
- **Amber:** the validation has not run since Build, has another non-failure current state, or passed before a managed dependency was established again.
- **Red:** the latest execution failed, errored or was blocked.

Elapsed time alone does not make a validation Amber. Test findings may carry missing and unexpected counts; Assumption findings may carry a violation count.

### Build

Build health checks installed-state consistency, not unbuilt project source. Red findings include:

- a declared Table or Folder without matching Registry certification;
- a validation declaration without its installed executable;
- an unresolved installed dependency;
- more than one logical installation claiming one physical address; and
- when inventory is enabled, a certified object absent from its expected local or borrowed physical form.

Build has no Amber classification in the current assessment: contradictions above are Red and no finding is Green.

## `as_of` and dependency freshness

`--as-of` is the oldest acceptable settled Load completion time. It accepts an ISO-8601 instant with a time zone, normalises it to UTC and defaults to 24 hours before Health began. A naive or invalid instant is a command error.

The cutoff applies to Load age only. It does not replace dependency freshness: a recent load can be Amber when an ancestor is unestablished or newer, and a validation can be Amber after a dependency moves regardless of `as_of`.

## Report and exit behaviour

The report contains Load, Tests and Build sections, subject and outcome counts, non-Green findings, selected targets, `generated_at`, `as_of`, current Load workflow/timing summary and matching Load activity where available. A finding includes a condition code and may include logical identity, physical target, runtime outcome, workflow, times and failure count.

The Python operation returns `HealthReport`; `is_healthy` is true only for Green. The CLI exits `0` only for Green. Amber, Red and command errors exit `1`. Human output conveys status without requiring terminal colour.

`--json` emits the current report mapping with an explicit `format_version`. The source does not promise that field set, ordering or format-version compatibility remains unchanged; consumers must not infer a broader stability guarantee from the current representation.

Health never writes current state or history. It reports partial state left by other operations; rerunning Health only rereads that state and does not repair, retry or roll it back.

See [`weaver health`](../cli/health.md), [Load](load.md), [Test](test.md), [State and health](../../core-concepts/state-and-health.md), and [Catalogue schema](../catalogue-schema.md).
