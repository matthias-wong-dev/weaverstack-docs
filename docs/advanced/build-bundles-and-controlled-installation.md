# Build bundles and controlled installation

A build bundle separates installation planning from installation execution. One process reads reviewed project source and the intended destination, then emits frozen installation work. Another process transfers and installs that work without reopening the project.

```text
check source
→ plan bundle for destination
→ review and transfer
→ install frozen work
→ Load → Test → Health
```

This is a controlled handoff, not a general promotion or retargeting mechanism.

## Check source before planning

Run Check against the reviewed project revision first. Check parses the Weaver documents locally and catches declaration errors without contacting Fabric. It does not prove that the destination exists, that credentials can reach it or that the planned installation will succeed.

Keep the reviewed source revision as the provenance for the handoff. A bundle contains generated installation inputs, not another copy of the project repository.

## Plan against the intended destination

Bundle-only Build still reads the destination catalogue and physical inventory. It uses the selected workspace, catalogue and item bindings to decide what is new, changed, affected or removable, then freezes:

- the selected physical targets;
- ordered installation sequences and actions;
- generated payloads;
- destination-specific state changes; and
- integrity hashes for payload-bearing actions.

Planning therefore needs destination access even though it does not install anything. Generate a separate bundle for each destination. Changing a workspace configuration after generation does not rewrite the targets already recorded in the bundle.

## Review and transfer one complete artifact

Review the Build selection and the destination for which it was planned. Transfer the complete bundle directory, or a supported local bundle archive, through the organisation's artifact controls. Keep its manifest and payload tree together.

Do not edit the manifest or payloads. Install validates the supported representation, structure and payload checksums before executing actions, but the bundle is still a handoff artifact rather than a substitute for source review or artifact-store controls. Exact files, fields and validation rules are in the [Build bundle reference](../reference/build-bundle-format.md).

Credentials are not part of the bundle. The installation process authenticates independently to the workspace in which the frozen targets exist.

## Install frozen work without replanning

Install loads and validates the local bundle, prepares the target capabilities it needs, then executes the recorded sequences in order. It does not:

- reread project source;
- rediscover dependencies;
- recalculate Build impact;
- replace the recorded physical targets with bindings from another configuration; or
- choose a different catalogue or Fabric Environment for the plan.

The workspace supplies execution context; the bundle supplies the installation targets and work. If the reviewed source, intended bindings or relevant destination state changed, return to bundle planning and produce a new artifact.

A failed installation action stops later sequences. Completed physical changes remain applied, and later planned work is reported as not completed. Installation is not an operation-wide transaction. Inspect the report and destination state before deciding whether to correct the cause and reinstall or generate a new bundle.

## Continue the lifecycle at the destination

Installing a bundle changes installed definitions and catalogue state. It does not run the installed data or validation work. Complete the destination lifecycle with:

```text
Load → Test → Health
```

Use Health and the catalogue to inspect the estate established by those operations. Keep their evidence with the bundle identity and reviewed source revision so the handoff, installation and runtime results can be correlated.

See the [`build`](../reference/cli/build.md) and [`install`](../reference/cli/install.md) references for exact command syntax and the [Build behaviour](../reference/operation-behaviour/build.md) reference for installation barriers. [Automation and execution contexts](automation-and-execution-contexts.md) explains unattended policy, credentials and machine-readable results.
