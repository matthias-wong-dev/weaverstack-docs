# `weaver initialise`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver initialise [-h] [--workspace WORKSPACE] [--project-folder PATH] [--catalogue CATALOGUE] [--environment ENVIRONMENT] [--lakehouse LAKEHOUSE] [--warehouse WAREHOUSE] [--semantic-model NAME] [--example NAME] [--interactive] [--non-interactive] [--dry-run] [--json] [--publish-environment]
weaver initialize [-h] [--workspace WORKSPACE] [--project-folder PATH] [--catalogue CATALOGUE] [--environment ENVIRONMENT] [--lakehouse LAKEHOUSE] [--warehouse WAREHOUSE] [--semantic-model NAME] [--example NAME] [--interactive] [--non-interactive] [--dry-run] [--json] [--publish-environment]
```

## Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric workspace name. It must exist.

`--project-folder PATH`
: Project folder to create or reuse. Required for unattended setup.

`--catalogue CATALOGUE`
: Catalogue Warehouse. Defaults to Catalogue for data projects; omitted for native-only projects.

`--environment ENVIRONMENT`
: Fabric Environment for Python work. Defaults to Weaver for data projects; omitted for native-only projects.

`--lakehouse LAKEHOUSE`
: Lakehouse for Delta tables and files.

`--warehouse WAREHOUSE`
: Warehouse for SQL tables and views.

`--semantic-model NAME`
: Add PowerBI/NAME/NAME.tmdl, or name the example's Power BI project. Build creates the SemanticModel.

`--example NAME`
: Add the Parcel or Sales example for the selected items.

`--interactive`
: Ask setup questions even when input is not a terminal.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--dry-run`
: Preview the setup without making changes.

`--json`
: Emit the result as JSON.

`--publish-environment`
: Publish the project Environment after setup.

<!-- END GENERATED CLI -->

## Responsibility and selection

Create or extend a project folder for selected Lakehouse, Warehouse and native Power BI items. Data projects also create or reuse a catalogue Warehouse and Fabric Environment. `initialize` is an accepted alias.

Without explicit values, terminal use starts a wizard. Unattended use requires `--workspace` and `--project-folder`. Data projects default catalogue and Environment names to `Catalogue` and `Weaver`. A native-only `--semantic-model` selection needs neither supporting item; explicit catalogue or Environment requests remain available. Adding a Lakehouse or Warehouse later supplies missing supporting configuration without changing existing bindings.

## Execution

Initialisation creates missing Fabric items and writes the project files. Existing items, edited source files and physical bindings are preserved. Rerunning with another item extends the configuration; omitting an existing item does not remove it. New file or identity collisions are refused before project writes or item creation. An unchanged selection is idempotent. `--example Parcel` or `--example Sales` adds the named example for the selected items; omitting the option adds no example content. `--publish-environment` publishes the Environment after setup.

`--dry-run` resolves the requested setup and reports planned items and files without creating or writing them.

## Interaction

The wizard offers None, Parcel or Sales and reviews all choices before making changes and permits cancellation. `--interactive` allows questions when input is not a terminal. `--non-interactive` forbids questions and requires the unattended inputs. The two options cannot be combined.

`--json` also runs without questions. It does not imply `--publish-environment`.

## Output and exit behaviour

Human output lists each item as existing or created, states Environment publication status, and gives the next lifecycle commands. A dry run lists planned changes and says that nothing changed.

`--json` emits the current initialisation report as one JSON document. Its fields are not presented here as a compatibility contract.

The command exits `0` when the report succeeds, including user cancellation before setup, and `1` for a failed report or command error. Argument errors exit through `argparse`.

## Examples

Interactive setup:

```bash
weaver initialise
```

Unattended setup without example files or immediate Environment publication:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --catalogue Catalogue \
  --environment Weaver \
  --lakehouse Landing \
  --warehouse Operations \
  --non-interactive
```

Preview the same setup:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel \
  --lakehouse Landing \
  --dry-run \
  --non-interactive
```


Extend the same project with a Warehouse, retaining its Lakehouse and edited sources:

```bash
weaver initialise --workspace "Parcel Development" --project-folder ./parcel --warehouse Operations --example Parcel
```

`--semantic-model Parcel --example Parcel` adds the native inline model and linked Report. When source items exist, separately named source-backed models are additional definitions, not replacements for native partitions. Source-backed refresh needs an existing supported service connection and SQL permissions. Initialise itself neither loads nor wipes data.
