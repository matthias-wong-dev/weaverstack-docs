"""Selected Notebook cells keep code, context and output together."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def hook():
    spec = importlib.util.spec_from_file_location(
        "notebook_presentation", ROOT / "tools/notebook_presentation.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def entry(*, output=None):
    cell = {
        "code": "import weaver\nresult = weaver.load(items=['Warehouse/Operations'], workspace='Parcel Development', catalogue='Warehouse/Catalogue')\nresult.report()\n"
    }
    if output is not None:
        cell["output"] = output
    return {
        "page": "warehouse/example.md",
        "ordinal": 0,
        "terminal": "weaver load Warehouse/Operations\n",
        "language": "bash",
        "cells": [cell],
    }


def test_notebook_cell_has_line_numbers_and_no_redundant_filename():
    rendered = hook().pair_markdown(
        "```bash\nweaver load Warehouse/Operations\n```\n",
        page="warehouse/example.md",
        examples=[entry()],
    )
    assert '=== "Terminal"' in rendered
    assert '=== "Notebook"' in rendered
    assert 'linenums="1"' in rendered
    assert ".weaver-notebook-cell" in rendered
    assert 'title="Notebook"' not in rendered
    assert "result.report()" in rendered


def test_terminal_only_block_is_left_untouched():
    original = "Before\n\n```bash\nweaver doctor\n```\n\nAfter\n"
    assert (
        hook().pair_markdown(original, page="reference/example.md", examples=[])
        == original
    )


def test_command_returned_intro_stays_in_both_modes():
    capture = '<!-- cli-capture: {"id": "unit"} -->\n<p class="terminal-intro">The command returned:</p>\n<figure class="weaver-terminal"><figcaption>Terminal output</figcaption><pre><code>CLI fixture</code></pre></figure>\n<!-- /cli-capture -->'
    original = "```bash\nweaver load Warehouse/Operations\n```\n" + capture + "\n"
    rendered = hook().pair_markdown(
        original,
        page="warehouse/example.md",
        examples=[entry(output="Notebook fixture\n")],
    )
    terminal, notebook = rendered.split('=== "Notebook"')
    assert terminal.count("The command returned:") == 1
    assert notebook.count("The command returned:") == 1
    assert "CLI fixture" in terminal and "CLI fixture" not in notebook
    assert "Notebook fixture" in notebook and "Notebook output" in notebook


def test_notebook_output_remains_literal_after_markdown_rendering():
    from html.parser import HTMLParser

    import markdown

    output = (
        "{'path': 'Landing/_/file.py', 'literal': '*stars* `code`'}\n\n    help text\n"
    )
    paired = hook().pair_markdown(
        "```bash\nweaver load Warehouse/Operations\n```\n",
        page="warehouse/example.md",
        examples=[entry(output=output)],
    )
    rendered = markdown.markdown(
        paired,
        extensions=["pymdownx.tabbed", "pymdownx.superfences", "md_in_html"],
        extension_configs={"pymdownx.tabbed": {"alternate_style": True}},
    )

    class Reader(HTMLParser):
        in_figure = False
        active = False
        text = ""

        def handle_starttag(self, tag, attrs):
            if tag == "figure" and dict(attrs).get("class", "").endswith(
                "weaver-notebook-output"
            ):
                self.in_figure = True
            elif tag == "pre" and self.in_figure:
                self.active = True

        def handle_endtag(self, tag):
            if tag == "pre":
                self.active = False
            elif tag == "figure":
                self.in_figure = False

        def handle_data(self, data):
            if self.active and data != "Notebook output":
                self.text += data

    reader = Reader()
    reader.feed(rendered)
    assert reader.text == output


def test_adjacent_selected_pairs_stay_separate():
    original = "```bash\nweaver load A\n```\n\n```bash\nweaver test A\n```\n"
    examples = []
    for ordinal, operation in enumerate(("load", "test")):
        examples.append(
            {
                "page": "example.md",
                "ordinal": ordinal,
                "terminal": f"weaver {operation} A\n",
                "language": "bash",
                "cells": [
                    {
                        "code": f"import weaver\nresult = weaver.{operation}(items=['A'])\nresult.report()\n"
                    }
                ],
            }
        )
    rendered = hook().pair_markdown(original, page="example.md", examples=examples)
    assert rendered.count("<!-- notebook-pair-end -->") == 2
