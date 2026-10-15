#!/usr/bin/env python3
"""Keep displayed Initialise files equal to the installed generator's sources."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(
    r"(<!-- initialise:([^\s]+) -->\n(?:[ \t]*\n)*```[^\n]*\n)(.*?)(```\n(?:[ \t]*\n)*<!-- /initialise -->)",
    re.S,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sys.path.insert(0, str(args.weaver_checkout.resolve() / "src"))
    from weaver.initialise import _generated_files
    from weaver.onboarding.project import ProjectRequest

    generated = _generated_files(
        ProjectRequest(
            workspace="Parcel Development",
            catalogue="Catalogue",
            environment="Weaver",
            lakehouse="Landing",
            warehouse="Operations",
            semantic_model="Parcel",
            example="Parcel",
        )
    )
    count = 0
    drift = []
    for page in sorted((ROOT / "docs").rglob("*.md")):
        before = page.read_text()
        marked = before.count("<!-- initialise:")
        assert (
            len(BLOCK.findall(before)) == marked == before.count("<!-- /initialise -->")
        ), f"Malformed generated-source marker: {page}"

        def replace(match):
            nonlocal count
            count += 1
            return match[1] + generated[match[2]].rstrip("\n") + "\n" + match[4]

        after = BLOCK.sub(replace, before)
        if after != before:
            drift.append(str(page.relative_to(ROOT)))
            if not args.check:
                page.write_text(after)
    assert count, "No generated-file snippets were checked"
    if args.check and drift:
        raise SystemExit("Generated snippets differ: " + ", ".join(drift))
    print(f"PASS: {count} displayed generated files match Initialise")


if __name__ == "__main__":
    main()
