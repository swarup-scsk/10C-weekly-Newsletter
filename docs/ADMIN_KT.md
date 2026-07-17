# 10C AI Weekly — Admin / KT Guide

A one-page handover for whoever runs the newsletter.

## What it is
An automated weekly AI newsletter for the 10C team. Every Wednesday it researches the week's
enterprise-AI news, writes an issue in a fixed template, and publishes it to a public web page.

- **Stack:** DeepSeek V4 Flash (writing) + Tavily (web search) + GitHub Actions (automation) +
  GitHub Pages (public site).
- **Runs:** every Wednesday, 06:00 UTC, automatically.
- **Current mode:** auto-publish (the issue goes live in the same run; no review gate).

## Key locations
- **Private repo (code + issues):** github.com/swarup-scsk/10C-weekly-Newsletter
- **Live newsletter:** https://swarup-scsk.github.io/10C-weekly-Newsletter/
- **Issues (source Markdown):** `issues/` in the private repo.

## The two workflows (private repo → Actions tab)
1. **10C AI Weekly** — generates the issue, commits it to `issues/`. (Scheduled + manual.)
2. **Publish site to public repo** — builds the site and deploys it to GitHub Pages (this repo). Runs
   automatically after step 1, or manually.

## Weekly routine
- Normally: nothing. It generates and publishes on its own.
- To change an issue: open the file in `issues/` → pencil icon → edit → **Commit**. The site
  redeploys automatically within ~1–2 minutes.
- To run off-schedule: Actions → **10C AI Weekly** → **Run workflow**.

## Where to edit what
| To change… | Edit… |
|---|---|
| A week's content | the `.md` file in `issues/` (GitHub web editor) |
| Format / structure | `prompts/generate.md` |
| Tone / voice rules | `prompts/voice_system.md` |
| Research topics/focus | `newsletter.focus` in `config.yaml` (+ `prompts/research*.md`) |
| Schedule | `cron` line in `.github/workflows/newsletter.yml` |
| Model / provider | `research`/`generate` in `config.yaml` |
| Site look (CSS) | `site/build_site.py` |
Log any prompt change in `prompts/PROMPT_LOG.md`.

## Accounts & secrets
API keys live as GitHub Actions **secrets** in the private repo
(Settings → Secrets and variables → Actions). Never put keys in files.
- `DEEPSEEK_API_KEY` — platform.deepseek.com
- `TAVILY_API_KEY` — tavily.com (free tier ~1,000 searches/month)
- `TEAMS_WEBHOOK_URL` — Teams channel Workflow webhook (optional; enables auto-posting)

## Costs & quotas to watch
- **DeepSeek:** pay-per-use; keep a small balance topped up. A weekly run is cents.
- **Tavily:** free tier is plenty for weekly; watch the monthly search cap.
- **GitHub:** free. Note: scheduled workflows are auto-paused after 60 days of repo inactivity —
  a commit or a manual run re-enables them.

## Troubleshooting (Actions → open the red run → read the failing step)
- **429 / quota / RESOURCE_EXHAUSTED** → DeepSeek or Tavily out of credit/quota. Top up.
- **Unknown model** → the `deepseek-v4-flash` model id changed; update `config.yaml`.
  is valid and `SITE_REPO` matches the public repo name.
- **404 on the site** → Pages not enabled on the public repo (Settings → Pages → Deploy from a
  branch → `main` / root), or wait 1–2 minutes after first deploy.
- **Links show as text** → an issue used bare URLs; the builder auto-links them on rebuild, and
  the prompt now enforces `[text](url)`.

## Good to know
- No review gate today: issues publish automatically. Ask the developer to add a `drafts/`
  review step if you want to approve before it goes public.
- The public site is world-readable (anyone with the link). Code and drafts stay private.
