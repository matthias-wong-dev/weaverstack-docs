"""Offline Lakehouse page/parser/checkpoint checks, never Fabric execution."""

import argparse
import ast
import contextlib
import hashlib
import io
import json
import re
import shlex
import socket
import sys
import tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--docs", type=Path, required=True)
p.add_argument("--product", type=Path, required=True)
a = p.parse_args()
a.docs = a.docs.resolve()
a.product = a.product.resolve()
sys.path.insert(0, str(a.product / "src"))
import weaver

assert Path(weaver.__file__).resolve().is_relative_to(a.product / "src")
print("weaver.__file__:", weaver.__file__)
import yaml
from named_journey_support import OfflineInitialiser, sources
from weaver.config import parse_workspace
from weaver.declaration import parse_item_repository
from weaver.declaration.load import generate_load
from weaver.declaration.metadata import SPARK_SQL
from weaver.declaration.validation import generate_validation
from weaver.locations import Location
from weaver.spark import FabricSparkTarget
from weaver_cli.main import build_parser
from weaver_cli.main import main as cli_main


def blocked(*args, **kwargs):
    raise AssertionError("Network forbidden in local documentation checks")


socket.socket.connect = blocked
socket.create_connection = blocked


def blocks(page, language):
    return re.findall(
        r"^```" + language + r"[^\n]*\n(.*?)^```",
        page.read_text(),
        re.MULTILINE | re.DOTALL,
    )


counts = {
    "pages": 0,
    "commands": 0,
    "python_blocks": 0,
    "workspace_configs": 0,
    "synced_blocks": 0,
    "checkpoints": 0,
    "generated_modules": 0,
}
pages = sorted((a.docs / "docs/lakehouse").glob("*.md"))
pages = [page for page in pages if page.stem != "index"]
assert len(pages) == 6
for page in pages:
    counts["pages"] += 1
    for block in blocks(page, "bash"):
        for line in block.replace("\\\n", " ").splitlines():
            if line.startswith("weaver "):
                build_parser().parse_args(shlex.split(line)[1:])
                counts["commands"] += 1
    for block in blocks(page, "python"):
        ast.parse(block)
        counts["python_blocks"] += 1
    for block in blocks(page, "yaml"):
        raw = yaml.safe_load(block)
        if isinstance(raw, dict) and "workspace" in raw:
            parse_workspace(raw)
            counts["workspace_configs"] += 1

sync = [
    (
        "python",
        "python",
        "parcel-lakehouse",
        "Lakehouse/Landing/Files/Parcel__Events.py",
    ),
    (
        "python",
        "python",
        "parcel-lakehouse",
        "Lakehouse/Landing/Tables/Parcel__Event.py",
    ),
    (
        "spark-sql",
        "sql",
        "parcel-lakehouse",
        "Lakehouse/Landing/Tables/Parcel.CurrentStatus.sql",
    ),
    (
        "tests",
        "sql",
        "parcel-lakehouse",
        "Lakehouse/Landing/tests/Parcel.CurrentStatusMatches.sql",
    ),
    (
        "tests",
        "sql",
        "parcel-lakehouse",
        "Lakehouse/Landing/assumptions/Parcel.EventStatusIsKnown.sql",
    ),
    ("incremental", "csv", "parcel-incremental", "source/parcel-status/P-1001.csv"),
    ("incremental", "csv", "parcel-incremental", "source/parcel-status/P-1002.csv"),
]
for page, language, fixture, relative in sync:
    content = (a.docs / "examples" / fixture / relative).read_text().rstrip() + "\n"
    assert content in blocks(a.docs / f"docs/lakehouse/{page}.md", language), (
        page,
        relative,
    )
    counts["synced_blocks"] += 1

files = [
    "Files/Parcel__Events.py",
    "Tables/Parcel__Event.py",
    "Tables/Parcel.CurrentStatus.sql",
    "tests/Parcel.CurrentStatusMatches.sql",
    "assumptions/Parcel.EventStatusIsKnown.sql",
]
fixture = a.docs / "examples/parcel-lakehouse"
original = {
    str(path): hashlib.sha256(path.read_bytes()).hexdigest()
    for name in ("parcel-lakehouse", "parcel-incremental")
    for path in (a.docs / "examples" / name).rglob("*")
    if path.is_file()
}
with (
    tempfile.TemporaryDirectory(prefix="lakehouse-checkpoints-") as temporary,
    OfflineInitialiser() as initialise,
):
    temp = Path(temporary)
    checkpoint = temp / "parcel"
    initialise(checkpoint, lakehouse="Landing")
    initial_sources = sources(checkpoint)
    for name in ("python", "spark-sql", "validation"):
        n = len(files)
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            result = cli_main(["check", str(checkpoint), "--json", "--non-interactive"])
        assert result == 0, (name, capture.getvalue())
        assert json.loads(capture.getvalue())["status"] == "succeeded"
        repository = parse_item_repository(Location(str(checkpoint)))
        expected_paths = {"Lakehouse/Landing/" + relative for relative in files[:n]}
        documents = [
            document
            for document in repository.source_documents.values()
            if document.relative_path in expected_paths
        ]
        assert len(documents) == n, (
            n,
            [document.relative_path for document in documents],
        )
        print("checkpoint:", name, "Project valid;", n, "authored documents")
        if name == "validation":
            target = FabricSparkTarget(
                workspace="Parcel Development", lakehouse="Landing"
            )
            for document in documents:
                if document.language == SPARK_SQL:
                    generated = (
                        generate_validation(document, destination=target)
                        if document.is_validation
                        else generate_load(document, destination=target)
                    )
                    ast.parse(generated.payload.decode())
                    counts["generated_modules"] += 1
            edges = {
                (edge.upstream, edge.downstream)
                for edge in repository.dependency_graph.edges
            }
            expected_edges = {
                (
                    "Lakehouse/Landing/Files/Parcel.Events",
                    "Lakehouse/Landing/Tables/Parcel.Event",
                ),
                (
                    "Lakehouse/Landing/Tables/Parcel.Event",
                    "Lakehouse/Landing/Tables/Parcel.CurrentStatus",
                ),
                (
                    "Lakehouse/Landing/Tables/Parcel.CurrentStatus",
                    "Lakehouse/Landing/Parcel.CurrentStatusMatches",
                ),
                (
                    "Lakehouse/Landing/Tables/Parcel.Event",
                    "Lakehouse/Landing/Parcel.EventStatusIsKnown",
                ),
            }
            assert expected_edges <= edges, edges
            print("authored dependency edges:", sorted(expected_edges))
        counts["checkpoints"] += 1
    # Add the complete changing-source task alongside the generated pipeline.
    snippets = blocks(a.docs / "docs/lakehouse/incremental.md", "python")
    for filename, needle in (
        ("shortcuts.py", "from weaver import Shortcut"),
        ("Files/Parcel__StatusFiles.py", "class Parcel__StatusFiles"),
        ("Tables/Parcel__LiveStatus.py", "class Parcel__LiveStatus"),
    ):
        target = checkpoint / "Lakehouse/Landing" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(next(block for block in snippets if needle in block))
    assert cli_main(["check", str(checkpoint), "--json", "--non-interactive"]) == 0
    repository = parse_item_repository(Location(str(checkpoint)))
    assert (
        "Lakehouse/Landing/Files/Parcel.StatusFiles",
        "Lakehouse/Landing/Tables/Parcel.LiveStatus",
    ) in {(e.upstream, e.downstream) for e in repository.dependency_graph.edges}
    assert all(
        sources(checkpoint).get(path) == content
        for path, content in initial_sources.items()
    )
    counts["checkpoints"] += 1
    before_extension = sources(checkpoint)
    initialise(checkpoint, warehouse="Operations")
    assert all(
        sources(checkpoint).get(path) == content
        for path, content in before_extension.items()
    )
    assert (checkpoint / "Warehouse/Operations/shortcuts.yml").read_text() in blocks(
        a.docs / "docs/lakehouse/shortcuts.md", "yaml"
    )
    assert cli_main(["check", str(checkpoint), "--json", "--non-interactive"]) == 0
    counts["checkpoints"] += 1
for name in ("parcel-lakehouse", "parcel-incremental"):
    assert (
        cli_main(
            ["check", str(a.docs / "examples" / name), "--json", "--non-interactive"]
        )
        == 0
    )
    counts["checkpoints"] += 1
assert original == {
    str(path): hashlib.sha256(path.read_bytes()).hexdigest()
    for name in ("parcel-lakehouse", "parcel-incremental")
    for path in (a.docs / "examples" / name).rglob("*")
    if path.is_file()
}
route_map = (a.docs / "acceptance/docs-item-first-2026-10/route-map.md").read_text()
planned = set(re.findall(r"`(docs/[^`]+\.md)` →", route_map))
missing = set()
for page in pages:
    for target in re.findall(r"\]\(([^)]+)\)", page.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        destination = (page.parent / target.split("#")[0]).resolve()
        if not destination.exists():
            relative = str(destination.relative_to(a.docs))
            assert relative in planned, (page, target)
            missing.add(relative)
print("planned sibling destinations pending integration:", sorted(missing))
assert counts["generated_modules"] == 3, counts
print(json.dumps(counts, sort_keys=True))
print("PASS: offline authored shape and compilation only; no service results asserted")
