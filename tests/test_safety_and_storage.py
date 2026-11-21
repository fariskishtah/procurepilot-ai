from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch, Mock
import pytest
from procurepilot.models import Request, Product, Evidence, RunResult, Status
from procurepilot.engine import rank
from procurepilot.sources import TavilySearch, SourceBlocked, fetch_permitted
from procurepilot.storage import save, load, list_runs
from procurepilot.report import generate

URL="https://example.com/product"
NOW=datetime.now(timezone.utc)
def make_product(**changes):
    fields=dict(id="p1",name="Laptop SSD",supplier="Example",source_url=URL,captured_at=NOW,capture_mode="test",price=Decimal("1000"),currency="EGP",ram_gb=16,storage_gb=512,warranty_months=12,availability="in_stock",shipping=Decimal("50"),tax=Decimal("100"),tax_included=True)
    fields.update(changes)
    evidence=[Evidence(field=k,value=str(fields[k]),excerpt=f"{k}: {fields[k]}",source_url=URL,captured_at=NOW,method="test") for k in ("price","ram_gb","storage_gb","warranty_months") if fields[k] is not None]
    return Product(**fields,evidence=evidence)

def test_tax_not_double_counted():
    a=rank([make_product()],Request(quantity=2,required_terms=[]))[0]
    assert a.known_total==2050 and a.status==Status.ELIGIBLE

def test_currency_mismatch_and_unknown_price():
    assert rank([make_product(currency="USD")],Request(required_terms=[]))[0].status==Status.NEEDS_VERIFICATION
    assert rank([make_product(price=None)],Request(required_terms=[]))[0].status==Status.NEEDS_VERIFICATION

def test_injection_cannot_change_report(tmp_path):
    p=make_product(name='<script>alert("bad")</script>',availability="in_stock")
    a=rank([p],Request(required_terms=[]))
    r=RunResult(run_id="safe",request=Request(required_terms=[]),products=[p],assessments=a,recommendation_status="eligible_offer",recommendation_id=p.id)
    html=generate(r,tmp_path/"safe.html").read_text()
    assert '<script>alert' not in html and '&lt;script&gt;' in html

def test_missing_key_fails_closed(monkeypatch):
    monkeypatch.delenv("TAVILY_API_KEY",raising=False)
    with pytest.raises(RuntimeError,match="missing"):
        TavilySearch().search("laptops")

def test_unreviewed_domain_blocked():
    with pytest.raises(SourceBlocked,match="permission"):
        fetch_permitted(URL,set())

def test_storage_roundtrip(tmp_path):
    path=tmp_path/"runs.db"
    r=RunResult(run_id="abc",request=Request(),products=[],assessments=[],recommendation_status="none")
    save(r,path)
    assert load("abc",path).run_id=="abc"
    assert list_runs(path)[0][0]=="abc"

def test_scrapegraph_adapter_mock(monkeypatch):
    import sys, types
    from procurepilot.sources import ScrapeGraphExtractor
    outer=types.ModuleType("scrapegraphai")
    graphs=types.ModuleType("scrapegraphai.graphs")
    class Graph:
        def __init__(self, **kwargs): self.source=kwargs["source"]
        def run(self): return {"price":"1000", "invented":"9999"}
    graphs.SmartScraperGraph=Graph
    monkeypatch.setitem(sys.modules,"scrapegraphai",outer)
    monkeypatch.setitem(sys.modules,"scrapegraphai.graphs",graphs)
    result=ScrapeGraphExtractor().extract("<html><body>Price: 1000</body></html>")
    assert result=={"price":"1000"}
