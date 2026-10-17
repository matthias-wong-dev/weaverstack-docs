"""Notebook examples stay on natural data-engineering operations."""

import ast
import importlib.util
import inspect
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATURAL = {
    "initialise",
    "build",
    "load",
    "test",
    "health",
    "mirror",
    "wipe",
    "deploy_catalogue_dashboard",
}


def generator():
    spec = importlib.util.spec_from_file_location(
        "generate_notebook_examples", ROOT / "tools/generate_notebook_examples.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def context():
    return {
        "workspace": "Parcel Development",
        "catalogue": "Warehouse/Catalogue",
    }


def test_core_cell_spells_out_parameters_and_uses_report():
    cell = generator().compile_command(
        "weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --dry-run --workspace-config workspace-development.yml",
        context=context(),
    )
    tree = ast.parse(cell["code"])
    call = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "load"
    )
    parameters = {keyword.arg: keyword.value for keyword in call.keywords}
    assert ast.literal_eval(parameters["items"]) == ["Warehouse/Operations"]
    assert ast.literal_eval(parameters["names"]) == ["Parcel[.]Events"]
    assert ast.literal_eval(parameters["ancestors"]) is True
    assert ast.literal_eval(parameters["dry_run"]) is True
    assert ast.literal_eval(parameters["workspace"]) == "Parcel Development"
    assert ast.literal_eval(parameters["catalogue"]) == "Warehouse/Catalogue"
    assert "workspace_config" not in parameters
    assert cell["code"].endswith("load_result.report()\n")


def test_catalogue_dashboard_calls_its_python_operation():
    cell = generator().compile_command(
        'weaver catalogue-dashboard --name "Catalogue Dashboard" --workspace-config workspace-development.yml',
        context=context(),
    )
    assert cell["operation"] == "deploy_catalogue_dashboard"
    assert cell["parameters"] == {
        "catalogue": "Warehouse/Catalogue",
        "name": "Catalogue Dashboard",
        "workspace": "Parcel Development",
    }
    assert "dashboard_result = weaver.deploy_catalogue_dashboard(" in cell["code"]
    assert cell["code"].endswith("dashboard_result.report()\n")


def test_initialise_uses_the_notebook_resources_project_without_a_cd_cell():
    cells = generator().compile_terminal(
        'weaver initialise --workspace "Parcel Development" --project-folder ./parcel --catalogue Catalogue --warehouse Operations --example Parcel\ncd parcel\n',
        context={},
    )
    assert [cell["operation"] for cell in cells] == ["initialise"]
    code = cells[0]["code"]
    assert "from pathlib import Path" in code
    assert 'project = Path("builtin") / "project"' in code
    assert "project_folder=project" in code
    assert "initialise_result.report()" in code


def test_build_and_file_mode_test_name_the_resources_project_explicitly():
    build = generator().compile_command(
        "weaver build --item Warehouse/Operations", context=context()
    )
    tested = generator().compile_command(
        "weaver test Warehouse/Operations --source . --file Warehouse/Operations/tests",
        context=context(),
    )
    for cell in (build, tested):
        assert 'project = Path("builtin") / "project"' in cell["code"]
        assert "source=project" in cell["code"]


def test_terminal_shaped_commands_are_not_manufactured_into_notebook_cells():
    tool = generator()
    for source in (
        "weaver doctor\n",
        "weaver fabric capacity status --resource-group parcel --capacity-name dev\n",
        "weaver fabric notebook run Parcel\n",
        "weaver fabric environment publish ParcelRuntime\n",
        "python -m pip install weaverstack\n",
    ):
        assert tool.compile_terminal(source, context=context()) == []


def test_mixed_terminal_procedure_stays_terminal_only():
    assert (
        generator().compile_terminal(
            "cp Parcel.tmdl saved.tmdl\nweaver build --item SemanticModel/Parcel\n",
            context=context(),
        )
        == []
    )


def test_destructive_operation_keeps_review_and_execution_separate():
    cells = generator().compile_terminal(
        "weaver wipe Warehouse/Operations --unbind --workspace-config workspace-development.yml\n",
        context=context(),
    )
    assert [cell["operation"] for cell in cells] == ["plan_wipe", "wipe"]
    assert "weaver.plan_wipe(" in cells[0]["code"]
    assert "wipe_plan.report()" in cells[0]["code"]
    assert "weaver.wipe(plan=wipe_plan)" in cells[1]["code"]
    assert "wipe_result.report()" in cells[1]["code"]


def test_capture_context_supplies_explicit_workspace_catalogue_and_mirror():
    text = """The command returned:\nWorkspace              Parcel Development\nSource catalogue       Warehouse/Catalogue\nDestination catalogue  Warehouse/CatalogueDev\n"""
    assert generator().capture_context(text) == {
        "workspace": "Parcel Development",
        "catalogue": "Warehouse/CatalogueDev",
        "mirror": "Warehouse/Catalogue",
    }


def test_collection_selects_only_captured_pure_core_operations(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    capture = '<!-- cli-capture: {"id": "unit"} -->\n<p class="terminal-intro">The command returned:</p>\n<figure><pre><code>Workspace  Parcel Development\nCatalogue  Warehouse/Catalogue\n</code></pre></figure>\n<!-- /cli-capture -->'
    (docs / "example.md").write_text(
        "```bash\nweaver load Warehouse/Operations --workspace-config workspace-development.yml\n```\n"
        + capture
        + "\n```bash\nweaver doctor\n```\n"
        + capture
    )
    examples = generator().collect_examples(docs)
    assert len(examples) == 1
    assert examples[0]["cells"][0]["operation"] == "load"
    assert "workspace_config" not in examples[0]["cells"][0]["code"]


def test_uncaptured_initialise_is_selected_on_a_task_page_but_not_cli_reference(
    tmp_path,
):
    docs = tmp_path / "docs"
    (docs / "lakehouse").mkdir(parents=True)
    (docs / "reference/cli").mkdir(parents=True)
    source = '```bash\nweaver initialise --workspace "Parcel Development" --project-folder ./parcel --lakehouse Landing\n```\n'
    (docs / "lakehouse/python.md").write_text(source)
    (docs / "reference/cli/initialise.md").write_text(source)
    (entry,) = generator().collect_examples(docs)
    assert entry["page"] == "lakehouse/python.md"
    assert entry["cells"][0]["operation"] == "initialise"


def test_page_context_fills_an_observed_core_result_without_context_lines(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    contextual = '<!-- cli-capture: {"id": "context"} -->\n<figure><pre><code>Workspace  Parcel Development\nCatalogue  Warehouse/Catalogue\n</code></pre></figure>\n<!-- /cli-capture -->'
    result_only = '<!-- cli-capture: {"id": "health"} -->\n<figure><pre><code>Health green</code></pre></figure>\n<!-- /cli-capture -->'
    (docs / "example.md").write_text(
        "```bash\nweaver check\n```\n"
        + contextual
        + "\n```bash\nweaver health --workspace-config workspace-development.yml\n```\n"
        + result_only
    )
    (entry,) = generator().collect_examples(docs)
    assert "workspace='Parcel Development'" in entry["cells"][0]["code"]
    assert "catalogue='Warehouse/Catalogue'" in entry["cells"][0]["code"]


def test_each_configuration_in_one_block_gets_its_own_explicit_workspace():
    cells = generator().compile_terminal(
        "weaver load SemanticModel/Parcel --workspace-config workspace-development.yml\n"
        "weaver load SemanticModel/Parcel --workspace-config workspace-production.yml\n",
        context={},
        configuration_contexts={
            "workspace-development.yml": {"workspace": "Parcel Development"},
            "workspace-production.yml": {"workspace": "Parcel Production"},
        },
    )
    assert "workspace='Parcel Development'" in cells[0]["code"]
    assert "workspace='Parcel Production'" in cells[1]["code"]


def test_current_manifest_contains_only_bound_core_calls():
    import weaver

    payload = json.loads((ROOT / "notebook-examples.json").read_text())
    assert payload["examples"]
    for entry in payload["examples"]:
        if not entry["cli_captures"]:
            assert all(cell["operation"] == "initialise" for cell in entry["cells"])
        assert entry["context"].get("workspace") or all(
            cell["operation"] == "initialise" for cell in entry["cells"]
        )
        assert entry["cells"]
        for cell in entry["cells"]:
            assert cell["operation"].removeprefix("plan_") in NATURAL
            tree = ast.parse(cell["code"])
            assert "workspace_config" not in cell["code"]
            assert ".to_mapping()" not in cell["code"]
            assert ".as_dict()" not in cell["code"]
            assert ".report()" in cell["code"] or "print(" in cell["code"]
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "weaver"
                    and hasattr(weaver, node.func.attr)
                ):
                    inspect.signature(getattr(weaver, node.func.attr)).bind(
                        *[None for _ in node.args],
                        **{keyword.arg: None for keyword in node.keywords},
                    )
    for page in ("lakehouse/python.md", "warehouse/first-project.md"):
        cells = [
            cell
            for entry in payload["examples"]
            if entry["page"] == page
            for cell in entry["cells"]
            if cell["operation"] != "initialise"
        ]
        assert cells and all(
            "catalogue='Warehouse/Catalogue'" in cell["code"] for cell in cells
        )
    initialise = [
        cell
        for entry in payload["examples"]
        for cell in entry["cells"]
        if cell["operation"] == "initialise"
    ]
    assert len(initialise) >= 2
    assert sum("output" in cell for cell in initialise) == 2


def test_recorded_output_requires_the_exact_cell_source(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    capture = '<!-- cli-capture: {"id": "unit"} -->\n<figure><pre><code>Workspace  Parcel Development\nCatalogue  Warehouse/Catalogue\n</code></pre></figure>\n<!-- /cli-capture -->'
    (docs / "example.md").write_text(
        "```bash\nweaver health --workspace-config workspace-development.yml\n```\n"
        + capture
    )
    manifest = tmp_path / "notebook-examples.json"
    tool = generator()
    args = [
        "--weaver-checkout",
        str(ROOT.parent / "runtime"),
        "--docs",
        str(docs),
        "--output",
        str(manifest),
    ]
    tool.main([*args, "--write"])
    payload = json.loads(manifest.read_text())
    entry = payload["examples"][0]
    observations = tmp_path / "observations.json"
    observed = {
        "example_id": entry["id"],
        "cell": 0,
        "source": entry["cells"][0]["code"],
        "output": "Unit fixture\n",
        "error_type": None,
        "host": "IPython",
    }
    observations.write_text(
        json.dumps(
            {
                "runtime_revision": payload["runtime_revision"],
                "observations": [observed],
            }
        )
    )
    tool.main([*args, "--write", "--observations", str(observations)])
    assert (
        json.loads(manifest.read_text())["examples"][0]["cells"][0]["output"]
        == "Unit fixture\n"
    )
    observed["source"] = "different code\n"
    observations.write_text(
        json.dumps(
            {
                "runtime_revision": payload["runtime_revision"],
                "observations": [observed],
            }
        )
    )
    import pytest

    with pytest.raises(ValueError, match="source"):
        tool.main([*args, "--write", "--observations", str(observations)])


def test_canonical_spelling_does_not_relabel_the_source_that_was_executed():
    tool = generator()
    examples = [
        {
            "id": "one",
            "terminal": "weaver health\n",
            "cli_captures": ["capture"],
            "cells": [{"operation": "health", "code": "new spelling\n"}],
        }
    ]
    previous = json.dumps(
        {
            "examples": [
                {
                    "id": "one",
                    "terminal": "weaver health\n",
                    "cells": [
                        {
                            "operation": "health",
                            "code": "executed spelling\n",
                            "output": "observed\n",
                            "observation": {
                                "capture_id": "capture",
                                "captured_source_sha256": "original-evidence-hash",
                            },
                        }
                    ],
                }
            ]
        }
    )
    tool._carry_observed_outputs(examples, previous)
    assert (
        examples[0]["cells"][0]["observation"]["captured_source_sha256"]
        == "original-evidence-hash"
    )


def test_carried_output_stays_with_the_matching_operation_parameters():
    tool = generator()
    examples = [
        {
            "id": "one",
            "terminal": "two loads\n",
            "cli_captures": ["capture"],
            "cells": [
                {
                    "operation": "load",
                    "parameters": {"dry_run": True, "workspace": "Development"},
                    "code": "preview\n",
                },
                {
                    "operation": "load",
                    "parameters": {"workspace": "Development"},
                    "code": "execution\n",
                },
            ],
        }
    ]
    previous = json.dumps(
        {
            "examples": [
                {
                    "id": "one",
                    "terminal": "two loads\n",
                    "cells": [
                        {
                            "operation": "load",
                            "parameters": {
                                "dry_run": True,
                                "workspace_config": "workspace-development.yml",
                            },
                            "code": "old preview\n",
                            "output": "preview output\n",
                            "observation": {"capture_id": "capture"},
                        }
                    ],
                }
            ]
        }
    )
    tool._carry_observed_outputs(examples, previous)
    assert examples[0]["cells"][0]["output"] == "preview output\n"
    assert "output" not in examples[0]["cells"][1]
