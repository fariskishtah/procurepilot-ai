# Reproducibility

Use Python 3.12, CrewAI 1.15.44 and Ollama `qwen2.5:1.5b-instruct`. Run `scripts_run.py` with no Tavily key to reproduce an honest empty-evidence workflow. The exact LLM wording and duration can vary. Unit tests do not require Ollama. The included trace is a genuine run, not a deterministic mock. Replays require a permitted capture manifest; none is shipped. The app stores independent runs in SQLite, excluded from Git.
