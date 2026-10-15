"""Beginner journeys use installed examples; acceptance checks stay here."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReviewPreparation(unittest.TestCase):
    def test_native_task_is_an_ordinary_modelling_exercise(self):
        text = (ROOT / "docs/semantic-models/native-tmdl.md").read_text()
        for required in (
            "--example Parcel",
            "--semantic-model Parcel",
            'ROW("DeliveryCount", [Delivery Count])',
            "Weaver.AutoHideForeignKeys",
            "field list",
        ):
            self.assertIn(required, text)
        for removed in (
            "sha256",
            "SHA-256",
            "query-model.py",
            "inspect-model.py",
            "get_definition(",
            "native-source.",
        ):
            self.assertNotIn(removed, text)

    def test_first_use_routes_select_installed_named_examples(self):
        for relative, selection in (
            ("lakehouse/python.md", "--lakehouse Landing"),
            ("warehouse/first-project.md", "--warehouse Operations"),
            ("semantic-models/native-tmdl.md", "--semantic-model Parcel"),
        ):
            text = (ROOT / "docs" / relative).read_text()
            self.assertIn("weaver initialise", text)
            self.assertIn("--example Parcel", text)
            self.assertIn(selection, text)
        for page in (ROOT / "docs").rglob("*.md"):
            self.assertNotIn("--no-example", page.read_text(), str(page))

    def test_rerun_heading_keeps_its_original_anchor(self):
        text = (ROOT / "docs/estate/selective-runs.md").read_text()
        self.assertNotIn("## 8. Choose the right kind of rerun", text)
        self.assertIn(
            "## Choose the right kind of rerun {#8-choose-the-right-kind-of-rerun}",
            text,
        )

    def test_rule_preserves_native_model_and_import_partitions(self):
        checkout = os.environ.get("WEAVER_CHECKOUT")
        if not checkout:
            self.skipTest("Set WEAVER_CHECKOUT for the production compiler check")
        sys.path.insert(0, str(Path(checkout).resolve() / "src"))
        from weaver.initialise import _generated_files, _write
        from weaver.onboarding.project import ProjectRequest
        from weaver.declaration.repository import parse_item_repository
        from weaver.locations import Location
        from weaver.semantic_models import TmdlDefinition
        from weaver.semantic_models.binding import bind_semantic_sources
        from weaver.declaration.model import WeaverItemId

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _write(
                root,
                _generated_files(
                    ProjectRequest(
                        workspace="Example",
                        catalogue="Catalogue",
                        environment="Weaver",
                        semantic_model="Parcel",
                        example="Parcel",
                    )
                ),
            )
            native = root / "PowerBI/Parcel/Parcel.SemanticModel"
            before = {
                p.relative_to(native): p.read_bytes()
                for p in native.rglob("*")
                if p.is_file()
            }
            (root / "PowerBI/Parcel/Parcel.tmdl").write_text(
                "model Model\n\tannotation 'Weaver.AutoHideForeignKeys' = true\n"
            )
            repository = parse_item_repository(Location(str(root)))
            compiled = bind_semantic_sources(repository, {}, repository.semantic_models)
            model = TmdlDefinition(
                compiled.semantic_models[
                    WeaverItemId.parse("SemanticModel/Parcel")
                ].parts
            ).model
            self.assertIs(model.tables["Delivery"].columns["DepotId"].isHidden, True)
            self.assertIsNot(model.tables["Depot"].columns["DepotId"].isHidden, True)
            self.assertEqual(
                model.relationships["Delivery_Depot"].fromColumn, "Delivery.DepotId"
            )
            for name in ("Delivery", "Depot"):
                self.assertEqual(model.tables[name].partitions[name].mode, "import")
                self.assertIn("#table", model.tables[name].partitions[name].source)
            self.assertEqual(
                before,
                {
                    p.relative_to(native): p.read_bytes()
                    for p in native.rglob("*")
                    if p.is_file()
                },
            )


if __name__ == "__main__":
    unittest.main()


def test_generated_markers_allow_blank_lines():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "sync_examples", ROOT / "tools/sync_initialise_examples.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text = (
        "<!-- initialise:source.sql -->\n\n```sql\nselect 1;\n```\n<!-- /initialise -->"
    )
    assert len(module.BLOCK.findall(text)) == 1
