"""Convert a subset of Markdown into Notion block objects.

Supports the elements the newsletter template uses: H1/H2/H3 headings, paragraphs, bulleted
and numbered lists, block quotes (including multi-line), dividers, and inline bold, italic and
links. This is deliberately small and well-tested rather than a full Markdown engine.
"""
from __future__ import annotations

import re

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_EMPHASIS_RE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*)")
_BULLET_RE = re.compile(r"^[-*]\s+")
_NUMBERED_RE = re.compile(r"^\d+\.\s+")

NOTION_TEXT_LIMIT = 1900  # stay safely under Notion's 2000-char rich_text limit


def _annotate(text: str, link: str | None = None) -> list[dict]:
    """Turn a plain string into rich_text objects, honouring **bold** and *italic*."""
    objs: list[dict] = []
    for part in _EMPHASIS_RE.split(text):
        if not part:
            continue
        bold = italic = False
        content = part
        if part.startswith("**") and part.endswith("**"):
            bold = True
            content = part[2:-2]
        elif part.startswith("*") and part.endswith("*"):
            italic = True
            content = part[1:-1]
        objs.append(_text_obj(content, bold=bold, italic=italic, link=link))
    return objs


def _text_obj(content: str, bold=False, italic=False, link: str | None = None) -> dict:
    content = content[:NOTION_TEXT_LIMIT]
    text: dict = {"content": content}
    if link:
        text["link"] = {"url": link}
    obj: dict = {"type": "text", "text": text}
    if bold or italic:
        obj["annotations"] = {"bold": bold, "italic": italic}
    return obj


def parse_rich_text(text: str) -> list[dict]:
    """Parse inline Markdown (links + emphasis) into a Notion rich_text array."""
    objs: list[dict] = []
    pos = 0
    for m in _LINK_RE.finditer(text):
        if m.start() > pos:
            objs.extend(_annotate(text[pos:m.start()]))
        label, url = m.group(1), m.group(2)
        objs.extend(_annotate(label, link=url))
        pos = m.end()
    if pos < len(text):
        objs.extend(_annotate(text[pos:]))
    return objs or [_text_obj("")]


def _block(block_type: str, rich: list[dict]) -> dict:
    return {"object": "block", "type": block_type, block_type: {"rich_text": rich}}


def markdown_to_blocks(md: str) -> list[dict]:
    lines = md.split("\n")
    blocks: list[dict] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue

        if line == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif line.startswith("### "):
            blocks.append(_block("heading_3", parse_rich_text(line[4:])))
        elif line.startswith("## "):
            blocks.append(_block("heading_2", parse_rich_text(line[3:])))
        elif line.startswith("# "):
            blocks.append(_block("heading_1", parse_rich_text(line[2:])))
        elif line.startswith(">"):
            quote_lines = [re.sub(r"^>\s?", "", lines[i])]
            while i + 1 < len(lines) and lines[i + 1].lstrip().startswith(">"):
                i += 1
                quote_lines.append(re.sub(r"^>\s?", "", lines[i].lstrip()))
            text = "\n".join(ql for ql in quote_lines if ql != "").strip()
            blocks.append(_block("quote", parse_rich_text(text)))
        elif _BULLET_RE.match(line):
            blocks.append(_block("bulleted_list_item", parse_rich_text(_BULLET_RE.sub("", line))))
        elif _NUMBERED_RE.match(line):
            blocks.append(_block("numbered_list_item", parse_rich_text(_NUMBERED_RE.sub("", line))))
        else:
            blocks.append(_block("paragraph", parse_rich_text(line)))
        i += 1
    return blocks
