# Prompt Log

A version history of every prompt the pipeline uses. Update this whenever you change a prompt
file so we can trace why an issue read the way it did. Prompts live in this `prompts/` folder
and are loaded by the pipeline at runtime, so editing a prompt file changes behaviour without
touching code.

## Prompts in use

| File | Stage | Purpose |
|---|---|---|
| `voice_system.md` | both | System prompt. Voice, tone and source-discipline rules. |
| `research.md` | research | Instructs the model to gather and verify 6 to 9 weekly developments. |
| `generate.md` | generate | Turns the verified research into the locked newsletter template. |

## Change history

### 2026-06-24 — v0.1.0 (initial)
- Created `voice_system.md`: plain/educational voice, no em dashes, no hyperbole, no AI-speak,
  mandatory sourcing. Derived from the agreed editorial standard.
- Created `research.md`: 6 to 9 verified items, category tags, source flagging, focus on
  decision-relevant developments and EU regulation.
- Created `generate.md`: encodes the locked template (TL;DR mapped to detailed sections;
  Headline of the week with per-story headline + sub-headline + individual 10C take; Briefs
  in explanatory prose; Conversation Starter; Question of the week; Worth a read). "One thing
  to try" removed per review feedback.

<!-- Template for new entries:
### YYYY-MM-DD — vX.Y.Z (short label)
- What changed and why.
-->

### 2026-06-24 — v0.2.0 (DeepSeek + Tavily)
- Added `research_queries.md`: asks a non-browsing model (DeepSeek) to propose web search
  queries. Used only in the search-augmented research path.
- `research.md` unchanged, but in search-augmented mode the pipeline appends a "Search results
  to use" block (real Tavily results) and instructs the model to cite only those sources.
