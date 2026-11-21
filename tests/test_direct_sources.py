from datetime import datetime, timezone
from decimal import Decimal
import pytest
from procurepilot.direct_sources import DIRECT_PAGES, parse_direct_offer
from procurepilot.catalog_crew import module_request
from procurepilot.engine import rank
from procurepilot.models import Status

NOW=datetime.now(timezone.utc)
MAKERS='''<html><h1>HC-05 Bluetooth Module 3.3V</h1><div class="product-price"><span class="woocommerce-Price-amount">195.00 EGP</span></div><div class="availability stock">Availability: In Stock</div><script type="application/ld+json">{"@type":"Product","name":"HC-05 Bluetooth Module 3.3V","offers":{"price":"195.00","priceCurrency":"EGP","availability":"https://schema.org/InStock"}}</script></html>'''
AMPERE='''<html><h1>HC-05 Bluetooth Module, Serial TTL</h1><p class="price"><span class="woocommerce-Price-amount">195,00 EGP</span></p><p class="stock">141 in stock</p><script type="application/ld+json">{"@type":"Product","name":"HC-05 Bluetooth Module, Serial TTL","offers":{"price":"195.00","priceCurrency":"EGP","availability":"https://schema.org/InStock"}}</script></html>'''
RAM='''<html><section id="product_detail"><h1>HC-05 Original Chip Bluetooth Module - Industrial Grade Module</h1><span class="oe_price">295.00 EGP</span></section></html>'''

def test_three_independent_direct_supplier_pages_and_price_provenance():
    products=[parse_direct_offer(html,DIRECT_PAGES[name],NOW) for name,html in [('Makers Electronics',MAKERS),('Ampere Electronics',AMPERE),('RAM Electronics',RAM)]]
    assert len({p.source_url.host for p in products})==3
    assert [p.price for p in products]==[Decimal('195'),Decimal('195'),Decimal('295')]
    assert [p.availability for p in products]==['in_stock','in_stock',None]
    assert all(p.warranty_months is None for p in products)
    assert all(all(str(e.source_url)==str(p.source_url) and e.content_sha256 for e in p.evidence) for p in products)
    assessed=rank(products,module_request())
    assert all(a.status==Status.NEEDS_VERIFICATION and a.rank is None for a in assessed)
    assert [a.known_total for a in assessed]==[Decimal('1950'),Decimal('1950'),Decimal('2950')]

def test_visible_and_structured_price_must_agree():
    with pytest.raises(ValueError,match='disagree'):
        parse_direct_offer(MAKERS.replace('"195.00"','"295.00"'),DIRECT_PAGES['Makers Electronics'],NOW)

def test_unreviewed_url_and_missing_model_are_rejected():
    with pytest.raises(ValueError,match='reviewed'):
        parse_direct_offer(MAKERS,'https://example.com/product',NOW)
    with pytest.raises(ValueError,match='HC-05'):
        parse_direct_offer(MAKERS.replace('HC-05','HC-06'),DIRECT_PAGES['Makers Electronics'],NOW)

def test_scrapegraph_nested_string_requires_exact_visible_product_fields(monkeypatch):
    import sys, types
    from procurepilot.sources import ScrapeGraphExtractor
    class Graph:
        def __init__(self,**kwargs): pass
        def run(self): return {'content':"{'name': 'HC-05 Bluetooth Module', 'price': '195.00', 'currency': 'EGP', 'availability': 'In Stock'}"}
    graphs=types.ModuleType('scrapegraphai.graphs'); graphs.SmartScraperGraph=Graph
    package=types.ModuleType('scrapegraphai'); package.graphs=graphs
    monkeypatch.setitem(sys.modules,'scrapegraphai',package)
    monkeypatch.setitem(sys.modules,'scrapegraphai.graphs',graphs)
    fields=ScrapeGraphExtractor().extract(MAKERS)
    assert fields=={'price':'195.00','currency':'EGP','availability':'In Stock'}
