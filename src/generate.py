"""Stage 2: generate.

Loads the generate prompt and the voice system prompt, injects the research brief, and asks
the configured provider to produce the final newsletter Markdown in the locked template.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from .config import Config
from .prompting import load_prompt_body, render
from .providers import get_provider


def load_system(cfg: Config) -> str:
    system_file = cfg.get("generate.system_file")
    if not system_file:
        return ""
    return Path(cfg.resolve(system_file)).read_text(encoding="utf-8").strip()


def run_generate(
    cfg: Config,
    research_brief: str,
    issue_number: int,
    issue_date: str | None = None,
) -> str:
    gcfg = cfg.get("generate", {})
    provider = get_provider(gcfg["provider"], gcfg["model"])

    template = load_prompt_body(cfg.resolve(gcfg["prompt_file"]))
    if issue_date is None:
        issue_date = date.today().strftime("%A, %-d %B %Y")

    prompt = render(
        template,
        title=cfg.get("newsletter.title", "10C AI Weekly"),
        issue_number=issue_number,
        date=issue_date,
        audience=str(cfg.get("newsletter.audience", "")).strip(),
        research_brief=research_brief,
    )

    resp = provider.generate(prompt, system=load_system(cfg), web_search=False)
    return resp.text
