# Supplied Weaver logo and social cards

## Source and use

The supplied `weaver-logo-svg-kit.zip` contains light/dark full logos, light/dark compact icons, and a light/dark preview. Its four original SVG files are retained byte-for-byte in both repositories:

- Product: `docs/assets/brand/`.
- Developer docs: `docs/assets/images/brand/`.

The mark is a wide blue folded-ribbon W; the full lockup stacks it above the outlined lowercase wordmark. No paths, gradients, proportions or original wordmark spacing were changed. The SVGs have no script, external image or font dependency.

Product headers and footers use the supplied compact mark beside the existing name. The dark comparison-table heading uses its dark variant. Material's header and mobile drawer use the appropriate variant for the actual selected theme. Its standard mobile header visibility and controls are preserved; the mark appears in the drawer on narrow screens. Header and drawer rules explicitly preserve the wide SVG aspect ratio rather than inheriting Material's square logo sizing.

Both sites now have the new 128 × 128 PNG favicon. The default 1200 × 630 PNG social cards use the unchanged full stacked lockup, existing “Making Fabric easier to use” proposition, and site domain. The incremental-load social card retains its topic, supporting copy and URL with the same supplied full lockup. Open Graph and Twitter metadata retain matching absolute production URLs, declared PNG dimensions and appropriate alt text.

The product repository's `tools/render_brand_assets.py` exports these assets, with optional exact-byte source copying to this repository. Its `tools/BRAND-ASSETS.md` records regeneration instructions. Playwright is a rendering-tool dependency, not a site or product runtime dependency. Reviewed PNGs are committed assets; deployment must not rerender them.

## Verification

- Parsed all four source SVGs, inspected the supplied identity preview, and visually compared exported lockups with it.
- Verified all four SVGs match the supplied bytes in both repositories. The eight product pages retain every original non-brand byte; all 17 old CSS-drawn marks were replaced, including the comparison heading.
- Exported and inspected the social cards at full size and 600 × 315 thumbnail size; checked full SVG proportions, intact wordmark, legibility and unclipped copy. Verified 1200 × 630 PNG dimensions and 128 × 128 favicon dimensions.
- Passed a **96-state** served-preview matrix: eight product pages and four documentation routes, widths 320/390/1440, JavaScript enabled/disabled, and both actual documentation themes. Verified loaded/undistorted marks, one active theme variant, OG/Twitter correspondence, no page-wide overflow, no local 404s or page errors, working mobile menus and an actual two-way theme toggle.
- Fetched all three served OG assets and both favicons: PNG content types, dimensions and bytes match their canonical local files. This verifies the private preview, not deployment to the public domains.
- Repeated the separate **40-state** two-homepage DAG/layout checks across five widths and both theme preferences. Existing project overview geometry, labels and local scrolling remain intact.
- Strict MkDocs build passed. Paired-site validation checked **23,944** local links/assets and **276** cross-site links across 162 HTML pages with no broken targets. Product-site gate, **12** renderer/product-checker tests, Ruff and whitespace checks passed. All **51** existing CLI panels still match their complete historical transcripts; capture assets were not changed.
- Inspected settled desktop/mobile and light/dark screenshots, including the open mobile drawer. Drawer captures wait for the transition to finish rather than treating an animation frame as final layout.

These are changes to the existing review branches and private previews only. No public deployment or merge is authorised by this verification.
