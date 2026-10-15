"""Package tracked examples as deterministic, same-site downloads."""

from __future__ import annotations

import argparse
import subprocess
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "docs/assets/examples"


def archives() -> dict[str, bytes]:
    tracked = (
        subprocess.check_output(["git", "ls-files", "-z", "--", "examples"], cwd=ROOT)
        .decode()
        .split("\0")
    )
    projects: dict[str, list[str]] = {}
    for name in sorted(filter(None, tracked)):
        path = Path(name)
        if len(path.parts) >= 3:
            projects.setdefault(path.parts[1], []).append(name)
    output = {}
    for project, names in projects.items():
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            for name in names:
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (ROOT / name).read_bytes())
        output[project + ".zip"] = buffer.getvalue()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = archives()
    if args.check:
        assert {p.name for p in DESTINATION.glob("*.zip")} == set(expected)
        for name, payload in expected.items():
            assert (DESTINATION / name).read_bytes() == payload, name
    else:
        DESTINATION.mkdir(parents=True, exist_ok=True)
        for name, payload in expected.items():
            (DESTINATION / name).write_bytes(payload)
    print(
        f"{'Checked' if args.check else 'Packaged'} {len(expected)} complete tracked example projects"
    )


if __name__ == "__main__":
    main()
