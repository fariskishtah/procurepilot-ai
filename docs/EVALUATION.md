# Evaluation

The final 21 November 2026 live run `ba0e0163e5f8` produced five current catalog offers, five `needs_verification` assessments, zero eligible offers, six completed CrewAI tasks, one actual agent-selected source tool call and two labeled orchestrator recovery calls. Crew duration was 53.92 seconds. The source provides price observations, not complete direct supplier quotations. A deterministic price-only order is shown; there is no weighted eligible ranking or purchase recommendation.

The automated suite passed 22/22 tests with no failures or skips. It checks source-row exclusion, evidence, cost/eligibility, stable ranking, scoring weight sensitivity, safety checks, crew structure, fallback labels, report generation and storage. It does not prove model extraction accuracy. ScrapeGraphAI's real local output failed literal validation; see `SCRAPEGRAPH_INTEGRATION.md`. No multi-agent superiority claim is made.

Browser verification on the refreshed Streamlit process covered overview, products, scoring, report preview/download and a 390-pixel mobile viewport. The checked session showed zero browser console errors and nine warnings. Five final-run screenshots are included under `artifacts/screenshots/final/`.
