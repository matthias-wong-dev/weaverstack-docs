# Development-runtime procedures (maintainer only)

These procedures belong to pre-release verification, not public onboarding. The public draft is now written for the intended matching PyPI release under Matthias's instruction. This does not assert that the release has been uploaded or authorise uploading it.

## Prior snapshot installation

## Install the documented snapshot

!!! warning "Private documentation preview"
    These pages describe Weaver revision `74b4d15ee65ed2740593af1f4d459771b801b132`. The published PyPI package `0.9.0` does not contain all of these interfaces. Public publication is held until its matching package is available. For this preview, use the exact source target below rather than an unqualified package install.

Use Python 3.11 or later and Git. In a Python environment:

```bash
python -m pip install "weaverstack @ git+https://github.com/matthias-wong-dev/weaverstack.git@74b4d15ee65ed2740593af1f4d459771b801b132"
weaver --version
weaver --help
```

The installation provides the `weaver` command and importable `weaver` package. The snapshot has a derived development version; it is not a new named release. The help should include Build `--dry-run`, Load recursive selection, invocation concurrency and Unbind.

Check an existing project without service access:

```bash
weaver check .
```

Check parses declarations and native project files. It does not deploy, run DAX, execute SQL or establish workspace permissions.


## When the preview needs a hosted runtime

A Lakehouse tutorial that publishes `--dev` needs a checkout-backed installation so Weaver can build the exact local wheel. Use this alternative to the direct Git package install above:

```bash
git clone https://github.com/matthias-wong-dev/weaverstack.git
git -C weaverstack checkout 74b4d15ee65ed2740593af1f4d459771b801b132
python -m pip install -e "./weaverstack[dev]"
```

Keep that checkout at the documented revision, return to the tutorial project directory, and use its Environment publication step. Do not overlay an unpublished development version from PyPI. A notebook already running in Fabric needs the matching package and dependencies in its attached runtime; it does not need a second remote session merely to run in that workspace.


## Pre-release source checkout

Use the commands above without `--dev` for a released Weaver installation. `--dev` is only for testing an unreleased source checkout in Fabric: it builds that checkout as a wheel and publishes the wheel with its Fabric runtime dependencies.

Install the checkout in editable mode so the `weaver` executable and imported module both resolve to that source tree, then invoke that executable:

```bash
git clone https://github.com/matthias-wong-dev/weaverstack.git
cd weaverstack
python -m venv .venv
.venv/bin/python -m pip install -e .

.venv/bin/weaver fabric environment publish \
  --path ../parcel-ops/Environment/ParcelRuntime.Environment \
  --workspace "Parcel Development" \
  --dev
```

On Windows, use `.venv\Scripts\python.exe` and `.venv\Scripts\weaver.exe`. The package declares the wheel builder needed by `--dev`. The command finds the checkout from the installed `weaver` module, not from an unrelated `pyproject.toml` in the current directory. A released installation should continue to use normal publication rather than `--dev`.

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
