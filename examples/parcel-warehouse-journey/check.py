"""Check published Warehouse blocks and assembled checkpoints offline."""

from __future__ import annotations

import argparse
import hashlib
import re
import shlex
import shutil
import socket
import sys
import tempfile
from pathlib import Path


def blocks(page, language):
    return re.findall(
        r"^```" + language + r"[^\n]*\n(.*?)^```",
        page.read_text(),
        re.MULTILINE | re.DOTALL,
    )


def refuse_network(*args, **kwargs):
    raise AssertionError("This check must not contact a service")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    args = parser.parse_args()
    source = args.weaver_checkout.resolve() / "src"
    sys.path.insert(0, str(source))
    import weaver
    import yaml
    from weaver.config import parse_workspace
    from weaver.declaration import parse_item_repository, read_source_document
    from weaver.declaration.model import WeaverItemId
    from weaver.declaration.tsql_program import parse_tsql_program
    from weaver.errors import DiscoveryError
    from weaver.locations import Location
    from weaver_cli.main import build_parser
    from weaver_cli.main import main as cli_main

    assert weaver.__file__ and Path(weaver.__file__).resolve().is_relative_to(source)
    socket.socket.connect = refuse_network
    socket.create_connection = refuse_network
    fixture = Path(__file__).resolve().parent
    root = fixture.parents[1]
    pages = sorted((root / "docs/warehouse").glob("*.md"))
    counts = {
        "commands": 0,
        "configurations": 0,
        "authored_sql_blocks": 0,
        "sql_program_blocks": 0,
        "fixture_block_matches": 0,
        "checkpoints": 0,
    }
    before = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in fixture.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    for page in pages:
        for block in blocks(page, "bash"):
            for line in block.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts["commands"] += 1
        for block in blocks(page, "yaml"):
            raw = yaml.safe_load(block)
            if isinstance(raw, dict) and "workspace" in raw:
                parse_workspace(raw)
                counts["configurations"] += 1
        for block in blocks(page, "sql"):
            parse_tsql_program(block, what=str(page), error=DiscoveryError)
            counts["sql_program_blocks"] += 1
            match = re.search(r"(Table|View|Test|Assumption) ID: (\S+)", block)
            if not match:
                continue
            kind, name = match.groups()
            prefix = {"Test": "tests/", "Assumption": "assumptions/"}.get(kind, "")
            document = read_source_document(
                prefix + name + ".sql", block.encode(), "Warehouse"
            )
            program = parse_tsql_program(
                document.sql_body, what=name, error=DiscoveryError
            )
            expected_queries = (
                2 if kind == "Test" or document.document.is_incremental else 1
            )
            assert len(program.queries) == expected_queries, (page, name)
            if kind == "Table":
                generated = document.create_load(
                    item=WeaverItemId.parse("Warehouse/Operations")
                )
                assert generated is not None
                assert generated.object_type == "stored_procedure"
                assert (
                    f"create or alter procedure [_].[Load {name}]".encode()
                    in generated.payload
                )
            counts["authored_sql_blocks"] += 1
    sync = {
        "first-project.md": (
            fixture,
            [
                "workspace-config.yml",
                "Warehouse/Operations/Parcel.StatusEvent.sql",
                "Warehouse/Operations/Parcel.CurrentStatus.sql",
            ],
        ),
        "tests.md": (
            fixture,
            [
                "Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql",
                "Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql",
                "failure/Parcel.CurrentStatusMatches.sql",
            ],
        ),
        "incremental.md": (
            root / "examples/parcel-incremental-warehouse",
            [
                "workspace-config.yml",
                "Warehouse/Operations/shortcuts.yml",
                "Warehouse/Operations/Parcel.CurrentStatus.sql",
                "source/ParcelSource/01-setup.sql",
                "source/ParcelSource/02-seed.sql",
                "source/ParcelSource/03-change.sql",
            ],
        ),
    }
    for name, (snapshot, files) in sync.items():
        for relative in files:
            file = snapshot / relative
            language = "yaml" if file.suffix == ".yml" else "sql"
            assert file.read_text() in blocks(
                root / "docs/warehouse" / name, language
            ), relative
            counts["fixture_block_matches"] += 1
    for name in ("Parcel.StatusEvent.sql", "Parcel.CurrentStatus.sql"):
        assert (fixture / "Warehouse/Operations" / name).read_bytes() == (
            root / "examples/parcel-warehouse/Warehouse/Operations" / name
        ).read_bytes()
    with tempfile.TemporaryDirectory(prefix="warehouse-journey-") as directory:
        trial = Path(directory)
        shutil.copytree(fixture / "Warehouse", trial / "Warehouse")
        shutil.rmtree(trial / "Warehouse/Operations/tests")
        shutil.rmtree(trial / "Warehouse/Operations/assumptions")
        for checkpoint in ("first", "passing", "finding", "restored"):
            if checkpoint == "passing":
                for folder in ("tests", "assumptions"):
                    shutil.copytree(
                        fixture / "Warehouse/Operations" / folder,
                        trial / "Warehouse/Operations" / folder,
                    )
            if checkpoint in ("finding", "restored"):
                origin = (
                    fixture / "failure/Parcel.CurrentStatusMatches.sql"
                    if checkpoint == "finding"
                    else fixture
                    / "Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql"
                )
                shutil.copyfile(
                    origin,
                    trial
                    / "Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql",
                )
            assert cli_main(["check", str(trial), "--non-interactive"]) == 0
            repository = parse_item_repository(Location(str(trial)))
            edges = {
                (edge.consumer.object_id.qualified, edge.producer.object_id.qualified)
                for edge in repository.dependency_edges
            }
            expected = {("Parcel.CurrentStatus", "Parcel.StatusEvent")}
            if checkpoint != "first":
                expected |= {
                    ("Parcel.CurrentStatusMatches", "Parcel.CurrentStatus"),
                    ("Parcel.StatusIsKnown", "Parcel.StatusEvent"),
                }
            assert edges == expected, (checkpoint, edges)
            print(checkpoint, "dependencies:", sorted(edges))
            counts["checkpoints"] += 1
    incremental = root / "examples/parcel-incremental-warehouse"
    assert cli_main(["check", str(incremental), "--non-interactive"]) == 0
    repository = parse_item_repository(Location(str(incremental)))
    assert not repository.dependency_edges
    counts["checkpoints"] += 1
    assert before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in before}
    print("Validated against", weaver.__file__)
    print(counts)
    print("No service calls or native SQL execution; fixture hashes unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
