from datetime import datetime, timezone
from decimal import Decimal
import pytest
from procurepilot.models import Request, Product, Evidence, Status
from procurepilot.engine import rank
from procurepilot.sources import validate_public_url, SourceBlocked, extract_jsonld
from procurepilot.report import generate
from procurepilot.models import RunResult

URL="https://example.com/laptop"
NOW=datetime.now(timezone.utc)
def product(**kwargs):
    data=dict(id="one",name="Example Laptop SSD",supplier="Example",source_url=URL,captured_at=NOW,capture_mode="test",brand="Example",price=Decimal("10000"),currency="EGP",ram_gb=16,storage_gb=512,warranty_months=12,availability="in_stock",shipping=Decimal("100"),tax_included=True,raw_specs={"storage":"512GB SSD"})
    data.update(kwargs)
    evidence=[Evidence(field=f,value=str(data[f]),excerpt=f"{f}: {data[f]}",source_url=URL,captured_at=NOW,method="test") for f in ("price","ram_gb","storage_gb","warranty_months") if data.get(f) is not None]
    return Product(**data,evidence=evidence)

def test_weights():
    with pytest.raises(ValueError):Request(weights={"price":50})
def test_eligible_and_budget():
    p=product(); assert rank([p],Request())[0].status==Status.ELIGIBLE
    assert rank([p],Request(budget=Decimal("50000")))[0].status==Status.REJECTED
def test_missing_mandatory():
    assert rank([product(ram_gb=None)],Request())[0].status==Status.NEEDS_VERIFICATION
def test_unknown_shipping():
    assert rank([product(shipping=None)],Request())[0].status==Status.NEEDS_VERIFICATION
def test_ranking_is_deterministic():
    a,b=product(id="a"),product(id="b",price=Decimal("15000"))
    scores=rank([a,b],Request())
    assert scores[0].rank==1 and scores[1].rank==2
def test_url_blocks_private():
    with pytest.raises(SourceBlocked):validate_public_url("https://127.0.0.1/private")
    with pytest.raises(SourceBlocked):validate_public_url("http://example.com")
def test_jsonld_literal():
    html='<script type="application/ld+json">{"@type":"Product","name":"Office Laptop","offers":{"price":"12000","priceCurrency":"EGP"}}</script>'
    products=extract_jsonld(html,URL,NOW)
    assert len(products)==1 and products[0].price==12000 and products[0].ram_gb is None
def test_report_no_fabrication(tmp_path):
    result=RunResult(run_id="test",request=Request(),products=[],assessments=[],recommendation_status="no_verified_recommendation")
    html=generate(result,tmp_path/"report.html").read_text()
    assert "No evidence-supported purchase recommendation" in html
    assert "No verified offers were collected" in html
