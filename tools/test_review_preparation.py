"""Reader-preparation regressions; no tenant access."""

import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReviewPreparation(unittest.TestCase):
    def test_native_task_supplies_executable_inspection(self):
        text = (ROOT / "docs/semantic-models/native-tmdl.md").read_text()
        for required in (
            'EVALUATE ROW("DeliveryCount", [Delivery Count])',
            'get_definition(format="TMDL")',
            "isHidden is True",
            "isHidden is not True",
            'relationships["Delivery_Depot"]',
            "sha256",
        ):
            self.assertIn(required, text)

    def test_example_downloads_are_local_complete_projects(self):
        links = []
        for page in (ROOT / "docs").rglob("*.md"):
            text = page.read_text()
            self.assertNotRegex(
                text,
                r"github\.com/matthias-wong-dev/weaverstack-docs/(?:tree|blob)/main/examples",
            )
            for target in re.findall(r"\]\(([^)]+\.zip)\)", text):
                archive = (page.parent / target).resolve()
                self.assertTrue(archive.is_file(), str(archive))
                with zipfile.ZipFile(archive) as opened:
                    for name in opened.namelist():
                        self.assertEqual(
                            opened.read(name), (ROOT / name).read_bytes(), name
                        )
                links.append(target)
        self.assertGreaterEqual(len(links), 10)

    def test_rerun_heading_keeps_its_original_anchor(self):
        text = (ROOT / "docs/estate/selective-runs.md").read_text()
        self.assertNotIn("## 8. Choose the right kind of rerun", text)
        self.assertIn(
            "## Choose the right kind of rerun {#8-choose-the-right-kind-of-rerun}",
            text,
        )

    def test_exact_inspector_runs_on_compiler_output_without_network(self):
        import base64
        import contextlib
        import hashlib
        import io
        import json
        import os
        import shlex
        import shutil
        import socket
        import subprocess
        import sys
        import tempfile
        from unittest.mock import patch

        checkout = os.environ.get("WEAVER_CHECKOUT")
        if not checkout:
            self.skipTest("Set WEAVER_CHECKOUT for the production compiler check")
        source = Path(checkout).resolve()
        sys.path[:0] = [
            str(source / "src"),
            str(source / "tests"),
            str(source / "tests/targeted"),
        ]
        import weaver
        from check_docs_refresh_examples import compile_models, item
        from weaver.semantic_models import TmdlDefinition

        self.assertTrue(Path(weaver.__file__).resolve().is_relative_to(source / "src"))
        text = (ROOT / "docs/semantic-models/native-tmdl.md").read_text()
        code = re.search(
            r'```python title="inspect-model.py"\n(.*?)```', text, re.DOTALL
        )[1]
        # Exercise only the local assertions with real compiler output, not API readback.
        assertions = code[code.index("parts = {") :]
        remember = next(
            line for line in text.splitlines() if line.startswith("python -c ")
        )
        rule = re.findall(r"```tmdl\n(.*?)```", text, re.DOTALL)[0]
        previous = Path.cwd()
        with tempfile.TemporaryDirectory(prefix="review-prep-") as tmp:
            trial = Path(tmp) / "project"
            shutil.copytree(ROOT / "examples/parcel-powerbi", trial)
            subprocess.run(
                [sys.executable, *shlex.split(remember)[1:]], cwd=trial, check=True
            )
            (trial / "PowerBI/Parcel/Parcel.tmdl").write_text(rule)
            try:
                os.chdir(trial)
                with patch.object(
                    socket.socket, "connect", side_effect=AssertionError("offline only")
                ):
                    compiled = compile_models(trial)
                    payload = compiled.semantic_models[
                        item("SemanticModel/Parcel")
                    ].parts
                    namespace: dict[str, object] = {
                        "base64": base64,
                        "hashlib": hashlib,
                        "json": json,
                        "Path": Path,
                        "TmdlDefinition": TmdlDefinition,
                    }
                    namespace["definition"] = {
                        "parts": [
                            {
                                "path": path,
                                "payloadType": "InlineBase64",
                                "payload": base64.b64encode(data).decode(),
                            }
                            for path, data in payload.items()
                        ]
                    }
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(assertions, namespace)  # noqa: S102 - Run the repository-owned example.
                        marker = (
                            trial
                            / "PowerBI/Parcel/Parcel.SemanticModel/definition.pbism"
                        )
                        marker.write_bytes(marker.read_bytes() + b"\n")
                        with self.assertRaises(AssertionError):
                            exec(assertions, namespace)  # noqa: S102 - Run the repository-owned example.
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
