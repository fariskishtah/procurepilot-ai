# Reproducibility

Use Python 3.12, CrewAI 1.15.44, Ollama and `qwen2.5:1.5b-instruct`. Install the project and run `pytest` as shown in the root README. Run `run_catalog()` for a fresh reviewed-page lookup; the website, offers, model wording and duration can change. The included trace `artifacts/traces/ba0e0163e5f8.json` records the observed 21 November 2026 result. Unit tests use synthetic fixtures and do not require Ollama. No raw website capture is bundled for replay. The Streamlit app stores runs in a local SQLite file excluded from Git.
