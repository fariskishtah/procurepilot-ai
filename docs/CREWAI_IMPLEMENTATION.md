# CrewAI implementation

`procurepilot/catalog_crew.py` builds six distinct agents and six sequential tasks. Each task after the first receives the previous task as context. The live run `ba0e0163e5f8` completed all six tasks in 53.92 seconds on local Ollama. The sourcing agent invoked its registered tool once. The collection and procurement agents omitted their tools, so guardrails retried and then invoked deterministic recovery. The trace marks one `agent_tool` and two `orchestrator_tool` events. Those are not interchangeable.

A separate minimal CrewAI tool probe showed that `Task.used_tools` can remain zero even when the tool body executes, so instrumentation now lives inside each tool function. The general workflow in `procurepilot/crew.py` has the same direct-call logging. See `TOOL_CALLING_ROOT_CAUSE.md` and `FINAL_PROCUREMENT_RUN.md`.

Documentation: https://docs.crewai.com/en/concepts/crews and https://docs.crewai.com/en/concepts/tasks.
