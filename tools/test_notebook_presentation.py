"""Code and its corresponding output change mode as one tab."""

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


def generator():
    spec = importlib.util.spec_from_file_location(
        "generate_notebook_examples", ROOT / "tools/generate_notebook_examples.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_terminal_block_gets_its_native_notebook_cell():
    original = "Before\n\n```bash\nweaver load Warehouse/Operations\n```\n\nAfter\n"
    examples = [
        {
            "page": "warehouse/example.md",
            "ordinal": 0,
            "terminal": "weaver load Warehouse/Operations\n",
            "language": "bash",
            "cells": [
                {
                    "code": "import weaver\nresult = weaver.load(items=['Warehouse/Operations'], workspace='Parcel Development')\nresult.to_mapping()\n"
                }
            ],
        }
    ]
    rendered = hook().pair_markdown(
        original, page="warehouse/example.md", examples=examples
    )
    assert '=== "Terminal"' in rendered
    assert '=== "Notebook"' in rendered
    assert "    weaver load Warehouse/Operations" in rendered
    assert "    result.to_mapping()" in rendered
    assert 'title="Notebook"' not in rendered
    assert "```python {.weaver-notebook-cell .weaver-notebook-shell-cell}" in rendered
    assert rendered.startswith("Before\n")
    assert rendered.endswith("After\n")


def test_plain_reference_and_console_tabs_keep_their_zero_top_gap():
    for language, source in (
        ("text", "weaver build [-h]\n"),
        ("console", "$ weaver session\n"),
    ):
        original = f"```{language}\n{source}```\n"
        examples = [
            {
                "page": "reference/example.md",
                "ordinal": 0,
                "terminal": source,
                "language": language,
                "cells": [{"code": "import weaver\nhelp(weaver.build)\n"}],
            }
        ]
        rendered = hook().pair_markdown(
            original, page="reference/example.md", examples=examples
        )
        assert "```python {.weaver-notebook-cell}" in rendered
        assert "weaver-notebook-shell-cell" not in rendered


def test_mode_switch_keeps_each_output_with_its_producing_cell():
    capture = '<!-- cli-capture: {"id": "unit-fixture"} -->\n<figure class="weaver-terminal">CLI fixture output</figure>\n<!-- /cli-capture -->'
    original = "```bash\nweaver check\n```\n\n" + capture + "\n\nAfter\n"
    examples = [
        {
            "page": "reference/example.md",
            "ordinal": 0,
            "terminal": "weaver check\n",
            "language": "bash",
            "cells": [
                {
                    "code": "import weaver\nresult = weaver.check()\nprint(result.project_folder)\n",
                    "output": "Notebook fixture <literal>\n",
                }
            ],
        }
    ]
    rendered = hook().pair_markdown(
        original, page="reference/example.md", examples=examples
    )
    terminal, notebook = rendered.split('=== "Notebook"')
    assert "CLI fixture output" in terminal
    assert "CLI fixture output" not in notebook
    assert "Notebook fixture &lt;literal&gt;" in notebook
    assert "Notebook output" in notebook
    assert rendered.endswith("After\n")


def test_the_mkdocs_hook_loads_only_checked_in_examples(tmp_path, monkeypatch):
    import json
    from types import SimpleNamespace

    module = hook()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    entry = {
        "page": "example.md",
        "ordinal": 0,
        "terminal": "weaver check\n",
        "language": "bash",
        "cells": [{"code": "import weaver\nweaver.check()\n"}],
    }
    (tmp_path / "notebook-examples.json").write_text(json.dumps({"examples": [entry]}))
    result = module.on_page_markdown(
        "```bash\nweaver check\n```",
        page=SimpleNamespace(file=SimpleNamespace(src_uri="example.md")),
        config=None,
        files=None,
    )
    assert '=== "Notebook"' in result


def test_adjacent_pairs_cannot_merge_into_duplicate_mode_labels():
    original = "```bash\nweaver check\n```\n\n```bash\nweaver health\n```\n"
    examples = [
        {
            "page": "example.md",
            "ordinal": i,
            "terminal": f"weaver {name}\n",
            "language": "bash",
            "cells": [{"code": f"import weaver\nweaver.{name}()\n"}],
        }
        for i, name in enumerate(["check", "health"])
    ]
    rendered = hook().pair_markdown(original, page="example.md", examples=examples)
    assert rendered.count("<!-- notebook-pair-end -->") == 2


def test_notebook_output_is_literal_after_markdown_rendering():
    from html.parser import HTMLParser

    import markdown

    output = "{'path': 'Landing/_/Load/file_name.py', 'literal': '*not emphasis* `code` [link](target)'}\n\n    indented help text\n"
    entry = {
        "page": "example.md",
        "ordinal": 0,
        "terminal": "weaver check\n",
        "language": "bash",
        "cells": [{"code": "print('result')\n", "output": output}],
    }
    paired = hook().pair_markdown(
        "```bash\nweaver check\n```\n", page="example.md", examples=[entry]
    )
    rendered = markdown.markdown(
        paired,
        extensions=["pymdownx.tabbed", "pymdownx.superfences", "md_in_html"],
        extension_configs={"pymdownx.tabbed": {"alternate_style": True}},
    )

    class Reader(HTMLParser):
        active = False
        text = ""

        def handle_starttag(self, tag, attrs):
            if tag == "pre":
                self.active = True

        def handle_endtag(self, tag):
            if tag == "pre":
                self.active = False

        def handle_data(self, data):
            if self.active:
                self.text += data

    reader = Reader()
    reader.feed(rendered[rendered.index("<figure") :])
    assert reader.text == output


def test_cli_output_retains_literal_punctuation_inside_tabs():
    original = '```bash\nweaver check\n```\n\n<!-- cli-capture: {"id": "unit"} -->\n<figure><pre><code><span class="terminal-status-green">_literal_ *stars*</span></code></pre></figure>\n<!-- /cli-capture -->\n'
    examples = [
        {
            "page": "example.md",
            "ordinal": 0,
            "terminal": "weaver check\n",
            "language": "bash",
            "cells": [{"code": "import weaver\nweaver.check()\n"}],
        }
    ]
    rendered = hook().pair_markdown(original, page="example.md", examples=examples)
    assert (
        '<span class="terminal-status-green">&#95;literal&#95; &#42;stars&#42;</span>'
        in rendered
    )


def test_every_terminal_output_has_one_equivalent_notebook_output():
    import json

    examples = json.loads((ROOT / "notebook-examples.json").read_text())["examples"]
    captures = {
        row["label"]: row
        for row in json.loads(
            (ROOT / "docs/assets/cli-captures/manifest.json").read_text()
        )["captures"]
    }
    module = generator()

    def semantic_parameters(values):
        values = dict(values or {})
        if values.get("source") == ".":
            values.pop("source")
        if values.get("project_folder") == ".":
            values.pop("project_folder")
        return values

    failures = []
    for entry in examples:
        if not entry["cli_captures"]:
            continue
        assert len(entry["cli_captures"]) == 1
        capture_id = entry["cli_captures"][0]
        expected = module.compile_terminal(captures[capture_id]["command"])[-1]
        observed = [
            cell
            for cell in entry["cells"]
            if cell.get("observation", {}).get("capture_id") == capture_id
            and "output" in cell
        ]
        if (
            len(observed) != 1
            or observed[0]["operation"] != expected["operation"]
            or semantic_parameters(observed[0].get("parameters"))
            != semantic_parameters(expected.get("parameters"))
        ):
            failures.append((entry["page"], entry["ordinal"], capture_id))
    assert failures == []
