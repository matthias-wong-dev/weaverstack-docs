# Intended-release website and onboarding copy

## Scope chosen by Matthias

Matthias stopped the current-PyPI alignment audit and directed: “pypi is not yet published. please focus on making the website changes, as if the pypi is out”. This is prospective release copy for the advertised four-item capability set, **not** a request to roll the docs/product back to 0.9.0 and **not** permission to publish a package or either website. The release-ready words assume a matching PyPI package at publication; no new version number/date is invented.

Both existing PRs remain drafts. The original source evidence pin remains `74b4d15ee65ed2740593af1f4d459771b801b132` for local implementation-shape verification only. It is no longer a public installation target. The aborted clean-wheel audit is not represented as an acceptance run of the intended release.

## Changes

- Product Get started now shows Python 3.11+, `python -m pip install --upgrade weaverstack` and `weaver --version`, then four independent Lakehouse/Warehouse/model/Report routes. No compulsory Warehouse detour. The tagline, single Features tab, four feature pages and existing concise engineering/scale positioning remain.
- Public Installation leads with the same PyPI command and version check. Private warnings, development fingerprints, Git/editable package installation and development-wheel prerequisites removed.
- First Lakehouse, runtime, incremental and automation instructions use normal Environment publication while retaining the genuine matching-runtime requirement. Workspace configuration does not publish an Environment; Warehouse-only work does not need Spark.
- Old runtime/installation anchors retained at their new owning sections. Source fingerprints and obsolete “older PyPI” qualifications removed from public Reference; generated API/CLI facts unchanged. Optional `--dev` remains an exact reference option, not a tutorial requirement.
- Development-runtime procedures preserved privately in development-runtime.md, outside the rendered site. Example README installation headers use the normal route. Public example links target the permanent docs main paths for publication, not the draft branch; those destinations depend on merging the coordinated documentation when authorised.
- Item-first information architecture and full traditional left navigation unchanged. No content capability deferred, no runtime/interface/tenant/resource changes and no broad information-architecture redesign.

## Actual verification

- Tight release-ready copy guard first failed on missing normal PyPI onboarding, then passed after correction. Maintained story guard now requires PyPI install/version verification and rejects snapshot prerequisites in onboarding.
- Locked strict build; rendered route/fragment gate: 114 original pages, 872 IDs, 35 canonical owners, no errors.
- Paired crawl: 161 HTML pages, 23,185 local link/asset checks, 201 cross-site links, zero broken targets/fragments. Eleven product routes, metadata/nav/footer and seven unchanged benchmark rows pass.
- Source-pinned Lakehouse gate: seven Checks, 30 forms, twelve exact blocks. Six fixture Checks / 53 README commands; combined journey checker (15 pages, 81 forms, ten configs, three Python calls, twelve exact blocks, four assembled projects); all four deterministic generators pass. These are source/shape checks, **not PyPI-only acceptance or live service outcomes**.
- Ruff lint/format for changed story guard and whitespace pass.
- Focused rendered QA: sixteen states across product Get started / docs Installation / first Lakehouse / runtime, 390 and 1440, light/dark. Normal package commands visible, four item links, no preview/Git warnings, no page errors or horizontal overflow, top tabs still absent. Product desktop and installation mobile screenshots inspected.
- Preview loopback servers were found stopped after interruption; only those two static servers were restarted. Both target routes read HTTP 200; existing Tailscale handlers preserved. No independent peer-browser claim.

## Still held

Release/package publication, installed matching-wheel acceptance, live Fabric/model/Report service validation, human editorial approval and public publication remain separate gates. No upload, merge, release, tenant/Environment operation or capacity change was performed. Keep these gates in maintainer evidence and PR bodies, not as ordinary-user installation warnings.
