#!/usr/bin/env python3
"""Check rendered task commands and assembled local projects, never services."""

from __future__ import annotations

import argparse
import ast
import inspect
import re
import shlex
import shutil
import socket
import sys
import tempfile
from pathlib import Path

from check_docs_refresh_examples import compile_models, hashes, model, refuse_network


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
    assert (
        re.search(
            r"Inspect Delivery's metadata row.*?mapping failed\.",
            readback_pages[0].read_text(),
            re.DOTALL,
        ).group()
        == re.search(
            r"Inspect Delivery's metadata row.*?mapping failed\.",
            readback_pages[1].read_text(),
            re.DOTALL,
        ).group()
    )
    pages = sorted((docs / "semantic-models").glob("*.md"))
    pages += sorted((docs / "reports").glob("*.md"))
    pages += [
        docs / "estate" / f"{name}.md"
        for name in ("selective-runs", "concurrency", "performance", "environments")
    ]
    assert len(pages) == 15
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
    sync = [
        (
            "semantic-models/native-tmdl.md",
            "yaml",
            "parcel-powerbi",
            "workspace-dev.yml",
        ),
        (
            "reports/environments.md",
            "yaml",
            "parcel-powerbi",
            "workspace-dev.yml",
        ),
        (
            "reports/environments.md",
            "yaml",
            "parcel-powerbi",
            "workspace-prod.yml",
        ),
        (
            "semantic-models/validation.md",
            "dax",
            "parcel-powerbi-validation",
            "PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax",
        ),
        (
            "semantic-models/validation.md",
            "tmdl",
            "parcel-powerbi-validation",
            "failure/Parcel.tmdl",
        ),
        (
            "semantic-models/managed-sources.md",
            "yaml",
            "parcel-powerbi-fabric",
            "workspace-dev.yml",
        ),
        (
            "semantic-models/managed-sources.md",
            "tmdl",
            "parcel-powerbi-fabric",
            "PowerBI/Parcel/Parcel.tmdl",
        ),
        (
            "semantic-models/shared-policy.md",
            "tmdl",
            "parcel-powerbi-standards",
            "PowerBI/policy.tmdl",
        ),
        (
            "semantic-models/custom-annotations.md",
            "python",
            "parcel-powerbi-standards",
            "PowerBI/annotations/Parcel__DisplayFolder.py",
        ),
        (
            "semantic-models/custom-annotations.md",
            "tmdl",
            "parcel-powerbi-standards",
            "PowerBI/Parcel/Parcel.tmdl",
        ),
        (
            "semantic-models/composition.md",
            "tmdl",
            "parcel-powerbi-variants",
            "PowerBI/Parcel/ParcelOperations.tmdl",
        ),
        (
            "semantic-models/composition.md",
            "tmdl",
            "parcel-powerbi-variants",
            "PowerBI/Parcel/ParcelExecutive.tmdl",
        ),
    ]
    for page, language, fixture, name in sync:
        expected = (root / "examples" / fixture / name).read_text().rstrip() + "\n"
        assert expected in blocks(docs / page, language), (page, name)
    before = hashes(root / "examples")
    with tempfile.TemporaryDirectory(prefix="journey-examples-") as directory:
        temp = Path(directory)
        for name, guide in (("rule", "modelling-rule"), ("policy", "shared-policy")):
            trial = temp / name
            shutil.copytree(root / "examples/parcel-powerbi", trial)
            guide_path = docs / (
                "semantic-models/native-tmdl.md"
                if name == "rule"
                else "semantic-models/shared-policy.md"
            )
            snippets = blocks(guide_path, "tmdl")
            if name == "rule":
                snippets = [
                    text for text in snippets if "Weaver.AutoHideForeignKeys" in text
                ]
                assert len(snippets) == 1
            if name == "policy":
                (trial / "PowerBI/policy.tmdl").write_text(snippets[0])
            (trial / "PowerBI/Parcel/Parcel.tmdl").write_text(snippets[-1])
            assert cli_main(["check", str(trial), "--json", "--non-interactive"]) == 0
            effective = model(compile_models(trial))
            assert effective.tables["Delivery"].columns["DepotId"].isHidden is True
            assert effective.tables["Depot"].columns["DepotId"].isHidden is None
            if name == "policy":
                assert (
                    effective.tables["Delivery"].measures["Delivery Count"].formatString
                    == '0 "deliveries"'
                )
                assert (
                    effective.tables["Delivery"].measures["InternalCost"].formatString
                    == "#,##0.00"
                )
                group = effective.tables["Display"].calculationGroup
                assert group.precedence == "10"
                assert (
                    group.calculationItems["Current"].expression == "SELECTEDMEASURE()"
                )
        guide = docs / "semantic-models/from-tmdl.md"
        snippets = blocks(guide, "tmdl")
        for number, text in enumerate(snippets):
            trial = temp / f"tmdl-{number}"
            (trial / "PowerBI/Parcel").mkdir(parents=True)
            (trial / "PowerBI/Parcel/ParcelSummary.tmdl").write_text(text)
            if number:
                shutil.copytree(
                    root / "examples/parcel-powerbi-fabric/Warehouse",
                    trial / "Warehouse",
                )
            assert cli_main(["check", str(trial), "--json", "--non-interactive"]) == 0
            if not number:
                native = model(compile_models(trial), "ParcelSummary")
                assert native.tables["Delivery"].partitions["Delivery"].mode == "import"
                assert (
                    native.tables["Delivery"].measures["Delivery Count"].expression
                    == "SUM(Delivery[Delivered])"
                )
    assert hashes(root / "examples") == before
    print(
        f"PASS: {counts}; {len(sync)} byte-identical fixture blocks; four exact rendered projects Check; local rule/policy/standalone compilation; no network or service execution"
    )


if __name__ == "__main__":
    main()
