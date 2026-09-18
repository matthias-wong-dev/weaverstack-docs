# Contributing

The documentation repository describes Weaver's public behaviour. Product positioning belongs on `weaverstack.dev`; implementation design belongs in the Weaver source repository.

Choose the contribution path that matches the change:

- [Write or revise a page](writing.md) — choose the right page type, establish evidence and connect the page to its reader journey.
- [Update generated reference](generated-reference.md) — reconcile CLI commands or public Python exports with their authoritative reference pages.
- [Validate a change](validation.md) — set up the documentation environment and run the checks for the changed surface.

## Before editing

Use evidence in this order:

1. current Weaver source;
2. acceptance journeys and tests;
3. current design documents;
4. realistic project usage.

When sources disagree, establish the implemented and tested behaviour before changing the docs. Do not complete a pattern by inference or turn observed output into a compatibility promise.

Keep examples small and independent. Use the parcel and logistics domain already used across the site, and replace names from private or production projects before publishing them.

Planning and coverage tracking stay outside `docs/`. Public pages describe the best supported guidance available; they do not expose the maintenance backlog.