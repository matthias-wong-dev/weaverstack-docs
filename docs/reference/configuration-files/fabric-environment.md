# Fabric Environment definition

`weaver fabric environment publish` accepts either an existing Fabric Environment reference or a local Environment definition. The two inputs have different authority boundaries.

## Local directory shape

A local definition is a directory named exactly `<Name>.Environment`. The final `.Environment` suffix is case-sensitive, and `<Name>` must not be empty. The directory may live anywhere; `Environment/` is a project convention, not part of the parser contract.

The directory name supplies the Fabric Environment name. Workspace configuration may name a different Environment and is not consulted for that name when `--path` is used.

The accepted relative files are:

| Relative path | Meaning |
| --- | --- |
| `.platform` | Fabric platform metadata. |
| `Libraries/PublicLibraries/environment.yml` | External package declaration. |
| `Setting/Sparkcompute.yml` | Spark compute settings. |
| `Libraries/CustomLibraries/<file>` | A custom library. Any file name below this directory is accepted as definition content. |

Subdirectories may be absent. Any file outside those four parts is a validation error. A missing path, a file in place of the `<Name>.Environment` directory, and a malformed directory name are also errors.

`initialise` writes the conventional path `Environment/<Name>.Environment/` with `.platform` and `Libraries/PublicLibraries/environment.yml`. It does not generate `Setting/Sparkcompute.yml`; Fabric then applies the workspace's Spark settings.

## `environment.yml`

`Libraries/PublicLibraries/environment.yml` may be absent or empty. When present, it must be a YAML mapping. If it has `dependencies`, that value must be a list. A `pip` entry under that list must itself be a list:

```yaml
dependencies:
  - pip:
      - pandas==2.3.0
      - --index-url https://packages.example.invalid/simple
      - weaverstack
```

Weaver edits this pip list as text rather than round-tripping the full YAML document. Comments, ordering, pip options, unrelated dependencies, and authored spellings of dependencies Weaver does not replace are retained. If no pip section exists, publication adds one.

Invalid YAML, a non-mapping document, non-list `dependencies`, or a non-list `pip` section is rejected before publication.

## Weaver's overlay

The selected publication mode owns Weaver's package entries; it does not treat an authored Weaver requirement as authoritative.

### Released mode

Released mode removes case-insensitive variants and duplicates of the `weaverstack` requirement, then adds the requirement for the publishing client:

- a released client adds `weaverstack==<client-version>`;
- a development or prerelease client adds unpinned `weaverstack` because that version has no corresponding released package.

It removes staged Weaver custom wheels. Other external requirements and custom libraries remain.

### Development mode

`--dev` finds the Weaver source checkout by walking upward from the installed module until it finds `pyproject.toml`. It builds a wheel into that checkout's `dist/` directory using the running Python interpreter and `python -m build`.

Development mode:

- removes every `weaverstack` requirement from `environment.yml`;
- adds the checkout's Fabric runtime requirements explicitly, because Fabric does not install dependencies from a custom wheel;
- uploads the newly built Weaver wheel under `Libraries/CustomLibraries/`; and
- removes stale Weaver wheels while preserving unrelated custom libraries.

Runtime requirements come from the checkout's `project.dependencies`. Desktop transports and build tools are excluded: `azure-identity`, `requests`, `build`, `prompt-toolkit`, and `packaging`. Existing authored requirements are retained when they can satisfy Weaver's requirement. A provable exact-pin or bounds conflict is rejected before any Environment changes are staged, with the conflicting authored and required specifiers named in the error.

A missing checkout root, failed wheel build, or wheel build that produces no matching `weaverstack-*.whl` is an error.

## Local and remote authority

### Publishing with `--path`

The local directory supplies the complete desired definition. Weaver overlays its released requirement or development wheel and dependencies, then creates or updates the named Fabric Environment from that definition.

This route makes local content authoritative for `.platform`, Spark settings, external libraries, and custom libraries represented by the directory. Do not use `--path` as a partial patch: remote definition parts absent locally are absent from the desired definition.

### Publishing an existing Environment by name

The remote Fabric Environment is authoritative for everything except Weaver's own library entries. The Environment must already exist. Weaver reads its staged libraries, changes the Weaver requirement or Weaver wheel and required runtime packages, and preserves other libraries and settings.

An unqualified Environment needs `--workspace` or workspace configuration. A `Workspace/Environment` reference supplies the owner. If an explicit workspace conflicts with that owner, publication fails.

`--path` and a positional Environment reference are mutually exclusive; one of them is required.

## Publication and preservation

After staging a change, Weaver asks Fabric to publish and waits for a terminal result. `success` and `succeeded` are accepted. A failed or cancelled result is an error; when Fabric identifies failed components, the error names them. A timeout reports the last observed state.

If the desired definition already matches what Fabric preserves and the Environment's published state is successful, no update or publish request is sent. The result uses `action: unchanged`, `published: false`, and `publish_status: AlreadyInstalled`.

Definition comparison accounts for Fabric's observed normalization of line endings, JSON/YAML formatting, and `runtime_version` quoting. Weaver custom-wheel bytes are compared by their content-addressed filename; unrelated custom libraries are compared by bytes.

Environment publication is not a catalogue operation. It changes the Python runtime available to notebooks and Livy sessions; it does not build project documents or install a build bundle.

## Current validation boundary

Validation covers the directory name and supported files, the `environment.yml` container shapes, Weaver dependency conflicts, workspace ownership, wheel creation, and Fabric's publish result. It does not define a general schema for `.platform`, `Setting/Sparkcompute.yml`, arbitrary external packages, or arbitrary custom-library bytes beyond what Fabric accepts.

The paths and overlay rules on this page describe the current implementation. They are not a versioned Environment-definition compatibility promise.
