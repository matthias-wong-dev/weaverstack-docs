#!/usr/bin/env python3
"""Generate and validate the public Python API reference from ``weaver.__all__``."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Sequence
from pathlib import Path
from typing import Any

BEGIN = "<!-- BEGIN GENERATED PYTHON -->"
END = "<!-- END GENERATED PYTHON -->"
DEFAULT_MANIFEST = Path("generated/python-reference.json")

# Every name in weaver.__all__ has one documentation owner. These are public
# exports, not every name that can be imported from an internal Weaver module.
OWNERSHIP: tuple[tuple[str, str], ...] = (
    ("__version__", "docs/reference/python/index.md"),
    ("initialise", "docs/reference/python/operations.md"),
    ("build", "docs/reference/python/operations.md"),
    ("mirror", "docs/reference/python/operations.md"),
    ("plan_mirror", "docs/reference/python/operations.md"),
    ("check_mirror", "docs/reference/python/operations.md"),
    ("plan_wipe", "docs/reference/python/operations.md"),
    ("wipe", "docs/reference/python/operations.md"),
    ("load", "docs/reference/python/operations.md"),
    ("test", "docs/reference/python/operations.md"),
    ("health", "docs/reference/python/operations.md"),
    ("session", "docs/reference/python/session.md"),
    ("Lakehouse", "docs/reference/python/session.md"),
    ("default_lakehouse", "docs/reference/python/session.md"),
    ("lakehouse_for", "docs/reference/python/session.md"),
    ("current_workspace", "docs/reference/python/session.md"),
    ("WeaverObject", "docs/reference/python/objects.md"),
    ("Shortcut", "docs/reference/python/objects.md"),
    ("Folder", "docs/reference/python/objects.md"),
    ("Table", "docs/reference/python/objects.md"),
    ("SparkSqlTable", "docs/reference/python/objects.md"),
    ("View", "docs/reference/python/objects.md"),
    ("Test", "docs/reference/python/validation.md"),
    ("Assumption", "docs/reference/python/validation.md"),
    ("SparkSqlTest", "docs/reference/python/validation.md"),
    ("SparkSqlAssumption", "docs/reference/python/validation.md"),
    ("InitialiseReport", "docs/reference/python/results.md"),
    ("FabricItemOutcome", "docs/reference/python/results.md"),
    ("ExampleOutcome", "docs/reference/python/results.md"),
    ("BuildResult", "docs/reference/python/results.md"),
    ("MirrorResult", "docs/reference/python/results.md"),
    ("MirrorPlan", "docs/reference/python/results.md"),
    ("WipePlan", "docs/reference/python/results.md"),
    ("WipeItemResult", "docs/reference/python/results.md"),
    ("WipeReport", "docs/reference/python/results.md"),
    ("WipeResult", "docs/reference/python/results.md"),
    ("LoadRunReport", "docs/reference/python/results.md"),
    ("LoadNodeReport", "docs/reference/python/results.md"),
    ("LoadMessage", "docs/reference/python/results.md"),
    ("LoadResult", "docs/reference/python/results.md"),
    ("ValidationRunReport", "docs/reference/python/results.md"),
    ("HealthReport", "docs/reference/python/results.md"),
    ("HealthSection", "docs/reference/python/results.md"),
    ("HealthFinding", "docs/reference/python/results.md"),
    ("LoadActivity", "docs/reference/python/results.md"),
    ("ValidationNodeReport", "docs/reference/python/results.md"),
    ("WeaverError", "docs/reference/python/errors.md"),
    ("CommandError", "docs/reference/python/errors.md"),
    ("ConfigError", "docs/reference/python/errors.md"),
    ("IdentityError", "docs/reference/python/errors.md"),
    ("ValidationError", "docs/reference/python/errors.md"),
)


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _public_exports(module: ast.Module) -> list[str]:
    assignments = [
        node
        for node in module.body
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        and any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in (
                node.targets if isinstance(node, ast.Assign) else [node.target]
            )
        )
    ]
    if len(assignments) != 1:
        raise ValueError("weaver.__init__ must assign __all__ exactly once")
    expression = assignments[0].value
    if expression is None:
        raise ValueError("weaver.__all__ must be a literal sequence of names")
    try:
        value = ast.literal_eval(expression)
    except (TypeError, ValueError) as exc:
        raise ValueError("weaver.__all__ must be a literal sequence of names") from exc
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(name, str) for name in value
    ):
        raise ValueError("weaver.__all__ must be a literal sequence of names")
    duplicates = sorted(name for name, count in Counter(value).items() if count != 1)
    if duplicates:
        raise ValueError(
            "weaver.__all__ contains duplicate names: " + ", ".join(duplicates)
        )
    return list(value)


def _ownership(entries: Sequence[tuple[str, str]]) -> dict[str, str]:
    counts = Counter(name for name, _page in entries)
    duplicates = sorted(name for name, count in counts.items() if count != 1)
    if duplicates:
        raise ValueError(
            "public exports assigned more than once: " + ", ".join(duplicates)
        )
    return dict(entries)


def _import_sources(module: ast.Module, module_name: str) -> dict[str, tuple[str, str]]:
    sources: dict[str, tuple[str, str]] = {}
    for node in module.body:
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if node.level:
            package = module_name.split(".")[:-1] if module_name != "__init__" else []
            keep = len(package) - (node.level - 1)
            if keep < 0:
                continue
            imported_module = ".".join([*package[:keep], node.module])
        elif node.module.startswith("weaver."):
            imported_module = node.module.removeprefix("weaver.")
        else:
            continue
        for alias in node.names:
            sources[alias.asname or alias.name] = (imported_module, alias.name)
    return sources


def _definition(module: ast.Module, name: str) -> ast.AST | None:
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == name:
                return node
        elif isinstance(node, ast.Assign):
            if any(
                isinstance(target, ast.Name) and target.id == name
                for target in node.targets
            ):
                return node
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
        ):
            return node
    return None


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    rendered = f"({ast.unparse(node.args)})"
    if node.returns is not None:
        rendered += f" -> {ast.unparse(node.returns)}"
    return rendered


def _fact(name: str, node: ast.AST) -> dict[str, str]:
    fact = {"name": name}
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        fact.update(kind="function", signature=_signature(node))
    elif isinstance(node, ast.ClassDef):
        fact["kind"] = "class"
    else:
        fact["kind"] = "value"
    return fact


def _source_path(source: Path, module: str) -> Path:
    parts = module.split(".")
    file_path = source.joinpath("weaver", *parts).with_suffix(".py")
    if file_path.is_file():
        return file_path
    package_path = source.joinpath("weaver", *parts, "__init__.py")
    if package_path.is_file():
        return package_path
    raise ValueError(f"source module for public export is absent: weaver.{module}")


def _resolve_definition(
    source: Path,
    module_name: str,
    name: str,
    parsed: dict[str, ast.Module],
    trail: tuple[tuple[str, str], ...] = (),
) -> ast.AST:
    key = (module_name, name)
    if key in trail:
        chain = " -> ".join(f"weaver.{module}.{symbol}" for module, symbol in trail)
        raise ValueError(f"cyclic public export alias: {chain}")
    if module_name not in parsed:
        parsed[module_name] = _parse(_source_path(source, module_name))
    module = parsed[module_name]
    node = _definition(module, name)
    if node is not None:
        return node
    imported = _import_sources(module, module_name)
    imported_name = imported.get(name)
    if imported_name is None:
        raise ValueError(
            f"public export {name} has no inspectable definition in weaver.{module_name}"
        )
    origin, original_name = imported_name
    return _resolve_definition(source, origin, original_name, parsed, (*trail, key))


def build_manifest(
    checkout: Path, *, ownership: Sequence[tuple[str, str]] = OWNERSHIP
) -> dict[str, Any]:
    source = checkout.resolve() / "src"
    init_path = source / "weaver" / "__init__.py"
    if not init_path.is_file():
        raise ValueError(f"Weaver public module not found: {init_path}")
    public_module = _parse(init_path)
    exports = _public_exports(public_module)
    owners = _ownership(ownership)
    live, assigned = set(exports), set(owners)
    unassigned = sorted(live - assigned)
    retired = sorted(assigned - live)
    if unassigned:
        raise ValueError("public exports are unassigned: " + ", ".join(unassigned))
    if retired:
        raise ValueError("retired public exports remain owned: " + ", ".join(retired))

    imported = _import_sources(public_module, "__init__")
    parsed: dict[str, ast.Module] = {"__init__": public_module}
    facts = []
    for name in sorted(exports):
        module_name, original_name = imported.get(name, ("__init__", name))
        node = _resolve_definition(source, module_name, original_name, parsed)
        facts.append(_fact(name, node))

    return {
        "schema_version": 1,
        "export_count": len(facts),
        "page_count": len(set(owners.values())),
        "ownership": owners,
        "exports": facts,
    }


def render_page(facts: list[dict[str, str]]) -> str:
    if not facts:
        raise ValueError("cannot render a page without public exports")
    lines = [BEGIN, "", "## Public exports", ""]
    for fact in sorted(facts, key=lambda item: item["name"]):
        name = fact["name"]
        lines.extend([f"### `weaver.{name}`", ""])
        if fact["kind"] == "function":
            lines.extend(["```python", f"weaver.{name}{fact['signature']}", "```", ""])
        else:
            lines.extend([f"Kind: {fact['kind']}", ""])
    while lines and not lines[-1]:
        lines.pop()
    lines.extend(["", END])
    return "\n".join(lines)


def _facts_by_page(manifest: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    by_name = {fact["name"]: fact for fact in manifest["exports"]}
    pages: dict[str, list[dict[str, str]]] = defaultdict(list)
    for name, page in manifest["ownership"].items():
        pages[page].append(by_name[name])
    return dict(sorted(pages.items()))


def _replace_block(page: Path, generated: str) -> bool:
    text = page.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"{page}: expected exactly one generated Python block")
    updated = pattern.sub(generated, text)
    if updated == text:
        return False
    page.write_text(updated, encoding="utf-8")
    return True


def _manifest_text(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write(
    root: Path,
    checkout: Path,
    manifest_path: Path,
    *,
    ownership: Sequence[tuple[str, str]] = OWNERSHIP,
) -> tuple[int, list[str]]:
    manifest = build_manifest(checkout, ownership=ownership)
    target = root / manifest_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_manifest_text(manifest), encoding="utf-8")
    updated = []
    for relative, facts in _facts_by_page(manifest).items():
        page = root / relative
        if page.is_file() and _replace_block(page, render_page(facts)):
            updated.append(relative)
    return manifest["export_count"], updated


def check(
    root: Path,
    checkout: Path,
    manifest_path: Path,
    *,
    present_only: bool,
    ownership: Sequence[tuple[str, str]] = OWNERSHIP,
) -> tuple[int, int, list[str]]:
    expected = build_manifest(checkout, ownership=ownership)
    target = root / manifest_path
    if not target.is_file():
        raise ValueError(f"generated manifest is absent: {target}")
    if target.read_text(encoding="utf-8") != _manifest_text(expected):
        raise ValueError(
            "generated Python manifest has drifted; run the generator with --write"
        )

    missing = []
    checked = 0
    for relative, facts in _facts_by_page(expected).items():
        page = root / relative
        if not page.is_file():
            missing.append(relative)
            continue
        checked += 1
        text = page.read_text(encoding="utf-8")
        wanted = render_page(facts)
        if text.count(BEGIN) != 1 or text.count(END) != 1 or wanted not in text:
            raise ValueError(f"{relative}: generated Python block has drifted")
    if missing and not present_only:
        raise ValueError("mapped pages are absent: " + ", ".join(missing))
    return expected["export_count"], checked, missing


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write generated facts")
    mode.add_argument(
        "--check", action="store_true", help="validate all mapped pages and facts"
    )
    mode.add_argument(
        "--check-present",
        action="store_true",
        help="validate generated facts and mapped pages present in this checkout",
    )
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    try:
        if args.write:
            exports, updated = write(args.root, args.weaver_checkout, args.manifest)
            print(f"wrote {exports} public exports; updated {len(updated)} page(s)")
        else:
            exports, checked, missing = check(
                args.root,
                args.weaver_checkout,
                args.manifest,
                present_only=args.check_present,
            )
            print(f"validated {exports} public exports across {checked} page(s)")
            if missing:
                print("not present (bounded check): " + ", ".join(missing))
        return 0
    except (OSError, SyntaxError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
