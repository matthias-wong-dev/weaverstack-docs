#!/usr/bin/env python3
"""Check item-first route retention; reader/editorial acceptance remains separate.

Uses the locked docs environment (Markdown and PyYAML). Without --developer-site,
checks Markdown-rendered IDs and source links, not built search or template output.
With a built site, checks its actual HTML URLs, article links and search index.
A successful run is not evidence that every original explanation survived editing;
the reference-route audit and independent reader review own that judgement.
"""

from __future__ import annotations

import argparse
import json
import posixpath
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import markdown
import yaml

HOST = "docs.weaverstack.dev"


def route(path):
    """Map a MkDocs Markdown path to its public directory URL."""
    stem = path.removesuffix(".md")
    if stem == "index":
        return "/"
    return "/" + stem.removesuffix("/index") + "/"


class Page(HTMLParser):
    def __init__(self, html, *, article_only=True):
        super().__init__()
        self.article_only = article_only
        self.ids = set()
        self.events = []
        self.in_article = not article_only
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.in_article = True
        identifier = attrs.get("id") or (attrs.get("name") if tag == "a" else None)
        if identifier:
            self.ids.add(identifier)
            if self.in_article:
                self.events.append(("id", identifier))
        if (
            tag == "a"
            and attrs.get("href")
            and self.in_article
            and "headerlink" not in (attrs.get("class") or "").split()
        ):
            self.events.append(("link", attrs["href"]))

    def handle_endtag(self, tag):
        if tag == "article" and self.article_only:
            self.in_article = False


def metadata(text):
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return yaml.safe_load(parts[1]) or {}, parts[2]
    return {}, text


def source_page(text, config):
    _, text = metadata(text)
    extensions = []
    options = {}
    for entry in config.get("markdown_extensions", ["toc"]):
        if isinstance(entry, str):
            extensions.append(entry)
        else:
            for name, settings in entry.items():
                extensions.append(name)
                options[name] = settings or {}
    html = markdown.markdown(text, extensions=extensions, extension_configs=options)
    return Page("<article>" + html + "</article>")


def nav_paths(nav):
    if isinstance(nav, str):
        yield nav
    elif isinstance(nav, dict):
        for child in nav.values():
            yield from nav_paths(child)
    elif isinstance(nav, list):
        for child in nav:
            yield from nav_paths(child)


def resolve(href, source, *, rendered=False, host=HOST):
    """Resolve Markdown links before rendering, or HTML links after rendering."""
    if not rendered and not urlsplit(href).scheme and not href.startswith("//"):
        link = urlsplit(href)
        if link.path.endswith(".md"):
            path = posixpath.normpath(
                posixpath.join(posixpath.dirname(source), link.path)
            )
            return HOST, route(path.lstrip("/")), unquote(link.fragment)
    base = f"https://{host}" + (source if rendered else route(source))
    link = urlsplit(urljoin(base, href))
    path = unquote(link.path)
    if path.endswith("/index.html"):
        path = path.removesuffix("index.html")
    return link.netloc, path, unquote(link.fragment)


def audit(root, records, developer_site=None, product_site=None):
    errors = []
    config = yaml.safe_load((root / "mkdocs.yml").read_text())
    top = [
        name
        for group in config.get("nav", [])
        if isinstance(group, dict)
        for name in group
    ]
    expected_top = [
        "Home",
        "Getting started",
        "Lakehouse",
        "Warehouse",
        "Semantic models",
        "Reports",
        "Coordinate your estate",
        "Reference",
    ]
    if top != expected_top:
        errors.append(f"item navigation order: expected {expected_top}, got {top}")
    nav = set(nav_paths(config.get("nav", [])))
    moves = records["moves"]
    pages = {}
    excluded = set()
    for path in sorted((root / "docs").rglob("*.md")):
        relative = path.relative_to(root / "docs").as_posix()
        text = path.read_text()
        meta, _ = metadata(text)
        if meta.get("search", {}).get("exclude") is True:
            excluded.add(relative)
        if developer_site:
            html = developer_site / route(relative).lstrip("/") / "index.html"
            if not html.is_file():
                errors.append(f"missing rendered page: {relative}")
                continue
            pages[relative] = Page(html.read_text())
        else:
            pages[relative] = source_page(text, config)
    urls = {route(path): path for path in pages}
    checked_links = 0

    def target(href, source, *, rendered=None, host=HOST):
        nonlocal checked_links
        is_rendered = bool(developer_site) if rendered is None else rendered
        hostname, url, fragment = resolve(href, source, rendered=is_rendered, host=host)
        if hostname != HOST:
            return None, fragment
        destination = urls.get(url)
        if destination is None:
            # This gate covers pages, not CSS/images/downloads; the paired crawl owns assets.
            if url.endswith(("/", ".html", ".md")):
                errors.append(f"unresolved documentation URL: {source} -> {href}")
            return None, fragment
        checked_links += 1
        if fragment and fragment not in pages[destination].ids:
            errors.append(f"missing target fragment: {source} -> {href}")
        return destination, fragment

    for path, url in records["original_urls"].items():
        if route(path) != url:
            errors.append(
                f"original URL no longer matches Markdown route: {path} -> {url}"
            )
        if path not in pages:
            errors.append(f"missing original page: {path}")
            continue
        for identifier in records["original_fragments"][path]:
            if identifier not in pages[path].ids:
                errors.append(f"missing original fragment: {path}#{identifier}")
        if path not in moves and path in excluded:
            errors.append(f"retained page excluded from search: {path}")

    for path in records["canonical_pages"]:
        if path not in pages:
            errors.append(f"missing canonical page: {path}")
        if path not in nav:
            errors.append(f"canonical page absent from nav: {path}")
        if path in excluded or path in moves:
            errors.append(f"canonical page is a pointer/search stub: {path}")

    for path, owner in moves.items():
        if path not in pages:
            continue
        if path not in excluded:
            errors.append(f"retired page not search-excluded: {path}")
        if path in nav:
            errors.append(f"retired page still in nav: {path}")
        if owner in moves or owner in excluded:
            errors.append(f"pointer chain: {path} -> {owner}")
        events = pages[path].events
        for identifier in records["original_fragments"][path]:
            start = next(
                (i for i, event in enumerate(events) if event == ("id", identifier)),
                None,
            )
            if start is None:
                continue
            href = next(
                (
                    value
                    for kind, value in events[start + 1 :]
                    if kind == "link" and not value.startswith("#")
                ),
                None,
            )
            if href is None:
                errors.append(
                    f"legacy ID has no contextual direct link: {path}#{identifier}"
                )
                continue
            actual, fragment = target(href, route(path) if developer_site else path)
            intended = (
                records["fragment_overrides"].get(path, {}).get(identifier, owner)
            )
            expected_path, _, expected_fragment = intended.partition("#")
            if actual != expected_path or (
                expected_fragment and fragment != expected_fragment
            ):
                errors.append(
                    f"wrong fragment destination: {path}#{identifier} -> {href}; expected {intended}"
                )

    for path, page in pages.items():
        for kind, href in page.events:
            if kind != "link":
                continue
            destination, _ = target(href, route(path) if developer_site else path)
            if destination in moves and destination != path:
                label = "pointer chain" if path in moves else "noncanonical inbound"
                errors.append(f"{label}: {path} -> {href}")

    if product_site:
        if not product_site.is_dir() or not any(product_site.rglob("*.html")):
            errors.append(f"product site missing or contains no HTML: {product_site}")
        if not developer_site:
            errors.append(
                "--product-site requires --developer-site for actual cross-site URLs"
            )
        for path in sorted(product_site.rglob("*.html")):
            relative = path.relative_to(product_site).as_posix()
            # Product incoming links include navigation and footers, not only articles.
            page = Page(path.read_text(), article_only=False)
            for kind, href in page.events:
                if kind != "link":
                    continue
                destination, _ = target(
                    href, "/" + relative, rendered=True, host="weaverstack.dev"
                )
                if destination in moves:
                    errors.append(f"noncanonical product inbound: {relative} -> {href}")

    if developer_site:
        search = developer_site / "search/search_index.json"
        if not search.is_file():
            errors.append("built search index missing")
        else:
            locations = {
                urlsplit(entry["location"]).path
                for entry in json.loads(search.read_text())["docs"]
            }
            for path in moves:
                if route(path).lstrip("/") in locations or route(path) in locations:
                    errors.append(f"retired search result: {path}")
            for path in (set(records["original_urls"]) - set(moves)) | set(
                records["canonical_pages"]
            ):
                if (
                    route(path).lstrip("/") not in locations
                    and route(path) not in locations
                ):
                    errors.append(f"live explanation missing from search: {path}")

    return sorted(set(errors)), {
        "original_pages": len(records["original_urls"]),
        "original_fragments": sum(map(len, records["original_fragments"].values())),
        "canonical_pages": len(records["canonical_pages"]),
        "canonical_present": sum(path in pages for path in records["canonical_pages"]),
        "compatibility_routes": len(moves),
        "documentation_links_checked": checked_links,
        "rendered": bool(developer_site),
        "editorial_acceptance": "not assessed by this gate",
    }


def self_test():
    """Exercise route/pointer refusals without touching repository content."""
    import unittest

    class Routes(unittest.TestCase):
        def test_markdown_route_is_an_actual_directory_url(self):
            self.assertEqual(route("reference/cli.md"), "/reference/cli/")
            self.assertEqual(route("lakehouse/index.md"), "/lakehouse/")
            self.assertEqual(route("index.md"), "/")

    class Audit(unittest.TestCase):
        def test_missing_original_fragment_cannot_pass(self):
            import tempfile

            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "docs").mkdir()
                (root / "docs/old.md").write_text(
                    "# Old\n\nUseful existing explanation.\n"
                )
                records = {
                    "original_urls": {"old.md": "/old/"},
                    "original_fragments": {"old.md": ["old", "original-detail"]},
                    "canonical_pages": [],
                    "moves": {},
                    "fragment_overrides": {},
                }
                (root / "mkdocs.yml").write_text(
                    "nav: []\nmarkdown_extensions: [toc]\n"
                )
                errors, counts = audit(root, records)
                self.assertTrue(any("original-detail" in e for e in errors), errors)
                self.assertEqual(counts["original_pages"], 1)

    class Compatibility(unittest.TestCase):
        def setUp(self):
            import tempfile

            self.temp = tempfile.TemporaryDirectory()
            self.addCleanup(self.temp.cleanup)
            self.root = Path(self.temp.name)
            (self.root / "docs").mkdir()
            (self.root / "docs/new.md").write_text(
                "# New\n\n## Details\n\nA real explanation.\n"
            )
            (self.root / "docs/old.md").write_text(
                "---\nsearch:\n  exclude: true\n---\n# Old\n\n[Read details](new.md#details)\n"
            )
            (self.root / "mkdocs.yml").write_text(
                "nav:\n  - Home: new.md\n  - Getting started: []\n  - Lakehouse: []\n  - Warehouse: []\n  - Semantic models: []\n  - Reports: []\n  - Coordinate your estate: []\n  - Reference: []\nmarkdown_extensions: [toc]\n"
            )
            self.records = {
                "original_urls": {"old.md": "/old/"},
                "original_fragments": {"old.md": ["old"]},
                "canonical_pages": ["new.md"],
                "moves": {"old.md": "new.md"},
                "fragment_overrides": {"old.md": {"old": "new.md#details"}},
            }

        def test_item_order_is_checked_without_locking_prose(self):
            (self.root / "mkdocs.yml").write_text(
                "nav:\n  - Home: new.md\n  - Getting started: []\n  - Warehouse: []\n  - Lakehouse: []\n  - Semantic models: []\n  - Reports: []\n  - Coordinate your estate: []\n  - Reference: []\nmarkdown_extensions: [toc]\n"
            )
            errors, _ = audit(self.root, self.records)
            self.assertTrue(any("item navigation order" in e for e in errors), errors)

        def test_direct_pointer_passes(self):
            errors, _ = audit(self.root, self.records)
            self.assertEqual(errors, [])

        def test_missing_canonical_page_fails(self):
            (self.root / "docs/new.md").unlink()
            errors, _ = audit(self.root, self.records)
            self.assertTrue(any("canonical page" in e for e in errors), errors)

        def test_wrong_fragment_intent_fails_despite_resolving_link(self):
            (self.root / "docs/old.md").write_text(
                "---\nsearch:\n  exclude: true\n---\n# Old\n\n[Read](new.md)\n"
            )
            errors, _ = audit(self.root, self.records)
            self.assertTrue(any("fragment destination" in e for e in errors), errors)

        def test_pointer_chain_fails(self):
            (self.root / "docs/new.md").write_text(
                "---\nsearch:\n  exclude: true\n---\n# New\n\n## Details\n\n[Read](old.md)\n"
            )
            errors, _ = audit(self.root, self.records)
            self.assertTrue(any("pointer chain" in e for e in errors), errors)

        def test_retained_page_must_remain_searchable(self):
            self.records["moves"] = {}
            errors, _ = audit(self.root, self.records)
            self.assertTrue(any("retained page excluded" in e for e in errors), errors)

        def test_local_fragment_is_not_an_inbound_to_a_retired_route(self):
            text = (self.root / "docs/old.md").read_text()
            (self.root / "docs/old.md").write_text(text + "\n[Local](#old)\n")
            errors, _ = audit(self.root, self.records)
            self.assertEqual(errors, [])

        def test_product_footer_after_article_is_checked(self):
            site = self.root / "site"
            for name, html in {
                "old": '<article><h1 id="old">Old</h1><a href="../new/#details">Read</a></article>',
                "new": '<article><h1 id="new">New</h1><h2 id="details">Details</h2></article>',
            }.items():
                (site / name).mkdir(parents=True)
                (site / name / "index.html").write_text(html)
            (site / "search").mkdir()
            (site / "search/search_index.json").write_text(
                json.dumps({"docs": [{"location": "new/"}]})
            )
            product = self.root / "product"
            product.mkdir()
            page = product / "index.html"
            page.write_text(
                '<article>Product</article><footer><a href="https://docs.weaverstack.dev/old/">Docs</a></footer>'
            )
            errors, _ = audit(self.root, self.records, site, product)
            self.assertTrue(
                any("noncanonical product inbound" in e for e in errors), errors
            )

        def test_missing_product_site_cannot_pass(self):
            errors, _ = audit(
                self.root, self.records, None, self.root / "missing-product"
            )
            self.assertTrue(any("product site missing" in e for e in errors), errors)

        def test_live_narrative_must_not_link_to_retired_page(self):
            (self.root / "docs/new.md").write_text(
                "# New\n\n## Details\n\n[Back](old.md)\n"
            )
            errors, _ = audit(self.root, self.records)
            self.assertTrue(any("noncanonical inbound" in e for e in errors), errors)

    suite = unittest.TestSuite(
        unittest.defaultTestLoader.loadTestsFromTestCase(cls)
        for cls in (Routes, Audit, Compatibility)
    )
    result = unittest.TextTestRunner().run(suite)
    return int(not result.wasSuccessful())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--developer-site", type=Path)
    parser.add_argument("--product-site", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    records = json.loads(
        (args.root / "acceptance/docs-item-first-2026-10/routes.json").read_text()
    )
    errors, counts = audit(args.root, records, args.developer_site, args.product_site)
    print(json.dumps({**counts, "errors": errors}, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
