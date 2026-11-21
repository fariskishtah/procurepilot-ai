"""Generate the source-backed Sprint 4 academic completion research report."""
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
    c.setFillColor(NAVY);c.rect(0,765,595,77,fill=1,stroke=0)
    c.setFont('Helvetica-Bold',17);c.setFillColor(HexColor('#ffffff'));c.drawString(44,803,title)
    c.setFont('Helvetica',9);c.setFillColor(HexColor('#d5dfec'));c.drawString(44,785,subtitle)
    c.setStrokeColor(GOLD);c.setLineWidth(2);c.line(44,752,551,752)
    c.setFont('Helvetica',8);c.setFillColor(MUTED);c.drawString(44,28,'ProcurePilot AI | Faris Mohamed Kishtah | 21 November 2026')
    c.drawRightString(551,28,str(page))

def block(y,title,body):
    c.setFillColor(NAVY);c.setFont('Helvetica-Bold',12);c.drawString(44,y,title);y-=18
    c.setFillColor(INK);c.setFont('Helvetica',9.5)
    for line in simpleSplit(body,'Helvetica',9.5,507):
        c.drawString(44,y,line);y-=14
    return y-18

header('PROCUREPILOT AI','Technical research report | Sprint 4 - Project 5 | Academic completion sprint')
y=718
y=block(y,'Executive summary','Three independent Egyptian supplier product pages were fetched directly for a coherent fictional NileTech R&D request: ten HC-05 wireless serial modules within 3,000 EGP. A real six-agent CrewAI run completed. The sourcing and data collection agents each selected a tool; deterministic assessment was run by a labeled orchestrator guardrail. Shipping, tax, warranty and confirmed ten-unit stock remain incomplete. No purchase recommendation is supported. Academic status: PARTIAL.')
y=block(y,'Scenario and requirements','The final demonstration uses HC-05 modules, not business laptops. Exact model HC-05, quantity ten, delivery in Egypt, EGP currency and a 3,000 EGP ceiling are the stated requirements. The original ten-laptop, 300,000 EGP request remains unverified and is not evaluated using module offers. NileTech Operations is fictional.')
y=block(y,'Architecture','Request -> three permission-reviewed direct supplier URLs -> public HTTPS fetch -> visible HTML and JSON-LD cross-check -> Pydantic evidence -> deterministic eligibility and price comparison -> sequential CrewAI tasks -> HTML report, Streamlit app and SQLite. The LLM cannot change accepted product records or final arithmetic.')
y=block(y,'Trust and access','The project fetches exact reviewed product URLs only, with public-host checks, redirect rejection, timeout and size limits. Makers, Ampere and RAM robots/terms were reviewed. No raw third-party page capture is redistributed. Source URLs, retrieval timestamps, short factual excerpts and page hashes are recorded in the JSON trace.')
c.showPage()
header('DIRECT SUPPLIER RESULTS','Three independent sites, different HC-05 configurations')
y=718
y=block(y,'Observed offers','Makers Electronics: HC-05 Bluetooth Module 3.3V, 195 EGP, listed in stock. Ampere Electronics: HC-05 Bluetooth Module, Serial TTL, 195 EGP, page showed 141 in stock. RAM Electronics: HC-05 Original Chip Bluetooth Module - Industrial Grade Module, 295 EGP, stock not evidenced on its product page. These are observations on 21 November 2026, not binding quotes or like-for-like configurations.')
y=block(y,'Source pages','Makers: makerselectronics.com/product/hc-05-bluetooth-module-3-3v/. Ampere: ampere-electronics.com/product/hc-05-bluetooth-module-serial-ttl/. RAM: ram-e-shop.com/shop/kit-bluetooth-hc05-original-hc-05-original-chip-bluetooth-module-industrial-grade-module-8577. Full HTTPS links appear in docs/ACADEMIC_COMPLETION_RUN.md and the HTML report.')
y=block(y,'Cost and eligibility','Known merchandise subtotals for ten units: 1,950 EGP, 1,950 EGP and 2,950 EGP. Ampere displays a comma decimal price; the normalized 195.00 value is checked against the literal 195,00 EGP text. All subtotals exclude shipping and tax. Warranty is unstated; listed stock does not establish order acceptance for ten units. All three offers are needs_verification. No eligible weighted ranking or purchase recommendation exists.')
y=block(y,'CrewAI run','Run 49bba9141fdb: 6/6 sequential task outputs in 43.51 seconds using local qwen2.5:1.5b-instruct. Actual agent-selected tools: reviewed_supplier_lookup and literal_supplier_extraction. One orchestrator call: deterministic_procurement_assessment after the analyst omitted its tool. The specification, verification and reporting agents produced prose; final HTML is generated from validated Python records.')
c.showPage()
header('EVALUATION AND LIMITS','Testing, ScrapeGraphAI and reproducibility')
y=718
y=block(y,'Automated and browser checks','The automated suite passed 26/26 tests, with no failures or skips. It checks source provenance, independent domains, literal extraction, decimal normalization, configuration and price agreement, eligibility, cost, report consistency, safety, storage, crew structure and fallback labels. The real CrewAI run is separate from fixture tests. The actual HTML and Streamlit screens were opened in a browser; final screenshots are bundled.')
y=block(y,'ScrapeGraphAI','Open-source ScrapeGraphAI 2.3.1 ran locally on reviewed HTML fragments using Ollama. The 1.5B model truncated a product title, while a 3B run once returned all four expected fields and later repeats returned no usable result. Strict validation rejects unsupported values. It is not the production extractor and no reliable accuracy rate is claimed. Tavily was not called because its API key was absent. No paid service was used.')
y=block(y,'Reproduction and remaining gaps','Install Python 3.12 dependencies, start Ollama, pull qwen2.5:1.5b-instruct, run pytest, then call procurepilot.multisource_crew.run_multisource(). Supplier content and model output may change. The bundled trace records the observed run. The original laptop scenario, complete landed costs, warranty, confirmed ten-unit stock, autonomous assessment selection and free cloud hosting remain open.')
y=block(y,'References and release','Direct supplier links and robots/terms review are in docs/REAL_SOURCING_VALIDATION.md. CrewAI: docs.crewai.com; Tavily: docs.tavily.com; ScrapeGraphAI: github.com/ScrapeGraphAI/Scrapegraph-ai. Public source: github.com/fariskishtah/procurepilot-ai. Project source is MIT licensed; third-party materials retain their own terms.')
y=block(y,'Conclusion','ProcurePilot AI now demonstrates genuine independent multi-supplier sourcing and two agent-selected tool calls. It still abstains from recommending a purchase because the evidence does not support complete landed cost or order availability. The academic assignment remains PARTIAL.')
c.save()
print(OUT.resolve())
