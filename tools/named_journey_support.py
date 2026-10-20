"""Offline boundaries shared by checks of the named, continuing Parcel journey.

Inventory, item creation and SQL column readback are explicitly test inputs.
These helpers do not claim that Fabric Build, Load or refresh has executed.
"""

import contextlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


def sources(root):
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for prefix in ("Lakehouse", "Warehouse", "PowerBI")
        for p in (root / prefix).rglob("*")
        if p.is_file() and not p.name.endswith(".pyc")
    }


class OfflineInitialiser:
    def __enter__(self):
        from weaver.fabric import resources

        self.resources = resources
        self.workspace = resources.WorkspaceItem(
            "offline-workspace", "Parcel Development"
        )
        self.held = []
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(
            patch.object(resources, "find_workspace", lambda *a, **k: self.workspace)
        )
        self.stack.enter_context(
            patch.object(resources, "list_items", lambda *a, **k: tuple(self.held))
        )
        self.stack.enter_context(
            patch.object(
                resources,
                "create_lakehouse",
                lambda w, n, **k: self.create(w, n, "Lakehouse"),
            )
        )
        self.stack.enter_context(
            patch.object(
                resources,
                "create_warehouse",
                lambda w, n, **k: self.create(w, n, "Warehouse"),
            )
        )
        self.stack.enter_context(
            patch(
                "weaver.fabric.environment.create_with_definition",
                lambda w, n, d, **k: self.create(w, n, "Environment"),
            )
        )
        return self

    def create(self, workspace, name, kind):
        item = self.resources.Item("offline-" + name, name, kind, workspace.id)
        self.held.append(item)
        return item

    def __call__(self, root, **items):
        import weaver
        from weaver.sessions import TestSession

        with TestSession(resolver=SimpleNamespace(client=object())) as session:
            report = weaver.initialise(
                root,
                workspace="Parcel Development",
                example="Parcel",
                session=session,
                **items,
            )
        assert report.succeeded
        return report

    def __exit__(self, *args):
        return self.stack.__exit__(*args)


def compiled(root):
    from check_docs_refresh_examples import parse
    from weaver.semantic_models.binding import bind_semantic_sources

    raw = parse(root)
    observed = {}
    for contribution in raw.semantic_models.values():
        for reference in contribution.source_references.values():
            schema, entity = reference.rsplit("/", 1)[1].split(".")
            observed[reference] = {
                "reference": reference,
                "server": "offline.example.invalid",
                "database": "Offline",
                "schema": schema,
                "object": entity,
                "description": "",
                "column_notes": {},
                "source_columns": [
                    {"column_name": n, "data_type": "varchar"}
                    for n in ("Parcel ID", "Status", "Depot")
                ],
            }
    return bind_semantic_sources(raw, observed, raw.semantic_models)


def append_target(root, identity):
    import yaml

    path = Path(root) / "workspace-config.yml"
    value = yaml.safe_load(path.read_text())
    value["targets"][identity] = identity.partition("/")[2]
    path.write_text(yaml.safe_dump(value, sort_keys=False))
