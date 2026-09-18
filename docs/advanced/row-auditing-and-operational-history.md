# History contract

The catalogue separates current state from append-only operational history. Current state answers what is true for the installed generation now. History answers what settled during earlier and current workflows.

## Current state

`_.Bookmark`, `_.LoadStatus` and `_.TestStatus` contain the current row for a logical object.

- `_.Bookmark` is the next incremental boundary for a loadable object.
- `_.LoadStatus` is the latest Load outcome and timing for a Table, Folder or View lifecycle state.
- `_.TestStatus` is the latest installed Test or Assumption outcome, timing and available failure count.

A later settled attempt replaces the object's current status by key. It does not append another current-state row. A partial run updates only objects it reaches, so the estate's current Load state can be composed from several workflow identifiers.

A Build that replaces a loadable object resets its Bookmark and Load status for the new installed generation. Rebuilding a validation resets its Test status. Unaffected current rows remain unchanged.

## Append-only records

`_.Log` and `_.LoadStatistic` are history.

`_.Log` receives one row for each settled unit of installed Load or Test work, including failures and blocked work. It records the workflow, task, logical object where one exists, physical target, result, times, message and available detail.

`_.LoadStatistic` receives one row when Load work executed. It records the workflow and logical object, timing, row counts, reload mode and static-skip marker. A blocked node has Log and current Load status but no statistic because no data work ran. A static skip is executed lifecycle work and is distinguished from a clean read that moved zero rows.

History is append-only through supported operations. Direct catalogue updates or deletes are not a retention interface.

## Workflow correlation

Each orchestrated Load or installed Test run has a workflow identifier. Commands inside one workflow share its identifier, so Log and status rows from the commands that ran can be correlated. A standalone object load or validation also receives a workflow identifier for its own recorded unit.

Current status stores the workflow that most recently settled that object. It is not necessarily the workflow most recently started for the estate. After partial work, filtering Log by one workflow reconstructs that attempt, while reading current statuses reconstructs the present estate from every workflow that last touched an object.

Load statistics correlate to a Load execution by workflow identifier and logical object identity together. Health uses that boundary when presenting activity behind current Load state. It does not read an arbitrary recent prefix of accumulated statistics.

A direct source-file Test has no installed workflow evidence: it neither updates Test status nor appends installed-estate history.

## Retention boundary

Weaver appends operational history but does not define a time-based retention duration, automatic compaction policy or public pruning operation for `_.Log` and `_.LoadStatistic`. This contract therefore does not promise indefinite physical retention outside operations that preserve these tables, nor does it authorise manual deletion.

Use read-only queries for historical reporting. If external retention or export is required, treat it as management of copied data rather than mutation of the Weaver catalogue.

## Rebuild boundary

Build reconciliation does not erase `_.Log` or `_.LoadStatistic`. Rebuilding a Table, Folder, Test or Assumption resets only the applicable current state for that installed generation. Historical records remain evidence of what happened to earlier generations.

An unchanged Build changes neither current state nor history. Item-scoped Build leaves current state and history for unselected items outside its boundary.

## Mirror boundary

Mirror copies installed declaration state and current state into the destination catalogue. It does not copy source `_.Log` or `_.LoadStatistic` rows. The destination rebuild creates those history tables empty, while source history remains in the source catalogue.

Mirror is destructive at the destination: it empties and rebuilds the destination catalogue. Consequently, history that existed only in the previous destination catalogue is not preserved by the mirror. This is not deletion from the source and not a transfer of source history.

After the mirror, new destination Load and Test work appends destination history. Work on objects still borrowed remains recorded where that work executes. Health can combine current borrowed Load state and matching source statistics for reporting, but it does not copy those rows into destination history.

## Publication and failure

A Load or installed Test does not report successful completion until its required catalogue writes have been flushed. If work completes but its record cannot be made durable, the operation reports a recording failure rather than claiming a fully recorded success.

History records settled units, not every planning, authentication, configuration or preflight message. Preserve command output for failures that happen before a node settles or before catalogue recording is available.

## Defined behaviour

The History contract specifies that Weaver:

1. keeps one current Bookmark, Load status and Test status per applicable logical object;
2. appends Log evidence for settled installed work and Load statistics only for executed Load work;
3. correlates current and historical evidence by workflow and logical identity;
4. permits present estate state to span several workflows after partial runs;
5. preserves history when Build resets current state for a rebuilt generation;
6. copies current and installed state, but not source history, during Mirror;
7. replaces rather than preserves previous destination history when Mirror rebuilds the destination catalogue; and
8. defines no automatic history-retention or pruning promise beyond these operation boundaries.
