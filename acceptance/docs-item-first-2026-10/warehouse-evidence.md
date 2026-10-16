# Warehouse journey evidence

## Outcome and scope

Reader path: `warehouse/index.md` → `warehouse/first-project.md` →
`warehouse/tests.md` → `warehouse/incremental.md` →
`warehouse/schema-and-protection.md` → estate tasks where needed.

The first task uses the existing `Parcel.StatusEvent` Table and
`Parcel.CurrentStatus` View verbatim from `examples/parcel-warehouse`. Tests
continue those names and the same three event rows; no second initialisation.
The new `examples/parcel-warehouse-journey` is the necessary combined snapshot for
checking that continuation and its passing/finding/restored checkpoints. It adds
no runtime behaviour. The existing incremental Warehouse fixture is unchanged.

Created four assigned task pages, this evidence file, and the combined fixture
(SQL, configuration, README and offline checker). `warehouse/index.md` needed no
change. Nav, root guidance, Reference, old routes, other examples and tools were
not edited. Old-route compatibility and shared installation remain parent work.

## Two transitions, as published

First → Tests:

> The View now gives you one row per parcel, but a successful Load does not prove that it chose the right event. Testing Warehouse data adds an independent expected result and a check for unknown statuses to this same project, without initialising another one.

Tests → incremental variation:

> These checks now describe the result you expect, but the event feed is still a constant in a SQL file. Loading changes uses a complete mutable-source variation: the same parcels arrive through an external Warehouse, and a keyed Table consumes updates and cancellations without rebuilding its definition.

## Fixture and checkpoint mapping

| Page/checkpoint | Exact fixture files | Locally verified | Reader's expected Fabric result, not observed locally |
| --- | --- | --- | --- |
| First Table/View | `parcel-warehouse-journey/Warehouse/Operations/{Parcel.StatusEvent,Parcel.CurrentStatus}.sql` | Byte-equal to original `parcel-warehouse`; published blocks equal; Check; View → event dependency; generated Table load installer | Three events read/inserted; View returns P-1001/In transit/Central and P-1002/Delivered/South |
| Passing validation | Same files plus `tests/Parcel.CurrentStatusMatches.sql`, `assumptions/Parcel.StatusIsKnown.sql` | Check; two-result Test, one-result Assumption; Test → View, Assumption → event dependency | 0 missing, 0 unexpected; 0 violations; Green Health |
| Deliberate finding | Replace only Test with `failure/Parcel.CurrentStatusMatches.sql` | Check still passes; dependencies unchanged; full published block equal | P-1002/In transit/South missing; P-1002/Delivered/South unexpected; Test non-zero; Tests Red |
| Restored | Restore passing Test | Check; dependencies unchanged | Both validations pass; Health Green |
| Mutable-source variation | Unchanged `parcel-incremental-warehouse`: configuration, Shortcut, CurrentStatus Table, three external source scripts | Published blocks equal; Check; two result queries after setup; empty managed producer edge; generated Table load installer | Initial two rows; data-only change updates P-1001, deletes target P-1002 but retains Cancelled source row; clean no-op advances consumer bookmark |
| Schema/protection | Uses preceding examples; links retained deeper pages | Links/anchors; source tests for metadata, Build protection, reload and wipe representations | No service action requested by this entry page |

The incremental page explicitly changes `CurrentStatus` from a View to a Table,
physical targets from `Operations`/`Catalogue` to
`ParcelOperations`/`ParcelCatalogue`, and source mode from constants to external
`ParcelSource`. It says not to overlay snapshots or retain the fixed expected-row
Test. Shortcut readback occurs after Build and before first Load. Source-only
updates then run Load without Build. Exact existing source scripts and consumer
SQL are preserved.

## Frozen source and actual local commands

Worktree: `/opt/data/scratch/Fors/weaver-docs-refresh/item-first-warehouse`, branch
`docs/item-first-warehouse`. Define the command paths below as:

```bash
PRODUCT=/opt/data/scratch/Fors/weaver-docs-refresh/product
PYTHON=/opt/data/repos/weaverstack/.venv/bin/python
```

The product checkout is at `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`; behaviour is
pinned to `74b4d15ee65ed2740593af1f4d459771b801b132`. From that product checkout:

```bash
git diff --quiet 74b4d15ee65ed2740593af1f4d459771b801b132 HEAD -- src tests pyproject.toml uv.lock
```

Exit 0: selected runtime/test/dependency trees equal the pin. Import verification
returned `/opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py`,
not an installed package from the dependency environment.

From the docs worktree:

```bash
PYTHONPATH="$PRODUCT/src" "$PYTHON" examples/parcel-warehouse-journey/check.py --weaver-checkout "$PRODUCT"
```

Exit 0; output:

```text
Project valid. (five actual Check calls, one per assembled checkpoint)
{'commands': 25, 'configurations': 2, 'authored_sql_blocks': 6, 'sql_program_blocks': 14, 'fixture_block_matches': 12, 'checkpoints': 5}
No service calls or native SQL execution; fixture hashes unchanged.
```

The line grouping Check calls above abbreviates their repeated output, not a
literal CLI line. The checker reports actual production dependency edges:
`CurrentStatus → StatusEvent`, plus `CurrentStatusMatches → CurrentStatus` and
`StatusIsKnown → StatusEvent` after validation additions. Its socket boundaries
reject service calls. All fourteen exact published SQL blocks go through the
product statement/result-query parser, including source setup and readback;
six metadata-bearing blocks also go through the Weaver document parser. Both
Table declarations generate a stored-procedure installer locally.

From the product checkout:

```bash
PYTHONPATH="$PRODUCT/src" "$PYTHON" -m pytest -q tests/test_tsql_program_declaration.py tests/test_incremental_build_install.py tests/targeted/test_runtime_reference_load_cycle.py tests/targeted/test_run_record_representation.py tests/test_warehouse_wipe_sql_representation.py
```

Actual result: **86 passed in 7.80s**.

```bash
PYTHONPATH="$PRODUCT/src" "$PYTHON" -m pytest -q tests/test_validation_repository_declaration.py tests/test_validation_run_representation.py tests/test_declaration_metadata_declaration.py tests/targeted/test_reload_cycle.py
```

Actual result: **217 passed in 2.59s**. These are offline product tests, not this
example's observed Warehouse execution.

From the docs worktree:

```bash
/opt/data/repos/weaverstack/.venv/bin/ruff check examples/parcel-warehouse-journey/check.py
/opt/data/repos/weaverstack/.venv/bin/ruff format --check examples/parcel-warehouse-journey/check.py
git diff --check
```

Final results: `All checks passed!`, `1 file already formatted`, and exit 0.
The initial formatter check failed; formatting was applied and the check rerun.
Exploratory introspection initially used nonexistent `weaver.check` and a
repository `dependencies` field; both were corrected to actual production CLI
Check and `dependency_edges` before final verification. No product change was
made. Generated-load inspection likewise required the declaring logical item;
the committed checker supplies it explicitly.

A local relative-link/heading scan of all five Warehouse pages found **35 links**:
**32 existing**, including linked fragment checks; **3 approved integration
links** not yet present in this worktree (`estate/development-cycle.md` twice,
`estate/recovery.md` once). No unexpected missing target. This is not a rendered
site/link-crawl result.

## Evidence limits and integration work

Weaver's T-SQL parser classifies statements and query result contracts; it does
not validate native Warehouse SQL grammar. No Fabric provisioning, Build, Load,
Test, Health, Shortcut resolution, SQL endpoint access, bookmark readback,
capacity or tenant work ran. All remote outcomes are explicitly expected.
Timestamp-based incremental consumption assumes compatible UTC change times
and retained/visible source change evidence; hard deletes require tombstones or
another retained feed. Those limits remain beside the example.

`Prohibit rebuild` is explicitly a Build replacement guard, not protection from
Load/reload, Wipe or Mirror/reset. External ownership is the stronger boundary.
The deep schema/protection/incremental pages remain substantive searchable
owners; no copied full contract or altered generated Reference blocks.

Full strict site build, browser/mobile/search read-through, complete generated
reference gates, old-route compatibility and incoming product links await parent
integration. The new snapshot's GitHub link targets the existing draft branch;
its remote availability awaits the parent's push. No push, PR operation,
publication or live service acceptance is claimed.
