"""Anthropic (Claude) provider — the reference implementation.

Uses the Messages API with the server-side web search tool so the model can gather
current news and return citations. Requires env var ANTHROPIC_API_KEY.

NOTE: The web search tool type string and citation shape should be confirmed against the
current Anthropic API docs before first live run; they are isolated here so a change does
not ripple into the rest of the pipeline.
"""
from __future__ import annotations

import os

from .base import Citation, LLMProvider, LLMResponse

WEB_SEARCH_TOOL_TYPE = "web_search_20250305"  # verify against current docs


class AnthropicProvider(LLMProvider):
    supports_web_search = True

    def __init__(self, model: str, **options):
        super().__init__(model, **options)
        import anthropic  # lazy import so the package is only needed if used
        self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        web_search: bool = False,
        max_searches: int = 8,
    ) -> LLMResponse:
        tools = []
        if web_search:
            tools.append({
                "type": WEB_SEARCH_TOOL_TYPE,
                "name": "web_search",
                "max_uses": max_searches,
            })

        kwargs = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools

        resp = self._client.messages.create(**kwargs)

        text_parts: list[str] = []
        citations: list[Citation] = []
        for block in resp.content:
            btype = getattr(block, "type", None)
            if btype == "text":
                text_parts.append(block.text)
                for c in (getattr(block, "citations", None) or []):
                    url = getattr(c, "url", None)
                    if url:
                        citations.append(Citation(title=getattr(c, "title", "") or url, url=url))
            elif btype == "web_search_tool_result":
                for item in (getattr(block, "content", None) or []):
                    url = getattr(item, "url", None)
                    if url:
                        citations.append(Citation(title=getattr(item, "title", "") or url, url=url))

        return LLMResponse(text="".join(text_parts).strip(), citations=citations, raw=resp)
