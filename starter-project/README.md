# Starter Project

Scaffold for the hands-on steps in `../learning-plan.md`. Start here for Phase 1 and Phase 2; this is also the base you'll extend into the RAG project (Phase 3) and the agent project (Phase 4).

## Setup

```bash
cd starter-project
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Then get an API key and put it in `.env`:
- Anthropic: https://console.anthropic.com/ (has free trial credit)
- OpenAI: https://platform.openai.com/ (has free trial credit)

## Scripts

- **`01_raw_api_call.py`** (Phase 1) — a single raw API call, no framework, plus a temperature=0 vs. temperature=1 comparison on the same prompt. Confirms your setup works, shows you exactly what a request/response looks like, and makes "sampling" concrete instead of a parameter you just set and forget.
- **`02_structured_output.py`** (Phase 2) — the schema-in, validated-data-out pattern using Pydantic. This is the pattern you'll reuse for the classification/summarization project described in Phase 2 of the plan — swap `TICKET_TEXT` for your own real data.

## Where this goes next

- Phase 3: add a `rag/` folder here — ingest a real corpus (notes, articles, docs), chunk it, embed it, and retrieve against it before generating.
- Phase 4: add tools to the RAG assistant and let the model decide when to call them — that's the agent project.

Keep this as one evolving repo rather than starting fresh each phase — by Phase 6 it should be the project that ties everything together.
