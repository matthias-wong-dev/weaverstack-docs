#!/usr/bin/env python3
"""Check Reference commands, configuration and native/DAX examples offline."""

from __future__ import annotations

import argparse
import ast
import inspect
import re
import shlex
import sys
from pathlib import Path


def blocks(path, language):
    # Parser-owned pseudo-signatures are not executable code samples.
    text = re.sub(
        r"<!-- BEGIN GENERATED.*?<!-- END GENERATED[^>]*-->",
        "",
        path.read_text(),
        flags=re.DOTALL,
    )
    return re.findall(
        r"^```" + language + r"[^\n]*\n(.*?)^```", text, re.MULTILINE | re.DOTALL
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-checkout", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    source = args.weaver_checkout.resolve() / "src"
    sys.path.insert(0, str(source))
    import weaver
    import yaml
    from weaver.config import parse_workspace
    from weaver.declaration import read_source_document
    from weaver.semantic_models.objects import TmdlDefinition
    from weaver_cli.main import build_parser

    assert weaver.__file__ and Path(weaver.__file__).resolve().is_relative_to(source)
    cli = build_parser()
    counts = {
        "commands": 0,
        "configurations": 0,
        "operation_calls": 0,
        "dax_files": 0,
        "native_edits": 0,
    }
    for page in sorted((args.root / "docs/reference").rglob("*.md")):
        for block in blocks(page, "bash"):
            for line in block.replace("\\\n", " ").splitlines():
                if not line.startswith("weaver ") or "<command>" in line:
                    continue
                cli.parse_args(shlex.split(line)[1:])
                counts["commands"] += 1
        for block in blocks(page, "yaml"):
            raw = yaml.safe_load(block)
            if isinstance(raw, dict) and "workspace" in raw:
                parse_workspace(raw)
                counts["configurations"] += 1
            if isinstance(raw, dict) and "workflows" in raw:
                for entries in raw["workflows"].values():
                    for entry in entries:
                        words = shlex.split(entry)
                        cli.parse_args(words[1:] if words[0] == "weaver" else words)
                        counts["commands"] += 1
        for block in blocks(page, "python"):
            try:
                tree = ast.parse(block)
            except SyntaxError:
                # Constructor/method signature display, not a runnable module.
                continue
            for call in ast.walk(tree):
                if (
                    not isinstance(call, ast.Call)
                    or not isinstance(call.func, ast.Attribute)
                    or not isinstance(call.func.value, ast.Name)
                    or call.func.value.id != "weaver"
                ):
                    continue
                target = getattr(weaver, call.func.attr, None)
                if target is None:
                    raise ValueError(f"{page}: unknown weaver.{call.func.attr}")
                signature = inspect.signature(target)
                for keyword in call.keywords:
                    if keyword.arg and keyword.arg not in signature.parameters:
                        raise ValueError(
                            f"{page}: unsupported {call.func.attr} keyword {keyword.arg}"
                        )
                counts["operation_calls"] += 1
        for block in blocks(page, "dax"):
            match = re.search(r"(Assumption|Test) ID: (\S+)", block)
            if match:
                kind, name = match.groups()
                directory = "assumptions" if kind == "Assumption" else "tests"
                read_source_document(
                    f"SemanticModel/Parcel/{directory}/{name}.dax",
                    block.encode(),
                    "SemanticModel",
                )
                counts["dax_files"] += 1
    page = args.root / "docs/reference/python/semantic-models.md"
    sample = next(
        block for block in blocks(page, "python") if block.startswith("parts =")
    )
    namespace = {"TmdlDefinition": TmdlDefinition}
    exec(compile(sample, str(page), "exec"), namespace)  # noqa: S102 - checked local documentation sample
    model = namespace["definition"].model
    assert model.tables["Metrics"].measures["Deliveries"].expression == "1"
    assert model.tables["Metrics"].measures["Deliveries"].formatString == "0"
    counts["native_edits"] += 1
    print("Validated against", weaver.__file__)
    print(counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
