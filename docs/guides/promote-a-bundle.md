# Promote a build bundle

Weaver has a public split-build route: `weaver build --bundle-only` writes a local bundle directory, and `weaver install` installs that frozen bundle later. Use it when one process prepares and approves installation work and another process applies exactly that work.

This route is a bundle handoff, not a general retargeting mechanism. Build plans against a selected destination workspace and its current catalogue and target state. Install does not reopen project source, recalculate dependencies or replace the bundle's physical target names.

## Prerequisites

- [Install Weaver](../get-started/installation.md) in both processes. Use compatible installations: the installer accepts only its supported bundle format and tells you to regenerate an unsupported bundle with that Weaver version.
- Make the project and the destination workspace configuration available to the planning process. This documentation repository includes the checked example at `examples/parcel-automation/`.
- Authenticate both processes for the destination workspace. Bundle planning reads that workspace's catalogue and target inventory even though `--bundle-only` does not install the plan.
- Transfer the complete bundle directory through your normal artifact store without editing it. Keep credentials outside the bundle and repository.

## Check the source

From the documentation repository root:

```bash
weaver check examples/parcel-automation \
  --non-interactive \
  --json > check.json
```

A zero exit status confirms that the project source parses locally. This checkpoint does not contact Fabric and does not establish that the destination can accept the build.

## Plan a bundle for the destination

Use the destination's workspace configuration while creating the bundle:

```bash
rm -rf ./dist/parcel-operations

weaver build examples/parcel-automation \
  --item Warehouse/Operations \
  --workspace-config examples/parcel-automation/workspace-config.yml \
  --bundle-only \
  --bundle-path ./dist/parcel-operations \
  --non-interactive \
  --json > build-bundle.json
```

`--bundle-path` requires `--bundle-only`. The path must not exist or must be an empty directory. A successful result has `"installation": false`, a `bundle_id`, a `bundle_path` and `"status": "succeeded"`.

The directory contains `plan.yml` and generated files under `payload/`. It does not contain a copy of the project repository. The plan freezes the selected physical targets, ordered installation actions, generated definitions and payload checksums from this planning run.

Review the Build selection and retain the complete directory as one artifact. Do not edit `plan.yml` or payloads: Install validates the bundle structure, format and payload checksums before running an action.

## Transfer and install the same bundle

Move or copy `./dist/parcel-operations/` to the installation process with its directory structure intact. Then install it into the workspace for which it was planned:

```bash
weaver install ./dist/parcel-operations \
  --workspace-config examples/parcel-automation/workspace-config.yml \
  --non-interactive \
  --json > install-bundle.json
```

The checkpoint is a zero exit status and an installation report whose status is `succeeded` and whose `bundle_id` matches `build-bundle.json`. The installer runs the frozen sequences in order. A failed action stops later sequences, marks remaining planned work skipped and returns non-zero; completed changes are not rolled back. See [Fault tolerance](../core-concepts/fault-tolerance.md).

`weaver install` accepts a local bundle directory or a local `.weaver.zip` archive. The public CLI creates a directory; it does not expose a command that packages that directory as `.weaver.zip`. This guide therefore uses the complete directory rather than inventing an archive command. Install rejects URL locations, so download an approved artifact to local storage before invoking it.

## Respect compatibility and host boundaries

- **Generate per destination.** Build reads the destination catalogue and target inventories and embeds target names in the bundle. Install accepts a workspace selection, not new item bindings, catalogue selection or Environment selection. To use another destination configuration, generate another bundle against that destination.
- **Do not treat delayed installation as replanning.** Install validates the frozen files but does not reread source or recalculate the plan from later destination state. If the intended source, bindings or destination state changed, generate and review a new bundle.
- **Keep source access on the Build side.** A desktop Build accepts a local project folder. An `abfss://` source is supported only while Weaver is running inside a Fabric session. Install still requires a local bundle directory or archive.
- **Match the bundle format.** The installer accepts exactly the bundle format it supports. An unsupported format, unknown installation method, malformed target, missing payload or checksum mismatch is rejected before installation actions run.
- **Check host capabilities.** The same bundle can be installed by a desktop Session or inside Fabric, but a host may skip an operation it cannot perform. For example, a host without SQL endpoint refresh capability records that refresh as skipped rather than inferring replacement work. Treat the installation report as the outcome.

These are source- and test-backed interface boundaries. The commands above were not run against a live Fabric workspace as part of this documentation check; a local parser or bundle test is not evidence of a live destination installation.

## Know what the bundle is not

A build bundle is generated installation input. It is not:

- a Git commit, tag, release archive or replacement for source review;
- a copy of the project source;
- a [Mirror](../core-concepts/development-cycle.md), which creates a development catalogue and borrowed estate from another installed catalogue;
- a portable request to choose new physical targets at install time.

Use Git to review and version the authored Weaver documents. Use a bundle to hand frozen installation work to another process. Use Mirror when the task is to establish a development estate from another catalogue.

## Next actions

After installation, run Load, Test and Health against the destination and inspect the resulting [Catalogue](../core-concepts/catalogue.md). [Weaver operations](../core-concepts/weaver-operations.md) explains why installation changes definitions but does not run their data or validation work. See [Sessions and workflows](sessions-and-workflows.md), [Run Weaver unattended](automation.md), the [CLI reference](../reference/cli.md) and [Contracts](../contracts/index.md) for composition, automation and exact command surfaces.
