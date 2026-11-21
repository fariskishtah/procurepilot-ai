from crewai import Process
from procurepilot.crew import build_crew
from procurepilot.models import Request

def test_six_distinct_agents_and_sequential_context():
    crew,tasks=build_crew(Request(),[],[])
    assert crew.process==Process.sequential
    assert len(crew.agents)==len(tasks)==6
    assert len({agent.role for agent in crew.agents})==6
    assert tasks[0].context==[]
    for previous,current in zip(tasks,tasks[1:]):
        assert current.context==[previous]

def test_evidence_tool_is_registered_on_relevant_agents():
    crew,_=build_crew(Request(),[],[])
    for index in (0,1,3,4):
        assert any(tool.name=="Read validated procurement evidence" for tool in crew.agents[index].tools)
