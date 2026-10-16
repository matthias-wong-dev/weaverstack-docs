# Live CLI capture inventory

Live execution and documentation integration pass: **16 October 2026 (Australia/Canberra)**. The earlier named-example acceptance was offline; this pass additionally exercised the authorised **Weaver Example** disposable Fabric trial workspace. No production workspace, new capacity, tenant settings or new service connections were used.

## Execution provenance

- Runtime revision: `bf908f4754eca4d10a56afd218e9e18d423636d7`, unchanged throughout capture.
- Installed package: built wheel `weaverstack-0.9.0.dev16746776803276843971-py3-none-any.whl`, **not a published PyPI release**.
- Matching development runtime published to the existing Weaver Fabric Environment before Lakehouse Build/Load.
- One continuing additive `parcel` project: Operations, then Landing and its distinct cross-item additions, external incremental sources, then native Power BI. Existing data-source files and bindings retained during model extension. Controlled validation changes were restored.
- Commands, working context, statuses, timing and runtime provenance: [capture manifest](docs/assets/cli-captures/manifest.json). Complete sanitised text and ANSI streams live beside it. [SQL/API readbacks](docs/assets/cli-captures/readbacks.json) are separately labelled observations, not CLI transcripts or UI screenshots. Original raw evidence remains private.

## Coverage and observed outcomes

| Capture | Live result | Integrated owners |
| --- | --- | --- |
| Warehouse Initialise, Check, Build, Load, Test, Health | Complete, captures 10–15. Three seeded event rows and two current-status rows independently queried. | [First Warehouse](docs/warehouse/first-project.md) |
| Warehouse validation failure and restoration | Complete. Deliberate missing/unexpected pair, non-zero Test, Red Health, restored passing Test and Green Health; source-file mode also exercised. | [Warehouse Tests](docs/warehouse/tests.md), [Health](docs/estate/catalogue-and-health.md) |
| Lakehouse Folder → Python Table → Spark SQL, validations and Health | Complete, captures 42–48, including matching runtime publication at 44. Real Spark execution and independent SQL-endpoint row readbacks. | [Python](docs/lakehouse/python.md), [Spark SQL](docs/lakehouse/spark-sql.md), [Tests](docs/lakehouse/tests.md) |
| Warehouse external SQL changes and consumer bookmark | Complete, captures 30–36. Initial insert, source updates becoming target update/delete, unchanged Load and increasing first/changed/no-op bookmarks. | [Warehouse incremental processing](docs/warehouse/incremental.md) |
| Lakehouse external files and consumer bookmark | Complete, captures 70–76. Real DFS source creation/mutation, initial publication, file update/deletion, target upsert/delete, clean `return None` no-op and increasing bookmarks. | [Lakehouse incremental processing](docs/lakehouse/incremental.md) |
| Additive preservation and connected-item execution | Complete with an explicit local Shortcut merge workaround. Cross-item Check/Build/Load succeeded; both Warehouse current-status results matched. | [Connected items](docs/estate/connected-items.md) |
| Health, named previews, ancestors/descendants, concurrency | Complete, captures 50–68. Stale successful Tests were Amber, failed Test was Red, scoped revalidation was Green. Named scopes and dependencies visible; no-match preview refused. Two independent capped Tests started before either completed. | [Health](docs/estate/catalogue-and-health.md), [Operate](docs/estate/operate.md), [Selections](docs/estate/selective-runs.md), [Concurrency](docs/estate/concurrency.md) |
| Native model Build, refresh, DAX and annotation | Complete, captures 80–94. Explicit Catalogue-free configuration used within the same project. Actual DAX returned 2; foreign-key visibility changed only on Delivery; deliberate -1 measure failed, prior overlay restored and Test passed again. | [Native TMDL](docs/semantic-models/native-tmdl.md), [Validation](docs/semantic-models/validation.md) |
| Report binding in development/production configurations | Complete within authorised workspace, captures 100–103. Readbacks verified `Parcel_Report_Dev` → `Parcel_Dev` and `Parcel_Report` → `Parcel`; both models refreshed and returned 2. Both configurations used Weaver Example, not two service workspaces. | [Report deployment](docs/reports/deploy.md), [Report environments](docs/reports/environments.md) |
| Managed-source model and DAX/SQL reconciliation | **Partial:** source Build/Load and model Build/certification succeeded (110–113). Refresh failed (114): no explicit cloud/gateway connection with credentials for Operations. Health (126) records Load Red, Test pending, Build Green. Reconciliation and its discrepancy/restoration sequence were not run against an unrefreshed model. | [Managed sources](docs/semantic-models/managed-sources.md); the successful native validation captures remain in [Validation](docs/semantic-models/validation.md) |
| Mirror plan/reset/result | **Not executed:** no reset/re-mirror destination scope approved. No Mirror, Wipe or reset was attempted. | Existing [Mirror guide](docs/estate/mirror.md) retained unchanged |

Final scoped Lakehouse/Warehouse Test and Health (127–128) passed: four validations, Green Load/Tests/Build, 29 installed objects. The separate managed model remains failed/pending until its connection is supplied. Unrelated pre-existing Catalogue installations were not repaired or removed.

## Disagreements, substitutions and limits

- **Authored Shortcut collision:** extending Operations after its incremental task refused the unowned `Warehouse/Operations/shortcuts.yml` (40). The capture protected that local file, ran extension, then merged its physical Source.Parcel mapping with the generated logical LakehouseEvent mapping before Check/Build (42–43). Existing Table/View bytes and physical bindings were retained. This is a real conservative generator refusal and an explicit workaround, not an unqualified straight-line success or a runtime fix.
- **Health scope:** cross-item Load succeeded while older validations became stale (53). Subsequent Test and scoped Health passed (54, 56). Unscoped Health also exposed unrelated older installations (55); narrowing a report does not repair them.
- **Source mutation context:** the external Lakehouse notebook file operations were executed through the real DFS API; the generated Folder/Table code ran in Fabric Spark. Ordinary SQL endpoint queries supplied independent target readbacks. Notebook UI attachment/cell interaction was not observed.
- **Managed source checkpoint:** the measure and reconciliation Test from the next validation task were authored before batching the managed model Build. The manifest records that context. No result is claimed for the blocked comparison.
- **Capture-harness failures:** initial PTY Initialise required recorded wizard responses; the first unfinished attempt was retained privately. A no-match command entered an interactive retry prompt and was terminated (67); its completed unattended diagnostic is 68. An accidentally appended workspace flag was rejected by Check (88); the documented Check was correct and the corrected capture is 88b. These are not successful tutorial outcomes.
- **Service UI and second-workspace limits:** deployed model definitions, actual query results and Report bindings were read back. Report card rendering, the service field-list UI and cross-workspace access were not observed. No mock service screenshots were created.
- Optional larger branching fixtures, shared-policy/custom-handler/composition walkthroughs and destructive recovery were not separately exercised live in this pass. Their existing offline example gates remain distinct evidence.

## Presentation and verification

Temporary yellow **TODO** markers sit at the specific missing command result, field check or UI action—not in generic page-top warnings. They name the exact output/check still needed, including optional live walkthroughs, destructive scope and released-package acceptance. Remove them before publication. Commands and their following outputs use matching-width terminal boxes; visual shell prompts do not enter copied code, and real output is introduced with “The command returned:” rather than custom visible result headings.

The existing pages now contain **51 authentic output panels across 17 pages**, backed by 81 recorded command attempts and 27 selected SQL/API observations. Attempt totals include deliberate failures and the two qualified harness attempts above; they are not a success count.

`tools/render_cli_captures.py` generates static escaped, selectable HTML from each complete plain-text capture. Shared `.weaver-terminal` CSS adds Weaver status colours, preserved glyphs and keyboard-focusable scrolling within a maximum height of `min(28rem, 60vh)`. Panels show the whole output directly, without summary excerpts, secondary disclosures, transcript footers or raw-file/JSON links. Evidence files and provenance remain available here for maintainers. Rendering needs no JavaScript or external service. Existing navigation, pages and runtime source are unchanged.

Checks and reader review are recorded in [live capture verification](acceptance/live-cli-captures/verification.md); the complete-output presentation follow-up is recorded in [presentation verification](acceptance/live-cli-captures/complete-output-presentation.md). Publication remains held for a matching released-package check and Matthias’s explicit approval. This pass does not authorise merging or public deployment.
