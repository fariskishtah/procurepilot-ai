# Tools and source policy

Tavily Search uses the official HTTPS `/search` endpoint, bearer token from environment, basic depth, up to five results, and two calls per run. Missing credentials fail closed. Docs: https://docs.tavily.com/documentation/api-reference/endpoint/search.

The permitted HTML fetch requires a domain manually added after terms review. It blocks private addresses and redirects. JSON-LD Product extraction takes literal fields only. ScrapeGraphAI `SmartScraperGraph` is an optional local HTML adapter; it was not installed or executed in the verified run. Repo: https://github.com/ScrapeGraphAI/Scrapegraph-ai.

No supplier domains were approved for the included run. No source captures are redistributed.
