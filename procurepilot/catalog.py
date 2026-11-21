"""Permission-reviewed makhzan product-page adapter; no search/API crawling."""
from __future__ import annotations
import hashlib, re
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .models import Evidence, Product

CATALOG_URL = "https://makhzan.merope.dev/products/b8c70b58-ff9c-406e-8d22-e256089ce7ca-hc-05-bluetooth-module-serial-ttl"
CATALOG_HOST = "makhzan.merope.dev"

def _live_offer_rows(html: str):
    soup = BeautifulSoup(html, "html.parser")
    section = soup.select_one('section[aria-labelledby="offers-heading"]')
    if section is None: raise ValueError("Offer section missing")
    current = section.select_one("ul")
    if current is None: raise ValueError("Current offer list missing")
    return current.select("li[data-offer]")

def catalog_leads(html: str) -> list[dict]:
    leads=[]
    for row in _live_offer_rows(html):
        title=row.select_one('[data-offer-title="true"]')
        shop=row.select_one('a[href^="/shops/"]')
        target=row.select_one('a[aria-label^="View at"]')
        if title and shop and target:
            leads.append({"title":title.get_text(" ",strip=True),"supplier":shop.get_text(" ",strip=True),"supplier_url":target.get("href")})
    return leads

def extract_catalog_offers(html: str, url: str, captured_at: datetime) -> list[Product]:
    if urlparse(url).hostname != CATALOG_HOST: raise ValueError("Unexpected catalog host")
    digest=hashlib.sha256(html.encode()).hexdigest()
    offers=[]
    for row in _live_offer_rows(html):
        title=row.select_one('[data-offer-title="true"]')
        shop=row.select_one('a[href^="/shops/"]')
        target=row.select_one('a[aria-label^="View at"]')
        price_node=row.select_one('[data-price="true"]')
        freshness=row.select_one('[data-freshness]')
        if not all((title,shop,target,price_node)): continue
        price_text=price_node.get_text(" ",strip=True)
        match=re.fullmatch(r"EGP\s+([\d,]+(?:\.\d{1,2})?)",price_text)
        if not match: continue
        name=title.get_text(" ",strip=True)
        supplier=shop.get_text(" ",strip=True)
        supplier_url=target.get("href")
        checked=freshness.get_text(" ",strip=True) if freshness else None
        excerpt=f"{name} | {supplier} | {price_text} | {checked or 'check time unknown'}"
        evidence=[Evidence(field=field,value=value,excerpt=excerpt,source_url=url,captured_at=captured_at,method="catalog_html",content_sha256=digest) for field,value in (("name",name),("supplier",supplier),("price",str(Decimal(match.group(1).replace(',','')))),("currency","EGP"))]
        if "HC-05" in name:
            evidence.append(Evidence(field="model",value="HC-05",excerpt=name,source_url=url,captured_at=captured_at,method="catalog_html",content_sha256=digest))
        offers.append(Product(id=row.get("data-offer"),name=name,supplier=supplier,supplier_url=supplier_url,source_url=url,captured_at=captured_at,capture_mode="live_catalog",verification_status="aggregator_observed",source_checked_text=checked,model="HC-05" if "HC-05" in name else None,category="wireless serial modules",price=Decimal(match.group(1).replace(',','')),currency="EGP",availability=None,raw_specs={"model":"HC-05"} if "HC-05" in name else {},evidence=evidence))
    return offers
