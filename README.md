# 10C AI Weekly

An automated, modular pipeline that researches the week's enterprise-AI developments, drafts
the **10C AI Weekly** newsletter in a fixed editorial template and voice, publishes it to
Notion as a **Draft**, and notifies the editor. The editor reviews and edits in Notion, sets
the status to **Published**, and shares the page link with the team.

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
3. **publish** (`src/publish/`) converts the Markdown to Notion blocks and creates a Draft page
   in your database. (Or writes a local `.md` file with the `markdown_file` target / `--dry-run`.)
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

## Setup checklist

1. **Push this folder to a GitHub repo.**
2. **Notion**
   - Create an internal integration at https://www.notion.so/my-integrations and copy its
     secret (this is `NOTION_API_KEY`).
   - Create a database, e.g. "10C AI Weekly", with properties: `Name` (title), `Status`
     (status type, with a `Draft` and a `Published` option), and `Date` (date).
   - Share the database with your integration (Share -> add your integration).
   - Copy the database ID from its URL (the 32-character string). That is `NOTION_DATABASE_ID`.
3. **LLM key** for your chosen provider: `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY` /
   `GEMINI_API_KEY`).
4. **Notifications** (optional): SMTP settings for email, or `SLACK_WEBHOOK_URL` for Slack.
5. **Config:** copy `config.example.yaml` to `config.yaml`, set your providers/models and the
   Notion property names, and commit it (it holds no secrets).
6. **GitHub secrets:** in the repo, Settings -> Secrets and variables -> Actions, add the keys
   from steps 2 to 4. The workflow reads them as environment variables.
7. The workflow runs every **Wednesday 06:00 UTC**, or trigger it manually from the Actions tab.

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
pip install pytest
python -m pytest -q
```

## Notes / things to verify before first live run

- The web-search tool identifiers and citation shapes in each provider adapter are isolated at
  the top of their files. Confirm them against current provider docs before the first run.
- If your Notion `Status` property is a *select* rather than a *status* type, change the payload
  in `src/publish/notion_publisher.py` from `{"status": {...}}` to `{"select": {...}}`.
