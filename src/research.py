"""Stage 1: research.

Loads the research prompt, runs it through the configured provider with web search, and
returns a verified Markdown research brief plus the citations the provider reported.
"""
from __future__ import annotations

from datetime import date, timedelta

from .config import Config
from .prompting import load_prompt_body, render
from .providers import get_provider
from .providers.base import LLMResponse


def run_research(cfg: Config, system: str | None = None) -> LLMResponse:
    rcfg = cfg.get("research", {})
    provider = get_provider(rcfg["provider"], rcfg["model"])

    template = load_prompt_body(cfg.resolve(rcfg["prompt_file"]))
    today = date.today()
    prompt = render(
        template,
        focus=str(cfg.get("newsletter.focus", "")).strip(),
        date=today.isoformat(),
        since_date=(today - timedelta(days=7)).isoformat(),
    )

    return provider.generate(
        prompt,
        system=system,
        web_search=bool(rcfg.get("web_search", False)),
        max_searches=int(rcfg.get("max_searches", 8)),
    )
