"""DeepSeek provider (OpenAI-compatible Chat Completions API).

DeepSeek V4 Flash is the non-reasoning model `deepseek-v4-flash`. The API is OpenAI-compatible,
so we use the openai SDK pointed at https://api.deepseek.com. Requires env DEEPSEEK_API_KEY.

DeepSeek has no hosted web-search tool, so `supports_web_search` is False. Live news comes from
the separate search module (see src/search), wired in src/research.py.
"""
from __future__ import annotations

import os

from .base import LLMProvider, LLMResponse

DEFAULT_BASE_URL = "https://api.deepseek.com"


class DeepSeekProvider(LLMProvider):
    supports_web_search = False

    def __init__(self, model: str, **options):
        super().__init__(model, **options)
        from openai import OpenAI  # lazy import; DeepSeek speaks the OpenAI API
        self._client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url=options.get("base_url", DEFAULT_BASE_URL),
        )

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        web_search: bool = False,
        max_searches: int = 8,
    ) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=8000,
        )
        text = (resp.choices[0].message.content or "").strip()
        return LLMResponse(text=text, citations=[], raw=resp)
