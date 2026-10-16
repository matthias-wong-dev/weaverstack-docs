# Weaver: final independent editorial review

## Judgment

**Four reader routes are coherent; the estate route is not yet a continuous Landing/Dispatch journey through selection and concurrency.** I would not call the entire requested reader acceptance complete until the owner dispositions that continuity defect. I found no blocking rendered-navigation or code-readability defect in the selected desktop/phone states. There are smaller search-findability, footer-contrast and editorial defects below, plus an unresolved copy-verification gap. This is independent editorial/browser review, not live Fabric acceptance or human approval.

No website, product source, fixture or Git changes were authored. All review artifacts are outside Git.

## Reviewed boundary and evidence

- Product snapshot: `/opt/data/scratch/Fors/weaver-docs-refresh/product`, HEAD **`37180e10426f392dc3f220b9a3692547d8f20a76`**.
- Developer snapshot: `/opt/data/scratch/Fors/weaver-docs-refresh/journeys`, HEAD **`737f4462687ec61b2453e9194e0809c7035dcafb`**.
- Behaviour pin: **`74b4d15ee65ed2740593af1f4d459771b801b132`**. My `git diff` of product `src/` and `tests/` against that pin returned no changes. Both snapshots were clean at initial inspection.
- Browser: existing Playwright and Chrome headless shell 141.0.7390.54. Rendered product at `http://127.0.0.1:8847/`; developer at `http://127.0.0.1:8846/`.
- Layouts: **1440 × 1000** and **390 × 844**, light and dark system preferences. Developer actually rendered `default` and `slate` themes. Product remained its light design under both system preferences; a separate product dark appearance was therefore **not** verified.
- Independently collected **40 selected page/layout states**, **30 continuous link clicks**, and **12 successful search-result hit-tests/clicks**. These are selected telling states, not a repetition of the parent's full sweep. Cross-site preview URLs were substituted locally in browser DOM only; original and substituted URLs are recorded.
- A read-only parser probe imported Weaver from the pinned checkout and accepted **62 distinct rendered command forms**, with no parser failures. No operation handler ran. **12 complete Warehouse/Lakehouse authored documents**, including the Warehouse failure example and mutable-source Folder/Table, matched checked-in fixtures after trimming surrounding whitespace. This is command/document shape evidence, not remote execution.
- Public installation was reviewed as prospective copy for the intended matching PyPI release. Matching wheel availability, installation from PyPI and hosted runtime admission remain unclaimed. No package was installed/released and no Fabric/Power BI service, capacity, setting or resource was touched.

Primary evidence directory: `/opt/data/scratch/Fors/weaver-docs-refresh/screenshots/final-editorial-review/`.

## Findings requiring owner disposition

### F1 — Acceptance defect: estate continuity breaks at selective runs

**Location:** `http://127.0.0.1:8846/estate/selective-runs/`, opening context and first command; carried into `/estate/concurrency/`.

The preceding route has Landing's `Parcel.Events → Parcel.Event → Parcel.CurrentStatus`, a Dispatch Shortcut View, and an active `workspace-development.yml`. Connection, mappings and Health preserve that checkpoint.[12][13][14] Selective runs instead opens with **“Use the parcel-load-selection project from the documentation repository”**, asks the reader to **“Build and Load that project”**, and moves to `Warehouse/Operations`, `Warehouse/Reporting`, `Parcel.RawEvents → Parcel.Events → Parcel.Daily → Parcel.Summary`, and `workspace-dev.yml`.[15] Concurrency then says **“Continue with the installed workload from selective runs”** and caps Operations rather than the reader's Landing/Dispatch work.[16]

The new fixture is clearly labelled and technically useful. Its README supplies provisioning, preload and omitted-producer conditions. The defect is not invalid selector syntax: it is that the mandated continuing reader must provision/install a second estate to discover named selection and the simple invocation cap. Landing naming appears only near the end, explicitly labelled **“not a command for the Warehouse-only fixture”**.[15]

**Required outcome for disposition:** keep a leading named dry-run, expansion and concurrency-2 checkpoint runnable against the working Landing configuration. The larger Warehouse branching graph can remain an explicitly optional depth example. This is a continuity correction within the existing architecture, not a redesign.

**Evidence:** `estate.json`, `depth.json`, `continuous-links-and-accessibility.json`; fixture `journeys/examples/parcel-load-selection/README.md`, especially its provisioning/preload sections. I followed connected items → mappings → Health → selective runs → concurrency by actual links.

### F2 — Nonblocking search defect: the first annotation's short identifier is not findable

At `http://127.0.0.1:8846/`, typing **`AutoHideForeignKeys`** through the visible search field returned **“No matching documents”** in all four width/theme combinations, despite the annotation being central to the native-model task.[9] This was reproduced with sequential keyboard input and settled search, not inferred from a static index.

`bookmark`, `Report binding` and `concurrency` all returned relevant results that were visible, hit-testable and actually navigable. Thus this is identifier findability, not a broken search overlay. I did **not** test the fully qualified identifier or alternative natural-language query before the bounded stopping instruction; those are explicit gaps, not presumed failures.

**Evidence:** `interactive-complete.json`; `1440-light-search-AutoHideForeignKeys-no-result.png`, `390-dark-search-AutoHideForeignKeys-no-result.png`. Retain a searchable short-name entry or alias if identifier lookup is part of acceptance.

### F3 — Nonblocking accessibility defect: developer light footer attribution is nearly invisible

On the reviewed developer pages, the **“Material for MkDocs”** footer link has computed foreground `rgba(255, 255, 255, 0.7)` against `rgb(236, 236, 234)`, giving **1.13:1** composited contrast at 12.8 px. The light desktop home screenshot visibly confirms it. This does not obstruct tutorial content or previous/next navigation, but is a real link-contrast defect, not a preference.

**Evidence:** `initial-0.png`, `computed-summary.json`, `interactive-complete.json`. The sampled code-token measurements did not produce an equivalent below-4.5:1 issue.

### F4 — Small editorial defects, not acceptance blockers

- `/estate/concurrency/` says **“Source/file-mode Tests are serial by default by default.”** Remove the duplicate wording when convenient.[16]
- `/reference/catalogue-schema/`, `_.LoadStatistic` → `Is reload`, says **“False until reload is available.”** That future-looking gloss is inconsistent with the current tutorial/reference treating `--reload` as available. The parser accepts that flag. I have not verified the statistic writer's actual value; the owner should resolve the gloss against implementation rather than infer that it must be true on every reload.[28][15]

## Five continuous reader outcomes

All service outcomes in this section are **expected reader checks**, not results I executed.

### 1. Installation → Warehouse first project → Tests

**Reader-flow outcome: pass.** Installation uses normal pip installation and version inspection; interactive sign-in is the default, with unattended execution deferred.[1] The task initialises an empty ordinary project, uses SQL Table and View documents, explains declining unnecessary Spark Environment publication, and gives scoped Check/Build/Load/Health commands.[2]

The first useful result is explicit: three event rows yield two current-status rows, `P-1001 / In transit / Central` and `P-1002 / Delivered / South`. The tutorial explains the generated loading procedure, inferred SQL dependency and operational recording only after showing the query result.[2] The next page retains that project and runs the independently authored expected-result Test **before** adding the Assumption or exposing the optional deliberate failure.[3]

Expected first quality checkpoint: `Parcel.CurrentStatusMatches` passes with zero missing/unexpected rows. The optional failure disclosure opens and closes, includes the complete wrong expected query, names the discrepancy, restores the passing file and distinguishes file-mode results from persisted status. I opened and read it. The two validation stages repeat a command sequence intentionally; neither requires another Initialise. Further discovery into loading changes and exact Test behaviour is worthwhile rather than a conceptual admission gate.[3]

**Command/fixture assessment:** relevant command forms parse against the pin; five complete SQL blocks, including the failure variant, match their fixtures. Remote provisioning, T-SQL execution and the passing Test were not run.

### 2. Installation → Python Lakehouse → runtime as needed → Spark SQL → validation → incremental

**Reader-flow outcome: pass, with an explicitly separate advanced variation.** The Python task starts with a Folder staging a known three-event CSV and a Table importing that Folder. It publishes the matching Fabric Environment **before first remote Build**, rather than incorrectly treating a Build that does not call `read()` as runtime-free.[4][5]

Expected first useful result: one managed CSV followed by three queryable event rows. The next Spark SQL page preserves the Folder/Event and adds CurrentStatus with explicit `Dependencies`, then shows the two expected parcel statuses.[6] Validation retains the same loaded Tables and runtime, tests independent expected rows and recognised statuses, and distinguishes installed from file-mode recording.[7]

Incremental is honestly labelled a complete **Tracking mutable-source variation**, not an unexplained mutation of the constant Landing feed. It leaves Landing intact, supplies source upload/visibility checks, an external ownership boundary, a physical Shortcut, consumer-owned bookmark and explicit delete keys. Its second run changes source files without Build; the reader should observe a changed P-1001 and deleted P-1002, followed by a clean no-op advancing the consumer boundary.[8] This additional setup is justified by the move from deterministic inline bytes to externally changing data, unlike F1's replacement of the leading coordination checkpoint.

**Command/fixture assessment:** the relevant rendered commands parse; Folder/Event/Spark SQL/validation blocks and the mutable-source Folder/Table match fixtures. Complete Table Reference supplies accepted returns, metadata, incompatible combinations and lifecycle effects.[26] Spark execution, runtime publication, SQL-endpoint visibility and incremental results were not run.

### 3. Power BI-only → native model → AutoHideForeignKeys → Report → environments

**Reader-flow outcome: pass; search caveat F2.** The model route uses inline Import data in an existing standalone Power BI workspace, explicitly needs no Warehouse/catalogue and warns **not** to run Initialise. Its first Build selects **`SemanticModel/Parcel` alone**; the Report stays local.[9]

Expected first useful result: deployed/refreshed Parcel_Dev with Delivery Count 2. The first built-in annotation is one same-name overlay, `Weaver.AutoHideForeignKeys = true`. Its checkpoint is specific: Delivery[DepotId] becomes hidden, Depot[DepotId] remains visible, and partitions/relationship remain. The optional native-relationship disclosure opens and explains the many side. The tutorial makes native-file preservation, Desktop's nonexecution of annotations and the false/no-op boundary clear.[9]

The Report page retains the existing project/overlay. It explains why catalogue-free deployment selects **the linked pair** with `PowerBI/Parcel`, even after the earlier model-only deployment. This is a real same-Build requirement, not unnecessary reauthoring. It verifies binding with `datasetId` **and** `datasetWorkspaceId`, then separates refresh/card viewing from Report deployment.[10][29]

The environment page preserves source/overlay, selects two configuration files and requires the production-labelled Report to point to its own model/workspace, not development. Both workspaces are disposable. There is no fabricated Report Load/Test.[11] Shared policy, composition, validation and exact binding Reference provide worthwhile next tasks; the task and Reference retain the catalogue-backed Report-only alternative without making it the starter.[9][29]

**Command/fixture assessment:** model-only and linked-pair commands parse. I read the native fixture's Delivery measure/inline rows and its standalone provisioning README. Service deployment, definition transformation, refresh, binding readback and card rendering were not executed.

### 4. Connected items → Catalogue/Health → selective runs → concurrency

**Reader-flow outcome: partial; F1 prevents an unqualified continuous-route pass.** Connection begins with existing Landing, adds Dispatch, preserves configuration/runtime and gives a concrete SQL query expected to expose the same three events. It states the no-Load boundary of a Warehouse Shortcut View and the difference between ordering selected items and selecting unnamed dependencies.[12]

I followed the actual intermediate mappings hand-off before Health. It saves the current bindings as `workspace-development.yml` and explicitly selects that file thereafter. Health preserves the mapped estate and asks for no redundant Load/Test. Its question-led catalogue entries distinguish installation, current status, bookmarks and history.[13][14] Direct entry from the connection page without mappings requires retaining the current working configuration, as Health's alternative-entry paragraph allows; I do not call the extra mapping hand-off a defect.

Selective runs has good **local pedagogy**: named dry-run first, then ancestors/descendants, union-from-original-seeds, omitted Depot prerequisite, explicit cross-item boundary, no-match refusal and destructive Reload warning. Concurrency leads with **2**, then separates an invocation cap from persistent resource limits and Spark compute.[15][16] Those explanations are technically consistent with the pinned parser and exact selection Reference.[27] The failure is the replacement estate/configuration at their leading runnable checkpoint, not the concepts themselves.

Mirror remains optional. Its page puts reconstruction of the **destination catalogue and selected targets** before the command and distinguishes the settled confirmation plan, lack of dry-run and nonrollback after mutation. Reload's warning is visible alongside selection, including enlarged destructive scope and no automatic restoration. Neither was run.

### 5. Product home → Features/four feature pages → scale → mechanism/comparison → deep Reference

**Reader-flow outcome: pass.** The homepage retains exact H1 **“Making Fabric easier to use”**, leads with familiar Python/SQL/native files and presents Lakehouse → Warehouse → semantic model → Reports rather than a competing Power BI product route.[17] Features has four distinct destinations, not four copies of the same promise.[18]

- Lakehouse removes surrounding file/Table orchestration and demonstrates the import dependency.[19]
- Warehouse removes hand-built load procedures with an ordinary SELECT and declaration, then adds independent validation.[20]
- Semantic models begins with native deployment, then a concrete annotation, DAX checking and optional managed sources.[21]
- Reports uses environment configuration and actual model/workspace binding, keeping refresh with the model.[22]

Scale starts useful at **3**, then **30/300/3,000**. It names synthetic F64 provenance, about an hour first Load, about 13 minutes later incremental loads **with the first incremental day around 19 minutes**, and row insertions across layers rather than distinct records. It explicitly disclaims an arbitrary-workload SLA.[23]

How-it-works explains logical mappings, separate source/model Build calls, installed Load/Test and freshness. It also distinguishes Python/T-SQL inference from explicit Spark SQL dependencies.[24] The dbt page gives dbt a legitimate transformation role, uses partial marks where appropriate, acknowledges its Power BI Semantic Layer connector and distinguishes it from native model/Report/DAX lifecycle.[25] I retrieved its cited dbt Power BI and Fabric adapter documentation. The connector's live-query purpose agrees with the comparison.[30] The adapter documentation supports the separate configuration surfaces and within-Warehouse clone distinction.[31][32] I did not independently audit every comparison-table cell.

Actual deep hand-offs reached Report-binding Reference, including its service-readback and catalogue-free selection boundaries.[29] They also reached Table return-contract Reference, operation-selection Reference, workspace configuration and catalogue schema. These contain consequential constraints, accepted forms, defaults, ownership and failure/state boundaries rather than merely a second overview.[26][27][28] No redesign is warranted.

## Rendered usability and remaining gaps

- **Navigation:** desktop item-first collapsible left tree and right TOC remain; current groups expand. I navigated Warehouse → Reports using the tree and the mobile drawer/back controls. Product Features overview is a real link with a separate disclosure. Its four children remained navigable without JavaScript; developer mobile cross-section navigation also worked without JavaScript with reduced motion.
- **Search:** bookmark, Report binding and concurrency each passed visible-bounds, `elementFromPoint` and actual click checks at both widths/themes. Phone output measured 390 × 796 below the 48 px search form; it was not clipped to the header. Result destinations were incremental Lakehouse, Report environments and concurrency respectively. F2 is the separate identifier miss.
- **Code and tables:** sampled SQL/Python/metadata/string/class tokens were readable in developer light/dark. At 390 px, Python code's local scroller measured 388 px viewport / 681 px content and moved to scrollLeft 100; Report environment table scroller measured 390 / 672 and moved to 100. No body horizontal overflow occurred in the 40 recorded states. This is not a whole-site contrast certification.
- **Optional details:** generated bindings, Warehouse failure/restore and native relationship disclosures were exercised. Required runtime/destructive warnings were visible outside optional disclosures.
- **Keyboard/theme:** developer dark choice persisted across a navigation. Escape closed search; observed focus then returned to body, not a specifically verified trigger. The skip link was the first Tab stop and Enter reached its content fragment. A full keyboard focus-order audit was not performed.
- **Copy gap:** code-copy controls were clicked, but the harness compared clipboard content with `innerText` and reported inequality. Rendered code has line wrappers/extra extracted newlines; raw-text equality and asynchronous clipboard settling were not rechecked before the stopping instruction. Therefore **correct copied bytes are unverified**, and this is not promoted to a confirmed copy corruption defect. See `continuous-links-and-accessibility.json`.
- **Scope gaps:** full product dark rendering (no alternate appearance observed), fully qualified/natural-language annotation search, every Reference page/interface, every dbt cell, exhaustive broken-link/fragment crawl, nonselected route/layout combinations, real wheel onboarding and all live tenant outcomes. Three guessed exploratory URLs returned 404 (`/lakehouse/validation/`, `/semantic-models/annotations/`, `/estate/workspace-mappings/`); the real site links led to `/lakehouse/tests/`, the inline native annotation task, and `/estate/environments/`. Those guesses are **not site broken-link findings**.
- Initial harness attempts hit a lazy-search initialization timing issue, a theme already selected by system preference, ambiguous mobile search selectors and a no-JS animation-stability timeout. These were isolated and the affected core interactions rerun with appropriate selectors/input/reduced motion. They are not counted as site defects. The completed four-context interaction batches recorded no console/page errors.

## Evidence index

All paths below are under `/opt/data/scratch/Fors/weaver-docs-refresh/screenshots/final-editorial-review/`:

- `warehouse.json`, `lakehouse.json`, `powerbi.json`, `estate.json`, `product.json`, `followups.json`, `depth.json`: rendered text, literal code and links, not just Markdown source.
- `interactive-complete.json`, `computed-summary.json`: deduplicated viewport/theme states, dimensions, search hit-tests/destinations and sampled colours.
- `continuous-links-and-accessibility.json`: continuous links, original preview substitutions, disclosures, local scrollers, copy caveat, no-JS and keyboard checks.
- `source-shape-checks.json`: checkout import, parsed commands and 12 literal fixture matches.
- `initial-0.png`, `initial-1.png`: desktop developer/product home.
- `1440-dark-warehouse-first-project-code.png`, `390-dark-python-metadata.png`: desktop and phone code states.
- `390-light-search-Report-binding.png`, `390-dark-search-bookmark.png`: usable visible mobile search.
- `390-light-vs-dbt-top.png`, `390-dark-home-top.png`: product phone comparison/home; the latter records the fixed light product appearance under dark preference.

**Handoff:** disposition F1 first. F2–F4 are bounded polish/reference findings. Correct copying needs a focused verification if included in the delivery gate. No live-result or publication gate should be represented as completed by this review.

## Sources

[1] http://127.0.0.1:8846/getting-started/installation
[2] http://127.0.0.1:8846/warehouse/first-project
[3] http://127.0.0.1:8846/warehouse/tests
[4] http://127.0.0.1:8846/lakehouse/python
[5] http://127.0.0.1:8846/lakehouse/runtime
[6] http://127.0.0.1:8846/lakehouse/spark-sql
[7] http://127.0.0.1:8846/lakehouse/tests
[8] http://127.0.0.1:8846/lakehouse/incremental
[9] http://127.0.0.1:8846/semantic-models/native-tmdl
[10] http://127.0.0.1:8846/reports/deploy
[11] http://127.0.0.1:8846/reports/environments
[12] http://127.0.0.1:8846/estate/connected-items
[13] http://127.0.0.1:8846/estate/environments
[14] http://127.0.0.1:8846/estate/catalogue-and-health
[15] http://127.0.0.1:8846/estate/selective-runs
[16] http://127.0.0.1:8846/estate/concurrency
[17] http://127.0.0.1:8847
[18] http://127.0.0.1:8847/features
[19] http://127.0.0.1:8847/lakehouse
[20] http://127.0.0.1:8847/warehouse
[21] http://127.0.0.1:8847/semantic-models
[22] http://127.0.0.1:8847/reports
[23] http://127.0.0.1:8847/scale
[24] http://127.0.0.1:8847/how-it-works
[25] http://127.0.0.1:8847/vs-dbt
[26] http://127.0.0.1:8846/reference/weaver-documents/table
[27] http://127.0.0.1:8846/reference/operation-behaviour/shared-selection-and-identity
[28] http://127.0.0.1:8846/reference/catalogue-schema
[29] http://127.0.0.1:8846/reference/power-bi/requirements-and-compatibility
[30] https://docs.getdbt.com/docs/platform-integrations/semantic-layer/power-bi
[31] https://docs.getdbt.com/reference/resource-configs/fabric-configs
[32] https://docs.getdbt.com/reference/resource-configs/fabricspark-configs


## Owner dispositions after the independent review

The findings above are preserved against the reviewer's exact original heads. Fors made the following corrections afterward; these are parent verification, not a claim that the independent reviewer reapproved the revised head.

- **F1 corrected:** the leading selective Load task now uses the working Landing/Dispatch source and `workspace-development.yml`. Named dry-run first; real ancestors select Folder Events → Event; real descendants select Event → CurrentStatus. The execution and concurrency-2 tasks keep that estate/configuration. The branching Operations/Reporting example and every consequential dependency rule remain optional depth. New maintained `tools/check_estate_examples.py` parses all estate commands/configs, checks the coherent source and proves all three selected sets with production `LoadDag` over its installed catalogue projection. No fabricated service results.
- **F2 corrected:** the native task has a searchable short-name heading `AutoHideForeignKeys`, while retaining the old foreign-key heading fragment explicitly. The exact identifier was searched, hit-tested and clicked to the task on phone/desktop/light/dark.
- **F3 corrected:** Material's `html .md-footer-meta.md-typeset a` selector outranked the earlier footer rule. The scoped override now wins. Measured attribution contrast is 6.33:1 light and 8.37:1 dark in the four correction contexts. The copy notification was also given readable existing code-palette colours after parent screenshot inspection.
- **F4 corrected:** duplicate `by default` removed. The actual `RunRecord.reset/settled` writer records whether an object was reset for a reload, including failed attempts. Catalogue rendering now uses that source-verified meaning rather than the stale declaration comment. The source inventory remains untouched; the generated table was regenerated, not hand-edited. A generator regression was observed red, then green. The stale product-source description remains a separate product-maintenance follow-up; no runtime source was modified.
- **Copy gap closed for the introductory samples:** compare clipboard text with the exact authored fence via `textContent`, not `innerText`'s rendered line layout, and wait for the asynchronous clipboard update. All 18 visible blocks across Warehouse first task, Python Lakehouse and native-model task copied byte-for-byte apart from terminal newlines in each of four phone/desktop/light/dark contexts. Collapsed optional blocks and every site block are not claimed by this sample.

Parent correction evidence: `/opt/data/scratch/Fors/weaver-docs-refresh/final-editorial-correction-results.json` and `screenshots/final-editorial-corrections/`. The product retains its existing fixed light design under dark system preference; developer documentation has actual light and dark themes. No new product dark-mode design is implied.

No remaining verified acceptance defect from this review is left unresolved. Service, matching-wheel, release/publication and independent peer-access gates remain unclaimed.
