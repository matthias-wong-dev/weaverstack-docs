# Machine-readable output

This page records current CLI machine output. Each command owns its result shape; there is no stream of records or schema shared by every command. Each supported invocation writes one indented JSON document. Unless that command exposes a `format_version`, the fields below have no schema-version or forward-compatibility promise.

## Stream and process behaviour

Commands with `--json` write the result document to stdout and do not prompt. Their Session enters machine-output mode, suppressing its ordinary reports and progress; representation tests require stderr to remain empty for normal JSON Load, Test, and Health output. Parser help and parser usage errors happen before command JSON handling and retain `argparse`'s text streams. `fabric environment publish` is the exception to the flag rule: it has no `--json` option, always writes its successful result as JSON to stdout, and can write progress to stderr.

A handled Weaver error under `--json` has this current shape:

```json
{
  "status": "failed",
  "error": {
    "executor": "TDS",
    "message": "..."
  }
}
```

`executor` is omitted when no executor reported the error. Load may also add `report`, containing its partial load report. A Test or Assumption failure that produced a validation report emits that report directly instead of the generic error envelope.

Successful command outcomes normally exit `0`. A report that does not satisfy the command's success condition, a handled Weaver error, a refused confirmation, or a failed waited-for notebook run exits `1`. `argparse` usage errors write diagnostics to stderr and exit `2`. Do not treat this as a universal exit-code protocol for unhandled Python or host failures.

## Commands with `--json`

| Command | Current top-level fields | Current exit condition |
| --- | --- | --- |
| `initialise` / `initialize` | `project_folder`, `workspace`, `resources`, `files`, `example`, `example_added`, `environment_publication`, `environment_definition`, `dry_run`, `next_commands` | `0` for a produced report; handled setup errors return `1` through the error envelope. |
| `doctor` | `workspace`, `authentication`, `workspaces`, `succeeded`, `checks` | `0` only when the report succeeds; otherwise `1`. |
| `check` | `status`, `project_folder` | `0` for valid source; `1` with the error envelope for a Weaver error. |
| `build` | `source`, `items`, `bundle_id`, `installation`, `bundle_path`, `status`, `errors` | `0` when `status` is `succeeded`; otherwise `1`. |
| `install` | `bundle_id`, `status`, `started_at`, `finished_at`, `sequences` | `0` when the installation report succeeds; otherwise `1`. |
| `load` | `requested`, `status`, `dry_run`, `fault_tolerant`, `reload`, `workspace`, `workflow_id`, `started_at`, `finished_at`, `order`, `edges`, `nodes`, `messages` | `0` for `succeeded` or `succeeded_with_rejects`; otherwise `1`. |
| `test` | `status`, `nodes`, `totals`, `workflow_id`, `started_at`, `finished_at` | `0` for a completed passing or planned report; failed or invalid validation returns `1` while still emitting the report. |
| `health` | `format_version`, `generated_at`, `as_of`, `status`, `targets`, `sections`, `current_load`, `load_activity` | `0` only for Green; Amber or Red returns `1`. |
| `wipe --dry-run` | `workspace`, `targets`, `catalogue`, `catalogue_action`, `unbound` | `0` after reporting the settled plan. |
| `wipe` | `workspace`, `plan`, `items`, `unbound`, `dry_run` | `0` after the operation returns; refusal or a handled operation error returns `1`. |
| `mirror` | `workspace`, `source_catalogue`, `destination_catalogue`, `wiped`, `copied`, `uncopied`, `items`, `mirrored`, `status` | `0` after the operation returns; refusal or a handled operation error returns `1`. |
| `fabric notebook push` | `workspace`, `notebook`, `notebook_id`, `source`, `action` | `0` after create or update; handled errors return `1`. |
| `fabric notebook run` | `workspace`, `notebook`, `notebook_id`, `job_url`, `status`, `exit_value` | Waited runs return `0` when completed or deduped. `--no-wait` returns `0` for the accepted job. A handled failure returns `1`. |

Only Health currently includes a top-level JSON `format_version`; its current value is `2`. A Build result's `bundle_id` identifies the bundle contents, but the Build result is not the bundle manifest and has no result format version.

## Commands without JSON result mode

`session`, `workflow`, and `fabric capacity` have no `--json` option. A bare invocation, `--help`, and `--version` also use text output. Their terminal presentation is not a stable machine format; do not parse it as a substitute JSON schema.

## Nested field shapes

### Initialise

`resources[]` has `role`, `name`, `status`, and nullable `action`. `example` has `generated`; `example_added` repeats that Boolean for the current representation. `files` and `next_commands` are arrays of strings. `dry_run` is Boolean.

### Doctor

`checks[]` has `name`, `status`, nullable `detail`, nullable `remedy`, and nullable `via`. Current check statuses are `ok`, `not tested`, `missing`, `failed`, and `error`. `authentication` is a provider mapping and `workspaces[]` contains Fabric workspace mappings; their provider-owned nested fields are not normalized by Weaver.

### Build

`items[]` contains logical item references. `installation` is Boolean and `bundle_path` is a string or null. `errors[]` has `id`, nullable `type`, nullable `message`, nullable `artefact`, and nullable `source`.

### Install

`sequences[]` has `number`, `description`, `status`, and `actions`. Each action has `action_id`, nullable `resource_node_id`, `target_id`, `executor`, `status`, nullable `started_at`, nullable `finished_at`, and nullable `duration_seconds`. `source_path`, `error_type` plus `error_message`, and `details` appear only when present.

### Load

`order[]` contains node IDs and `edges[]` contains two-element node-ID arrays. `nodes[]` has:

- `node_id`, nullable `logical_id`, `physical_target`, `primitive_kind`, and nullable `dispatch_location`;
- `status`, `executed`, nullable `started_at`, and nullable `finished_at`;
- nullable `rows`; and
- `messages[]`.

When present, `rows` is the load result row, including the operation's row counts and result details. Message objects currently carry `code`, `severity`, and `message`, with optional context fields supplied by the run representation. Status vocabulary differs between execution and dry run; do not infer another command's status set from it.

### Test

`totals` has `planned`, `executed`, `passed`, `failed`, `invalid`, `missing_count`, `unexpected_count`, and `violation_count`. `nodes[]` has `logical_id`, `kind`, `physical_target`, `primitive_kind`, nullable `dispatch_location`, `status`, `executed`, `messages`, nullable timestamps, and result-specific count/error fields.

A Test result adds `missing_count`, `unexpected_count`, and nullable `error_message`. An Assumption result adds `violation_count` and nullable `error_message`. When `--name` or `--file` selects one validation and diagnostic rows exist, that node also has `diagnostics`; values such as datetimes and bytes are converted to ISO strings and hexadecimal strings by the CLI JSON renderer.

### Health

`sections` is an object with `load`, `tests`, and `build`. Each section has `status`, `subjects`, `counts`, and `findings`. A finding has `area`, `code`, `severity`, nullable `status`, `message`, nullable `object_id`, nullable `target`, nullable `workflow_id`, nullable timestamps, and nullable `failure_count`.

`current_load` is null or has `workflow_ids`, nullable timestamps, and `counts`. `load_activity[]` has object and target identity, workflow and timing fields, row counts, `is_reload`, and `is_static_skip`. Health timestamps are ISO 8601 strings. `format_version: 2` versions this report only; it says nothing about the other command documents.

### Wipe

A dry-run `targets[]` entry has `target` and Boolean `catalogue`. A completed result embeds that same shape as `plan`. Its `items[]` entries have `target`, `outcome`, Boolean `catalogue`, Boolean `unbound`, and a `counts` mapping. Top-level `unbound` is null or the catalogue-unbind result mapping.

### Mirror

`copied` maps catalogue table names to copied row counts. `uncopied[]` names historical catalogue tables rebuilt without copied rows. `items[]` names mirrored logical items. `mirrored` maps each item to the operation-specific result: all item results include `source` and `target`, while Lakehouse and Warehouse entries expose different count fields for the physical work performed.

### Fabric notebooks

Notebook push `action` is currently `created` or `updated`. Notebook run preserves Fabric's status spelling. With `--no-wait`, the current status is `Accepted` and `exit_value` is null.

## Environment publication JSON

`weaver fabric environment publish` has no `--json` option because JSON is its only successful result rendering. Its current fields are:

```text
workspace_name, workspace_id,
environment_name, environment_id,
source_path, mode, weaver_requirement, wheel_filename,
removed_wheels, action, published, publish_status, timings
```

`source_path`, `weaver_requirement`, and `wheel_filename` are nullable. `removed_wheels` is an array. `mode` is `released` or `dev`; `action` is `created`, `updated`, or `unchanged`; `published` records whether this invocation asked Fabric to publish. `timings` is a mapping of measured phase names to seconds and the CLI adds `total`.

This document has no `format_version`. On a handled publication error, this command writes a human-readable diagnostic to stderr, writes no JSON result, and exits `1`: unlike the commands with `--json`, it has no JSON error mode.

## Compatibility boundary

These are the fields emitted by the referenced source revision and pinned by its representation tests. Absence of `format_version` is not an implicit version 1. Scripts should validate the command-specific fields they need and reject an unexpected shape; this page does not promise that unversioned documents remain unchanged in later releases.
