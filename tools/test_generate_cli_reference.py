"""Generated CLI facts describe effective positional optionality."""

import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generator():
    spec = importlib.util.spec_from_file_location(
        "generate_cli_reference", ROOT / "tools/generate_cli_reference.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zero_or_more_positional_is_not_reported_as_required():
    parser = argparse.ArgumentParser()
    parser.add_argument("items", nargs="*")
    action = next(action for action in parser._actions if action.dest == "items")
    assert parser.parse_args([]).items == []
    assert generator()._action_fact(parser, action)["required"] is False
