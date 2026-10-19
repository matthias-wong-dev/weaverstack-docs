#!/usr/bin/env python3
"""Write the Catalogue Dashboard's pages over a generated estate, for the docs.

Each page is the HTML its page measure returns, with the renderer's style and
script moved to two shared files. The estate is the deterministic one Weaver's
own renderer tests use, stamped at a fixed time, so the pages never age.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("docs/assets/catalogue-dashboard")
OBJECTS = 120
VERSION = "0.10.0"
# 04:00 on 17 October in Canberra, so the nightly runs fall in the small hours there.
AT = datetime(2026, 10, 16, 17, 0, tzinfo=timezone.utc)
TITLES = {
    "overview": "Overview",
    "health": "Health",
    "orchestration": "Orchestration",
    "performance": "Performance",
    "gantt": "Gantt",
    "entities": "Entity dictionary",
    "semantic": "Semantic model",
}


def render(checkout: Path) -> dict[str, str]:
    sys.path[:0] = [str(checkout / "src"), str(checkout / "tests")]
    from support.dashboard_estate import make_estate
    from support.dashboard_payload import PAGES, page_html
    from weaver.catalogue_dashboard import renderer_html

    assert set(PAGES) == set(TITLES), f"Dashboard pages changed: {sorted(PAGES)}"
    found = re.fullmatch(
        r"<style>(.*)</style><script>(.*)</script>", renderer_html(), re.S
    )
    assert found, "Renderer is no longer one style and one script element"
    css, script = found.groups()
    rows = make_estate(OBJECTS, at=AT)
    # The Dashboard is not catalogued; the test estate still records it.
    rows["Installation"] = [
        {**r, "weaver_version": VERSION}
        for r in rows["Installation"]
        if r["item_name"] != "Catalogue Dashboard"
    ]
    files = {"renderer.css": css + "\n", "renderer.js": script + "\n"}
    for page, title in TITLES.items():
        files[f"{page}.html"] = (
            "<!doctype html>\n"
            '<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="robots" content="noindex">\n'
            f"<title>{title} · Catalogue Dashboard demo</title>\n"
            '<link rel="stylesheet" href="renderer.css">\n'
            "<style>html,body{margin:0;height:100%}</style>\n"
            "</head>\n<body>\n"
            + page_html(rows, page, at=AT, renderer="")
            + '\n<script src="renderer.js"></script>\n</body>\n</html>\n'
        )
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--weaver-checkout",
        type=Path,
        default=os.environ.get("WEAVER_CHECKOUT"),
        required="WEAVER_CHECKOUT" not in os.environ,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = render(Path(args.weaver_checkout).resolve())
    if args.write:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (OUTPUT / name).write_text(text, encoding="utf-8")
        print(f"Wrote {len(files)} files to {OUTPUT}")
        return 0
    stale = [
        name
        for name, text in files.items()
        if not (OUTPUT / name).is_file()
        or (OUTPUT / name).read_text(encoding="utf-8") != text
    ]
    if stale:
        print("Regenerate with --write: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"{len(files)} Catalogue Dashboard demo files are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
