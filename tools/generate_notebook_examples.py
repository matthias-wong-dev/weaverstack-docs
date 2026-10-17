"""Compile documented CLI requests into public Python calls."""

from __future__ import annotations

import hashlib
import inspect
import json
import re
import shlex
from pathlib import Path
from textwrap import dedent


def compile_command(command, *, session_name=None):
    from weaver.command_parser import build_parser
    from weaver.commandline import command_words
    from weaver.operations.workflow import operation_call

    parsed = build_parser().parse_args(command_words(command))
    if parsed.command in {"initialise", "initialize"} and parsed.project_folder is None:
        parsed.project_folder = "./parcel"
    operation, function, parameters = operation_call(parsed)
    signature = inspect.signature(function)
    parameters = parameters.copy()
    if (
        operation == "publish_environment"
        and not parameters.get("workspace")
        and not parameters.get("workspace_config")
        and parameters.get("environment")
    ):
        from weaver.workspaces import EnvironmentRef

        owner = EnvironmentRef.parse(parameters["environment"]).workspace
        if owner is not None:
            parameters["workspace"] = owner
    if (
        "workspace_config" in signature.parameters
        and session_name is None
        and not parameters.get("workspace")
        and not parameters.get("workspace_config")
    ):
        parameters["workspace_config"] = "workspace-config.yml"
    values = {
        key: repr(value)
        for key, value in parameters.items()
        if key not in signature.parameters or value != signature.parameters[key].default
    }
    lines = ["import weaver"]
    if operation == "capacity":
        credential_type = (
            "DefaultAzureCredential"
            if getattr(parsed, "non_interactive", False)
            else "DeviceCodeCredential"
        )
        lines.extend(
            [
                f"from azure.identity import {credential_type}",
                f"capacity_credential = {credential_type}()",
            ]
        )
        values["credential"] = "capacity_credential"
        if parameters.get("subscription_id") is None:
            lines.extend(
                ["import os", 'subscription_id = os.environ["FABRIC_SUBSCRIPTION_ID"]']
            )
            values["subscription_id"] = "subscription_id"
    workspace_expression = None
    if "workspace" in signature.parameters:
        if parameters.get("workspace") is not None:
            workspace_expression = repr(parameters["workspace"])
        elif session_name is not None:
            workspace_expression = f"{session_name}.workspace.workspace"
        elif parameters.get("workspace_config") is not None:
            workspace_expression = f"weaver.current_workspace(workspace_config={parameters['workspace_config']!r}).workspace"
        else:
            workspace_expression = "weaver.current_workspace().workspace"
        lines.append("workspace = " + workspace_expression)
        values["workspace"] = "workspace"
    if session_name is not None and "session" in signature.parameters:
        values["session"] = session_name
    variable = "session" if operation == "session" else operation + "_result"
    lines.append(f"{variable} = weaver.{operation}(")
    lines.extend(f"    {key}={value}," for key, value in values.items())
    output = f"{variable}.to_mapping()"
    if operation == "check":
        output = f'print(f"Checked {{{variable}.project_folder}}")'
    elif operation == "publish_environment":
        output = f"{variable}.as_dict()"
    elif operation == "capacity":
        output = f"print({variable})"
    elif operation == "session":
        output = "print(session.workspace.workspace)"
    lines.extend([")", output])
    return {
        "operation": operation,
        "parameters": parameters,
        "workspace_expression": workspace_expression,
        "timings": bool(getattr(parsed, "timings", False)),
        "requires_review": operation in {"wipe", "mirror", "unbind", "workflow"}
        and not getattr(parsed, "yes", False)
        and not getattr(parsed, "dry_run", False),
        "code": "\n".join(lines) + "\n",
    }


def compile_terminal(source, *, language="bash", state=None):
    state = {} if state is None else state
    cells = []
    for line in dedent(source).replace("\\\n", " ").splitlines():
        command = line.strip()
        if not command or command.startswith("#"):
            continue
        command = command.removeprefix("$ ")
        interactive = command.startswith("weaver>")
        if interactive:
            command = command[len("weaver>") :].strip()
            if command in {"exit", "quit"}:
                code = "session.close()\n"
                if state.get("timings"):
                    code += "session.telemetry.to_mapping()\n"
                cells.append({"operation": "session_exit", "code": code})
                state.clear()
                continue
            command = "weaver " + command
        words = shlex.split(command)
        if words[0] == "weaver":
            if words[1:] == ["--version"]:
                cells.append(
                    {
                        "operation": "version",
                        "code": "import weaver\nprint(weaver.__version__)\n",
                    }
                )
                continue
            if (language == "text" and not interactive) or "--help" in words:
                name = words[1] if len(words) > 1 else ""
                if name == "fabric":
                    area = words[2] if len(words) > 2 else ""
                    name = {
                        "capacity": "capacity",
                        "environment": "publish_environment",
                        "notebook": "run_notebook"
                        if "run" in words
                        else "push_notebook",
                    }.get(area, "")
                name = "initialise" if name == "initialize" else name
                import weaver

                target = (
                    f"weaver.{name}" if name and hasattr(weaver, name) else "weaver"
                )
                code = (
                    "import weaver\nprint('\\n'.join(sorted(weaver.__all__)))\n"
                    if target == "weaver"
                    else f"import weaver\nhelp({target})\n"
                )
                if not any(cell["code"] == code for cell in cells):
                    cells.append({"operation": "inspection", "code": code})
                continue
            cell = compile_command(
                command, session_name="session" if interactive else None
            )
            if cell["operation"] == "session":
                state.update({"session": True, "timings": cell["timings"]})
            if cell.get("requires_review") and cell["operation"] == "workflow":
                parameters = cell["parameters"]
                review = f"# Review these commands before running the next cell.\nfrom pathlib import Path\nimport yaml\ncommands = yaml.safe_load(Path({parameters.get('file', 'workflow.yml')!r}).read_text())['workflows'][{parameters['name']!r}]\nprint('\\n'.join(commands))\n"
                cells.append({"operation": "review_workflow", "code": review})
            elif cell.get("requires_review"):
                operation = cell["operation"]
                plan = operation + "_plan"
                review_code = (
                    cell["code"]
                    .replace(f"weaver.{operation}(", f"weaver.plan_{operation}(")
                    .replace(operation + "_result", plan)
                )
                if operation == "mirror":
                    reused = (
                        ", session=session" if "session=session" in cell["code"] else ""
                    )
                    review_code = review_code.replace(
                        f"{plan}.to_mapping()",
                        f"{plan} = weaver.check_mirror({plan}{reused})\nprint({plan}.describe())",
                    )
                cells.append(
                    {
                        **cell,
                        "operation": "plan_" + operation,
                        "code": "# Review this plan before running the next cell.\n"
                        + review_code,
                    }
                )
                reused = ", session=session" if interactive else ""
                cell = {
                    **cell,
                    "code": f"import weaver\n{operation}_result = weaver.{operation}(plan={plan}{reused})\n{operation}_result.to_mapping()\n",
                }
            cells.append(cell)
            continue
        if words[:3] == ["python", "-m", "pip"]:
            code = "%pip " + " ".join(shlex.quote(word) for word in words[3:]) + "\n"
        elif words == ["az", "login"]:
            code = "import weaver\nworkspace = weaver.current_workspace().workspace\nprint(workspace)\n"
        elif words[0] == "cd" and len(words) == 2:
            code = f"import os\nos.chdir({words[1]!r})\n"
        elif words[0] in {"cp", "mv"} and len(words) == 3:
            operation = "copy" if words[0] == "cp" else "move"
            code = f"import shutil\nshutil.{operation}({words[1]!r}, {words[2]!r})\n"
        else:
            raise ValueError(f"No native Notebook setup equivalent for {command!r}")
        cells.append({"operation": words[0], "code": code})
    return cells


def collect_examples(docs):
    from notebook_presentation import CAPTURE, terminal_blocks

    examples = []
    for path in sorted(docs.rglob("*.md")):
        page = path.relative_to(docs).as_posix()
        markdown = path.read_text()
        state = {}
        for ordinal, (match, language) in enumerate(terminal_blocks(markdown)):
            source = match["source"]
            identifier = hashlib.sha256(
                f"{page}:{ordinal}\0{source}".encode()
            ).hexdigest()[:20]
            captured = []
            end = match.end()
            while capture := CAPTURE.match(markdown, end):
                spec = json.loads(
                    re.search(r"<!-- cli-capture: ([^\n]+) -->", capture[0])[1]
                )
                captured.append(spec["id"])
                end = capture.end()
            examples.append(
                {
                    "id": identifier,
                    "page": page,
                    "ordinal": ordinal,
                    "language": language,
                    "terminal": source,
                    "cli_captures": captured,
                    "cells": compile_terminal(source, language=language, state=state),
                }
            )
    assert len({entry["id"] for entry in examples}) == len(examples)
    return examples


def main(argv=None):
    import argparse
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    parser.add_argument("--docs", type=Path, default=root / "docs")
    parser.add_argument("--output", type=Path, default=root / "notebook-examples.json")
    parser.add_argument("--observations", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    checkout = args.weaver_checkout.resolve()
    sys.path.insert(0, str(checkout / "src"))
    import weaver

    assert Path(weaver.__file__).resolve() == checkout / "src/weaver/__init__.py", (
        "Weaver imported from a different checkout"
    )
    examples = collect_examples(args.docs)
    payload = {
        "schema": 1,
        "runtime_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=checkout, text=True
        ).strip(),
        "examples": examples,
    }
    previous = args.output.read_text() if args.output.exists() else None
    if previous is not None:
        old = json.loads(previous)
        if old.get("runtime_revision") == payload["runtime_revision"]:
            observed = {entry["id"]: entry for entry in old["examples"]}
            for entry in examples:
                prior = observed.get(entry["id"], {})
                for cell, captured in zip(entry["cells"], prior.get("cells", [])):
                    if cell["code"] == captured["code"]:
                        for field in ("output", "observation"):
                            if field in captured:
                                cell[field] = captured[field]
    if args.observations:
        records = json.loads(args.observations.read_text())
        assert records["runtime_revision"] == payload["runtime_revision"], (
            "Capture runtime revision does not match"
        )
        by_id = {entry["id"]: entry for entry in examples}
        for record in records["observations"]:
            cell = by_id[record["example_id"]]["cells"][record["cell"]]
            if record["source"] != cell["code"]:
                raise ValueError(
                    "Notebook capture source does not match the generated cell"
                )
            cell["output"] = record["output"]
            cell["observation"] = {
                key: value
                for key, value in record.items()
                if key not in {"source", "output", "stderr", "example_id", "cell"}
            }
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if previous != rendered:
            args.output.write_text(rendered)
    else:
        assert previous == rendered, (
            "Notebook examples drifted; regenerate with --write"
        )
    print(
        f"PASS: {len(examples)} terminal blocks have {sum(len(entry['cells']) for entry in examples)} native Notebook cells"
    )


if __name__ == "__main__":
    main()
