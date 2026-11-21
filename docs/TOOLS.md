# Tools and source policy

Three exact HC-05 product pages are reviewed and allowlisted in `procurepilot/direct_sources.py`. The project fetches each once per run, directly from its supplier, over public HTTPS with redirect rejection, size limit and timeout. It does not crawl search, cart, checkout, API or other pages. The review used each site's robots.txt and terms: Makers permits AI assistant product crawling but restricts republication; Ampere allows search/reference use and restricts training bots; RAM product paths are not disallowed, and RAM terms warn that prices, tax and stock can change. Short factual observations, source links, retrieval times and hashes are retained; raw page HTML is not distributed.

The parser requires an exact approved URL, a visible HC-05 title with expected configuration, a scoped visible EGP price, and a matching JSON-LD Product offer for Makers and Ampere. Ampere's comma decimal separator is normalized only after its literal value is validated. RAM has no Product JSON-LD, so its product detail price is used. Stock is accepted only from a visible product stock element. No warranty, shipping or tax is inferred.

Tavily uses the official HTTPS `/search` endpoint, bearer token from environment, basic depth and a two-call budget. Missing credentials fail closed. No Tavily live call occurred. Docs: https://docs.tavily.com/documentation/api-reference/endpoint/search.

ScrapeGraphAI ran on local snippets with Ollama, but its outputs were inconsistent. Strict literal validation remains in `procurepilot/sources.py`; production supplier extraction is deterministic. See `SCRAPEGRAPH_INTEGRATION.md`.
