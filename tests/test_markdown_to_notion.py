"""Unit tests for the Markdown -> Notion block converter."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.publish.markdown_to_notion import markdown_to_blocks, parse_rich_text


def test_headings_and_divider():
    blocks = markdown_to_blocks("# Title\n\n## Section\n\n### Sub\n\n---\n")
    types = [b["type"] for b in blocks]
    assert types == ["heading_1", "heading_2", "heading_3", "divider"]


def test_paragraph_and_lists():
    md = "A paragraph.\n\n- bullet one\n- bullet two\n\n1. first\n2. second\n"
    blocks = markdown_to_blocks(md)
    types = [b["type"] for b in blocks]
    assert types == [
        "paragraph",
        "bulleted_list_item",
        "bulleted_list_item",
        "numbered_list_item",
        "numbered_list_item",
    ]


def test_multiline_quote():
    md = "> line one\n> line two\n"
    blocks = markdown_to_blocks(md)
    assert len(blocks) == 1
    assert blocks[0]["type"] == "quote"
    text = "".join(rt["text"]["content"] for rt in blocks[0]["quote"]["rich_text"])
    assert "line one" in text and "line two" in text


def test_inline_link():
    rich = parse_rich_text("See [CNBC](https://cnbc.com) today.")
    linked = [r for r in rich if r["text"].get("link")]
    assert linked and linked[0]["text"]["link"]["url"] == "https://cnbc.com"
    assert linked[0]["text"]["content"] == "CNBC"


def test_inline_bold_and_italic():
    rich = parse_rich_text("**bold** and *italic* text")
    bold = [r for r in rich if r.get("annotations", {}).get("bold")]
    italic = [r for r in rich if r.get("annotations", {}).get("italic")]
    assert bold and bold[0]["text"]["content"] == "bold"
    assert italic and italic[0]["text"]["content"] == "italic"


def test_long_text_is_truncated():
    rich = parse_rich_text("x" * 5000)
    assert len(rich[0]["text"]["content"]) <= 1900
