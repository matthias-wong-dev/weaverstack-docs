# Validate a documentation change

Run checks from the documentation repository root. Python 3.11 or later and [uv](https://docs.astral.sh/uv/) are required.

## Set up the documentation environment

```bash
uv sync --locked --python 3.11
```

Preview while editing:

```bash
uv run mkdocs serve
```

The preview is for reading and navigation checks. It does not replace the strict build.

## Check the changed surface

Use the product boundary that owns each fact:

- compare commands and options with the live parser or `weaver <command> --help`;
- parse YAML with Weaver's parser rather than a generic YAML loader when Weaver semantics matter;
- run the focused Weaver tests for behavioural claims;
- run the generated-reference checks when CLI commands or `weaver.__all__` changed;
- compare code blocks with any checked-in example files they reproduce.

See [Update generated reference](generated-reference.md) for the CLI and Python generator commands.

## Build strictly

```bash
uv run mkdocs build --strict
```

The strict build catches unresolved internal links, invalid navigation entries and rendering warnings. After it succeeds, inspect the rendered changed pages at desktop and narrow widths. Check headings, code blocks, tables, next-step links and long reference sections.

## Review the diff

Before submitting:

```bash
git diff --check
git diff --stat
git diff
```

Confirm that:

- every changed claim is supported by the selected Weaver revision;
- examples contain no private project, workspace, tenant or item names;
- current output has not been presented as a compatibility guarantee;
- generated blocks were changed by their generator;
- section indexes and contextual links still form a complete reader journey;
- planning notes and coverage gaps remain outside the rendered site.

Record the Weaver source revision used for behavioural or generated-reference changes in the pull request. A successful site build verifies the documentation structure, not the product behaviour.