# October documentation refresh baseline

## Approved scope and version boundary

Implement the supplied product/developer documentation plan against Weaver `74b4d15ee65ed2740593af1f4d459771b801b132` and developer docs `f35c943ed0ca423b92ab53aa571c43ae2817b74e`. Both are fetched remote main heads at the initial audit on 13 October 2026 (Australia/Canberra).

Matthias approved this implementation target and **holding publication for a matching package release**. No release number/date is assigned. PyPI's latest package is `0.9.0`, uploaded on 19 September 2026. The selected main has substantial additions since `v0.9.0`; it is not the installation target for these new instructions. Package/release, live acceptance, merge and publication remain separate gates.

## Workspaces

- Product/source: `/opt/data/scratch/Fors/weaver-docs-refresh/product`, branch `docs/product-and-scale-refresh`, starting at the selected Weaver revision.
- Reference: `/opt/data/scratch/Fors/weaver-docs-refresh/reference`, branch `docs/reference-compatibility-refresh`, starting at the selected documentation revision.
- Journeys/examples: separate worktree; A2 examples integrate into the stacked reader-journeys PR, not the reference PR.
- Existing shared checkouts retain their original branches and uncommitted files. No edits are authorised there.

## Overlap audit

GitHub open PR lists returned no open documentation PRs. Existing local documentation branches are historical work predating the merged acceptance corrections; the new work starts from current main rather than reviving their stale trees.

Open product PRs:

- [#220: installation physical identity](https://github.com/matthias-wong-dev/weaverstack/pull/220), audited head `8a806f80b1bdd833f7cb3dfcf97c04a7e02cf971`: catalogue Installation schema and bindings change. **Excluded until merged and an explicit target refresh is accepted**. Recheck before publication; do not mix those fields into this baseline.
- [#208: Catalogue Dashboard](https://github.com/matthias-wong-dev/weaverstack/pull/208), audited head `ed877659546d1e6e78954760535b82d163441998`: dashboard, configuration, catalogue GraphNode/GraphEdge and runtime additions. **Excluded**. README overlap must be rechecked before the product PR merges.

## Ownership

Fors owns `mkdocs.yml`, landing pages, COVERAGE, cross-site integration, final ledger and review. Approved first two-agent batch:

1. Reference author: `docs/reference/**`, `tools/*reference*`, `generated/*reference*`, reference evidence.
2. Fixture author: six directories named in plan section 10 and offline fixture-check tooling/evidence. No public page/nav ownership.

Later delegation batches need separate approval. Children do not publish, push, mutate remote resources, edit Weaver runtime, or expand scope.

## Evidence labels

- **Source-backed**: current implementation and named tests located; not a report that tests were executed.
- **Locally checked**: actual commands executed against this revision; record outputs and failure/skips.
- **Remotely exercised**: exact authorised service operation and supported readback recorded. No fresh remote tests are authorised by this brief.
- **Not yet verified**: missing evidence, including live licensing/service/render results.

Historical benchmark evidence remains labelled historical. Site/source checks cannot establish tenant licensing or report rendering. Publication must proceed matching package → developer docs → product links, with explicit approval and live URL verification.
