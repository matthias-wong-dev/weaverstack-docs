# Item-first routes, retention and example checkpoints

## Frozen evidence and scope

Docs starting head: `1f5220f17e8f698ebafc6bf4bab8b297dc1797b0`; product starting head: `942f3798fdbc534375b45ee0a7af0aaa7b4773fe`. Behaviour/interfaces: `74b4d15ee65ed2740593af1f4d459771b801b132`; runtime/test/configuration/workflow trees compared equal before edits. Existing draft PRs remain the delivery vehicle; no runtime, release or service mutation.

The approved item-first plan supersedes the earlier visible Core/Basics/Advanced taxonomy, not technical behaviour. Parent owns nav, entrances, shared guidance, migration and acceptance. Four approved sequential two-agent pairs: Lakehouse/Warehouse; models/Reports; estate/reference-link audit; independent reader/technical retention reviews. Children commit only isolated branches; parent integrates and verifies.

## Canonical task destinations

- `docs/lakehouse/index.md` → `/lakehouse/`
- `docs/lakehouse/python.md` → `/lakehouse/python/`
- `docs/lakehouse/spark-sql.md` → `/lakehouse/spark-sql/`
- `docs/lakehouse/tests.md` → `/lakehouse/tests/`
- `docs/lakehouse/incremental.md` → `/lakehouse/incremental/`
- `docs/lakehouse/shortcuts.md` → `/lakehouse/shortcuts/`
- `docs/lakehouse/runtime.md` → `/lakehouse/runtime/`
- `docs/warehouse/index.md` → `/warehouse/`
- `docs/warehouse/first-project.md` → `/warehouse/first-project/`
- `docs/warehouse/tests.md` → `/warehouse/tests/`
- `docs/warehouse/incremental.md` → `/warehouse/incremental/`
- `docs/warehouse/schema-and-protection.md` → `/warehouse/schema-and-protection/`
- `docs/semantic-models/index.md` → `/semantic-models/`
- `docs/semantic-models/native-tmdl.md` → `/semantic-models/native-tmdl/`
- `docs/semantic-models/managed-sources.md` → `/semantic-models/managed-sources/`
- `docs/semantic-models/validation.md` → `/semantic-models/validation/`
- `docs/semantic-models/shared-policy.md` → `/semantic-models/shared-policy/`
- `docs/semantic-models/custom-annotations.md` → `/semantic-models/custom-annotations/`
- `docs/semantic-models/composition.md` → `/semantic-models/composition/`
- `docs/semantic-models/from-tmdl.md` → `/semantic-models/from-tmdl/`
- `docs/reports/index.md` → `/reports/`
- `docs/reports/deploy.md` → `/reports/deploy/`
- `docs/reports/environments.md` → `/reports/environments/`
- `docs/estate/index.md` → `/estate/`
- `docs/estate/connected-items.md` → `/estate/connected-items/`
- `docs/estate/environments.md` → `/estate/environments/`
- `docs/estate/catalogue-and-health.md` → `/estate/catalogue-and-health/`
- `docs/estate/development-cycle.md` → `/estate/development-cycle/`
- `docs/estate/operate.md` → `/estate/operate/`
- `docs/estate/recovery.md` → `/estate/recovery/`
- `docs/estate/mirror.md` → `/estate/mirror/`
- `docs/estate/selective-runs.md` → `/estate/selective-runs/`
- `docs/estate/concurrency.md` → `/estate/concurrency/`
- `docs/estate/performance.md` → `/estate/performance/`
- `docs/estate/automation-and-deployment.md` → `/estate/automation-and-deployment/`

## Example checkpoints

| Item | First state | Next states | Deliberate fixture boundary |
|---|---|---|---|
| Lakehouse | Landing: Folder Parcel.Events → Table Parcel.Event from existing Python tutorial | CurrentStatus Spark SQL transformation → validation of the same Event/CurrentStatus names | Incremental Tracking fixture is a complete external-snapshot variant: explain Landing → Tracking explicitly; never imply rebuilding a source constant is a data-only incremental run |
| Warehouse | Operations: use the current complete first/pipeline SQL source; pick and document one Table/View pair, then keep it for Tests | Tests reference those installed names; use a compatible current-status source for incremental work | Existing parcel-incremental-warehouse uses a separate external ParcelSource and CurrentStatus; state this as a complete mutable-source variation, not a silent continuation |
| Semantic models | parcel-powerbi: Parcel native Import model/Report pair, Delivery Count = 2, add AutoHideForeignKeys | shared-policy/annotations snapshot preserves Parcel, Delivery and Depot; validation adds an Assumption to the working native model | parcel-powerbi-fabric explicitly changes partitions and adds Warehouse Operations; DAX/SQL reconciliation continues that managed-source checkpoint without provisioning it again |
| Reports | parcel-powerbi native Report with byPath, associated local Parcel model | same authored files with workspace-dev.yml and workspace-prod.yml bindings | no second modelling tutorial; Report-only support conditional on catalogue-backed known model; no Report Load/Test |
| Estate | working item(s), existing compatible catalogue; complete configs linked | connect → map → inspect → iterate → operate → recover → optional Mirror → select → tune → automate | selection oracle independent test fixture, not a fabricated live service; no mandatory Mirror/reset |

Item entrances stay short. Full execution belongs to first tasks. Tests/Health occur where applicable, not mechanically on every introduction. Source/native fixture changes must be explicit; direct entrants get full snapshots, continuing readers get the additions. Detailed concepts and advanced mechanisms remain substantive/searchable at their stable URLs, with Related links from new tasks; they are not compatibility stubs.

## Complete original page retention map

| Original page | Canonical owner(s) | Treatment | Existing rendered IDs retained or linked |
|---|---|---|---|
| `advanced/automation-and-execution-contexts.md` | `advanced/automation-and-execution-contexts.md` | retain substantive page and contextual links | `automation-and-execution-contexts`, `the-host-supplies-the-execution-context`, `sessions-reuse-acquired-capabilities`, `make-unattended-policy-explicit`, `supply-credentials-before-the-job-starts`, `treat-machine-readable-output-as-the-automation-interface` |
| `advanced/build-bundles-and-controlled-installation.md` | `advanced/build-bundles-and-controlled-installation.md` | retain substantive page and contextual links | `build-bundles-and-controlled-installation`, `inspect-without-retaining-a-bundle`, `check-source-before-planning`, `plan-against-the-intended-destination`, `review-and-transfer-one-complete-artifact`, `install-frozen-work-without-replanning`, `continue-the-lifecycle-at-the-destination` |
| `advanced/concurrency.md` | `estate/concurrency.md` | move with search-excluded direct pointer | `control-concurrency`, `limit-one-run`, `use-the-same-cap-in-python`, `tune-persistent-resource-limits-only-when-needed`, `measure-before-increasing-a-limit`, `related-tasks` |
| `advanced/incremental-build-selection.md` | `advanced/incremental-build-selection.md` | retain substantive page and contextual links | `how-incremental-build-selection-works`, `certification-is-the-starting-point`, `how-an-object-is-classified`, `why-descendants-appear`, `the-item-boundary-stops-propagation`, `logical-shortcuts-can-reveal-deferred-staleness`, `mirrored-objects-become-local-only-when-selected-work-needs-them`, `rebuild-starts-a-new-current-state` |
| `advanced/incremental-data-processing.md` | `advanced/incremental-data-processing.md` | retain substantive page and contextual links | `incremental-data-processing`, `the-incremental-table-contract`, `a-warehouse-table-over-an-ordinary-source`, `configure-the-managed-warehouse`, `provision-and-seed-the-external-source`, `declare-the-incremental-consumer`, `change-source-rows-then-load-without-build`, `bookmarks-separate-processing-state-from-source-data`, `folder-history-as-a-change-source`, `provision-the-external-lakehouse`, `declare-the-physical-folder-shortcut`, `declare-the-snapshot-folder`, `declare-the-incremental-table`, `establish-the-first-boundary`, `change-source-data-then-load-without-build`, `declaration-changes-cross-the-build-boundary` |
| `advanced/index.md` | `estate/index.md` | move with search-excluded direct pointer | `advanced`, `semantic-models` |
| `advanced/mirror-and-materialisation-strategies.md` | `advanced/mirror-and-materialisation-strategies.md` | retain substantive page and contextual links | `mirror-and-materialisation-strategies`, `choose-the-estate-shape`, `start-with-a-catalogue-only-branch`, `mirror-only-the-items-that-need-development-targets`, `let-build-create-a-mixed-estate`, `retain-protected-borrowed-contents`, `treat-re-mirroring-as-a-reset` |
| `advanced/partial-failures-rejected-data-and-thresholds.md` | `advanced/partial-failures-rejected-data-and-thresholds.md` | retain substantive page and contextual links | `partial-failures-rejected-data-and-stability-thresholds`, `a-node-failure-does-not-erase-completed-work`, `rejected-input-is-local-to-one-load`, `stability-thresholds-guard-target-wide-change`, `waive-a-threshold-only-for-a-reviewed-large-change`, `read-the-estate-as-partial-state` |
| `advanced/performance-and-scale.md` | `estate/performance.md` | move with search-excluded direct pointer | `investigate-performance-and-scale`, `1-keep-the-comparison-fixed`, `2-separate-work-waits-and-overhead`, `3-adjust-the-work-not-just-the-lane-count`, `a-measured-estate`, `related-tasks` |
| `advanced/portable-execution-between-desktop-and-fabric.md` | `advanced/portable-execution-between-desktop-and-fabric.md` | retain substantive page and contextual links | `portable-execution-between-desktop-and-fabric`, `1-project-portability-use-one-source-tree`, `2-move-the-project-both-ways-with-fabric-git`, `3-operation-portability-change-the-entry-point`, `4-installed-artifact-portability-run-built-work-in-fabric`, `5-keep-the-lifecycle-in-fabric` |
| `advanced/power-bi/custom-annotations.md` | `semantic-models/custom-annotations.md` | move with search-excluded direct pointer | `add-a-custom-model-annotation`, `before-you-start`, `1-define-the-handler`, `2-declare-its-use`, `3-build-and-inspect`, `4-read-a-located-diagnostic`, `choose-a-phase-only-when-needed`, `related-tasks` |
| `advanced/power-bi/model-composition.md` | `semantic-models/composition.md` | move with search-excluded direct pointer | `compose-two-model-variants`, `before-you-start`, `1-read-each-difference`, `2-select-only-the-outputs`, `3-inspect-the-outputs`, `4-diagnose-a-missing-base`, `related-tasks` |
| `advanced/power-bi/model-from-tmdl.md` | `semantic-models/from-tmdl.md` | move with search-excluded direct pointer | `author-a-model-from-tmdl`, `1-write-one-complete-model`, `2-deploy-and-refresh`, `3-generate-from-a-managed-source-only-when-needed`, `related-tasks` |
| `advanced/power-bi/shared-policy.md` | `semantic-models/shared-policy.md` | move with search-excluded direct pointer | `share-native-modelling-standards`, `1-add-the-shared-policy`, `2-override-one-convention-locally`, `3-deploy-and-inspect`, `related-tasks` |
| `advanced/protecting-data.md` | `advanced/protecting-data.md` | retain substantive page and contextual links | `protecting-data`, `choose-the-ownership-boundary`, `keep-irreplaceable-sources-outside-weaver-ownership`, `retain-an-existing-weaver-owned-object`, `a-protected-borrowed-object-can-become-local-without-resetting-its-contents`, `know-what-prohibit-rebuild-does-not-do`, `revisit-the-choice-when-recovery-changes` |
| `advanced/row-auditing-and-operational-history.md` | `advanced/row-auditing-and-operational-history.md` | retain substantive page and contextual links | `row-auditing-and-operational-history`, `row-audit-columns-describe-current-rows`, `bookmarks-are-current-cursor-state`, `load-and-test-status-answer-what-is-true-now`, `_log-and-_loadstatistic-answer-what-happened`, `correlate-a-run-by-workflow-and-object`, `rebuild-resets-current-state-not-history`, `mirror-starts-destination-history-at-the-boundary` |
| `advanced/run-part-of-an-estate.md` | `estate/selective-runs.md` | move with search-excluded direct pointer | `run-part-of-an-estate`, `1-choose-the-item-boundary`, `2-choose-the-seed`, `3-inspect-the-preview`, `4-include-upstream-or-downstream-work`, `5-run-the-selection-you-inspected`, `6-cross-an-item-boundary-deliberately`, `7-match-several-names-and-diagnose-a-refusal`, `8-choose-the-right-kind-of-rerun`, `related-tasks` |
| `advanced/schemas-keys-and-managed-columns.md` | `advanced/schemas-keys-and-managed-columns.md` | retain substantive page and contextual links | `schemas-keys-and-managed-columns`, `declared-schema-and-inferred-schema`, `primary-keys-identify-rows-for-load`, `unique-keys-and-foreign-keys-add-logical-rules`, `nullability-is-authored`, `comparison-columns-decide-whether-a-matched-row-changed`, `identity-is-a-managed-surrogate`, `audit-and-signature-columns-are-not-business-columns`, `physical-representation-follows-the-engine` |
| `basics/development-cycle.md` | `estate/development-cycle.md` | move with search-excluded direct pointer | `the-development-cycle`, `optional-establish-a-mirrored-development-baseline`, `edit-and-iterate`, `include-semantic-models-and-reports` |
| `basics/index.md` | `index.md` | move with search-excluded direct pointer | `basics`, `author-the-items`, `validate-and-configure`, `develop-and-operate` |
| `basics/lakehouse-python.md` | `lakehouse/python.md` | move with search-excluded direct pointer | `build-a-lakehouse-pipeline-with-python`, `prerequisites`, `1-initialise-the-project`, `2-add-the-snapshot-folder`, `3-add-the-python-table`, `4-check-the-documents`, `5-publish-the-python-runtime`, `6-reuse-one-session-for-remote-work`, `7-inspect-the-result` |
| `basics/lakehouse-spark-sql.md` | `lakehouse/spark-sql.md` | move with search-excluded direct pointer | `build-a-lakehouse-pipeline-with-spark-sql`, `prerequisites`, `1-initialise-the-project`, `2-add-the-source-table`, `3-add-the-dependent-table`, `4-check-the-documents`, `5-build-and-load-the-item`, `6-inspect-the-result` |
| `basics/power-bi/deploy-pbip.md` | `semantic-models/native-tmdl.md`, `semantic-models/managed-sources.md`, `reports/deploy.md` | split with search-excluded direct pointer | `deploy-semantic-models-and-reports-with-pbip`, `native-files-first`, `before-you-start`, `1-choose-the-destination`, `2-check-the-project`, `3-deploy-the-model-and-linked-report`, `4-refresh-and-view-the-result`, `add-an-overlay-and-a-weaver-annotation`, `hide-relationship-foreign-keys`, `1-inspect-the-native-relationship`, `2-add-the-same-name-overlay`, `3-deploy-and-inspect`, `use-your-own-convention`, `cleanup`, `use-a-managed-source`, `before-the-source-backed-example`, `1-configure-destination-and-source-separately`, `2-build-and-load-the-warehouse-first`, `3-deploy-the-model-and-report`, `related-tasks` |
| `basics/power-bi/environments.md` | `reports/environments.md` | move with search-excluded direct pointer | `choose-development-and-production-targets` |
| `basics/power-bi/fabric-integration.md` | `semantic-models/managed-sources.md` | move with search-excluded direct pointer | `connect-a-semantic-model-to-source-data` |
| `basics/power-bi/index.md` | `semantic-models/index.md` | move with search-excluded direct pointer | `semantic-models-and-reports` |
| `basics/power-bi/modelling-rule.md` | `semantic-models/native-tmdl.md` | move with search-excluded direct pointer | `hide-relationship-foreign-keys` |
| `basics/power-bi/validate.md` | `semantic-models/validation.md` | move with search-excluded direct pointer | `validate-a-semantic-model` |
| `basics/recover-failed-work.md` | `estate/recovery.md` | move with search-excluded direct pointer | `recover-failed-work`, `choose-the-recovery`, `reconcile-corrected-source`, `rerun-failed-or-stale-load-work`, `include-related-work-deliberately`, `reconstruct-a-table`, `rerun-validation`, `recover-a-model-or-report`, `refresh-a-mirrored-baseline`, `wipe-only-when-the-desired-state-is-empty`, `remove-a-claim-without-emptying-the-item`, `verify-the-result` |
| `basics/run-and-inspect-estate.md` | `estate/operate.md` | move with search-excluded direct pointer | `run-and-inspect-an-estate`, `1-inspect-the-starting-state`, `2-run-installed-data-work`, `3-run-installed-validations`, `4-inspect-the-resulting-state` |
| `basics/sessions-and-workflows.md` | `estate/automation-and-deployment.md` | move with search-excluded direct pointer | `work-in-sessions-and-workflows`, `open-one-session`, `turn-the-accepted-sequence-into-a-workflow` |
| `basics/shortcuts.md` | `lakehouse/shortcuts.md` | move with search-excluded direct pointer | `connect-data-with-shortcuts`, `connect-managed-items-with-a-logical-shortcut`, `prerequisites`, `1-initialise-both-items`, `2-add-the-source-table`, `3-present-it-in-the-warehouse`, `4-check-and-build-the-relationship`, `5-load-the-producer`, `6-query-through-the-shortcut`, `connect-external-data-with-a-physical-shortcut` |
| `basics/tests-and-assumptions.md` | `lakehouse/tests.md`, `warehouse/tests.md`, `semantic-models/validation.md` | split with search-excluded direct pointer | `add-tests-and-assumptions`, `choose-the-validation-form`, `warehouse-validations`, `prerequisites`, `1-initialise-the-project`, `2-add-data-to-validate`, `3-add-a-test`, `4-add-an-assumption`, `5-check-build-and-load`, `6-run-the-validations`, `7-diagnose-one-deliberate-failure`, `semantic-model-validations`, `before-you-start`, `1-deploy-and-refresh`, `2-run-the-source-assumption`, `3-produce-a-finding`, `4-correct-it`, `compare-dax-with-source-sql`, `produce-and-correct-a-discrepancy`, `read-the-estate-result` |
| `basics/troubleshooting.md` | `basics/troubleshooting.md` | retain substantive page and contextual links | `troubleshooting`, `check-fails`, `build-fails`, `load-fails`, `test-cannot-run`, `health-is-amber`, `health-is-red`, `runtime-or-authentication-fails`, `windows-output-is-garbled-or-cannot-be-decoded` |
| `basics/warehouse-pipeline.md` | `warehouse/first-project.md` | move with search-excluded direct pointer | `build-a-warehouse-pipeline`, `prerequisites`, `1-initialise-the-project`, `2-add-the-table`, `3-add-the-dependent-view`, `4-check-the-documents`, `5-build-the-item`, `6-load-and-inspect-the-result` |
| `basics/workspace-and-python-runtime.md` | `estate/environments.md`, `lakehouse/runtime.md`, `reports/environments.md` | split with search-excluded direct pointer | `configure-a-workspace-and-python-runtime`, `bind-the-project-to-fabric`, `keep-development-and-production-bindings-separate`, `model-and-report-targets`, `1-map-the-two-destinations`, `2-deploy-and-refresh-each-pair`, `cleanup`, `add-a-fabric-environment-for-python-work`, `publish-the-runtime` |
| `core-concepts/build-load-and-test.md` | `core-concepts/build-load-and-test.md` | retain substantive page and contextual links | `build-load-and-test`, `build-interprets-authored-source`, `load-runs-installed-data-work`, `test-runs-installed-validations`, `health-reads-state`, `each-operation-has-its-own-boundary`, `a-workflow-composes-ordinary-operations` |
| `core-concepts/catalogue.md` | `core-concepts/catalogue.md` | retain substantive page and contextual links | `weaver-catalogue`, `how-to-read-the-_-schema`, `installed-and-declaration-state`, `current-operational-state`, `operational-history`, `mirrored-and-borrowed-state`, `inspect-the-catalogue-change-it-through-weaver` |
| `core-concepts/dependencies.md` | `core-concepts/dependencies.md` | retain substantive page and contextual links | `dependencies`, `document-dependencies`, `item-dependencies`, `logical-shortcuts-carry-managed-relationships-across-items`, `semantic-model-dependencies`, `dependencies-do-not-widen-selection` |
| `core-concepts/design-philosophy.md` | `core-concepts/design-philosophy.md` | retain substantive page and contextual links | `design-philosophy`, `natural-authoring`, `declaration-and-execution-are-separate`, `reconcile-change-rather-than-recreate-the-estate`, `fabric-native-by-construction`, `operational-state-is-data`, `failure-is-local`, `one-project-many-estates` |
| `core-concepts/fault-tolerance.md` | `core-concepts/fault-tolerance.md` | retain substantive page and contextual links | `fault-tolerance`, `fail-fast-and-fault-tolerant-execution`, `policies-belong-to-operations`, `partial-state-and-recovery` |
| `core-concepts/how-weaver-works.md` | `core-concepts/how-weaver-works.md` | retain substantive page and contextual links | `how-weaver-works`, `keep-the-source-in-a-project`, `build-deploys-definitions`, `load-follows-the-dependency-graph`, `test-checks-the-data`, `health-reads-the-whole-estate`, `develop-against-existing-data` |
| `core-concepts/index.md` | `estate/index.md` | move with search-excluded direct pointer | `core-concepts`, `establish-the-estate-boundary`, `follow-authored-work-into-operation`, `reason-about-ordering-and-failure` |
| `core-concepts/logical-and-physical-items.md` | `core-concepts/logical-and-physical-items.md` | retain substantive page and contextual links | `logical-and-physical-items`, `choose-one-of-three-ownership-cases`, `logical-identity-stays-with-the-source`, `workspace-configyml-supplies-an-environment`, `one-project-can-bind-to-development-and-production` |
| `core-concepts/mirrors.md` | `core-concepts/mirrors.md` | retain substantive page and contextual links | `mirrors`, `borrowed-data-and-local-data`, `destination-bindings-create-the-development-estate`, `build-turns-borrowed-objects-into-local-objects`, `_mirror-records-what-is-still-borrowed` |
| `core-concepts/projects-and-estates.md` | `core-concepts/projects-and-estates.md` | retain substantive page and contextual links | `projects-and-estates`, `a-project-is-organised-by-logical-item`, `build-makes-source-changes-operational`, `recorded-operational-state-belongs-to-the-installed-generation` |
| `core-concepts/sessions-and-workflows.md` | `core-concepts/sessions-and-workflows.md` | retain substantive page and contextual links | `sessions-and-workflows`, `a-session-is-shared-execution-context`, `a-workflow-orders-ordinary-commands`, `composition-does-not-create-a-transaction` |
| `core-concepts/state-and-health.md` | `core-concepts/state-and-health.md` | retain substantive page and contextual links | `state-and-health`, `three-views-of-the-estate`, `green-amber-and-red`, `stale-is-not-failed`, `build-consistency-is-installed-consistency`, `health-is-a-read` |
| `core-concepts/weaver-documents.md` | `core-concepts/weaver-documents.md` | retain substantive page and contextual links | `weaver-documents`, `documents-that-hold-or-present-data`, `table`, `folder`, `view`, `native-models-overlays-and-annotations`, `documents-that-validate-data`, `test`, `assumption`, `documents-that-connect-or-describe-the-estate`, `shortcut`, `warehouse-programmable`, `schema-metadata`, `supporting-files-travel-with-an-item` |
| `getting-started/first-project.md` | `warehouse/first-project.md` | move with search-excluded direct pointer | `first-fabric-project`, `1-initialise-the-project`, `2-add-a-table`, `3-add-a-test`, `4-check-the-project`, `5-build-the-installed-estate`, `6-load-the-table`, `7-run-the-test`, `8-read-health`, `9-run-the-lifecycle-as-a-workflow` |
| `getting-started/index.md` | `getting-started/index.md` | retain substantive page and contextual links | `getting-started` |
| `getting-started/installation.md` | `getting-started/installation.md` | retain substantive page and contextual links | `installation`, `install-the-documented-snapshot`, `configure-fabric-access`, `model-and-report-access`, `when-the-preview-needs-a-hosted-runtime`, `sign-in-for-the-operation` |
| `index.md` | `index.md` | retain substantive page and contextual links | `weaver-documentation`, `build-your-first-project`, `add-work-to-the-project`, `operate-the-estate` |
| `reference/build-bundle-format.md` | `reference/build-bundle-format.md` | retain substantive page and contextual links | `build-bundle-format`, `directory-and-archive`, `manifest-fields`, `action-graph`, `payloads`, `integrity-and-refusals`, `install-boundary` |
| `reference/catalogue-schema.md` | `reference/catalogue-schema.md` | retain substantive page and contextual links | `catalogue-schema`, `reading-the-tables`, `what-to-inspect`, `physical-table-declarations`, `_bookmark`, `_columndictionary`, `_dependency`, `_folderdictionary`, `_foreignkeydictionary`, `_installation`, `_keydictionary`, `_loadstatistic`, `_loadstatus`, `_log`, `_mirror`, `_registry`, `_schemadictionary`, `_semanticmodel`, `_semanticmodelcolumn`, `_semanticmodelmeasure`, `_semanticmodelrelationship`, `_semanticmodeltable`, `_semanticmodeltest`, `_shortcut`, `_tabledictionary`, `_testdictionary`, `_teststatus`, `ownership-and-relationships`, `standard-item-surface`, `read-and-format-boundary` |
| `reference/cli.md` | `reference/cli.md` | retain substantive page and contextual links | `cli-reference`, `commands`, `workspace-options`, `item-and-target-selection`, `interaction-and-automation`, `build-and-install`, `load-test-and-health-selection`, `destructive-commands`, `shared-cli-behaviour`, `parsing-and-help`, `interactive-and-non-interactive-input`, `destructive-authorisation`, `human-output-and-machine-output`, `status-and-exit-semantics`, `interruption`, `defined-behaviour` |
| `reference/cli/build.md` | `reference/cli/build.md` | retain substantive page and contextual links | `weaver-build`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution-modes`, `interaction-and-outcomes`, `examples`, `build-source-items-then-models-and-reports` |
| `reference/cli/check.md` | `reference/cli/check.md` | retain substantive page and contextual links | `weaver-check`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples` |
| `reference/cli/doctor.md` | `reference/cli/doctor.md` | retain substantive page and contextual links | `weaver-doctor`, `synopsis`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples` |
| `reference/cli/fabric-capacity.md` | `reference/cli/fabric-capacity.md` | retain substantive page and contextual links | `weaver-fabric-capacity`, `weaver-fabric-capacity_1`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples`, `control-a-fabric-capacity`, `prerequisites`, `inspect-state-before-changing-it`, `resume-and-confirm-the-transition`, `suspend-only-after-work-has-settled`, `run-from-unattended-automation` |
| `reference/cli/fabric-environment.md` | `reference/cli/fabric-environment.md` | retain substantive page and contextual links | `weaver-fabric-environment`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples`, `pre-release-source-checkout` |
| `reference/cli/fabric-notebook.md` | `reference/cli/fabric-notebook.md` | retain substantive page and contextual links | `weaver-fabric-notebook`, `weaver-fabric-notebook_1`, `weaver-fabric-notebook-push`, `synopsis`, `positional-arguments`, `options`, `weaver-fabric-notebook-run`, `synopsis_1`, `positional-arguments_1`, `options_1`, `responsibility-and-selection`, `execution`, `push`, `run`, `interaction`, `output-and-exit-behaviour`, `examples`, `push-and-run-a-fabric-notebook`, `prerequisites`, `push-the-notebook-definition`, `run-and-wait-for-the-result`, `submit-without-waiting`, `use-an-environment-from-another-workspace` |
| `reference/cli/health.md` | `reference/cli/health.md` | retain substantive page and contextual links | `weaver-health`, `synopsis`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples`, `one-report-for-the-estate` |
| `reference/cli/initialise.md` | `reference/cli/initialise.md` | retain substantive page and contextual links | `weaver-initialise`, `synopsis`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples` |
| `reference/cli/install.md` | `reference/cli/install.md` | retain substantive page and contextual links | `weaver-install`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution-and-outcomes` |
| `reference/cli/load.md` | `reference/cli/load.md` | retain substantive page and contextual links | `weaver-load`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution-and-warnings`, `interaction-and-outcomes`, `examples`, `refresh-a-model-with-its-source-work` |
| `reference/cli/mirror.md` | `reference/cli/mirror.md` | retain substantive page and contextual links | `weaver-mirror`, `synopsis`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples` |
| `reference/cli/session.md` | `reference/cli/session.md` | retain substantive page and contextual links | `weaver-session`, `synopsis`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `example` |
| `reference/cli/test.md` | `reference/cli/test.md` | retain substantive page and contextual links | `weaver-test`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution-and-outcomes`, `examples`, `validate-source-data-and-semantic-models-together` |
| `reference/cli/unbind.md` | `reference/cli/unbind.md` | retain substantive page and contextual links | `weaver-unbind`, `synopsis`, `positional-arguments`, `options` |
| `reference/cli/wipe.md` | `reference/cli/wipe.md` | retain substantive page and contextual links | `weaver-wipe`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `examples` |
| `reference/cli/workflow.md` | `reference/cli/workflow.md` | retain substantive page and contextual links | `weaver-workflow`, `synopsis`, `positional-arguments`, `options`, `responsibility-and-selection`, `execution`, `interaction`, `output-and-exit-behaviour`, `example` |
| `reference/configuration-files/fabric-environment.md` | `reference/configuration-files/fabric-environment.md` | retain substantive page and contextual links | `fabric-environment-definition`, `local-definition-directory`, `complete-example`, `environmentyml-shape`, `released-publication`, `development-publication`, `local-definition-authority`, `existing-environment-authority`, `publication-result-and-unchanged-definitions` |
| `reference/configuration-files/index.md` | `reference/configuration-files/index.md` | retain substantive page and contextual links | `configuration-files` |
| `reference/configuration-files/workflow.md` | `reference/configuration-files/workflow.md` | retain substantive page and contextual links | `workflow-configuration`, `file-selection`, `document-shape`, `entry-grammar`, `workspace-restrictions`, `validation-boundary` |
| `reference/configuration-files/workspace-config.md` | `reference/configuration-files/workspace-config.md` | retain substantive page and contextual links | `workspace-configuration`, `file-and-discovery`, `complete-shape`, `top-level-keys`, `execution`, `data_sources`, `targets`, `what-each-binding-controls`, `workspace-resolution-and-precedence`, `configuration-selection`, `mirror-source-and-destination-resolution`, `validation-boundary` |
| `reference/index.md` | `reference/index.md` | retain substantive page and contextual links | `reference` |
| `reference/machine-readable-output.md` | `reference/machine-readable-output.md` | retain substantive page and contextual links | `machine-readable-output`, `stream-and-process-behaviour`, `commands-with-json`, `commands-without-json-result-mode`, `nested-field-shapes`, `initialise`, `doctor`, `build`, `install`, `load`, `test`, `health`, `wipe`, `unbind`, `mirror`, `fabric-notebooks`, `environment-publication-json`, `compatibility-boundary` |
| `reference/operation-behaviour/build.md` | `reference/operation-behaviour/build.md` | retain substantive page and contextual links | `build-behaviour`, `inputs-and-selection`, `source-item-reconciliation`, `power-bi-deployment-modes`, `read-only-preview`, `retained-bundle-and-installation`, `state-outcomes-and-reruns` |
| `reference/operation-behaviour/fault-and-outcome-vocabulary.md` | `reference/operation-behaviour/fault-and-outcome-vocabulary.md` | retain substantive page and contextual links | `fault-and-outcome-vocabulary`, `build-and-install`, `load`, `test`, `health`, `mirror-wipe-and-workflow`, `persisted-catalogue-outcomes`, `message-severity-and-compatibility` |
| `reference/operation-behaviour/health.md` | `reference/operation-behaviour/health.md` | retain substantive page and contextual links | `health-behaviour`, `selection-and-evidence`, `inventory-and-host-boundaries`, `status-aggregation`, `load`, `tests`, `build`, `as_of-and-dependency-freshness`, `report-and-exit-behaviour` |
| `reference/operation-behaviour/index.md` | `reference/operation-behaviour/index.md` | retain substantive page and contextual links | `operation-behaviour` |
| `reference/operation-behaviour/load.md` | `reference/operation-behaviour/load.md` | retain substantive page and contextual links | `load-behaviour`, `selection`, `planning-and-ordering`, `dry-run`, `execution`, `reload`, `outcomes-and-failure-policy`, `persistent-state-and-partial-effects`, `host-qualification` |
| `reference/operation-behaviour/mirror.md` | `reference/operation-behaviour/mirror.md` | retain substantive page and contextual links | `mirror-behaviour`, `source-and-destination`, `item-selection`, `preflight-and-authorisation`, `catalogue-copy`, `selected-item-state`, `failure-partial-effects-and-re-mirroring` |
| `reference/operation-behaviour/session-runtime.md` | `reference/operation-behaviour/session-runtime.md` | retain substantive page and contextual links | `session-and-runtime-behaviour`, `workspace-binding`, `host-position`, `capability-acquisition-reuse-and-close`, `credentials`, `fabric-environment-qualification`, `runtime-definition-boundary` |
| `reference/operation-behaviour/shared-selection-and-identity.md` | `reference/operation-behaviour/shared-selection-and-identity.md` | retain substantive page and contextual links | `shared-selection-and-identity`, `project-identity`, `logical-item-identity`, `schema-and-document-identity`, `case-lookup-and-collisions`, `physical-fabric-identities`, `selector-summary`, `build-selection`, `load-selection`, `test-selection`, `health-selection`, `wipe-selection`, `mirror-selection`, `selection-and-dependency-boundary` |
| `reference/operation-behaviour/test.md` | `reference/operation-behaviour/test.md` | retain substantive page and contextual links | `test-behaviour`, `selection`, `planning-and-host-requirements`, `validation-semantics`, `dry-run`, `outcomes-reports-and-process-status`, `current-state-history-and-reruns` |
| `reference/operation-behaviour/unbind.md` | `reference/operation-behaviour/unbind.md` | retain substantive page and contextual links | `unbind-behaviour`, `selection-and-preflight`, `confirmation-and-execution`, `resulting-state` |
| `reference/operation-behaviour/wipe.md` | `reference/operation-behaviour/wipe.md` | retain substantive page and contextual links | `wipe-behaviour`, `physical-target-selection`, `catalogue-disposition`, `semantic-model-reset-and-source-preservation`, `preview-and-authorisation`, `ordering-failure-and-results` |
| `reference/operation-behaviour/workflow.md` | `reference/operation-behaviour/workflow.md` | retain substantive page and contextual links | `workflow-behaviour`, `discovery-and-yaml-shape`, `command-parsing`, `one-workspace-and-one-session`, `confirmation`, `execution-and-failure` |
| `reference/power-bi/annotations.md` | `reference/power-bi/annotations.md` | retain substantive page and contextual links | `semantic-model-annotations`, `weaversource`, `weaverbasesemanticmodels`, `weavermeasuretable`, `weaverswitch`, `weaverautohidecolumns`, `weaverautohideforeignkeys`, `weaverexclude` |
| `reference/power-bi/index.md` | `reference/power-bi/index.md` | retain substantive page and contextual links | `semantic-models-and-reports-reference` |
| `reference/power-bi/project-layout.md` | `reference/power-bi/project-layout.md` | retain substantive page and contextual links | `power-bi-project-layout`, `model-discovery-and-identity`, `report-discovery-and-association`, `validation-ownership` |
| `reference/power-bi/requirements-and-compatibility.md` | `reference/power-bi/requirements-and-compatibility.md` | retain substantive page and contextual links | `power-bi-requirements-and-compatibility`, `runtime-and-service-access`, `mode-matrix`, `native-formats-and-preservation`, `report-binding`, `source-mapping-and-connections` |
| `reference/power-bi/tmdl.md` | `reference/power-bi/tmdl.md` | retain substantive page and contextual links | `tmdl-policy-overlays-and-composition`, `addressing-and-merge-rules`, `policy-and-local-precedence`, `compose-named-models`, `preservation-and-deployment-boundary` |
| `reference/power-bi/validations.md` | `reference/power-bi/validations.md` | retain substantive page and contextual links | `dax-tests-and-assumptions`, `location-and-body`, `metadata`, `comparison`, `file-and-catalogue-modes` |
| `reference/python/errors.md` | `reference/python/errors.md` | retain substantive page and contextual links | `python-exceptions`, `public-exports`, `weavererror`, `commanderror`, `configerror`, `identityerror`, `validationerror` |
| `reference/python/index.md` | `reference/python/index.md` | retain substantive page and contextual links | `python-api`, `public-exports` |
| `reference/python/objects.md` | `reference/python/objects.md` | retain substantive page and contextual links | `python-authored-objects`, `public-exports`, `weaverobject`, `folder`, `table`, `sparksqltable`, `view`, `shortcut` |
| `reference/python/operations.md` | `reference/python/operations.md` | retain substantive page and contextual links | `python-operations`, `lifecycle-calls`, `plan-before-changing-state`, `public-exports`, `weaverbuild`, `weavercheck_mirror`, `weaverhealth`, `weaverinitialise`, `weaverload`, `weavermirror`, `weaverplan_mirror`, `weaverplan_unbind`, `weaverplan_wipe`, `weavertest`, `weaverunbind`, `weaverwipe` |
| `reference/python/results.md` | `reference/python/results.md` | retain substantive page and contextual links | `python-result-and-report-types`, `public-exports`, `initialisation`, `fabricitemoutcome`, `exampleoutcome`, `initialisereport`, `build`, `buildresult`, `mirror`, `mirrorplan`, `mirrorresult`, `wipe`, `wipeplan`, `wipereport`, `wipeitemresult`, `wiperesult`, `unbind`, `unbindplan`, `unbindresult`, `load`, `loadresult`, `loadmessage`, `loadnodereport`, `loadrunreport`, `validation`, `validationnodereport`, `validationrunreport`, `health`, `healthfinding`, `healthsection`, `loadactivity`, `healthreport` |
| `reference/python/semantic-models.md` | `reference/python/semantic-models.md` | retain substantive page and contextual links | `semantic-model-extension-api`, `define-an-annotation`, `phases`, `edit-native-parts`, `supported-extension-signatures`, `weaversemantic_modelsannotationannotation`, `weaversemantic_modelsobjectstmdldefinition`, `weaversemantic_modelsobjectstmdlobject`, `weaversemantic_modelsobjectstmdlcollection` |
| `reference/python/session.md` | `reference/python/session.md` | retain substantive page and contextual links | `session-and-workspace-helpers`, `lakehouse-locations`, `public-exports`, `weaverlakehouse`, `weavercurrent_workspace`, `weaverdefault_lakehouse`, `weaverlakehouse_for`, `weaversession` |
| `reference/python/validation.md` | `reference/python/validation.md` | retain substantive page and contextual links | `python-validation-objects`, `public-exports`, `test`, `assumption`, `sparksqltest`, `sparksqlassumption` |
| `reference/weaver-documents/assumption.md` | `reference/weaver-documents/assumption.md` | retain substantive page and contextual links | `assumption`, `location-and-identity`, `metadata`, `python-body`, `sql-body`, `operations-and-managed-state` |
| `reference/weaver-documents/common-metadata.md` | `reference/weaver-documents/common-metadata.md` | retain substantive page and contextual links | `common-metadata`, `location-filename-and-identity`, `shared-metadata-keys`, `dependency-inference-and-override`, `python-and-sql-structure`, `complete-example`, `operation-and-catalogue-boundary` |
| `reference/weaver-documents/folder.md` | `reference/weaver-documents/folder.md` | retain substantive page and contextual links | `folder`, `location-and-authored-form`, `metadata`, `read-contract`, `complete-example`, `build-load-test-and-managed-state` |
| `reference/weaver-documents/overview.md` | `reference/weaver-documents/overview.md` | retain substantive page and contextual links | `weaver-documents`, `document-model`, `supported-forms`, `metadata-and-bodies`, `dependencies`, `page-map` |
| `reference/weaver-documents/schema-metadata.md` | `reference/weaver-documents/schema-metadata.md` | retain substantive page and contextual links | `schema-metadata`, `location-and-identity`, `keys`, `operations-and-managed-state` |
| `reference/weaver-documents/shortcut.md` | `reference/weaver-documents/shortcut.md` | retain substantive page and contextual links | `shortcut`, `supported-declaration-files`, `lakehouse-shortcutspy`, `warehouse-shortcutsyml`, `identity-compatibility-and-dependencies`, `operations-and-managed-state` |
| `reference/weaver-documents/table.md` | `reference/weaver-documents/table.md` | retain substantive page and contextual links | `table`, `location-and-authored-form`, `metadata`, `incompatible-combinations`, `body-and-return-contract`, `python`, `spark-sql`, `t-sql`, `complete-examples`, `build-load-test-and-managed-state` |
| `reference/weaver-documents/test.md` | `reference/weaver-documents/test.md` | retain substantive page and contextual links | `test`, `location-and-identity`, `metadata`, `python-body`, `sql-body`, `operations-and-managed-state` |
| `reference/weaver-documents/view.md` | `reference/weaver-documents/view.md` | retain substantive page and contextual links | `view`, `location-and-authored-form`, `metadata`, `sql-body`, `complete-examples`, `build-load-test-and-managed-state` |
| `reference/weaver-documents/warehouse-programmable.md` | `reference/weaver-documents/warehouse-programmable.md` | retain substantive page and contextual links | `warehouse-programmable`, `location-and-identity`, `operations-and-managed-state` |

## Split fragment ownership

- `basics/power-bi/deploy-pbip.md#use-a-managed-source` → `semantic-models/managed-sources.md`
- `basics/power-bi/deploy-pbip.md#add-an-overlay-and-a-weaver-annotation` → `semantic-models/native-tmdl.md#hide-relationship-foreign-keys`
- `basics/power-bi/deploy-pbip.md#hide-relationship-foreign-keys` → `semantic-models/native-tmdl.md#hide-relationship-foreign-keys`
- `basics/tests-and-assumptions.md#semantic-model-validations` → `semantic-models/validation.md`
- `basics/tests-and-assumptions.md#compare-dax-with-source-sql` → `semantic-models/validation.md#compare-dax-with-source-sql`
- `basics/tests-and-assumptions.md#warehouse-validations` → `warehouse/tests.md`
- `basics/workspace-and-python-runtime.md#model-and-report-targets` → `reports/environments.md`

Every retired fragment remains at its original route with an explicit link directly to its final owner. Integration chooses equivalent anchors on retained moved headings where possible, otherwise the new owning task. No pointer chains. Fixture, root README and product links are updated after final owner anchors exist.

## Incoming product targets before migration

- `docs/index.html` → `https://docs.weaverstack.dev/`
- `docs/index.html` → `https://docs.weaverstack.dev/getting-started/first-project/`
- `docs/index.html` → `https://docs.weaverstack.dev/basics/development-cycle/`
- `docs/index.html` → `https://docs.weaverstack.dev/getting-started/first-project/`
- `docs/index.html` → `https://docs.weaverstack.dev/`
- `docs/vs-dbt/index.html` → `https://docs.weaverstack.dev/`
- `docs/vs-dbt/index.html` → `https://docs.weaverstack.dev/`
- `docs/warehouse/index.html` → `https://docs.weaverstack.dev/`
- `docs/warehouse/index.html` → `https://docs.weaverstack.dev/basics/warehouse-pipeline/`
- `docs/warehouse/index.html` → `https://docs.weaverstack.dev/basics/development-cycle/`
- `docs/warehouse/index.html` → `https://docs.weaverstack.dev/advanced/mirror-and-materialisation-strategies/`
- `docs/warehouse/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/#use-a-managed-source`
- `docs/warehouse/index.html` → `https://docs.weaverstack.dev/`
- `docs/reports/index.html` → `https://docs.weaverstack.dev/`
- `docs/reports/index.html` → `https://docs.weaverstack.dev/basics/workspace-and-python-runtime/#model-and-report-targets`
- `docs/reports/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/`
- `docs/reports/index.html` → `https://docs.weaverstack.dev/reference/power-bi/requirements-and-compatibility/`
- `docs/reports/index.html` → `https://docs.weaverstack.dev/`
- `docs/lakehouse/index.html` → `https://docs.weaverstack.dev/`
- `docs/lakehouse/index.html` → `https://docs.weaverstack.dev/basics/lakehouse-python/`
- `docs/lakehouse/index.html` → `https://docs.weaverstack.dev/advanced/incremental-data-processing/`
- `docs/lakehouse/index.html` → `https://docs.weaverstack.dev/advanced/mirror-and-materialisation-strategies/`
- `docs/lakehouse/index.html` → `https://docs.weaverstack.dev/basics/run-and-inspect-estate/`
- `docs/lakehouse/index.html` → `https://docs.weaverstack.dev/`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/#use-a-managed-source`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/#add-an-overlay-and-a-weaver-annotation`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/advanced/power-bi/shared-policy/`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/basics/tests-and-assumptions/#semantic-model-validations`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/advanced/power-bi/model-composition/`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/`
- `docs/semantic-models/index.html` → `https://docs.weaverstack.dev/`
- `docs/scale/index.html` → `https://docs.weaverstack.dev/`
- `docs/scale/index.html` → `https://docs.weaverstack.dev/advanced/performance-and-scale/`
- `docs/scale/index.html` → `https://docs.weaverstack.dev/`
- `docs/features/index.html` → `https://docs.weaverstack.dev/`
- `docs/features/index.html` → `https://docs.weaverstack.dev/`
- `docs/how-it-works/index.html` → `https://docs.weaverstack.dev/`
- `docs/how-it-works/index.html` → `https://docs.weaverstack.dev/basics/run-and-inspect-estate/`
- `docs/how-it-works/index.html` → `https://docs.weaverstack.dev/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/getting-started/installation/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/getting-started/first-project/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/basics/lakehouse-python/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/basics/warehouse-pipeline/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/basics/power-bi/deploy-pbip/`
- `docs/get-started/index.html` → `https://docs.weaverstack.dev/`
- `docs/problem/index.html` → `https://docs.weaverstack.dev/`
- `docs/problem/index.html` → `https://docs.weaverstack.dev/`

## First-pair integration checkpoint

Lakehouse parent integration retains Landing Folder Parcel.Events → Python Parcel.Event → SQL CurrentStatus → validations. The existing parcel-lakehouse fixture gains the latter three declarations; optional independent ServiceLevel remains deliberate fixture-only support. Warehouse settles on the existing Parcel.StatusEvent Table → CurrentStatus View and adds independent expected-row/known-status validations in the coherent parcel-warehouse-journey snapshot. Its original SQL remains byte-identical. Mutable-source variations are explicit, separate complete snapshots, not silent replacements.

Parent reviewed actual diffs and all new prose; reran the maintained Lakehouse checker (7 checkpoints, 12 exact blocks, 3 generated modules) and Warehouse checker (5 checkpoints, 12 exact blocks, 14 SQL program blocks). Removed evaluator diary from public pages while retaining operation qualifications; an overbroad prose whitespace cleanup initially changed fenced bytes, the exact fences were restored and both synchronization/check gates passed. No source runtime or remote service change.

## Second-pair integration checkpoint

Parent reviewed the actual model/Report diffs, then reran seven semantic owners through 12 assembled local Check/compiler checkpoints with 16 byte-identical fixture blocks. Source failure/correction preserves an existing rule/custom overlay and handles an absent overlay separately. Native model/config fixture bytes remain unchanged. Report gate rerun: 8 parsed commands, one JSON plus three exact YAML occurrences, 17 fixture hashes unchanged, native card/model and real dev/prod encoder over explicit offline inventory passed. No live binding/readback claim.

Reproducible gates now live in `tools/check_semantic_examples.py` and `tools/check_report_examples.py`; Lakehouse has its maintained gate too. Parent started re-homing old paths into 27 direct search-excluded pointers with captured IDs, and updated narrative links outside source fences. The guide checker now targets new canonical model/Report/estate owners rather than stubs. Final anchor, search and strict build gates await estate integration and the route audit.
