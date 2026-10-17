"""Pair terminal examples with checked native Notebook cells at build time."""

from __future__ import annotations

import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from string import punctuation
from textwrap import dedent, indent

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(
    r"(?m)^(?P<indent>[ \t]*)(?P<mark>`{3,}|~{3,})(?P<info>[^\n]*)\n"
    r"(?P<source>.*?)(?m:^(?P=indent)(?P=mark)[ \t]*$)",
    re.DOTALL,
)
TERMINAL_LANGUAGES = {
    "bash",
    "sh",
    "shell",
    "console",
    "powershell",
    "pwsh",
    "shell-session",
}
CAPTURE = re.compile(
    r"\s*<!-- cli-capture: [^\n]+ -->\n.*?<!-- /cli-capture -->", re.DOTALL
)


def literal_html(text):
    return "".join(
        f"&#{ord(char)};"
        if char in "\n\r\t"
        else escape(char)
        if char in "&<>\"'"
        else f"&#{ord(char)};"
        if char in punctuation
        else char
        for char in text
    )


class LiteralTranscript(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.in_code = False

    def handle_starttag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())
        if tag == "code":
            self.in_code = True

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")
        if tag == "code":
            self.in_code = False

    def handle_startendtag(self, tag, attrs):
        self.parts.append(self.get_starttag_text())

    def handle_data(self, text):
        self.parts.append(literal_html(text) if self.in_code else text)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def handle_comment(self, text):
        self.parts.append(f"<!--{text}-->")


def terminal_blocks(markdown):
    for match in FENCE.finditer(markdown):
        language = match["info"].split()[0] if match["info"].split() else ""
        if language in TERMINAL_LANGUAGES or (
            language in {"text", ""}
            and ("weaver " in match["source"] or "weaver>" in match["source"])
        ):
            yield match, language


def pair_markdown(markdown, *, page, examples):
    assigned = {entry["ordinal"]: entry for entry in examples if entry["page"] == page}
    chunks = []
    previous = 0
    for ordinal, (match, language) in enumerate(terminal_blocks(markdown)):
        entry = assigned[ordinal]
        assert entry["terminal"] == match["source"] and entry["language"] == language, (
            f"{page}: Notebook example {ordinal} has drifted"
        )
        prefix = match["indent"]
        terminal = indent(dedent(match[0]), prefix + "    ")
        end = match.end()
        while captured := CAPTURE.match(markdown, end):
            transcript = LiteralTranscript()
            transcript.feed(dedent(captured[0].strip("\n")))
            terminal += "\n\n" + indent("".join(transcript.parts), prefix + "    ")
            end = captured.end()
        notebook = []
        for cell in entry["cells"]:
            notebook.append(
                indent(
                    '```python title="Notebook"\n'
                    + cell["code"].rstrip("\n")
                    + "\n```",
                    prefix + "    ",
                )
            )
            if "output" in cell:
                # Tab containers also process inline Markdown inside raw HTML.
                literal = literal_html(cell["output"])
                figure = (
                    '<figure class="weaver-terminal weaver-notebook-output">\n<figcaption>Notebook output</figcaption>\n<pre tabindex="0" aria-label="Notebook output"><code>'
                    + literal
                    + "</code></pre></figure>"
                )
                notebook.append(indent(figure, prefix + "    "))
        tabs = (
            prefix
            + '=== "Terminal"\n\n'
            + terminal
            + "\n\n"
            + prefix
            + '=== "Notebook"\n\n'
            + "\n\n".join(notebook)
        )
        tabs += "\n\n" + prefix + "<!-- notebook-pair-end -->\n"
        chunks.extend([markdown[previous : match.start()], tabs])
        previous = end
    chunks.append(markdown[previous:])
    return "".join(chunks)


def on_page_markdown(markdown, *, page, config, files):
    if not any(terminal_blocks(markdown)):
        return markdown
    examples = json.loads((ROOT / "notebook-examples.json").read_text())["examples"]
    return pair_markdown(markdown, page=page.file.src_uri, examples=examples)
