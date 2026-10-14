#!/usr/bin/env python3
"""Generate physical catalogue tables/columns from Weaver's table declarations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED CATALOGUE REFERENCE -->"
END = "<!-- END GENERATED CATALOGUE REFERENCE -->"
PAGE = Path("docs/reference/catalogue-schema.md")
MANIFEST = Path("generated/catalogue-reference.json")


def build_manifest(checkout: Path) -> dict:
    import importlib

    source = checkout.resolve() / "src"
    sys.path.insert(0, str(source))
    try:
        module = importlib.import_module("weaver.catalogue.tables")
        if not module.__file__ or not Path(module.__file__).resolve().is_relative_to(
            source
        ):
            raise ValueError("catalogue module came from a different checkout")
        tables = []
        for table in (*module.CATALOGUE_TABLES, module.MIRROR):
            columns = []
            for name in table.physical_columns:
                audit = name in module.AUDIT_COLUMN_NAMES
                column = table.column(name) if not audit else None
                assert audit or column is not None
                columns.append(
                    {
                        "name": table.public_name_of(name),
                        "type": "datetime2(6)" if audit else column.warehouse_type,
                        "required": True if audit else column.not_null,
                        "notes": "UTC row audit timestamp"
                        if audit
                        else column.description,
                        "vocabulary": None if audit else column.vocabulary,
                    }
                )
            tables.append(
                {
                    "name": table.qualified,
                    "source": "src/weaver/catalogue/tables.py",
                    "description": table.description,
                    "key": [table.public_name_of(n) for n in table.key],
                    "columns": columns,
                }
            )
    finally:
        sys.path.remove(str(source))
    names = [t["name"] for t in tables]
    if len(names) != len(set(names)):
        raise ValueError("duplicate catalogue table")
    return {"schema_version": 1, "tables": sorted(tables, key=lambda t: t["name"])}


def render(manifest: dict) -> str:
    lines = [BEGIN, "", "## Physical table declarations", ""]
    for table in manifest["tables"]:
        lines += [
            f"### `{table['name']}`",
            "",
            "**Key:** " + ", ".join(f"`{n}`" for n in table["key"]),
            "",
            "| Column | Type | Null | Meaning |",
            "| --- | --- | --- | --- |",
        ]
        for column in table["columns"]:
            notes = column["notes"]
            if (table["name"], column["name"]) == ("_.LoadStatistic", "Is reload"):
                # RunRecord.reset/settled owns the flag; the declaration's note is stale.
                notes = (
                    "Whether this object was reset for this reload attempt. "
                    "A failed attempted reload is still marked as a reload."
                )
            meaning = notes.replace("|", "&#124;").replace(chr(10), " ")
            lines.append(
                f"| `{column['name']}` | `{column['type']}` | "
                f"{'required' if column['required'] else 'nullable'} | {meaning} |"
            )
        lines += [""]
    return "\n".join(lines + [END])


def update(root: Path, checkout: Path, *, write: bool) -> None:
    manifest = build_manifest(checkout)
    expected = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    text = (root / PAGE).read_text()
    if (
        text.count(BEGIN) != 1
        or text.count(END) != 1
        or text.index(BEGIN) > text.index(END)
    ):
        raise ValueError("catalogue reference needs one ordered marker pair")
    start, stop = text.index(BEGIN), text.index(END) + len(END)
    block = render(manifest)
    if write:
        (root / MANIFEST).parent.mkdir(parents=True, exist_ok=True)
        (root / MANIFEST).write_text(expected)
        (root / PAGE).write_text(text[:start] + block + text[stop:])
    elif (root / MANIFEST).read_text() != expected or text[start:stop] != block:
        raise ValueError("catalogue reference drift; regenerate with --write")


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
        count = len(build_manifest(args.weaver_checkout)["tables"])
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(
        f"{'wrote' if args.write else 'validated'} {count} catalogue table declarations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
