# `weaver initialise`

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver initialise [-h] [--workspace WORKSPACE] [--project-folder PATH] [--catalogue CATALOGUE] [--environment ENVIRONMENT] [--lakehouse LAKEHOUSE] [--warehouse WAREHOUSE] [--example] [--no-example] [--interactive] [--non-interactive] [--dry-run] [--json] [--publish-environment]
weaver initialize [-h] [--workspace WORKSPACE] [--project-folder PATH] [--catalogue CATALOGUE] [--environment ENVIRONMENT] [--lakehouse LAKEHOUSE] [--warehouse WAREHOUSE] [--example] [--no-example] [--interactive] [--non-interactive] [--dry-run] [--json] [--publish-environment]
```

## Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric workspace name. It must exist.

`--project-folder PATH`
: Project folder to create or reuse. Required for unattended setup.

`--catalogue CATALOGUE`
: Catalogue Warehouse. Defaults to Catalogue.

`--environment ENVIRONMENT`
: Fabric Environment for the project. It may already exist. Defaults to Weaver.

`--lakehouse LAKEHOUSE`
: Lakehouse for Delta tables and files.

`--warehouse WAREHOUSE`
: Warehouse for SQL tables and views.

`--example`
: Add Sales example source files.

`--no-example`
: Do not add example source files.

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

Create or reuse a project folder, catalogue Warehouse, Fabric Environment, and optional Lakehouse and Warehouse. `initialize` is an accepted alias.

Without explicit values, terminal use starts a wizard. Unattended use requires `--workspace` and `--project-folder`; omitted catalogue and Environment names default to `Catalogue` and `Weaver`. Lakehouse and Warehouse are optional.

## Execution

Initialisation creates missing Fabric items and writes the project files. Existing compatible items and generated files are reused. `--example` adds the Sales example; `--no-example` leaves it out. `--publish-environment` publishes the Environment after setup.

`--dry-run` resolves the requested setup and reports planned items and files without creating or writing them.

## Interaction

The wizard reviews all choices before making changes and permits cancellation. `--interactive` allows questions when input is not a terminal. `--non-interactive` forbids questions and requires the unattended inputs. The two options cannot be combined.

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
  --no-example \
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
