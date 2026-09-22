# AI & Agentic Development Learning Plan

A self-contained, 7-phase learning plan for going from zero to genuinely hands-on with LLM foundations, RAG, agentic systems, and MLOps/LLMOps — built almost entirely from free resources, with paid options clearly flagged where relevant. No prior AI/ML background assumed beyond general comfort writing code.

## Start here

Open **`site/index.html`** in your browser (just double-click it — no server or install needed). That's the course overview — from there, each phase is its own page (no accidentally scrolling past one phase into the next), broken into checkable lectures, with a sidebar curriculum tree and progress tracked locally in your browser.

If you'd rather read plain markdown, the same content lives in `learning-plan.md`.

## Structure

```
learning-plan.md          The source of truth — 7 phases, courses, videos, checkpoints
site/                      A generated, browsable version of the plan above (one page per phase)
  index.html               ← open this (course overview, links to every phase page)
  build.py                  Regenerates the site from learning-plan.md (run after editing it)
resources/                 Downloaded PDFs (whitepapers + foundational papers) + a README describing them
reference-repos/           4 cloned GitHub repos used for hands-on phases — see reference-repos/README.md to fetch them
starter-project/           A ready-to-run Python scaffold for the Phase 1-2 hands-on exercises
```

## If you're picking this up fresh

1. Read `learning-plan.md` (or open `site/index.html`) start to finish once, to get the shape of it.
2. `cd reference-repos && ` run the clone commands in `reference-repos/README.md`.
3. `cd starter-project`, follow its `README.md` to set up a virtualenv and API key, and run the two example scripts.
4. Work the plan phase by phase — it's sequenced deliberately; each phase assumes the last.

## Keeping the site in sync

`learning-plan.md` is canonical. If you edit it, regenerate the site:

```bash
cd site
python3 -m venv .venv && source .venv/bin/activate   # first time only
pip install -r requirements.txt                       # first time only
python build.py
```
