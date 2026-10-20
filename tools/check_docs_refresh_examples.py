#!/usr/bin/env python3
"""Offline fixture checks against pinned Weaver; no Fabric client is used.

Requires the pinned checkout's test dependencies and small offline test helpers.
Boundary answers below are test inputs, not DAX evaluation or service readback.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
PIN = "74b4d15ee65ed2740593af1f4d459771b801b132"
FIXTURES = (
    "parcel-powerbi",
    "parcel-powerbi-validation",
    "parcel-powerbi-standards",
    "parcel-powerbi-variants",
    "parcel-load-selection",
    "parcel-powerbi-fabric",
)
ROOT = Path(__file__).resolve().parents[1]


def hashes(root):
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def refuse_network(*args, **kwargs):
    raise AssertionError("Offline checks attempted a network connection")


def parse(root):
    from weaver.declaration.repository import parse_item_repository
    from weaver.locations import Location

    return parse_item_repository(Location(str(root)))


def compile_models(root, selected=None):
    from weaver.semantic_models.binding import bind_semantic_sources

    raw = parse(root)
    return bind_semantic_sources(
        raw, {}, raw.semantic_models if selected is None else selected
    )


def item(text):
    from weaver.declaration.model import WeaverItemId

    return WeaverItemId.parse(text)


def model(repository, name="Parcel"):
    from weaver.semantic_models import TmdlDefinition

    return TmdlDefinition(
        repository.semantic_models[item("SemanticModel/" + name)].parts
    ).model


def check_readme_commands(root):
    from weaver_cli.main import build_parser

    count = 0
    for line in (root / "README.md").read_text().splitlines():
        if line.startswith("weaver "):
            build_parser().parse_args(shlex.split(line)[1:])
            count += 1
    assert count, root
    return count


def check_native(root, repository, expected):
    for name in expected["models"]:
        native = root / f"PowerBI/Parcel/{name}.SemanticModel"
        assert (native / "definition.pbism").is_file()
        assert (native / "definition/database.tmdl").is_file()
        assert (native / "definition/model.tmdl").is_file()
        effective = model(compile_models(root), name)
        assert effective.tables["Delivery"].partitions["Delivery"].mode == "import"
        assert effective.tables["Depot"].partitions["Depot"].mode == "import"
        relationship = effective.relationships["Delivery_Depot"]
        assert relationship.fromColumn == "Delivery.DepotId"
        assert relationship.toColumn == "Depot.DepotId"
        assert relationship.fromCardinality == "many"
        assert relationship.toCardinality == "one"
        assert (
            effective.tables["Delivery"].measures["Delivery Count"].expression
            == "SUM(Delivery[Delivered])"
        )
    for report_name, model_name in expected["reports"].items():
        report = repository.reports[item("Report/" + report_name)]
        assert str(report.model) == "SemanticModel/" + model_name
        project = root / f"PowerBI/Parcel/{report_name}.pbip"
        assert (
            json.loads(project.read_text())["artifacts"][0]["report"]["path"]
            == report_name + ".Report"
        )
        parts = report.parts
        assert "definition/report.json" in parts and "definition/version.json" in parts
        pages = json.loads(parts["definition/pages/pages.json"])
        for page_name in pages["pageOrder"]:
            page_path = f"definition/pages/{page_name}/page.json"
            page = json.loads(parts[page_path])
            assert page["width"] > 0 and page["height"] > 0
            assert page.get("visibility", "AlwaysVisible") == "AlwaysVisible"
            visuals = [
                json.loads(data)
                for path, data in parts.items()
                if path.startswith(f"definition/pages/{page_name}/visuals/")
                and path.endswith("visual.json")
            ]
            assert visuals, "A report with no visible result is not this fixture"
            for visual in visuals:
                assert not visual.get("isHidden", False)
                assert visual["position"]["width"] > 0
                field = visual["visual"]["query"]["queryState"]["Values"][
                    "projections"
                ][0]["field"]["Measure"]
                assert field["Expression"]["SourceRef"]["Entity"] == "Delivery"
                assert field["Property"] == "Delivery Count"
                assert (
                    model(compile_models(root), model_name)
                    .tables["Delivery"]
                    .measures[field["Property"]]
                )


def check_report_bindings(root, repository):
    from support.workspaces import InventoryClient
    from weaver.config import load_workspace
    from weaver.fabric.resolution import FabricResolver
    from weaver.report_definition import decode_report, encode_report, verify_report
    from weaver.targets import ItemRef

    for long, short in (("development", "dev"), ("production", "prod")):
        # The Report fixture uses the full names the Report pages use.
        path = root / f"workspace-{long}.yml"
        if not path.exists():
            path = root / f"workspace-{short}.yml"
        workspace = load_workspace(path)
        inventory = InventoryClient(
            workspace.workspace,
            [(i.item_type, target.physical) for i, target in workspace.targets.items()],
        )
        resolver = FabricResolver(workspace, client=inventory)
        for report in repository.reports.values():
            target = workspace.targets[report.model].physical
            physical = resolver.resolve(ItemRef(target), item_type="SemanticModel")
            binding = {"workspace_id": physical.workspace_id, "item_id": physical.id}
            bound = replace(report, binding=binding)
            payload = encode_report(bound)
            assert verify_report(payload, payload) == ()
            parts = decode_report(payload)
            assert {p: b for p, b in parts.items() if p != "definition.pbir"} == {
                p: b for p, b in report.parts.items() if p != "definition.pbir"
            }
            reference = json.loads(parts["definition.pbir"])["datasetReference"]
            assert binding["item_id"] in reference["byConnection"]["connectionString"]
            assert "byPath" not in reference
    # This is the real encoder over an offline inventory, not deployed binding evidence.


def check_standards(root, expected):
    original = model(parse(ROOT / "examples/parcel-powerbi"))
    assert original.tables["Delivery"].columns["DepotId"].isHidden is None
    effective = model(compile_models(root))
    assert effective.tables["Delivery"].columns["DepotId"].isHidden is True
    assert effective.tables["Depot"].columns["DepotId"].isHidden is None
    assert effective.tables["Delivery"].columns["ParcelId"].isHidden is None
    count = effective.tables["Delivery"].measures["Delivery Count"]
    assert count.formatString == expected["overlay_format"]
    assert count.displayFolder == expected["custom_display_folder"]
    assert (
        effective.tables["Delivery"].measures["InternalCost"].formatString == "#,##0.00"
    )
    assert effective.discourageImplicitMeasures is True
    group = effective.tables[expected["calculation_group"]].calculationGroup
    assert group.precedence == "10"
    assert (
        group.calculationItems[expected["calculation_item"]].expression
        == "SELECTEDMEASURE()"
    )
    # Native unrelated partitions survive, not only the small requested-property projection.
    for name in ("Delivery", "Depot"):
        assert (
            effective.tables[name].partitions[name].source
            == original.tables[name].partitions[name].source
        )


def check_variants(root, expected):
    raw = parse(root)
    from weaver.config import load_workspace
    from weaver.declaration.selectors import expand_item_selectors
    from weaver.errors import ConfigError
    from weaver.operations.build import _item_bindings

    selectors = [
        f"{kind}/{name}"
        for name in expected["selected_models"]
        for kind in ("SemanticModel", "Report")
    ]
    for environment in ("dev", "prod"):
        workspace = load_workspace(root / f"workspace-{environment}.yml")
        bindings = _item_bindings(selectors, workspace, repository=raw)
        assert set(bindings.by_item) == {item(selector) for selector in selectors}
        assert item("SemanticModel/" + expected["base_model"]) not in bindings.by_item
        project_wide = expand_item_selectors(
            ["PowerBI/Parcel"],
            repository=raw,
            configured_items=workspace.configured_items,
        )
        assert "SemanticModel/" + expected["base_model"] in project_wide
        try:
            _item_bindings(["PowerBI/Parcel"], workspace, repository=raw)
        except ConfigError as exc:
            assert "No target is configured for SemanticModel/ParcelBase" in str(exc)
        else:
            raise AssertionError(
                "The source-only base unexpectedly has a deployment target"
            )
    selected = {item("SemanticModel/" + n) for n in expected["selected_models"]}
    compiled = compile_models(root, selected)
    base = item("SemanticModel/" + expected["base_model"])
    assert base not in selected
    assert compiled.semantic_models[base].parts == raw.semantic_models[base].parts
    operations = model(compiled, "ParcelOperations")
    executive = model(compiled, "ParcelExecutive")
    assert (
        operations.tables["Delivery"].measures["Delivery Rate"].expression
        == "DIVIDE([Delivery Count], COUNTROWS(Delivery))"
    )
    assert "InternalCosts" in {t.name for t in operations.tables}
    assert "InternalCosts" not in {t.name for t in executive.tables}
    assert (
        executive.tables["Delivery"].measures["Delivery Count"].formatString == "#,##0"
    )
    for name in expected["selected_models"]:
        validations = [
            str(d)
            for d, source in raw.source_documents.items()
            if source.is_validation and d.item == item("SemanticModel/" + name)
        ]
        assert validations == [f"SemanticModel/{name}/Parcel.PositiveDeliveryCount"]
    assert not [
        s for d, s in raw.source_documents.items() if s.is_validation and d.item == base
    ]


def check_failures(root, temporary):
    from weaver.errors import ConfigError

    cases = {
        "parcel-powerbi-validation": ("Parcel", None),
        "parcel-powerbi-standards": ("Parcel", "requires a non-empty display folder"),
        "parcel-powerbi-variants": ("ParcelExecutive", "MissingBase"),
        "parcel-powerbi-fabric": ("Parcel", None),
    }
    if root.name not in cases:
        return
    name, error = cases[root.name]
    trial = temporary / root.name
    shutil.copytree(root, trial)
    shutil.copyfile(
        trial / f"failure/{name}.tmdl", trial / f"PowerBI/Parcel/{name}.tmdl"
    )
    if error:
        try:
            compile_models(trial)
        except ConfigError as exc:
            assert error in str(exc), str(exc)
            location = (
                f"PowerBI/Parcel/{name}.tmdl"
                if root.name.endswith("standards")
                else "PowerBI/Parcel"
            )
            assert location in str(exc)
        else:
            raise AssertionError(f"Deliberate invalid overlay accepted: {root.name}")
    else:
        expression = (
            model(compile_models(trial))
            .tables["Delivery"]
            .measures["Delivery Count"]
            .expression
        )
        assert expression == (
            "-1" if root.name.endswith("validation") else "SUM(Delivery[Delivered]) + 1"
        )


def check_load_selection(root, expected):
    from factories import installed_catalogue, item_bindings
    from weaver.errors import LoadError
    from weaver.load_plan import LoadDag

    repository = parse(root)
    catalogue = installed_catalogue(
        repository,
        item_bindings(
            ("Warehouse/Operations", "Parcel_Operations_Dev"),
            ("Warehouse/Reporting", "Parcel_Reporting_Dev"),
        ),
    )
    before = catalogue.to_mapping()
    operations, reporting = item("Warehouse/Operations"), item("Warehouse/Reporting")
    for label, policy in (
        ("plain", {}),
        ("ancestors", {"ancestors": True}),
        ("descendants", {"descendants": True}),
        ("both", {"ancestors": True, "descendants": True}),
    ):
        plan = LoadDag.from_catalogue(
            catalogue, items=[operations], names=[expected["seed"]], **policy
        )
        assert [n.logical_id.object_id.qualified for n in plan.order()] == expected[
            "selection"
        ][label]
        if label == "plain":
            assert plan.edges == ()
    cross = LoadDag.from_catalogue(
        catalogue,
        items=[operations, reporting],
        names=[expected["seed"]],
        descendants=True,
    )
    assert [str(n.logical_id) for n in cross.order()] == expected["selection"][
        "cross_item"
    ]
    repeated = LoadDag.from_catalogue(
        catalogue, items=[operations], names=["parcel[.]events", "Reference[.]Service"]
    )
    assert {n.logical_id.object_id.qualified for n in repeated.nodes} == {
        "Parcel.Events",
        "Reference.Service",
    }
    assert repeated.edges == ()
    ordinary = LoadDag.from_catalogue(catalogue, items=[operations, reporting])
    assert len(ordinary.nodes) == 7
    assert len(ordinary.edges) == 5
    # Each pattern must match; substring, malformed regex and partial matches refuse.
    for patterns in (
        ["Events"],
        ["Parcel[.]Missing"],
        ["Parcel[.]Events", "Parcel[.]Missing"],
        ["["],
    ):
        try:
            LoadDag.from_catalogue(catalogue, items=[operations], names=patterns)
        except LoadError:
            pass
        else:
            raise AssertionError(f"Expected regex refusal: {patterns}")
    assert catalogue.to_mapping() == before
    print(
        "PASS: fixture LoadDag exact sets, cross-item scope, original-seed union and regex refusals"
    )
    return catalogue


def check_area_identity(temporary, expected):
    from factories import (
        folder_document,
        installed_catalogue,
        item_bindings,
        lakehouse_table,
        single_document_repository,
    )
    from weaver.errors import LoadError
    from weaver.load_plan import LoadDag

    logical = "Lakehouse/AreaProbe"
    table = lakehouse_table("Parcel.Events").replace(
        "from weaver import Table",
        "from Files.Parcel__Events import Parcel__Events as FilesEvents\nfrom weaver import Table",
    )
    repository = single_document_repository(
        temporary / "area-probe",
        item=logical,
        schemas=("Parcel",),
        documents={
            "Files/Parcel__Events.py": folder_document("Parcel.Events"),
            "Tables/Parcel__Events.py": table,
        },
    )
    catalogue = installed_catalogue(
        repository, item_bindings((logical, "Parcel_Area_Dev"))
    )
    identities = expected["lakehouse_area_identity"]
    try:
        LoadDag.from_catalogue(
            catalogue, items=[item(logical)], names=[identities["ambiguous"]]
        )
    except LoadError as exc:
        assert "Choose an area-qualified name" in str(exc)
    else:
        raise AssertionError("Bare colliding Lakehouse identity accepted")
    for area, key in (("Tables", "table"), ("Files", "folder")):
        plan = LoadDag.from_catalogue(
            catalogue, items=[item(logical)], names=[identities[key]]
        )
        (node,) = plan.nodes
        assert str(node.logical_id) == f"{logical}/{area}/Parcel.Events"
    print(
        "PASS: real LoadDag Lakehouse bare-area ambiguity and both qualified identities"
    )


def check_fixture_concurrency(catalogue, cap, warehouse_limit):
    import threading
    import time

    from weaver.run import Runner, RunRequest, RunState
    from weaver.run.runner import Lanes
    from weaver.runtime.load_result import LoadResult

    # Only dispatch is a double. The seven-node graph, resolution and scheduler
    # are the production path over the catalogue projected from these files.
    lock = threading.Lock()
    active = 0
    peak = 0
    per_warehouse = {}
    warehouse_peaks = {}
    events = []

    def dispatch(node, **kwargs):
        nonlocal active, peak
        lane = node.physical_target.name
        with lock:
            active += 1
            peak = max(peak, active)
            per_warehouse[lane] = per_warehouse.get(lane, 0) + 1
            warehouse_peaks[lane] = max(
                warehouse_peaks.get(lane, 0), per_warehouse[lane]
            )
            events.append((node.node_id, "start"))
        time.sleep(0.03)
        with lock:
            events.append((node.node_id, "end"))
            active -= 1
            per_warehouse[lane] -= 1
        return LoadResult(succeeded=True)

    request = RunRequest.load(
        [item("Warehouse/Operations"), item("Warehouse/Reporting")], concurrency=cap
    )
    runner = Runner(RunState(catalogue), request)
    result = runner.run(dispatch=dispatch, lanes=Lanes(warehouse=warehouse_limit))
    assert result.succeeded, result.to_mapping()
    assert len(result.nodes) == 7
    assert 1 <= peak <= cap, (peak, warehouse_limit)
    if warehouse_limit == 4:
        assert peak == cap
    assert all(value <= warehouse_limit for value in warehouse_peaks.values())
    assert warehouse_peaks["Parcel_Operations_Dev"] == min(warehouse_limit, cap)
    assert active == 0 and not any(per_warehouse.values())
    for upstream, downstream in runner.graph.edges:
        assert events.index((upstream, "end")) < events.index((downstream, "start"))
    print(
        f"PASS: fixture real Runner total cap {cap}, per-Warehouse {warehouse_limit}, observed peak {peak}"
    )


def check_file_validation(root, *, rows, expected_status):
    import weaver
    from support.workspaces import InventoryClient
    from weaver.config import load_workspace
    from weaver.fabric.resolution import FabricResolver
    from weaver.sessions import TestSession
    from weaver.store import FilesystemStore

    workspace = replace(load_workspace(root / "workspace-dev.yml"), catalogue=None)
    inventory = InventoryClient(
        workspace.workspace,
        [(i.item_type, target.physical) for i, target in workspace.targets.items()],
    )
    session = TestSession(
        workspace=workspace,
        store=FilesystemStore(),
        resolver=FabricResolver(workspace, client=inventory),
    )
    queries = []

    def query_dax(query):
        queries.append(query)
        if isinstance(rows, Exception):
            raise rows
        return rows

    physical = session.resolve_item("Parcel_Dev", item_type="SemanticModel")
    session.answer_semantic_model(
        physical.workspace_id, physical.id, SimpleNamespace(query_dax=query_dax)
    )
    if root.name.endswith("fabric"):
        sources = [s for s in parse(root).source_documents.values() if s.is_validation]
        (source,) = sources
        session.answer_tsql(source.document.expected_sql, [{"DeliveryCount": 2}])
    with session:
        report = weaver.test(
            "SemanticModel/Parcel",
            source=root,
            session=session,
            names=r"Parcel[.](PositiveDeliveryCount|DeliveryReconciles)",
        )
    (node,) = report.nodes
    assert node.status == expected_status, report.to_mapping()
    assert report.workflow_id is None
    assert len(queries) == 1
    if expected_status == "failed":
        assert node.diagnostics
    # The double answers DAX/SQL only. Source mode must not write catalogue state.
    assert not any(
        c.kind == "tsql" and c.detail.get("statement", "").startswith("MERGE")
        for c in session.calls
    )
    return node.status


def check_pbir_schemas():
    """Optional public-schema check; needs jsonschema, never a Fabric connection."""
    import urllib.request
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from jsonschema import Draft7Validator, RefResolver
    cache = {}
    fetched = set()

    def retrieve(url):
        assert url.startswith(
            "https://developer.microsoft.com/json-schemas/fabric/item/report/"
        ), url
        if url not in cache:
            with urllib.request.urlopen(url, timeout=30) as response:
                cache[url] = json.load(response)
            fetched.add(url)
            if "$id" in cache[url]:
                cache[cache[url]["$id"]] = cache[url]
        return cache[url]

    count = 0
    for name in FIXTURES:
        for path in sorted((ROOT / "examples" / name / "PowerBI").rglob("*")):
            if not path.is_file() or path.suffix not in {".json", ".pbir"}:
                continue
            instance = json.loads(path.read_text())
            if "$schema" not in instance:
                continue
            schema = retrieve(instance["$schema"])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                resolver = RefResolver.from_schema(schema, handlers={"https": retrieve})
                errors = list(
                    Draft7Validator(schema, resolver=resolver).iter_errors(instance)
                )
            assert not errors, f"{path}: " + "; ".join(e.message for e in errors)
            count += 1
    print(
        f"PASS: {count} PBIR JSON documents; {len(fetched)} public Microsoft schemas fetched; no Fabric calls"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", type=Path)
    parser.add_argument(
        "--runtime-revision",
        default=PIN,
        help="Explicit integrated runtime revision; original fixture provenance stays pinned",
    )
    parser.add_argument(
        "--check-pbir-schemas",
        action="store_true",
        help="Separate optional check using public Microsoft schemas; requires jsonschema and network",
    )
    args = parser.parse_args()
    if args.check_pbir_schemas:
        check_pbir_schemas()
        return
    if args.weaver_checkout is None:
        parser.error("--weaver-checkout is required for offline checks")
    checkout = args.weaver_checkout.resolve()
    revision = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    # A parallel product-site worktree may advance docs without changing runtime.
    runtime_paths = ["src", "tests", "pyproject.toml"]
    for comparison in ([args.runtime_revision, "HEAD"], ["HEAD"]):
        result = subprocess.run(
            [
                "git",
                "-C",
                str(checkout),
                "diff",
                "--quiet",
                *comparison,
                "--",
                *runtime_paths,
            ],
            check=False,
        )
        assert result.returncode == 0, (
            f"Checkout runtime differs from pinned {args.runtime_revision} (HEAD {revision})"
        )
    print(
        f"Source runtime matches {args.runtime_revision}; checkout HEAD {revision}; fixture provenance {PIN}"
    )
    sys.path[:0] = [
        str(checkout / "src"),
        str(checkout / "tests"),
        str(checkout / "tests/targeted"),
    ]
    import weaver

    assert Path(weaver.__file__).resolve().is_relative_to(checkout / "src")
    socket.create_connection = refuse_network
    socket.socket.connect = refuse_network
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(checkout / "src"),
    }
    command_count = 0
    with tempfile.TemporaryDirectory(prefix="weaver-doc-fixtures-") as directory:
        temporary = Path(directory)
        for name in FIXTURES:
            root = ROOT / "examples" / name
            assert root.is_dir(), f"Missing complete fixture: {name}"
            before = hashes(root)
            expected = json.loads((root / "expected-results.json").read_text())
            assert expected["source_revision"] == PIN
            command_count += check_readme_commands(root)
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from weaver_cli.main import main; raise SystemExit(main())",
                    "check",
                    str(root),
                    "--json",
                    "--non-interactive",
                ],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0, result.stdout + result.stderr
            assert json.loads(result.stdout)["status"] == "succeeded"
            repository = parse(root)
            check_native(root, repository, expected)
            check_report_bindings(root, repository)
            if name.endswith("standards"):
                check_standards(root, expected)
            if name.endswith("variants"):
                check_variants(root, expected)
            if name.endswith("selection"):
                catalogue = check_load_selection(root, expected)
                check_area_identity(temporary, expected)
                for warehouse_limit in (4, 1):
                    check_fixture_concurrency(
                        catalogue, expected["concurrency"], warehouse_limit
                    )
            if name.endswith("fabric"):
                contribution = repository.semantic_models[item("SemanticModel/Parcel")]
                assert contribution.source_references == {
                    "Delivery": expected["source"]
                }
                assert ("Delivery", expected["source"]) in contribution.dependencies
                compiled = compile_models(root).semantic_models[
                    item("SemanticModel/Parcel")
                ]
                assert (
                    model(repository).tables["Delivery"].partitions["Delivery"].source
                    == model(compile_models(root))
                    .tables["Delivery"]
                    .partitions["Delivery"]
                    .source
                )
                assert compiled.source_bindings["Delivery"]["access"] is None
            check_failures(root, temporary)
            if name.endswith("validation"):
                statuses = [
                    check_file_validation(root, rows=rows, expected_status=status)
                    for rows, status in (
                        (expected["pass_rows"], "passed"),
                        (expected["finding_rows"], "failed"),
                        (
                            RuntimeError("offline DAX permission refusal input"),
                            "invalid",
                        ),
                        ([], "passed"),
                    )
                ]
                print("PASS: file Assumption boundary inputs -> " + ", ".join(statuses))
            if name.endswith("fabric"):
                statuses = [
                    check_file_validation(root, rows=rows, expected_status=status)
                    for rows, status in (
                        ([{"[DeliveryCount]": 2}], "passed"),
                        (expected["discrepancy_rows"], "failed"),
                        (RuntimeError("offline DAX query refusal input"), "invalid"),
                        ([{"[DeliveryCount]": 2}], "passed"),
                    )
                ]
                print("PASS: file DAX/SQL boundary inputs -> " + ", ".join(statuses))
            assert hashes(root) == before, f"Authored fixture changed: {name}"
            print(
                f"PASS: {name}: real CLI Check, definitions, expected manifest, bindings and SHA-256 unchanged"
            )
    print(
        f"PASS: {len(FIXTURES)} fixtures; {command_count} README Weaver commands parsed; no live service exercised"
    )


if __name__ == "__main__":
    main()
