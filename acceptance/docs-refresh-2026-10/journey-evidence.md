# Reader-journey implementation evidence

Product/source target: `74b4d15ee65ed2740593af1f4d459771b801b132`.
Documentation base: `f35c943ed0ca423b92ab53aa571c43ae2817b74e`.

## Current checkpoint

Fors has implemented D01 and D07–D09, the two entry-route indexes, mode-specific Core concept updates, ordinary run/recovery/validation links, Build preview, and targeted existing Advanced/runtime/protection corrections. D02–D06 and D10–D13 depend on the fixture/reference batch and are not yet claimed complete. Navigation and final coverage reconciliation follow integration.

## Fresh local source evidence

Executed from the pinned product worktree:

```text
PYTHONPATH=/opt/data/scratch/Fors/weaver-docs-refresh/product/src /opt/data/repos/weaverstack/.venv/bin/python -m pytest tests/targeted/test_load_recursive_selection_cycle.py tests/test_cli_load_representation.py tests/targeted/test_invocation_api_concurrency_boundary.py tests/targeted/test_invocation_concurrency_boundary.py tests/targeted/test_notebook_source_concurrency_boundary.py -q
```

Result: **176 passed in 9.77s**, core only, no declared external resources. This exercises current public API/parser recursive selection, original-seed union, scope/error behaviour and total/resource concurrency. It is not a report of the new fixture's service execution.

## Additional source-backed corrections

- `weaver_cli/workflow.py::_execute`: Test/Health returned findings accumulate while later entries run, then final exit is 1; an execution exception/non-finding failure stops the sequence. Reconciled Concepts, Basics and automation prose. Fresh focused workflow tests remain pending.
- `sessions/{base,console,hosted_runtime}.py`: Spark-backed Build admits a matching hosted runtime before mutation. Old “Build never needs a published Environment” prose is incorrect at this target. Desktop generated Lakehouse Load/Test also needs Weaver in the Environment. Corrected workspace/runtime, Python/Spark SQL guides, portability and automation.
- `sessions/hosted_runtime.py::require_compatible`: actual checks include exact Weaver version, supported plan format, Delta writer and executor capabilities; previews do not establish runtime compatibility.
- `build_bundle/{materialisation,executors/materialise_mirror}.py` and `targeted/test_protected_mirror_materialisation_cycle.py`: protected borrowed Tables/Folders use CTAS/shallow-clone/native-copy materialisation and retain bookmarks. Source retention and destination partial-failure boundaries remain explicit; it is not backup or universal Wipe/reload protection. Fresh focused tests remain pending.
- `operations/test.py`: `--source` alone does not force file mode with a configured catalogue. `--file` or a catalogue-free workspace selects file mode. Python uses `names`/`files`, returns reports and does not accept obsolete `strict=`.
- `catalogue/tables.py`: five SemanticModel metadata tables plus SemanticModelTest exist at this target; Report registration is through existing Installation/Registry claims, not an invented Report table.

Official Microsoft model-creation permissions and licensing pages were freshly extracted; the API requires Contributor rights and appropriate licensing. Workspace-specific API/refresh/query entitlement is not locally established.

## Preview and storage status

Matthias requested completion and private Tailscale previews overnight. Existing Tailscale node is running as `klein.tail48523a.ts.net`; existing Serve routes are preserved. New preview mappings are not yet claimed configured.

Product static server is locally healthy on 127.0.0.1:8845, serving only `product/docs/`, not repository/configuration roots. Browser tests found and corrected a narrow Reports-card overflow (`min-width: 0`). Full-page screenshot capture failed in the installed headless browser; viewport JPEG capture works. A subsequent multi-page browser pass encountered `ERR_INSUFFICIENT_RESOURCES` while persistent storage was nearly full. Product browser acceptance is therefore still pending, not passed.

## Gates not claimed

No live resource mutation, package release, merge or public publication. Independent service deployments, Report viewing/binding readback, DAX pass/finding/query failure, SQL reconciliation, native deployed rule/variant inspection and licensing-mode acceptance remain unrun. The matching public release and explicit publication approval remain gates even after draft PRs/previews are delivered.
