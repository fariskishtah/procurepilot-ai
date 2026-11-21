"""Generate the source-backed, bounded Sprint 4 research report."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

OUT=Path('ProcurePilot_AI_Research_Report.pdf')
c=canvas.Canvas(str(OUT),pagesize=(595,842))
NAVY=HexColor('#111d35'); GOLD=HexColor('#b89447'); INK=HexColor('#28354c'); MUTED=HexColor('#607086')
page=0

def header(title, subtitle):
    global page
    page+=1
    c.setFillColor(NAVY); c.rect(0,765,595,77,fill=1,stroke=0)
    c.setFont('Helvetica-Bold',17); c.setFillColor(HexColor('#ffffff')); c.drawString(44,803,title)
    c.setFont('Helvetica',9); c.setFillColor(HexColor('#d5dfec')); c.drawString(44,785,subtitle)
    c.setStrokeColor(GOLD); c.setLineWidth(2); c.line(44,752,551,752)
    c.setFont('Helvetica',8); c.setFillColor(MUTED); c.drawString(44,28,'ProcurePilot AI | Faris Mohamed Kishtah | 21 November 2026')
    c.drawRightString(551,28,str(page))

def block(y,title,body):
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold',12); c.drawString(44,y,title); y-=18
    c.setFillColor(INK); c.setFont('Helvetica',9.5)
    for line in simpleSplit(body,'Helvetica',9.5,507):
        c.drawString(44,y,line); y-=14
    return y-18

header('PROCUREPILOT AI','Technical research report | Sprint 4 - Project 5 | Evidence-first procurement')
y=718
y=block(y,'Executive summary','A real six-task CrewAI run completed locally on Ollama. A reviewed Egyptian catalog product page supplied five current HC-05 module offers. One agent-selected source lookup executed. The model skipped extraction and assessment tools, so guardrails ran those deterministic functions and labeled them as orchestrator calls. All five offers require verification. No purchase recommendation is supported. Academic status: PARTIAL.')
y=block(y,'Two procurement scenarios','The original NileTech Operations request is 10 business laptops within 300,000 EGP, with RAM, storage, warranty and SSD requirements. It remains unverified. A separate fictional NileTech R&D scenario requests 10 HC-05 wireless serial modules within 3,000 EGP and is used for real catalog sourcing. Neither scenario represents a real buyer.')
y=block(y,'Architecture and trust boundary','Request validation -> reviewed public HTTPS source -> literal current-offer extraction -> Pydantic evidence -> deterministic cost and eligibility -> sequential CrewAI analysis -> HTML report, Streamlit app and SQLite. External page text is data, not instructions. Tool bodies record actual invocation events; the language model cannot alter accepted product records or numeric calculations.')
y=block(y,'Six-agent workflow','Sourcing, supplier collection, technical review, procurement analysis, evidence audit and executive reporting each have a distinct CrewAI Agent and Task. Each task receives the previous task as context. Source lookup is agent-selected; extraction and assessment fell back to explicit guardrail execution after retries.')
c.showPage()
header('LIVE SOURCE AND RESULTS','Observed catalog offers and deterministic assessment')
y=718
y=block(y,'Reviewed source','The source is Makhzan: makhzan.merope.dev/products/b8c70b58-ff9c-406e-8d22-e256089ce7ca-hc-05-bluetooth-module-serial-ttl. Its terms permit work-related comparison within robots guidance, and the reviewed product path is allowed. The current offer list was parsed; the stale-offer disclosure was excluded. No raw page capture is bundled.')
y=block(y,'Catalog observations','Makers Electronics: 195 EGP; Ampere Electronics: 195 EGP; Most Electronic: 205 EGP; 3D Smart Shop: 250 EGP; RAM Electronics: 295 EGP. For 10 units, known merchandise subtotals are 1,950; 1,950; 2,050; 2,500; and 2,950 EGP. They exclude unknown shipping and tax. These prices were observed on 21 November 2026 and can change.')
y=block(y,'Run trace','Run ba0e0163e5f8: six of six CrewAI task outputs, 53.92 seconds, local qwen2.5:1.5b-instruct. Actual agent tool calls: one catalog_source_lookup. Orchestrator recovery calls: catalog_evidence_retrieval and deterministic_procurement_assessment. Five products and five needs_verification assessments. No eligible rank or recommendation. See the bundled JSON trace and HTML report.')
y=block(y,'Uncertainty','Makhzan is an aggregator and flags AI-based offer matching. One Makers supplier page was manually checked and showed 195 EGP in stock, but direct confirmation for the other shops, 10-unit stock, exact configuration, warranty, shipping and tax is missing. Price-only ordering is a comparison aid, not a purchasing decision.')
c.showPage()
header('EVALUATION AND REPRODUCTION','Limits, testing and release evidence')
y=718
y=block(y,'Automated and real-model tests','The automated suite passed 22/22 tests with no failures or skips. It covers extraction boundaries, safety, cost and eligibility, stable ranking, weight sensitivity, report consistency, crew structure and recovery labeling. The real six-agent run is separate from those fixture tests. A tiny tool-call probe established that CrewAI Task.used_tools may remain zero after a tool body executes; direct tool-body instrumentation is used instead.')
y=block(y,'ScrapeGraphAI and Tavily','ScrapeGraphAI 2.3.1 ran locally on reviewed HTML with Ollama and telemetry disabled. Its first output included stale rows and truncated titles; a second constrained run produced no accepted tuples. It was not used for final evidence. Tavily was not called because TAVILY_API_KEY was absent. No paid service was used.')
y=block(y,'Reproduction','Install Python 3.12 dependencies from pyproject.toml, start Ollama, pull qwen2.5:1.5b-instruct, run pytest, then run procurepilot.catalog_crew.run_catalog(). A fresh live page may differ. The bundled trace documents the observed result. Start Streamlit with streamlit run app.py. The old laptop workflow remains available with reviewed URLs or Tavily credentials.')
y=block(y,'References and release','Makhzan product, terms and robots pages are linked in docs/REAL_SOURCING_VALIDATION.md. CrewAI: docs.crewai.com; Tavily: docs.tavily.com; ScrapeGraphAI: github.com/ScrapeGraphAI/Scrapegraph-ai. Public source: github.com/fariskishtah/procurepilot-ai. No free cloud hosting is verified. No credentials, model weights or third-party raw page captures are distributed.')
y=block(y,'Conclusion','This release demonstrates a genuine six-agent workflow and an evidence-backed five-offer catalog comparison. Full agent tool selection, direct supplier validation, complete landed costs and the original laptop scenario remain open. The correct procurement outcome is insufficient evidence for a purchase recommendation.')
c.save()
print(OUT.resolve())
