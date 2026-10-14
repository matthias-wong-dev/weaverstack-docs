# Final editorial revision — scope and first integration

## Frozen scope

Reviewed starting heads: product `47ff689a04b1b867eb09888d51dbbc0db7448e15`; documentation `a7b23a0246e19bb0eaf0f70ce3ec4b331b9408de`. Both exact remote heads were read again before the final integration commits; PRs remain open drafts on the existing branches with base `main`.

This revision changes product copy, task progression, editorial rules and verification, not runtime behaviour or the item-first architecture. The approved homepage headline, four-feature menu, standalone scale route, full left navigation/right TOC and exhaustive Reference remain. Getting started now links directly to the existing Warehouse task; its forwarding route and fragments remain search-excluded compatibility pointers.

Public copy assumes the intended matching PyPI release and normal installation. Matching-wheel acceptance, public release and live Fabric/Power BI acceptance remain separate, unclaimed gates.

## Principal decisions

- Product pages lead with the engineering burden removed, a credible example and a first task; home states the proposition and Features helps choose the task.
- Scale follows 3 → 30 → 300 → 3,000 and preserves the synthetic F64 evidence. Later measured incremental loads are about 13 minutes; the first incremental day was about 19 minutes. Row insertions across processing layers are not distinct source records or an SLA. Machine attributes bind displayed rounded statistics to the unchanged measured data.
- Warehouse setup allows normal browser sign-in; generated configuration is optional reading. One passing Test is ordinary; failure/recovery is optional.
- Native models first select `SemanticModel/Parcel`, confirmed through real `_item_bindings`; `PowerBI/Parcel` selects both model and Report. Model-rule/policy/custom tasks remain model-only. Report deployment separately selects `Report/Parcel` after the model and verifies binding.
- Built-in foreign-key hiding precedes policy/custom/composition. A passing DAX Assumption precedes optional failure/backup/restoration; the exercise preserves prior overlay state. The managed-source SQL comparison stays a separate natural continuation.
- Estate pages retain Landing → Dispatch and active configuration, lead with operational questions, show dry-run named selection before ancestors/descendants and total concurrency before resource tuning.
- Environment publication prose agrees with the actual CLI: human summary normally, JSON with `--json`. Generated blocks were not hand-edited.
- Reference, source fixture bytes, configuration contracts, incrementals, destructive boundaries and Report Build-only semantics remain intact. Tests protect behaviour and provenance, not approved incidental prose or code-block position.

## Fresh first-integration evidence

- Strict MkDocs build; route/fragment retention, paired-site crawl, product-site checker and Fabric-first/nav/story checks passed.
- Four deterministic generators passed: 18 leaf CLI commands, 55 Python exports, four supported extension classes and 23 catalogue table declarations. Generator tests: 16 passed; route self-tests: 12 passed. These are separate suites, not summed with product tests.
- Reference examples: 103 commands, six configurations, four operation calls, two DAX files and one native edit checked against the pinned source.
- Six maintained projects passed parser/compiler/config/selection/concurrency/native-hash gates; 56 README commands parsed. Journey gate passed 15 pages, 81 commands, ten configurations, three Python calls and 12 byte-identical fixture blocks.
- Lakehouse assembled projects, Warehouse five-state SQL checkpoints, semantic overlay/Assumption/composition and Report native schema/binding gates passed. The semantic checker was corrected to locate the foreign-key rule by behaviour, not its old last-code-block position.
- Fresh responsive sweep passed 132 route/width/theme states, with real direct navigation into the Warehouse task, model-only first Build and passing DAX/optional disclosure checks; no page errors or document overflow. Parent inspected opening screenshots on phone/desktop/light/dark.
- An attempted broader pytest invocation collected no tests because one guessed filename did not exist; it supplies no evidence. Discover and rerun the exact selected file set before final delivery. The earlier 69-test source-sensitive run is recorded separately, not added to a later overlapping suite.

The authorised fresh independent reviewer has not yet reviewed this first-integration snapshot. Final exact-head checks and reviewer dispositions will be appended separately without rewriting their findings.

All browser artifacts and executable QA scripts remain outside the repositories under `/opt/data/scratch/Fors/weaver-docs-refresh/`. No remote service, package release, merge or publication is claimed.
