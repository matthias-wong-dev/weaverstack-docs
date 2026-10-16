"""Render captured terminal text without changing its words, whitespace or outcomes."""

from __future__ import annotations

import argparse
import json
import os
import re
from html import escape
from pathlib import Path


def _line(line: str) -> str:
    colour = None
    if not re.fullmatch(r"\s*0 (?:passed|failed|succeeded|blocked|invalid)\s*", line):
        if re.search(r"✗|\berror:|\b(?:Red|failed|invalid)\b", line):
            colour = "red"
        elif re.search(r"\b(?:Amber|pending|blocked|warning)\b", line):
            colour = "amber"
        elif re.search(r"✓|\b(?:Green|passed|succeeded)\b", line):
            colour = "green"
    text = escape(line)
    return f'<span class="terminal-status-{colour}">{text}</span>' if colour else text


def _pre(text: str) -> str:
    styled = "\n".join(_line(line) for line in text.split("\n"))
    return (
        '<pre tabindex="0" aria-label="Captured terminal output"><code>'
        + styled
        + "</code></pre>"
    )


def render_terminal(
    text: str,
    *,
    title: str,
    raw_href: str,
    exit_code: int,
    full_text: str | None = None,
    excerpted: bool = False,
) -> str:
    manifest_href = str(Path(raw_href).with_name("manifest.json"))
    full = ""
    if full_text is not None and full_text != text:
        full = (
            "<details><summary>Show the complete capture</summary>"
            + _pre(full_text)
            + "</details>"
        )
    return (
        '<p class="terminal-intro">The command returned:</p>\n'
        f'<figure class="weaver-terminal" aria-label="{escape(title, quote=True)}">\n'
        f'<figcaption>Terminal output <span class="terminal-exit">exit {int(exit_code)}</span></figcaption>\n'
        + _pre(text)
        + "\n"
        + full
        + f'<p class="terminal-source"><a href="{escape(raw_href, quote=True)}">Sanitised transcript</a>'
        + f' · <a href="{escape(manifest_href, quote=True)}">Capture details</a>'
        + (" · Transcript excerpt" if excerpted else "")
        + " · Live CLI capture; progress redraws omitted.</p>\n</figure>"
    )


def excerpt(text: str, *, start: str | None = None, end: str | None = None) -> str:
    lines = text.splitlines(keepends=True)
    first = next(i for i, line in enumerate(lines) if start in line) if start else 0
    last = (
        next(i for i in range(first + 1, len(lines)) if end in lines[i])
        if end
        else len(lines)
    )
    return "".join(lines[first:last])


BLOCK = re.compile(
    r"(<!-- cli-capture: ([^\n]+) -->\n)(.*?)(<!-- /cli-capture -->)", re.DOTALL
)


def asset_href(page: Path, asset: Path) -> str:
    route = page.parent if page.name == "index.md" else page.with_suffix("")
    return os.path.relpath(asset, route)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    docs = Path(__file__).resolve().parents[1] / "docs"
    assets = docs / "assets/cli-captures"
    manifest = json.loads((assets / "manifest.json").read_text())
    captures = {entry["label"]: entry for entry in manifest["captures"]}
    count = 0
    for page in sorted(docs.rglob("*.md")):
        original = page.read_text()
        matches = list(BLOCK.finditer(original))
        assert (
            len(matches)
            == original.count("<!-- cli-capture: ")
            == original.count("<!-- /cli-capture -->")
        ), page

        def replace(match, page=page):
            spec = json.loads(match[2])
            record = captures[spec["id"]]
            text = (assets / record["text"]).read_text()
            selected = excerpt(text, start=spec.get("start"), end=spec.get("end"))
            html = render_terminal(
                selected,
                title=spec["title"],
                raw_href=asset_href(page, assets / record["text"]),
                exit_code=record["exit_code"],
                full_text=text if spec.get("full") else None,
                excerpted=selected != text,
            )
            return match[1] + html + "\n" + match[4]

        updated = BLOCK.sub(replace, original)
        if args.write:
            if updated != original:
                page.write_text(updated)
        else:
            assert updated == original, (
                f"{page}: capture rendering drift; run with --write"
            )
        count += len(matches)
    assert count > 0, "No integrated capture panels were checked"
    print(f"PASS: {count} panels match their sanitised real transcripts")


if __name__ == "__main__":
    main()
