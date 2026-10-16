# Live CLI capture inventory

Full live walkthrough and capture refresh: **17 October 2026 (Australia/Canberra)**. Every tutorial and estate page was followed in reader order against the disposable **Weaver Example** Fabric workspace, starting from an empty workspace. All 73 terminal panels were recaptured from that run; earlier captures from runtime `bf908f4` were removed.

## Execution provenance

- Runtime: scratch integration `afb5b31c36498aeb8b70927e7f723de054225d5e` = Weaver `feat/catalogue-dashboard` (`5ecccde`) + the runtime commits from weaverstack PR #222 (`80af419b`, `89e93c78`, `bf908f47`, `fb725f76`, `1521ab9b`) + three Initialise fixes found during this pass (below). The Parcel generator these docs depend on is **not in Weaver `main`**; it exists only in PR #222.
- Installed from a checkout wheel, then an editable checkout. The Fabric Environment was published with `--dev`. The docs show the PyPI command without `--dev`.
- Captures display the workspace as `Parcel Development`. The managed-source captures (111–117) ran against `CatalogueBI`/`OperationsBI` in a separate Power BI-first project, so they would not overwrite the estate's Operations Warehouse; they display those items as `Catalogue`/`Operations`. Identifiers, run IDs, local paths and endpoint hosts are redacted. See the [manifest](docs/assets/cli-captures/manifest.json).
- SQL, DAX, definition and notebook observations are recorded separately in [readbacks](docs/assets/cli-captures/readbacks.json).

## Runtime fixes made during the pass

These are needed for the documented commands to work from a normal `pip install`. They are committed only in the scratch integration above and must land in Weaver before release:

1. **Bytecode in the installed example.** `pip` compiles the bundled Parcel `.py` files into `__pycache__`; the PR #222 example reader then fails with `UnicodeDecodeError` on any Lakehouse Initialise. Fix: skip `__pycache__`/`.pyc` when reading the example tree.
2. **Authored `shortcuts.yml` on extension.** Adding Landing to a Warehouse project that already has an authored physical Shortcut refused with "would overwrite … Choose another project folder". Fix: merge generated Shortcut mappings into the authored file when no destination conflicts (conflicts still refuse). Resolves the former connected-items TODO.
3. **Re-asked bindings on extension.** Interactive extension asked for the Catalogue and Environment again although `workspace-config.yml` bound them. Fix: the wizard takes configured bindings and existing items as answers.

## Coverage and outcomes

| Route | Result |
| --- | --- |
| Warehouse first project, Tests (failure and restore, file mode), incremental (insert, update+cancel, no-op, bookmarks) | Complete. |
| Lakehouse Python, Spark SQL, Tests, incremental with ParcelSourceArchive, notebook checks | Complete. The three notebook cells ran as real Fabric notebooks with the stated default Lakehouse attached; a deliberate failing control notebook reported Failed. |
| Connected items, mappings, Health, operate, selective runs including the branching Reporting graph, concurrency | Complete. |
| Session, workflow, bundle-only Build and Install | Complete (not shown as panels). |
| Reload, Mirror, materialisation after Mirror, re-mirror, Wipe preview and Wipe with `--unbind`, rebuild after Wipe | Complete. The first rebuild after Wipe hit a transient Fabric `Snapshot isolation transaction failed`; rerunning Build succeeded (documented on the Recovery page). |
| Native model, AutoHideForeignKeys, DAX Assumption (pass, fail, restore), shared policy, custom annotation and diagnostic, composition, standalone TMDL | Complete. Shared policy initially failed Build readback (`/model/tables/Display/partitions`); the documented calculation group now declares its `calculationGroup` partition. |
| Report deploy and two configurations | Bindings and DAX verified in one workspace. |
| Power BI-first project gaining a Catalogue and Warehouse | Complete through Build; the Catalogue-backed Build adopted the previously Catalogue-free `Parcel` model. |

## Open TODOs (still marked on pages)

| Marker | Blocker |
| --- | --- |
| `managed-refresh`, `parcel-native-source-refresh`, `dax-sql` | Need a credentialled cloud connection to the Operations SQL endpoint. None exists in the tenant; none was created. |
| `report-workspaces` | Needs a second disposable workspace. |
| `report-rendering`, `report-cards` | Need someone signed in to the Power BI service; Report export returns 403 on the trial capacity. |

## Product observations not changed in the runtime

- Initialise's closing hint always suggests `weaver fabric environment publish` and `weaver workflow full`, even for Warehouse-only projects.
- Errors in an interactive terminal stop at `Enter to retry, Esc to exit`; a pasted next line becomes the answer. Pages that pair an expected error with a restore command say to run them one at a time.
- Extending a project that contains the composition example's `ParcelBase.SemanticModel` adds a `SemanticModel/ParcelBase` target, which undoes the composition page's "no base target" setup.
- `weaver mirror --workspace-config workspace-development.yml` (no `mirror:` key) reports "mirror needs a destination catalogue", which does not point at the missing source.
- Build progress groups one Verify step as `SemanticModel/ParcelOperations, Report/ParcelExecutive` when deploying two variants.
- Health shows a never-run installed DAX Assumption as "the last run pending".

## Verification

`render_cli_captures.py --check` (73 panels), `sync_initialise_examples.py --check`, the four reference generators, the reference/journey/Report/estate/homepage/semantic/Lakehouse example gates, `check_item_routes.py`, `check_fabric_first_story.py` (against the PR #222 product site), the tool unit tests, and a strict MkDocs build all pass. `check_docs_refresh_examples.py` is pinned to fixture provenance `74b4d15` and refuses another checkout by design; it was not run. All 327 documented `weaver …` commands parse with the runtime's CLI parser.
