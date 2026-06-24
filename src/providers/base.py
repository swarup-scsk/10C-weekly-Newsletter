"""Provider abstraction.

Every LLM provider implements the same `generate` method, so the rest of the pipeline
never needs to know which model is being used. To add a new provider, subclass
`LLMProvider`, implement `generate`, and register it in `providers/__init__.py`.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Citation:
    title: str
    url: str


@dataclass
class LLMResponse:
    text: str
    citations: list[Citation] = field(default_factory=list)
    raw: object = None


class LLMProvider(ABC):
    """Common interface for all chat/completion providers."""

    #: Whether this provider can perform live web search / grounding.
    supports_web_search: bool = False

    def __init__(self, model: str, **options):
        self.model = model
        self.options = options

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: str | None = None,
        web_search: bool = False,
        max_searches: int = 8,
    ) -> LLMResponse:
        """Return a completion for `prompt`.

        If `web_search` is True the provider should use its native search/grounding
        tool and populate `LLMResponse.citations`.
        """
        raise NotImplementedError
