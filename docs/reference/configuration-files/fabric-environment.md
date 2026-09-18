# Fabric Environment definition

`weaver fabric environment publish` has two publication routes:

- `--path <Name>.Environment` sends a local definition as the complete desired Environment definition;
- positional `ENVIRONMENT` updates Weaver's libraries in an existing remote Environment while leaving the remote definition authoritative.

This publication is separate from workspace configuration. The `environment` key in `workspace-config.yml` selects a published Environment for Spark work; it does not create or publish one.

## Local definition directory

A local definition is a directory whose basename is exactly `<Name>.Environment`.

- `.Environment` is case-sensitive.
- `<Name>` must be non-empty.
- The directory may be anywhere. `Environment/` is a project convention, not a discovery rule.
- The basename supplies the Fabric Environment name. A positional Environment reference and the workspace configuration's `environment` value do not rename a `--path` publication.

A complete definition can have this shape:

```text
Environment/
└── ParcelRuntime.Environment/
    ├── .platform
    ├── Libraries/
    │   ├── PublicLibraries/
    │   │   └── environment.yml
    │   └── CustomLibraries/
    │       └── parcel_rules-1.0.0-py3-none-any.whl
    └── Setting/
        └── Sparkcompute.yml
```

Only these file paths are accepted:

| Relative path | Cardinality | Weaver validation |
| --- | --- | --- |
| `.platform` | zero or one | Carried as bytes. Weaver does not define or validate its JSON schema. |
| `Libraries/PublicLibraries/environment.yml` | zero or one | YAML container shape and the first `pip` list are validated as described below. |
| `Setting/Sparkcompute.yml` | zero or one | Carried as bytes. Weaver does not define or validate its keys. |
| `Libraries/CustomLibraries/<relative-file>` | zero or more | Any file beneath this directory is carried as bytes, including files in nested subdirectories. |

Directories may be absent, and the definition may initially contain no files. Any file outside those paths is rejected before publication. Fabric remains authoritative for the contents it accepts inside `.platform`, `Setting/Sparkcompute.yml` and custom library files.

`weaver initialise` writes only `.platform` and `Libraries/PublicLibraries/environment.yml` beneath `Environment/<Name>.Environment/`. It omits `Setting/Sparkcompute.yml`, so Fabric applies the workspace's Spark settings.

## Complete example

`.platform`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Environment",
    "displayName": "ParcelRuntime"
  },
  "config": {
    "version": "2.0"
  }
}
```

`Libraries/PublicLibraries/environment.yml`:

```yaml
dependencies:
  - pip:
      - pandas==2.3.0
      - --index-url https://packages.example.invalid/simple
      - pyarrow==20.0.0
```

`Setting/Sparkcompute.yml`:

```yaml
runtime_version: "1.3"
driver_cores: 8
```

The `.platform` and Spark settings above are passed to Fabric; their keys are not a Weaver configuration schema. The custom wheel and external requirements are independent inputs.

## `environment.yml` shape

`Libraries/PublicLibraries/environment.yml` is optional and may be empty. When non-empty, it must parse as a YAML mapping.

| Key or entry | Accepted shape | Default when absent |
| --- | --- | --- |
| document | mapping | empty library list |
| `dependencies` | list | no declared dependencies |
| a `pip` entry inside `dependencies` | mapping key whose value is a list | publication adds a pip section when Weaver needs one |
| each pip-list value | YAML value converted to text | — |

Other top-level keys and non-`pip` dependency entries are preserved rather than interpreted by Weaver. Weaver edits the first dependency mapping containing `pip`. Invalid YAML, a non-mapping document, non-list `dependencies`, or a non-list `pip` value is rejected.

The pip list may contain package requirements and pip options such as `--index-url`. Weaver edits it as text so comments, ordering, options, unrelated dependency entries and authored requirement spellings can remain intact.

## Released publication

Released mode is the default. It owns the `weaverstack` distribution entry:

1. remove all requirements whose distribution name normalises to `weaverstack`, including case, hyphen, underscore and dot variants;
2. remove staged custom wheels named `weaverstack-*.whl`;
3. add `weaverstack==<client-version>` for a released client, or unpinned `weaverstack` when the publishing client is a development or prerelease build.

Duplicate Weaver requirements collapse to one managed requirement. Other requirements and custom libraries remain.

```bash
weaver fabric environment publish \
  --path Environment/ParcelRuntime.Environment \
  --workspace-config workspace-development.yml
```

## Development publication

`--dev` publishes the running checkout rather than a PyPI Weaver requirement. Weaver finds the checkout by walking upward from its installed module until it finds `pyproject.toml`, then runs the active Python interpreter with:

```text
python -m build --wheel --outdir <checkout>/dist <checkout>
```

Development mode:

- removes every `weaverstack` requirement from `environment.yml`;
- builds and uploads one `weaverstack-*.whl` beneath `Libraries/CustomLibraries/`;
- removes stale Weaver wheels while preserving unrelated custom libraries;
- reads `project.dependencies` from the checkout and adds the dependencies needed inside Fabric; and
- excludes desktop transports and build tools: `azure-identity`, `requests`, `build`, `prompt-toolkit` and `packaging`.

An existing authored requirement is retained when Weaver cannot prove a conflict. A conflicting exact pin or non-overlapping bound is rejected before Environment changes are staged, and the error names both specifiers.

A checkout without `pyproject.toml`, a failed wheel build or a build producing no matching wheel is an error.

## Local-definition authority

With `--path`, the local directory supplies the complete desired definition. Weaver overlays its released requirement or development libraries in memory and does not modify the local files. It then creates the named remote Environment if absent, or updates it if present.

Files absent from the local directory are absent from the desired definition. Do not use `--path` as a partial patch to preserve remote definition parts that are not represented locally.

Publishing a local definition requires a workspace from `--workspace`, `--workspace-config` or normal workspace discovery. The selected configuration's `environment` key is not consulted for the Environment name.

## Existing-Environment authority

Without `--path`, name an Environment that already exists:

```bash
weaver fabric environment publish ParcelRuntime \
  --workspace-config workspace-development.yml

weaver fabric environment publish "Platform Runtimes/ParcelRuntime"
```

The positional reference accepts `Environment` or `Workspace/Environment`.

- An unqualified reference requires a resolved workspace.
- A qualified reference supplies its owner workspace. With neither `--workspace` nor `--workspace-config`, this form uses that owner directly and does not perform automatic workspace-configuration discovery.
- A workspace selected with `--workspace` or `--workspace-config` must match the qualified owner.
- The Environment must already exist; only the `--path` route creates one.
- A positional reference and `--path` are alternative inputs; supply exactly one.

On this route, the remote Environment is authoritative for platform metadata, Spark settings, external libraries other than Weaver's managed entries and unrelated custom libraries. Weaver reads staged libraries and changes only the Weaver requirement, Weaver wheel and required development dependencies.

## Publication result and unchanged definitions

After staging a change, Weaver asks Fabric to publish and waits up to 1,800 seconds. Terminal `success` and `succeeded` states are accepted. Failed or cancelled publication is an error; failed component names are included when Fabric provides them. A timeout reports the last observed state.

No update or publish request is sent when the desired managed definition already matches and the Environment's published state is successful. The result then reports:

```text
action: unchanged
published: false
publish_status: AlreadyInstalled
```

For comparison, Weaver accounts for Fabric's observed normalisation of line endings, JSON/YAML formatting and `runtime_version` quoting. A Weaver wheel is compared by its content-addressed filename; unrelated custom libraries are compared by bytes.

Environment publication changes the Python runtime available to notebooks and Livy sessions. It does not Build project documents, install a build bundle, select a catalogue or run Mirror.

The file paths, overlay and comparison rules above describe the implemented interface. Weaver does not define a general schema for Fabric's `.platform` or `Sparkcompute.yml` content.
