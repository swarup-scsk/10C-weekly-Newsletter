"""End-to-end dry-run test using a mock provider (no API keys, no network).

Verifies the wiring: config load -> generate (mocked) -> markdown_file publish -> file on disk.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.generate as generate_mod
from src.config import Config
from src.main import compute_issue_number, main
from src.providers.base import LLMResponse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


class _MockProvider:
    def __init__(self, *a, **k):
        pass

    def generate(self, prompt, system=None, web_search=False, max_searches=8):
        return LLMResponse(text="# 10C AI Weekly\n\n**Issue #1**\n\nMock body.\n", citations=[])


def test_compute_issue_number():
    cfg = Config.load(os.path.join(REPO, "config.example.yaml"))
    from datetime import datetime
    anchor = datetime.strptime("2026-06-24", "%Y-%m-%d").date()
    # same week -> issue 1; two weeks later -> issue 3
    assert compute_issue_number(cfg, anchor) == 1
    from datetime import timedelta
    assert compute_issue_number(cfg, anchor + timedelta(days=14)) == 3


def test_dry_run_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_mod, "get_provider", lambda *a, **k: _MockProvider())
    monkeypatch.chdir(tmp_path)

    brief = os.path.join(HERE, "fixtures", "research_brief.sample.md")
    rc = main([
        "--config", os.path.join(REPO, "config.example.yaml"),
        "--dry-run",
        "--research-file", brief,
        "--issue-number", "1",
    ])
    assert rc == 0
    written = list((tmp_path / "output").glob("*.md"))
    assert written, "expected a markdown file to be written in dry-run"
    assert "10C AI Weekly" in written[0].read_text(encoding="utf-8")
