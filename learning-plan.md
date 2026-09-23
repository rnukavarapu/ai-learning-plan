# AI & Agentic Development Learning Plan

## Context

You're starting from zero on AI/LLM and agentic development and want a structured, sequential path to genuine hands-on competence — not just familiarity with which buttons to click. You can spend about 6 hrs/week, and want all four pillars covered: LLM foundations, agentic systems, RAG, and MLOps/LLMOps.

The plan below is sequenced so each phase's concepts are prerequisites for the next. Phase 0 and Phase 1 go deeper than a typical "quick start" — more foundational videos and concepts than you might expect from just two phases — because everything later (RAG, agents, evaluation) leans on actually understanding tokens, embeddings, and how these models behave, not just knowing which library to import. Every phase now also ends with a **🧪 Test yourself** block — a short quiz plus a small task — before the checkpoint, so you're actively checking retention instead of just recognizing things as familiar.

**Pace assumption:** ~6 hrs/week, ~20 weeks (~4.5-5 months) for Phases 0-5, plus an open-ended Phase 6 capstone. If a week is heavier or lighter, shift the checkpoint dates rather than skipping content — the sequencing matters more than the calendar.

**Free vs. paid:** Everything below is free unless explicitly marked **[PAID]**, in which case I've noted price/why it might be worth it and a free alternative.

**Local repos:** Four GitHub repos are cloned locally under `reference-repos/` (one per phase where hands-on code matters most — Phases 1, 2, 3, 4). They're referenced inline in the relevant phase below rather than as a separate list — these are deliberately the *only* repos in this plan; more wasn't more useful.

---

## Phase 0 — Orientation & Mental Models (Weeks 1-2, ~13 hrs)

Goal: build an accurate, durable mental model of what these systems actually are — and aren't — before touching any code.

- **Anthropic Academy — "AI capabilities and limitations"** (free, ~3.5h) — [academy.claude.com](https://academy.claude.com/courses) — covers next-token prediction, knowledge, working memory, steerability, context limits. Best single resource for a solid mental model.
- **Anthropic Academy — "AI Fluency: Framework and foundations"** (free, ~4h) — the 4D framework (Delegation, Description, Discernment, Diligence) for working with AI systems thoughtfully rather than trusting output blindly.
- **Anthropic — "Building Effective Agents"** (free blog post, ~30 min) — [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents) — the canonical framing of agents vs. workflows. You won't build one for a few phases yet, but the vocabulary is worth having early.

**🎥 Watch first (all free, YouTube):**

- IBM Technology — ["What are Generative AI models?"](https://www.youtube.com/watch?v=hfIUstzHs9A) (~9 min) — the broadest possible starting point.
- 3Blue1Brown — ["But what is a neural network?"](https://www.youtube.com/watch?v=aircAruvnKk) (19 min) — the single best "no math background needed" visual intuition for what's actually happening inside a model.
- IBM Technology — ["How Large Language Models Work"](https://www.youtube.com/watch?v=5sLYAQS9sWQ) (~8 min) — narrows the previous two videos down to LLMs specifically.
- 3Blue1Brown — ["Large Language Models explained briefly"](https://www.youtube.com/watch?v=LPZh9BOjkQs) (8 min) — fast recap that ties the previous three together.
- IBM Technology — ["Why Large Language Models Hallucinate"](https://www.youtube.com/watch?v=cfqtFvWOfg0) (~9 min) — directly answers "why does it just make things up sometimes," which is the single most common confusion at this stage.
- IBM Technology — ["What are AI Agents?"](https://www.youtube.com/watch?v=F8NKVhkZZWI) (~9 min) — a preview of where this is all heading (Phase 4); IBM's channel is consistently good for crisp, jargon-light 10-minute explainers — worth searching it directly whenever a term below is unfamiliar (e.g. "vector database," "fine-tuning").

**Big picture (optional):** skim a16z's "AI Canon" reading list (free) and Anthropic's Economic Index reports (free) if you want the wider context of how this technology is playing out beyond your own learning. Not required to move on.

**🧪 Test yourself:**

- Quiz, no notes: What is a token? Why does an LLM sometimes state something false with total confidence? What's the difference between a "workflow" and an "agent"?
- Task: explain what an LLM is to a friend or family member who isn't technical, in under 2 minutes, without saying "AI" more than once. If they can repeat the core idea back to you afterward, you've actually got it — if you find yourself hand-waving, that's exactly the part to go re-watch.

**Checkpoint:** You can explain to someone else, in plain language, what an LLM is doing, why it hallucinates, and the difference between a "workflow" and an "agent."

---

## Phase 1 — LLM Foundations & Prompting (Weeks 3-6, ~26 hrs)

Goal: understand tokens, embeddings, and context well enough to reason about *why* things work, and become genuinely skilled at prompting — the mechanics underneath everything you'll build later.

### Tokens & tokenization

**🎥 Watch first:**

- Hugging Face — ["The tokenization pipeline"](https://www.youtube.com/watch?v=Yffk5aydLzg) — short conceptual overview of how text becomes the units a model processes.
- Optional, deeper: Andrej Karpathy — ["Let's build the GPT Tokenizer"](https://www.youtube.com/watch?v=zduSFxRajkE) (~2h) — build one from scratch, byte by byte. This is the real depth version of the concept above if the short video leaves you wanting more.

**Hands-on (5 min):** OpenAI's [Tokenizer tool](https://platform.openai.com/tokenizer) — paste in a sentence and watch it split into tokens in real time. Makes "context window" a concrete, countable thing instead of an abstraction.

### Embeddings (the concept)

**🎥 Watch first:**

- StatQuest — ["Word Embedding and Word2Vec, Clearly Explained!!!"](https://www.youtube.com/watch?v=viZrOnJclY0) — the foundational idea (text → vectors, similarity via distance) before Phase 3 applies it to search. Understanding this now makes RAG click much faster later instead of feeling like magic.

### How these models are actually built

- **DeepLearning.AI — "Attention in Transformers: Concepts and Code in PyTorch"** (free, StatQuest, ~1h15m) — if you want one level deeper into the actual mechanism.

**🎥 Watch first:**

- 3Blue1Brown — ["Transformers, the tech behind LLMs"](https://www.youtube.com/watch?v=wjZofJX0v4M) (~27 min) and ["Attention in transformers, step-by-step"](https://www.youtube.com/watch?v=eMlx5fFNoYc) (~26 min) — the visual deep-dive companion to the StatQuest course above.
- Optional alternate style: StatQuest — ["Transformer Neural Networks, ChatGPT's foundation, Clearly Explained!!!"](https://www.youtube.com/watch?v=zxQyTK8quyY) — if 3Blue1Brown's animation-heavy explanation isn't clicking, this covers the same ground differently.
- Andrej Karpathy — ["[1hr Talk] Intro to Large Language Models"](https://www.youtube.com/watch?v=zjkBMFhNj_g) — the best single mid-length overview once you've done the videos above; covers training, capabilities, and limitations in plain language.
- Andrej Karpathy — ["How I use LLMs"](https://www.youtube.com/watch?v=EWvNQjAaOHw) — practical, not theoretical: how a leading practitioner actually uses these tools day to day.

Optional deeper dive (skip if time is tight — nothing later depends on these):

- Karpathy's ["Deep Dive into LLMs like ChatGPT"](https://www.youtube.com/watch?v=7xTGNNLPyMI) (~3.5h) — the full technical version of everything above in one sitting.
- **Andrej Karpathy — "Let's build GPT: from scratch, in code"** (free, YouTube, ~2h) — the single best resource if you want to *really* understand the mechanics rather than just use the API.
- Andrej Karpathy — ["Let's reproduce GPT-2 (124M)"](https://www.youtube.com/watch?v=l8pRSuU81PU) (~4h) — the furthest-depth option in this whole plan: training an actual GPT-2-scale model from scratch. Only for if "Let's build GPT" wasn't enough and you want the full production-grade version.
- **Repo (pairs with the video above):** [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) — cloned locally at `reference-repos/LLMs-from-scratch`. Sebastian Raschka's step-by-step PyTorch build of a GPT-style model. Only open this if you did the Karpathy video and want the more polished, book-quality version of the same exercise.

### Prompting

- **DeepLearning.AI — "AI Prompting for Everyone"** (free, Andrew Ng, ~7h) — solid, non-code-heavy prompting foundations.
- **Prompt Engineering Guide** (free, [promptingguide.ai](https://www.promptingguide.ai/)) — reference the Techniques and Agents sections as you go (zero-shot, few-shot, chain-of-thought, ReAct); use as an ongoing reference, not a linear read.
- **Anthropic's own prompt engineering docs** (free, [docs.claude.com](https://docs.claude.com) → "Prompt engineering") — practical, example-heavy, and matches what you'll use hands-on later.

**Hands-on (start now, ~2 hrs):** Get an Anthropic Console or OpenAI API key (both have free trial credit) and just talk to the API directly in a Python script or notebook — no framework. Confirms you understand context windows, system prompts, and message formatting before any framework hides it from you. Then run the same prompt twice — once with `temperature=0`, once with `temperature=1` — and compare the outputs side by side. Makes the abstract idea of "sampling" concrete instead of a parameter you set and forget.

**🧪 Test yourself:**

- Quiz, no notes: what does temperature actually control? What's an embedding, in one sentence? Roughly how many tokens is an average paragraph of English text?
- Task: take a prompt you'd write for something totally unrelated to this plan (an email, a recipe, a to-do list) and rewrite it using two techniques from the Prompt Engineering Guide (e.g. few-shot examples, chain-of-thought). Run both versions and compare the outputs — can you predict which technique would help *before* you see the result?

**Checkpoint:** You can explain what a token and an embedding are without notes, describe what changing temperature actually does, write a well-structured prompt with role, context, and examples, and you've made at least one raw API call in Python.

---

## Phase 2 — Hands-On Building Basics (Weeks 7-9, ~17 hrs)

Goal: comfortable writing small Python programs that call LLMs, handle structured output, and chain calls together — the substrate everything else (RAG, agents) sits on.

- **DeepLearning.AI — "Pydantic for LLM Workflows"** (free, ~1h50m) — structured/validated output; you'll use this pattern everywhere afterward.
- **DeepLearning.AI short courses catalog** ([deeplearning.ai/courses](https://www.deeplearning.ai/courses/)) — pick 2-3 beginner/intermediate courses matching gaps you feel. All free with email signup.
- **OpenAI Cookbook** (free, [cookbook.openai.com](https://cookbook.openai.com)) — practical recipes for function calling, structured outputs, batching — vendor-agnostic patterns even if you use Claude day-to-day.
- **Repo:** [anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) — cloned locally at `reference-repos/anthropic-cookbook`. This is the one to actually work through hands-on: tool use, structured extraction, and multimodal recipes as runnable notebooks.

**Hands-on project (the important part):** Build a small CLI or notebook tool that takes unstructured text (e.g., a batch of product reviews, support tickets, or short news articles) and uses an LLM with structured (Pydantic) output to classify/summarize it. Keep it small and real.

**🧪 Test yourself:**

- Task: run your script on 10 new examples you did *not* look at while building it. Count how many outputs are actually correct/useful without you reading the code to justify them — a fresh-eyes accuracy check, not a "does it run" check.
- Quiz, no notes: what's the actual benefit of validating LLM output against a Pydantic schema instead of just parsing the raw text with string matching or regex?

**Checkpoint:** A working script in a repo that calls an LLM API, validates its output against a schema, and does something useful with real (or realistic) data.

---

## Phase 3 — RAG & Knowledge Systems (Weeks 10-13, ~22 hrs)

Goal: RAG is fundamentally a data pipeline problem (ingestion, chunking, indexing, retrieval) wrapped around an LLM — and now you already have the embeddings concept from Phase 1 to make sense of the "retrieval" half.

- **DeepLearning.AI — "Retrieval Augmented Generation (RAG)"** (free, ~26h total but modular — pace it across the phase) — architecture through deployment and evaluation of production RAG.
- **DeepLearning.AI — "Advanced Retrieval for AI with Chroma"** (free, ~1h) — query relevancy, why naive retrieval fails.
- **Pinecone Learning Center** (free, [pinecone.io/learn](https://www.pinecone.io/learn/)) — explainers on embeddings applied to vector search and chunking strategies specifically.
- **LlamaIndex documentation** (free, [docs.llamaindex.ai](https://docs.llamaindex.ai)) — the most RAG-native framework; work through their basic RAG tutorial.
- **LLM Zoomcamp by DataTalksClub** (free, self-paced via GitHub, [github.com/DataTalksClub/llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)) — a full free course covering RAG, vector search, evaluation, and monitoring. Treat this as the spine of this phase if you only pick one thing.
- **Repo:** [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) — cloned locally at `reference-repos/RAG_Techniques`. The best hands-on complement to LLM Zoomcamp: standalone runnable notebooks for chunking strategies, re-ranking, query rewriting, and RAG evaluation. Pick 4-5 notebooks relevant to your project below rather than working through all of them.

**🎥 Watch first (all free, YouTube):**

- IBM Technology — ["What is Retrieval-Augmented Generation (RAG)?"](https://www.youtube.com/watch?v=T-D1OfcDW1M) (~7 min) — the fast conceptual overview before you touch code.
- freeCodeCamp — ["Learn RAG From Scratch – Python AI Tutorial from a LangChain Engineer"](https://www.youtube.com/watch?v=sVcwVQRHIc8) (full-length, several hours) — a complete build-along tutorial; treat it as a spine you dip into alongside the RAG_Techniques notebooks rather than watching start to finish in one sitting.

**Hands-on project:** Build a RAG assistant over something you actually have — personal notes, a hobby project's docs, articles you've saved, or any body of text you care about being able to query. This becomes a concrete artifact you built and understand end-to-end.

**🧪 Test yourself:**

- Task: ask your RAG assistant 5 questions it has no business being able to answer from its corpus (genuinely out-of-scope). Does it correctly say "I don't know," or does it hallucinate a confident-sounding answer anyway? This single test matters more than any accuracy metric on the questions it's *supposed* to answer.
- Quiz, no notes: list the steps in a RAG pipeline, in order, from ingestion to generation, without looking back at your own code.

**Checkpoint:** A working RAG pipeline (ingest → chunk → embed → store → retrieve → generate) over a real corpus, with a rough sense of where retrieval quality breaks down.

---

## Phase 4 — Agentic Systems & Tool Use (Weeks 14-17, ~22 hrs)

Goal: move from single LLM calls to systems that plan, use tools, and orchestrate multi-step work — the "agentic" core of this whole plan.

- **Hugging Face — "Agents Course"** (free, [huggingface.co/learn/agents-course](https://huggingface.co/learn/agents-course)) — the most complete free, structured course on agent architectures, tool use, and evaluation.
- **Model Context Protocol (MCP) docs + quickstart** (free, [modelcontextprotocol.io](https://modelcontextprotocol.io)) — increasingly the standard for tool/data access across agent frameworks; worth understanding regardless of which framework you settle on.
- **DeepLearning.AI — "MCP: Build Rich-Context AI Apps with Anthropic"** (free, ~2h) — hands-on MCP building.
- **LangGraph documentation + tutorials** (free, open-source docs at [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)) — the most widely adopted agent orchestration framework; work through the core tutorials (not the paid LangSmith platform — the framework and docs are free and open source).
- **DeepLearning.AI — "Agentic AI"** (free, Andrew Ng, ~10h) — multi-step, iterative agent workflows; good mid-to-advanced synthesis course once you've done the HF course.
- **CrewAI documentation** (free, [docs.crewai.com](https://docs.crewai.com)) — lighter-weight alternative framework for multi-agent orchestration; skim for contrast rather than going deep in both frameworks.
- **Repo:** [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) — cloned locally at `reference-repos/GenAI_Agents`. Same style/quality as the RAG_Techniques repo above, progressing from basic conversational bots to multi-agent systems — the natural next step after Phase 3's RAG notebooks.

**🎥 Watch first (all free, YouTube):**

- IBM Technology — ["What is MCP? Integrate AI Agents with Databases & APIs"](https://www.youtube.com/watch?v=eur8dUO9mvE) (~9 min) and Shaw Talebi — ["Model Context Protocol (MCP) Explained in 20 Minutes"](https://www.youtube.com/watch?v=N3vHJcHBS-w) — two short, complementary MCP explainers before the DeepLearning.AI MCP course above.
- IBM Technology — ["What is LangChain?"](https://www.youtube.com/watch?v=1bUy-1hGZpI) (~8 min) — quick framework orientation before the LangGraph docs/tutorials.
- Optional, longer: AI Engineer — ["Building Agents with Model Context Protocol - Full Workshop with Mahesh Murag of Anthropic"](https://www.youtube.com/watch?v=kQmXtrmQ5Zg) — a full hands-on workshop if you want a guided build session rather than docs.
- Andrej Karpathy — ["Software Is Changing (Again)"](https://www.youtube.com/watch?v=LCEmiRjPEtQ) (Y Combinator talk, ~40 min) — his framing of the actual paradigm shift agents represent for how software gets built. More substantive than a "what is an agent" explainer now that you've done the HF Agents Course — this is the "so what" for everything in this phase.

**Big picture:** re-read Anthropic's "Building Effective Agents" now that you have hands-on context — it'll read completely differently than it did in Phase 0.

**Hands-on project:** Extend your Phase 3 RAG assistant into an agent — give it tools (e.g., a "search my notes," "check a metrics API," "open a ticket" tool) and let it decide when to use them, rather than a fixed pipeline. A strong artifact showing real agentic behavior, not just an API call.

**🧪 Test yourself:**

- Task: give your agent one intentionally ambiguous or broken request (missing information it needs for a tool call, or a request that could use two different tools). Document exactly what it does — does it ask for clarification, guess and proceed, or fail silently? Knowing your agent's actual failure mode is more valuable than another successful run.
- Quiz, no notes: explain the ReAct pattern (reason → act → observe loop) in your own words, without reusing the paper's phrasing.

**Checkpoint:** A working agent that uses at least 2 tools, makes decisions about when to call them, and you can explain its failure modes.

---

## Phase 5 — MLOps / LLMOps & Production (Weeks 18-20, ~17 hrs)

Goal: the production concerns — evaluation, monitoring, cost, latency, guardrails — that separate a demo from something reliable.

- **LLM Zoomcamp (DataTalksClub)** — revisit the evaluation/monitoring modules you may have skipped in Phase 3.
- **DeepLearning.AI — "Safe and reliable AI via guardrails"** (free, GuardrailsAI, ~1h40m).
- **DeepLearning.AI — "Fast & Efficient LLM Inference with vLLM"** (free, ~1h40m) and **"Fast LLM Inference with Cerebras"** — cost/latency tradeoffs, useful vocabulary either way.
- **DeepLearning.AI — "Orchestrating Workflows for GenAI Applications"** (free, Astronomer, ~1h50m) — Airflow-based orchestration for GenAI pipelines.
- **Made With ML by Goku Mohandas** (free, [madewithml.com](https://madewithml.com)) — MLOps fundamentals (testing, versioning, CI/CD for ML) if you want the classical-MLOps grounding underneath LLMOps.
- **Chip Huyen's blog** (free, [huyenchip.com/blog](https://huyenchip.com/blog)) — the best free ongoing writing on production LLM systems and evaluation design.

**🎥 Watch first (free, YouTube):**

- DeepLearning.AI — ["A Chat with Andrew on MLOps: From Model-centric to Data-centric AI"](https://www.youtube.com/watch?v=06-AZXmwHjo) — Andrew Ng specifically on the production/ops mindset shift.

**[PAID, optional]** Chip Huyen's book **"AI Engineering"** (O'Reilly, ~$50-65) — if you want the book-length, structured version of the above blog content. Her earlier **"Designing Machine Learning Systems"** (~$50-65) is the classical-MLOps equivalent. Worth buying if you prefer books to scattered free content; not required.

**🧪 Test yourself:**

- Task: write 5 automated eval test cases (input → expected behavior, not exact output) against your Phase 3 or Phase 4 project and actually run them. How many pass? Fix one that fails before moving on.
- Quiz, no notes: name two things that can make an LLM app slow or expensive in production, and one concrete mitigation for each.

**Checkpoint:** You can articulate an evaluation strategy for an LLM feature (what to measure, how to catch regressions) and explain the cost/latency levers available to you.

---

## Phase 6 — Capstone & Consolidation (Weeks 21-23+, ongoing)

Goal: consolidate everything into one coherent project and a clear personal record of what you learned.

- Turn your Phase 4 agent project into a polished GitHub repo with a README that reads like a case study (problem, architecture, tradeoffs, what you'd do differently). A clear demonstration piece for yourself.
- Write 1-2 short posts or notes reflecting on what you built and what surprised you along the way — solidifies the learning and gives you something to look back on later.
- Explore one adjacent topic that interested you most along the way (fine-tuning, multimodal models, evaluation frameworks, a different agent framework) as a final self-directed mini-project.
- **Staying current (ongoing, ~30 min/week):** subscribe to Anthropic's and OpenAI's engineering blogs, Chip Huyen's newsletter, and the **DataTalksClub** community (free) for continued exposure after this plan ends — this space moves fast enough that a one-time plan isn't enough.

**🧪 Test yourself (cumulative):**

- Task: without opening any notes, explain your capstone project end-to-end out loud or in writing — the problem, the architecture, why you made the choices you did, and what would break it. This is the same test as Phase 0's "explain it to a friend," but now applied to something you built rather than a concept you watched.
- Quiz, no notes, one question per phase: what's a token vs. an embedding? What does a Pydantic schema buy you? What's the one RAG failure mode you must always test for? What's a concrete agent failure mode you personally saw? What's one lever for controlling LLM cost in production? If you can answer all five without hesitating, the plan did its job.

**Checkpoint:** A complete project you understand end-to-end and are proud of, plus a written reflection on what you learned and what you'd do differently.

---

## Summary of Paid Resources Flagged (all optional)

| Resource | Cost | Why it might be worth it | Free alternative used instead |
|---|---|---|---|
| Chip Huyen, *AI Engineering* | ~$50-65 | Structured, book-length version of production LLM practices | Her free blog (huyenchip.com/blog) |
| Chip Huyen, *Designing Machine Learning Systems* | ~$50-65 | Classical MLOps grounding | Made With ML (free) |
| DAIR.AI Academy courses (via promptingguide.ai) | Paid, varies | Structured prompting/agents courses from the same team as the free guide | The free promptingguide.ai site itself covers the core techniques |

Nothing in the core path requires a purchase — these are enrichment options if you want book-depth.
