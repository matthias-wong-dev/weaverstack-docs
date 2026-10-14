# Running Python in Fabric

Publish the Python packages once, then keep editing and building your project. The Fabric Environment supplies Weaver to hosted Spark work; it is separate from the Lakehouse and catalogue bindings in your workspace configuration.

The [first Python task](python.md) creates `Environment/Weaver.Environment` and publishes it before Build. Use this page when setting up that runtime or changing its packages. The [mutable-source variation](incremental.md) uses the same process with its Environment named `ParcelRuntime`.

## Bind the runtime you will use

A complete configuration for the Landing journey is:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
environment: Weaver

targets:
  Lakehouse/Landing: Landing
```

Use your actual workspace and the bindings written by Initialise. `environment` selects the Fabric Environment to attach; it does not create or publish it. For development/production mappings of the whole project, use [Workspace and environment mappings](../estate/environments.md).

Local Check needs no Fabric runtime. Desktop Lakehouse Build, Load and Test use hosted Spark, including when their source is Spark SQL. Build checks the hosted runtime before mutation; not calling authored `read()` does not remove that prerequisite. Load imports your installed Table and Folder code; Test imports or executes installed validations.

## Publish the matching packages

For this source preview, use the [editable source checkout](../getting-started/installation.md#when-the-preview-needs-a-hosted-runtime) at `74b4d15ee65ed2740593af1f4d459771b801b132`, with its build dependencies installed. Keep local and hosted Weaver at the same pinned version. From the Landing project root:

```bash
weaver fabric environment publish \
  --path Environment/Weaver.Environment \
  --workspace-config workspace-config.yml \
  --dev
```

`--dev` builds the matching wheel from that checkout. An unqualified PyPI requirement cannot supply this unpublished development version. For a matching published release, omit `--dev`. Publication creates or updates the selected Environment, overlays the Weaver package requirement and waits for Fabric's terminal publication result. An unchanged successful definition is reported without another publication.

For Tracking, use its `ParcelRuntime` local Environment definition and the configuration from that complete fixture. If it was created in the Fabric portal and no local definition exists, publication can instead use that existing Environment as its authority:

```bash
weaver fabric environment publish ParcelRuntime --dev
```

Run that command from the Tracking project root so the workspace is discovered from its configuration. [Fabric Environment definition](../reference/configuration-files/fabric-environment.md) owns local-directory shape, libraries and existing-Environment authority. A Notebook already in Fabric needs the matching package in its attached runtime, not another remote Spark session.

## Keep the runtime and project changes separate

Republish after changing Environment libraries or the Weaver package mode/version. Editing a Python Table, Folder, Test or Assumption does not itself require republication: Check and Build install project changes. Adding a Spark SQL transformation follows the same project loop.

Build checks matching Weaver version, supported plan format, writer version and required executor capabilities before mutation. A read-only preview does not establish runtime compatibility.

Return to [the first pipeline](python.md#check-build-and-load), or use [the development cycle](../estate/development-cycle.md) for repeated edits. [Session and runtime behaviour](../reference/operation-behaviour/session-runtime.md) and [Environment CLI](../reference/cli/fabric-environment.md) own the exact runtime and publication interfaces.
