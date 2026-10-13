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
    assert home.headings[0] == "Data engineering for Microsoft Fabric."
    assert home.links[0].endswith("/getting-started/first-project/")
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
    basics = next(group["Basics"] for group in nav if "Basics" in group)
    authoring = [next(iter(entry.values())) for entry in basics[1:5]]
    assert authoring == [
        "basics/lakehouse-python.md",
        "basics/lakehouse-spark-sql.md",
        "basics/warehouse-pipeline.md",
        "basics/power-bi/deploy-pbip.md",
    ], authoring
    assert not any(isinstance(entry, dict) and "Power BI" in entry for entry in basics)
    advanced = next(group["Advanced"] for group in nav if "Advanced" in group)
    assert "Semantic models" in advanced[-1]
    assert "Power BI modelling" not in (root / "mkdocs.yml").read_text()
    assert config["site_description"].startswith("Build and operate Microsoft Fabric")
    installation = (root / "docs/getting-started/installation.md").read_text()
    assert "Route 1: native Power BI" not in installation
    assert installation.index("## Configure Fabric access") < installation.index(
        "## Model and Report access"
    )
    counts = {"shared_cli_leaves": 4, "authored_commands_parsed": 0}
    targets = [
        root / f"docs/reference/cli/{name}.md"
        for name in ("build", "load", "test", "health")
    ]
    targets += [
        root / f"docs/{name}.md"
        for name in (
            "basics/development-cycle",
            "basics/recover-failed-work",
            "basics/run-and-inspect-estate",
            "core-concepts/state-and-health",
            "basics/power-bi/fabric-integration",
        )
    ]
    for path in targets:
        text = path.read_text()
        if path.parent.name == "cli":
            intro = text.split("<!-- BEGIN GENERATED CLI -->")[0].lower()
            assert all(term in intro for term in ("lakehouse", "warehouse", "model")), (
                path
            )
        for block in re.findall(
            r"^```bash[^\n]*\n(.*?)^```", text, re.DOTALL | re.MULTILINE
        ):
            for line in block.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts["authored_commands_parsed"] += 1
    for name in (
        "docs/basics/run-and-inspect-estate.md",
        "docs/reference/cli/health.md",
    ):
        text = (root / name).read_text()
        assert "whole installed estate" in text
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
