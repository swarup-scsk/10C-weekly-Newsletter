"""Notifier factory. Select with notify.channel in config."""
from __future__ import annotations

from .base import Notifier, NullNotifier


def get_notifier(cfg, force_none: bool = False) -> Notifier:
    channel = "none" if force_none else cfg.get("notify.channel", "none")
    if channel == "email":
        from .email_notifier import EmailNotifier
        return EmailNotifier(cfg.get("notify.email", {}))
    if channel == "slack":
        from .slack_notifier import SlackNotifier
        return SlackNotifier(cfg.get("notify.slack", {}))
    return NullNotifier()


__all__ = ["get_notifier", "Notifier", "NullNotifier"]
