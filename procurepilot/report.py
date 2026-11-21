from __future__ import annotations
from html import escape
from pathlib import Path
from .models import RunResult

def e(value) -> str:
    return escape(str(value), quote=True)

def generate(result: RunResult, path: str | Path) -> Path:
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    req=result.request
    by_id={p.id:p for p in result.products}
    rows=[]
    for a in result.assessments:
        p=by_id[a.product_id]
        source_label="Supplier evidence" if p.capture_mode=="live_direct_supplier" else "Catalog evidence"
        source=f'<a href="{e(p.source_url)}">{source_label}</a>'
        if p.supplier_url and str(p.supplier_url)!=str(p.source_url): source+=f' · <a href="{e(p.supplier_url)}">Supplier page</a>'
        check_text=f' · {e(p.source_checked_text)}' if p.source_checked_text else ''
        source+=f'<small>Captured {e(p.captured_at.isoformat())}{check_text} · {e(p.verification_status.replace("_"," "))}</small>'
        availability_text="Listed in stock" if p.availability=="in_stock" else "Unknown"
        rows.append('<tr>'+''.join(f'<td>{value}</td>' for value in [e(p.name),e(p.supplier),e(f"{p.price} {p.currency}" if p.price is not None else "Unknown"),e(p.raw_specs.get("configuration","Unknown")),e(availability_text),e(p.warranty_months if p.warranty_months is not None else "Unknown"),e(a.status.value.replace('_',' ')),e(a.comparison_rank if a.comparison_rank is not None else '—'),source])+'</tr>')
    risks=sorted({reason for a in result.assessments for reason in a.reasons})
    if not result.products: risks.append("No source-backed product records were collected; no supplier recommendation is possible.")
    eligible=sorted((a for a in result.assessments if a.status.value=='eligible' and a.rank is not None),key=lambda a:a.rank)
    if eligible and result.recommendation_id:
        chosen=by_id[result.recommendation_id]
        recommendation=f"Top eligible offer: {e(chosen.name)} from {e(chosen.supplier)}. Confirm terms directly before ordering."
    else: recommendation="INSUFFICIENT VERIFIED EVIDENCE FOR RECOMMENDATION. No purchase order should be placed from this report alone."
    modes=', '.join(sorted({p.capture_mode for p in result.products})) or 'no collected source'
    method_note='Direct supplier product pages provide price observations; ten-unit stock and full landed cost remain unconfirmed.' if all(p.capture_mode=='live_direct_supplier' for p in result.products) and result.products else 'Catalog observations are not direct supplier confirmations.'
    rows_html=''.join(rows) or '<tr><td colspan="9">No verified offers were collected.</td></tr>'
    risks_html=''.join(f'<li>{e(r)}</li>' for r in risks) or '<li>Confirm price, stock, tax, delivery and warranty with the supplier.</li>'
    sources_html=''.join(f'<li><a href="{e(p.source_url)}">{e(p.supplier)} {"supplier page" if p.capture_mode=="live_direct_supplier" else "catalog observation"}</a> · retrieved {e(p.captured_at.isoformat())} · {e(p.verification_status.replace("_"," "))}</li>' for p in result.products) or '<li>No product source URLs were accepted.</li>'
    ram_requirement=f"{req.min_ram_gb} GB" if req.min_ram_gb else "not specified"
    storage_requirement=f"{req.min_storage_gb} GB" if req.min_storage_gb else "not specified"
    warranty_requirement=f"{req.min_warranty_months} months" if req.min_warranty_months else "not specified"
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:"><title>ProcurePilot procurement report</title><style>
:root{{--navy:#101b32;--blue:#2563eb;--gold:#b89447;--ink:#263144}}*{{box-sizing:border-box}}body{{margin:0;background:#f2f5fa;color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}header{{background:var(--navy);color:white;padding:56px max(24px,calc((100vw - 1080px)/2))}}h1{{font-size:2.5rem;margin:.2em 0}}header p{{color:#cdd8eb}}main{{max-width:1080px;margin:auto;padding:28px 20px 80px}}section{{background:white;border:1px solid #dce3ee;border-radius:14px;padding:24px;margin:20px 0;box-shadow:0 5px 20px #14213d0a}}h2{{color:var(--navy);margin-top:0;border-left:4px solid var(--gold);padding-left:12px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}.metric{{padding:14px;background:#f4f7fc;border-radius:9px}}.metric strong{{display:block;font-size:1.25rem}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #e0e7f0;vertical-align:top}}th{{background:#eaf0fb;color:#10203b}}a{{color:var(--blue);overflow-wrap:anywhere}}small{{display:block;color:#67758a}}.warn{{background:#fff7e8;border-left:4px solid var(--gold);padding:16px}}@media(max-width:600px){{h1{{font-size:1.9rem}}section{{padding:16px}}}}@media print{{body{{background:white}}section{{box-shadow:none;break-inside:avoid}}}}</style></head><body><header><div style="color:#dabd75;font-weight:700;letter-spacing:.16em">PROCUREPILOT AI</div><h1>Procurement intelligence report</h1><p>{e(req.company)} · {e(req.category)} · {e(result.created_at.strftime('%Y-%m-%d %H:%M UTC'))}</p><p>Research mode: {e(modes)} · Run {e(result.run_id)}</p></header><main>
<section><h2>Executive summary</h2><div class="grid"><div class="metric">Quantity<strong>{req.quantity}</strong></div><div class="metric">Budget<strong>{req.budget} {e(req.currency)}</strong></div><div class="metric">Suppliers<strong>{len({p.supplier for p in result.products})}</strong></div><div class="metric">Offers<strong>{len(result.products)}</strong></div></div><p class="warn">{recommendation}</p></section>
<section><h2>Company context and requirements</h2><p>{e(req.industry)} · Delivery country: {e(req.country)}</p><p>Minimum RAM: {ram_requirement} · Storage: {storage_requirement} · Warranty: {warranty_requirement} · Required terms: {e(', '.join(req.required_terms))}</p></section>
<section><h2>Research methodology</h2><p>Six sequential CrewAI roles: sourcing, collection, normalization, analysis, verification and reporting. Product claims require source excerpts. Numeric eligibility and price comparison are calculated in Python. This report uses validated records, not the agents' free-form text. {method_note}</p></section>
<section><h2>Supplier, specification and price comparison</h2><div class="scroll"><table><thead><tr><th>Offer</th><th>Supplier</th><th>Observed unit price</th><th>Configuration</th><th>Listed availability</th><th>Warranty months</th><th>Eligibility</th><th>Price-only order</th><th>Source evidence</th></tr></thead><tbody>{rows_html}</tbody></table></div><p>All offers are HC-05 models. Price-only order compares observed unit prices in {e(req.currency)}; it is not a weighted quality rank or purchase recommendation. Confirm ten-unit stock, shipping, tax and warranty directly.</p></section>
<section><h2>Cost and weighted scoring</h2><p>Known cost = unit price × quantity + documented shipping + documented tax when tax is excluded. Unknown components remain unknown. Weights: {e(req.weights)}. Only eligible offers receive a weighted value score or final rank.</p></section>
<section><h2>Risk assessment</h2><ul>{risks_html}</ul><p>Observed prices can change and are not binding supplier quotations. The procurement team must confirm bulk quantity, delivery, tax and warranty directly before purchase.</p></section>
<section><h2>Source references</h2><ul>{sources_html}</ul></section></main></body></html>'''
    path.write_text(html,encoding="utf-8")
    return path
