"""Offline tests for complete deterministic catalogue inventory extraction."""

from __future__ import annotations

import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import generate_catalogue_reference as reference


class CatalogueReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "product"
        self.source = self.checkout / "src/weaver/catalogue/tables.py"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("# source identity\n")
        column = types.SimpleNamespace(
            warehouse_type="varchar(128)",
            not_null=True,
            description="Item name.",
            vocabulary=None,
        )
        self.table = types.SimpleNamespace(
            qualified="_.Installation",
            description="Bindings",
            key=("item_name",),
            physical_columns=("item_name", "row_insert_datetime"),
            column=lambda name: column,
            public_name_of=lambda name: {
                "item_name": "Item name",
                "row_insert_datetime": "Row insert datetime",
            }[name],
        )
        self.mirror = types.SimpleNamespace(**vars(self.table))
        self.mirror.qualified = "_.Mirror"
        self.module = types.SimpleNamespace(
            __file__=str(self.source),
            CATALOGUE_TABLES=(self.table,),
            MIRROR=self.mirror,
            AUDIT_COLUMN_NAMES=("row_insert_datetime",),
        )
        (self.root / reference.PAGE).parent.mkdir(parents=True)
        (self.root / reference.PAGE).write_text(f"{reference.BEGIN}\n{reference.END}")

    def tearDown(self):
        self.temporary.cleanup()

    def test_complete_inventory_including_optional_mirror_and_audit(self):
        with patch("importlib.import_module", return_value=self.module):
            first = reference.build_manifest(self.checkout)
            self.assertEqual(first, reference.build_manifest(self.checkout))
            self.assertEqual(
                [t["name"] for t in first["tables"]], ["_.Installation", "_.Mirror"]
            )
            audit = first["tables"][0]["columns"][1]
            self.assertEqual(audit["type"], "datetime2(6)")
            self.assertTrue(audit["required"])

    def test_write_check_and_column_drift(self):
        with patch("importlib.import_module", return_value=self.module):
            reference.update(self.root, self.checkout, write=True)
            reference.update(self.root, self.checkout, write=False)
            self.table.key = ("row_insert_datetime",)
            with self.assertRaisesRegex(ValueError, "drift"):
                reference.update(self.root, self.checkout, write=False)

    def test_duplicate_table_and_wrong_checkout_are_refused(self):
        with patch("importlib.import_module", return_value=self.module):
            self.mirror.qualified = self.table.qualified
            with self.assertRaisesRegex(ValueError, "duplicate"):
                reference.build_manifest(self.checkout)
            self.module.__file__ = str(
                self.root / "other/src/weaver/catalogue/tables.py"
            )
            with self.assertRaisesRegex(ValueError, "different checkout"):
                reference.build_manifest(self.checkout)

    def test_reload_meaning_uses_the_current_writer_not_stale_source_prose(self):
        manifest = {
            "tables": [
                {
                    "name": "_.LoadStatistic",
                    "key": ["Load statistic SK"],
                    "columns": [
                        {
                            "name": "Is reload",
                            "type": "bit",
                            "required": False,
                            "notes": "False until reload is available.",
                        }
                    ],
                }
            ]
        }
        text = reference.render(manifest)
        self.assertNotIn("False until reload is available", text)
        self.assertIn("reset for this reload attempt", text)

    def test_duplicate_markers_are_refused(self):
        with patch("importlib.import_module", return_value=self.module):
            (self.root / reference.PAGE).write_text(reference.BEGIN * 2 + reference.END)
            with self.assertRaisesRegex(ValueError, "ordered marker"):
                reference.update(self.root, self.checkout, write=True)


if __name__ == "__main__":
    unittest.main()
