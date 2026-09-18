# Internal documentation coverage map

This maintainer-only ledger maps the accepted five-section site to the staged migration. It lives outside `docs/` and is not rendered. A target path or owner records intent; it does not mean the page has received its later editorial or source-verification pass.

## Phase 1 checkpoint

Phase 1 establishes navigation and ownership. At this checkpoint:

- public ownership is **Getting started / Core concepts / Basics / Advanced / Reference**;
- Guides, Contracts and Contributing are no longer target top-level sections;
- contribution guidance is owned by root-level `CONTRIBUTING.md`, `AGENTS.md` and `PROSE.md`;
- Notebook and Capacity are CLI Reference topics, not Advanced topics;
- target paths may contain moved, split or placeholder material inherited from the old structure;
- substantive reframing, exhaustive Reference work, cross-link reconciliation and editorial calibration remain for Phases 2–6.

Do not mark a topic complete because its navigation entry or destination file exists. Completion requires the content work and verification assigned to its later phase.

## Section ownership and remaining work

| Section | Owns | Phase 1 state | Remaining work |
| --- | --- | --- | --- |
| Getting started | Installation and the shortest first-project lifecycle | Target ownership established; existing material is migration input. | Phase 2: restrict prerequisites, simplify the first project and verify the complete path independently. |
| Core concepts | The public mental model | Target ownership and planned splits established. | Phase 2: refactor operations; add State and health, Mirrors, and Sessions and workflows; move the practical development cycle; reframe Dependencies. |
| Basics | Normal authoring, development and operation | Receives former task-oriented Guides material. Moves do not establish final examples or routes. | Phase 3: split Lakehouse paths, simplify workflows and validation, create the development cycle, and apply defaults/inference-first examples. |
| Advanced | Deeper mechanisms and non-basic operating patterns | Receives selected Guide and Contract explanations; Notebook and Capacity are excluded. | Phase 4: reframe change detection, incrementality, history, schema, partial failure, mirroring, bundles and automation. |
| Reference | Exact documents, APIs, CLI, configuration, schemas, formats and operation behaviour | Existing reference and contract material has a target owner; generated CLI and Python reference remain authoritative only for their generated facts. | Phase 5: build exhaustive Weaver-document and configuration reference, redistribute operation contracts, and retire legacy Contracts only after every rule has a verified owner. |

## Migration ledger

| Legacy material | Target owner | Editorial status after Phase 1 |
| --- | --- | --- |
| `get-started/*` | Getting started | Retained for Phase 2 simplification. |
| Core overview, projects, logical/physical items, documents and catalogue | Core concepts | Retained; later passes separate concepts from exact syntax. |
| Weaver operations | Core concepts / Build, Load and Test | Rename and refactor remain in Phase 2. |
| Core development cycle | Core concepts / Mirrors plus Basics / The development cycle | Split and substantive rewrite remain in Phases 2–3. |
| Core dependencies and fault tolerance | Core concepts, with exact rules in Reference | Concept reframing remains; exact rules must be reconciled in Phase 5. |
| Task-oriented `guides/*` | Mostly Basics | Re-homing does not validate commands, examples or reader routes. Phase 3 owns that work. |
| Incremental loads, automation and bundle promotion | Advanced | Mechanism reframing remains in Phase 4. |
| Specialised estate mirroring | Advanced | Retained for Phase 4 reframing. |
| Notebook and Capacity explanations | Reference / CLI | Removed from Advanced ownership; no broader conceptual page is planned. |
| Explanatory Contract material | Core concepts or Advanced | Must be merged without duplicating the exact rule. |
| Exact Contract behaviour | Reference / Operation behaviour or Weaver documents | Redistribution and source verification remain in Phase 5. |
| Existing `reference/*` | Reference | Retained, then reorganised and checked for exhaustive ownership in Phase 5. |
| `contributing/*` | Root maintainer documentation | Useful guidance has a root owner; rendered copies are structural migration material and must not be treated as the canonical instructions. |

## Reference coverage still required

Phase 1 does not establish exhaustive reference coverage. Phase 5 must verify these surfaces against current source and tests:

- every Weaver document kind, location, identity rule, supported language and metadata key;
- defaults, accepted values, conditional requirements and incompatible combinations;
- dependency inference and override behaviour, including the current Spark SQL requirement;
- required Python methods and accepted return forms;
- configuration keys, discovery, precedence and restrictions;
- Build, Load, Test, Health, Mirror, Wipe, Workflow and Session selection, ordering, state changes, outcomes and failure boundaries;
- catalogue schema, build-bundle representation and machine-readable command output;
- generated CLI leaves and public names exported by `weaver.__all__`.

The generated CLI and Python checks prove assignment and generated-block consistency for a selected source checkout. They do not verify authored explanation, behavioural completeness or compatibility policy.

## Cross-cutting integration work

Phase 6 still owns:

- stale links and vocabulary left by moves and splits;
- section landing pages and complete reader routes;
- duplication between concept, task, mechanism and reference pages;
- syntax contrast and code/table rendering in both themes;
- header labels and presentation alignment;
- checked example validation against current Weaver;
- strict builds, internal-link checks, responsive inspection and whole-site editorial calibration.

## Explicitly withheld claims

Until the product specifies and tests them, the site must not claim:

- compatibility guarantees for bundle or catalogue formats beyond documented current behaviour;
- stability for internal Python modules;
- a complete compatibility contract for every authored metadata key;
- a universal authentication prerequisite beyond the implemented credential chain;
- that every Fabric workspace exposes every Doctor probe;
- that an Environment is required for Warehouse-only work;
- that workflow files are a general orchestration language;
- stable `--json` schemas where no versioned format contract exists;
- that source design documents are themselves a supported public API.

Record exact current behaviour in Reference when useful, but do not convert observation into a guarantee.
