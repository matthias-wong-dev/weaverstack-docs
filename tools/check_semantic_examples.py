"""Compile the exact semantic-model journey checkpoints offline."""


def main():
    """Check the seven new owning pages with pinned production functions, offline."""
    import ast
    import json
    import os
    import re
    import shlex
    import shutil
    import socket
    import subprocess
    import sys
    import tempfile
    from pathlib import Path

    ROOT = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else Path(__file__).resolve().parents[1]
    )
    SOURCE = Path(os.environ["WEAVER_CHECKOUT"]).resolve()
    sys.path[:0] = [
        str(SOURCE / "src"),
        str(SOURCE / "tests"),
        str(SOURCE / "tests/targeted"),
        str(ROOT / "tools"),
    ]
    import weaver
    import yaml
    from check_docs_refresh_examples import (
        compile_models,
        hashes,
        model,
        refuse_network,
    )
    from weaver.catalogue.tables import CATALOGUE_TABLES
    from weaver.config import parse_workspace
    from weaver_cli.main import build_parser, main

    assert Path(weaver.__file__).resolve().is_relative_to(SOURCE / "src")
    print("Imported:", weaver.__file__)
    print("PYTHONPATH:", os.environ.get("PYTHONPATH"))
    socket.socket.connect = refuse_network
    socket.create_connection = refuse_network
    DOC = ROOT / "docs/semantic-models"
    PAGES = [
        "native-tmdl",
        "managed-sources",
        "validation",
        "shared-policy",
        "custom-annotations",
        "composition",
        "from-tmdl",
    ]

    def blocks(page, language):
        return re.findall(
            r"^```" + language + r"[^\n]*\n(.*?)^```",
            (DOC / (page + ".md")).read_text(),
            re.MULTILINE | re.DOTALL,
        )

    counts = {"pages": len(PAGES), "commands": 0, "configs": 0, "python_blocks": 0}
    for page in PAGES:
        for block in blocks(page, "bash"):
            for line in block.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts["commands"] += 1
        for block in blocks(page, "yaml"):
            parse_workspace(yaml.safe_load(block))
            counts["configs"] += 1
        for block in blocks(page, "python"):
            ast.parse(block)
            counts["python_blocks"] += 1
    sync = [
        ("native-tmdl", "yaml", "parcel-powerbi", "workspace-dev.yml"),
        (
            "native-tmdl",
            "tmdl",
            "parcel-powerbi",
            "PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl",
        ),
        ("managed-sources", "yaml", "parcel-powerbi-fabric", "workspace-dev.yml"),
        (
            "managed-sources",
            "tmdl",
            "parcel-powerbi-fabric",
            "PowerBI/Parcel/Parcel.tmdl",
        ),
        (
            "managed-sources",
            "tmdl",
            "parcel-powerbi-fabric",
            "PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl",
        ),
        (
            "managed-sources",
            "tmdl",
            "parcel-powerbi-fabric",
            "PowerBI/Parcel/Parcel.SemanticModel/definition/expressions.tmdl",
        ),
        (
            "validation",
            "dax",
            "parcel-powerbi-validation",
            "PowerBI/Parcel/assumptions/Parcel/Parcel.PositiveDeliveryCount.dax",
        ),
        ("validation", "tmdl", "parcel-powerbi-validation", "failure/Parcel.tmdl"),
        (
            "validation",
            "dax",
            "parcel-powerbi-fabric",
            "PowerBI/Parcel/tests/Parcel/Parcel.DeliveryReconciles.dax",
        ),
        ("validation", "tmdl", "parcel-powerbi-fabric", "failure/Parcel.tmdl"),
        ("shared-policy", "tmdl", "parcel-powerbi-standards", "PowerBI/policy.tmdl"),
        (
            "custom-annotations",
            "python",
            "parcel-powerbi-standards",
            "PowerBI/annotations/Parcel__DisplayFolder.py",
        ),
        (
            "custom-annotations",
            "tmdl",
            "parcel-powerbi-standards",
            "PowerBI/Parcel/Parcel.tmdl",
        ),
        (
            "custom-annotations",
            "tmdl",
            "parcel-powerbi-standards",
            "failure/Parcel.tmdl",
        ),
        (
            "composition",
            "tmdl",
            "parcel-powerbi-variants",
            "PowerBI/Parcel/ParcelOperations.tmdl",
        ),
        (
            "composition",
            "tmdl",
            "parcel-powerbi-variants",
            "PowerBI/Parcel/ParcelExecutive.tmdl",
        ),
    ]
    for page, lang, fixture, path in sync:
        assert (ROOT / "examples" / fixture / path).read_text() in blocks(page, lang), (
            page,
            path,
        )
    readback = re.search(
        r"Inspect Delivery's metadata row.*?mapping failed\.",
        (DOC / "validation.md").read_text(),
        re.DOTALL,
    ).group()
    assert readback in (ROOT / "examples/parcel-powerbi-fabric/README.md").read_text()
    names = set(re.findall(r"`(_\.[A-Za-z]+)`", (DOC / "validation.md").read_text()))
    assert (
        {"_.SemanticModelTable", "_.Dependency", "_.SemanticModelTest", "_.TestStatus"}
        <= names
        <= {t.qualified for t in CATALOGUE_TABLES}
    )
    assert "SemanticModelSource" not in (DOC / "validation.md").read_text()
    before = hashes(ROOT / "examples")
    checks = []

    def check(trial, name):
        assert main(["check", str(trial), "--json", "--non-interactive"]) == 0
        checks.append(name)

    def assert_native(effective, original):
        assert (
            effective.relationships["Delivery_Depot"].fromColumn == "Delivery.DepotId"
        )
        for table in ("Delivery", "Depot"):
            assert (
                effective.tables[table].partitions[table].source
                == original.tables[table].partitions[table].source
            )
        assert effective.tables["Delivery"].columns["DepotId"].isHidden is True
        assert effective.tables["Depot"].columns["DepotId"].isHidden is None

    with tempfile.TemporaryDirectory(
        prefix="semantic-model-owning-pages-"
    ) as directory:
        temp = Path(directory)
        trial = temp / "continuous"
        shutil.copytree(ROOT / "examples/parcel-powerbi", trial)
        original = model(compile_models(trial))
        overlay = trial / "PowerBI/Parcel/Parcel.tmdl"
        native_rule = next(
            block
            for block in blocks("native-tmdl", "tmdl")
            if "annotation 'Weaver.AutoHideForeignKeys' = true" in block
        )
        overlay.write_text(native_rule)
        check(trial, "native rule")
        assert_native(model(compile_models(trial)), original)
        (trial / "PowerBI/policy.tmdl").write_text(blocks("shared-policy", "tmdl")[0])
        overlay.write_text(blocks("shared-policy", "tmdl")[-1])
        check(trial, "shared policy")
        policy = model(compile_models(trial))
        assert_native(policy, original)
        assert (
            policy.tables["Delivery"].measures["Delivery Count"].formatString
            == '0 "deliveries"'
        )
        assert (
            policy.tables["Delivery"].measures["InternalCost"].formatString
            == "#,##0.00"
        )
        assert (
            policy.tables["Display"]
            .calculationGroup.calculationItems["Current"]
            .expression
            == "SELECTEDMEASURE()"
        )
        # Move the rule to shared policy exactly as the new page directs.
        policy_text = blocks("shared-policy", "tmdl")[0]
        header = blocks("shared-policy", "tmdl")[1].rstrip()
        (trial / "PowerBI/policy.tmdl").write_text(
            header + policy_text[policy_text.index("\n\ntable Delivery") :]
        )
        overlay.write_text(
            blocks("shared-policy", "tmdl")[-1].replace(
                "    annotation 'Weaver.AutoHideForeignKeys' = true\n", ""
            )
        )
        check(trial, "foreign-key rule moved to shared policy")
        assert_native(model(compile_models(trial)), original)
        handler = trial / "PowerBI/annotations/Parcel__DisplayFolder.py"
        handler.parent.mkdir()
        handler.write_text(blocks("custom-annotations", "python")[0])
        overlay.write_text(blocks("custom-annotations", "tmdl")[0])
        check(trial, "custom annotation")
        custom = model(compile_models(trial))
        assert_native(custom, original)
        assert (
            custom.tables["Delivery"].measures["Delivery Count"].displayFolder
            == "Parcel metrics"
        )
        saved = overlay.read_bytes()
        overlay.write_text(
            re.sub(
                r"^([ \t]*measure 'Delivery Count')(?: =.*)?$",
                r"\1 = -1",
                overlay.read_text(),
                count=1,
                flags=re.MULTILINE,
            )
        )
        check(trial, "Assumption failure edits measure in prior custom/rule overlay")
        failed = model(compile_models(trial))
        assert_native(failed, original)
        assert failed.tables["Delivery"].measures["Delivery Count"].expression == "-1"
        overlay.write_bytes(saved)
        check(trial, "prior overlay restored")
        restored = model(compile_models(trial))
        assert_native(restored, original)
        assert (
            restored.tables["Delivery"].measures["Delivery Count"].expression
            == "SUM(Delivery[Delivered])"
        )
        assert (
            restored.tables["Delivery"].measures["Delivery Count"].displayFolder
            == "Parcel metrics"
        )
        # The actual native-to-validation entry has only the model-level rule.
        for start in ("native-rule", "no-overlay"):
            direct = temp / start
            shutil.copytree(ROOT / "examples/parcel-powerbi-validation", direct)
            path = direct / "PowerBI/Parcel/Parcel.tmdl"
            prior = native_rule.encode() if start == "native-rule" else None
            if prior is not None:
                path.write_bytes(prior)
            path.write_text(
                (prior.decode() if prior else "")
                + "\n"
                + blocks("validation", "tmdl")[0]
            )
            check(direct, start + " failure")
            effective = model(compile_models(direct))
            assert (
                effective.tables["Delivery"].measures["Delivery Count"].expression
                == "-1"
            )
            if prior is not None:
                assert effective.tables["Delivery"].columns["DepotId"].isHidden is True
                path.write_bytes(prior)
            else:
                path.unlink()
            check(direct, start + " correction")
            effective = model(compile_models(direct))
            assert (
                effective.tables["Delivery"].measures["Delivery Count"].expression
                == "SUM(Delivery[Delivered])"
            )
            assert (
                path.read_bytes() == prior if prior is not None else not path.exists()
            )
            # Exercise the page's exact backup/restoration shell branches in one shell.
            backup = next(
                b for b in blocks("validation", "bash") if "had_overlay=false" in b
            )
            restore = next(
                b for b in blocks("validation", "bash") if 'test "$had_overlay"' in b
            )
            restore = "\n".join(
                line for line in restore.splitlines() if not line.startswith("weaver ")
            )
            candidate = direct / "candidate.tmdl"
            candidate.write_text(
                (prior.decode() if prior else "")
                + "\n"
                + blocks("validation", "tmdl")[0]
            )
            subprocess.run(
                [
                    "bash",
                    "-c",
                    backup
                    + "\ncp candidate.tmdl PowerBI/Parcel/Parcel.tmdl\n"
                    + restore,
                ],
                cwd=direct,
                check=True,
            )
            assert (
                path.read_bytes() == prior if prior is not None else not path.exists()
            )
            assert not (direct / "Parcel.tmdl.saved").exists()
        for i, text in enumerate(blocks("from-tmdl", "tmdl")):
            trial = temp / f"standalone-{i}"
            path = trial / "PowerBI/Parcel/ParcelSummary.tmdl"
            path.parent.mkdir(parents=True)
            path.write_text(text)
            if i:
                shutil.copytree(
                    ROOT / "examples/parcel-powerbi-fabric/Warehouse",
                    trial / "Warehouse",
                )
            check(trial, f"standalone TMDL {i}")
            if not i:
                effective = model(compile_models(trial), "ParcelSummary")
                assert (
                    effective.tables["Delivery"].partitions["Delivery"].mode == "import"
                )
                assert (
                    effective.tables["Delivery"].measures["Delivery Count"].expression
                    == "SUM(Delivery[Delivered])"
                )
    assert hashes(ROOT / "examples") == before
    print(
        "PASS:",
        json.dumps(counts, sort_keys=True),
        f"; {len(sync)} byte-identical fixture blocks; {len(checks)} assembled Check checkpoints",
    )
    print("PASS:", "; ".join(checks))
    print(
        "PASS: effective visibility, relationship/partition preservation, policy precedence/calculation group, shared-rule transfer, custom folder, failure/correction preserve prior overlay; exact catalogue names/readback; authored fixture SHA-256 unchanged; no service execution"
    )


if __name__ == "__main__":
    main()
