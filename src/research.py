"""Stage 1: research.

Two modes, chosen automatically:
  - Native: if the provider supports web search (Anthropic/OpenAI/Gemini) and it is enabled,
    the provider gathers and cites sources itself.
  - Search-augmented: if the provider cannot browse (e.g. DeepSeek), we ask it to propose search
    queries, run them through the configured search tool (e.g. Tavily), then feed the real
    results back for it to synthesise and cite.
"""
from __future__ import annotations

from datetime import date, timedelta

from .config import Config
from .prompting import load_prompt_body, render
from .providers import get_provider
from .providers.base import Citation, LLMResponse
from .search import get_searcher


def _focus(cfg: Config) -> str:
    return str(cfg.get("newsletter.focus", "")).strip()


def _generate_queries(cfg, provider, system, today, since) -> list[str]:
    qfile = cfg.get("research.query_prompt_file", "prompts/research_queries.md")
    template = load_prompt_body(cfg.resolve(qfile))
    num = int(cfg.get("research.search.num_queries", 6))
    prompt = render(
        template,
        focus=_focus(cfg),
        date=today.isoformat(),
        since_date=since.isoformat(),
        num_queries=num,
    )
    resp = provider.generate(prompt, system=system, web_search=False)
    queries = []
    for line in resp.text.splitlines():
        q = line.strip().lstrip("-*0123456789. ").strip()
        if q:
            queries.append(q)
    return queries[:num]


def run_research(cfg: Config, system: str | None = None) -> LLMResponse:
    rcfg = cfg.get("research", {})
    provider = get_provider(rcfg["provider"], rcfg["model"])

    days = int(cfg.get("research.search.days", 7))
    today = date.today()
    since = today - timedelta(days=days)

    template = load_prompt_body(cfg.resolve(rcfg["prompt_file"]))
    base_prompt = render(
        template,
        focus=_focus(cfg),
        date=today.isoformat(),
        since_date=since.isoformat(),
    )

    # Native web search path.
    if rcfg.get("web_search", False) and getattr(provider, "supports_web_search", False):
        return provider.generate(
            base_prompt, system=system, web_search=True,
            max_searches=int(rcfg.get("max_searches", 8)),
        )

    # Search-augmented path (provider cannot browse).
    searcher = get_searcher(cfg.get("research.search", {}))
    if searcher is None:
        # No search configured: last-resort plain generation (not recommended).
        return provider.generate(base_prompt, system=system, web_search=False)

    queries = _generate_queries(cfg, provider, system, today, since)
    results = []
    seen = set()
    for q in queries:
        try:
            hits = searcher.search(q)
        except Exception as exc:  # one bad query should not sink the run
            print(f"[research] search failed for '{q}': {exc}")
            continue
        for r in hits:
            if r.url and r.url not in seen:
                seen.add(r.url)
                results.append(r)

    blocks, citations = [], []
    for i, r in enumerate(results, 1):
        blocks.append(
            f"[{i}] {r.title}\nURL: {r.url}\nDate: {r.published_date or 'n/a'}\n"
            f"{(r.content or '')[:600]}"
        )
        citations.append(Citation(title=r.title or r.url, url=r.url))
    sources_block = "\n\n".join(blocks) if blocks else "(no results found)"

    augmented = base_prompt + (
        "\n\n## Search results to use\n"
        "Use ONLY the sources below. Do not invent other sources, figures, or quotes. "
        "Cite the URL of each source you rely on, and drop anything you cannot support "
        "from these results.\n\n" + sources_block
    )
    resp = provider.generate(augmented, system=system, web_search=False)
    resp.citations = citations
    return resp
