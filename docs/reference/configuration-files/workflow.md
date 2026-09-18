# Workflow configuration

A workflow file maps names to ordered lists of ordinary Weaver CLI command lines. Workflow adds one shared Session, one workspace check and one confirmation around those commands; it does not define another operation language.

## File selection

The default path is exactly `./workflow.yml`, relative to the process's current working directory. Weaver does not search parent directories or derive this path from `workspace-config.yml`.

```bash
weaver workflow verify
weaver workflow verify --file deploy/parcel-workflows.yml
```

`--file PATH` selects another file. `~` is expanded. The selected path must be a file containing valid YAML.

## Document shape

The only workflow-defining top-level key is `workflows`:

```yaml
workflows:
  verify:
    - check .
    - build . --item Warehouse/Operations
    - load Warehouse/Operations
    - test Warehouse/Operations
    - health --item Warehouse/Operations

  refresh-development:
    - mirror --item Warehouse/Operations --yes
    - build . --item Warehouse/Operations
    - load Warehouse/Operations --stale
    - test Warehouse/Operations
```

| Location | Required shape | Restrictions |
| --- | --- | --- |
| document | YAML mapping | A scalar or sequence is rejected. |
| `workflows` | mapping | Required. Other top-level entries do not define workflows and are ignored by the loader. |
| workflow name | mapping key selected by the positional `name` argument | Use a string. The requested name must be present exactly as written. |
| workflow value | non-empty YAML list | Empty lists and non-list values are rejected. |
| list entry | string containing one command line | Empty or whitespace-only strings and non-string values are rejected. Leading and trailing whitespace is removed. |

There are no workflow-level defaults, variables, parameters or per-entry mappings. Each list element is the complete command line.

## Entry grammar

A leading literal `weaver` is optional:

```yaml
workflows:
  equivalent:
    - weaver check .
    - check .
```

Arguments use command-line quoting. Quoted whitespace remains part of one argument:

```yaml
workflows:
  development:
    - build . --workspace-config "workspace development.yml"
    - load --workspace-config "workspace development.yml"
```

Every entry is tokenised and then parsed by the live Weaver CLI parser before the first entry runs. The command, positional arguments, options, repeatability and mutually exclusive options are therefore the same as at the command line.

A workflow entry is not a shell command. Outside quotes, Weaver rejects `|`, `>`, `<`, `&`, `;`, `$` and backticks. It does not perform redirection, pipelines, command substitution, environment-variable expansion or command chaining. Backslashes are not escape characters in the command-line tokenizer, so quote arguments containing whitespace rather than using backslash escaping. A newline inside one YAML string is also rejected.

Only Weaver commands are accepted. `session` and `workflow` are specifically excluded: a workflow cannot open an interactive Session or nest another workflow.

## Workspace restrictions

The outer workflow invocation and entries must resolve to at most one equal Workspace configuration. The outer options are:

```text
--workspace
--workspace-config
--catalogue
--environment
```

If the outer invocation resolves a Workspace, entries that omit workspace arguments inherit it through the workflow's Session. An entry may explicitly resolve the same complete Workspace configuration. If outer or entry arguments resolve different workspace configurations, validation fails before the sequence is displayed or executed.

When neither the outer invocation nor an entry supplies workspace arguments, normal workspace discovery may supply `workspace-config.yml` from the current working directory. A sequence containing only commands that require no workspace can remain without one.

The shared Workspace restriction includes more than the workspace display name: catalogue, Environment, Mirror source, execution settings and targets are part of the resolved configuration. Use one selected workspace configuration for the sequence rather than mixing per-entry estate definitions.

## Validation boundary

Before asking for confirmation, Weaver:

1. loads the requested named list;
2. validates every entry with the ordinary CLI parser;
3. rejects excluded commands and shell syntax; and
4. resolves the one shared Workspace configuration.

This validates local syntax and configuration. It does not prove that remote Fabric items exist or that every operation will succeed.

Execution order, confirmation, stop-on-failure and non-rollback behaviour belong to [Workflow operation behaviour](../operation-behaviour/workflow.md). Command selection remains owned by [Shared selection and identity](../operation-behaviour/shared-selection-and-identity.md) and the individual operation pages.
