"""Tavily web search (news topic, recency-filtered). Requires env TAVILY_API_KEY.

Free tier is ~1,000 searches/month, ample for a weekly newsletter.
"""
from __future__ import annotations

import os

import requests

from .base import SearchProvider, SearchResult

ENDPOINT = "https://api.tavily.com/search"


class TavilySearch(SearchProvider):
    def __init__(self, search_cfg: dict):
        self.days = int(search_cfg.get("days", 7))
        self.max_results = int(search_cfg.get("max_results_per_query", 5))
        self.topic = search_cfg.get("topic", "news")
        self.search_depth = search_cfg.get("search_depth", "basic")

    def search(self, query: str) -> list[SearchResult]:
        payload = {
            "api_key": os.environ.get("TAVILY_API_KEY", ""),
            "query": query,
            "topic": self.topic,
            "days": self.days,
            "max_results": self.max_results,
            "search_depth": self.search_depth,
        }
        resp = requests.post(ENDPOINT, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("results", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                content=item.get("content", ""),
                published_date=item.get("published_date", ""),
            ))
        return results
