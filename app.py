from __future__ import annotations
from decimal import Decimal
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from procurepilot.models import Request, RunResult
from procurepilot.crew import run
from procurepilot.storage import save, list_runs, load
from procurepilot.engine import rank

st.set_page_config(page_title="ProcurePilot AI", page_icon="◆", layout="wide")
st.markdown('''<style>
.stApp{background:#f3f6fb;color:#182337}.block-container{max-width:1360px;padding-top:2rem}h1,h2,h3{color:#101c32!important}.stButton button[kind="primary"]{background:#2563eb;border:0;border-radius:9px}.stMetric{background:#fff;padding:12px;border-radius:10px;border:1px solid #dce3ee}.hero{background:linear-gradient(120deg,#111c33,#203f76);color:white;padding:32px 38px;border-radius:17px;margin-bottom:20px}.hero h1{color:white!important;margin:0}.hero p{color:#d3dfef;margin:7px 0 0}.eyebrow{color:#e0bf70;letter-spacing:.2em;font-size:.75rem;font-weight:800}.status{background:#fff7e7;padding:14px;border-left:4px solid #c19a50;border-radius:6px}</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow">PROCUREPILOT AI</div><h1>AI-Powered Procurement Intelligence</h1><p>From sourcing to strategy — one intelligent procurement workflow.</p></div>', unsafe_allow_html=True)
with st.sidebar:
    st.subheader("Workspace")
    page = st.radio("Navigate", ["Overview", "Request Builder", "Agent Timeline", "Products & Suppliers", "Scoring & Costs", "Evidence Inspector", "Report Center"], label_visibility="collapsed")
    previous = list_runs()
    if previous:
        run_id = st.selectbox("Previous runs", ["Current"] + [x[0] for x in previous])
        if run_id != "Current": st.session_state.result = load(run_id)
result: RunResult | None = st.session_state.get("result")
if page == "Request Builder":
    st.header("Procurement request")
    with st.form("request"):
        a,b,c = st.columns(3)
        with a:
            company=st.text_input("Company", "NileTech Operations")
            industry=st.text_input("Industry", "Technology and operations (fictional demo company)")
            category=st.text_input("Product category", "business laptops")
            country=st.text_input("Delivery country", "Egypt")
        with b:
            quantity=st.number_input("Quantity", min_value=1, value=10)
            budget=st.number_input("Maximum budget", min_value=1.0, value=300000.0, step=1000.0)
            currency=st.text_input("Currency (ISO code)", "EGP")
            ram=st.number_input("Minimum RAM, GB (0 = none)", min_value=0, value=16)
            storage=st.number_input("Minimum storage, GB (0 = none)", min_value=0, value=512)
        with c:
            warranty=st.number_input("Minimum warranty, months (0 = none)", min_value=0, value=12)
            terms=st.text_input("Required terms (comma separated)", "SSD")
            excluded=st.text_input("Excluded brands (comma separated)", "")
            urls=st.text_area("Reviewed product URLs (one per line)", help="Only HTTPS pages from documented approved domains will be fetched.")
            domains=st.text_input("Approved domains after terms review (comma separated)")
        st.caption("Scoring weights must total 100%")
        cols=st.columns(5)
        weights={key:cols[i].number_input(key.title(), min_value=0,max_value=100,value=val) for i,(key,val) in enumerate({"price":35,"specifications":35,"warranty":15,"availability":10,"evidence":5}.items())}
        submitted=st.form_submit_button("Run six-agent research", type="primary")
    if submitted:
        try:
            request=Request(company=company,industry=industry,category=category,country=country,quantity=quantity,budget=Decimal(str(budget)),currency=currency,min_ram_gb=ram or None,min_storage_gb=storage or None,min_warranty_months=warranty or None,required_terms=[x.strip() for x in terms.split(',') if x.strip()],excluded_brands=[x.strip() for x in excluded.split(',') if x.strip()],weights=weights)
            with st.spinner("Running source checks and sequential CrewAI tasks. This may take several minutes on a local model."):
                result=run(request,seed_urls=[x.strip() for x in urls.splitlines() if x.strip()],approved_domains={x.strip().lower() for x in domains.split(',') if x.strip()})
                save(result)
                st.session_state.result=result
            st.success(f"Run {result.run_id} saved. Crew completed: {result.crew_completed}.")
        except Exception as exc: st.error(f"Run failed: {type(exc).__name__}: {exc}")
else:
    if result is None:
        st.info("Start in Request Builder. No procurement results are shown until a real run is saved.")
    elif page == "Overview":
        st.header("Executive overview")
        cols=st.columns(5)
        for col,label,value in zip(cols,["Company","Category","Quantity","Products","Suppliers"],[result.request.company,result.request.category,result.request.quantity,len(result.products),len({p.supplier for p in result.products})]): col.metric(label,value)
        st.markdown(f'<div class="status">Recommendation status: <b>{result.recommendation_status}</b>. CrewAI completed: <b>{result.crew_completed}</b>. Run ID: {result.run_id}</div>',unsafe_allow_html=True)
        st.caption(f"Budget: {result.request.budget} {result.request.currency} · Created: {result.created_at.isoformat()}")
    elif page == "Agent Timeline":
        st.header("Real execution timeline")
        for event in result.task_trace:
            with st.expander(f"{event.get('stage','task')} · {event.get('agent',event.get('tool',''))} · {event.get('status','')}"):
                st.json(event)
    elif page == "Products & Suppliers":
        st.header("Product intelligence")
        if not result.products: st.warning("No source-backed products were collected in this run.")
        else:
            rows=[{"Product":p.name,"Supplier":p.supplier,"Price":float(p.price) if p.price is not None else None,"Currency":p.currency,"RAM GB":p.ram_gb,"Storage GB":p.storage_gb,"Warranty months":p.warranty_months,"Availability":p.availability,"Source":str(p.source_url)} for p in result.products]
            st.dataframe(pd.DataFrame(rows),use_container_width=True)
    elif page == "Scoring & Costs":
        st.header("Eligibility, scoring, and cost")
        st.write("Weights:",result.request.weights)
        new={}
        cols=st.columns(5)
        for i,(k,v) in enumerate(result.request.weights.items()): new[k]=cols[i].number_input(k.title(),0,100,v,key=f"weight_{k}")
        if sum(new.values())==100:
            req=result.request.model_copy(update={"weights":new})
            assessment=rank(result.products,req)
        else:
            st.error("Weights must total 100%")
            assessment=result.assessments
        rows=[{"Product":next((p.name for p in result.products if p.id==a.product_id),a.product_id),"Status":a.status.value,"Known total":float(a.known_total) if a.known_total is not None else None,"Complete total":a.total_is_complete,"Score":float(a.score) if a.score is not None else None,"Rank":a.rank,"Reasons":"; ".join(a.reasons)} for a in assessment]
        if rows:
            df=pd.DataFrame(rows);st.dataframe(df,use_container_width=True)
            costs=df.dropna(subset=["Known total"])
            if not costs.empty:st.plotly_chart(px.bar(costs,x="Product",y="Known total",color="Status",title="Known cost only; unknown components excluded"),use_container_width=True)
        else: st.info("No offers to score.")
    elif page == "Evidence Inspector":
        st.header("Source evidence")
        if not result.products: st.info("No accepted product evidence in this run.")
        for p in result.products:
            with st.expander(p.name):
                st.write("Source:",str(p.source_url),"Captured:",p.captured_at,"Mode:",p.capture_mode)
                for e in p.evidence:st.json(e.model_dump(mode="json"))
    elif page == "Report Center":
        st.header("Procurement report")
        if result.report_path and Path(result.report_path).exists():
            html=Path(result.report_path).read_text()
            st.download_button("Download HTML report",html,file_name="ProcurePilot_Procurement_Report.html",mime="text/html")
            st.iframe(Path(result.report_path), height=800, alt="Procurement HTML report preview")
        else:st.warning("Report file missing")
