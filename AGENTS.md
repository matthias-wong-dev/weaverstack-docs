# Weaver documentation agent guide

## Purpose

This repository is the public technical documentation for Weaver. It explains supported behaviour, public contracts, configuration, commands and APIs to people building and operating Weaver projects.

Keep three surfaces distinct:

- `weaverstack.dev` is the concise product and evaluation site.
- This repository is public technical documentation.
- Source-level implementation narration belongs in the main `weaverstack` repository.

## Sources of truth

Use these in order:

1. the explicitly frozen Weaver evidence checkout (`WEAVER_CHECKOUT`); after the requested main integration, behaviour/interfaces are checked against `0f51b02ce5c33bd46e944c871083663948c6ca6e`; original fixture provenance remains `74b4d15ee65ed2740593af1f4d459771b801b132`;
2. acceptance journeys and tests that establish behaviour;
3. existing design documentation in the Weaver repository;
4. realistic usage in `/opt/data/repos/ilovegov-etl`.

If code and prose disagree, investigate the current behaviour. Do not choose the nicer answer and do not invent one.

Read `/opt/data/repos/weaverstack/PROSE.md` before writing. Use the public terms established by the source repository. Clearly distinguish guaranteed behaviour, host-specific behaviour, examples and implementation detail.

## Writing

Write as one senior engineer to another. Use plain, direct language. Prefer small working examples to ceremonial explanation. Reference pages should be terse and searchable; concept pages should explain the mental model needed to reason correctly.

Avoid claims such as “powerful”, “seamless”, “robust”, “safe”, “predictable” and “enterprise-grade”. State the mechanism or property instead. Do not tell readers what behaviour or state they “can rely on”; describe the defined behaviour or recorded state directly. Do not write “current versions of Weaver” unless a version distinction matters.

Use Weaver's user model rather than deriving a taxonomy from internal nouns. A project contains Weaver documents such as Tables, Folders, Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata. Do not introduce `resource` or `artefact` as a user-facing category.

Examples use a neutral parcel and logistics domain. Keep one continuous story and stable logical names per item, not one enormous site-wide estate. Each page declares the prior working checkpoint or links to a complete direct-entry snapshot. A fixture switch must explain the changed source/mode; do not restart setup midway through a first task.

## Public site structure

The reader-facing navigation is **Getting started → Lakehouse → Warehouse → Semantic models → Reports → Coordinate your estate → Reference**. Home exposes the four items, estate coordination and a quiet Start here link. Item groups teach first success, validation and later useful capabilities. Estate coordination owns shared dependencies, mappings, state, development, recovery and tuning. Reference owns exact interfaces. Concepts and deeper mechanisms remain available through contextual links at stable URLs; Core/Basics/Advanced are no longer reader-facing destinations.

Use the full collapsible navigation tree on the left, with the current section expanded and the page headings on the right. Do not restore horizontal section tabs or hide other top-level groups on desktop. Mobile retains the theme’s drawer and back controls.

Do not add public **Guides**, **Contracts**, **Contributing** or **Architecture** sections. Exact behavioural material belongs under Reference; maintainer instructions belong in root `CONTRIBUTING.md`, `AGENTS.md`, `PROSE.md` and `COVERAGE.md`.

`COVERAGE.md` is the internal documentation ledger. Keep it outside `docs/` and out of public navigation. A target path records ownership, not completion.

Coverage comes before volume: give each public concept, command, API and behaviour one authoritative home before filling every page. Keep concept, task, mechanism and reference material separate, and link to the owning page rather than repeating a partial specification.
