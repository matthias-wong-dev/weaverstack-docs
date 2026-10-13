# Reader-journey implementation evidence

Behaviour target: `74b4d15ee65ed2740593af1f4d459771b801b132`.
Documentation base: `f35c943ed0ca423b92ab53aa571c43ae2817b74e`.

## Integrated scope

All D01–D13 paths are implemented. The ordinary Power BI route, second-environment deployment, source DAX Assumption, native modelling rule and optional Warehouse integration are separate tasks. Shared TMDL policy, trusted custom annotations, composition and standalone/source-generated models remain optional. Existing concept and operating URLs are retained and reconciled for mode-specific behaviour.

A1 and A2 commits are integrated, not just reported complete by their authors. Fors inspected their evidence and reran the combined fixture and generator checks. Full owner/source mappings remain in `reference-evidence.md` and fixture inventories/hash and unavailable service gates in `fixture-evidence.md`.

## Fresh parent execution

From the integrated docs worktree, using `/opt/data/repos/weaverstack/.venv/bin/python` with pinned `PYTHONPATH` or the tools' explicit `--weaver-checkout`:

- `tools/check_docs_refresh_examples.py --weaver-checkout <product>`: six real local CLI Checks; 53 README Weaver commands; actual fixture LoadDag/Runner and compiler/binding boundary checks; unchanged authored hashes; pass. Query/inventory answers are explicit offline doubles, never service results.
- `tools/check_journey_examples.py --weaver-checkout <product>`: all 13 task pages; 68 command lines parsed; five configurations; three public Python-call keyword sets; 12 fixture blocks byte-identical to the public page; four exact rendered projects assembled and checked. Rule/policy/standalone native compilation pass. Source-generation declaration Check does not claim resolved live metadata or deployed generated output.
- All four reference generators: two `--write` passes then `--check`; no byte changes. Ownership is 18 CLI leaves, 55 root Python exports, four supported semantic-extension class/protocol owners and 23 physical catalogue tables.
- Generator unit tests: Python 5, semantic 7, catalogue 4; all pass.
- `tools/check_reference_examples.py --weaver-checkout <product>`: 98 command lines, six configurations, four public-operation calls, two DAX blocks and one native editing example; pass.
- Optional public PBIR schema mode through `/opt/hermes/.venv/bin/python`: 36 documents against eight public Microsoft schemas; pass. No tenant contact.
- Locked MkDocs environment: `reference/.venv/bin/python -m mkdocs build --strict --site-dir <static-output>`; pass. Repository dependencies were not changed.
- Paired built-site crawl: 126 HTML pages, 20,500 local page/asset/fragment references, 166 cross-site links; zero broken targets/fragments. Seven developer benchmark rows match the product JSON's labels, raw seconds and displays. Counts apply to the unmodified public-origin build; private-origin rewrites are a separate preview preparation step.
- Ruff checks/format for all tools and `git diff --check`: pass.
- Every one of the 93 original documentation/asset paths is retained. New pages have navigation owners. Public text/examples scan found no selected credential patterns, private source-project/employer identifiers, local paths or truncation markers.

## Fresh parent source suite

Executed from the product worktree with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=src:tests:tests/targeted`, the existing product interpreter and `pytest -q -p no:cacheprovider`:

```text
tests/targeted/test_load_recursive_selection_cycle.py
tests/test_cli_load_representation.py
tests/targeted/test_invocation_api_concurrency_boundary.py
tests/targeted/test_invocation_concurrency_boundary.py
tests/targeted/test_notebook_source_concurrency_boundary.py
tests/test_workflow_cycle.py
tests/targeted/test_hosted_runtime_identity_boundary.py
tests/targeted/test_protected_mirror_materialisation_cycle.py
```

**232 passed in 13.36s**, core only, no declared external resources. This reruns original-seed expansion, resource/total caps, workflow findings versus exceptions, exact runtime admission and protected materialisation. The earlier parent 176-case run is overlapping coverage, not an additional total. A1's 1,559-case and A2's 311-case author suites are separately recorded and overlap one another and this run; do not sum them.

Final product runtime/test/configuration trees still match the source pin. Product HEAD contains website documentation changes only; the whole checkout is not claimed to remain at the pin.

## Browser and visual evidence

- Product: 55 route/viewport checks at 375, 768, 1024, 1250 and 1440px; keyboard/touch/native disclosure, focus return, Escape, no-JavaScript access at 375/1440, static benchmark rows, no console/page errors; pass.
- Developer: 190 route/viewport/theme checks over 19 task/reference/entry routes at the same widths in light/dark; touch drawer, no-JavaScript content/navigation, real built search index and correct documentation edit URLs; pass, no page errors.
- Inspected selected phone/desktop screenshots for entry routes, benchmark, code, long configuration and navigation. These are viewport states, not full-page stitched captures.
- Corrected intrinsic Reports-card overflow with `min-width: 0`, inherited dark GitHub CTA text, light-mode Python name/builtin token contrast, and dark-block filename-label contrast.
- Focused final CSS contrast recheck: 774 token observations across four representative code pages in both themes, minimum 9.72:1; product GitHub CTA 18.36:1. Final corrected screenshots inspected.
- Screenshot evidence stays outside the repository in the private review workspace. Independent reader review is the approved final batch, still a separate gate until its findings are integrated.

## Corrected failures and unavailable gates

Initial storage exhaustion caused browser/installation failures; existing runtimes were reused. Full-page capture failed while viewport JPEG worked. A test harness initially treated pointer focus as keyboard focus, then correctly entered keyboard modality. Another selected the hidden drawer overlay rather than its actual header control; fixing the locator made the 190-case pass. A later redundant whole-browser rerun timed out after the product pass; the preceding complete developer pass is preserved, not relabelled as that timed-out run. The final small CSS changes were instead exercised by the focused contrast/render pass.

The first rendered-policy assertion incorrectly addressed a native calculation-group block as a child collection; it was corrected to the supported live `calculationGroup` property and Current item, and the exact four rendered projects passed. No runtime defect was patched.

Private paired preview artifacts and loopback HTTP targets are healthy; their HTTPS mappings were read back with all existing Serve routes unchanged and no public Funnel. A userspace self-hairpin probe timed out, so a separate tailnet peer has not been observed loading the sites. Private preview addresses are supplied outside this public repository.

No capacity operation, live service mutation, merge, package release or public publication. Deployment/refresh, real DAX/SQL outcomes, Report rendering/binding, deployed native-rule/variant/generation inspection, catalogue readback, service-deployment hash preservation and licence eligibility remain **not run**. Matching package availability and explicit publication approval remain gates. Installation explains the exact source snapshot rather than attributing these interfaces to PyPI `0.9.0`.
