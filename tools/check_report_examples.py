"""Check the Report guide's exact native files and offline binding payloads."""

import argparse
import json
import re
import shlex
import socket
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    args = parser.parse_args()
    source = args.weaver_checkout.resolve()
    sys.path[:0] = [
        str(source / "src"),
        str(source / "tests"),
        str(source / "tests/targeted"),
    ]
    import weaver
    from check_docs_refresh_examples import (
        check_native,
        check_report_bindings,
        hashes,
        parse,
        refuse_network,
    )
    from weaver_cli.main import build_parser

    assert Path(weaver.__file__).resolve().is_relative_to(source / "src")
    socket.socket.connect = refuse_network
    socket.create_connection = refuse_network
    root = Path(__file__).resolve().parents[1]
    fixture = root / "examples/parcel-powerbi"
    before = hashes(fixture)
    repository = parse(fixture)
    check_native(
        fixture, repository, json.loads((fixture / "expected-results.json").read_text())
    )
    check_report_bindings(fixture, repository)
    import yaml
    from weaver.config import parse_workspace
    from weaver.operations.build import _item_bindings

    workspace = parse_workspace(
        yaml.safe_load((fixture / "workspace-development.yml").read_text())
    )
    model_only = _item_bindings(
        "SemanticModel/Parcel", workspace, repository=repository
    )
    assert [str(binding.item) for binding in model_only.entries] == [
        "SemanticModel/Parcel"
    ]
    pair = _item_bindings("PowerBI/Parcel", workspace, repository=repository)
    assert {str(binding.item) for binding in pair.entries} == {
        "SemanticModel/Parcel",
        "Report/Parcel",
    }
    assert hashes(fixture) == before
    counts = {"commands": 0, "exact_fixture_blocks": 0}
    for name in ("deploy", "environments"):
        text = (root / f"docs/reports/{name}.md").read_text()
        for block in re.findall(
            r"^```bash[^\n]*\n(.*?)^```", text, re.MULTILINE | re.DOTALL
        ):
            for line in block.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    assert not re.match(r"weaver (?:load|test) Report/", line)
                    counts["commands"] += 1
        for language, expected in (
            ("yaml", fixture / "workspace-development.yml"),
            ("yaml", fixture / "workspace-production.yml"),
            ("json", fixture / "PowerBI/Parcel/Parcel.Report/definition.pbir"),
        ):
            blocks = re.findall(
                r"^```" + language + r"[^\n]*\n(.*?)^```",
                text,
                re.MULTILINE | re.DOTALL,
            )
            if expected.read_text() in blocks:
                counts["exact_fixture_blocks"] += 1
    # Named Initialise supplies the first-use configuration; only the two
    # environment mappings and linked native definition are repeated here.
    assert counts["commands"] > 0 and counts["exact_fixture_blocks"] == 3, counts
    print(
        json.dumps(
            {
                **counts,
                "fixture_hashes_unchanged": len(before),
                "native_and_offline_dev_prod_binding": "pass",
                "service_readback": "not exercised",
            }
        )
    )


if __name__ == "__main__":
    main()
