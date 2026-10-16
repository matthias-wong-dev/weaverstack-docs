# Notebook equivalence delivery

This is a maintainer plan, not a public documentation page.

## Accepted requirements — 17 October 2026

Notebook equivalence is a completion criterion for the documentation refresh, not an optional capability or a small calibration-only subset.

1. Every terminal CLI block has a matching **Notebook** tab containing the corresponding cell. Switching modes switches the producing code and its corresponding output together.
2. Preserve the operation, selections, parameter values, defaults, ordering, safety and failure behaviour. Notebook keyword arguments closely follow the CLI parameters, with the workspace supplied explicitly for workspace-scoped calls. Ordinary Python spelling and collections are fine; silently changing the operation is not.
3. If a supported CLI operation has no public notebook call, or its parameters cannot express the same request, fix the product API. Do not waive the block as CLI-only, teach private implementation imports, or substitute a shell subprocess for native operation equivalence.
4. Include setup and management blocks in the inventory. Where the notebook host performs a setup action differently, supply its working host-appropriate cell and account for its semantics explicitly; do not omit it from coverage.
5. Assess the output of every notebook call. Reuse existing sensible returned reports, summaries, tables and display support. Quiet assignment is normal Python behaviour, not itself a defect. Do not manufacture output or build a new renderer when useful output already exists.
6. Record absent, inadequate, misleading or excessively verbose output in the output-fix ledger with the affected calls and evidence. Output deficiencies do not reduce the required CLI/Notebook coverage. Track verification gaps separately from product defects.
7. A calibration pair establishes presentation only; it does not reduce the final all-block scope. Completion requires inventory reconciliation, parameter parity, useful result handling, and tests of tab switching, copying, themes and narrow screens.

## PR dependency

Runtime/API fixes belong only on `feat/notebook-cli-equivalence` in `weaverstack`: [runtime/API PR #226](https://github.com/matthias-wong-dev/weaverstack/pull/226), reviewed separately above the existing `docs/product-and-scale-refresh` branch. Notebook-tab website work belongs on `docs/notebook-cli-equivalence` in `weaverstack-docs`, above `docs/progressive-journeys-refresh`. The website PR depends on runtime/API PR #226 and must not be merged or published ahead of its required runtime. This is a cross-repository dependency, not a literal Git base relationship between repositories. Keep the existing parent PRs unchanged.

## Implementation boundaries

Keep the accepted site structure, branding, CLI transcript presentation and user edits. Use the dedicated review branches above. Keep the plan, evidence and output-fix ledger outside the rendered documentation. No merge or publication is authorised. The existing disposable trial workspace remains the only live probe destination; no new connection, tenant setting or capacity is authorised. Do not launch subagents without Matthias's separate approval.

## Evidence already available

The scratch Fabric notebook exercised Initialise plus Build, Load, Test and Health against dedicated Warehouse/Lakehouse targets. The final capture contains 37 cases. All eight ordinary operation calls completed successfully. Assigned reports produced no cell streams; bare report display supplied long `text/plain` representations. Explicit status summaries were readable.

A deliberately unequal Test returned a failed validation report without an exception while the notebook job completed. Result inspection must not be replaced by job-completion status. Health exposes `status` rather than the other reports' `succeeded` property. These differences must be handled accurately, without inventing uniform report fields.

Probe evidence remains under `/opt/data/scratch/Fors/weaver-notebook-equivalence-2026-10-17/`. Its runtime and source boundaries are recorded there; observed results are not automatically evidence for later product changes.

## Current work

- Inventory every terminal block and the CLI parameters it uses.
- Implement missing public calls and repair parameter parity.
- Generate/test corresponding native notebook cells and paired tab presentation.
- Reuse useful existing output and record output deficiencies separately.
- Reconcile coverage and verify the complete private preview before delivery.

The initial Bash inventory is not a coverage-completion claim. Blocks, calls, parameter checks, observed outputs and remaining fixes need separate statuses.

## Output and API findings

| ID | Surface | Finding | Required treatment | State |
|---|---|---|---|---|
| API-001 | Check | The probe found `weaver.check` absent; CLI Check and the internal checker work. | Public export and native regression added in runtime/API PR #226. | Initial fix locally verified; matching live runtime pending |
| API-002 | Management/workflow/install | The public entry-point and parameter audit is incomplete. | Audit each documented request and fix actual gaps. Do not classify unreviewed calls as unsupported. | Audit pending |
| OUT-001 | Build/Load/Test/Health | Structured reports and concise status fields exist; bare display is verbose and only `text/plain`. | Use sensible existing fields in cells. Record any lesson that needs missing detail; assess native presentation separately. | Usable summaries verified; full audit pending |
| OUT-002 | Health | No `succeeded` property; `status` is available. | Use the real Health result surface; do not copy a generic incorrect summary. | Handling required |
| OUT-003 | Test | A validation finding does not raise an exception; notebook job completion can still be successful. | Display findings and preserve the operation/workflow's actual failure policy. | Failed-report control verified |
| OUT-004 | Other notebook calls | Output quality has not been established for every call. | Inspect existing output, reuse it if useful, and add a specific fix entry only where evidence supports one. | Audit pending |
