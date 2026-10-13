#!/usr/bin/env python3
"""Crawl built product/developer links and reconcile historical benchmark rows."""

from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        key = "href" if tag in {"a", "link"} else "src"
        if tag in {"a", "link", "script", "img"} and attrs.get(key):
            self.links.append(attrs[key])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product-site", required=True, type=Path)
    parser.add_argument("--developer-site", required=True, type=Path)
    args = parser.parse_args()
    roots = {
        "weaverstack.dev": args.product_site.resolve(),
        "docs.weaverstack.dev": args.developer_site.resolve(),
    }
    pages = {
        path: Page(path) for root in roots.values() for path in root.rglob("*.html")
    }
    checked = 0
    crossed = 0
    for host, root in roots.items():
        for path, page in pages.items():
            if not path.is_relative_to(root):
                continue
            relative = path.relative_to(root).as_posix()
            base = f"https://{host}/" + (relative.removesuffix("index.html"))
            for href in page.links:
                resolved = urlsplit(urljoin(base, href))
                if resolved.netloc not in roots or resolved.scheme not in {
                    "http",
                    "https",
                }:
                    continue
                target_root = roots[resolved.netloc]
                target = target_root / unquote(resolved.path).lstrip("/")
                if target.is_dir():
                    target = target / "index.html"
                assert target.is_file(), (relative, href, str(target))
                if resolved.fragment and target.suffix == ".html":
                    assert unquote(resolved.fragment) in pages[target].ids, (
                        relative,
                        href,
                        "missing fragment",
                    )
                checked += 1
                crossed += int(resolved.netloc != host)
    data = json.loads(
        (args.product_site / "assets/data/scale-benchmark.json").read_text()
    )
    source = (
        Path(__file__).resolve().parents[1]
        / "acceptance/docs-refresh-2026-10/scale-measurements.md"
    )
    text = source.read_text()
    for operation in data["operations"]:
        assert (
            f"| {operation['label']} | {operation['seconds']} | {operation['display']} |"
            in text
        )
    assert data["source_revision"] in text
    assert (
        sum(data["counts"][kind] for kind in ["tables", "views", "folders"])
        == data["counts"]["declared_objects"]
    )
    print(
        json.dumps(
            {
                "html_pages": len(pages),
                "local_links_and_assets": checked,
                "cross_site_links": crossed,
                "broken_links_or_fragments": 0,
                "benchmark_rows": len(data["operations"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
