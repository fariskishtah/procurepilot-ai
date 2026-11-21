# Tool-calling root cause analysis

The previous trace read `Task.used_tools` and reported zero calls. A controlled real CrewAI 1.15.44 + Ollama qwen2.5:1.5b-instruct probe registered a `@tool` function, had an agent call it, and recorded the function's side effect. **The function ran once while `Task.used_tools` still read zero.** The old trace therefore undercounted and cannot prove the prior agents made zero actual calls. It also cannot prove they made any, because the old tool function lacked its own instrumentation.

The original workflow preloaded request and product data before `Crew.kickoff`, gave source data directly in the first task prompt, and allowed agents to complete summaries without calling tools. That design made tool selection optional. The source search also stopped before kickoff when Tavily credentials were missing. Product discovery was not accomplished by CrewAI agents.

The recovery workflow uses simple snake-case CrewAI tool names, explicit task instructions, source and evidence tools attached to the relevant agents, and event recording **inside each tool function**. The sourcing tool fetches a reviewed public product page. The extraction tool parses its current offer list. The assessment tool runs deterministic Python. Events distinguish `agent_selected` calls from any orchestrator action. The Crew remains `Process.sequential` with each task linked to the previous task.

A local model's prose can still be wrong or omit a tool call. The final report is generated from validated state, and missing calls result in missing evidence rather than fabricated output. Inspect `docs/FINAL_PROCUREMENT_RUN.md` and its JSON trace for the actual recovery-run counts.
