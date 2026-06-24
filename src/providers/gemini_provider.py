"""Google Gemini provider.

Uses the google-genai SDK with the Google Search grounding tool. Requires env var
GEMINI_API_KEY. A cheap, search-capable option.

NOTE: grounding-metadata shape should be confirmed against current docs.
"""
from __future__ import annotations

import os

from .base import Citation, LLMProvider, LLMResponse


class GeminiProvider(LLMProvider):
    supports_web_search = True

    def __init__(self, model: str, **options):
        super().__init__(model, **options)
        from google import genai  # lazy import
        self._genai = genai
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        web_search: bool = False,
        max_searches: int = 8,
    ) -> LLMResponse:
        from google.genai import types

        cfg_kwargs = {}
        if system:
            cfg_kwargs["system_instruction"] = system
        if web_search:
            cfg_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]

        resp = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(**cfg_kwargs) if cfg_kwargs else None,
        )

        text = getattr(resp, "text", None) or ""
        citations: list[Citation] = []
        for cand in (getattr(resp, "candidates", None) or []):
            meta = getattr(cand, "grounding_metadata", None)
            for chunk in (getattr(meta, "grounding_chunks", None) or []):
                web = getattr(chunk, "web", None)
                url = getattr(web, "uri", None)
                if url:
                    citations.append(Citation(title=getattr(web, "title", "") or url, url=url))

        return LLMResponse(text=text.strip(), citations=citations, raw=resp)
