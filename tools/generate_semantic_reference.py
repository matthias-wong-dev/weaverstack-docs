#!/usr/bin/env python3
"""Extract the supported semantic extension surface without importing project code."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

from generate_python_reference import _signature

BEGIN = "<!-- BEGIN GENERATED SEMANTIC PYTHON -->"
END = "<!-- END GENERATED SEMANTIC PYTHON -->"
PAGE = Path("docs/reference/python/semantic-models.md")
MANIFEST = Path("generated/semantic-reference.json")
# Explicit modules/classes prevent private compiler classes becoming public API.
CLASSES = (
    ("semantic_models.annotation", "Annotation"),
    ("semantic_models.objects", "TmdlDefinition"),
    ("semantic_models.objects", "TmdlObject"),
    ("semantic_models.objects", "TmdlCollection"),
)
PROTOCOLS = {
    "__init__",
    "__getitem__",
    "__setitem__",
    "__delitem__",
    "__iter__",
    "__len__",
    "__contains__",
}


def build_manifest(checkout: Path) -> dict:
    facts = []
    for module, name in CLASSES:
        path = checkout / "src/weaver" / Path(*module.split(".")).with_suffix(".py")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        definitions = [
            n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name
        ]
        if len(definitions) != 1:
            raise ValueError(f"{module}.{name}: expected one class")
        members = []
        for node in definitions[0].body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_") and node.name not in PROTOCOLS:
                    continue
                if node.name == "__init__" and name != "TmdlDefinition":
                    continue
                prop = any(
                    isinstance(d, ast.Name) and d.id == "property"
                    for d in node.decorator_list
                )
                members.append(
                    {
                        "name": node.name,
                        "kind": "property" if prop else "method",
                        "signature": _signature(node),
                    }
                )
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        members.append(
                            {
                                "name": target.id,
                                "kind": "attribute",
                                "default": ast.unparse(node.value)
                                if node.value
                                else None,
                            }
                        )
        names = [m["name"] for m in members]
        if len(names) != len(set(names)):
            raise ValueError(f"{module}.{name}: duplicate public member")
        facts.append(
            {
                "name": f"weaver.{module}.{name}",
                "members": sorted(members, key=lambda m: m["name"]),
            }
        )
    return {"schema_version": 1, "owner": str(PAGE), "classes": facts}


def render(manifest: dict) -> str:
    lines = [BEGIN, "", "## Supported extension signatures", ""]
    for fact in manifest["classes"]:
        lines += [f"### `{fact['name']}`", "", "```python"]
        short = fact["name"].rsplit(".", 1)[1]
        for member in fact["members"]:
            if member["kind"] == "attribute":
                lines.append(f"{short}.{member['name']} = {member['default']}")
            elif member["kind"] == "property":
                lines.append(f"{short}.{member['name']}  # property")
            else:
                lines.append(f"{short}.{member['name']}{member['signature']}")
        lines += ["```", ""]
    return "\n".join(lines + [END])


def update(root: Path, checkout: Path, *, write: bool) -> None:
    manifest = build_manifest(checkout)
    expected = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    page = root / PAGE
    text = page.read_text(encoding="utf-8")
    if (
        text.count(BEGIN) != 1
        or text.count(END) != 1
        or text.index(BEGIN) > text.index(END)
    ):
        raise ValueError(f"{PAGE}: expected one ordered marker pair")
    start, stop = text.index(BEGIN), text.index(END) + len(END)
    block = render(manifest)
    if write:
        (root / MANIFEST).parent.mkdir(parents=True, exist_ok=True)
        (root / MANIFEST).write_text(expected, encoding="utf-8")
        page.write_text(text[:start] + block + text[stop:], encoding="utf-8")
    elif (root / MANIFEST).read_text(encoding="utf-8") != expected or text[
        start:stop
    ] != block:
        raise ValueError("semantic extension reference drift; regenerate with --write")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--weaver-checkout", required=True, type=Path)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    try:
        update(args.root, args.weaver_checkout, write=args.write)
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"{'wrote' if args.write else 'validated'} 4 supported extension classes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
