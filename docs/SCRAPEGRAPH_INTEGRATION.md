# ScrapeGraphAI integration result

Open-source ScrapeGraphAI 2.3.1 was installed in a separate `.venv-scrapegraph` environment. `SmartScraperGraph` ran on local HTML captured from the reviewed Makhzan product page, with local Ollama `qwen2.5:1.5b-instruct` and telemetry disabled. No managed API or paid service was used; ScrapeGraphAI did not fetch the live page.

The first 23.19-second run returned seven rows despite a prompt for the first two current offers. Two rows came from a stale-offer disclosure, and two current titles were truncated. Literal comparison with the five current DOM rows would accept only three exact tuples. A second run on just the current-offer section returned no accepted tuples. These results show package/model compatibility, not reliable extraction accuracy. The production catalog path uses deterministic HTML parsing and requires exact current-row evidence. `ScrapeGraphExtractor` rejects model tuples that do not match literal current rows. See `procurepilot/sources.py`.

The raw page HTML and model result are not redistributed. Source: https://github.com/ScrapeGraphAI/Scrapegraph-ai.
