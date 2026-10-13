# Scale measurement record

Exact pre-revision measurements and provenance retained for claim checks. Public pages use rounded, workload-specific results approved by Matthias.

## Historical benchmark: PR #193

The following measurements were reported in [PR #193](https://github.com/matthias-wong-dev/weaverstack/pull/193), whose head was `39dd32dc4bff4998f3e4a5a98d96d3079477e029`. They are **historical results, not a fresh run of this documentation release**.

A synthetic F64 estate used one Lakehouse and two Warehouses. Its 3,000 declared data objects comprised 2,144 tables, 816 views and 40 folders, with 30 business columns. It ran 24 Spark lanes and 12 lanes per Warehouse. Nine convergence Tests passed after first Load and each changed day.

| Operation | Seconds | Time | Work |
| --- | ---: | --- | --- |
| Build from empty | 828 | 13m 48s | 5,372 actions |
| First Load | 3680 | 61m 20s | 2,185 nodes; approximately 4.05B rows inserted across the estate |
| Unchanged Build | 77 | 1m 17s | No actions |
| Unchanged Load | 477 | 7m 57s | 2,185 nodes; no changed rows |
| Day 1 Load | 1165 | 19m 25s | Approximately 5.75M inserted, 2.03M updated, 40,910 deleted |
| Day 2 Load | 785 | 13m 05s | Approximately 5.70M inserted, 1.98M updated, 44,563 deleted |
| Day 3 Load | 776 | 12m 56s | Approximately 5.66M inserted, 1.86M updated, 33,105 deleted |

Rows inserted across several layers are not distinct source records. Declared objects, scheduled Load nodes and physical Build actions are different measures. The dependency fan-in includes declared waits without the corresponding join workload, so this does not establish a runtime for an arbitrary warehouse with the same row count. It is not a semantic-model or Report-rendering benchmark.

### Two observations from that investigation

Targeted endpoint refresh reduced that component of the initial Build from **9m 41s to 1m 49s** and of the unchanged Load from **6m 41s to 19s**. These are component timings, not the whole operation.

The same 60-node probe within one Spark application on F64 measured:

| Spark lanes | Seconds |
| ---: | ---: |
| 4 | 208 |
| 8 | 140 |
| 16 | 85 |
| 24 | 60 |

These settings are not defaults, maximum supported concurrency or universal capacity recommendations. Earlier whole-workload comparisons also changed width and incremental design; do not read them as a controlled speedup. Simulated scheduler results are not in the measured-results table.

Later [PR #218](https://github.com/matthias-wong-dev/weaverstack/pull/218) exercised 3,000 objects at `--scale 0.01`. That separate reduced-volume qualification does not carry the #193 4.05B volume or these timings. Separate 1,000-declaration guardrails are not this benchmark either. Exact run timestamp and raw-log identifiers are not supplied by this table.

For reproduction, consult the source revision's stress-generator and run instructions and the cited PR. A full-scale run needs a separately authorised disposable estate and appropriate capacity; it is not a getting-started requirement.
