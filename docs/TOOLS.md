# Tools and source policy

The reviewed Makhzan `/products/` page is fetched with an exact public HTTPS allowlist, redirect rejection, timeout and size cap. Its terms allow work-related search/comparison within robots guidance. Its `/search` and `/api` paths are not fetched. The current-offer DOM list is parsed literally, with stale offers excluded. Source: https://makhzan.merope.dev/terms and https://makhzan.merope.dev/robots.txt.

Tavily uses the official HTTPS `/search` endpoint, bearer token from environment, basic depth and a two-call budget. Missing credentials fail closed. No Tavily live call occurred. Docs: https://docs.tavily.com/documentation/api-reference/endpoint/search.

ScrapeGraphAI `SmartScraperGraph` was run locally on reviewed HTML with Ollama. Its unverified rows were not accepted as procurement evidence. No third-party page captures or secrets are redistributed.
