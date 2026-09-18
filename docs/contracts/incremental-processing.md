# Incremental-processing contract

Incremental processing reconciles one installed Table or Folder against a boundary recorded in the catalogue. The authored declaration decides whether the source is a complete replacement or an incremental change set. Load does not infer incremental intent from the amount of data returned.

## Bookmark boundary

A bookmark is the timezone-aware UTC instant immediately before an object's latest clean load began. A newly built or reset loadable object has the sentinel boundary, which asks an incremental source for its complete available history.

The boundary is captured before authored `read()` work starts. It advances only after a clean successful load, including a successful incremental no-op that returns `None`. It does not advance after:

- a failed or errored load;
- a blocked or pending node;
- a load that completed with rejected input; or
- a static skip that consumed no source window.

Bookmarks are keyed by logical item, Lakehouse area where applicable, schema and object. A Table and Folder with the same `Schema.Object` therefore have distinct boundaries.

Rebuilding a loadable object resets its current bookmark and Load status for the new installed generation. Unchanged objects keep their boundaries.

## Keyed Table updates and deletes

An incremental Table has a declared primary key. Its staging rows are a partial change set:

- a key absent from the target is inserted;
- a key already present is updated when its comparison values changed;
- a target key absent from staging is retained; and
- a delete occurs only when the authored result explicitly claims that primary key.

`read()` may return staging alone or `(staging, deletes)`. The delete value is a relation containing the declared primary-key columns. `(None, deletes)` is a deletion-only load. `None` or `(None, None)` is a successful no-op for an incremental Table.

A non-incremental keyed Table treats staging as the complete source. Target rows absent from staging are deleted, and the authored method must not return a separate delete claim. An unkeyed Table replaces its contents wholesale. Returning `None` for a non-incremental Table is invalid because an empty complete source must be represented as an empty staging relation.

Incoming rows that violate recoverable key or nullability checks can be rejected under the selected fault-tolerance policy. A proposed incremental merge that would leave a declared unique key duplicated is a fatal target-validity failure under either policy.

## Folder publication and history

A Folder publishes files matching its declared managed scope. An incremental Folder adds or replaces staged files and deletes only explicitly named files. A non-incremental Folder treats staging as the complete managed snapshot and retires managed files omitted from it. Files outside the declared managed scope are not removed by replacement.

After a Folder changes, Weaver writes a change document recording inserted, updated and deleted relative paths. Byte-identical staged files are not recorded as updates. Change history is the evidence used by:

- `files_since(bookmark)` — current files whose latest recorded event after the boundary is an insert or update;
- `deleted_since(bookmark)` — paths whose latest recorded event after the boundary is a delete; and
- `latest_files()` — surviving files from the newest recorded change that left files in place.

The boundary is strict: an event at the bookmark instant is excluded. A later event for the same path supersedes an earlier event in the requested window. Returned change times are UTC, and a naive bookmark is invalid.

Physical files without a change document are not historical events. Before an ordinary non-static Folder's first authored read, Weaver records existing destination files once when no Folder history exists, so retained files enter subsequent history. Existing history suppresses that adoption. The change-history directory is Weaver metadata rather than managed Folder content.

An incremental Folder may return `None` for a no-op or `(None, deletes)` for deletion-only work. A non-incremental Folder must return its issued staging folder. Folders do not support reload.

## Stability thresholds

A keyed Table can declare delete and update percentage thresholds and a minimum target-row count at which they apply. Defaults are 5% deletes, 20% updates and 1,000,000 target rows.

The gate is evaluated after the proposed insert, update and delete sets are settled but before the target is mutated. It does not apply to wholesale replacement, an empty target or a target smaller than the minimum. A change breaches only when its percentage is strictly greater than the declared limit.

A breach leaves the target unchanged through that reconciliation path and records failure evidence. Fault tolerance does not make the proposed change acceptable. The public Python Table load can explicitly waive the stability gate for that invocation; the waiver does not alter the installed declaration.

## Stale selection

`load --stale`, or `stale=True`, narrows the selected item boundary to loadable objects whose Load health is not Green. This includes pending, failed, errored, blocked, rejected and stale objects. It uses the same freshness assessment and zoned `as_of` cutoff as Health.

Stale selection does not include borrowed objects as destination work, does not select Views and does not widen into unselected items. A local descendant can be selected because a borrowed ancestor advanced. A plan with no non-Green local work succeeds without mutation.

`as_of` is valid on Load only with stale selection. Stale and reload modes cannot be combined.

## Reload and commit boundaries

Reload applies only to selected Tables. For each Table as the run reaches it, Weaver:

1. writes and durably flushes Pending Load status and the sentinel bookmark;
2. empties the target while preserving the installed Table definition;
3. calls the ordinary authored load against the empty target and reset boundary; and
4. records the resulting Load status, statistic and clean bookmark where applicable.

The reset occurs per reached node, not across the whole plan. A fail-fast run does not reset a later node it never reaches. Reload does not add descendants or reset unselected Tables. Selecting a Folder makes the reload request invalid before execution.

If execution fails after reset or emptying, the old bookmark and target contents are not restored. The Table remains in the state established by the reset and partial execution evidence. A later reload is a new reconstruction attempt.

Ordinary successful Table and Folder loads publish target changes before their clean bookmark is committed. Catalogue recording is part of completion: an operation does not report clean success before its required state writes are durable. There is no operation-wide transaction across several selected objects.

## Defined behaviour

The Incremental-processing contract specifies that Weaver:

1. uses the instant before a clean load starts as that object's next incremental boundary;
2. advances a bookmark only for a clean success, including a no-op;
3. applies keyed incremental inserts and updates from staging and deletes only from explicit primary-key claims;
4. treats non-incremental staging as complete source state;
5. records Folder insert, update and delete history and queries it with a strict boundary;
6. selects stale work from the same assessment as Health without widening item scope;
7. evaluates stability before target mutation and keeps it independent of fault tolerance; and
8. resets and flushes each reached Table before reload empties and rereads it, without rollback.
