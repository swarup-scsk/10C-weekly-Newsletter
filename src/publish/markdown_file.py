"""Fallback publisher: write the issue to a local Markdown file.

Used when publish.target = markdown_file and by --dry-run. Handy for previewing without
touching Notion or any API.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from .base import Publisher


class MarkdownFilePublisher(Publisher):
    def __init__(self, out_dir: str = "output"):
        self.out_dir = Path(out_dir)

    def publish(self, *, title: str, markdown: str, issue_date_iso: str) -> str:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        slug = title.lower().replace(" ", "-").replace("#", "").replace("·", "-")
        slug = "-".join(filter(None, slug.split("-")))
        filename = f"{issue_date_iso or date.today().isoformat()}-{slug}.md"
        path = self.out_dir / filename
        path.write_text(markdown, encoding="utf-8")
        return str(path.resolve())
