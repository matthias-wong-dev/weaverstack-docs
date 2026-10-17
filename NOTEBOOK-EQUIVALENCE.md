# Notebook equivalence delivery

This is a maintainer plan, not a public documentation page.

## Implementation and current acceptance

- Every terminal fence is paired: **232 blocks across 59 pages**, producing **383 native cells**. Setup, interactive sessions, management and inspection are included. There are no CLI-only exemptions or subprocess substitutes in the emitted cells.
- All generated operation calls are bound against the public signatures. Workspace selection is explicit; configuration, filters, ordering and Session reuse are retained. The older hand-authored Notebook examples now name their workspace too.
- Destructive operations and unconfirmed workflows have separate review and execution cells. Mirror reviews the existing resolved plan through `check_mirror(...).describe()` and passes that exact plan to execution.
- All **29 cell-operation categories** have an output assessment in `generated/notebook-output-audit.json`. Existing report mappings, Environment dictionaries, resolved-plan descriptions, help text, destination paths and quiet setup/close behaviour are reused. No synthetic service result is supplied.
- **68 cells have static authentic outputs**. This is not a claim that every documented scenario was executed in a Notebook. Missing captures remain explicitly separate from missing or inadequate API output.
- The matching development runtime passed **7,827 core tests** and the current-head Windows CI. A real Fabric Notebook recorded **50 cells without execution errors**, including all eight Warehouse/Lakehouse Build/Load/Test/Health calls and a deliberately failed Test/workflow. Job completion is not used as a substitute for the returned reports.
- The exact first-task native cells were replayed and their eight operation outputs integrated. Native Notebook create/update/run and frozen-bundle installation were also exercised. Owned resource identities and definitions were read back privately.
- Native Power BI deployment reached the owned model and Report, but Report-binding verification and model refresh returned **HTTP 403** under the Notebook identity. The failed Build report is preserved. No tenant/identity setting or connection was changed. Catalogue-free Health and Test run from the wrong source directory were invalid probe requests, not API-equivalence defects.
- Azure SDK capacity request/state handling is tested locally. No live capacity resume/suspend is authorised or claimed. Development-Environment publication is not a public package release.

Implementation and source/type output coverage do not close the remaining live, matching-release or publication gates. The accepted all-block requirement below is unchanged.

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

## Historical probe evidence

The scratch Fabric notebook exercised Initialise plus Build, Load, Test and Health against dedicated Warehouse/Lakehouse targets. The final capture contains 37 cases. All eight ordinary operation calls completed successfully. Assigned reports produced no cell streams; bare report display supplied long `text/plain` representations. Explicit status summaries were readable.

A deliberately unequal Test returned a failed validation report without an exception while the notebook job completed. Result inspection must not be replaced by job-completion status. Health exposes `status` rather than the other reports' `succeeded` property. These differences must be handled accurately, without inventing uniform report fields.

Probe evidence remains under `/opt/data/scratch/Fors/weaver-notebook-equivalence-2026-10-17/`. Its runtime and source boundaries are recorded there; observed results are not automatically evidence for later product changes.

## Delivery status

- Complete terminal inventory and public-call parameter binding are checked in.
- Missing public entry points and configuration/Session parity fixes are in the separate runtime PR.
- Native code/result tab presentation is wired into MkDocs and the private preview.
- Every emitted cell has an output assessment; genuine static observations are retained separately from source/type coverage.
- Live Notebook Power BI access, unexecuted live Azure capacity control and matching public-package acceptance remain held gates, not waived requirements.

Blocks, calls, parameter checks, observed outputs and remaining fixes have separate statuses in this plan and the generated audit.

## Output and API findings

| ID | Surface | Finding | Required treatment | State |
|---|---|---|---|---|
| API-001 | Check | The original probe found `weaver.check` absent. | Public export and native regression in runtime/API PR #226. | Fixed; matching Notebook runtime verified |
| API-002 | Management/workflow/install | Missing public entry points and parameter/configuration gaps. | Native public wrappers, shared grammar, workflow, capacity and sealed-target confirmation in #226. | Implemented; signature binding covers the full generated corpus; live scope and exceptions above |
| OUT-001 | Build/Load/Test/Health | Existing structured reports are useful; bare object display is verbose. | Use their existing `to_mapping()` surfaces. | Implemented and captured for both Warehouse and Lakehouse |
| OUT-002 | Health | No `succeeded` property; `status` is available. | Preserve the real Health result surface. | Implemented |
| OUT-003 | Test | A validation finding does not raise an exception; notebook job completion can still be successful. | Display findings and preserve the operation/workflow's actual failure policy. | Failed-report control verified |
| OUT-004 | Other notebook calls | Output surfaces differ by result type. | Audit all categories; use `.as_dict()`, `.to_mapping()`, resolved `.describe()` or existing text/quiet behaviour as appropriate. | All 383 cells classified in the generated output audit; execution coverage recorded separately |
| OUT-005 | Unqualified package help | `help(weaver)` produced a 140 KB package dump rather than a useful operation index. | The root discovery cell prints the actual `weaver.__all__` index; operation-specific cells keep `help(weaver.operation)`. Both outputs were executed and recaptured. | Fixed without excerpting an output or adding a runtime API |
