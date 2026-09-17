#!/usr/bin/env python3
"""Generate and validate Weaver CLI parser facts in the public reference."""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

BEGIN = "<!-- BEGIN GENERATED CLI -->"
END = "<!-- END GENERATED CLI -->"
DEFAULT_MANIFEST = Path("generated/cli-reference.json")

# Every executable parser leaf has one documentation owner. A page may own
# several leaves when aliases or one command family are deliberately combined.
OWNERSHIP: tuple[tuple[str, str], ...] = (
    ("session", "docs/reference/cli/session-and-workflow.md"),
    ("workflow", "docs/reference/cli/session-and-workflow.md"),
    ("initialise", "docs/reference/cli/initialise.md"),
    ("initialize", "docs/reference/cli/initialise.md"),
    ("doctor", "docs/reference/cli/doctor.md"),
    ("check", "docs/reference/cli/check.md"),
    ("build", "docs/reference/cli/build.md"),
    ("install", "docs/reference/cli/install.md"),
    ("load", "docs/reference/cli/load.md"),
    ("test", "docs/reference/cli/test.md"),
    ("health", "docs/reference/cli/health.md"),
    ("wipe", "docs/reference/cli/wipe.md"),
    ("mirror", "docs/reference/cli/mirror.md"),
    ("fabric environment publish", "docs/reference/cli/fabric-environment.md"),
    ("fabric notebook push", "docs/reference/cli/fabric-notebook.md"),
    ("fabric notebook run", "docs/reference/cli/fabric-notebook.md"),
    ("fabric capacity", "docs/reference/cli/fabric-capacity.md"),
)


def _normalise(text: str | None) -> str | None:
    if text is None:
        return None
    return " ".join(text.split())


def _formatter(parser: argparse.ArgumentParser) -> argparse.HelpFormatter:
    return argparse.HelpFormatter(parser.prog, width=1_000_000, max_help_position=24)


def _synopsis(parser: argparse.ArgumentParser) -> str:
    formatter = _formatter(parser)
    formatter.add_usage(
        parser.usage, parser._actions, parser._mutually_exclusive_groups
    )
    usage = " ".join(formatter.format_help().split())
    return usage.removeprefix("usage: ")


def _invocation(parser: argparse.ArgumentParser, action: argparse.Action) -> str:
    return _formatter(parser)._format_action_invocation(action)


def _action_fact(
    parser: argparse.ArgumentParser, action: argparse.Action
) -> dict[str, Any]:
    fact: dict[str, Any] = {
        "invocation": _invocation(parser, action),
        "help": _normalise(action.help),
        "required": bool(action.required),
    }
    if action.choices is not None:
        fact["choices"] = [str(choice) for choice in action.choices]
    return fact


def _command_fact(
    path: tuple[str, ...], parser: argparse.ArgumentParser
) -> dict[str, Any]:
    visible = [
        action for action in parser._actions if action.help is not argparse.SUPPRESS
    ]
    positionals = [action for action in visible if not action.option_strings]
    options = [action for action in visible if action.option_strings]
    return {
        "command": " ".join(path),
        "synopsis": _synopsis(parser),
        "positionals": [_action_fact(parser, action) for action in positionals],
        "options": [_action_fact(parser, action) for action in options],
    }


def _leaves(
    parser: argparse.ArgumentParser, path: tuple[str, ...] = ()
) -> list[dict[str, Any]]:
    subparsers = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    choices = {
        name: child for action in subparsers for name, child in action.choices.items()
    }
    if not choices:
        if not path:
            raise ValueError("the root parser has no commands")
        return [_command_fact(path, parser)]
    facts: list[dict[str, Any]] = []
    for name in sorted(choices):
        facts.extend(_leaves(choices[name], (*path, name)))
    return facts


def _load_parser(checkout: Path) -> argparse.ArgumentParser:
    source = checkout.resolve() / "src"
    if not source.is_dir():
        raise ValueError(f"Weaver source directory not found: {source}")
    sys.path.insert(0, str(source))
    try:
        module = importlib.import_module("weaver_cli.main")
        return module.build_parser()
    finally:
        sys.path.remove(str(source))


def _ownership() -> dict[str, str]:
    counts = Counter(command for command, _page in OWNERSHIP)
    duplicates = sorted(command for command, count in counts.items() if count != 1)
    if duplicates:
        raise ValueError("commands assigned more than once: " + ", ".join(duplicates))
    return dict(OWNERSHIP)


def build_manifest(checkout: Path) -> dict[str, Any]:
    commands = _leaves(_load_parser(checkout))
    commands.sort(key=lambda fact: fact["command"])
    live = {fact["command"] for fact in commands}
    ownership = _ownership()
    assigned = set(ownership)
    unassigned = sorted(live - assigned)
    retired = sorted(assigned - live)
    if unassigned:
        raise ValueError("live leaf commands are unassigned: " + ", ".join(unassigned))
    if retired:
        raise ValueError("retired commands remain owned: " + ", ".join(retired))
    return {
        "schema_version": 1,
        "leaf_count": len(commands),
        "page_count": len(set(ownership.values())),
        "ownership": ownership,
        "commands": commands,
    }


def _description(fact: dict[str, Any]) -> str:
    return fact["help"] or "No description is provided by the parser."


def _mechanics(fact: dict[str, Any], *, level: int) -> list[str]:
    hashes = "#" * level
    lines = [f"{hashes} Synopsis", "", "```text", fact["synopsis"], "```", ""]
    if fact["positionals"]:
        lines.extend([f"{hashes} Positional arguments", ""])
        for action in fact["positionals"]:
            lines.extend([f"`{action['invocation']}`", f": {_description(action)}", ""])
    lines.extend([f"{hashes} Options", ""])
    for action in fact["options"]:
        lines.extend([f"`{action['invocation']}`", f": {_description(action)}", ""])
    return lines


def render_page(facts: list[dict[str, Any]]) -> str:
    if not facts:
        raise ValueError("cannot render a page without commands")
    same_mechanics = all(
        (fact["positionals"], fact["options"])
        == (facts[0]["positionals"], facts[0]["options"])
        for fact in facts[1:]
    )
    lines = [BEGIN, ""]
    if len(facts) == 1:
        lines.extend(_mechanics(facts[0], level=2))
    elif same_mechanics:
        lines.extend(["## Synopsis", "", "```text"])
        lines.extend(fact["synopsis"] for fact in facts)
        lines.extend(["```", ""])
        shared = dict(facts[0], synopsis="")
        mechanics = _mechanics(shared, level=2)
        options_start = (
            mechanics.index("## Positional arguments")
            if shared["positionals"]
            else mechanics.index("## Options")
        )
        lines.extend(mechanics[options_start:])
    else:
        for fact in facts:
            lines.extend([f"## `weaver {fact['command']}`", ""])
            lines.extend(_mechanics(fact, level=3))
    while lines and not lines[-1]:
        lines.pop()
    lines.extend(["", END])
    return "\n".join(lines)


def _facts_by_page(manifest: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_command = {fact["command"]: fact for fact in manifest["commands"]}
    pages: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for command, page in manifest["ownership"].items():
        pages[page].append(by_command[command])
    for facts in pages.values():
        facts.sort(key=lambda fact: fact["command"])
    return dict(sorted(pages.items()))


def _replace_block(page: Path, generated: str) -> bool:
    text = page.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise ValueError(f"{page}: expected exactly one generated CLI block")
    updated = pattern.sub(generated, text)
    if updated == text:
        return False
    page.write_text(updated, encoding="utf-8")
    return True


def _manifest_text(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write(root: Path, checkout: Path, manifest_path: Path) -> tuple[int, list[str]]:
    manifest = build_manifest(checkout)
    target = root / manifest_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_manifest_text(manifest), encoding="utf-8")
    updated: list[str] = []
    for relative, facts in _facts_by_page(manifest).items():
        page = root / relative
        if page.is_file() and _replace_block(page, render_page(facts)):
            updated.append(relative)
    return manifest["leaf_count"], updated


def check(
    root: Path, checkout: Path, manifest_path: Path, *, present_only: bool
) -> tuple[int, int, list[str]]:
    expected = build_manifest(checkout)
    target = root / manifest_path
    if not target.is_file():
        raise ValueError(f"generated manifest is absent: {target}")
    if target.read_text(encoding="utf-8") != _manifest_text(expected):
        raise ValueError(
            "generated manifest has drifted; run the generator with --write"
        )

    missing: list[str] = []
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
            raise ValueError(f"{relative}: generated CLI block has drifted")
    if missing and not present_only:
        raise ValueError("mapped pages are absent: " + ", ".join(missing))
    return expected["leaf_count"], checked, missing


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--write",
        action="store_true",
        help="write the manifest and present page blocks",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="validate the manifest and every mapped page",
    )
    mode.add_argument(
        "--check-present",
        action="store_true",
        help="validate the manifest and mapped pages present in this checkout",
    )
    parser.add_argument("--weaver-checkout", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    try:
        if args.write:
            leaves, updated = write(args.root, args.weaver_checkout, args.manifest)
            print(f"wrote {leaves} leaf commands; updated {len(updated)} page(s)")
        else:
            leaves, checked, missing = check(
                args.root,
                args.weaver_checkout,
                args.manifest,
                present_only=args.check_present,
            )
            print(f"validated {leaves} leaf commands across {checked} page(s)")
            if missing:
                print("not present (bounded check): " + ", ".join(missing))
        return 0
    except (ImportError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
