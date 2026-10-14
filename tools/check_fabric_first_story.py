#!/usr/bin/env python3
"""Check Fabric-first discovery and commands against the real Weaver parser."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from html.parser import HTMLParser
from pathlib import Path


class Content(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.main = False
        self.parts = []
        self.headings = []
        self.heading = None
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.main = True
        if not self.main:
            return
        if tag in {"h1", "h2", "h3"}:
            self.heading = []
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))

    def handle_endtag(self, tag):
        if tag in {"h1", "h2", "h3"} and self.heading is not None:
            self.headings.append("".join(self.heading))
            self.heading = None
        if tag == "main":
            self.main = False

    def handle_data(self, data):
        if self.main:
            self.parts.append(data)
            if self.heading is not None:
                self.heading.append(data)

    @property
    def text(self):
        return " ".join(self.parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product-site", required=True, type=Path)
    parser.add_argument("--weaver-checkout", required=True, type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.weaver_checkout / "src"))
    import yaml
    from weaver_cli.main import build_parser

    root = Path(__file__).resolve().parents[1]
    site = args.product_site
    pages = {
        str(p.relative_to(site)): Content(p.read_text())
        for p in site.rglob("index.html")
    }
    home = pages["index.html"]
    features = pages["features/index.html"]
    expected = ["Lakehouse", "Warehouse", "Semantic Models", "Reports"]
    for page in (home, features):
        assert [h for h in page.headings if h in expected] == expected
        assert not any("catalogue" in h.lower() for h in page.headings)
    assert home.headings[0] == "Making Fabric easier to use"
    assert home.links[0].endswith("/getting-started/")
    assert (
        "Weaver works with native Fabric Lakehouse and Warehouse items, as well as Power BI projects."
        in features.text
    )
    for page in pages.values():
        assert "Warehouse or Lakehouse" not in page.text
        assert "Power BI and Fabric" not in page.text
    scale = pages["scale/index.html"]
    assert "About an hour" in scale.text and "Under 15 minutes" in scale.text
    assert not any("/pull/" in href for href in scale.links)
    assert not re.search(r"61[.m]|\d+m \d+s", scale.text)
    comparison = pages["vs-dbt/index.html"]
    assert "Native semantic models and Reports" in comparison.headings
    assert "dbt does not deploy native Power BI models or Reports." in comparison.text
    assert any("semantic-layer/power-bi" in href for href in comparison.links)

    config = yaml.load((root / "mkdocs.yml").read_text(), Loader=yaml.BaseLoader)
    nav = config["nav"]
    groups = [next(iter(group)) for group in nav]
    assert groups == [
        "Home",
        "Getting started",
        "Lakehouse",
        "Warehouse",
        "Semantic models",
        "Reports",
        "Coordinate your estate",
        "Reference",
    ], groups
    assert "navigation.sections" not in config["theme"].get("features", [])
    routes = json.loads(
        (root / "acceptance/docs-item-first-2026-10/routes.json").read_text()
    )
    for path in routes["canonical_pages"]:
        target = root / "docs" / path
        assert target.is_file(), path
        body = target.read_text()
        assert re.search(r"^# .+", body, re.MULTILINE), path
        assert not re.search(r"^search:\s*\n\s+exclude: true", body, re.MULTILINE), path
    # These are technical features and boundaries, not prescribed paragraph order.
    native = (root / "docs/semantic-models/native-tmdl.md").read_text()
    assert "Weaver.AutoHideForeignKeys" in native
    assert "shared-policy.md" in native
    validation = (root / "docs/semantic-models/validation.md").read_text()
    assert "EVALUATE" in validation and "weaver test SemanticModel/Parcel" in validation
    assert "SemanticModelSource" not in validation
    reports = (root / "docs/reports/deploy.md").read_text()
    assert "byPath" in reports
    for block in re.findall(
        r"^```bash[^\n]*\n(.*?)^```", reports, re.MULTILINE | re.DOTALL
    ):
        assert not re.search(r"weaver (?:load|test) Report/", block)
    selection = (root / "docs/estate/selective-runs.md").read_text()
    assert all(
        term in selection.lower()
        for term in ("regex", "original", "seed", "--ancestors", "--descendants")
    )
    concurrency = (root / "docs/estate/concurrency.md").read_text()
    assert all(
        term in concurrency for term in ("--concurrency", "execution", "build", "run")
    )
    assert "Making Fabric easier to use" in (root / "docs/index.md").read_text()
    assert (
        "74b4d15ee65ed2740593af1f4d459771b801b132"
        in (root / "docs/getting-started/installation.md").read_text()
    )
    counts = {"shared_cli_leaves": 4, "authored_commands_parsed": 0}
    targets = [
        root / f"docs/reference/cli/{name}.md"
        for name in ("build", "load", "test", "health")
    ]
    targets += [
        root / f"docs/{name}.md"
        for name in (
            "estate/development-cycle",
            "estate/recovery",
            "estate/operate",
            "core-concepts/state-and-health",
            "semantic-models/native-tmdl",
            "semantic-models/validation",
            "estate/environments",
        )
    ]
    for path in targets:
        text = path.read_text()
        for block in re.findall(
            r"^```bash[^\n]*\n(.*?)^```", text, re.DOTALL | re.MULTILINE
        ):
            for line in block.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts["authored_commands_parsed"] += 1
    for name in (
        "docs/estate/operate.md",
        "docs/reference/cli/health.md",
    ):
        text = (root / name).read_text()
        assert re.search(
            r"^weaver health(?: --workspace-config [^\n]+)?$", text, re.MULTILINE
        )
    print(
        json.dumps(
            {
                "fabric_first_discovery": "pass",
                "rounded_scale": "pass",
                "native_model_dbt_comparison": "pass",
                "shared_lifecycle_integration": "pass",
                **counts,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
