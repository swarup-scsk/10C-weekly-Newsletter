"""Search-augmented research flow (non-browsing provider + mock search), no network."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.research as research_mod
from src.config import Config
from src.providers.base import LLMResponse
from src.search.base import SearchProvider, SearchResult

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MockProvider:
    supports_web_search = False

    def __init__(self, *a, **k):
        pass

    def generate(self, prompt, system=None, web_search=False, max_searches=8):
        if "one query per line" in prompt.lower():
            return LLMResponse(text="ai model launch news\nEU AI Act deadline\n", citations=[])
        # synthesis call must have received the injected sources
        assert "Search results to use" in prompt
        assert "https://example.com/a" in prompt
        return LLMResponse(text="BRIEF built from sources", citations=[])


class MockSearcher(SearchProvider):
    def search(self, query):
        slug = query.split()[0].lower()
        return [SearchResult(title=f"Item {slug}", url=f"https://example.com/a-{slug}",
                             content="snippet", published_date="2026-06-20")]


def test_deepseek_registered():
    from src.providers.deepseek_provider import DeepSeekProvider
    assert DeepSeekProvider.supports_web_search is False


def test_search_augmented_research(monkeypatch):
    monkeypatch.setattr(research_mod, "get_provider", lambda *a, **k: MockProvider())
    monkeypatch.setattr(research_mod, "get_searcher", lambda *a, **k: MockSearcher())

    cfg = Config.load(os.path.join(REPO, "config.example.yaml"))
    resp = research_mod.run_research(cfg, system="sys")

    assert resp.text == "BRIEF built from sources"
    assert resp.citations and all(c.url.startswith("https://example.com/") for c in resp.citations)
