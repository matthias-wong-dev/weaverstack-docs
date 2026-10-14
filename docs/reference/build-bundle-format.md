# Build bundle format

A retained Build bundle is frozen, destination-bound installation input. `weaver build --bundle-only` writes a local directory; `weaver install` accepts it or a `.weaver.zip` archive. Build preview (`--dry-run`) presents the canonical plan but retains no deployable bundle. Neither mode provisions missing Power BI targets.

This page describes Build bundle format **5**. The loader accepts exactly this format number, not older format-3/4 plans. This is a current representation, not a cross-version interchangeability or upgrade-window promise.

## Directory and archive

```text
bundle/
├── plan.yml
└── payload/
    └── <action-specific paths>
```

Payload bytes are written first and `plan.yml` last; no manifest means no loadable bundle. Payloadless actions have no file. `--bundle-path` requires bundle-only mode and an absent/empty destination. Without an explicit path the returned bundle directory is retained.

Install writes `install-report.yml` beside a directory bundle after execution. The report is not input or part of bundle identity. Archive Install extracts into a temporary directory and removes it afterward, so its sidecar report is temporary. Direct Build separately retains its report outside the temporary bundle.

An archive contains `plan.yml` and `payload/...` at its root, without an extra wrapper directory. The CLI does not create archives. Python archive helpers order paths, use DEFLATE level 9, timestamp `1980-01-01 00:00:00` and regular-file mode `0644`. Extraction rejects absolute/invalid traversal paths and symbolic links. Directory/archive URLs are not Install inputs.

## Manifest fields

| Field | Current shape |
| --- | --- |
| `format_version` | integer `5` |
| `bundle_id` | SHA-256 of canonical manifest with this field blank |
| `targets` | frozen target mappings |
| `sequences` | presentation groups containing target batches and actions |
| `execution` | frozen workspace/catalogue/Environment/Spark attachment |
| `build_envelope` | Build-specific repository, impact, runtime and publication evidence; nullable for generic mutation plans |
| `driver_contracts` | explicitly frozen extension driver declarations |
| `required_completion` | action IDs that must complete for plan success |
| `protected_scopes` | target-relative scopes protected against destructive overlap |

A target has required `id`, `kind`, `item_id`; optional `item_name`, `workspace_id`, `workspace_name`, `sql_endpoint_id`, `logical_item_type`, `logical_item_name` are omitted when absent. Kinds are `lakehouse`, `warehouse`, `semanticmodel`, `report`. Logical kind/name must be paired and agree with the physical kind. IDs are local manifest references; resolved service IDs/names are frozen, not re-derived from a later configuration.

`execution` emits `workspace_name`, nullable `workspace_id`, `catalogue_target_id`, `environment`, `spark_home_target_id`. The last two target IDs reference the manifest's own targets. Environment is null or `{name, workspace, item_id}`; a qualified Environment keeps its owning workspace. No planned Spark work requires no Spark attachment.

## Action graph

A sequence emits `number`, `description`, `batches`. A batch emits `id`, `target_id`, `actions`. These are presentation/target groups, not serial global execution barriers. Each action carries its own execution edges.

| Action field | Meaning |
| --- | --- |
| `id`, `kind`, `executor` | unique identity, operation label and dispatch method |
| `resource_node_id` | logical subject or null |
| `payload`, `payload_sha256` | relative payload path and exact-byte SHA-256, or both null |
| `source_path` | optional authored relative path for diagnostics |
| `awaits_name_release` | emitted only when true for shortcut name reuse |
| `depends_on` | successful prerequisite action IDs |
| `settle_after` | known-terminal ordering IDs; failure may settle, uncertainty does not |
| `result_from` | null or `{action_id, result_type}` for a typed prior result |
| `certifies` | identities certified by successful action completion |
| `resources`, `exclusions` | frozen resource lanes and mutual-exclusion keys |
| `writes`, `destructive_scopes` | arrays of `{target_id, path}`; empty path means whole target |

Actions include source DDL/runtime/prune/publication work, explicit shortcut/endpoint readiness, protected-mirror materialisation, semantic deployment/readback/catalogue publication and Report definition/readback. The literal `resource_node_id` is machine vocabulary, not a separate authoring category. A payloadless `completion_gate` is a special graph action and is excluded from ordinary installation action presentation.

`build_envelope` holds Build-specific facts such as `repository_name`, `repository_signature`, `selection`, `omitted_nodes`, `target_changes`, `runtime_state`, `runtime_state_established`, certification and validation-definition decisions when present. Selection contains `impact` (`new`, `changed`, `impacted_descendants`), `prohibited`, `selected_for_drop`, `selected_for_build`. Omissions identify `node_id`, `reason` and optional `detail`; supported reasons are `target_unbound`, `depends_on_omitted_node`, `unsupported_executor`, `shortcut_unsupported`. These are nested evidence, not the old top-level format-3 layout.

## Payloads

| Executor | Required suffix/form |
| --- | --- |
| `spark_sql` | `.spark.sql`, UTF-8 statement |
| `spark_sql_batch` | `.spark-sql-batch.json`, ordered SQL strings |
| `spark_table` | `.spark-table.json`, frozen table creation instruction |
| `tsql` | `.sql`, UTF-8 script |
| `tsql_batch` | `.tsql-batch.json`, ordered SQL scripts |
| `shortcut` | `.shortcut.json`, frozen create/remove instructions |
| `shortcut_readiness` | `.shortcut-readiness.json`, frozen readiness paths |
| `load_file` | `.payload`, exact bytes; `delete_file` is payloadless |
| `runtime_state` | `.runtime-state.json`, establish/invalidate instructions |
| `copy_files` | `.copy-files.json` |
| `materialise_mirror` | `.materialise-mirror.json` |
| `await_endpoint_objects` | `.endpoint-objects.json` |
| `semantic_model` | `.semantic_model.json` |
| `semantic_readback` | `.semantic_readback.json` |
| `semantic_catalogue` | `.semantic_catalogue.json` |
| `report_definition` | `.report_definition.json` |
| `report_readback` | `.report_readback.json` |
| `semantic_wipe` | `.semantic-wipe.json` |
| `folder`, `lakehouse_wipe` | payloadless |

Explicit driver contracts can declare other executor suffixes and typed result/completion policy; this representation does not make arbitrary private executors a supported public extension API. Regenerate bundles with Weaver, rather than editing manifests or manufacturing payloads.

## Integrity and refusals

Canonical JSON sorts keys and removes presentation whitespace. Bundle identity includes destinations, execution context, graph edges, protection/completion declarations, Build evidence and payload checksums, with no timestamp. A non-empty `bundle_id` is recomputed and checked against the plan. Payload checksums protect exact file bytes. Neither is authentication or an issuer's cryptographic signature; accept only trusted bundles/code.

Loading rejects unsupported formats, duplicate YAML/unknown mapping fields, malformed required fields, duplicate IDs, unordered sequence numbers, bad target kinds/paired identities, unknown/cyclic action references, invalid typed-result/completion/protection rules, unsupported executors, omitted-node actions and invalid payload presence/suffixes. Payload paths must start `payload/`, contain no colon/backslash/NUL and no empty, `.` or `..` component. Missing/corrupt payloads fail before dispatch. Frozen execution descriptors and expected driver contracts are checked before target work.

## Install boundary

Install uses the manifest's execution workspace, Environment, catalogue and Spark attachment. The CLI accepts no workspace/configuration, item-binding, catalogue or Environment override. A reused Python Session with a conflicting workspace is refused. Source is not reopened and impact/state is not replanned. Destination drift after generation remains a reason to regenerate, not a promise that frozen work will adapt.

Spark-backed execution admits a matching Weaver runtime before dispatch, including exact client version, plan format, Delta writer and executor capabilities. Desktop execution probes the published Environment; successful preparation/preview is not runtime admission. See [Session runtime](operation-behaviour/session-runtime.md#fabric-environment-qualification).

The shared scheduler dispatches ready graph actions subject to success/settlement edges, resource limits and exclusions. Independent branches may continue after known failures; dependent publication/certification cannot succeed without its required work. Uncertain mutation results fail rather than authorize replay. Installation reports `succeeded`, `failed` and `skipped` actions and has no operation-wide rollback. Earlier effects remain.

See [Build behaviour](operation-behaviour/build.md), [`weaver install`](cli/install.md) and [machine output](machine-readable-output.md).
