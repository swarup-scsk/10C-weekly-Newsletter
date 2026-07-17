"""Post the latest published issue's public link to a Microsoft Teams channel.

Uses a Teams "Workflows" (Power Automate) incoming webhook. Set TEAMS_WEBHOOK_URL and
SITE_BASE_URL in the environment. If TEAMS_WEBHOOK_URL is not set, this is a no-op.

Run after the site has been published (see pages.yml).
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests


def _newest_issue(issues_dir: Path):
    files = sorted(issues_dir.glob("*.md"), reverse=True)
    return files[0] if files else None


def _title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _date(name: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", name)
    if not m:
        return ""
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").strftime("%d %B %Y")
    except ValueError:
        return m.group(1)


def main() -> int:
    webhook = os.environ.get("TEAMS_WEBHOOK_URL", "").strip()
    if not webhook:
        print("[teams] TEAMS_WEBHOOK_URL not set; skipping.")
        return 0

    base = os.environ.get("SITE_BASE_URL", "").rstrip("/")
    issues_dir = Path(os.environ.get("ISSUES_DIR", "issues"))
    latest = _newest_issue(issues_dir)
    if latest is None:
        print("[teams] no issues found; skipping.")
        return 0

    text = latest.read_text(encoding="utf-8")
    title = _title(text, latest.stem)
    date_str = _date(latest.name)
    url = f"{base}/{latest.stem}.html"

    card = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.4",
                "body": [
                    {"type": "TextBlock", "size": "Medium", "weight": "Bolder",
                     "text": "10C AI Weekly"},
                    {"type": "TextBlock", "spacing": "None", "isSubtle": True,
                     "text": date_str, "wrap": True},
                    {"type": "TextBlock", "text": title, "wrap": True},
                ],
                "actions": [
                    {"type": "Action.OpenUrl", "title": "Read this week's issue", "url": url}
                ],
            },
        }],
    }

    resp = requests.post(webhook, json=card, timeout=30)
    resp.raise_for_status()
    print(f"[teams] posted: {title} -> {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
