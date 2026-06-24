"""Publish the newsletter to Notion as a Draft page in a database.

Reads NOTION_API_KEY from the environment. Property names and the draft status value are
configurable so this works with your database schema without code changes.
"""
from __future__ import annotations

import os

import requests

from .base import Publisher
from .markdown_to_notion import markdown_to_blocks

API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
MAX_CHILDREN_PER_REQUEST = 100


class NotionPublisher(Publisher):
    def __init__(self, notion_cfg: dict):
        self.database_id = notion_cfg["database_id"]
        self.title_property = notion_cfg.get("title_property", "Name")
        self.status_property = notion_cfg.get("status_property", "Status")
        self.draft_value = notion_cfg.get("draft_value", "Draft")
        self.date_property = notion_cfg.get("date_property", "Date")
        self._headers = {
            "Authorization": f"Bearer {os.environ['NOTION_API_KEY']}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def publish(self, *, title: str, markdown: str, issue_date_iso: str) -> str:
        blocks = markdown_to_blocks(markdown)

        properties = {
            self.title_property: {"title": [{"text": {"content": title}}]},
            self.status_property: {"status": {"name": self.draft_value}},
            self.date_property: {"date": {"start": issue_date_iso}},
        }

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
            "children": blocks[:MAX_CHILDREN_PER_REQUEST],
        }
        resp = requests.post(f"{API}/pages", headers=self._headers, json=payload, timeout=60)
        resp.raise_for_status()
        page = resp.json()
        page_id = page["id"]

        # Append any remaining blocks in batches of 100.
        for start in range(MAX_CHILDREN_PER_REQUEST, len(blocks), MAX_CHILDREN_PER_REQUEST):
            batch = blocks[start:start + MAX_CHILDREN_PER_REQUEST]
            r = requests.patch(
                f"{API}/blocks/{page_id}/children",
                headers=self._headers,
                json={"children": batch},
                timeout=60,
            )
            r.raise_for_status()

        return page.get("url", page_id)
