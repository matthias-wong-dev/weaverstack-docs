#!/usr/bin/env python3
"""Check rendered task commands and assembled local projects, never services."""

from __future__ import annotations

import argparse
import ast
import inspect
import json
import re
import shlex
import socket
import sys
import tempfile
from pathlib import Path

from check_docs_refresh_examples import refuse_network
from named_journey_support import OfflineInitialiser, sources


def blocks(path, language):
    return re.findall(
        r"^```" + language + r"[^\n]*\n(.*?)^```",
        path.read_text(),
        re.MULTILINE | re.DOTALL,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    args = parser.parse_args()
    checkout = args.weaver_checkout.resolve()
    sys.path.insert(0, str(checkout / "src"))
    import weaver
    import yaml
    from weaver.config import parse_workspace
    from weaver_cli.main import build_parser
    from weaver_cli.main import main as cli_main

    assert Path(weaver.__file__).resolve().is_relative_to(checkout / "src")
    socket.socket.connect = refuse_network
    socket.create_connection = refuse_network
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    from weaver.catalogue.tables import CATALOGUE_TABLES

    catalogue_names = {table.qualified for table in CATALOGUE_TABLES}
    readback_pages = [
        docs / "semantic-models/validation.md",
        root / "examples/parcel-powerbi-fabric/README.md",
    ]
    required_names = {
        "_.SemanticModelTable",
        "_.Dependency",
        "_.SemanticModelTest",
        "_.TestStatus",
    }
    for readback_page in readback_pages:
        text = readback_page.read_text()
        assert "SemanticModelSource" not in text, readback_page
        named = set(re.findall(r"`(_\.[A-Za-z]+)`", text))
        assert required_names <= named <= catalogue_names, (readback_page, named)
    pages = sorted((docs / "semantic-models").glob("*.md"))
    pages += sorted((docs / "reports").glob("*.md"))
    pages += [
        docs / "estate" / f"{name}.md"
        for name in ("selective-runs", "concurrency", "performance", "environments")
    ]
    pages += sorted((docs / "warehouse").glob("*.md"))
    assert len(pages) == 20
    counts = {"pages": len(pages), "commands": 0, "configs": 0, "python_calls": 0}
    for page in pages:
        for text in blocks(page, "bash"):
            for line in text.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts["commands"] += 1
        for text in blocks(page, "yaml"):
            raw = yaml.safe_load(text)
            if isinstance(raw, dict) and "workspace" in raw:
                parse_workspace(raw)
                counts["configs"] += 1
        for text in blocks(page, "python"):
            tree = ast.parse(text)
            for call in ast.walk(tree):
                if (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id == "weaver"
                ):
                    fn = getattr(weaver, call.func.attr)
                    signature = inspect.signature(fn)
                    for keyword in call.keywords:
                        assert keyword.arg in signature.parameters, (page, keyword.arg)
                    counts["python_calls"] += 1
    # Native generation and modelling checkpoints belong to the dedicated
    # generator/semantic checks; this gate also checks each Report mapping.
    with (
        tempfile.TemporaryDirectory(prefix="report-journey-") as directory,
        OfflineInitialiser() as initialise,
    ):
        trial = Path(directory)
        initialise(trial, semantic_model="Parcel")
        original = sources(trial)
        report = json.loads(
            (trial / "PowerBI/Parcel/Parcel.Report/definition.pbir").read_text()
        )
        assert report["datasetReference"]["byPath"]["path"] == "../Parcel.SemanticModel"
        configs = blocks(docs / "reports/environments.md", "yaml")
        assert len(configs) == 2
        for config in configs:
            parse_workspace(yaml.safe_load(config))
            (trial / "workspace-config.yml").write_text(config)
            assert cli_main(["check", str(trial), "--json", "--non-interactive"]) == 0
            assert sources(trial) == original
    with (
        tempfile.TemporaryDirectory(prefix="warehouse-journey-") as directory,
        OfflineInitialiser() as initialise,
    ):
        trial = Path(directory)
        initialise(trial, warehouse="Operations")
        original = sources(trial)
        page = docs / "warehouse/incremental.md"
        (trial / "Warehouse/Operations/shortcuts.yml").write_text(
            blocks(page, "yaml")[0]
        )
        (trial / "Warehouse/Operations/Parcel.LiveStatus.sql").write_text(
            next(
                text
                for text in blocks(page, "sql")
                if "Table ID: Parcel.LiveStatus" in text
            )
        )
        assert cli_main(["check", str(trial), "--json", "--non-interactive"]) == 0
        assert all(sources(trial).get(p) == content for p, content in original.items())
        assert "from [Parcel].[LiveStatus]" in page.read_text()
        before_extension = sources(trial)
        initialise(trial, semantic_model="Parcel")
        assert all(
            sources(trial).get(p) == content for p, content in before_extension.items()
        )
        assert cli_main(["check", str(trial), "--json", "--non-interactive"]) == 0
    print(
        f"PASS: {counts}; generated native Report link and both environment mappings; Warehouse incremental addition and native extension preserve working sources; no service execution"
    )


if __name__ == "__main__":
    main()
