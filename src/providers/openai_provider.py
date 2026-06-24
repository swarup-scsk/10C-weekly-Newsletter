"""OpenAI provider.

Uses the Responses API with the built-in web_search tool. Requires env var OPENAI_API_KEY.

NOTE: tool name and output parsing should be confirmed against current OpenAI docs.
Implemented behind the same interface so it can be selected in config without code changes
elsewhere.
"""
from __future__ import annotations

import os

from .base import Citation, LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    supports_web_search = True

    def __init__(self, model: str, **options):
        super().__init__(model, **options)
        from openai import OpenAI  # lazy import
        self._client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        web_search: bool = False,
        max_searches: int = 8,
    ) -> LLMResponse:
        kwargs = {"model": self.model, "input": prompt}
        if system:
            kwargs["instructions"] = system
        if web_search:
            kwargs["tools"] = [{"type": "web_search"}]

        resp = self._client.responses.create(**kwargs)

        text = getattr(resp, "output_text", None) or ""
        citations: list[Citation] = []
        # Walk annotations for URL citations where available.
        for item in (getattr(resp, "output", None) or []):
            for content in (getattr(item, "content", None) or []):
                for ann in (getattr(content, "annotations", None) or []):
                    url = getattr(ann, "url", None)
                    if url:
                        citations.append(Citation(title=getattr(ann, "title", "") or url, url=url))

        return LLMResponse(text=text.strip(), citations=citations, raw=resp)
