from datetime import datetime, timezone
from decimal import Decimal
import pytest
from procurepilot.catalog import CATALOG_URL, catalog_leads, extract_catalog_offers
from procurepilot.catalog_crew import module_request
from procurepilot.engine import rank
from procurepilot.models import Status

HTML='''<section aria-labelledby="offers-heading"><h2 id="offers-heading">Offers</h2><ul>
<li data-offer="offer-1"><span data-offer-title="true">HC-05 Bluetooth Module</span><a href="/shops/one">Shop One</a><span data-freshness="quiet">checked 1 day ago</span><span data-price="true">EGP 195</span><a aria-label="View at Shop One" href="https://shop-one.example/product/hc05">View</a></li>
<li data-offer="offer-2"><span data-offer-title="true">HC-05 Serial Module</span><a href="/shops/two">Shop Two</a><span data-price="true">EGP 205</span><a aria-label="View at Shop Two" href="https://shop-two.example/product/hc05">View</a></li>
</ul><details><ul><li data-offer="old"><span data-offer-title="true">HC-05 old</span><span data-price="true">EGP 99</span></li></ul></details></section>'''
NOW=datetime.now(timezone.utc)

def test_live_offer_list_excludes_stale_details():
    leads=catalog_leads(HTML)
    assert len(leads)==2 and leads[0]["supplier"]=="Shop One"
    products=extract_catalog_offers(HTML,CATALOG_URL,NOW)
    assert len(products)==2
    assert [p.price for p in products]==[Decimal("195"),Decimal("205")]
    assert products[0].verification_status=="aggregator_observed"
    assert products[0].availability is None
    assert products[0].source_checked_text=="checked 1 day ago"
    assert products[0].evidence[0].content_sha256

def test_catalog_offer_comparison_never_becomes_purchase_approval():
    products=extract_catalog_offers(HTML,CATALOG_URL,NOW)
    assessments=rank(products,module_request())
    assert [a.comparison_rank for a in assessments]==[1,2]
    assert all(a.status==Status.NEEDS_VERIFICATION and a.rank is None for a in assessments)
    assert all("Supplier page was not independently verified" in a.reasons for a in assessments)

def test_catalog_rejects_wrong_host_and_malformed_rows():
    with pytest.raises(ValueError,match="host"):
        extract_catalog_offers(HTML,"https://example.com/product",NOW)
    with pytest.raises(ValueError,match="Offer section"):
        catalog_leads("<html></html>")

def test_orchestrator_recovery_is_labeled_not_agent_selected(monkeypatch,tmp_path):
    from crewai import Crew
    import procurepilot.catalog_crew as module
    def failed_kickoff(self): raise RuntimeError("Local model unavailable")
    monkeypatch.setattr(Crew,"kickoff",failed_kickoff)
    monkeypatch.setattr(module,"fetch_permitted",lambda url,hosts:(HTML,NOW,"synthetic-test-hash"))
    result=module.run_catalog(output_dir=tmp_path)
    assert result.crew_completed is False
    assert len(result.products)==2
    assert not any(e.get("stage")=="agent_tool" for e in result.task_trace)
    assert sum(e.get("stage")=="orchestrator_tool" for e in result.task_trace)==3
    assert result.report_path
