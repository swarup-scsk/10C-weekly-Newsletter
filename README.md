# 10C AI Weekly

An automated, modular pipeline that researches the week's enterprise-AI developments, drafts
the **10C AI Weekly** newsletter in a fixed editorial template and voice, and publishes it
(by default, as a Markdown file committed to this repo). The editor reviews and edits it, then
shares the link with the team. Notion and other targets are supported by changing one config line.

The build is deliberately modular: every stage names its provider and model in `config.yaml`,
so you can swap the LLM (Anthropic, OpenAI, Gemini, or your own) or the publish/notify target
without changing pipeline code. All prompts live in `prompts/` and are versioned in
`prompts/PROMPT_LOG.md`.

## How it works

```
research  ->  generate  ->  publish  ->  notify
(LLM +        (LLM +        (Notion or   (email /
 web search)   template)     md file)     slack)
```

1. **research** (`src/research.py`) runs the `prompts/research.md` prompt through the configured
   provider with web search, returning a verified Markdown research brief with sources.
2. **generate** (`src/generate.py`) feeds that brief into `prompts/generate.md` (plus the voice
   rules in `prompts/voice_system.md`) to produce the final newsletter Markdown.
3. **publish** (`src/publish/`) writes the issue where you've configured it:
   - `github` (default): commits the issue as a Markdown file in the repo's `issues/` folder
     and returns a github.com link. Edit it in the GitHub web editor, then share the link.
   - `notion`: converts the Markdown to Notion blocks and creates a Draft page in a database.
   - `markdown_file` / `--dry-run`: writes a local `.md` file for previewing.
4. **notify** (`src/notify/`) emails or Slacks you a link to review.

## Project layout

```
config.example.yaml      Copy to config.yaml and edit. No secrets live here.
prompts/                 All prompts + PROMPT_LOG.md (version history)
src/
  config.py              YAML loader with ${ENV} expansion
  providers/             LLM abstraction + anthropic / openai / gemini adapters
  research.py            Stage 1
  generate.py            Stage 2
  publish/               Notion publisher, markdown_file fallback, md->blocks converter
  notify/                email / slack / none
  main.py                Orchestrator + CLI
tests/                   Converter unit tests + dry-run pipeline test (mock provider)
.github/workflows/       Weekly cron (Wednesday)
```

## Setup checklist (GitHub publishing — default)

1. **Push this folder to a GitHub repo** (private is fine).
2. **LLM key** for your chosen provider, e.g. `GEMINI_API_KEY` (or `ANTHROPIC_API_KEY` /
   `OPENAI_API_KEY`). Gemini keys come from Google AI Studio.
3. **Config:** copy `config.example.yaml` to `config.yaml`, set your provider/model, keep
   `publish.target: github`, and commit it (it holds no secrets).
4. **GitHub secret:** repo Settings -> Secrets and variables -> Actions -> add `GEMINI_API_KEY`
   (and any others you use). The workflow already has permission to commit issues back.
5. Run the workflow manually (Actions tab -> Run workflow) to test. A new file appears in
   `issues/`. After that it runs every **Wednesday 06:00 UTC**.
6. **Each week:** open the new file in `issues/`, click the pencil to edit in GitHub, commit,
   then share the file's link with the team.

   Note: a github.com file link is only viewable by people with access to the repo. If your
   team is not on GitHub, enable GitHub Pages (or add them as repo collaborators) so they can
   open the link. Ask if you want Pages set up.

### Optional: publish to Notion instead

Set `publish.target: notion` and provide `NOTION_API_KEY` + `NOTION_DATABASE_ID`. Create a
database with `Name` (title), `Status` (status type with Draft/Published) and `Date` (date)
properties, and share it with your Notion integration.

## Run locally

```bash
pip install -r requirements.txt

# Full run (needs the relevant API keys in your environment):
python -m src.main --config config.yaml

# Dry run: writes a local Markdown file, no Notion, no notification:
python -m src.main --config config.yaml --dry-run

# Skip live research and use a saved brief:
python -m src.main --config config.yaml --research-file tests/fixtures/research_brief.sample.md
```

## Swapping the model or provider

Edit `config.yaml`. The research and generate stages are independent:

```yaml
research:
  provider: gemini          # cheap + has search
  model: "gemini-2.5-flash"
generate:
  provider: anthropic       # stronger writer for the final prose
  model: "claude-opus-4-8"
```

To add a **new provider**, create `src/providers/<name>_provider.py` subclassing `LLMProvider`,
implement `generate`, and register it in `src/providers/__init__.py`. Nothing else changes.

To add a **new publish or notify target**, subclass `Publisher` / `Notifier` and register it in
the respective `__init__.py`.

## Editing the newsletter format

Change `prompts/generate.md` (structure) or `prompts/voice_system.md` (tone/rules). Record the
change in `prompts/PROMPT_LOG.md` so issues remain traceable.

## Tests

```bash
pip install pytest pyyaml
python -m pytest -q
```

## Notes / things to verify before first live run

- The web-search tool identifiers and citation shapes in each provider adapter are isolated at
  the top of their files. Confirm them against current provider docs before the first run.
- A github.com file link is only viewable by people with repo access. If your team is not on
  GitHub, enable GitHub Pages or add them as collaborators so they can open the shared link.
- If you switch to Notion and your `Status` property is a *select* rather than a *status* type,
  change the payload in `src/publish/notion_publisher.py` from `{"status": {...}}` to
  `{"select": {...}}`.

## Using a non-browsing model (e.g. DeepSeek) + Tavily

DeepSeek has no built-in web search. Set `research.search.provider: tavily` and add a
`TAVILY_API_KEY` secret (free tier ~1,000 searches/month). The pipeline then asks the model for
search queries, runs them through Tavily, and feeds the real results back for the model to
synthesise and cite. Set the provider to `deepseek` and model to `deepseek-v4-flash`, with
`DEEPSEEK_API_KEY` as a secret. The base URL is https://api.deepseek.com (OpenAI-compatible).

## Public sharing via GitHub Pages (this repo)

The repo is public, so it serves the newsletter directly via GitHub Pages. No
separate site repo is needed.

One-time: repo Settings -> Pages -> Build and deployment -> Source: **GitHub Actions**.

After that, every new issue (or manual edit) builds `issues/*.md` into a site and
deploys it to https://swarup-scsk.github.io/10C-weekly-Newsletter/ via the "Publish to GitHub Pages" workflow, which runs
automatically after the weekly newsletter workflow completes.

