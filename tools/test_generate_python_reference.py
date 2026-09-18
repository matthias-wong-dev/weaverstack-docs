from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import generate_python_reference as reference


class PythonReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        package = self.root / "source" / "src" / "weaver"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text(
            "from .api import OriginalResult as Result, run\n"
            "__version__ = '1.2.3'\n"
            "__all__ = ['__version__', 'run', 'Result']\n",
            encoding="utf-8",
        )
        (package / "api.py").write_text(
            "from dataclasses import dataclass\n"
            "@dataclass\n"
            "class OriginalResult:\n"
            "    value: str\n"
            "def run(value: str, *, count: int = 1) -> OriginalResult:\n"
            "    return OriginalResult(value * count)\n",
            encoding="utf-8",
        )
        self.checkout = self.root / "source"
        self.ownership = (
            ("__version__", "docs/reference/python/index.md"),
            ("run", "docs/reference/python/operations.md"),
            ("Result", "docs/reference/python/results.md"),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_manifest_covers_exports_and_is_deterministic(self) -> None:
        first = reference.build_manifest(self.checkout, ownership=self.ownership)
        second = reference.build_manifest(self.checkout, ownership=self.ownership)

        self.assertEqual(first, second)
        self.assertEqual(first["export_count"], 3)
        self.assertEqual(
            [fact["name"] for fact in first["exports"]],
            ["Result", "__version__", "run"],
        )
        run = next(fact for fact in first["exports"] if fact["name"] == "run")
        self.assertEqual(
            run["signature"],
            "(value: str, *, count: int=1) -> OriginalResult",
        )
        result = next(fact for fact in first["exports"] if fact["name"] == "Result")
        self.assertEqual(result["kind"], "class")
        self.assertNotIn("signature", result)

    def test_unassigned_export_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "public exports are unassigned: Result"
        ):
            reference.build_manifest(self.checkout, ownership=self.ownership[:-1])

    def test_duplicate_assignment_is_rejected(self) -> None:
        duplicated = (*self.ownership, ("run", "docs/reference/python/index.md"))
        with self.assertRaisesRegex(
            ValueError, "public exports assigned more than once: run"
        ):
            reference.build_manifest(self.checkout, ownership=duplicated)

    def test_retired_assignment_is_rejected(self) -> None:
        retired = (*self.ownership, ("removed", "docs/reference/python/old.md"))
        with self.assertRaisesRegex(
            ValueError, "retired public exports remain owned: removed"
        ):
            reference.build_manifest(self.checkout, ownership=retired)

    def test_present_pages_mode_skips_absent_pages_and_detects_drift(self) -> None:
        docs = self.root / "docs" / "reference" / "python"
        docs.mkdir(parents=True)
        page = docs / "index.md"
        page.write_text(
            f"# Python API\n\n{reference.BEGIN}\nplaceholder\n{reference.END}\n",
            encoding="utf-8",
        )
        manifest_path = Path("generated/python-reference.json")
        reference.write(
            self.root,
            self.checkout,
            manifest_path,
            ownership=self.ownership,
        )

        exports, checked, missing = reference.check(
            self.root,
            self.checkout,
            manifest_path,
            present_only=True,
            ownership=self.ownership,
        )
        self.assertEqual((exports, checked), (3, 1))
        self.assertEqual(len(missing), 2)

        with self.assertRaisesRegex(ValueError, "mapped pages are absent"):
            reference.check(
                self.root,
                self.checkout,
                manifest_path,
                present_only=False,
                ownership=self.ownership,
            )

        page.write_text(
            page.read_text(encoding="utf-8").replace("Kind: value", "Kind: changed"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "generated Python block has drifted"):
            reference.check(
                self.root,
                self.checkout,
                manifest_path,
                present_only=True,
                ownership=self.ownership,
            )


if __name__ == "__main__":
    unittest.main()
