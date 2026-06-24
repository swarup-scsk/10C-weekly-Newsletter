"""Publisher interface. Implement `publish` and return a link or path to the result."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Publisher(ABC):
    @abstractmethod
    def publish(self, *, title: str, markdown: str, issue_date_iso: str) -> str:
        """Publish the issue and return a URL (Notion) or file path (markdown_file)."""
        raise NotImplementedError
