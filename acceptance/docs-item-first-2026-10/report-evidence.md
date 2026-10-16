# Report deployment and environment binding evidence

## Scope and reader route

Branch: `docs/item-first-reports`. This batch adds only `docs/reports/deploy.md`, `docs/reports/environments.md` and this evidence record, plus direct-entry/checkpoint instructions in `examples/parcel-powerbi/README.md`. The existing Reports index already describes the correct Build-only boundary and links to both tasks; it was reviewed unchanged. No native definitions, configurations, runtime, generated Reference, navigation or legacy routes changed.

Reader route: **Reports → Deploy a native Report → Development and production Reports → Workspace and environment mappings** (`docs/reports/index.md` → `deploy.md` → `environments.md` → `docs/estate/environments.md`). The last destination and whole-site integration belong to the parent/estate batch.

- Direct-entry state: the complete existing `examples/parcel-powerbi` native Import model/Report snapshot and its two configurations. No semantic-model tutorial or model reauthoring is required.
- Continuing state: keep the same project, Report and any overlay from the native-model task. First Build selects both local items with `PowerBI/Parcel`; the next task selects the second configuration, with no native-file change.
- Result: development `Parcel_Report_Dev` binds to `Parcel_Dev`; production `Parcel_Report` binds to `Parcel`. Local checks below prove payload construction, not remote installation.
- Separate viewing checkpoint: optional semantic-model refresh, then Delivery Count expected to be 2. Reports have no independent Load, Test or refresh. Nothing here claims the card was rendered remotely.

Two transition paragraphs from the new pages:

> The development Report now has a destination-specific model binding while the source still names `../Parcel.SemanticModel`. Use the same Report in development and production by selecting a second configuration, not editing that path.

> The Report now follows its model into each workspace without a source edit. When you also need to move its Lakehouse or Warehouse sources, use workspace and environment mappings for the whole project. Destination names alone do not change source expressions or credentials. For changes to the model itself, return to native TMDL and overlays.

## Evidence source

Behaviour pin: `74b4d15ee65ed2740593af1f4d459771b801b132`.

Evidence checkout: `/opt/data/scratch/Fors/weaver-docs-refresh/product`, actual HEAD `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`. Both the committed tree and working tree were compared for `src`, `tests`, `pyproject.toml` and `uv.lock`; no differences from the pinned behaviour were found. The reused product interpreter was `/opt/data/repos/weaverstack/.venv/bin/python`. With the pinned checkout's `src` first on `PYTHONPATH`, the actual import was:

```text
/opt/data/scratch/Fors/weaver-docs-refresh/product/src/weaver/__init__.py
```

| Claim | Production source and focused tests |
| --- | --- |
| Local model association, same-name precedence, unrelated `byConnection` retained | `src/weaver/powerbi.py:read_reports`; `tests/test_report_convention_cycle.py`, `tests/test_powerbi_project_declaration.py` |
| Resolved IDs go into the deployment payload; native parts unchanged | `src/weaver/report_definition.py:encode_report`, `service_reference`; `tests/test_report_definition_representation.py` |
| Model deployment/readback precede Report; wrong workspace binding blocks success | `tests/test_report_build_cycle.py` exercising production Build and its action graph |
| Linked Report-only requires a certified installed model when not selected | `src/weaver/build_bundle/reports.py:bind_reports`; `tests/test_report_binding_boundary.py`, `tests/test_report_catalogue_cycle.py` |
| Ordinary Build creates missing selected model/Report items | `tests/test_powerbi_item_creation_cycle.py` |

The published JSON is the entire fixture `PowerBI/Parcel/Parcel.Report/definition.pbir`, including schema URL, version `4.0` and `byPath.path = ../Parcel.SemanticModel`. All three published YAML blocks match the existing dev/prod files byte-for-byte. No destination GUIDs were put into reader-facing examples.

## Executed local checks

The focused checker was run with the product interpreter and pinned `PYTHONPATH`. It reused `tools/check_docs_refresh_examples.py` functions `parse`, `check_native`, `check_report_bindings`, `hashes` and `check_readme_commands`. In-process and CLI Check subprocess socket connections were blocked. An additional call used production `_item_bindings`, `bind_reports`, `FabricResolver`, `encode_report` and `decode_report` over the source tests' existing `InventoryClient`. No binding algorithm or service-response implementation was substituted.

Actual output:

```text
PASS existing fixture helpers: native model/card, dev/prod encoder; no service readback
PASS linked Report-only without certified catalogue: Report/Parcel: SemanticModel/Parcel is not certified; build the model first
PASS published blocks: 1 exact JSON, 3 exact YAML; 8 CLI commands parsed
PASS README CLI commands: 5
CLI Check JSON: {
  "status": "succeeded",
  "project_folder": "."
}
PASS 17 fixture file SHA-256 values unchanged after all local checks
Authored definition.pbir SHA-256: 2bee1238155460ae456f766cb91afc43dc88fe8f1e520225a584d2464db68305
```

The hash baseline was taken after the authorised README addition, before parsing/compilation/encoding/Check. Every fixture file matched afterward. Git diff additionally confirms that native and configuration bytes were not edited.

The real resolver over **offline inventory inputs**, followed by production binding/encoding, produced these mappings:

| Configuration | Report target | Model target | Offline workspace ID | Offline model ID |
| --- | --- | --- | --- | --- |
| dev | `Parcel_Report_Dev` | `Parcel_Dev` | `8ef5926e-8ee7-5fc9-b1d1-664dcc50a0dd` | `ed9d228e-4d1c-5839-a090-7b77d65f0177` |
| prod | `Parcel_Report` | `Parcel` | `45e88337-608d-56a1-b991-6cf15ec330c8` | `aedce665-c160-5237-abfa-17e5673caf62` |

These IDs come from the existing test helper, **not** a tenant. Both encoded `byConnection.connectionString` values carry the corresponding workspace ID in `Data Source`, and the model ID in both `Initial Catalog` and `semanticModelId`. The two model IDs and workspace IDs differ. All Report parts other than `definition.pbir` match the original bytes. The authored file still has `byPath`.

Reproduce the focused fixture/binding helper checks from this worktree:

```bash
WEAVER_CHECKOUT=/opt/data/scratch/Fors/weaver-docs-refresh/product
PYTHONPATH="$WEAVER_CHECKOUT/src:$WEAVER_CHECKOUT/tests:$WEAVER_CHECKOUT/tests/targeted" \
  PYTHONDONTWRITEBYTECODE=1 /opt/data/repos/weaverstack/.venv/bin/python - <<'PY'
import importlib.util
from pathlib import Path
import json
import socket
spec = importlib.util.spec_from_file_location('checks', 'tools/check_docs_refresh_examples.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
socket.create_connection = checks.refuse_network
socket.socket.connect = checks.refuse_network
root = Path('examples/parcel-powerbi').resolve()
before = checks.hashes(root)
repository = checks.parse(root)
checks.check_native(root, repository, json.loads((root / 'expected-results.json').read_text()))
checks.check_report_bindings(root, repository)
assert checks.hashes(root) == before
print('PASS native fixture, dev/prod encoding and authored hashes unchanged')
PY
```

Focused product suite:

```bash
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src \
  PYTHONDONTWRITEBYTECODE=1 /opt/data/repos/weaverstack/.venv/bin/python -m pytest \
  tests/test_report_build_cycle.py tests/test_report_binding_boundary.py \
  tests/test_report_definition_representation.py tests/test_report_convention_cycle.py \
  tests/test_report_catalogue_cycle.py tests/test_powerbi_item_creation_cycle.py \
  tests/test_powerbi_project_declaration.py -q -p no:cacheprovider
```

Run from the product checkout. Actual result: **101 passed in 6.10s**, all declared as core tests. Their service boundaries are offline test doubles; their success does not mean live service acceptance.

Public PBIR schema validation reused the existing helper, restricted to this fixture, with the already-installed Hermes interpreter because the product interpreter lacks `jsonschema`. No package/environment was installed:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/hermes/.venv/bin/python - <<'PY'
import importlib.util
spec = importlib.util.spec_from_file_location('checks', 'tools/check_docs_refresh_examples.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
checks.FIXTURES = ('parcel-powerbi',)
checks.check_pbir_schemas()
PY
```

Actual result: **6 PBIR JSON documents validated; 8 public Microsoft schemas fetched; no Fabric calls**. Fixture hashes were also compared before/after that check and remained unchanged.

`git diff --check` passed. The temporary focused-check harness initially referred to argparse's nonexistent `item` rather than `items`; it was corrected and the complete check rerun successfully. The initial schema attempt with the product interpreter failed for missing `jsonschema`; the existing Hermes interpreter completed it. Neither issue required a repository-tool or runtime change.

## Limits and integration handoff

No service deployment, refresh, DAX query, Report rendering, tenant/licence eligibility, live credentials, capacity action or deletion was attempted. The pages' lineage/API binding inspection and card value are **reader readback steps with expected results**, not remotely observed evidence. Public schema validation covers authored PBIR files; it is not service validation of an encoded payload.

Parent owns the strict full-site build, browser/search/link integration, incoming/legacy fragment migration and independent reader review. `../semantic-models/native-tmdl.md` and `../estate/environments.md` are the approved sibling/later-batch destinations, not pages added by this branch. The direct-entry project link remains on the existing draft's `docs/progressive-journeys-refresh` branch. No push, PR change, publication or release was performed.
