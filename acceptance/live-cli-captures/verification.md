# Live CLI capture verification

## Evidence boundary

- Documentation starting head: `b4eb2d61c3b910eabbddc6ea58618d9471fe3a2d`, existing `docs/progressive-journeys-refresh` branch and draft PR #3.
- Runtime and installed wheel: `bf908f4754eca4d10a56afd218e9e18d423636d7`, `weaverstack 0.9.0.dev16746776803276843971`. This is a built development wheel, not released-PyPI acceptance. The source worktree remained clean at that exact revision on final readback.
- Execution: authorised Weaver Example disposable Fabric trial workspace, one continuing additive Parcel project. Existing Weaver Environment received the matching development runtime. No production workspace, additional capacity, tenant-setting change, new credentialled service connection, Mirror, Wipe or reset was used.
- Capture date: 16 October 2026 in Australia/Canberra. Full original PTY streams, command/status metadata, direct SQL/API observations and private snapshots are retained outside Git. The committed [manifest](../../docs/assets/cli-captures/manifest.json) records substitutions, commands, working context, statuses and sanitisation.

## Delivered evidence

**81 recorded command attempts**, **51 output panels across 17 existing pages**, and **27 selected SQL/API observations**. Attempt totals include deliberate failed validations, genuine operational findings, one interrupted retry prompt and one qualified capture-helper invocation error. They are not 81 successful operations. See [capture inventory](../../CAPTURE-INVENTORY.md) for the operation-by-operation ledger and remaining scope.

Actual Warehouse and Lakehouse Build/Load/Test/Health were exercised, including their generated SQL/Python and Spark SQL. Both external incremental examples demonstrated initial rows, changed input, target update/deletion, unchanged Load and increasing consumer bookmarks. Native Power BI ran without a configured Catalogue through explicit normal workspace configuration: model Build, refresh, DAX = 2, deployed before/after foreign-key visibility, deliberate DAX = -1 finding and restoration. Report definitions and destination-specific model bindings were independently read back.

Backend readbacks in [readbacks.json](../../docs/assets/cli-captures/readbacks.json) are labelled as SQL/API observations, not CLI output or screenshots. Full encoded model/Report definitions remain private; only selected decoded observations are published.

## Automated checks

All completed successfully on the integrated working tree:

- `tools/render_cli_captures.py --check`: **51 panels** match real sanitised transcript line ranges. Escaping, zero-failure colouring, exact text/glyph order, rendered-route asset links and explicit excerpt labelling have regression tests; each new renderer behaviour was observed failing before implementation.
- Documentation tests: **27 passed, 3 subtests passed**, including the five capture renderer regressions. No product/runtime behaviour was changed.
- Four reference generators in strict check mode: CLI, Python, semantic extensions and Catalogue.
- **16 generated Initialise excerpts** match their source. Reference, refresh, journey, estate, Report, Lakehouse and semantic-model fixture/example gates pass. The refresh gate uses its existing explicit `--runtime-revision bf908f4754eca4d10a56afd218e9e18d423636d7`; its old-default refusal remains intact.
- Ruff check and format check of both new Python tools; `git diff --check`.
- Strict MkDocs build: **162 HTML pages**, no navigation/configuration changes or new public pages.
- Built route retention: **114 original pages, 872 original fragments, 35 canonical pages present, 27 compatibility routes, 3,957 documentation links**, no errors. Route-gate self-tests also passed (12 tests).
- Paired-site crawl: **23,417 local links/assets**, 276 cross-site links, **zero broken links/fragments**. Fabric-first story/parser gate passed.

### Browser checks

The final built-content identity completed **85 states across all 17 changed output-bearing routes**:

- 390px and 1280px, both actual Material light/dark themes with JavaScript;
- 390px light theme with JavaScript disabled;
- **255 panel text checks**, exact browser `textContent` versus selected real output, native DOM selection and successful complete-transcript asset fetches;
- **792 clipboard checks** against authored source or real transcript bytes, with Markdown's established four-column tab expansion for source and terminal-newline normalisation declared;
- **105 full-transcript disclosures** opened and compared with source, including no-JavaScript cases;
- no document-width overflow or page errors; local terminal scrolling retained;
- terminal foreground/status contrast minimum **9.42:1**, above the checked 4.5:1 threshold.

Representative phone light-mode Warehouse and desktop dark-mode native-model screenshots were inspected for the terminal hierarchy and legibility. Screenshots and the detailed browser matrix remain private. This is selected-state visual inspection plus automated geometry/content/interaction coverage, not Power BI UI or human editorial acceptance. Earlier preflight states were not added to the final 85-state count.

### Privacy

Credential and identifier scans covered **670 source/build text files**, including ANSI-stripped capture content. Three actual authorised credential/tenant/client values and observed private identifiers were checked without printing their values. No leaks were found. A separate general scan of all capture assets found no unredacted GUIDs, JWT-shaped tokens or private host filesystem paths. SQL endpoint hostnames, item/run identifiers and local paths are redacted; exact original evidence stays private.

## Continuous reader review

### First Warehouse

Initialise produces the visible project setup; generated StatusEvent and CurrentStatus source stays in place. Check, Build, initial Load, Test and Health each have their own immediately following output. The three-event Load result is distinguished from the two-row CurrentStatus SQL result. Predicted “should print/show” narration was removed. The Warehouse-only runtime qualification remains explicit, as do disposable-target and Build-pruning warnings. The capture note identifies the development wheel and actual workspace rather than implying published-package acceptance.

### Connected estate

The reader retains Landing, adds Operations without replacing its independent pipeline, reads the logical Shortcut and additional LakehouseCurrentStatus definition, then sees real cross-item Build, Load and Health. The Amber Test result is explained at that point and links to validation before the Green scoped report. Configured scope is carried through Test and Health; unrelated older Catalogue findings are not erased by narrowing the report. Named previews show installed producers/consumers before execution, and concurrency distinguishes a sequential dependency chain from two independent validations starting together.

The reverse extension after authored Warehouse shortcuts genuinely refused the unowned mapping. The page records a protected local save/merge before Check/Build; preservation was verified, not assumed. No runtime fix or silently discarded user mapping is claimed.

## Remaining limits and state left behind

1. **Managed source:** Build/certification and source Load succeeded, but ParcelWarehouse refresh failed because its default connection has no explicit cloud/gateway credentials for Operations and no matching connection was available. No connection was created. Its installed reconciliation Test remains pending; neither DAX/SQL equality nor the optional discrepancy/recovery exercise is claimed. The managed source capture includes the measure/Test introduced in the validation task; the manifest names that checkpoint.
2. **Final data estate:** scoped Test and Health (127–128) passed: four validations, Green Load/Tests/Build, 29 installed objects. The separately selected managed model's Health (126) is Load Red, Tests Amber/pending, Build Green. Narrowing to data items does not make that model healthy.
3. **Reports:** both environment configurations used distinct physical pairs in Weaver Example. Actual second-workspace access, Report card rendering and service field-list UI were not observed; live definition/binding/query checks are separate evidence.
4. **Mirror/destructive paths:** no approved reset/re-mirror destination scope; not executed. No cleanup/deletion was performed outside the example's explicit source-data mutations.
5. **Optional breadth:** the larger branching example, shared-policy/custom-handler/composition walkthroughs and notebook UI interaction were not separately exercised live. Their static/fixture gates passed; those are not substituted for live outcomes.
6. **Publication:** matching released-package acceptance and Matthias's publication approval remain required. Draft PR only; no merge, release or public documentation deployment.
