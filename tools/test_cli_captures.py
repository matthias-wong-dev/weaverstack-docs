import importlib.util
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_output_is_introduced_as_terminal_output_not_a_custom_result_heading():
    spec = importlib.util.spec_from_file_location(
        "render_cli_captures", ROOT / "tools/render_cli_captures.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rendered = module.render_terminal(
        "Project valid.\n",
        title="Check · Parcel declarations",
        raw_href="capture.txt",
        exit_code=0,
    )
    assert "The command returned:" in rendered
    assert "<figcaption>Terminal output " in rendered
    assert "<figcaption>Check · Parcel declarations" not in rendered
    parser = CodeText()
    parser.feed(rendered)
    assert "".join(parser.parts) == "Project valid.\n"


def test_selected_output_is_explicitly_labelled_as_an_excerpt():
    spec = importlib.util.spec_from_file_location(
        "render_cli_captures", ROOT / "tools/render_cli_captures.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rendered = module.render_terminal(
        "test passed\n",
        title="Actual Test",
        raw_href="capture.txt",
        exit_code=0,
        excerpted=True,
    )
    assert "Transcript excerpt" in rendered


def test_capture_links_are_relative_to_rendered_directory_routes():
    spec = importlib.util.spec_from_file_location(
        "render_cli_captures", ROOT / "tools/render_cli_captures.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "asset_href"), (
        "Rendered-route asset links are not implemented"
    )
    asset = ROOT / "docs/assets/cli-captures/13-warehouse-load.txt"
    assert (
        module.asset_href(ROOT / "docs/warehouse/first-project.md", asset)
        == "../../assets/cli-captures/13-warehouse-load.txt"
    )
    assert (
        module.asset_href(ROOT / "docs/warehouse/index.md", asset)
        == "../assets/cli-captures/13-warehouse-load.txt"
    )


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


def test_real_failed_capture_keeps_words_order_glyphs_and_failure_status():
    path = ROOT / "tools/render_cli_captures.py"
    assert path.is_file(), "The reusable terminal renderer has not been implemented"
    spec = importlib.util.spec_from_file_location("render_cli_captures", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text = (ROOT / "docs/assets/cli-captures/19-failed-warehouse-test.txt").read_text()
    excerpt = text[text.index("test failed\n") :]
    rendered = module.render_terminal(
        excerpt,
        title="Actual Test result",
        raw_href="../assets/cli-captures/19-failed-warehouse-test.txt",
        exit_code=1,
    )
    parser = CodeText()
    parser.feed(rendered)
    assert "".join(parser.parts) == excerpt
    assert "terminal-status-red" in rendered
    assert "exit 1" in rendered
    assert "<script" not in rendered


def test_error_text_is_escaped_and_zero_failures_are_not_coloured_red():
    path = ROOT / "tools/render_cli_captures.py"
    spec = importlib.util.spec_from_file_location("render_cli_captures", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rendered = module.render_terminal(
        "error: <missing> & unchanged\n    0 failed\n",
        title="Actual error",
        raw_href="capture.txt",
        exit_code=1,
    )
    assert 'terminal-status-red">error:' in rendered
    assert "&lt;missing&gt; &amp; unchanged" in rendered
    assert 'terminal-status-red">    0 failed' not in rendered


def test_excerpt_keeps_the_complete_observed_summary_lines():
    path = ROOT / "tools/render_cli_captures.py"
    spec = importlib.util.spec_from_file_location("render_cli_captures", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "excerpt"), "Line-boundary selection is not implemented"
    text = (ROOT / "docs/assets/cli-captures/13-warehouse-load.txt").read_text()
    actual = module.excerpt(text, start="Load summary", end="  Workflow:")
    assert actual == text[text.index("Load summary") : text.index("  Workflow:")]
    assert "inserted               3" in actual
