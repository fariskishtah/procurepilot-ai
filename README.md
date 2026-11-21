# ProcurePilot AI

Multi-Agent Procurement Intelligence & Strategic Sourcing Platform. Built for Faris Mohamed Kishtah's INSTANT AI Sprint 4 Project 5 assignment.

## Current status

**Partial.** A genuine six-agent CrewAI sequential run completed locally on Ollama, but no Tavily key was present and no permitted supplier listings were collected. The model made zero calls to its offered CrewAI evidence tool. The included HTML report therefore makes **no purchase recommendation**. See `PROJECT_STATUS.md` and the real trace in the submission package. NileTech Operations is a fictional example company, not a real buyer.

## Architecture

`Request -> Tavily search or reviewed seed URLs -> permission-gated HTML fetch -> literal JSON-LD extraction -> Pydantic evidence -> deterministic eligibility and scoring -> six CrewAI tasks -> offline HTML report -> Streamlit dashboard -> SQLite`

Agents: product sourcing, supplier data collection, technical normalization, procurement analysis, evidence audit, executive reporting. CrewAI `Process.sequential` and `Task.context` link tasks. The LLM comments on validated inputs; it cannot change numeric assessments or insert data into the final report.

## Install and run

Python 3.12 and Ollama are required. This project was tested with `qwen2.5:1.5b-instruct`.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[test]'
ollama pull qwen2.5:1.5b-instruct
.venv/bin/python -m pytest -q
.venv/bin/streamlit run app.py --server.address 127.0.0.1
```

For a CLI run: `.venv/bin/python scripts_run.py`. Set `TAVILY_API_KEY` in your shell to enable Tavily within a two-call budget. The application never subscribes or enables paid overage. To try reviewed pages, pass `--url https://... --approve-domain example.com`; review site terms, automated access guidance and robots instructions first. Only public HTTPS, allowlisted domains, no redirects, and small HTML responses are accepted. Search leads are never treated as verified products.

To opt into ScrapeGraphAI, install `.[scrapegraph]`. The adapter accepts local HTML and filters model claims against visible text. This optional dependency was not run in the verified local execution.

## Requirements, price, and ranking

The request covers company, category, delivery country, quantity, currency, budget, RAM, storage, warranty, required terms, excluded brands, and five weights totaling 100. Unverified mandatory fields mark an offer `needs_verification`; failed fields mark it `rejected`. Only fully eligible offers receive a score. Known cost is unit price times quantity, plus known shipping and tax when not already included. An unknown cost component prevents eligibility. Prices in other currencies are never converted silently. Numeric ranking is deterministic and does not use LLM arithmetic.

The Streamlit app includes a request builder, overview, execution timeline, product and supplier table, weight sensitivity controls, cost chart, evidence inspector, and HTML report preview/download. SQLite stores separate runs.

## Security and provenance

No API keys are embedded or logged. Remote URLs require public HTTPS and public DNS resolution. Fetches require an explicit approved domain, reject redirects, cap responses at 2 MB, and use a 15-second timeout. This does not substitute for a terms review. External content is untrusted. Source excerpts and hashes are stored in product evidence; missing claims remain missing. No source data or supplier prices are bundled.

## Limitations

Tavily live call, permitted supplier extraction, ScrapeGraphAI execution, live product ranking, and a source-backed recommendation have not been verified. The current report represents a completed agent workflow on empty source evidence, not a successful sourcing outcome. Local Ollama output quality is limited by the small model. Free cloud hosting is not deployed because a local Ollama server cannot be exposed safely or assumed available on a free host.

## Licensing

Project source is MIT licensed. CrewAI and ScrapeGraphAI license details should be checked against exact dependency versions before redistribution. No third-party product page captures are redistributed.
