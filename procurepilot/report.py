from __future__ import annotations
from html import escape
from pathlib import Path
from .models import RunResult

def generate(result: RunResult, path: str | Path) -> Path:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    request = result.request
    by_id = {p.id:p for p in result.products}
    rows = []
    for a in result.assessments:
        p = by_id[a.product_id]
        url = escape(str(p.source_url), quote=True)
        rows.append(f"<tr><td>{escape(p.name)}</td><td>{escape(p.supplier)}</td><td>{escape(str(p.price) if p.price is not None else 'Unknown')} {escape(p.currency or '')}</td><td>{escape(a.status.value)}</td><td>{escape(str(a.score) if a.score is not None else '—')}</td><td><a href='{url}'>{url}</a><small>Captured {escape(p.captured_at.isoformat())}; {escape(p.capture_mode)}</small></td></tr>")
    risks = sorted({reason for a in result.assessments for reason in a.reasons})
    if not result.products: risks.append("No source-backed product records were collected; no supplier recommendation is possible.")
    if result.recommendation_id:
        chosen = by_id[result.recommendation_id]
        recommendation = f"Top eligible offer: {escape(chosen.name)} from {escape(chosen.supplier)}. Confirm current terms directly before ordering."
    else: recommendation = "No evidence-supported purchase recommendation is available."
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ProcurePilot procurement report</title><style>
:root{{--navy:#101b32;--blue:#2563eb;--gold:#b89447;--ink:#263144}}*{{box-sizing:border-box}}body{{margin:0;background:#f2f5fa;color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}header{{background:var(--navy);color:white;padding:56px max(24px,calc((100vw - 1060px)/2))}}h1{{font-size:2.5rem;margin:.2em 0}}header p{{color:#cdd8eb}}main{{max-width:1060px;margin:auto;padding:28px 20px 80px}}section{{background:white;border:1px solid #dce3ee;border-radius:14px;padding:24px;margin:20px 0;box-shadow:0 5px 20px #14213d0a}}h2{{color:var(--navy);margin-top:0;border-left:4px solid var(--gold);padding-left:12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}.metric{{padding:14px;background:#f4f7fc;border-radius:9px}}.metric strong{{display:block;font-size:1.25rem}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #e0e7f0;vertical-align:top}}th{{background:#eaf0fb;color:#10203b}}a{{color:var(--blue);overflow-wrap:anywhere}}small{{display:block;color:#67758a}}.warn{{background:#fff7e8;border-left:4px solid var(--gold);padding:16px}}@media(max-width:600px){{h1{{font-size:1.9rem}}section{{padding:16px}}}}@media print{{body{{background:white}}section{{box-shadow:none;break-inside:avoid}}}}</style></head><body><header><div style="color:#dabd75;font-weight:700;letter-spacing:.16em">PROCUREPILOT AI</div><h1>Procurement intelligence report</h1><p>{escape(request.company)} · {escape(request.category)} · {escape(result.created_at.strftime('%Y-%m-%d %H:%M UTC'))}</p><p>Research mode: evidence-first · Run {escape(result.run_id)}</p></header><main>
<section><h2>Executive summary</h2><div class="grid"><div class="metric">Quantity<strong>{request.quantity}</strong></div><div class="metric">Budget<strong>{request.budget} {escape(request.currency)}</strong></div><div class="metric">Suppliers<strong>{len({p.supplier for p in result.products})}</strong></div><div class="metric">Products<strong>{len(result.products)}</strong></div></div><p class="warn">{recommendation}</p></section>
<section><h2>Company context and requirements</h2><p>{escape(request.industry)} · Delivery country: {escape(request.country)}</p><p>Minimum RAM: {request.min_ram_gb or '—'} GB · Storage: {request.min_storage_gb or '—'} GB · Warranty: {request.min_warranty_months or '—'} months · Required terms: {escape(', '.join(request.required_terms))}</p></section>
<section><h2>Sourcing and verification method</h2><p>Six sequential CrewAI roles: sourcing, collection, normalization, analysis, verification, and reporting. Product claims require source excerpts. Numeric eligibility and scoring are calculated in Python. Search and extraction limitations are recorded in the execution trace.</p></section>
<section><h2>Product and supplier comparison</h2><div class="scroll"><table><thead><tr><th>Product</th><th>Supplier</th><th>Unit price</th><th>Eligibility</th><th>Score</th><th>Source evidence</th></tr></thead><tbody>{''.join(rows) or '<tr><td colspan="6">No verified offers were collected.</td></tr>'}</tbody></table></div></section>
<section><h2>Cost and ranking</h2><p>Known cost = unit price × quantity + documented shipping + documented tax when tax is excluded. Unknown components remain unknown. Weights: {escape(str(request.weights))}. Only eligible offers receive a rank.</p></section>
<section><h2>Risks and limitations</h2><ul>{''.join('<li>'+escape(r)+'</li>' for r in risks) or '<li>Source freshness and supplier terms require confirmation before purchase.</li>'}</ul><p>This report is decision support, not a binding quote or purchase order.</p></section>
<section><h2>Source references</h2><ul>{''.join('<li><a href="'+escape(str(p.source_url),quote=True)+'">'+escape(str(p.source_url))+'</a> · '+escape(p.captured_at.isoformat())+'</li>' for p in result.products) or '<li>No product source URLs were accepted.</li>'}</ul></section></main></body></html>'''
    path.write_text(html, encoding="utf-8")
    return path
