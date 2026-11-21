# ProcurePilot AI

Evidence-first multi-agent procurement research for Faris Mohamed Kishtah's INSTANT AI Sprint 4 Project 5. **Academic status: PARTIAL.** NileTech Operations is a fictional example buyer.

## Verified result

A live, permission-reviewed Egyptian catalog page yielded five current HC-05 module offers from five shops. In run `ba0e0163e5f8`, six sequential CrewAI tasks completed in 53.92 seconds using local Ollama. The sourcing agent invoked `catalog_source_lookup` once. The small model omitted the required extraction and assessment tool calls; guardrails invoked those deterministic functions in the orchestrator after retries, and the trace labels them separately. All five offers require supplier, configuration, quantity, warranty, shipping, and tax confirmation. **No purchase recommendation is made.** The original 10-laptop request remains unverified.

The catalog observations were 195 EGP (Makers Electronics), 195 EGP (Ampere Electronics), 205 EGP (Most Electronic), 250 EGP (3D Smart Shop), and 295 EGP (RAM Electronics), observed on 21 November 2026. See [source validation](docs/REAL_SOURCING_VALIDATION.md) and the [final run record](docs/FINAL_PROCUREMENT_RUN.md) for source links and limits.

## Architecture

`Request -> bounded source lookup -> permission-gated HTML fetch -> literal extraction -> Pydantic evidence -> deterministic eligibility and scoring -> six CrewAI tasks -> HTML report, Streamlit app, SQLite`

The six roles cover sourcing, supplier collection, technical review, procurement analysis, evidence audit, and executive reporting. CrewAI uses sequential tasks with prior-task context. The local model cannot change final product records or arithmetic. Agent calls and orchestrator recovery calls have distinct trace stages.

## Run locally

Python 3.12 and a running Ollama server are required.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[test]'
ollama pull qwen2.5:1.5b-instruct
.venv/bin/python -m pytest -q
.venv/bin/python -c 'from procurepilot.catalog_crew import run_catalog; print(run_catalog().report_path)'
.venv/bin/streamlit run app.py --server.address 127.0.0.1
```

In the app, open Request Builder and run the reviewed Egyptian catalog scenario. The general laptop request form remains available; it requires reviewed supplier URLs or a Tavily key. Set `TAVILY_API_KEY` to enable the capped Tavily adapter. No paid services or overage were used. The optional ScrapeGraphAI package was tested in an isolated environment with local HTML and Ollama; it did not produce validated records for the final run. See [integration results](docs/SCRAPEGRAPH_INTEGRATION.md).

## Decision rules

Mandatory fields and complete landed cost gate eligibility. Unknown shipping, tax, warranty, direct supplier verification, or quantity availability leaves an offer needing verification. Only eligible offers get a weighted value score and recommendation rank. Catalog observations get a clearly labeled price-only order. No silent currency conversion is performed.

## Source and security controls

Approved public HTTPS domains only; private addresses, redirects, oversized responses and long requests are blocked. This technical gate follows a manual terms and robots review. External page text is treated as data. Evidence stores source URL, retrieval time, literal excerpt and page hash. Raw third-party page captures, credentials, model weights and local database files are excluded from Git and submission packages.

## Status and limitations

Tavily live search is blocked by missing credentials. CrewAI agent-selected tool use is verified for sourcing only; extraction and scoring were completed by labeled orchestrator recovery. Direct supplier checks are incomplete. Local model summaries may be inaccurate; the HTML report is generated from validated Python records. Free cloud hosting is not verified. The project is MIT licensed; dependencies retain their own licenses.
