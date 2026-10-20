# Public-copy qualification cleanup

Corrective prose-only pass following the review of testing qualifications in the product and documentation previews.

## Scope

- Remove development-wheel/runtime-hash provenance and capture-workspace commentary from tutorial prose.
- State actual prerequisites and recovery actions directly instead of narrating what a particular verification run proved or failed to prove.
- Remove defensive product-page benchmark and key-declaration asides; retain the measured workload/capacity context and actual results.
- Retain real operation limits, destructive warnings and the 18 explicitly requested review TODOs.
- Keep historical capture evidence, release acceptance and publication gates in the existing maintainer records. This pass does not change those records into successful execution evidence.

The pass makes 31 targeted replacements in 22 documentation pages and two product pages (Features and Scale). Documentation starts from `49532ad`; product copy starts from `d1dd0538`. There are no route, navigation, layout, brand, runtime or command changes.

## Preservation

Compared every public source with the before-state inventory. All fenced examples, complete CLI capture blocks, review TODO blocks, embedded scripts and protected generated blocks are unchanged. Separately compared HTML pre/code content and head metadata with the original Git revisions. All 164 capture asset files are byte-identical. Other public source files are unchanged.

## Checks

- Strict MkDocs build: passed.
- Complete-capture renderer: all 51 panels match their retained transcripts.
- Documentation tool tests: 31 passed, one skipped, three subtests passed.
- Product-site checker tests: eight passed.
- Product-site gate: seven canonical routes, four forwarding routes, 34 features and seven benchmark-operation records passed.
- Paired-site crawl: 161 pages; 23,906 local links/assets; 270 cross-site links; no broken links/fragments.
- Served-preview browser pass: all 24 edited pages, 70 desktop/mobile/theme/scripting states passed. Removed qualifications are absent from page bodies and the rebuilt search index. No page-wide overflow or page-script errors.
- Visually inspected the mobile Warehouse tutorial and desktop Features page.

Both private preview roots were refreshed from the checked sources/build. Detailed before-state fingerprints, exact substitutions, preservation results, browser progress and screenshots are retained under `/opt/data/scratch/Fors/weaver-docs-refresh/qualification-audit/`. No Fabric operations or publication occurred in this pass.
