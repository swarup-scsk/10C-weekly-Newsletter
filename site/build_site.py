"""Build a static GitHub Pages site from the Markdown issues in issues/.

Reads every issues/*.md, renders each to a styled HTML page, and builds an index that lists
all issues newest-first. Output goes to _site/ for the Pages deploy workflow to publish.

Usage: python site/build_site.py [issues_dir] [output_dir]
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

import markdown  # provided by the workflow (pip install markdown)

SITE_TITLE = "10C AI Weekly"

PAGE_CSS = """
:root { --ink:#1A2E4A; --accent:#289CCA; --muted:#5b6b7f; --line:#e3e8ee; }
* { box-sizing: border-box; }
body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       color:var(--ink); line-height:1.65; background:#fff; }
.wrap { max-width: 760px; margin: 0 auto; padding: 40px 24px 80px; }
header.site { border-bottom:2px solid var(--ink); margin-bottom:32px; padding-bottom:12px; }
header.site a { color:var(--ink); text-decoration:none; font-weight:700; letter-spacing:.3px; }
h1 { font-size:1.9rem; line-height:1.2; }
h2 { font-size:1.3rem; margin-top:2em; border-bottom:1px solid var(--line); padding-bottom:.2em; }
h3 { font-size:1.05rem; margin-top:1.5em; }
a { color:var(--accent); }
blockquote { margin:1.2em 0; padding:.6em 1.1em; border-left:3px solid var(--accent);
             background:#f5fafd; color:var(--ink); }
hr { border:none; border-top:1px solid var(--line); margin:2.2em 0; }
ul.issues { list-style:none; padding:0; }
ul.issues li { padding:14px 0; border-bottom:1px solid var(--line); }
ul.issues .date { color:var(--muted); font-size:.85rem; display:block; }
footer { margin-top:60px; color:var(--muted); font-size:.85rem; }
"""

PAGE_TMPL = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{css}</style></head>
<body><div class="wrap">
<header class="site"><a href="./index.html">{site_title}</a></header>
{body}
<footer>Produced for the 10C consulting team, SCSK / Sumitomo Europe.</footer>
</div></body></html>
"""


def _date_from_name(name: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", name)
    if not m:
        return ""
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").strftime("%d %B %Y")
    except ValueError:
        return m.group(1)


def _title_from_md(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def build(issues_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    md = markdown.Markdown(extensions=["extra", "sane_lists"])

    files = sorted(issues_dir.glob("*.md"), reverse=True)
    entries = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        md.reset()
        body_html = md.convert(text)
        page_title = _title_from_md(text, f.stem)
        date_str = _date_from_name(f.name)
        out_name = f.stem + ".html"
        (out_dir / out_name).write_text(
            PAGE_TMPL.format(title=page_title, css=PAGE_CSS, site_title=SITE_TITLE, body=body_html),
            encoding="utf-8",
        )
        entries.append((out_name, page_title, date_str))

    items = "\n".join(
        f'<li><a href="./{n}">{t}</a><span class="date">{d}</span></li>'
        for n, t, d in entries
    ) or "<li>No issues published yet.</li>"
    index_body = f"<h1>{SITE_TITLE}</h1><p>Weekly AI briefing archive.</p><ul class='issues'>{items}</ul>"
    (out_dir / "index.html").write_text(
        PAGE_TMPL.format(title=SITE_TITLE, css=PAGE_CSS, site_title=SITE_TITLE, body=index_body),
        encoding="utf-8",
    )
    print(f"Built {len(entries)} issue page(s) + index into {out_dir}")


if __name__ == "__main__":
    issues = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("issues")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("_site")
    build(issues, out)
