# `weaver mirror`

<!-- BEGIN GENERATED CLI -->
```text
usage: weaver mirror [-h] [--item ITEM[=TARGET]] [--no-item]
                     [--mirror CATALOGUE] [--workspace WORKSPACE]
                     [--workspace-config WORKSPACE_CONFIG]
                     [--environment ENVIRONMENT] [--catalogue CATALOGUE]
                     [--yes] [--json] [--non-interactive]

options:
  -h, --help            show this help message and exit
  --item ITEM[=TARGET]  A logical item to rebind, such as Warehouse/Model or
                        Warehouse/Model=Warehouse/Model_Dev. Repeat to select
                        multiple items. Naming none selects every configured
                        target.
  --no-item             Fork the catalogue and rebind no physical item.
  --mirror CATALOGUE    Catalogue to fork, for example Warehouse/Weaver.
                        Overrides mirror: in workspace configuration.
  --workspace WORKSPACE
                        Fabric Workspace name.
  --workspace-config WORKSPACE_CONFIG
                        Workspace configuration file.
  --environment ENVIRONMENT
                        Fabric Environment name or Workspace/Environment
                        reference.
  --catalogue CATALOGUE
                        Where the Weaver catalogue lives, for example
                        Warehouse/Weaver.
  --yes                 Authorise emptying the destinations without asking.
  --json                Emit the result as JSON.
  --non-interactive     Do not read stdin, wait for a keypress or open browser
                        sign-in. Missing authorisation or required input is an
                        error.
```
<!-- END GENERATED CLI -->

## Responsibility and selection

`mirror` forks the catalogue selected by `--mirror` into the destination catalogue selected by `--catalogue`. Either value may instead come from workspace configuration.

`--item ITEM` selects a logical Weaver item and uses its configured destination target. `ITEM=TARGET` supplies or overrides that physical destination binding. Repeat the option to select several items. Omitting `--item` selects every configured target; use `--no-item` to fork only the catalogue. `--item` and `--no-item` cannot be combined.

## Execution

Mirroring is destructive at the destination. Weaver resolves the source and destination together, proves that it can read the source catalogue, settles the item mappings and determines every destination that will be emptied before asking for confirmation. Execution uses that same settled plan.

The destination catalogue is emptied and rebuilt from the source catalogue. Selected destination items are also emptied and reconstructed from their source bindings. The source catalogue is read before any destination is changed.

`mirror` has no `--dry-run` option. In human output, the settled plan is always displayed before confirmation; declining the prompt or withholding `--yes` when no prompt is available leaves the destinations unchanged.

## Interaction

Without `--yes`, an interactive invocation asks once after displaying the settled source, destination and target mappings. `--yes` authorises every destination named by that plan but does not hide the preview.

`--non-interactive` prevents prompts and browser sign-in; it does not approve emptying. Unattended execution requires `--non-interactive --yes`. JSON mode never prompts and requires `--yes`.

## Output and exit behaviour

Human output first identifies the source catalogue, destination catalogue and selected target mappings. Completion output reports the catalogue fork, the number of logical items mirrored and the number of physical destinations emptied.

`--json --yes` writes one result document. Without `--yes`, JSON mode writes one failure document and performs no mutation. Treat these documents as command output, not as a versioned schema guarantee.

The command exits `0` after a completed mirror. Missing or declined confirmation exits `1`. Source validation happens before confirmation, so an unreadable or incompatible source fails without emptying a destination. Other planning, authentication and Fabric failures also produce a non-zero status.

## Examples

Preview the settled plan interactively and answer the confirmation prompt:

```bash
weaver mirror \
  --workspace-config workspace-development.yml \
  --item Warehouse/Operations=Warehouse/ParcelOperations_Dev
```

Fork only the catalogue in unattended execution:

```bash
weaver mirror \
  --workspace "Parcel Development" \
  --mirror Warehouse/ParcelCatalogue \
  --catalogue Warehouse/ParcelCatalogue_Dev \
  --no-item \
  --non-interactive \
  --yes
```
