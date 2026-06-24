# 10C AI Weekly

**Issue #1 · Wednesday, 24 June 2026**

*This issue covers the launch of a managed agent orchestration service on AWS, regulatory lobbying on AI-generated ads in Europe, new open-source long-context models, and adoption trends across manufacturing and consumer apps.*

---

## TL;DR

1. AWS launched AgentCore Harness, a managed service that reduces AI agent development to two API calls, handling concurrency and state. See *Headline of the week*.
2. Eurocommerce asked the EU to exempt AI-generated advertisements from transparency labelling under the AI Act, signalling where industry pushback will concentrate. See *The Briefs*.
3. Bloomberg reports that Europe is betting on AI to replace its retiring manufacturing workforce, with policy support accelerating adoption. See *The Briefs*.
4. Sensor Tower projects that global time spent on generative AI apps will double in 2026, with ChatGPT reaching one billion monthly active users. See *The Briefs*.

---

## Headline of the week

On 18 June at the AWS New York Summit, Amazon announced AgentCore Harness for Bedrock. This managed service lets developers create multi-agent workflows by making two API calls instead of stitching together custom infrastructure for concurrency, memory, identity, and state. The move turns agent orchestration into an operational layer that platform teams can treat as a commodity.

**Why AWS AgentCore Harness Is A Big Deal For Enterprise Agents**  
*Forbes report on the launch and its implications for enterprise multi-agent systems (Forbes, 21 June 2026)*  
[Link](https://www.forbes.com/sites/janakirammsv/2026/06/21/why-aws-agentcore-harness-is-a-big-deal-for-enterprise-agents/)

10C take: For clients building agent-based solutions for customer service, supply chain planning, or compliance monitoring, this reduces the need to build bespoke middleware. However, it also creates a new dependency on AWS’s platform. We should advise clients to design agent logic and data flows in a portable way, using the harness as a convenience layer rather than an irreversible architecture choice.

---

## The Briefs

**Models and tools**

z.AI released GLM-5.2, an open-source model with a 1 million token context window, matching the capacity of Anthropic’s Claude Opus 4.8 and OpenAI’s GPT 5.5. The model is available for on-premises deployment. (Business Insider, 21 June 2026)  
[Link](https://www.businessinsider.com/what-is-glm-5-2-chinese-ai-coding-model-2026-6)

_Why it matters to us_: European enterprises in regulated sectors can now evaluate a capable long-context model that does not require sending data to US API providers. This increases procurement flexibility and strengthens negotiation leverage with incumbent vendors.

**Regulation and governance**

Eurocommerce, whose members include Amazon, H&M, Inditex, and Ikea, asked EU tech chief Henna Virkkunen to exempt AI-generated advertisements from labelling requirements under the EU AI Act. The association argues that mandatory labels would undermine the effectiveness of AI-driven personalisation in retail marketing. (Reuters, 19 June 2026)  
[Link](https://www.reuters.com/legal/litigation/ai-generated-ads-should-be-exempt-eu-transparency-rules-retail-association-says-2026-06-19/)

_Why it matters to us_: This is the first major industry push to narrow the AI Act’s transparency rules on content. Retail and consumer goods clients with large-scale AI ad campaigns will need to monitor the regulatory outcome before designing compliance processes.

The US Department of Commerce opened the first proposal round under the American AI Exports Program. Industry consortia can submit export packages for the full US AI stack by 30 June, with priority government advocacy and potential federal financing. (Pillsbury Winthrop Shaw Pittman law firm alert, 18 June 2026)  
[Link](https://www.pillsburylaw.com/en/news-and-insights/doc-american-ai-exports-program.html)

_Why it matters to us_: European clients that depend on US hardware or cloud AI platforms should watch this program. If the US government actively promotes stack-level exports, it may change how European regulators view dependency on US technology and could trigger countermeasures or diversification strategies.

**Enterprise and industry**

Bloomberg reports that as factory workers retire across Europe, the region is making AI-driven manufacturing a strategic priority. The approach leverages Europe’s advanced industrial base rather than competing on foundation models. (Bloomberg, 18 June 2026)  
[Link](https://www.bloomberg.com/news/newsletters/2026-06-18/europe-wants-ai-in-manufacturing-before-its-workforce-retires)

Why it matters to us: Manufacturing clients should expect accelerated AI adoption in production lines, quality control, and predictive maintenance, driven by demographic necessity and policy support. Consultants should help these clients build a roadmap that integrates AI with existing MES and PLC investments.

Microsoft rolled out Anthropic’s Claude Code to thousands of employees in late 2025 but later reduced usage. The move signals a broader shift from AI hype to cost-conscious adoption within the company. (The Jerusalem Post, 22 June 2026)  
[Link](https://www.jpost.com/business-and-innovation/article-900131)

Why it matters to us: When one of the largest cloud vendors finds Claude uneconomical at scale, it reinforces the need for clients to measure total cost of ownership rigorously before committing to long-term LLM contracts. We should advise clients to run their own controlled pilots with cost tracking rather than assuming vendor benchmarks.

At Zscaler’s Zenith Live 2026, the company extended its Zero Trust Exchange platform to manage AI agents, unmanaged devices, and multi-cloud workloads, focusing on data residency and supply chain security. (CSOonline, 21 June 2026)  
[Link](https://www.csoonline.com/article/4187548/why-southeast-asia-cisos-need-zero-trust-as-their-ai-control-plane-ai-agents-data-borders-and-supply-chains.html)

Why it matters to us: As AI agents become digital workers in regulated European sectors, clients will need a security architecture that enforces data residency and access policies across agents. Zero trust is becoming a prerequisite for compliant AI deployment, not a separate project.

**Proof point**

Sensor Tower’s State of AI 2026 report forecasts a doubling of user time on generative AI apps in the first half of 2026. ChatGPT has reached one billion monthly active users and consumer spending is at record highs. (Hotel News Resource aggregator, 22 June 2026)  
[Link](https://www.hotelnewsresource.com/article141767.html) ⚠️ (Aggregator, original report not directly linked)

Why it matters to us: Rapid consumer adoption creates pressure on enterprises to match user expectations for AI assistants in customer service, employee tools, and internal knowledge retrieval. This data helps justify pilot budgets when clients ask for evidence of user demand.

At VivaTech 2026 in Paris, companies including Rebuilder AI, LVMH Dreamscape, Perfect Corp, and Stytrix demonstrated concrete generative AI applications for product design, virtual try-on, and personalised customer experience in fashion and beauty. (FashionUnited, 22 June 2026)  
[Link](https://fashionunited.in/news/fairs/vivatech-2026-how-generative-ai-is-used-by-fashion-professionals/2026062254997)

Why it matters to us: Luxury and retail clients can now point to tested, in-production use cases that move beyond prototypes. This helps de-risk similar proposals in sectors like consumer goods, hospitality, and healthcare.

---

## Client lens

This week’s developments highlight two cross-sector themes for our clients: managing the cost and lock-in of AI tooling, and preparing for regulation that will shape how AI can be used in customer-facing roles. Manufacturing clients should take the Bloomberg report as a signal to start workforce planning with AI augmentation in mind. Financial services and healthcare clients, who handle sensitive data, will benefit from the open-source model alternatives and zero-trust architectures now available. Retail clients need to track the Eurocommerce lobbying closely: if transparency rules are relaxed, the compliance burden shrinks, but if they remain, labelling workflows will be required.

---

## Conversation Starter

> “When even Microsoft pulls back on Anthropic’s Claude Code for cost reasons, it’s worth asking whether our preferred LLM partner has provided a total cost of ownership estimate that includes inference, fine-tuning, and retraining at scale.”

This opens a useful conversation about moving from proof-of-concept to production without overshooting the budget.

---

## Question of the week

**How should we advise clients to compare open-source models (like GLM-5.2) with proprietary APIs when both are viable for long-context tasks?**

Reply with your answer. We will feature a selection next week.

---

## Worth a read

- *Why AWS AgentCore Harness Is A Big Deal For Enterprise Agents* – Forbes analysis of the new managed orchestration layer on Bedrock. [Link](https://www.forbes.com/sites/janakirammsv/2026/06/21/why-aws-agentcore-harness-is-a-big-deal-for-enterprise-agents/)
- *Europe Wants AI in Manufacturing Before Its Workforce Retires* – Bloomberg on demographic-driven AI adoption in industrial settings. [Link](https://www.bloomberg.com/news/newsletters/2026-06-18/europe-wants-ai-in-manufacturing-before-its-workforce-retires)
- *AI-generated ads should be exempt from EU transparency rules, retail association says* – Reuters on Eurocommerce’s push to weaken AI Act labelling. [Link](https://www.reuters.com/legal/litigation/ai-generated-ads-should-be-exempt-eu-transparency-rules-retail-association-says-2026-06-19/)

---

*10C AI Weekly is produced for the 10C consulting team*
