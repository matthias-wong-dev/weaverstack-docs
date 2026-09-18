# Load behaviour

Load executes installed Table and Folder work from the catalogue. It does not read project source; unbuilt source changes do not affect a run.

## Selection

Logical items may be positional or use the repeatable legacy `--item` option. Naming none selects every item recorded in catalogue installations; an explicitly named uninstalled item is an error. See [Shared selection and identity](shared-selection-and-identity.md) for item and installed-object forms.

Within that item boundary, Load has three selection modes:

- **Item-wide:** with no `--name` or `--stale`, select every installed loadable owned by the items.
- **Stale:** `--stale` selects loadables whose Load assessment is not Green. It uses the same current-state, age and managed-ancestor rules as Health. `--as-of` is a zoned ISO-8601 cutoff, defaults to 24 hours before the run started and is valid only with `--stale`. An empty stale selection succeeds.
- **Named:** repeatable `--name` selects only the named installed loadables inside the item boundary. Area qualification distinguishes Lakehouse Tables and Folders where needed. Names are deduplicated. Named selection adds neither dependencies nor readiness barriers and has no dependency-order edges.

`--name` may be combined with `--stale`; the run is the named objects that are also non-Green, still without graph expansion or dependency ordering. `--reload` and `--stale` are mutually exclusive.

## Planning and ordering

Item-wide and stale runs use the installed dependency graph. Selected upstream work precedes selected downstream work, but dependencies never add an unselected item. Stale planning may cross an omitted Green loadable or View to preserve an ordering relationship between selected nodes without executing the omitted node.

Where an installed cross-engine path requires it, planning inserts SQL-endpoint refresh or OneLake-publication readiness barriers between selected work. Named selection deliberately omits those inferred edges and barriers.

A cycle, unresolved installed dependency, ambiguous physical address, unknown name or unsupported reload selection is rejected during planning. `--reload` accepts Tables only; selecting a Folder rejects the whole request before execution, including in a dry run.

## Dry run

`--dry-run` reads catalogue state, builds the selected graph and resolves each selected primitive and target. It does not dispatch authored work, refresh an endpoint, wait for publication, open a run record, write Log, LoadStatus or LoadStatistic, reset a bookmark, or change a target.

Dry-run nodes are `validated`, `invalid` or `blocked`. The report is `succeeded` only when the plan validates; an empty stale plan also succeeds. Otherwise it is `invalid`. A reload dry run reports reload mode and validates the Table-only restriction without resetting or emptying anything.

## Execution

For a normal item-wide or stale run, ready nodes execute in deterministic topological order. A named run executes its exact nodes without dependency ordering. Table and Folder code applies its installed contract; a Load run does not reparse the source project.

Static means load once for the installed generation. An ordinary run that reaches an already-loaded static object records a static skip and does not call its authored source or advance its bookmark. An established static object is Green regardless of age and is therefore excluded by `--stale`. Reload resets the generation state first, so a selected static Table runs again.

Rows or files that violate the installed key, null or file-key rules are rejects:

- without `--fault-tolerant`, a rejecting primitive refuses before modifying its target and the node fails;
- with `--fault-tolerant`, valid rows or files are published, rejects are retained as evidence, and the node is `succeeded_with_rejects`;
- a declared delete/update stability-threshold breach never modifies the target; fault tolerance changes whether that refusal is raised or returned, not whether the change is applied; and
- an incremental merge that would violate an existing unique key is fatal regardless of fault tolerance and does not modify the target.

The orchestrated CLI exposes no option to waive a declared stability threshold.

## Reload

`--reload` reconstructs each selected Table from zero. Immediately before a reached Table executes, Weaver writes and flushes pending Load state and the initial bookmark boundary, empties the target, then calls the installed load against that reset state.

Reload does not add descendants. A node never reached retains its previous target, bookmark and status. A failed reached reload is not rolled back: its target may be empty or partially reconstructed, its bookmark remains at the initial boundary and its current state records the failure. A later ordinary load starts from that reset boundary; rerun with `--reload` when full reconstruction is still required.

## Outcomes and failure policy

Executed nodes use `succeeded`, `succeeded_with_rejects`, `failed`, `blocked`, `skipped` and `pending`:

- `blocked` means unresolved or unsatisfied upstream work prevented execution;
- `pending` means fail-fast stopped scheduling before otherwise-ready work began; and
- `skipped` records policy or host behaviour such as a static skip.

Without `--fault-tolerant`, the first failed node stops new scheduling. Its dependants are blocked and other unreached ready nodes remain pending. Weaver records the complete planned report and then raises `LoadError` carrying that report.

With `--fault-tolerant`, independent branches continue. A descendant may run after an upstream execution failure has settled and sees whatever state that failure left. An unresolved or invalid upstream still blocks its descendants. Fault tolerance does not turn a failed node or run into success.

The execution report is `succeeded`, `succeeded_with_rejects`, `partially_succeeded` or `failed`. An empty execution succeeds. The CLI exits `0` only for the two successful statuses; failed, partial and invalid dry-run reports exit `1`. Pre-plan catalogue, selection or capability errors have no run report. For an intolerant execution failure, the CLI renders the carried partial report before the error.

## Persistent state and partial effects

Every node in an executed plan, including barriers, blocked and pending nodes, receives one append-only Log row. Each logical loadable receives current LoadStatus; executed primitives also write LoadStatistic. Required catalogue writes are flushed before a completed report is returned or an intolerant failure is raised. A catalogue write failure is an operation failure.

A bookmark advances only when executed work establishes a clean successful boundary. Rejecting, failed, blocked, pending and static-skip outcomes do not advance it. Dry runs write no state.

Load has no operation-wide transaction or rollback. Earlier successful nodes, tolerated valid rows/files, failure evidence and partial target changes remain when later work fails. Rerunning selects from the installed graph and current state again; `--stale` is the state-based catch-up mode.

## Host qualification

Warehouse loads execute over TDS. Lakehouse Spark SQL uses Spark. Python-authored Lakehouse loads executed from a desktop require a configured Fabric Environment in which Weaver can be imported; execution inside an existing Fabric session uses that session. Capability, authentication and transport failures are operation or node failures according to whether a report has been opened.

See [`weaver load`](../cli/load.md), [Health](health.md), [Catalogue schema](../catalogue-schema.md), and [Shared selection and identity](shared-selection-and-identity.md).
