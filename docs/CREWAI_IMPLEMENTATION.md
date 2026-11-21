# CrewAI implementation

`procurepilot/crew.py` creates six distinct `Agent` objects, six `Task` objects, and one `Crew(process=Process.sequential)`. Each task after the first has `context=[previous_task]`. Agents have bounded iterations and execution time. The verified 1.5B model run trace records six completed outputs in 8.14 seconds. Four agents are offered a read-only evidence tool, but the small local model made **zero tool calls** despite task instructions. This is a known limitation. Sourcing was blocked before Crew kickoff; completion establishes orchestration, not product discovery.

Docs checked: https://docs.crewai.com/en/concepts/crews, https://docs.crewai.com/en/concepts/tasks, https://docs.crewai.com/en/learn/llm-connections.
