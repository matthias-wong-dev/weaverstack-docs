"""Offline drift/ownership tests for CLI and semantic extension extraction."""

from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import generate_cli_reference as cli
import generate_semantic_reference as semantic


class CliReferenceTests(unittest.TestCase):
    def parser(self):
        parser = argparse.ArgumentParser(prog="weaver")
        leaves = parser.add_subparsers(dest="command")
        load = leaves.add_parser("load")
        load.add_argument("--name", action="append")
        load.add_argument("--ancestors", action="store_true")
        load.add_argument("--concurrency", type=int)
        leaves.add_parser("unbind").add_argument("targets", nargs="+")
        return parser

    def test_deterministic_complete_parser_facts(self):
        with (
            patch.object(cli, "_load_parser", return_value=self.parser()),
            patch.object(
                cli, "OWNERSHIP", (("load", "load.md"), ("unbind", "unbind.md"))
            ),
        ):
            first = cli.build_manifest(Path("unused"))
            self.assertEqual(first, cli.build_manifest(Path("unused")))
            self.assertEqual(first["leaf_count"], 2)
            self.assertIn("--concurrency", first["commands"][0]["synopsis"])

    def test_unowned_retired_and_duplicate_are_refused(self):
        for owners, message in [
            ((("load", "load.md"),), "unassigned"),
            (
                (
                    ("load", "load.md"),
                    ("unbind", "unbind.md"),
                    ("removed", "removed.md"),
                ),
                "retired",
            ),
            ((("load", "one.md"), ("load", "two.md")), "more than once"),
        ]:
            with (
                self.subTest(owners=owners),
                patch.object(cli, "_load_parser", return_value=self.parser()),
                patch.object(cli, "OWNERSHIP", owners),
                self.assertRaisesRegex(ValueError, message),
            ):
                cli.build_manifest(Path("unused"))

    def test_markers_and_content_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "load.md"
            page.write_text(f"{cli.BEGIN}\n{cli.END}")
            generated = cli.render_page(cli._leaves(self.parser())[:1])
            self.assertTrue(cli._replace_block(page, generated))
            self.assertFalse(cli._replace_block(page, generated))
            page.write_text(generated + generated)
            with self.assertRaisesRegex(ValueError, "exactly one"):
                cli._replace_block(page, generated)


class SemanticReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "source"
        modules = self.checkout / "src/weaver/semantic_models"
        modules.mkdir(parents=True)
        (modules / "annotation.py").write_text("""raise RuntimeError("must not import")
class Annotation:
    phase = "post_schema"
    @property
    def value(self) -> str: pass
    def apply(self, target) -> None: pass
    def _private(self): pass
class _Compiler: pass
""")
        (modules / "objects.py").write_text("""class TmdlDefinition:
    def __init__(self, parts): pass
    @property
    def parts(self): pass
class TmdlObject:
    def set_expression(self, key, expression): pass
    def __getitem__(self, key): pass
class TmdlCollection:
    def add(self, name, expression=None, *, description=None, **properties): pass
""")
        (self.root / semantic.PAGE).parent.mkdir(parents=True)
        (self.root / semantic.PAGE).write_text(f"{semantic.BEGIN}\n{semantic.END}")

    def tearDown(self):
        self.temporary.cleanup()

    def test_ast_only_deterministic_public_surface(self):
        first = semantic.build_manifest(self.checkout)
        self.assertEqual(first, semantic.build_manifest(self.checkout))
        self.assertEqual(len(first["classes"]), 4)
        rendered = semantic.render(first)
        self.assertNotIn("_private", rendered)
        self.assertNotIn("_Compiler", rendered)
        self.assertIn("Annotation.value  # property", rendered)
        self.assertIn("description=None, **properties", rendered)

    def test_signature_and_property_drift(self):
        semantic.update(self.root, self.checkout, write=True)
        semantic.update(self.root, self.checkout, write=False)
        path = self.checkout / "src/weaver/semantic_models/annotation.py"
        path.write_text(path.read_text().replace("-> str", "-> bytes"))
        with self.assertRaisesRegex(ValueError, "drift"):
            semantic.update(self.root, self.checkout, write=False)

    def test_missing_class_and_duplicate_member_are_refused(self):
        path = self.checkout / "src/weaver/semantic_models/annotation.py"
        original = path.read_text()
        path.write_text(original.replace("class Annotation:", "class Renamed:"))
        with self.assertRaisesRegex(ValueError, "expected one class"):
            semantic.build_manifest(self.checkout)
        path.write_text(
            original.replace(
                "def _private(self): pass", "def apply(self, target): pass"
            )
        )
        with self.assertRaisesRegex(ValueError, "duplicate public member"):
            semantic.build_manifest(self.checkout)

    def test_repeated_or_reversed_markers_are_refused(self):
        page = self.root / semantic.PAGE
        for text in [semantic.BEGIN * 2 + semantic.END, semantic.END + semantic.BEGIN]:
            page.write_text(text)
            with self.assertRaisesRegex(ValueError, "ordered marker"):
                semantic.update(self.root, self.checkout, write=True)


if __name__ == "__main__":
    unittest.main()
