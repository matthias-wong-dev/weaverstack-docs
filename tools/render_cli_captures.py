"""Render captured terminal text without changing its words, whitespace or outcomes."""

from __future__ import annotations

import argparse
import json
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
        '<pre tabindex="0" aria-label="Terminal output"><code>'
        + styled
        + "</code></pre>"
    )


def render_terminal(text: str, *, title: str, exit_code: int) -> str:
    return (
        '<p class="terminal-intro">The command returned:</p>\n'
        f'<figure class="weaver-terminal" aria-label="{escape(title, quote=True)}">\n'
        f'<figcaption>Terminal output <span class="terminal-exit">exit {int(exit_code)}</span></figcaption>\n'
        + _pre(text)
        + "\n</figure>"
    )


BLOCK = re.compile(
    r"(<!-- cli-capture: ([^\n]+) -->\n)(.*?)(<!-- /cli-capture -->)", re.DOTALL
)


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

        def replace(match):
            spec = {
                key: value
                for key, value in json.loads(match[2]).items()
                if key not in {"start", "end", "full"}
            }
            record = captures[spec["id"]]
            text = (assets / record["text"]).read_text()
            html = render_terminal(
                text,
                title=spec["title"],
                exit_code=record["exit_code"],
            )
            marker = (
                "<!-- cli-capture: " + json.dumps(spec, ensure_ascii=False) + " -->\n"
            )
            return marker + html + "\n" + match[4]

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
    print(f"PASS: {count} panels match their complete real transcripts")


if __name__ == "__main__":
    main()
