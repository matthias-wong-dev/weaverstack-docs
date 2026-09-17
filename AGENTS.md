# Weaver documentation agent guide

## Purpose

This repository is the public technical documentation for Weaver. It explains supported behaviour, public contracts, configuration, commands and APIs to people building and operating Weaver projects.

Keep three surfaces distinct:

- `weaverstack.dev` is the concise product and evaluation site.
- This repository is public technical documentation.
- Source-level implementation narration belongs in the main `weaverstack` repository.

## Sources of truth

Use these in order:

1. current source in `/opt/data/repos/weaverstack`;
2. acceptance journeys and tests that establish behaviour;
3. existing design documentation in the Weaver repository;
4. realistic usage in `/opt/data/repos/ilovegov-etl`.

If code and prose disagree, investigate the current behaviour. Do not choose the nicer answer and do not invent one.

Read `/opt/data/repos/weaverstack/PROSE.md` before writing. Use the public terms established by the source repository. Clearly distinguish guaranteed behaviour, host-specific behaviour, examples and implementation detail.

## Writing

Write as one senior engineer to another. Use plain, direct language. Prefer small working examples to ceremonial explanation. Reference pages should be terse and searchable; concept pages should explain the mental model needed to reason correctly.

Avoid claims such as “powerful”, “seamless”, “robust” and “enterprise-grade”. State concrete behaviour instead. Do not document a feature merely because it would complete a pattern.

Examples use a neutral parcel and logistics domain. Keep them small and independent rather than building one giant tutorial estate.

## Initial site structure

- Get started
- Guides
- Architecture and concepts
- Reference
- Contracts
- Advanced
- Contributing

Coverage comes before volume: give each public concept, command, API and contract an authoritative home before filling every page.
