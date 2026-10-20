import importlib.util
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def hook():
    spec = importlib.util.spec_from_file_location(
        "terminal_presentation", ROOT / "tools/terminal_presentation.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_separate_command_gets_a_prompt_but_escaped_lines_continue():
    assert hook().shell_prompts(
        [
            "python -m pip install --upgrade weaverstack",
            "weaver --version",
            "",
            "weaver initialise \\",
            '  --workspace "Parcel Development" \\',
            "  --example Parcel",
            "cd parcel",
        ]
    ) == ["$", "$", "", "$", ">", ">", "$"]


def test_compounds_quotes_and_heredocs_do_not_become_new_commands():
    assert hook().shell_prompts(
        [
            "if test -f file; then",
            "  cp file saved",
            "else",
            "  echo missing",
            "fi",
            "weaver check",
            'echo "hello',
            'world"',
            "cat <<EOF",
            "hello",
            "EOF",
            "weaver build",
        ]
    ) == ["$", ">", ">", ">", ">", "$", "$", ">", "$", ">", ">", "$"]


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def test_generated_prompts_are_attributes_not_copied_code_or_output():
    original = '<div class="language-bash highlight"><pre><code><span id="__span-0-0">weaver check</span>\n<span id="__span-0-1">weaver build <span class="se">\\</span></span>\n<span id="__span-0-2">  --item Warehouse/Operations</span>\n</code></pre></div><figure class="weaver-terminal"><pre><code>Build\n\n✓ Build\n</code></pre></figure>'
    result = hook().on_page_content(original, page=None, config=None, files=None)
    assert result.count('data-terminal-prompt="$"') == 2
    assert result.count('data-terminal-prompt="&gt;"') == 1
    a, b = Text(), Text()
    a.feed(original)
    b.feed(result)
    assert a.parts == b.parts
    assert result.endswith(
        '<figure class="weaver-terminal"><pre><code>Build\n\n✓ Build\n</code></pre></figure>'
    )
    assert hook().on_page_content(result, page=None, config=None, files=None) == result
