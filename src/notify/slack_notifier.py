"""Slack notifier via an incoming webhook URL."""
from __future__ import annotations

import requests

from .base import Notifier


class SlackNotifier(Notifier):
    def __init__(self, slack_cfg: dict):
        self.webhook_url = slack_cfg["webhook_url"]

    def notify(self, *, subject: str, message: str, link: str) -> None:
        text = f"*{subject}*\n{message}\n<{link}|Review the draft>"
        resp = requests.post(self.webhook_url, json={"text": text}, timeout=30)
        resp.raise_for_status()
