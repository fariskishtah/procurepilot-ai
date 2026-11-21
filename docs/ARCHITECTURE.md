# Architecture

The request is a Pydantic model. Sourcing uses Tavily with a strict call budget, or explicitly reviewed seed URLs. Extraction uses literal JSON-LD fields from a permission-gated HTML fetch. ScrapeGraphAI is optional for local HTML and its claims are filtered against visible text. Each claim retains a source URL, capture time, excerpt, extraction method, and content hash. The engine gates mandatory requirements, then scores only eligible products. Six CrewAI agents execute sequentially with prior task context. The final HTML is generated from validated Pydantic data, not from free-form model text. SQLite persists runs and Streamlit reads them.

Key trust boundary: website content is untrusted data. The LLM cannot mutate the deterministic Product, Assessment, or RunResult models used by reporting. No arbitrary shell or browser execution tool is available to agents.
