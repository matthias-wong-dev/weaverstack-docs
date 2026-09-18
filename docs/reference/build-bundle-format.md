# Build bundle format

A build bundle is frozen installation input. `weaver build --bundle-only` writes the CLI handoff as a local directory. `weaver install` accepts that directory or a local path whose name ends with `.weaver.zip`.

The CLI does not create archives. Python code can call the archive helpers, but renaming a directory or another ZIP to `.weaver.zip` does not make it a valid bundle. The format described here is the exact representation read and written by the referenced Weaver source, not a cross-version compatibility promise.

## Directory representation

Before installation, a bundle contains:

```text
bundle/
├── plan.yml
└── payload/
    └── <three-digit-sequence>-<stage>/
        └── <action-specific file>
```

`plan.yml` is the manifest. Files below `payload/` are generated, destination-specific installation inputs; they are not a copy of the source project. Payloadless actions create no file.

The writer stores payloads first and `plan.yml` last. A directory without the manifest is not loadable. `--bundle-path` is valid only with `--bundle-only`; the path must be absent or an empty directory. With no explicit path, bundle-only Build creates and reports a durable temporary directory.

Installing a directory writes `install-report.yml` beside `plan.yml` after execution. It contains the installation report, not part of the bundle identity or the input validation. The loader does not use it when loading the bundle.

## Archive representation

A `.weaver.zip` contains the same relative paths at the archive root:

```text
plan.yml
payload/...
```

An extra wrapping directory is invalid because the extracted root then has no `plan.yml`. Archive extraction rejects an absolute member path, an empty, `.` or `..` path component, and a symbolic-link entry. The Python archive writer orders files by relative path, uses DEFLATE level 9, fixes each timestamp at `1980-01-01 00:00:00`, and writes regular-file mode `0644`.

Install copies and extracts an archive into a temporary local directory, validates it there, executes it, and removes that temporary directory afterward. The resulting `install-report.yml` is therefore temporary for archive installation. Directory and archive URLs are rejected; Install requires a complete local handoff.

## `plan.yml`

The manifest is YAML generated from one mapping. Its current `format_version` is `3`, and the loader accepts only `3`.

| Field | Shape | Meaning |
| --- | --- | --- |
| `format_version` | integer | Exact bundle representation accepted by this implementation: `3`. |
| `bundle_id` | string | Generation-time SHA-256 identity of the canonical manifest with this field blank. |
| `repository_name` | string | Prepared source repository name. |
| `repository_signature` | string | Signature of the prepared repository state. |
| `targets` | array of target mappings | Frozen physical destinations. |
| `sequences` | array of sequence mappings | Ordered execution barriers. |
| `omitted_nodes` | array of omission mappings | Repository nodes not put in the plan. |
| `target_changes` | mapping from target ID to change arrays | Frozen physical additions and removals. |
| `runtime_state` | array of table/row mappings | Current-state rows to invalidate. |
| `runtime_state_established` | array of table/row mappings | Current-state rows to establish. |
| `selection` | mapping | Impact classification and selected identities. |

All listed top-level fields are emitted. Deserialisation requires `format_version`, `bundle_id`, `repository_name`, `repository_signature`, and `selection`; omitted collection fields currently read as empty collections. That tolerance is current loader behaviour, not permission to author partial manifests.

### Targets

Each `targets[]` entry has required `id`, `kind`, and `item_id`. It can also have `item_name`, `workspace_id`, `workspace_name`, `sql_endpoint_id`, `logical_item_type`, and `logical_item_name`; absent optional values are omitted rather than written as null.

`kind` is `lakehouse` or `warehouse` for plans Weaver generates. If logical identity is present, both `logical_item_type` and `logical_item_name` must be present, and the item type must agree with the target kind. A target `id` is local to this manifest. Item, workspace, endpoint, and display values are resolved and frozen during Build.

### Sequences, batches, and actions

A sequence has:

```yaml
number: 40
description: build dependency layer
batches: []
```

A batch has `id`, `target_id`, and `actions`. Every batch in a sequence runs in manifest order; every batch in one sequence settles before the next sequence starts. An action has these always-emitted fields:

```yaml
id: build-Lakehouse-Landing-Tables-Parcel.Event
kind: build_table
resource_node_id: Lakehouse/Landing/Tables/Parcel.Event
executor: spark_table
payload: payload/040-build/table-Parcel.Event.spark-table.json
payload_sha256: 0123456789abcdef...
```

`resource_node_id`, `payload`, and `payload_sha256` can be null. `source_path` is emitted only when an authored relative path is known. `awaits_name_release: true` is emitted only when a dropped shortcut's name will be reused; false is represented by absence.

Current planner action kinds are:

```text
create_schema, create_shortcut,
build_folder, build_table, build_view, build_procedure,
write_file, refresh_sql_endpoint,
drop_folder, drop_table, drop_view, drop_shortcut, drop_procedure, delete_file,
prune_table, prune_view, prune_schema, prune_folder,
delete_catalogue_claims, reconcile_runtime_state,
publish_catalogue, publish_registry
```

The structural loader does not independently whitelist `kind`; executor code interprets it where needed. The list above records what the current planner writes, not an extensibility point.

### Omitted nodes, changes, and runtime state

An `omitted_nodes[]` entry has `node_id`, `reason`, and optional `detail`. Current reasons are `target_unbound`, `depends_on_omitted_node`, `unsupported_executor`, and `shortcut_unsupported`.

`target_changes` maps a target ID to entries with `effect`, `object_kind`, `name`, and `action_id`. `effect` is `add` or `remove`. Current object kinds are `schema`, `table`, `view`, `folder`, `folder_schema`, `file`, `stored_procedure`, and `runtime_reference`.

Each `runtime_state[]` or `runtime_state_established[]` entry has `table` and `rows`. For invalidation, each row is a key mapping to remove; for establishment, each row is the complete current-state row to write. Historical tables are not represented here. The separate `.runtime-state.json` action payload has its own `format_version: 2` and arrays named `establish` and `invalidate`.

### Selection

`selection` has `impact`, `prohibited`, `selected_for_drop`, and `selected_for_build`. The last three are arrays of installed identity strings. `impact` has identity arrays named `new`, `changed`, and `impacted_descendants`.

## Payload and checksum forms

Every payload-bearing action stores a bundle-relative `payload` path and the lowercase hexadecimal SHA-256 of its exact bytes in `payload_sha256`.

| Executor | Required suffix | Payload form |
| --- | --- | --- |
| `spark_sql` | `.spark.sql` | One UTF-8 Spark SQL statement. |
| `spark_sql_batch` | `.spark-sql-batch.json` | JSON array of non-empty Spark SQL strings, executed in order in one submission. |
| `spark_table` | `.spark-table.json` | JSON table instruction with `object`, `source_query`, `setup`, `declared_columns`, `references`, `identity_column`, `audit_columns`, `internal_columns`, `schema_mode`, and `column_mapping`. Column entries are `[name, type, not_null]`. |
| `tsql` | `.sql` | One UTF-8 T-SQL script. |
| `tsql_batch` | `.tsql-batch.json` | JSON array of T-SQL scripts, executed separately in order. |
| `shortcut` | `.shortcut.json` | JSON object containing either `shortcuts` create entries or `remove` entries with frozen source and destination addresses. |
| `load_file` | `.payload` | Exact bytes to write for a `write_file` action. A `delete_file` action is the payloadless exception. |
| `runtime_state` | `.runtime-state.json` | Versioned JSON current-state establishment and invalidation instructions. |
| `folder` | none | Target-only folder reconciliation. |
| `sql_endpoint_refresh` | none | Target-only SQL endpoint refresh. |

Payload paths must start with `payload/`, be relative, contain no colon, and contain no empty, `.` or `..` component. A payloadless action has null `payload` and `payload_sha256`. `folder`, `sql_endpoint_refresh`, and `delete_file` reject an attached payload; all other accepted executor forms require one.

## Identity

`bundle_id` is the SHA-256 of UTF-8 canonical JSON for the complete manifest mapping after replacing `bundle_id` with an empty string. Canonical JSON sorts keys and removes presentation whitespace. The digest therefore includes repository identity, targets, ordered work, omissions, changes, runtime-state declarations, selection, and every payload checksum. It includes no timestamp.

The loader verifies payload bytes against `payload_sha256`, but it does **not** recompute or compare `bundle_id` when loading. `bundle_id` is current generation-time content identity, not a cryptographic signature over a manifest received from an untrusted party. Regenerate an edited bundle rather than repairing its manifest.

## Load-time validation

Bundle loading finishes before the installer executes an action. It currently checks:

- YAML parsing, a mapping at the document root, and required deserialisation fields;
- `format_version == 3`;
- supported omission reasons and executors;
- unique target IDs, batch IDs, action IDs, and sequence numbers;
- strictly increasing sequence numbers;
- complete logical item identity and agreement between logical item type and physical target kind;
- non-empty batch target IDs that refer to a declared target;
- no action whose `resource_node_id` is an omitted node;
- required or forbidden payload presence for the executor and action kind;
- executor-specific filename suffixes and payload paths that remain under the bundle root;
- presence of every referenced payload; and
- equality between each payload's SHA-256 and `payload_sha256`.

Construction of nested model values also rejects unsupported target-change effects and object kinds, and empty runtime-state table names. The loader currently ignores unknown mapping keys and does not recompute `bundle_id`; neither behaviour is a format extension guarantee.

## Destination-bound installation

Build reads the selected destination's catalogue and physical inventories before rendering this plan. Install then:

1. loads and validates the local directory or materialised archive;
2. offers the manifest's Lakehouse targets to the Session for Spark attachment;
3. resolves execution capabilities in the selected workspace;
4. executes manifest sequences and actions without replanning; and
5. writes an installation report containing one result for every planned action.

The workspace option supplies execution context. It does not retarget the manifest. Install accepts no catalogue, Environment, item-binding, or target override. It does not reopen source, recompute dependencies, reclassify impact, or substitute later bindings. Generate a new bundle when source, bindings, or destination state changes.

Actions within a batch run serially in manifest order, and the installer currently attempts every action in that batch even if an earlier one fails. If any action in the batch fails, later batches in that sequence are skipped. A failed sequence marks every later sequence and its actions skipped. Earlier side effects remain. Installation provides no operation-wide rollback.

The loader's acceptance of format 3 says only that this implementation accepts that exact format number. It does not establish interchangeability across Weaver releases or an upgrade window.
