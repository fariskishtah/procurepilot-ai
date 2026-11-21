# CrewAI implementation

`procurepilot/multisource_crew.py` builds six distinct `Agent` objects and six `Task` objects with `Process.sequential`; each later task receives the previous task as context. The final run `49bba9141fdb` completed all six outputs in `43.51` seconds on local Ollama `qwen2.5:1.5b-instruct`.

The sourcing agent invoked `reviewed_supplier_lookup` and fetched three exact, reviewed public product URLs. The data collection agent invoked `literal_supplier_extraction`; the parser cross-checked two JSON-LD offers against visible prices and parsed the third visible product detail price. The specification agent received the resulting source-backed records. The procurement analyst did not invoke its offered tool; its guardrail called deterministic Python assessment after retries and labeled the call `orchestrator_tool`. The verification and reporting agents produced outputs, but the final HTML uses validated Python records, not their prose. Thus six task outputs do not imply six autonomous tool decisions.

Instrumentation is inside each tool body. Individual page fetch events, agent-selected invocation events and orchestrator recovery events have separate trace stages. This avoids the prior misleading `Task.used_tools` counter; see `TOOL_CALLING_ROOT_CAUSE.md`.

Documentation: https://docs.crewai.com/en/concepts/crews and https://docs.crewai.com/en/concepts/tasks.
