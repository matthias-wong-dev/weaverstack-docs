# State and health

Build, Load and Test leave different kinds of evidence in the Weaver catalogue. Health reads that evidence to answer one question: what condition is the installed estate in now?

Health does not read unbuilt project source, execute data work or run validations. It is a view of installed and operational state, optionally checked against the physical objects in Fabric.

## Three views of the estate

A Health report separates three concerns:

- **Load** — whether each installed Table or Folder has settled for its installed generation and remains fresh enough to use.
- **Tests** — whether each installed Test and Assumption has run against the data it now depends on.
- **Build** — whether the catalogue's installed claims are internally consistent and, when inventory is read, agree with the physical estate.

The distinction matters because each concern has a different recovery path. A Table can be installed correctly but need loading. Its data can be current while a Test has not run. A recent successful Load does not repair an inconsistent installation.

## Green, Amber and Red

Each section, and the report as a whole, is classified as **Green**, **Amber** or **Red**. The overall status is the worst section status.

**Green** means the assessed subjects have no current finding. Loads have settled and are fresh, validations have passed since their dependencies last changed, and the installed catalogue is consistent with the evidence Health inspected.

**Amber** means the estate needs work but does not currently record a failure for that subject. Common examples are a Table that has not loaded since Build, a load that completed with rejected rows, data older than the chosen freshness point, or a Test whose inputs changed after it passed.

**Red** means the current state records a failure or contradiction. A failed, errored or blocked Load or validation is Red. So is Build state that claims an installation which cannot be resolved or, when inventory is enabled, cannot be found in the expected physical form.

## Stale is not failed

A stale object may have completed successfully before becoming out of date. Age can make a Load stale, but dependency order can do so as well: when an upstream object is established after its consumer, the consumer is stale even if both last ran successfully.

Tests use the same idea without an age threshold. A passing Test becomes stale when managed data it reads is established later. It needs to run again; the earlier result did not become a failed result.

A failure says that attempted work did not succeed. Staleness says that previously established state no longer describes the current dependency generation. This is why Amber and Red lead to different diagnoses and often different reruns.

## Build consistency is installed consistency

Build health checks the estate recorded in the catalogue. It can expose missing certifications, unresolved installed dependencies, ambiguous physical claims and certified objects absent from inventory.

It does not compare that estate with files edited since the last Build. An unbuilt source change is outside Health's view; Build first to make that generation part of the installed estate.

## Health is a read

Health leaves the estate unchanged. Its result is assembled from installed declarations, current Load and Test state, dependency relationships and optional physical inventory. In a mixed mirrored estate, borrowed objects take their current Load state from the source catalogue while local objects use destination state.

Selection narrows what Health reports, but freshness still follows managed ancestors needed to judge those subjects. The result is therefore a current estate view rather than a replay of one command or workflow. A partially updated estate can contain state established by several earlier runs.

Use the [Health operation reference](../reference/operation-behaviour/health.md) for exact selection, freshness, inventory, result and exit behaviour. The [Catalogue](catalogue.md) explains where the underlying current state and history are recorded.
