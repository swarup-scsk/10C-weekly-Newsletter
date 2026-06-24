# Research query prompt (stage 1a, used when the LLM cannot search the web itself)

Variables substituted at runtime: {focus}, {date}, {since_date}, {num_queries}.

---

You are preparing to research this week's developments for an enterprise AI newsletter.

Focus area:
{focus}

Today is {date}. We want developments from the last week (since {since_date}).

Write {num_queries} web search queries that, run against a news search engine, would surface
the most relevant and recent developments. Cover a spread: new models and tools, enterprise and
industry deployments, regulation and governance (such as the EU AI Act), and notable research or
proof points.

Output one query per line. No numbering, no bullet points, no commentary. Just the queries.
