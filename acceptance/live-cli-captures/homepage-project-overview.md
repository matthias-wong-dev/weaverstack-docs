# Homepage project overview verification

Scope: `docs/index.md`, homepage-scoped additions to `docs/assets/stylesheets/extra.css`, and a repeatable offline checker. No navigation, tutorial, capture, Reference or product-site changes.

## Source evidence

Runtime evidence remains `bf908f4754eca4d10a56afd218e9e18d423636d7`.

`tools/check_homepage_project.py --weaver-checkout ../product` invokes the real Parcel initialiser with existing offline service-boundary helpers and network calls refused. It checks every displayed path against the freshly generated project. The tree has 16 lines, including configuration, Environment, Landing, Operations and native Power BI folders.

The checker parses the generated project, projects its installed catalogue with production constructors, compares all five diagram identities and four selected edges, and checks production LoadDag ordering. Shortcut-mediated dependencies are displayed through their real logical Shortcut rather than inventing a dependency on Lakehouse CurrentStatus:

- `Lakehouse/Landing/Files/Parcel.Events` → `Lakehouse/Landing/Tables/Parcel.Event`
- `Lakehouse/Landing/Tables/Parcel.Event` → `Lakehouse/Landing/Tables/Parcel.CurrentStatus`
- `Lakehouse/Landing/Tables/Parcel.Event` → `Warehouse/Operations/Parcel.LakehouseEvent`
- `Warehouse/Operations/Parcel.LakehouseEvent` → `Warehouse/Operations/Parcel.LakehouseCurrentStatus`

Independent Warehouse seed and native Power BI branches are not falsely connected. The tree includes representative files; the DAG shows only this selected branch. These are source/graph checks, not new Fabric execution.

## Build and rendering

- Strict MkDocs build passed.
- Paired-site crawl: 162 HTML pages, 23,317 local links/assets and 276 cross-site links; no broken links/fragments.
- Ruff check and format check passed for the new checker.
- Served-preview browser checks passed in 20 states: 320, 390, 768, 1280 and 1440px; light/dark themes; JavaScript enabled/disabled. No page-wide horizontal overflow or page errors. All tree and diagram content remains available without JavaScript.
- Desktop illustration is approximately 485px tall at 1280/1440px. Mobile stacks the tree and DAG naturally. At 390px every tree line fits; at 320px the tree has local horizontal scrolling, preserving directory indentation without widening the page.
- Reviewed desktop and mobile screenshots in both themes. Diagram labels retain normal opacity rather than inheriting Material's faded `small` style. Long logical names wrap at explicit word boundaries.
- Existing homepage proposition, introductory copy, item links, estate link, Start here link and retained fragment anchors were compared with the prior version after removing the inserted section: byte-for-byte unchanged. Existing CSS is an unchanged prefix; all additions are scoped to the new illustration.
- The 51 existing CLI capture panels still pass their renderer synchronisation check.

## Editorial judgment

One tree answers what is authored and where it belongs; the adjacent small DAG shows a real fork rather than an all-capabilities chain. The new explanation names native file types, explicitly permits starting with one item and links to the two existing detail pages. There is no new tutorial, CLI output, feature inventory, dependency library or interactive control. The ten-second comprehension criterion remains a human editorial judgment, not a timing claim derived from automated tests.

The existing private preview was refreshed from this build. This work does not authorise merging or public publication.

## Follow-up: product restoration and left-to-right bands

The initial layout above was accepted for the developer landing, then revised after Matthias clarified that the restoration also belongs on the main product homepage. Both homepages now use static SVG flowing left to right through vertical Lakehouse, Warehouse, Semantic Model and Report bands. The product homepage restores the syntax-coloured tree and restrained tinted-node aesthetic from its historical `c48b650e` version, without reverting the current homepage copy.

The product diagram is explicitly illustrative and connects the Warehouse branch to a native model and Report. The documentation diagram retains the generated Parcel topology: four verified data edges and the independent inline-data model/Report pair. The checker now also verifies that the model has no managed source references and that the Report binds to that model. No Fabric execution or runtime source changes were required.

Final checks: strict MkDocs build; 23,317 local links/assets and 276 cross-site links with no broken targets; the existing product-site gate; 12 focused renderer/product-gate tests; Ruff check/format; and unchanged capture rendering. A fresh served-preview sweep passed 40 states across both homepages, at 320/390/768/1280/1440px, with JavaScript enabled and disabled. Documentation was checked in light and dark themes. The product site keeps its existing fixed-light theme, also tested under a dark system preference. SVG labels fit inside their bands and nodes, all edges point right, and narrow screens scroll only the diagram region. Desktop and mobile screenshots were inspected after correcting a test-only smooth-scrolling screenshot artefact.

The product change touches only `docs/index.html`, with page-local styling. All prior product-page bytes remain unchanged after removing the two inserted blocks. The docs tree and surrounding homepage copy remain byte-for-byte unchanged; only the diagram, its scoped styling and this verification/checker were revised. The existing product PR #222 and docs PR #3 remain review-only; no merge or public deployment is authorised.

## Review correction: one connected tutorial flow

The docs landing now presents the completed Warehouse → semantic model → Report path, without commentary about the starter model's sample partition. The file browser is a separate, centred card above the DAG card; browser checks verify their common centre and vertical separation. The accepted product illustration is unchanged apart from its exact requested heading: **End-to-end DAG orchestration across Fabric workspace**.

The generated native Parcel model gains a `ParcelStatus` table with `Parcel ID`, `Status` and `Depot` string columns and the same two status rows as the Warehouse example. Delivery, Depot, their relationship and the existing Report remain unchanged. `ParcelStatus` is distinct from the CurrentStatus table generated by the composed source-backed variants, so adding the local sample does not accidentally preserve a sample partition in those variants.

The native tutorial introduces that schema-aligned table, and the managed-source tutorial teaches connecting the same model with `Weaver.Source`, retaining its Report binding. Production binding deliberately retains authored partitions: the tutorial therefore explicitly removes only the sample partition before asking Weaver to generate the source partition. The checker executes this exact transition for both the independent Warehouse View and the connected Lakehouse/Warehouse consumer. It verifies unchanged columns, generated M source navigation, retained modelling policy/Report binding and preservation of other native files. The homepage's Warehouse/model connector represents that completed tutorial step, not a claim that the starter project already contacts the Warehouse.

Verification for this correction:

- New native-sample regression reproduced the missing table before implementation; the focused product run passed **120 tests**, including all named-example selection/extension/compilation cases and project declarations.
- The native-to-managed semantic journey checker passed **15 assembled Check checkpoints**, nine byte-identical fixture blocks and the existing rule/composition/restoration checks. All 16 displayed generated-source blocks still match Initialise.
- The homepage checker passes the sample-to-source transitions for both source paths. No live refresh or DAX/SQL result is claimed; the new same-model Build/refresh step has an exact-point TODO for live capture with an approved Operations connection.
- A development wheel was built and extracted into an isolated package target. Its actual generator produced `ParcelStatus.tmdl` and the corresponding native model reference from the wheel, with the intended schema and local rows. This is package verification, not a published release or service execution.
- Strict MkDocs build and paired links passed: **23,327** local links/assets, 276 cross-site links, no broken targets. Existing product-site gate, **12** renderer/product-gate tests, Ruff and whitespace checks passed. All **51** historical CLI panels remain synchronised; evidence assets were not rewritten.
- A fresh **40-state** served-preview matrix verifies both homepages across five widths, both theme preferences and JavaScript enabled/disabled. The docs were inspected in both actual themes; the product retains fixed-light styling. Checked connected geometry, centred separate cards, no homepage “inline” text, exact product heading, contained SVG labels and local-only scrolling. Representative final screenshots were inspected.

Only bundled example data/model-reference files and their regression test change in product source; the implementation engine and public interfaces are untouched. The prior live-capture runtime remains the provenance of those historical captures. Matching released-package acceptance and live acceptance of the new table/source transition remain separate publication gates.
