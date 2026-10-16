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
