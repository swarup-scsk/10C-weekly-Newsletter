"""Web-search abstraction. Implement `search` to return recent, relevant results.

Used to give non-browsing LLMs (e.g. DeepSeek) a source of current, citable news.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    content: str = ""
    published_date: str = ""


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> list[SearchResult]:
        raise NotImplementedError
