"""Orchestrator: research -> generate -> publish -> notify.

Run weekly by GitHub Actions, or by hand:
    python -m src.main --config config.yaml
    python -m src.main --config config.yaml --dry-run            # no API publish, writes a file
    python -m src.main --config config.yaml --research-file brief.md   # skip live research
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

from .config import Config
from .generate import load_system, run_generate
from .notify import get_notifier
from .publish import get_publisher
from .research import run_research


def compute_issue_number(cfg: Config, today: date) -> int:
    first_date = cfg.get("newsletter.first_issue_date")
    first_number = int(cfg.get("newsletter.first_issue_number", 1))
    if not first_date:
        return first_number
    anchor = datetime.strptime(str(first_date), "%Y-%m-%d").date()
    weeks = max(0, (today - anchor).days // 7)
    return first_number + weeks


def human_date(d: date) -> str:
    try:
        return d.strftime("%A, %-d %B %Y")  # Linux/macOS
    except ValueError:
        return d.strftime("%A, %d %B %Y")   # Windows fallback


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the 10C AI Weekly newsletter.")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="Write to a local Markdown file and skip notifications.")
    parser.add_argument("--research-file", default=None,
                        help="Use an existing research brief instead of live research.")
    parser.add_argument("--issue-number", type=int, default=None)
    args = parser.parse_args(argv)

    cfg = Config.load(args.config)
    today = date.today()
    issue_number = args.issue_number or compute_issue_number(cfg, today)

    # Stage 1: research
    if args.research_file:
        print(f"[research] using brief from {args.research_file}")
        brief = Path(args.research_file).read_text(encoding="utf-8")
    else:
        print(f"[research] provider={cfg.get('research.provider')} model={cfg.get('research.model')}")
        result = run_research(cfg, system=load_system(cfg))
        brief = result.text
        if result.citations:
            print(f"[research] {len(result.citations)} citations gathered")

    # Stage 2: generate
    print(f"[generate] provider={cfg.get('generate.provider')} model={cfg.get('generate.model')}")
    markdown = run_generate(cfg, brief, issue_number=issue_number,
                            issue_date=human_date(today))

    # Stage 3: publish
    publisher = get_publisher(cfg, force_markdown_file=args.dry_run)
    title = f"{cfg.get('newsletter.title', '10C AI Weekly')} - Issue #{issue_number}"
    link = publisher.publish(title=title, markdown=markdown, issue_date_iso=today.isoformat())
    print(f"[publish] {link}")

    # Stage 4: notify
    notifier = get_notifier(cfg, force_none=args.dry_run)
    notifier.notify(
        subject=f"{title} draft is ready for review",
        message="This week's draft has been created. Review, edit, then set Status to Published.",
        link=link,
    )
    print("[done]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
