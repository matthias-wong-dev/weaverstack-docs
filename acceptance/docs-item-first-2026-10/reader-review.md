# Independent reader-flow review

## Result and boundary

**Not ready to close editorial acceptance.** The Lakehouse, Warehouse and Report routes now have a coherent first success and an explicit continuation. The native model task delivers a meaningful built-in annotation without requiring a catalogue or custom Python. Two continuation defects remain in the assembled estate/model routes, and mobile/tablet search has a demonstrated rendering failure.

This is an independent agent review, not human approval. Matthias retains the final editorial decision. I changed no public page, navigation, fixture, tool or product file. The corrections below are recommendations for parent disposition, not revisions already made.

Reviewed documentation base: `8a94013c420e0889fefdf89c7a10546bb7bd2d62`, branch `docs/item-first-reader-review`. Authority: the approved reorganisation plan, repository `AGENTS.md` and `PROSE.md`, source `PROSE.md`, and `acceptance/docs-item-first-2026-10/route-map.md`. Public preview exercised: `http://127.0.0.1:8846/`. A byte comparison of Home and all five item/estate Markdown directories against the serving parent worktree at `journeys/docs` found **36 files, no differences**. This does not assert every generated HTML byte's provenance.

No live Fabric operation, model query, Report binding/readback, credential use, capacity action, remote GitHub mutation or release was performed. Previously supplied green build/route/link gates are not this review's editorial evidence and were not rerun here. No separate Tailscale peer-access claim is made.

## Required corrections

### R1 — P1: phone and tablet search produces results that readers cannot see

- **Reader state:** a direct entrant opens Search and types `Health` or `foreign keys` on the phone. The query is visible, but the area below it is blank. This blocks search as a route into later tasks even though the search index contains the correct owners.
- **Exact surface:** Search on [Home](http://127.0.0.1:8846/), reproduced at `390 × 844` and `768 × 844`. Relevant source: `docs/assets/stylesheets/extra.css:119–126`, specifically `.md-header { backdrop-filter: blur(14px); }` at line 125.
- **Measured evidence:** with Search open and results populated, `.md-search__inner` is only **58 px** high at 390 px width; `.md-search__output` is **10 px** high. At 768 px width these heights are **66 px** and **18 px**. The first result starts at y=84, outside the clipped output. A hit test at `(120, 180)` reaches the underlying article rather than a result. Desktop search at 1440 px width displays results normally.
- **Cause isolated without a repository edit:** disabling only the header's `backdrop-filter` in the diagnostic browser DOM expands the mobile search container to **844 px**, output to **796 px**, and makes the result occupy the hit-test point. The blur creates a containing block for Material's fixed mobile search panel. The diagnostic context was then closed; the preview's source remains unchanged.
- **Smallest correction:** prevent the header blur from establishing that containing block at the mobile search breakpoint, for example by disabling it there. Preserve the existing responsive search panel rather than hiding overflow or changing the search index.
- **Acceptance basis:** plan §9 Phase 5 and §10 require usable mobile/tablet search and direct entry, not merely indexed matches or HTTP 200.
- **Recheck:** repeat the same search at 390 and 768 px, assert results are inside the visible output and pointer-reachable, select a live result, and retain a desktop control. The current DOM-only matching counts must not be reported as a mobile search pass.

### R2 — P1: the estate's default progression still drops the checkpoint it just established

- **Reader state:** I already have Landing working. [Connect items](http://127.0.0.1:8846/estate/connected-items/#present-landings-event-in-dispatch) adds Dispatch and exposes Landing's three events. Its closing link promises to map development/production without changing those logical identities. The next page's first runnable example is instead Operations StatusEvent/View. Later, Health can use the managed Delivery model checkpoint, but the development page's first runnable loop sends me back to StatusEvent/View. The labels are honest; the continuous path is still assembled from different defaults.
- **Exact transitions:**
  - `connected-items.md:52,70` links to [Workspace and environment mappings](http://127.0.0.1:8846/estate/environments/).
  - Its first heading, [Bind the project to Fabric](http://127.0.0.1:8846/estate/environments/#bind-the-project-to-fabric), starts from the unrelated Warehouse first task (`environments.md:9–28`). Landing → Dispatch is addressed only at [Apply the mapping to Lakehouses and runtime](http://127.0.0.1:8846/estate/environments/#apply-the-mapping-to-lakehouses-and-runtime), lines 85–89, without a worked continuation of its configuration.
  - [Keep development and production bindings separate](http://127.0.0.1:8846/estate/environments/#keep-development-and-production-bindings-separate), lines 34–75, switches to managed Operations Delivery/model/Report. This change is explicitly explained and is technically legitimate.
  - [Catalogue and Health](http://127.0.0.1:8846/estate/catalogue-and-health/) lets me keep my installed item or the managed Delivery checkpoint, but its sample command uses `workspace-dev.yml` (`catalogue-and-health.md:5–9`).
  - Its next link reaches [The development cycle](http://127.0.0.1:8846/estate/development-cycle/), whose first prerequisite is StatusEvent/View and `workspace-development.yml` (`development-cycle.md:9–28`). The managed Delivery loop appears later at [Include semantic models and Reports](http://127.0.0.1:8846/estate/development-cycle/#include-semantic-models-and-reports), lines 39–54.
- **Why this is not a demand for one fictitious estate:** Landing/Dispatch, StatusEvent/View and Delivery/model are valid independent checkpoints. The managed-model variation must remain explicitly separate. The defect is promoting a different checkpoint as the next page's default after promising to continue the previous one; simply saying which different fixture is in use does not supply that continuation.
- **Smallest correction:** make the leading mapping, Health and ordinary-development instructions carry forward the reader's working project and selected configuration. Use the existing Landing/Dispatch configuration when demonstrating that particular continuation. Keep StatusEvent/View and managed Delivery as clearly marked worked alternatives, with direct links into the relevant existing sections. This needs a continuity/command-selection edit, not a new fixture or invented Landing-to-Delivery relationship.
- **Acceptance basis:** plan §1.3, §5 A–D, §7 continuity, and §10's continuous estate read-through. The route-map already requires connect → map → inspect → iterate, not restarting an earlier item tutorial to change default examples.
- **Recheck:** read connect → mappings → Health → development → operate with one actual checkpoint and configuration recorded at every stop. A reader choosing the managed variation once should not be sent back to StatusEvent for the ordinary loop.

### R3 — P2: the model footer's Next link lands on the wrong validation start state

- **Reader state:** I have just loaded Operations Delivery and refreshed its Warehouse-backed Parcel model. The authored closing link correctly offers reconciliation in that same checkpoint. The rendered footer's **Next — Validate a semantic model** instead lands at the top of a page whose first instructions say Parcel has *inline Import data* and direct entrants should deploy the native validation snapshot.
- **Exact links/headings:** [Managed sources](http://127.0.0.1:8846/semantic-models/managed-sources/) ends with the correct contextual [Compare DAX with source SQL](http://127.0.0.1:8846/semantic-models/validation/#compare-dax-with-source-sql) link (`managed-sources.md:99`). Its footer links to `/semantic-models/validation/` without the fragment. At [Start from the model you already deployed](http://127.0.0.1:8846/semantic-models/validation/#start-from-the-model-you-already-deployed), `validation.md:7–9` requires the inline checkpoint. The managed continuation is not reached until line 93.
- **Observed interruption:** following the footer on both desktop and mobile reaches the inline start state. This is not a broken URL or a missing reconciliation capability. It is two competing next-task instructions for a reader who already has the required managed-source state.
- **Smallest correction:** add a visible branch at the validation entrance that sends an already loaded managed-source reader directly to reconciliation, or make that footer land at the existing reconciliation fragment. Keep the independent inline Assumption route available. Do not ask the managed reader to reprovision or reverse the partition change.
- **Acceptance basis:** plan §1.3, §6's natural next step, §7's managed-source → reconciliation checkpoint, and §10's prohibition on unexpected fixture changes.
- **Recheck:** use both the in-body link and the footer from the managed-source task. Neither should imply returning to inline data before using the deployed managed model.

## Five independent read-throughs

### 1. New Lakehouse reader

Actual route: [Lakehouse](http://127.0.0.1:8846/lakehouse/) → [Python/files](http://127.0.0.1:8846/lakehouse/python/) → [Spark SQL](http://127.0.0.1:8846/lakehouse/spark-sql/) → [Tests](http://127.0.0.1:8846/lakehouse/tests/) → [Incremental changes](http://127.0.0.1:8846/lakehouse/incremental/).

The first result is comprehensible before the catalogue: a generated carrier CSV, its Python reader, three Event rows, then two CurrentStatus rows. The import supplies an understandable dependency. SQL explicitly retains Event and the Folder; Tests check those names and distinguish Load success from correct results. Installation and runtime publication occur once, at the operation that requires them. Subsequent pages do not initialise another Landing project.

The move to Tracking is not an unexplained jump. Both the Test page's closing paragraph and the incremental entrance call it a complete mutable-source variation. It retains parcel identities and the CurrentStatus result, explains why a source constant cannot demonstrate data-only changes, and leaves Landing intact. Direct entrants have a checked snapshot/checkpoint list and earlier setup links. The external archive and notebook verification are explicit rather than silently changing host context.

**Assessment:** no required local flow correction found. The incremental page is substantially longer than its predecessors, but still serves one result: one update, one deletion, a no-op and consumer progress without Build. Length is a preference noted below, not evidence of missing continuity.

### 2. New Warehouse reader

Actual route: [Warehouse](http://127.0.0.1:8846/warehouse/) → [First Table/View](http://127.0.0.1:8846/warehouse/first-project/) → [Tests](http://127.0.0.1:8846/warehouse/tests/) → [Loading changes](http://127.0.0.1:8846/warehouse/incremental/).

The first task begins with the SELECT and the work Weaver generates, not a catalogue schema lesson. StatusEvent feeds CurrentStatus; the independent expected rows do not copy the View's ranking query. The failure exercise restores the same Test, and file mode is offered without pretending it records installed state. Tests explicitly keep the loaded first checkpoint.

The incremental variation states that CurrentStatus changes from a View over StatusEvent to a managed Table over an external Warehouse, uses a separate directory/disposable targets, and forbids carrying the fixed expected-row Test over. This is a legitimate source variation, not a hidden continuation. Source SQL, managed SQL and catalogue queries identify their respective query editors. Direct-entry snapshots link to the provisioning route where required.

**Assessment:** no required local flow correction found. Setup qualifications are visible but relevant; the task does not require Spark publication or semantic-model material. The incremental page's size comes largely from complete runnable SQL and source/target evidence, not unrelated features.

### 3. Experienced PBIP/TMDL author

Actual route: [Semantic models](http://127.0.0.1:8846/semantic-models/) → [Native deployment and foreign-key rule](http://127.0.0.1:8846/semantic-models/native-tmdl/) → [Shared policy](http://127.0.0.1:8846/semantic-models/shared-policy/) → [Custom annotation](http://127.0.0.1:8846/semantic-models/custom-annotations/) → [Managed source](http://127.0.0.1:8846/semantic-models/managed-sources/) → [Validation/reconciliation](http://127.0.0.1:8846/semantic-models/validation/#compare-dax-with-source-sql). I also read the validation page from its top for native/direct-entry readers.

The first task is not merely publishing: it deploys native Import TMDL and adds `Weaver.AutoHideForeignKeys`. It names the many-side Delivery key, leaves Depot visible, explains how to inspect the effective deployed definition and distinguishes field hiding from security. No catalogue, Python handler or Fabric runtime is required. The standalone Power BI qualification is compact and local to setup rather than a competing Home route.

Policy preserves Delivery/Depot, adds native formats/calculation structure and gives a complete local override. The custom page keeps that policy/override, supplies the full trusted Python handler, then exercises a located failure with restoration. Complete standards snapshots support direct entry without claiming that each fixture is the next mandatory download.

Managed sources honestly changes Delivery's partition and configuration, explicitly warns that adding `Weaver.Source` alone does not switch data, and preserves separate source/model Builds. It also says the new snapshot lacks the optional visibility overlay and explains merging that rule with the source annotation. Validation's failure exercises preserve prior overlays, including the absent-overlay case. DAX Assumptions and independent SQL reconciliation remain available; capability is not withheld behind a generic Advanced hub.

**Assessment:** first deployment/annotation requirement is met in the documentation. Later continuity needs R3. The supplied custom → managed route also requires returning to the sidebar; there is no contextual link between those two tasks. This is a bounded editorial preference below, not a claim that custom annotations lacks a valid next task.

### 4. Report maintainer

Actual route: [Reports](http://127.0.0.1:8846/reports/) → [Native Report deployment](http://127.0.0.1:8846/reports/deploy/) → [Development/production bindings](http://127.0.0.1:8846/reports/environments/).

The Report task starts from a complete linked pair, shows native `byPath`, and explicitly does not require completing the model tutorial. It names the deployed Report/model/workspace and the readback IDs to compare. Model refresh/card rendering is separated from Build's deployment result; there is no invented Report Load or Test.

The environment page retains the same native files and any prior overlay. It distinguishes the newly needed production Build from a development Build already completed, uses disposable example workspaces and checks each actual binding rather than matching display names alone. External `byConnection` does not silently become environment-aware. Direct entrants have the same complete pair and local prerequisites.

**Assessment:** no required local flow correction found. The pages remain appropriately short; repeated service permissions are concise qualifications of the new workspace action, not a second modelling tutorial.

### 5. Estate owner

Actual route: [Coordinate your estate](http://127.0.0.1:8846/estate/) → [Connect](http://127.0.0.1:8846/estate/connected-items/) → [Mappings](http://127.0.0.1:8846/estate/environments/) → [Catalogue/Health](http://127.0.0.1:8846/estate/catalogue-and-health/) → [Development](http://127.0.0.1:8846/estate/development-cycle/) → [Operate](http://127.0.0.1:8846/estate/operate/) → [Recover](http://127.0.0.1:8846/estate/recovery/) → [Mirror](http://127.0.0.1:8846/estate/mirror/) → [Select](http://127.0.0.1:8846/estate/selective-runs/) → [Concurrency](http://127.0.0.1:8846/estate/concurrency/) → [Performance](http://127.0.0.1:8846/estate/performance/) → [Automation/deployment](http://127.0.0.1:8846/estate/automation-and-deployment/).

The entrance genuinely serves two items, not only a huge estate. Connection works from known Landing data and names what Dispatch adds. Ordering, unnamed-item boundaries, physical versus managed sources and model/Report differences are explained where they matter. Catalogue/Health introduces questions and actionable state before exact table details. The ordinary development loop appears before optional Mirror; there is no reset ceremony imposed on normal development.

The main checkpoint problem is R2. Explicit disclaimers successfully avoid inventing a combined Landing/StatusEvent/Delivery estate, but the leading examples still move between those checkpoints. The safety improvement is real; the continuity work is not finished.

Operate is more portable: it accepts the current project's configuration, calls out named-file flags and distinguishes installed work from edited source. Recovery gives state-based choices and keeps destructive scope with Reload/Wipe/re-Mirror. The longer recovery page is usable as a decision page with linked exact contracts; its fault-tolerance material does not claim that partial output is automatically correct.

Mirror introduces a necessary, explicitly hypothetical same-workspace source/destination arrangement. Selection deliberately changes to its independent RawEvents/Events/Daily/Summary graph and links the README's preload/oracle; it does not pretend those are renamed StatusEvent objects. Concurrency continues that installed graph and explains invocation versus resource caps. Performance distinguishes work, readiness waits and overhead; the synthetic benchmark is qualified rather than promised. Automation explicitly returns to the managed model snapshot, keeps source/model Builds separate and makes host/bundle boundaries discoverable.

**Assessment:** required estate continuity correction R2. Later optional variations are justified by new tasks and clearly declared; they are not all defects merely because they use different snapshots.

## Editorial preferences, not additional acceptance blockers

- **Model extension handoff:** at [Custom annotations — Related tasks](http://127.0.0.1:8846/semantic-models/custom-annotations/#related-tasks), there are zero contextual managed-source or validation links. The next offered task is composition, which is legitimate. One sentence linking source integration/validation would let the requested policy → custom → managed-source route continue without returning to the sidebar. Do not reorder the approved navigation just to make its global footer mimic every alternative reading route.
- **Footer versus prose:** native deployment's in-body continuation is shared policy, while its footer goes to managed sources. The approved nav order explains the difference. A short “choose the next need” bridge would reduce ambiguity; the existing policy link already provides the correct native-extension route, so I do not count this as a withheld capability.
- **Long pages:** rendered article word counts, including code, are Lakehouse incremental **1,349**, Warehouse incremental **1,104**, model validation **1,201**, recovery **1,315**. The first two mostly earn their length with complete mutable-source demonstrations and exact execution contexts. Validation earns two independently useful branches but needs the entrance selector in R3. Recovery earns its breadth as a state-to-action lookup. Prefer pruning repeated surrounding explanations to splitting them or removing safety evidence.
- **Search ranking on desktop:** `Health` first offers a generated Python result-type signature, and `Spark runtime` first offers Python validation signatures. Their practical owners are present farther down. Improve emphasis/discovery if cheap, but these are relevant substantive pages, not compatibility stubs; ranking alone is not an additional failed technical gate.

## Rendered evidence and checks

Evidence is outside Git at:

`/opt/data/scratch/Fors/weaver-docs-refresh/screenshots/item-first-review/`

- Read **25 task pages**, all five group entrances and Home. Playwright visited the resulting **31 routes at both 1440 × 1000 and 390 × 844: 62 visits**, all HTTP 200, no document-level horizontal overflow and no collected console/page errors during that route scan. Those measurements do **not** establish overlay visibility: R1 demonstrates why that distinction matters.
- Followed **38 actual contextual/footer transitions** across the two viewport sizes. Exercised Home → group → first task through real links for all five entrances on both sizes. Each first task was reached in two clicks; no compulsory Warehouse detour appears in the Lakehouse, model or Report entrance.
- Opened and closed all five mobile drawers. Only the active top-level sidebar group was checked on initial route load; Home had none. The visible menu has the approved item/estate order and no Core/Basics/Advanced or Node-centred top-level taxonomy. Screenshots show legible entrances and controls without overlap; mobile title/footer truncation leaves the in-body first-task links readable. The estate entrance was also visually inspected in dark mode.
- Searched eight terms using actual typing: `foreign keys`, `DAX`, `Mirror`, `ancestors`, `concurrency`, `Warehouse SQL`, `Spark runtime`, `Health`. Desktop results contained each expected practical owner. Matching-document counts were respectively **37, 34, 37, 11, 14, 102, 64, 58**. Mobile populated the DOM too, but its clipped results fail R1. An initial rapid-fill probe retained stale result text and was discarded; the fresh-page keyboard-typing run is the search evidence used here.
- Direct-entry later pages were checked for declared start state, complete snapshot/prerequisite links and truthful fixture boundaries. This is a documentation viability assessment, not execution of those projects on Fabric.

Reproducible browser records/scripts: `browser-evidence.json`, `interaction-evidence.json`, `transition-evidence.json`, `search-visibility-evidence.json`, `review_browser.py`, `review_interactions.py`, `review_transitions.py`, `probe_search.py`.

Representative inspected images: `desktop-home.png`, `mobile-home.png`, the five `desktop-<group>.png` / `mobile-<group>.png` entrances, `mobile-estate-drawer.png`, `mobile-estate-dark.png`, `mobile-model-annotation.png`, `mobile-managed-next-validation.png`, `desktop-search-Health.png`, `mobile-search-Health.png`, `mobile-search-foreign-keys.png`. The `search-repro-390.png` / `search-repro-768.png` failures and `search-diagnostic-no-blur-390.png` / `search-diagnostic-no-blur-768.png` are diagnostic before/after states only, not a committed fix.

## Disposition for the parent

- [ ] R1: restore usable mobile/tablet search and rerun its exact repro.
- [ ] R2: carry one chosen working estate checkpoint/configuration through the leading connect/map/inspect/develop path; retain honest variations.
- [ ] R3: preserve the managed-source state through both validation entrances.
- [ ] Record which preferences are accepted or declined; do not treat them as unbounded rewrite instructions.
- [ ] Have Matthias assess the corrected continuous routes. This report supplies independent findings, not his approval.

**Revision record:** review report only. No recommended public correction has been applied in this branch.

## Parent correction and recheck — 2026-10-14 13:55 AEDT

The original independent findings above remain an honest record of `8a94013`. The parent applied and verified the following corrections; this is **parent disposition**, not a new independent or human approval.

| Finding | Corrected surface | Actual recheck |
|---|---|---|
| R1, clipped mobile/tablet search | Disable header backdrop-filter only at Material's mobile search breakpoint; preserve desktop treatment | Exact new visibility/hit-test regression went RED with output height 10px, then GREEN at 390/768/960/1440, light/dark. Eight real result selections pass; mobile output now 796px at height 844. |
| R2, estate checkpoint jumps | Leading mapping, Health, development and operation continue Landing/Dispatch using workspace-development.yml. Warehouse and managed-model routes are explicit alternatives, not forced restarts. Managed readers keep workspace-dev.yml and its model-inclusive loop. | Two assembled continuous projects pass real Check; 75 Estate bash forms and six configs parse. Parent reread connect→map→inspect→develop→operate with the unchanged Landing/Dispatch checkpoint and inspected corrected desktop/mobile views. |
| R3, managed footer starts inline validation | Visible validation entrance offers managed-source reconciliation before the independent inline Assumption route | Both body and footer entries were exercised; the footer's new branch sends the existing managed model directly to compare-dax-with-source-sql, without setup. |
| Technical review P2, physical Shortcut fragment | routes.json and actual compatibility link now target lakehouse/shortcuts/#expose-an-external-carrier-archive | Actual old-fragment link followed to physical-source explanation at phone/tablet/desktop; rendered route gate and paired crawl pass. |

The focused corrected-page browser run covers 54 route/viewport/theme states, with actual footer and legacy-link interactions; batches were persisted before resuming after timeout. A premature locator count after navigation was corrected to wait for the real destination/heading, not waived. The broad earlier 410 checks remain evidence for the assembled pre-correction layout; the focused run and eight pointer-visible search states prove the changed surfaces. Parent inspected search, mapping, development and validation-chooser screenshots after correction.

Preferences: accepted one contextual custom→managed-source/validation handoff. Retained approved nav order and complete runnable incremental/recovery examples; no speculative split or ranking redesign. Search matches substantive practical owners as well as detailed Reference. Human editorial acceptance remains Matthias's; no new independent review is claimed after these bounded parent corrections.
