from pathlib import Path
import json, glob
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

trace=json.load(open('artifacts/traces/58e761a6d8a7.json'))
duration=next((x.get('duration_seconds') for x in trace['task_trace'] if x.get('stage')=='crewai' and x.get('duration_seconds') is not None), 'unknown')
out=Path('ProcurePilot_AI_Research_Report.pdf')
c=canvas.Canvas(str(out),pagesize=(595,842))
NAVY=HexColor('#111d35'); GOLD=HexColor('#b89447'); INK=HexColor('#28354c'); MUTED=HexColor('#607086')
page=0
def header(title, subtitle):
 global page
 page+=1
 c.setFillColor(NAVY);c.rect(0,765,595,77,fill=1,stroke=0)
 c.setFont('Helvetica-Bold',17);c.setFillColor(HexColor('#ffffff'));c.drawString(44,803,title)
 c.setFont('Helvetica',9);c.setFillColor(HexColor('#d5dfec'));c.drawString(44,785,subtitle)
 c.setStrokeColor(GOLD);c.setLineWidth(2);c.line(44,752,551,752)
 c.setFont('Helvetica',8);c.setFillColor(MUTED);c.drawString(44,28,'ProcurePilot AI | Faris Mohamed Kishtah | 21 November 2026')
 c.drawRightString(551,28,f'{page}')
def block(y,title,body):
 c.setFillColor(NAVY);c.setFont('Helvetica-Bold',12);c.drawString(44,y,title);y-=18
 c.setFillColor(INK);c.setFont('Helvetica',9.5)
 for line in simpleSplit(body,'Helvetica',9.5,507):
  c.drawString(44,y,line);y-=14
 return y-18
header('PROCUREPILOT AI','Technical research report | Sprint 4 - Project 5 | Evidence-first multi-agent procurement')
y=718
y=block(y,'Executive summary','A genuine CrewAI 1.15.44 sequential crew with six specialist agents completed on a local Ollama qwen2.5:1.5b-instruct model. The run found no permitted supplier evidence because Tavily credentials were absent and no approved product source URLs were provided. The report therefore contains no purchase recommendation. Academic assignment status: PARTIAL.')
y=block(y,'Procurement problem and company context','NileTech Operations is a fictional mid-sized technology and operations company in Egypt. The demonstration request is 10 business laptops, a 300,000 EGP ceiling, at least 16 GB RAM, 512 GB storage, 12-month warranty, and SSD evidence. These are configurable requirements, not real market facts.')
y=block(y,'Architecture','Request validation -> bounded source discovery -> permission-gated HTML extraction -> field evidence -> deterministic eligibility, known cost and weighted scoring -> CrewAI sequential analysis -> HTML report, Streamlit studio and SQLite run storage.')
y=block(y,'Agent workflow','1. Sourcing identifies candidate URLs. 2. Collection checks source evidence. 3. Technical review identifies missing or contradictory specifications. 4. Procurement analysis explains deterministic assessments. 5. Evidence audit checks unsupported claims and risks. 6. Reporting provides an executive summary. Each task receives the prior task as CrewAI context.')
y=block(y,'Trust boundary','Supplier pages are untrusted. Source claims must be literal page evidence with URL, timestamp and hash. The LLM cannot change product records, arithmetic, eligibility, scores or the generated HTML. Public HTTPS and a reviewed-domain allowlist gate remote requests.')
c.showPage()
header('METHODS AND RESULTS','Actual local execution and evidence availability')
y=718
y=block(y,'Tools','Tavily Search adapter: implemented with basic search depth and a two-call budget; live call blocked by missing TAVILY_API_KEY. ScrapeGraphAI SmartScraperGraph adapter: implemented for local HTML, but optional dependency and live extraction were not executed. JSON-LD extractor and permission-gated public HTML fetch are implemented.')
y=block(y,'Run outcome',f"Run ID: {trace['run_id']}. Six of six CrewAI tasks produced outputs; crew completion flag: {trace['crew_completed']}. Crew duration: {next((x.get('duration_seconds') for x in trace['task_trace'] if x.get('stage')=='crewai' and x.get('duration_seconds') is not None),'unknown')} seconds. Products collected: {len(trace['products'])}. Eligible offers: {sum(x['status']=='eligible' for x in trace['assessments'])}. Recommendation: none. The agent output establishes orchestration only; no actual supplier discovery was verified.")
y=block(y,'Scoring and cost','Mandatory requirements gate eligibility. Unknown mandatory fields, tax, shipping or availability require verification. A failed criterion rejects an offer. Only eligible offers are scored by configurable weights: price 35%, specifications 35%, warranty 15%, availability 10%, evidence 5%. Known cost equals unit price times quantity plus documented shipping and applicable tax. No cross-currency conversion is assumed.')
y=block(y,'Evaluation',f'Automated suite: 15 passed, 0 failed, 0 skipped. It covers request weights, eligibility, budget, missing evidence, cost uncertainty, stable ranking, private URL blocking, JSON-LD extraction, a mocked ScrapeGraph adapter, storage and honest report generation. No live extraction accuracy is reported because no real labeled supplier pages were captured. The {duration}-second crew run is not a procurement benchmark. CrewAI tool-call count was zero in this run; agent tool use remains unverified.')
y=block(y,'Limitations and next verification','A Tavily key or separately permitted seed sources are required for a complete sourcing demonstration. The exact ScrapeGraphAI dependency needs an isolated live compatibility check. A real multi-supplier evaluation and current-price validation remain open. Local Ollama output quality is limited by the small model. No free cloud deployment is verified.')
c.showPage()
header('REPRODUCIBILITY AND REFERENCES','Source documents and release notes')
y=718
y=block(y,'Reproduce locally','Install Python 3.12 dependencies from pyproject.toml, start Ollama and pull qwen2.5:1.5b-instruct. Run .venv/bin/python scripts_run.py and .venv/bin/python -m pytest -q. Start .venv/bin/streamlit run app.py. No key is needed to reproduce the empty-evidence agent workflow. The model wording and runtime may vary.')
y=block(y,'Source references','CrewAI: https://docs.crewai.com/en/concepts/crews and /tasks. Tavily API: https://docs.tavily.com/documentation/api-reference/endpoint/search. ScrapeGraphAI open source: https://github.com/ScrapeGraphAI/Scrapegraph-ai. The included run trace and source code are the primary evidence for this implementation.')
y=block(y,'Release status','The source repository is public at https://github.com/fariskishtah/procurepilot-ai. Free hosting is not verified. No supplier data, private credentials, model weights or third-party captures are included. Original project source is MIT licensed; dependency and model licenses remain separate.')
y=block(y,'Conclusion','ProcurePilot AI demonstrates an actual six-agent sequential CrewAI workflow and evidence-first decision logic. It does not yet meet the assignment requirement for source-backed multi-supplier comparison. Its honest no-recommendation output is the correct result for the verified run.')
c.save()
print(out.resolve())
