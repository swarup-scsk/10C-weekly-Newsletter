"""Search factory. Select with research.search.provider in config."""
from __future__ import annotations

from .base import SearchProvider, SearchResult


def get_searcher(search_cfg: dict | None):
    if not search_cfg:
        return None
    provider = search_cfg.get("provider", "tavily")
    if provider in (None, "none"):
        return None
    if provider == "tavily":
        from .tavily import TavilySearch
        return TavilySearch(search_cfg)
    raise ValueError(f"Unknown search provider '{provider}'")


__all__ = ["get_searcher", "SearchProvider", "SearchResult"]
