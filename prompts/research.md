# Research prompt (stage 1 of 2)

Variables substituted at runtime: {focus}, {date}, {since_date}.

---

You are researching the week's most relevant developments for an enterprise AI newsletter.

Focus area:
{focus}

Today is {date}. Only include developments from roughly the last 7 days (since {since_date}).
Use web search to verify everything. Do not rely on memory for recent events.

Find and verify 6 to 9 developments. For EACH one, capture:
1. The actual headline as published by the source.
2. A one-sentence factual summary of what happened.
3. The primary source: publication name, date, and a working URL. Prefer primary or
   reputable sources (company announcements, regulators, Reuters, CNBC, FT, official press
   releases, named research firms). Flag any item whose only source is an aggregator/blog.
4. A category tag, one of: Headline, Models and tools, Enterprise and industry,
   Regulation and governance, Proof point.
5. One sentence on why it matters specifically to a consulting team advising large European
   enterprises.

Selection rules:
- Prioritise things that change a decision a client or consultant would make.
- Include at least one regulation/governance item if any relevant one exists (EU AI Act etc).
- Include at least one real enterprise deployment or named research statistic ("proof point").
- Verify every number against a named primary source. Drop any figure you cannot source.

Output as structured Markdown: one section per development, with the fields above clearly
labelled. Mark unverified-source items with the flag emoji. Do not write the newsletter yet.
