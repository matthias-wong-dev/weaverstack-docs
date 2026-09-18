# Contributing to the Weaver documentation

This repository documents Weaver's public technical surface. Product positioning belongs on `weaverstack.dev`; implementation design belongs in the Weaver source repository.

Read `AGENTS.md` for section ownership and evidence rules, `PROSE.md` for the house style, and `COVERAGE.md` before moving material between sections.

## Establish the evidence

Use a specific Weaver source revision. For each behavioural claim:

1. locate the implementation;
2. find the tests or acceptance journey that exercises it;
3. determine whether it is specified behaviour, host-specific behaviour or current output;
4. link to the authoritative documentation owner instead of duplicating its contract.

Source and tests outrank design prose. Maintained projects are realism checks, not public contracts. If the desired workflow differs from current behaviour, document current behaviour and leave the product decision outside the public page.

## Choose one page job

| Section | Reader need | Page responsibility |
| --- | --- | --- |
| Getting started | Complete a first successful lifecycle | One shallow, ordered path with only the context needed for the next step. |
| Core concepts | Reason about Weaver | The public mental model and its consequences. |
| Basics | Complete normal work | Prerequisites, actions, observable results and recovery routes using defaults first. |
| Advanced | Understand or apply a deeper mechanism | A bounded explanation or operating pattern with explicit prerequisites and boundaries. |
| Reference | Look up an interface or specified behaviour | Exact syntax, fields, defaults, selection, state changes, outcomes and failure boundaries. |

If a page starts doing several jobs, keep the task in Basics and link to the owning concept, advanced explanation or reference entry.

## Write and connect the page

- Use public terms such as project, Weaver document, logical item, physical Fabric item, catalogue, Build, Load and Test.
- Keep implementation classes, planner structures and module ownership out of user-facing explanations unless an identifier is part of the interface.
- Distinguish current machine formats from compatibility guarantees.
- Use relative links for pages in this site.
- Give code blocks a language and make commands runnable as written.
- Use neutral parcel or logistics examples; remove private project, workspace, tenant and item names.
- Keep each example focused instead of extending one site-wide sample estate.

Add contextual links from the reader's likely entry page and onward to the next task or authoritative detail. Search `docs/` for retired paths and vocabulary after a move.

## Generated reference

Generated blocks own interface facts; prose around them owns purpose, effects, failure conditions and examples. Do not edit text between generated markers by hand.

Set `WEAVER_CHECKOUT` to the Weaver source checkout used as evidence. When the CLI parser changes, update the CLI generator ownership map and regenerate before checking. When `weaver.__all__` changes, update the Python ownership map, regenerate and run its tests.

```bash
uv run --project "$WEAVER_CHECKOUT" python tools/generate_cli_reference.py \
  --write --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/generate_cli_reference.py \
  --check --weaver-checkout "$WEAVER_CHECKOUT"

uv run python tools/test_generate_python_reference.py
uv run --project "$WEAVER_CHECKOUT" python tools/generate_python_reference.py \
  --write --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/generate_python_reference.py \
  --check --weaver-checkout "$WEAVER_CHECKOUT"
```

Inspect the manifest and every changed owning page. A clean generator check proves that generated facts match the selected checkout, not that surrounding explanations are correct.

## Validate the change

Python 3.11 or later and [uv](https://docs.astral.sh/uv/) are required.

```bash
uv sync --locked --python 3.11
uv run mkdocs build --strict
git diff --check
git diff --stat
git diff
```

Also run focused Weaver tests for changed behavioural claims, parse examples with Weaver where semantics matter, and compare published code blocks with checked-in fixtures. After the strict build, inspect changed pages at desktop and narrow widths, in light and dark mode where code or tables changed.

Before submitting, confirm that generated blocks came from their generator, planning notes remain outside `docs/`, links still form a complete reader journey and the change records the Weaver source revision used for behavioural or generated-reference work.
