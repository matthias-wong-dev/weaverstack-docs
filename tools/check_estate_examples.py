"""Check the continuing Landing/Operations instructions without service calls."""

import argparse
import json
import re
import shlex
import socket
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    source = args.weaver_checkout.resolve()
    sys.path[:0] = [
        str(source / "src"),
        str(source / "tests"),
        str(source / "tests/targeted"),
    ]
    import weaver
    import yaml
    from check_docs_refresh_examples import item, parse, refuse_network
    from factories import installed_catalogue, item_bindings
    from named_journey_support import OfflineInitialiser, sources
    from weaver.config import parse_workspace
    from weaver.load_plan import LoadDag
    from weaver_cli.main import build_parser
    from weaver_cli.main import main as cli_main

    assert Path(weaver.__file__).resolve().is_relative_to(source / "src")
    socket.socket.connect = refuse_network
    socket.create_connection = refuse_network
    counts = {
        "estate_commands": 0,
        "workspace_configs": 0,
        "continuous_project_checks": 0,
        "selection_plans": 0,
    }
    for page in (root / "docs/estate").glob("*.md"):
        text = page.read_text()
        for block in re.findall(
            r"^```bash[^\n]*\n(.*?)^```", text, re.MULTILINE | re.DOTALL
        ):
            for line in block.replace("\\\n", " ").splitlines():
                if line.startswith("weaver "):
                    build_parser().parse_args(shlex.split(line)[1:])
                    counts["estate_commands"] += 1
        for block in re.findall(
            r"^```yaml[^\n]*\n(.*?)^```", text, re.MULTILINE | re.DOTALL
        ):
            obj = yaml.safe_load(block)
            if isinstance(obj, dict) and "workspace" in obj:
                parse_workspace(obj)
                counts["workspace_configs"] += 1
    with (
        tempfile.TemporaryDirectory(prefix="estate-continuation-") as directory,
        OfflineInitialiser() as initialise,
    ):
        project = Path(directory)
        initialise(project, lakehouse="Landing")
        original = sources(project)
        initialise(project, warehouse="Operations")
        assert all(
            sources(project).get(p) == content for p, content in original.items()
        )
        connected = (root / "docs/estate/connected-items.md").read_text()
        for relative, language in (
            ("Warehouse/Operations/shortcuts.yml", "yaml"),
            ("Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql", "sql"),
        ):
            assert (project / relative).read_text() in re.findall(
                r"^```" + language + r"[^\n]*\n(.*?)^```",
                connected,
                re.MULTILINE | re.DOTALL,
            )
        assert cli_main(["check", str(project), "--json", "--non-interactive"]) == 0
        counts["continuous_project_checks"] += 1
        configs = re.findall(
            r"^```yaml[^\n]*\n(.*?)^```",
            (root / "docs/estate/environments.md").read_text(),
            re.MULTILINE | re.DOTALL,
        )
        config = next(block for block in configs if "workspace:" in block)
        (project / "workspace-development.yml").write_text(config)
        assert cli_main(["check", str(project), "--json", "--non-interactive"]) == 0
        counts["continuous_project_checks"] += 1
        catalogue = installed_catalogue(
            parse(project),
            item_bindings(
                ("Lakehouse/Landing", "Landing"),
                ("Warehouse/Operations", "ParcelOperationsDev"),
            ),
        )
        expected = {
            "plain": ["Lakehouse/Landing/Tables/Parcel.Event"],
            "ancestors": [
                "Lakehouse/Landing/Files/Parcel.Events",
                "Lakehouse/Landing/Tables/Parcel.Event",
            ],
            "descendants": [
                "Lakehouse/Landing/Tables/Parcel.Event",
                "Lakehouse/Landing/Tables/Parcel.CurrentStatus",
            ],
        }
        leading = (
            (root / "docs/estate/selective-runs.md")
            .read_text()
            .split("## Explore a larger branching selection")[0]
        )
        for label, identities in expected.items():
            flags = {} if label == "plain" else {label: True}
            plan = LoadDag.from_catalogue(
                catalogue,
                items=[item("Lakehouse/Landing")],
                names=["Tables/Parcel[.]Event"],
                **flags,
            )
            assert [str(node.logical_id) for node in plan.order()] == identities
            counts["selection_plans"] += 1
        for page, text in [
            ("selective-runs", leading),
            ("concurrency", (root / "docs/estate/concurrency.md").read_text()),
        ]:
            for block in re.findall(
                r"^```bash[^\n]*\n(.*?)^```", text, re.MULTILINE | re.DOTALL
            ):
                for line in block.splitlines():
                    if line.startswith("weaver "):
                        command = build_parser().parse_args(shlex.split(line)[1:])
                        assert (
                            command.workspace_config == "workspace-development.yml"
                        ), (page, line)
                        assert "Warehouse/Operations" not in line, (page, line)
            if page == "concurrency":
                assert "--concurrency 2" in text
    print(json.dumps(counts, sort_keys=True))
    print(
        "PASS: Landing/Operations continuation, exact real LoadDag selections and active configuration; no service calls"
    )


if __name__ == "__main__":
    main()
