"""Publish the newsletter as a Markdown file inside the repo.

The file is written to a folder (default `issues/`). The GitHub Actions workflow commits and
pushes it. The returned link is the rendered file URL on github.com, built from the standard
Actions environment variables, so you can share it directly.

Editing flow: open the committed file in GitHub's web editor (pencil icon), make your edits,
commit, then share the link with the team.
"""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from .base import Publisher


def _slug(title: str) -> str:
    out = title.lower()
    for ch in ("#", "·", ":", "/", "\\", ",", "-"):
        out = out.replace(ch, " ")
    return "-".join(part for part in out.split() if part)


class GitHubPublisher(Publisher):
    def __init__(self, gh_cfg: dict):
        self.dir = Path(gh_cfg.get("dir", "issues"))
        self.branch = gh_cfg.get("branch", "main")

    def publish(self, *, title: str, markdown: str, issue_date_iso: str) -> str:
        self.dir.mkdir(parents=True, exist_ok=True)
        stamp = issue_date_iso or date.today().isoformat()
        filename = f"{stamp}-{_slug(title)}.md"
        path = self.dir / filename
        path.write_text(markdown, encoding="utf-8")

        repo = os.environ.get("GITHUB_REPOSITORY")
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        if repo:
            return f"{server}/{repo}/blob/{self.branch}/{self.dir.as_posix()}/{filename}"
        # Local run (no Actions env): return the file path.
        return str(path.resolve())
