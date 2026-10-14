# Traditional documentation sidebar

User-approved presentation follow-up to item-first delivery. Keep all content, ordering, routes and product links unchanged; remove Material's navigation.tabs feature so the full section tree appears on the left. Default collapsible groups retain the active section expanded, and desktop page headings remain on the right. Narrow screens retain Material's native drawer/drill-down/back controls rather than attempting desktop sidebar clicks through the active panel.

## Actual verification

- Before the one-line configuration fix, the tight browser regression failed on the existing top tabs.
- Locked strict build and preview rebuild passed.
- Full-tree regression: sixteen page/viewport/theme states (native-model and deep CLI entry, 1440/1250/768/390, light/dark), all eight top-level groups, correct active expansion, real cross-section navigation and no page errors. Desktop page TOC remains visible. No-JavaScript cross-section navigation passes on desktop and phone with reduced motion.
- Initial test selector was corrected to click each section's separate disclosure control, not its overview. On mobile the real back controls are used before switching branches; pointer interception was not bypassed. Viewport batches were persisted and resumed after timeout.
- Search pointer visibility/result selections passed at phone/tablet in both themes after the layout change. The extended desktop sweep timed out; no completed eight-state post-layout search claim is made. The prior full search regression remains evidence for the unchanged search CSS.
- Rendered route gate: 114 original pages, 872 captured IDs, 35 canonical owners, no errors. Paired crawl: 161 HTML pages, 23,205 local link/asset checks, 201 cross-site links, zero broken targets/fragments. The reduced count comes from removing repeated tabs, not deleting content.
- Fabric-first story/source guard and whitespace passed. Desktop screenshot inspected: full left tree, Warehouse expanded, right page TOC, no top tabs.

Only mkdocs.yml, maintainer guidance and this evidence record changed. Private preview updated; existing draft PR #3 remains draft, no merge/publication or product/runtime change.
