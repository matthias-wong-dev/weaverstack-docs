"""Exercise the installed wheel without a checkout or network.

Fabric inventory/creation is an explicit offline boundary. No service execution
or Fabric Build/Load success is claimed by this generation check.
"""

import contextlib
import itertools
import json
import socket
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

installed = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(installed))
import weaver
from weaver.fabric import resources
from weaver.operations.check import check
from weaver.sessions import TestSession
from weaver_cli.main import build_parser

assert Path(weaver.__file__).resolve().is_relative_to(installed)


def refuse(*args, **kwargs):
    raise AssertionError("Wheel generation attempted network access")


def files(root):
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file()
    }


def source_files(root):
    return {
        p: b
        for p, b in files(root).items()
        if p.startswith(("Lakehouse/", "Warehouse/", "PowerBI/"))
        and not p.endswith(".gitkeep")
    }


keys = ("lakehouse", "warehouse", "semantic_model")
selections = [tuple(c) for n in range(1, 4) for c in itertools.combinations(keys, n)]
manifest = {
    "wheel_import": str(weaver.__file__),
    "network": "refused",
    "fabric_boundary": "offline inventory/creation only",
    "selections": {},
    "subset_pairs_verified": 0,
    "extension_orders_verified": [],
}
physical = resources.WorkspaceItem("offline-workspace", "Example")
held = []


def create(workspace, name, kind):
    item = resources.Item("offline-" + name, name, kind, workspace.id)
    held.append(item)
    return item


with contextlib.ExitStack() as guards:
    guards.enter_context(patch.object(socket.socket, "connect", refuse))
    guards.enter_context(patch.object(socket, "create_connection", refuse))
    guards.enter_context(
        patch.object(resources, "find_workspace", lambda *a, **k: physical)
    )
    guards.enter_context(
        patch.object(resources, "list_items", lambda *a, **k: tuple(held))
    )
    guards.enter_context(
        patch.object(
            resources, "create_lakehouse", lambda w, n, **k: create(w, n, "Lakehouse")
        )
    )
    guards.enter_context(
        patch.object(
            resources, "create_warehouse", lambda w, n, **k: create(w, n, "Warehouse")
        )
    )
    guards.enter_context(
        patch(
            "weaver.fabric.environment.create_with_definition",
            lambda w, n, d, **k: create(w, n, "Environment"),
        )
    )
    with tempfile.TemporaryDirectory(prefix="named-wheel-") as temporary:
        empty = Path(temporary)
        for example in (None, "Parcel", "Sales"):
            generated = {}
            for selection in selections:
                held.clear()
                root = empty / ((example or "None") + "-" + "-".join(selection))
                options = {
                    k: {
                        "lakehouse": "Landing",
                        "warehouse": "Operations",
                        "semantic_model": example or "Model",
                    }[k]
                    for k in selection
                }
                with TestSession(resolver=SimpleNamespace(client=object())) as session:
                    report = weaver.initialise(
                        root,
                        workspace="Example",
                        example=example,
                        session=session,
                        **options,
                    )
                assert report.succeeded
                if selection == ("semantic_model",):
                    assert not held and not report.resources
                    assert not (root / "Environment").exists()
                check(root)
                generated[selection] = source_files(root)
                manifest["selections"][
                    (example or "None") + "/" + "+".join(selection)
                ] = sorted(files(root))
                if example:
                    build_parser().parse_args(["initialise", "--example", example])
            if example:
                for small, first in generated.items():
                    for large, second in generated.items():
                        if set(small) < set(large):
                            assert all(second.get(p) == b for p, b in first.items()), (
                                example,
                                small,
                                large,
                            )
                            manifest["subset_pairs_verified"] += 1
        for example in ("Parcel", "Sales"):
            for order in (
                ("lakehouse", "warehouse"),
                ("warehouse", "lakehouse"),
                ("warehouse", "semantic_model"),
                ("semantic_model", "warehouse"),
                ("lakehouse", "warehouse", "semantic_model"),
            ):
                held.clear()
                root = empty / ("extend-" + example + "-".join(order))
                with TestSession(resolver=SimpleNamespace(client=object())) as session:
                    before = {}
                    for k in order:
                        value = {
                            "lakehouse": "Landing",
                            "warehouse": "Operations",
                            "semantic_model": example,
                        }[k]
                        weaver.initialise(
                            root,
                            workspace="Example",
                            example=example,
                            session=session,
                            **{k: value},
                        )
                        assert all(
                            source_files(root).get(p) == b for p, b in before.items()
                        )
                        before = source_files(root)
                    snapshot = files(root)
                    weaver.initialise(
                        root, workspace="Example", example=example, session=session
                    )
                    assert files(root) == snapshot
                manifest["extension_orders_verified"].append([example, *order])
        for name, module in sys.modules.copy().items():
            path = getattr(module, "__file__", None)
            if (
                name == "weaver"
                or name.startswith("weaver.")
                or name == "weaver_cli"
                or name.startswith("weaver_cli.")
            ) and path:
                assert Path(path).resolve().is_relative_to(installed), (name, path)
output.write_text(json.dumps(manifest, indent=2) + "\n")
print(
    json.dumps(
        {
            "generated_projects": len(manifest["selections"]),
            "source_subset_pairs": manifest["subset_pairs_verified"],
            "extension_orders": len(manifest["extension_orders_verified"]),
            "installed_import": manifest["wheel_import"],
            "network": "refused",
            "fabric": "not contacted",
        },
        indent=2,
    )
)
