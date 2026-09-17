# Weaver documentation

Source for the public technical documentation at `docs.weaverstack.dev`.

The site describes Weaver's supported public behaviour and contracts. Product positioning belongs at `weaverstack.dev`; implementation notes belong in the main `weaverstack` repository.

## Local preview

Python 3.11 or later and [uv](https://docs.astral.sh/uv/) are required.

```bash
uv sync --locked --python 3.11
uv run mkdocs serve
```

Build the site strictly before submitting a change:

```bash
uv run mkdocs build --strict
```

## Licence

This repository is licensed under the [Mozilla Public License 2.0](LICENSE), matching Weaver.
