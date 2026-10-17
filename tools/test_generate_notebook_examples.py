"""Notebook cells retain terminal selections and workspace configuration."""

import ast
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generator():
    spec = importlib.util.spec_from_file_location(
        "generate_notebook_examples", ROOT / "tools/generate_notebook_examples.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_native_load_retains_cli_selection_and_scope_parameters():
    cell = generator().compile_command(
        "weaver load Warehouse/Operations --name 'Parcel[.]Events' --ancestors --dry-run --workspace-config workspace-development.yml"
    )
    tree = ast.parse(cell["code"])
    call = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "weaver"
        and node.func.attr == "load"
    )
    parameters = {keyword.arg: keyword.value for keyword in call.keywords}
    assert ast.literal_eval(parameters["items"]) == ["Warehouse/Operations"]
    assert ast.literal_eval(parameters["names"]) == ["Parcel[.]Events"]
    assert ast.literal_eval(parameters["ancestors"]) is True
    assert ast.literal_eval(parameters["dry_run"]) is True
    assert (
        ast.literal_eval(parameters["workspace_config"]) == "workspace-development.yml"
    )
    assert isinstance(parameters["workspace"], ast.Name)
    assert parameters["workspace"].id == "workspace"
    assert "weaver_cli" not in cell["code"]
    assert "subprocess" not in cell["code"]


def test_explicit_workspace_does_not_discard_the_clis_implicit_configuration():
    cell = generator().compile_command("weaver load Warehouse/Operations")
    tree = ast.parse(cell["code"])
    call = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "load"
    )
    parameters = {keyword.arg: keyword.value for keyword in call.keywords}
    assert ast.literal_eval(parameters["workspace_config"]) == "workspace-config.yml"
    assert "workspace_config=" in cell["workspace_expression"]


def test_output_assessment_covers_the_exact_current_native_cells():
    import hashlib
    import json

    manifest = json.loads((ROOT / "notebook-examples.json").read_text())
    audit = json.loads((ROOT / "generated/notebook-output-audit.json").read_text())
    assert audit["runtime_revision"] == manifest["runtime_revision"]
    expected = [
        (
            entry["id"],
            index,
            cell["operation"],
            hashlib.sha256(cell["code"].encode()).hexdigest(),
            "captured"
            if "output" in cell
            else "source/type audited; no static execution output claimed",
        )
        for entry in manifest["examples"]
        for index, cell in enumerate(entry["cells"])
    ]
    assert [
        (
            row["example_id"],
            row["cell"],
            row["operation"],
            row["source_sha256"],
            row["handling"],
        )
        for row in audit["entries"]
    ] == expected
    assert all(row["surface"] for row in audit["entries"])
    assert audit["cells"] == len(expected)
    assert audit["captured_cells"] == sum(row[-1] == "captured" for row in expected)


def test_source_check_cell_runs_against_an_actual_project(tmp_path, capsys):
    from shutil import copytree

    product = ROOT.parent / "runtime"
    project = tmp_path / "project"
    copytree(product / "tests/fixtures/build-lakehouse-item", project)
    cell = generator().compile_command(f"weaver check '{project.as_posix()}'")
    exec(compile(cell["code"], "<generated-notebook-cell>", "exec"), {})  # noqa: S102 — execute the generated cell against the real fixture
    assert "Checked " in capsys.readouterr().out


def test_management_cells_use_their_existing_result_surfaces():
    environment = generator().compile_command(
        'weaver fabric environment publish ParcelRuntime --workspace "Parcel Development"'
    )
    assert "publish_environment_result.as_dict()" in environment["code"]
    capacity = generator().compile_command(
        "weaver fabric capacity status --resource-group parcel-platform --capacity-name parceldev --subscription-id 00000000-0000-0000-0000-000000000000"
    )
    assert "print(capacity_result)" in capacity["code"]


def test_shell_setup_and_file_commands_become_native_notebook_cells():
    cells = generator().compile_terminal(
        "python -m pip install --upgrade weaverstack\ncd parcel\ncp PowerBI/Parcel/Parcel.tmdl Parcel.tmdl.saved\nmv Parcel.tmdl.saved PowerBI/Parcel/Parcel.tmdl\n",
        language="bash",
    )
    assert cells[0]["code"] == "%pip install --upgrade weaverstack\n"
    assert "os.chdir('parcel')" in cells[1]["code"]
    assert "shutil.copy(" in cells[2]["code"]
    assert "shutil.move(" in cells[3]["code"]
    for cell in cells[1:]:
        ast.parse(cell["code"])


def test_cli_inspection_has_native_python_inspection_cells():
    synopsis = generator().compile_terminal(
        "weaver build [-h] [--item ITEM] [SOURCE]\n", language="text"
    )
    assert "help(weaver.build)" in synopsis[0]["code"]
    version = generator().compile_terminal("weaver --version\n", language="bash")
    assert "print(weaver.__version__)" in version[0]["code"]
    generic = generator().compile_terminal("weaver <command> --help\n", language="bash")
    assert "sorted(weaver.__all__)" in generic[0]["code"]
    assert "help(weaver)" not in generic[0]["code"]


def test_interactive_cli_commands_reuse_one_explicit_notebook_session():
    source = "$ weaver session --workspace-config workspace-development.yml --timings\nweaver> build ./parcel-operations\nweaver> load Warehouse/Operations\nweaver> exit\n"
    cells = generator().compile_terminal(source, language="console")
    assert "session = weaver.session(" in cells[0]["code"]
    assert "session=session" in cells[1]["code"]
    assert "workspace = session.workspace.workspace" in cells[1]["code"]
    assert "workspace-config.yml" not in cells[1]["code"]
    assert "session.close()" in cells[-1]["code"]
    assert "session.telemetry.to_mapping()" in cells[-1]["code"]
    for cell in cells:
        ast.parse(cell["code"])


def test_notebook_setup_uses_host_identity_and_explicit_initialise_inputs():
    login = generator().compile_terminal("az login\n")
    assert "weaver.current_workspace()" in login[0]["code"]
    assert "getToken" not in login[0]["code"]
    initial = generator().compile_terminal("weaver initialise\n")
    assert "project_folder='./parcel'" in initial[0]["code"]
    assert "workspace=workspace" in initial[0]["code"]


def test_qualified_environment_publication_names_its_owner_explicitly():
    cell = generator().compile_command(
        'weaver fabric environment publish "Platform Runtimes/ParcelRuntime"'
    )
    assert cell["workspace_expression"] == repr("Platform Runtimes")
    assert "workspace_config=" not in cell["code"]
    assert "environment='Platform Runtimes/ParcelRuntime'" in cell["code"]


def test_destructive_cli_review_is_not_collapsed_into_an_automatic_notebook_run():
    source = (
        'weaver wipe Warehouse/ParcelOperations_Dev --workspace "Parcel Development"'
    )
    cells = generator().compile_terminal(source)
    assert len(cells) == 2
    assert "weaver.plan_wipe(" in cells[0]["code"]
    assert "workspace=workspace" in cells[0]["code"]
    assert "weaver.wipe(plan=wipe_plan)" in cells[1]["code"]
    assert len(generator().compile_terminal(source + " --yes")) == 1
    assert len(generator().compile_terminal(source + " --dry-run")) == 1
    interactive = generator().compile_terminal(
        '$ weaver session --workspace "Parcel Development"\nweaver> wipe Warehouse/Operations\n'
    )
    assert "weaver.wipe(plan=wipe_plan, session=session)" in interactive[-1]["code"]


def test_every_documented_terminal_block_has_syntax_valid_public_cells():
    import inspect

    import weaver

    examples = generator().collect_examples(ROOT / "docs")
    assert len(examples) == 232
    assert len({(entry["page"], entry["ordinal"]) for entry in examples}) == len(
        examples
    )
    for entry in examples:
        assert entry["cells"], (entry["page"], entry["ordinal"])
        for cell in entry["cells"]:
            code = cell["code"]
            if code.startswith("%pip"):
                continue
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    assert not (node.module or "").startswith(
                        ("weaver.operations", "weaver_cli")
                    )
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "weaver"
                ):
                    function = getattr(weaver, node.func.attr)
                    inspect.signature(function).bind(
                        *[None for _ in node.args],
                        **{kw.arg: None for kw in node.keywords},
                    )


def test_generator_writes_a_manifest_that_can_be_checked(tmp_path):
    import json

    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "example.md").write_text("```bash\nweaver check\n```\n")
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
    assert len(payload["examples"]) == 1
    assert payload["examples"][0]["cells"][0]["operation"] == "check"
    payload["examples"][0]["cells"][0]["output"] = "Unit fixture output\n"
    manifest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    tool.main([*args, "--check"])


def test_capacity_cells_name_the_arm_identity_and_subscription():
    tool = generator()
    cell = tool.compile_command(
        "weaver fabric capacity status --resource-group parcel-platform --capacity-name parcel-development"
    )
    assert "DeviceCodeCredential" in cell["code"]
    assert "credential=capacity_credential" in cell["code"]
    assert "subscription_id=subscription_id" in cell["code"]
    assert "FABRIC_SUBSCRIPTION_ID" in cell["code"]
    unattended = tool.compile_command(
        "weaver fabric capacity status --resource-group parcel-platform --capacity-name parcel-development --non-interactive"
    )
    assert "DeviceCodeCredential" not in unattended["code"]
    assert "DefaultAzureCredential" in unattended["code"]


def test_recorded_output_requires_the_exact_cell_source(tmp_path):
    import json

    import pytest

    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "example.md").write_text("```bash\nweaver check\n```\n")
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
    with pytest.raises(ValueError, match="source"):
        tool.main([*args, "--write", "--observations", str(observations)])


def test_authored_notebook_operations_also_name_the_workspace():
    import re
    import textwrap

    scoped = {
        "initialise",
        "build",
        "load",
        "test",
        "health",
        "session",
        "workflow",
        "mirror",
        "wipe",
        "doctor",
        "push_notebook",
        "run_notebook",
        "publish_environment",
    }
    for path in (ROOT / "docs").rglob("*.md"):
        for fence in re.finditer(
            r"(?ms)^ *```python[^\n]*\n(.*?)^ *```", path.read_text()
        ):
            try:
                tree = ast.parse(textwrap.dedent(fence[1]))
            except SyntaxError:
                continue  # Generated reference signatures are not executable cells.
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "weaver"
                    and node.func.attr in scoped
                ):
                    assert any(
                        keyword.arg == "workspace" for keyword in node.keywords
                    ), (path, node.func.attr)


def test_mirror_review_uses_the_existing_resolved_plan_display():
    cells = generator().compile_terminal(
        "weaver mirror --workspace-config workspace-mirror.yml"
    )
    assert "weaver.check_mirror(mirror_plan)" in cells[0]["code"]
    assert "print(mirror_plan.describe())" in cells[0]["code"]
    assert "weaver.mirror(plan=mirror_plan)" in cells[1]["code"]


def test_workflow_confirmation_becomes_a_separate_review_cell():
    tool = generator()
    cells = tool.compile_terminal(
        "weaver workflow daily --file workflow-production.yml"
    )
    assert len(cells) == 2
    assert "workflow-production.yml" in cells[0]["code"]
    assert "['workflows']['daily']" in cells[0]["code"]
    assert "weaver.workflow(" in cells[1]["code"]
    assert (
        len(
            tool.compile_terminal(
                "weaver workflow daily --file workflow-production.yml --yes"
            )
        )
        == 1
    )
