# CLI reference

```text
weaver [--version] command ...
```

Run `weaver <command> --help` for the exact options in the installed version. This page records command responsibility and the selection grammar that differs between commands.

## Commands

| Command | Purpose |
| --- | --- |
| `session` | Run lifecycle commands in one persistent Session. |
| `workflow NAME` | Run a named sequence from `workflow.yml` in one Session. |
| `initialise` | Create or adopt named Fabric items and write a project. The `initialize` spelling is also accepted. |
| `doctor` | Check authentication and Fabric connectivity for a named workspace without reading a project. |
| `check [PROJECT_FOLDER]` | Parse and validate a project without contacting Fabric. |
| `build [SOURCE]` | Build project structure into selected logical items and install it, unless bundle-only mode is selected. |
| `install BUNDLE` | Install a previously built bundle directory or `.weaver.zip` archive. |
| `load [ITEM ...]` | Run installed loadable objects for the selected logical items. |
| `test [ITEM ...]` | Run installed Tests and Assumptions for the selected logical items. |
| `health` | Report load, test and build health for installed items. |
| `wipe [TARGET ...]` | Empty physical Lakehouses or Warehouses; with no targets, use the estate recorded by the catalogue. |
| `mirror` | Fork another catalogue's installed estate into the current workspace's catalogue. |
| `fabric environment publish` | Publish Weaver into a Fabric Environment. |
| `fabric notebook push` | Create or update a Fabric notebook definition. |
| `fabric notebook run` | Run a deployed Fabric notebook. |
| `fabric capacity` | Resume, suspend or report a Fabric capacity. |

## Workspace options

Lifecycle commands accept the applicable subset of:

```text
--workspace NAME
--workspace-config PATH
--catalogue Warehouse/Name
--environment Environment
--environment Workspace/Environment
```

Explicit command-line values override values from workspace configuration. If no workspace was otherwise supplied, project commands look for `workspace-config.yml` in the current directory. A workspace inherited from `weaver session` takes precedence over that file.

A typical configuration is:

```yaml
workspace: Parcel Development
environment: Weaver
catalogue: Warehouse/Catalogue

targets:
  Lakehouse/Landing: Landing_Dev
  Warehouse/Operations:
    name: Operations_Dev
    execution:
      parallel_workers: 4
```

`workspace` is the only required key. `targets` may be absent. Build reads target bindings from this configuration; load, test and health read installed bindings from the catalogue.

## Item and target selection

The nouns are deliberate:

- An **item** is a logical identity such as `Warehouse/Operations`.
- A **target** is a physical Fabric item such as `Warehouse/Operations_Dev`.

Build selects logical items with a repeatable option because its positional argument is the source:

```bash
weaver build ./parcel-ops \
  --item Lakehouse/Landing \
  --item Warehouse/Operations=Warehouse/Operations_Dev
```

`ITEM=TARGET` supplies or overrides the physical binding. The two sides must have the same kind. Naming no `--item` builds every configured item.

Load and test select logical items positionally. Naming none selects every installed item:

```bash
weaver load Lakehouse/Landing Warehouse/Operations
weaver test Warehouse/Operations
weaver load
```

Health uses repeatable `--item` options. Wipe selects physical targets positionally:

```bash
weaver health --item Warehouse/Operations
weaver wipe Warehouse/Operations_Dev --dry-run
```

## Interaction and automation

`--non-interactive` means the invocation must not wait for input, offer retry prompts or open browser sign-in. It does not approve destructive work.

`--yes` authorises an action that would otherwise require confirmation. An unattended destructive command needs both:

```bash
weaver wipe Warehouse/Operations_Dev \
  --workspace "Parcel Development" \
  --non-interactive \
  --yes
```

Commands that accept `--json` emit one JSON document to stdout and do not prompt. Output fields and version guarantees are command-specific; do not infer a stable schema from one example.

## Build and install

The normal build plans and installs in one command:

```bash
weaver build
```

For a split handoff, retain the bundle and install it later:

```bash
weaver build \
  --bundle-only \
  --bundle-path ./dist/parcel-bundle

weaver install ./dist/parcel-bundle \
  --workspace-config workspace-config.yml
```

Installation executes the bundle without reopening project source or replanning it.

## Load, test and health selection

`load --name` selects installed loadable objects and skips dependency ordering. In a Lakehouse, qualify ambiguous names as `Tables/Schema.Object` or `Files/Schema.Object`; a Warehouse uses `Schema.Object`.

`load --stale` selects objects whose load health is not Green. `--as-of` changes its freshness cutoff and is valid only with `--stale`. `--reload` reconstructs each selected table and cannot be combined with `--stale`. `--dry-run` reports the plan without running it.

`test --name Schema.Object` runs one installed validation and returns diagnostic rows. `test --file PATH` compiles and runs one source SQL validation without installing it. The options are mutually exclusive. An item-wide test reports counts rather than diagnostic rows.

`health --as-of DATETIME` changes the freshness instant; it must include a time zone. `--no-inventory` skips the physical inventory check for certified objects. Health exits `0` for Green and `1` for Amber or Red.

## Destructive commands

`wipe --dry-run` displays the settled plan and changes nothing. With named targets, wipe empties exactly those physical items. With none, it discovers the installed estate from the catalogue and empties the catalogue last. `--unbind` instead preserves the catalogue and removes its claims for the named targets; it requires both a catalogue and at least one target.

`mirror` also empties destination items. Inspect its plan and require `--yes` for unattended execution. The source catalogue is read before Weaver changes the destination, and the settled plan names the destination items it will empty.
