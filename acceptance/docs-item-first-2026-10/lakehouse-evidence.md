# Lakehouse author evidence

## Scope and reader path

This records local authoring observations, not the parent's editorial/service acceptance transitions.

`lakehouse/index.md` → `lakehouse/python.md` → `lakehouse/spark-sql.md` → `lakehouse/tests.md` → `lakehouse/incremental.md`. Shortcuts and runtime are contextual branches at `lakehouse/shortcuts.md` and `lakehouse/runtime.md`. Runtime publication first appears immediately before the first hosted Build. Shared configuration, dependencies, state and recovery point to the route map's final `estate/` destinations.

The first three tasks keep one project: `Lakehouse/Landing`, Folder `Parcel.Events`, Python Table `Parcel.Event`, then Spark SQL Table `Parcel.CurrentStatus`. The SQL page adds CurrentStatus; it neither replaces the Python Event nor provisions another project. The validation page contains complete runnable Spark SQL Test and Assumption documents, not just Reference links. Direct entry uses the earlier task's setup plus the existing fixture's explicit checkpoint list.

## Two transition paragraphs

Python → Spark SQL, verbatim from `docs/lakehouse/python.md`:

> You now have the event history in a Table. [Add a Spark SQL CurrentStatus Table](../../docs/lakehouse/spark-sql.md) to answer the next question: where is each parcel now? Keep the Python Event and its Folder; the next page adds one transformation to this project.

Spark SQL → validation, verbatim from `docs/lakehouse/spark-sql.md`:

> A successful Load tells you the query ran. It does not establish that the latest-event rule selected the right rows. [Test these same Tables](../../docs/lakehouse/tests.md) against an independent expected result and reject unknown event statuses.

## Fixture/checkpoint mapping

| Checkpoint | Fixture documents | Continuing reader action |
|---|---|---|
| Python | `examples/parcel-lakehouse/Lakehouse/Landing/Files/Parcel__Events.py`, `Tables/Parcel__Event.py` | Initialise once; add the Folder and Python Table; Check; publish matching Environment; Build/Load |
| Spark SQL | Above plus `Tables/Parcel.CurrentStatus.sql` | Add this one Table; Check/Build/Load in the same project |
| Validation | Above plus `tests/Parcel.CurrentStatusMatches.sql`, `assumptions/Parcel.EventStatusIsKnown.sql` | Compare independent expected statuses with CurrentStatus; check Event statuses; Build/Test; optional source-file mode records no catalogue state |
| Deliberate finding | Change only P-1001's expected Test status to Delivered | Check/Build/Test; no Load; restore and rerun; expected remote outcomes are not claimed observed |
| Mutable-source variation | Existing `examples/parcel-incremental` unchanged: Tracking physical StatusSource Shortcut → snapshot StatusFiles Folder → incremental CurrentStatus | Explicit complete external-source variation in a separate project, not a silent continuation of Landing's constant |
| Data-only second Load | Same Tracking definitions; update external P-1001.csv and remove P-1002.csv | No Build; Folder records update/delete; Table uses its own bookmark and explicit key deletes; third clean no-op advances the consumer bookmark |
| Optional existing-data access | Physical Shortcut block reused from parcel-incremental, added to Landing | Check/Build/read back mounted destination; no Shortcut Load; source availability not established by Check |
| Optional logical extension | Dispatch Shortcut View → `Lakehouse/Landing/Tables/Parcel.Event` | Parser resolves the same Python Event; complete cross-item execution belongs to Estate |

The existing independent `Parcel.ServiceLevel.sql` in parcel-lakehouse is unchanged and explicitly excluded from the required journey checkpoints. No new fixture project was generated. Only CurrentStatus, its two validations and a checkpoint README were added to the existing Lakehouse fixture.

Twelve fixture blocks are synchronised with published code: Python Folder/Table; CurrentStatus; Test/Assumption; Tracking configuration, physical Shortcut, snapshot Folder, incremental Table and two CSV uploads; optional Landing physical Shortcut declaration. The Tracking Folder's `source_root.is_dir()` guard remains before staging, so unavailable source differs from a deliberately empty snapshot. `files_since(self.bookmark())` and `deleted_since(self.bookmark())` remain consumer-specific; source omission is translated to an explicit Table deletion claim.

## Frozen source and behaviour evidence

- Behaviour pin: `74b4d15ee65ed2740593af1f4d459771b801b132`.
- Frozen checkout: `/opt/data/scratch/Fors/weaver-docs-refresh/product`, HEAD `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`; `git diff --exit-code 74b4d15ee65ed2740593af1f4d459771b801b132 HEAD -- src tests` returned 0 with no differences.
- Product Python: `/opt/data/repos/weaverstack/.venv/bin/python`, always with `PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src`.
- Import confirmation: `weaver.__file__` is `/opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py`.
- Source seams reviewed: `weaver/objects.py` bookmark/change helpers and clean bookmark recording; `declaration/validation.py`, `declaration/spark_sql_module.py`, `runtime/spark_sql_validation.py`; declaration/model/graph source for actual parser graph assertions. Existing Test/Assumption/Table/Folder/Shortcut and runtime references own exact contracts.
- Source tests exercised: `tests/targeted/test_spark_sql_validation_representation.py`, `tests/targeted/test_validation_artefacts_representation.py`, `tests/test_folder_change_feed_cycle.py`. These are core/offline tests, not service acceptance.

## Exact local checks and results

All commands below were actually executed. No Fabric operation, credential acquisition, capacity/tenant change, release, push or GitHub operation was performed.

From the isolated docs worktree:

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src \
/opt/data/repos/weaverstack/.venv/bin/python \
/opt/data/profiles/editor/cache/scratch/check_lakehouse_item_first.py \
  --docs /opt/data/scratch/Fors/weaver-docs-refresh/item-first-lakehouse \
  --product /opt/data/scratch/Fors/weaver-docs-refresh/product
```

The temporary author checker is outside the repository; no owned tooling was changed. It blocks socket connections, parses the real CLI commands and configurations, compares fixture blocks, assembles prior/next checkpoints in scratch, runs real Check, asserts production-parser dependency edges, generates three Spark SQL runtime modules using pinned product functions and parses their Python, and hashes fixture files before/after. Its final successful result was:

```json
{"checkpoints": 7, "commands": 30, "generated_modules": 3, "pages": 6, "python_blocks": 11, "synced_blocks": 12, "workspace_configs": 2}
```

The seven successful Check calls cover the Python, Spark SQL and validation checkpoints, optional physical and logical Shortcut additions, the entire parcel-lakehouse fixture and the unchanged parcel-incremental fixture. The four asserted authored edges are:

```text
Lakehouse/Landing/Files/Parcel.Events → Lakehouse/Landing/Tables/Parcel.Event
Lakehouse/Landing/Tables/Parcel.Event → Lakehouse/Landing/Tables/Parcel.CurrentStatus
Lakehouse/Landing/Tables/Parcel.CurrentStatus → Lakehouse/Landing/Parcel.CurrentStatusMatches
Lakehouse/Landing/Tables/Parcel.Event → Lakehouse/Landing/Parcel.EventStatusIsKnown
```

Parser iterations exposed a scratch-checker counting mistake: the product also generates standard item documents. The final checker selects exact authored source paths instead of claiming every parsed document was authored. A second checker mistake compared the SQL dialect to prose instead of `SPARK_SQL`; the final gate requires exactly three generated modules. The temporary publication example's unsupported `--environment` spelling was corrected to the real positional Environment argument before the successful command-parser run.

Broad unchanged-reference/journey regression commands, from the docs worktree:

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src \
/opt/data/repos/weaverstack/.venv/bin/python tools/check_reference_examples.py \
  --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product

PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src \
/opt/data/repos/weaverstack/.venv/bin/python tools/check_journey_examples.py \
  --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product

PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src \
/opt/data/repos/weaverstack/.venv/bin/python tools/check_docs_refresh_examples.py \
  --weaver-checkout /opt/data/scratch/Fors/weaver-docs-refresh/product
```

- Reference: 103 commands, 6 configurations, 4 operation calls, 2 DAX files, 1 native edit.
- Existing journey checker: 15 pages, 92 commands, 9 configurations, 3 Python calls; 12 byte-identical blocks; four rendered-project Checks and offline compilation. Its hard-coded old routes remain untouched for the parent to integrate.
- Existing refresh checker: 6 fixtures and 53 README commands; source-runtime comparison and offline boundary checks passed; no live service exercised.

From the frozen product checkout:

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src \
/opt/data/repos/weaverstack/.venv/bin/python -m pytest -q \
  tests/targeted/test_spark_sql_validation_representation.py \
  tests/targeted/test_validation_artefacts_representation.py \
  tests/test_folder_change_feed_cycle.py
```

Result: **79 core tests passed in 2.01s**. This supports generator/change-feed claims, not the example's remotely observed row counts.

`git diff --check` and final `git diff --cached --check` passed. `git diff --cached --name-only` and `--stat` showed only the eleven assigned page/evidence/fixture additions (871 added lines before this evidence update). `git diff --exit-code HEAD -- examples/parcel-incremental examples/parcel-lakehouse/Lakehouse/Landing/Files/Parcel__Events.py examples/parcel-lakehouse/Lakehouse/Landing/Tables/Parcel__Event.py examples/parcel-lakehouse/Lakehouse/Landing/Tables/Parcel.ServiceLevel.sql` returned 0, confirming unchanged reused source. A focused heading-target scan verified all six existing relative fragment targets on the new pages; the five absent sibling page paths are separately accounted for below.

## Limits and integration handoff

- No remote runtime publication, Build, Load, Test, SQL endpoint query, Shortcut path or Health outcome was observed. Published results are expected user verification outcomes. Check establishes authored shape, not Spark SQL engine acceptance or source/service permissions.
- The full site cannot build independently until sibling Estate destinations arrive. The author checker accounted for five missing paths, all declared in the approved route map: `estate/catalogue-and-health.md`, `connected-items.md`, `development-cycle.md`, `environments.md`, `recovery.md`. Parent owns strict build, browser/search acceptance, old URL/fragment pointers and cross-site links.
- Existing branch-based GitHub fixture URLs follow the current preview convention. Their remote publication/readability is not verified here; parent owns publication and inbound-link checks.
- Parent should include the new Lakehouse pages and twelve fixture-block mappings in its integrated checker. The temporary author script is a reproducible local probe, not a new maintained tooling surface.
- `lakehouse/index.md` required no edit: its links and claims already match this journey. Nav, root/shared guides, Reference, old source pages, other item directories and tools remain untouched.
