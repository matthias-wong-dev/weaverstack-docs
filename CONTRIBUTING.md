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
| Getting started | Install and choose a route | Setup with an optional small Warehouse starter, not an admission requirement. |
| Lakehouse / Warehouse / Semantic models / Reports | Use a familiar item | One start state, one useful result and a connected next task. |
| Coordinate your estate | Work with connected items | Dependencies, environment mappings, state, development, operation, recovery and tuning. |
| Reference | Look up precise behaviour | Syntax, defaults, selection, state changes, failures and API signatures. |

Retained concept and deep-dive URLs stay searchable and are linked contextually.
Before moving material, extend `acceptance/docs-item-first-2026-10/route-map.md`.
Record prior/next example checkpoints, direct-entry fixture and any intentional
source-mode change. Retired routes preserve meaningful fragments as direct links,
never chains. Human reader acceptance is separate from compiler/browser checks.

## Write and connect the page

- Use public terms such as project, Weaver document, logical item, physical Fabric item, catalogue, Build, Load, Test and Health.
- Present Fabric first, with Lakehouse, Warehouse, semantic model and Report tasks in that order. Explain the practical benefit where it changes the work; keep exhaustive exceptions in Reference.
- Keep implementation classes, planner structures and module ownership out of user-facing explanations unless an identifier is part of the interface.
- Distinguish current machine formats from compatibility guarantees.
- Use relative links for pages in this site.
- Give code blocks a language and make commands runnable as written.
- Use neutral parcel or logistics examples; remove private project, workspace, tenant and item names.
- Keep the initial example small; later tasks add declarations without replacing working item-owned sources.

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

Generated semantic-extension and catalogue inventories have explicit owners as well. Run these with the same checkout:

```bash
uv run python tools/test_generate_semantic_reference.py
uv run python tools/test_generate_catalogue_reference.py
uv run --project "$WEAVER_CHECKOUT" python tools/generate_semantic_reference.py --write --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/generate_semantic_reference.py --check --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/generate_catalogue_reference.py --write --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/generate_catalogue_reference.py --check --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/check_reference_examples.py --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/check_docs_refresh_examples.py --weaver-checkout "$WEAVER_CHECKOUT"
uv run --project "$WEAVER_CHECKOUT" python tools/check_journey_examples.py --weaver-checkout "$WEAVER_CHECKOUT"
```

For coordinated product/documentation revisions, also check the reader flow:

```bash
uv run --project "$WEAVER_CHECKOUT" python tools/check_fabric_first_story.py --product-site "$PRODUCT_SITE" --weaver-checkout "$WEAVER_CHECKOUT"
```

`PRODUCT_SITE` is the static product source or build directory. This checks Fabric-first discovery, rounded scale copy, the native Power BI comparison and shared CLI examples. It is an editorial/parser guard, not live acceptance.

The fixture checker uses the pinned source's small offline test helpers and explicit network-blocked boundaries. It does not deploy, query DAX/SQL or prove licence eligibility. Optional `--check-pbir-schemas` uses `jsonschema` and public Microsoft schemas, not a Fabric tenant.

Inspect the manifest and every changed owning page. A clean generator check proves that generated facts match the selected checkout, not that surrounding explanations are correct.

## Generated tutorial files

The installed Weaver package owns the Parcel and Sales starting examples. Tutorials use named `weaver initialise --example Parcel` selections and extend the same project; they do not distribute separate project snapshots. Displayed generated files use `initialise` markers. After changing an example, synchronise and check these blocks against the coordinated source checkout:

```bash
python tools/sync_initialise_examples.py --weaver-checkout "$WEAVER_CHECKOUT"
python tools/sync_initialise_examples.py --check --weaver-checkout "$WEAVER_CHECKOUT"
```

Keep technical preservation and compilation assertions in automated tests. Introductory tasks use ordinary queries, field lists and service lineage for observation, not acceptance scripts.

The continuing-project gates use the product interpreter and explicit offline inventory/column inputs:

```bash
PYTHONPATH="$WEAVER_CHECKOUT/src" "$PRODUCT_PYTHON" tools/check_lakehouse_examples.py --docs . --product "$WEAVER_CHECKOUT"
PYTHONPATH="$WEAVER_CHECKOUT/src" "$PRODUCT_PYTHON" tools/check_estate_examples.py --weaver-checkout "$WEAVER_CHECKOUT"
WEAVER_CHECKOUT="$WEAVER_CHECKOUT" PYTHONPATH="$WEAVER_CHECKOUT/src" "$PRODUCT_PYTHON" tools/check_semantic_examples.py
```

`PRODUCT_PYTHON` must have the selected runtime's dependencies. Keep that environment separate from the locked MkDocs environment. The fixture gate accepts an explicitly reviewed `--runtime-revision` when integration moves beyond its original provenance; a passing stale fixture is not acceptance of a new generator.

For an installed-wheel check, build a wheel, install it into an isolated target directory with its dependencies available to the test interpreter, then run from an empty scratch directory:

```bash
"$PRODUCT_PYTHON" -I /absolute/path/to/weaverstack-docs/tools/check_installed_examples.py \
  /absolute/path/to/isolated-install /absolute/path/to/results.json
```

This checks all named selections, subset preservation and extension orders through the public API with network connections refused. Fabric inventory/creation is an explicit test boundary; it does not prove deployment, SQL execution, refresh or Report rendering.

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
