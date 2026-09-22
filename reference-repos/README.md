# Reference Repos

Not tracked in this repo (see `../.gitignore`) — they're other people's projects, large (500MB+ combined), and each has its own git history that doesn't make sense to vendor into this one. Clone them yourself:

```bash
cd reference-repos
git clone --depth 1 https://github.com/anthropics/anthropic-cookbook.git
git clone --depth 1 https://github.com/NirDiamant/RAG_Techniques.git
git clone --depth 1 https://github.com/NirDiamant/GenAI_Agents.git
git clone --depth 1 https://github.com/rasbt/LLMs-from-scratch.git
```

`--depth 1` keeps it to a shallow clone (history isn't needed here). See `../learning-plan.md` for how each one maps to a phase.
