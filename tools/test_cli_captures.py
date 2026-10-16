import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def renderer():
    spec = importlib.util.spec_from_file_location(
        "render_cli_captures", ROOT / "tools/render_cli_captures.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CodeText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_code = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "code":
            self.in_code = True

    def handle_endtag(self, tag):
        if tag == "code":
            self.in_code = False

    def handle_data(self, data):
        if self.in_code:
            self.parts.append(data)


def test_carriage_return_redraw_does_not_become_a_blank_output_line():
    raw = "\x1b[2m⋯ Work\x1b[0m\r        \rRead catalogue  1.0s\r\nDone\r\n"
    assert renderer().terminal_text(raw) == "Read catalogue  1.0s\nDone\n"


def test_actual_blank_output_lines_and_overwritten_columns_are_preserved():
    raw = "Build\r\n\r\nabcdef\rXY\r\n\r\n\r\nSummary\r\n"
    assert renderer().terminal_text(raw) == "Build\n\nXYcdef\n\n\nSummary\n"


def test_every_plain_capture_is_derived_from_its_original_terminal_stream():
    module = renderer()
    assets = ROOT / "docs/assets/cli-captures"
    manifest = json.loads((assets / "manifest.json").read_text())
    for record in manifest["captures"]:
        raw = (assets / record["raw_ansi"]).read_bytes().decode("utf-8")
        assert module.terminal_text(raw) == (assets / record["text"]).read_text(), (
            record["label"]
        )


def test_every_tutorial_panel_shows_the_whole_capture_without_evidence_chrome():
    module = renderer()
    assets = ROOT / "docs/assets/cli-captures"
    manifest = json.loads((assets / "manifest.json").read_text())
    captures = {entry["label"]: entry for entry in manifest["captures"]}
    count = 0
    for page in sorted((ROOT / "docs").rglob("*.md")):
        for match in module.BLOCK.finditer(page.read_text()):
            marker = json.loads(match[2])
            assert not {"start", "end", "full"} & marker.keys()
            record = captures[marker["id"]]
            expected = (assets / record["text"]).read_text()
            parser = CodeText()
            parser.feed(match[3])
            assert "".join(parser.parts) == expected, (page, record["label"])
            assert match[3].count("<pre ") == 1
            assert "<details>" not in match[3]
            assert "<a " not in match[3]
            for label in (
                "Sanitised transcript",
                "Capture details",
                "Transcript excerpt",
            ):
                assert label not in match[3]
            count += 1
    assert count > 0


def test_output_is_introduced_as_terminal_output_not_a_custom_result_heading():
    rendered = renderer().render_terminal(
        "Project valid.\n", title="Check · Parcel declarations", exit_code=0
    )
    assert "The command returned:" in rendered
    assert "<figcaption>Terminal output " in rendered
    assert "<figcaption>Check · Parcel declarations" not in rendered
    parser = CodeText()
    parser.feed(rendered)
    assert "".join(parser.parts) == "Project valid.\n"


def test_real_failed_capture_keeps_words_order_glyphs_and_failure_status():
    text = (ROOT / "docs/assets/cli-captures/19-failed-warehouse-test.txt").read_text()
    rendered = renderer().render_terminal(text, title="Actual Test result", exit_code=1)
    parser = CodeText()
    parser.feed(rendered)
    assert "".join(parser.parts) == text
    assert "terminal-status-red" in rendered
    assert "exit 1" in rendered
    assert "<script" not in rendered


def test_error_text_is_escaped_and_zero_failures_are_not_coloured_red():
    rendered = renderer().render_terminal(
        "error: <missing> & unchanged\n    0 failed\n",
        title="Actual error",
        exit_code=1,
    )
    assert 'terminal-status-red">error:' in rendered
    assert "&lt;missing&gt; &amp; unchanged" in rendered
    assert 'terminal-status-red">    0 failed' not in rendered
