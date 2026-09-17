# Contributing to the documentation

Public Weaver documentation is maintained separately from product positioning and implementation design.

- `weaverstack.dev` explains the product concisely.
- This site documents supported public behaviour, commands, configuration, APIs and contracts.
- The Weaver source repository owns implementation design and module-level reasoning.

## Evidence order

Ground behavioural changes in:

1. current Weaver source;
2. acceptance journeys and tests;
3. current design documents;
4. realistic project usage.

When those sources disagree, establish current behaviour before editing the docs. Do not select the simpler claim or complete a pattern by inference.

## Writing and examples

Write directly for an engineer using Weaver. Separate guarantees from examples, host-specific behaviour and implementation detail. Examples should use a small parcel or logistics domain and only syntax established by source or tests.

Use relative Markdown links for pages on this site. Keep documentation planning outside `docs/`; the public site should contain the best available guidance rather than its maintenance backlog.

## Change checks

For documentation changes:

1. confirm every command and option against current parser declarations or command help;
2. validate code examples with the project parser where possible;
3. build the MkDocs site strictly;
4. inspect the changed-page set so public docs do not absorb source-level design narration.

```bash
uv run mkdocs build --strict
```
