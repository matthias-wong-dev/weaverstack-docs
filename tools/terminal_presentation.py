"""Add visual shell prompts at build time, outside copyable command text."""

import re
from html import escape
from html.parser import HTMLParser

from pygments import lex
from pygments.lexers import BashLexer
from pygments.token import Comment, Keyword, String

OPEN = {
    "if": "fi",
    "for": "done",
    "while": "done",
    "until": "done",
    "select": "done",
    "case": "esac",
}
CLOSE = set(OPEN.values())
VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


def shell_prompts(lines):
    """Distinguish independent commands from shell continuations."""
    if not lines:
        return []
    rows = [{"keywords": [], "quoted": False, "code": []} for _ in lines]
    index = 0
    for token, value in lex("\n".join(lines), BashLexer(stripnl=False, ensurenl=False)):
        parts = value.split("\n")
        for offset, part in enumerate(parts):
            if index >= len(rows):
                break
            if offset and token in String:
                rows[index]["quoted"] = True
            if token in Keyword:
                rows[index]["keywords"].append(part.strip())
            if token not in Comment:
                rows[index]["code"].append(part)
            if offset < len(parts) - 1:
                index += 1
    stack = []
    continuation = False
    prompts = []
    for line, row in zip(lines, rows, strict=True):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            prompts.append("")
            continue
        prompts.append(">" if stack or continuation or row["quoted"] else "$")
        for word in row["keywords"]:
            if word in OPEN:
                stack.append(OPEN[word])
            elif word in CLOSE and stack and stack[-1] == word:
                stack.pop()
        if stripped == "{" or re.match(r"(?:function\s+)?\w+\s*\(\)\s*\{", stripped):
            stack.append("}")
        elif stripped.startswith("}") and stack and stack[-1] == "}":
            stack.pop()
        code = "".join(row["code"]).rstrip()
        trailing = len(code) - len(code.rstrip("\\"))
        continuation = bool(trailing % 2) or code.endswith(("&&", "||", "|"))
    return prompts


class BashLines(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.groups = []
        self.bash_depth = None
        self.line = None

    def handle_starttag(self, tag, attrs):
        attributes = {key: value or "" for key, value in attrs}
        parent = self.stack[-1] if self.stack else None
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "div" and {"language-bash", "highlight"} <= set(
            attributes.get("class", "").split()
        ):
            self.bash_depth = len(self.stack)
            self.groups.append([])
        if (
            self.bash_depth is not None
            and parent == "code"
            and tag == "span"
            and attributes.get("id", "").startswith("__span-")
        ):
            self.line = {
                "tag": self.get_starttag_text(),
                "text": [],
                "depth": len(self.stack),
            }
            self.groups[-1].append(self.line)

    def handle_endtag(self, tag):
        if (
            self.line is not None
            and tag == "span"
            and len(self.stack) == self.line["depth"]
        ):
            self.line = None
        if self.bash_depth == len(self.stack) and tag == "div":
            self.bash_depth = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.line is not None:
            self.line["text"].append(data)


def on_page_content(html, *, page, config, files):
    parser = BashLines()
    parser.feed(html)
    for group in parser.groups:
        lines = ["".join(line["text"]).rstrip("\n") for line in group]
        for line, prompt in zip(group, shell_prompts(lines), strict=True):
            if not prompt or "data-terminal-prompt=" in line["tag"]:
                continue
            updated = (
                line["tag"][:-1]
                + f' data-terminal-prompt="{escape(prompt, quote=True)}">'
            )
            html = html.replace(line["tag"], updated, 1)
    return html
