"""Tests for the GitHub publisher: file written + correct blob URL in Actions."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.publish.github_publisher import GitHubPublisher


def test_writes_file_and_builds_url(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_REPOSITORY", "acme/10c-ai-weekly")
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")

    pub = GitHubPublisher({"dir": "issues", "branch": "main"})
    url = pub.publish(
        title="10C AI Weekly - Issue #1",
        markdown="# 10C AI Weekly\n\nBody.\n",
        issue_date_iso="2026-06-24",
    )
    assert url == (
        "https://github.com/acme/10c-ai-weekly/blob/main/issues/"
        "2026-06-24-10c-ai-weekly-issue-1.md"
    )
    written = list((tmp_path / "issues").glob("*.md"))
    assert written and "10C AI Weekly" in written[0].read_text(encoding="utf-8")


def test_local_run_returns_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    pub = GitHubPublisher({"dir": "issues"})
    result = pub.publish(title="Issue 2", markdown="# x\n", issue_date_iso="2026-07-01")
    assert result.endswith(".md") and os.path.exists(result)
