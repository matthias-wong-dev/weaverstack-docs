# Update generated reference

The CLI and public Python reference combine generated interface facts with authored explanation. Generated blocks own syntax and membership; prose around them owns purpose, effects, failure conditions and examples.

Do not edit text between generated markers by hand.

## CLI commands

`tools/generate_cli_reference.py` reads the live parser from a Weaver source checkout. Its ownership map assigns every executable command leaf to exactly one page under `docs/reference/cli/`.

When the parser changes:

1. update `OWNERSHIP` if a command was added, removed or moved;
2. make sure its owning page contains exactly one generated CLI marker pair;
3. regenerate the manifest and page blocks;
4. revise the authored prose for changed effects or failure behaviour;
5. run strict check mode.

From the documentation repository, with the Weaver repository checked out next to it:

```bash
uv run --project ../weaverstack python tools/generate_cli_reference.py \
  --write \
  --weaver-checkout ../weaverstack
uv run --project ../weaverstack python tools/generate_cli_reference.py \
  --check \
  --weaver-checkout ../weaverstack
```

The check rejects unassigned live commands, duplicate ownership, retired assignments, manifest drift, missing pages and changed generated blocks.

## Public Python API

`tools/generate_python_reference.py` reads the names exported by `weaver.__all__`. Its ownership map assigns every public top-level export to exactly one page under `docs/reference/python/`.

When the public namespace changes:

1. update `OWNERSHIP` for the added, removed or moved export;
2. make sure its owning page contains exactly one generated Python marker pair;
3. regenerate the manifest and page blocks;
4. document the meaning and behaviour of the public object outside the generated block;
5. run the generator tests and strict check mode.

```bash
uv run python tools/test_generate_python_reference.py
uv run --project ../weaverstack python tools/generate_python_reference.py \
  --write \
  --weaver-checkout ../weaverstack
uv run --project ../weaverstack python tools/generate_python_reference.py \
  --check \
  --weaver-checkout ../weaverstack
```

Importable names from nested implementation modules are not part of this generated public surface unless `weaver.__all__` exports them.

## Review the result

Inspect the generated manifest and every changed owning page. A clean generator check proves that the checked-in facts match the selected source checkout; it does not prove the surrounding explanation or examples are correct. Verify those claims against source and tests, then complete the [documentation validation](validation.md).