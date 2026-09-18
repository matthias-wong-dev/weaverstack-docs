# Build bundle

A build bundle is frozen installation input. `weaver build --bundle-only` writes the supported CLI handoff as a local directory; `weaver install` accepts that directory or a local `.weaver.zip` archive.

The CLI does not expose an archive-creation command. The Python implementation can persist archives for internal and programmatic workflows, but that does not create a CLI packaging interface. Do not rename a directory to `.weaver.zip`: Install chooses archive handling from the suffix.

## Directory shape

The bundle root has this shape:

```text
bundle/
├── plan.yml
└── payload/
    ├── <sequence-and-action path>.spark.sql
    ├── <sequence-and-action path>.sql
    ├── <sequence-and-action path>.json
    └── <sequence-and-action path>.payload
```

`plan.yml` is the canonical manifest. Payload files are generated installation inputs, not copies of the project source. Some action executors are target-only and have no payload.

The writer emits payloads first and `plan.yml` last. A directory without the manifest is not an installable bundle. `--bundle-path` requires `--bundle-only`; the requested path must not exist or must be an empty directory. When no path is supplied, Build creates a durable temporary directory and reports it as `bundle_path`.

## Archive input

Install recognizes an archive only when its local path ends with `.weaver.zip`. The ZIP entries must contain `plan.yml` at the archive root and payload paths directly below `payload/`; an extra wrapping directory is not accepted because the extracted root then has no manifest.

Archive extraction rejects:

- absolute member paths;
- empty, `.` or `..` path components; and
- symbolic-link entries.

The archive is materialized into a temporary local directory, validated there, and removed when installation finishes. Payload reads come from that materialized bundle, not from a target Lakehouse store.

Install rejects URLs for both directories and archives. Download the complete handoff to local storage first.

## Manifest

The current manifest format is `format_version: 3`. This Weaver implementation writes and accepts only that value. An unsupported value is rejected with an instruction to regenerate the bundle using the installing Weaver version. This is exact-version acceptance, not a compatibility window or a promise that another Weaver release accepts format 3.

Current top-level manifest fields are:

| Field | Meaning |
| --- | --- |
| `format_version` | Bundle representation version; currently `3`. |
| `bundle_id` | SHA-256 identity of the canonical manifest with this field blanked. |
| `repository_name` | Name of the prepared source repository. |
| `repository_signature` | Signature of the prepared repository state. |
| `targets` | Frozen physical target descriptors. |
| `sequences` | Ordered execution barriers containing target batches and actions. |
| `omitted_nodes` | Repository nodes omitted from the plan and their reasons. |
| `target_changes` | Added and removed object summaries keyed by target ID. |
| `runtime_state` | Current-state rows the plan invalidates. |
| `runtime_state_established` | Current-state rows the plan establishes. |
| `selection` | Impact and selected build/drop identities. |

A target contains required `id`, `kind`, and `item_id`, with optional `item_name`, workspace identifiers and names, `sql_endpoint_id`, and logical item type/name. The target `id` is local to the manifest. Physical names and IDs are frozen during Build; Install has no item-binding, catalogue, or Environment override.

A sequence contains `number`, `description`, and `batches`. A batch contains `id`, `target_id`, and `actions`. An action contains:

```text
id, kind, resource_node_id, executor, payload, payload_sha256
```

`source_path` appears when the action can identify an authored source, and `awaits_name_release: true` appears only for the shortcut-replacement case. Payloadless actions store null `payload` and `payload_sha256`.

`selection` contains `impact`, `prohibited`, `selected_for_drop`, and `selected_for_build`. `impact` contains `new`, `changed`, and `impacted_descendants`.

## Identity and payload integrity

`bundle_id` is the lowercase hexadecimal SHA-256 of a canonical JSON encoding of the whole manifest after replacing the stored `bundle_id` with an empty string. Canonicalization sorts keys, removes presentation whitespace, and uses UTF-8. The identity therefore includes the format version, repository signature, targets, ordered work, selection, runtime-state declarations, and every recorded payload hash. Timestamps do not participate.

Each payload-bearing action records its bundle-relative `payload` path and `payload_sha256`. Before returning a loaded bundle, Weaver validates that:

- every required payload exists;
- each payload's SHA-256 equals `payload_sha256`;
- payload paths are relative, contain no empty, `.` or `..` component, contain no drive/URL colon, and begin with `payload/`;
- the payload extension matches its executor; and
- payloadless executors and delete-file actions do not carry unexpected payloads.

Payload edits are detected by their recorded checksums. The loader does not currently recompute `bundle_id` from the manifest, so `bundle_id` is generation-time content identity rather than a signature over an untrusted manifest. Treat any manifest edit as invalid handoff procedure and regenerate the bundle instead of repairing it manually.

## Structural validation

Before checking payload bytes, the loader validates the complete plan structure. Current checks include:

- exact format version;
- supported omission reasons and executors;
- unique target, batch, action, and sequence identities;
- complete logical item identity where one half is present;
- agreement between logical item type and physical target kind;
- batches referring only to known targets;
- strictly increasing, unique sequence numbers;
- actions not installing an omitted node; and
- the executor's required payload shape.

Malformed YAML, a non-mapping manifest, and missing required manifest fields are also rejected. Bundle loading and all these checks complete before the installer runs an action.

## Installation boundary

Build plans against the selected destination's current catalogue and physical inventory. The manifest carries that settled plan. Install:

1. loads and validates the local bundle;
2. offers the bundle's Lakehouse targets to the Session for Spark attachment;
3. executes sequences in manifest order; and
4. returns an installation report with one result per planned action.

Install does not reopen project source, recompute dependencies, reclassify impact, or substitute later target bindings. It supplies the selected workspace as the execution context, but the manifest still names the planned physical targets. Generate a new bundle when source, bindings, or relevant destination state changes.

A failed action stops later sequences and leaves completed side effects in place; installation does not roll them back. The report marks subsequent work according to the installer's current failure handling.

## Compatibility boundary

The current loader accepts format 3 only. That fact does not guarantee that all format-3 bundles from another release are interchangeable, that future releases continue to accept format 3, or that there is an upgrade window. The supported handoff is a complete, unedited bundle generated for the destination and accepted by the installing Weaver version.
