"""Notifier interface. Implement `notify` to tell the editor a draft is ready."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def notify(self, *, subject: str, message: str, link: str) -> None:
        raise NotImplementedError


class NullNotifier(Notifier):
    def notify(self, *, subject: str, message: str, link: str) -> None:
        print(f"[notify:none] {subject} -> {link}")
