"""Compile selected engineering commands into natural public Python calls."""

from __future__ import annotations

import hashlib
import inspect
import json
import re
import shlex
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from textwrap import dedent

NATURAL_OPERATIONS = {
    "initialise",
    "build",
    "load",
    "test",
    "health",
    "mirror",
    "wipe",
}
NOTEBOOK_PROJECT = "builtin/project"
PAGE_CONTEXT = {
    # The page continues the Parcel estate established by the preceding guide;
    # its compact Health outputs do not repeat these two values.
    "estate/catalogue-and-health.md": {
        "workspace": "Parcel Development",
        "catalogue": "Warehouse/Catalogue",
    },
    "lakehouse/python.md": {
        "workspace": "Parcel Development",
        "catalogue": "Warehouse/Catalogue",
    },
    "warehouse/first-project.md": {
        "workspace": "Parcel Development",
        "catalogue": "Warehouse/Catalogue",
    },
}
PAGE_CONFIGURATION_CONTEXTS = {
    "reports/environments.md": {
        "workspace-development.yml": {"workspace": "Parcel Development"},
        "workspace-production.yml": {"workspace": "Parcel Production"},
    }
}
REMOVED_CLI_FIELDS = {
    "command",
    "handler",
    "requires",
    "lakehouses",
    "extra_items",
    "no_inventory",
    "mirror_source",
    "json",
    "yes",
    "non_interactive",
    "interactive",
    "workspace_config",
    "retired_target",
}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def _plain_text(value):
    reader = _Text()
    reader.feed(value)
    return unescape("".join(reader.parts) if reader.parts else value)


def _line_value(text, label):
    match = re.search(rf"(?m)^\s*{re.escape(label)}\s{{2,}}([^\n]+?)\s*$", text)
    return match[1].strip() if match else None


def capture_context(capture):
    """Read explicit operation parameters from the observed result context."""

    text = _plain_text(capture)
    workspace = _line_value(text, "Workspace")
    if workspace is None:
        match = re.search(r"(?m)^Wipe on (.+?)\s*$", text)
        workspace = match[1].strip() if match else None
    catalogue = _line_value(text, "Catalogue")
    source = _line_value(text, "Source catalogue")
    destination = _line_value(text, "Destination catalogue")
    if catalogue is None:
        match = re.search(
            r"(?m)^\s*(Warehouse/[^\s]+)\s+catalogue (?:preserved|emptied)", text
        )
        catalogue = match[1] if match else None
    result = {}
    if workspace:
        result["workspace"] = workspace
    if destination:
        result["catalogue"] = destination
    elif catalogue and catalogue.casefold() != "none":
        result["catalogue"] = catalogue.split(" → ")[-1].strip()
    if source:
        result["mirror"] = source
    return result


def _parse_command(command):
    words = shlex.split(command)
    if len(words) < 2 or words[0] != "weaver" or words[1] not in NATURAL_OPERATIONS:
        return None
    from weaver_cli.main import build_parser

    parsed = build_parser().parse_args(words[1:])
    return parsed


def _operation_values(parsed, function, *, context):
    name = parsed.command
    values = vars(parsed).copy()
    if values.get("extra_items"):
        values["items"] = [*(values.get("items") or []), *values["extra_items"]]
    if name == "health":
        values["inventories"] = not values.get("no_inventory", False)
    if name == "mirror":
        values["mirror"] = values.get("mirror_source")
    if name == "initialise":
        values["project_folder"] = NOTEBOOK_PROJECT
    elif (
        name in {"build", "load", "test"}
        and "source" in inspect.signature(function).parameters
        and values.get("source") in {None, "."}
    ):
        values["source"] = NOTEBOOK_PROJECT
    for key in REMOVED_CLI_FIELDS:
        values.pop(key, None)

    signature = inspect.signature(function)
    for key in ("workspace", "catalogue", "environment"):
        if key in signature.parameters and values.get(key) is None and context.get(key):
            values[key] = context[key]
    if name == "mirror" and values.get("mirror") is None and context.get("mirror"):
        values["mirror"] = context["mirror"]

    unsupported = {
        key
        for key, value in values.items()
        if value is not None and key not in signature.parameters
    }
    if unsupported:
        raise ValueError(
            f"{name} has no matching Python parameter for "
            + ", ".join(sorted(unsupported))
        )
    parameters = {}
    for key, parameter in signature.parameters.items():
        value = values.get(key)
        if value is None:
            continue
        if (
            parameter.default is not inspect.Parameter.empty
            and value == parameter.default
        ):
            continue
        parameters[key] = value
    signature.bind(**parameters)
    return parameters


def _call_code(operation, parameters, *, variable=None):
    variable = variable or operation + "_result"
    uses_project = any(
        key in {"source", "project_folder"} and value == NOTEBOOK_PROJECT
        for key, value in parameters.items()
    )
    lines = ["import weaver"]
    if uses_project:
        lines = [
            "from pathlib import Path",
            "",
            "import weaver",
            "",
            'project = Path("builtin") / "project"',
        ]
    lines.append(f"{variable} = weaver.{operation}(")
    lines.extend(
        f"    {key}={'project' if key in {'source', 'project_folder'} and value == NOTEBOOK_PROJECT else repr(value)},"
        for key, value in parameters.items()
    )
    lines.extend([")", f"{variable}.report()"])
    return "\n".join(lines) + "\n"


def compile_command(command, *, context=None):
    import weaver

    parsed = _parse_command(command)
    if parsed is None:
        return None
    operation = parsed.command
    function = getattr(weaver, operation)
    parameters = _operation_values(parsed, function, context=context or {})
    return {
        "operation": operation,
        "parameters": parameters,
        "requires_review": operation in {"wipe", "mirror"}
        and not getattr(parsed, "yes", False)
        and not getattr(parsed, "dry_run", False),
        "code": _call_code(operation, parameters),
    }


def _commands(source):
    return [
        line.strip().removeprefix("$ ")
        for line in dedent(source).replace("\\\n", " ").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _review_cells(cell):
    operation = cell["operation"]
    if not cell["requires_review"]:
        return [cell]
    parameters = cell["parameters"]
    plan_name = operation + "_plan"
    lines = [
        "import weaver",
        f"{plan_name} = weaver.plan_{operation}(",
        *(f"    {key}={value!r}," for key, value in parameters.items()),
        ")",
    ]
    if operation == "mirror":
        lines.extend(
            [
                f"{plan_name} = weaver.check_mirror({plan_name})",
                f"print({plan_name}.describe())",
            ]
        )
    else:
        lines.append(f"{plan_name}.report()")
    review = {
        **cell,
        "operation": "plan_" + operation,
        "code": "# Review this plan before running the next cell.\n"
        + "\n".join(lines)
        + "\n",
    }
    execute = {
        **cell,
        "parameters": {"plan": plan_name},
        "code": (
            f"import weaver\n{operation}_result = weaver.{operation}(plan={plan_name})\n"
            f"{operation}_result.report()\n"
        ),
    }
    return [review, execute]


def compile_terminal(
    source, *, language="bash", context=None, configuration_contexts=None
):
    del language  # Fence language affects presentation, not operation selection.
    commands = _commands(source)
    if (
        commands
        and commands[0].startswith("weaver initialise")
        and all(command.startswith("cd ") for command in commands[1:])
    ):
        commands = commands[:1]
    parsed = [_parse_command(command) for command in commands]
    if not commands or any(request is None for request in parsed):
        return []
    cells = []
    for command, request in zip(commands, parsed):
        effective_context = dict(context or {})
        configuration = getattr(request, "workspace_config", None)
        effective_context.update((configuration_contexts or {}).get(configuration, {}))
        cell = compile_command(command, context=effective_context)
        cells.extend(_review_cells(cell))
    return cells


def collect_examples(docs):
    from collections import defaultdict

    from notebook_presentation import CAPTURE, terminal_blocks

    recorded = []
    page_values = defaultdict(lambda: defaultdict(set))
    for path in sorted(docs.rglob("*.md")):
        page = path.relative_to(docs).as_posix()
        markdown = path.read_text()
        for ordinal, (match, language) in enumerate(terminal_blocks(markdown)):
            captured = []
            capture_blocks = []
            end = match.end()
            while capture := CAPTURE.match(markdown, end):
                spec = json.loads(
                    re.search(r"<!-- cli-capture: ([^\n]+) -->", capture[0])[1]
                )
                captured.append(spec["id"])
                capture_blocks.append(capture[0])
                end = capture.end()
            context = capture_context("\n".join(capture_blocks))
            if not captured and (
                page.startswith("reference/")
                or not re.search(r"(?m)^\s*weaver initialise(?:\s|$)", match["source"])
            ):
                continue
            for key, value in context.items():
                page_values[page][key].add(value)
            recorded.append((page, ordinal, match, language, captured, context))

    examples = []
    for page, ordinal, match, language, captured, context in recorded:
        context = {**PAGE_CONTEXT.get(page, {}), **context}
        for key, values in page_values[page].items():
            if key not in context and len(values) == 1:
                context[key] = next(iter(values))
        cells = compile_terminal(
            match["source"],
            language=language,
            context=context,
            configuration_contexts=PAGE_CONFIGURATION_CONTEXTS.get(page),
        )
        if not cells:
            continue
        identifier = hashlib.sha256(
            f"{page}:{ordinal}\0{match['source']}".encode()
        ).hexdigest()[:20]
        examples.append(
            {
                "id": identifier,
                "page": page,
                "ordinal": ordinal,
                "language": language,
                "terminal": match["source"],
                "cli_captures": captured,
                "context": context,
                "cells": cells,
            }
        )
    assert len({entry["id"] for entry in examples}) == len(examples)
    return examples


def _semantic_parameters(cell):
    parameters = dict(cell.get("parameters", {}))
    for key in ("workspace", "workspace_config", "catalogue", "environment"):
        parameters.pop(key, None)
    return parameters


def _carry_observed_outputs(examples, previous):
    if previous is None:
        return
    old = {entry["id"]: entry for entry in json.loads(previous).get("examples", [])}
    for entry in examples:
        prior = old.get(entry["id"])
        if prior is None or prior.get("terminal") != entry["terminal"]:
            continue
        captures = set(entry["cli_captures"])
        observed = [
            cell
            for cell in prior.get("cells", [])
            if "output" in cell
            and cell.get("observation", {}).get("capture_id") in captures
        ]
        for old_cell in observed:
            operation = old_cell["operation"]
            candidates = [
                cell
                for cell in entry["cells"]
                if cell["operation"] == operation and "output" not in cell
            ]
            if not candidates:
                continue
            matching = [
                cell
                for cell in candidates
                if _semantic_parameters(cell) == _semantic_parameters(old_cell)
            ]
            cell = (matching or candidates)[-1]
            cell["output"] = old_cell["output"]
            observation = dict(old_cell.get("observation", {}))
            observation.setdefault(
                "captured_source_sha256",
                hashlib.sha256(old_cell["code"].encode()).hexdigest(),
            )
            observation["display_source_sha256"] = hashlib.sha256(
                cell["code"].encode()
            ).hexdigest()
            observation["source_equivalence"] = (
                "Same public operation and observed target context; canonical cell uses "
                "explicit parameters and the report presentation alias."
            )
            cell["observation"] = observation


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
        "schema": 2,
        "runtime_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=checkout, text=True
        ).strip(),
        "examples": examples,
    }
    previous = args.output.read_text() if args.output.exists() else None
    _carry_observed_outputs(examples, previous)
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
        f"PASS: {len(examples)} selected Notebook examples contain "
        f"{sum(len(entry['cells']) for entry in examples)} cells"
    )


if __name__ == "__main__":
    main()
