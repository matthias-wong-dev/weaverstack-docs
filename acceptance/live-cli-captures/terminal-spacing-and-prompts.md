# Terminal spacing and shell prompts

## Scope

- Remove only the installation page's `release-check` review TODO. Keep the install/version commands and the other 18 step-specific TODOs.
- Correct derived terminal whitespace from the saved sanitised ANSI streams. Do not run new Fabric operations or alter captured commands, results, timings or provenance.
- Show `$` on each independent shell command and `>` on continuations, outside copyable text. Keep existing terminal geometry and full-output panels.

## Correction and preservation

The previous cleanup replaced carriage returns with newlines before discarding spinner frames. Each same-row redraw could therefore leave an artificial blank output line. `tools/render_cli_captures.py` now reads ANSI bytes without universal-newline translation and resolves carriage returns as returns to column zero. Genuine internal line feeds and blank lines remain. Unsupported cursor controls are rejected rather than silently discarded.

All 81 retained ANSI streams are byte-identical to the pre-correction snapshot. Every nonblank line in all 81 derived text captures is unchanged. Whitespace changes affect 70 text files; the renderer regenerates the 51 full-output panels on their 17 owning pages. Manifest values are unchanged except for the normalisation-method note.

`tools/terminal_presentation.py` is a static MkDocs build hook. It marks highlighted input lines; CSS supplies their visible prompts. Independent commands, escaped continuations, compound statements and multiline strings/heredocs have regression coverage. Source fences, output text and clipboard payloads contain no added prompts.

## Verification

- `uv run mkdocs build --strict --site-dir ../build/developer`: passed; served developer preview refreshed from that build.
- `python tools/render_cli_captures.py --check`: 51 complete panels match.
- `python -m pytest -q tools`: 31 passed, 1 skipped, 3 subtests passed.
- Ruff lint and format checks on the four changed Python tools/tests: passed.
- Paired-site crawl: 161 HTML pages; 23,906 local links/assets; 270 cross-site links; no broken links/fragments.
- Static build audit: all 194 Bash blocks on 59 pages have their expected attributes, including 343 primary and 169 continuation prompts.
- Existing complete-output browser matrix: 85 states, 255 output-panel checks, desktop/mobile, both themes and JavaScript disabled; passed.
- Existing command/result geometry matrix: 20 states; equal widths, labels, visual prompts and code-only clipboard targets; passed.
- Additional prompt/clipboard matrix: 24 states; 52 actual clipboard readbacks; 136 primary and 80 continuation prompt checks; passed. Source bytes, internal whitespace and copied text match; only one terminal newline may differ.
- Separate source audit verifies immutable ANSI bytes, unchanged nonblank text and manifest provenance, unchanged Markdown outside generated capture bodies and the requested TODO removal.
- Visually inspected desktop installation, mobile dark-theme continuation prompts and compact Build output.

Private QA scripts, inventory, before-text snapshots, JSON results and screenshots are under `/opt/data/scratch/Fors/weaver-docs-refresh/terminal-newline-review/`, with `qa-terminal-newlines-prompts.py` beside that directory. Existing matrix results remain beside the repository worktrees.

No new service run or released-wheel acceptance is implied. The matching-release and publication approval gates remain; this is a correction on the existing draft review branch, not publication.
