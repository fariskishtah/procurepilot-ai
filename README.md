# ProcurePilot AI

Evidence-first multi-agent procurement research for Faris Mohamed Kishtah's INSTANT AI Sprint 4 Project 5. **Academic status: PARTIAL.** NileTech Operations is a fictional example buyer.

## Current verified demonstration

The final demonstration is a coherent NileTech R&D request for ten HC-05 wireless serial modules within **3,000 EGP**. Three independent Egyptian supplier product pages were fetched directly: [Makers Electronics](https://makerselectronics.com/product/hc-05-bluetooth-module-3-3v/) at 195 EGP, [Ampere Electronics](https://ampere-electronics.com/product/hc-05-bluetooth-module-serial-ttl/) at 195 EGP, and [RAM Electronics](https://www.ram-e-shop.com/shop/kit-bluetooth-hc05-original-hc-05-original-chip-bluetooth-module-industrial-grade-module-8577) at 295 EGP. These are observed unit prices, not binding quotes. Exact product titles and configurations differ. Shipping, tax, warranty and confirmed ten-unit stock remain incomplete, so **no purchase recommendation is made**. The original 10-laptop scenario remains unverified.

Run `49bba9141fdb` completed six sequential CrewAI tasks in `43.51` seconds with local Ollama. The sourcing and data collection agents each invoked a real registered tool. The assessment tool was omitted by the model and executed by a labeled orchestrator guardrail. See [final run evidence](docs/ACADEMIC_COMPLETION_RUN.md), [trace](examples/verified_multisource_trace.json) and [HTML report](examples/ProcurePilot_Multisource_Report.html).

## Architecture

`Request -> three reviewed supplier URLs -> permission-gated HTTPS fetch -> literal visible HTML and JSON-LD cross-check -> Pydantic evidence -> deterministic eligibility and scoring -> six CrewAI tasks -> HTML report, Streamlit app and SQLite`

The six agents cover sourcing, data collection, specification review, procurement analysis, evidence verification and reporting. Tasks run sequentially with prior-task context. Numeric assessments and the final HTML come from validated Python records. Trace stages distinguish agent-selected tool calls, individual source fetches and orchestrator recovery.

## Run locally

Python 3.12 and a running Ollama server are required.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[test]'
ollama pull qwen2.5:1.5b-instruct
.venv/bin/python -m pytest -q
.venv/bin/python -c 'from procurepilot.multisource_crew import run_multisource; print(run_multisource().report_path)'
.venv/bin/streamlit run app.py --server.address 127.0.0.1
```

In Request Builder, select **Run three independent supplier pages**. The prior Makhzan catalog demonstration remains available separately. A fresh run can differ as supplier pages and local model output change. The general laptop request form requires reviewed URLs or a Tavily key. No Tavily live call or paid service was used.

## Decision rules and controls

Mandatory requirements and complete landed cost gate eligibility. Unknown shipping, tax, warranty or ten-unit availability prevents a confident purchase decision. Only eligible offers receive a weighted value score and recommendation rank; the current three-offer run has a price-only order. Currency is never converted silently.

Source URLs are exact, reviewed public HTTPS pages. Private addresses, redirects, oversized responses and long requests are blocked. Supplier page text is untrusted data. Evidence records source URL, retrieval time, short literal excerpt and page hash. No raw third-party page capture, credentials, local database or model weights are distributed. Makers' terms restrict republication, so only short factual observations and links are included.

ScrapeGraphAI 2.3.1 was tested on local HTML fragments with Ollama. Results varied between correct-looking fields, truncated titles and no answer; strict validation rejected unproven fields, and the final procurement path uses deterministic extraction. See [ScrapeGraphAI evaluation](docs/SCRAPEGRAPH_INTEGRATION.md). Free cloud hosting is not verified. Original project source is MIT licensed; dependencies retain their own licenses.
