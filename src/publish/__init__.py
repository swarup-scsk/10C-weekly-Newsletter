"""Publisher factory. Select with publish.target in config."""
from __future__ import annotations

from .base import Publisher


def get_publisher(cfg, force_markdown_file: bool = False) -> Publisher:
    target = "markdown_file" if force_markdown_file else cfg.get("publish.target", "notion")
    if target == "notion":
        from .notion_publisher import NotionPublisher
        return NotionPublisher(cfg.get("publish.notion", {}))
    if target == "markdown_file":
        from .markdown_file import MarkdownFilePublisher
        out_dir = cfg.get("publish.markdown_file.dir", "output")
        return MarkdownFilePublisher(out_dir)
    raise ValueError(f"Unknown publish target '{target}'")


__all__ = ["get_publisher", "Publisher"]
