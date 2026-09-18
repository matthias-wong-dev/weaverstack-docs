# Row auditing and operational history

Weaver records state at three different levels:

- managed columns describe the current lifecycle state of each stored row;
- current catalogue tables describe the latest state of an installed object; and
- history tables record settled Load and Test work across workflows.

These surfaces answer different questions. Row audit columns do not replace operation history, and the latest Load status is not a list of every earlier Load.

## Row audit columns describe current rows

Weaver adds three managed audit timestamps to Tables: when a row was inserted, when it was last updated and its delete-lifecycle value. A live row carries a non-null maximum-date sentinel in the delete field. These columns are outside the authored business schema and cannot be used as authored business columns.

For a Python Table, `dataframe()` returns business columns by default. Pass `row_audit_columns=True` to append the three audit columns:

```python
current = Parcel__CurrentStatus(self).dataframe(row_audit_columns=True)
```

The result still describes rows currently held by the Table. It is not an append-only record of every prior value or of rows that have already been physically removed. Use upstream history, a deliberately modelled history Table or Change Data Feed when the application needs business-row version history.

The row signature used for keyed comparisons is also managed, but it is never returned by `dataframe()`. [Schemas, keys and managed columns](schemas-keys-and-managed-columns.md) explains that boundary.

## Bookmarks are current cursor state

`_.Bookmark` contains the current incremental boundary for each loadable object. The boundary is the UTC instant immediately before its latest clean Load began. An object with no clean Load for its installed generation uses the initial boundary so incremental code asks for all available history.

A clean Load advances the bookmark, including an incremental no-op. A failure, rejected-row result, blocked or pending node, or static skip does not. The row is current state: a later clean Load replaces the boundary for that logical object rather than appending another bookmark.

A Table and Folder with the same `Schema.Object` name remain distinct because their installed identities include the Lakehouse area.

## Load and Test status answer “what is true now?”

`_.LoadStatus` holds the latest recorded Load state for each managed Table, Folder or View. `_.TestStatus` holds the latest recorded outcome for each installed Test or Assumption. A later settled attempt replaces that object's current row.

A partial run updates only the objects it reaches. Current estate state can therefore contain rows produced by several workflow identifiers. Read these tables, or Health, when the question is whether the installed estate is pending, current, failed, rejected, blocked or stale now.

A direct source-file validation does not create installed Test history. Installed Test and Assumption execution is the boundary that updates `_.TestStatus` and appends operational evidence.

## `_.Log` and `_.LoadStatistic` answer “what happened?”

`_.Log` receives evidence for settled units of installed Load or Test work, including unsuccessful, blocked and pending outcomes recorded for an executed plan. It is the broad history surface for reconstructing a run.

`_.LoadStatistic` records Load activity such as read, inserted, updated, deleted and rejected row counts, plus reload and static-skip distinctions. It exists only when Load work executed. A blocked node can therefore have a Log row and current Load status but no Load statistic; recording a row of zeroes would incorrectly imply that data work ran and moved nothing.

These tables are append-oriented history. The public operations do not expose time-based retention, compaction or manual pruning. Query them read-only and copy them elsewhere if another retention policy is required.

## Correlate a run by workflow and object

Each orchestrated Load or installed Test run receives a workflow identifier. Commands composed in one Weaver workflow share that identifier. Standalone object execution also receives an identifier for its recorded unit.

Use the workflow identifier to gather the Log rows from one attempt. For Load statistics, combine it with logical object identity: a partial run may leave another object's current status pointing to an older workflow, and several objects can have statistics under the same workflow.

This distinction is useful when Health shows a mixed current state:

```text
workflow A settled Parcel.StatusFiles
workflow B later settled Parcel.CurrentStatus
current estate = latest row for each object
history for workflow A = only work recorded under A
```

Health reads current status and the matching statistics behind that status. It does not present an arbitrary recent slice of all accumulated history.

## Rebuild resets current state, not history

Build starts a new current-state incarnation for work it rebuilds:

- rebuilding a loadable object resets its bookmark and current Load state;
- rebuilding a Test or Assumption resets its current Test state; and
- unaffected objects retain their current rows.

`_.Log` and `_.LoadStatistic` remain as evidence of earlier generations. An unchanged Build changes neither current state nor history. An item-scoped Build leaves unselected items outside the reset boundary.

Reload is a different boundary. For each selected Table that execution reaches, Reload resets its bookmark and Load status before emptying and rereading the target. If that execution fails, the earlier bookmark and contents are not restored.

## Mirror starts destination history at the boundary

Mirror copies installed declaration state and current operational state into the destination catalogue. It does not copy the source estate's `_.Log` or `_.LoadStatistic` rows. The destination history tables begin empty and record only later work performed there.

Mirror reconstructs the destination catalogue, so history that existed only in the previous destination catalogue is not preserved through that reset. Source history remains in the source catalogue.

Borrowed data keeps its Load ownership at the source. Health can use source current state and the matching source statistics when assessing borrowed objects, but those rows are not copied into destination history. Once an object is materialised locally, later local Load and Test work records destination state and history.

Use [Catalogue schema](../reference/catalogue-schema.md) for exact tables, columns, keys and stored values. [Load behaviour](../reference/operation-behaviour/load.md), [Test behaviour](../reference/operation-behaviour/test.md) and [Mirror behaviour](../reference/operation-behaviour/mirror.md) define their publication and reset boundaries.
