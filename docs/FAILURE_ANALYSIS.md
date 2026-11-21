# Failure analysis

- Original laptop request: still blocked by missing complete permitted supplier evidence. The final demonstration uses a distinct HC-05 R&D request with a 3,000 EGP budget.
- Tavily: no key, no live call. The three product URLs were reviewed directly.
- Old `Task.used_tools` counter: a real probe executed a tool while the counter stayed zero. Direct tool-body instrumentation is now used.
- Small local model: selected sourcing and extraction tools in the final multi-source run, but omitted deterministic assessment. The guardrail executed that calculation and labeled it as orchestrator action.
- Ampere price formatting: visible `195,00 EGP` did not initially pass a dot-decimal substring check. The parser and evidence check now normalize the specific comma-decimal format after literal page validation; a regression test confirms the 1,950 EGP subtotal.
- ScrapeGraphAI: output shape and title copying vary between local model runs. Strict validation rejects incomplete or unsupported fields; deterministic parsing supplies the final evidence.
- Stock, shipping, tax and warranty: page stock labels do not prove ten-unit order acceptance; landed cost remains incomplete. All three offers need verification, so no purchase recommendation is made.
- Browser warnings: the prior nine warnings came from Streamlit's feature policy and iframe sandbox. Connection-refused errors in the old log coincided with a deliberate server restart. A fresh stable browser session is checked separately.
