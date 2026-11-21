"""Exact, reviewed supplier product pages for the HC-05 R&D demonstration."""
from __future__ import annotations
import hashlib, re
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .models import Evidence, Product
from .sources import extract_jsonld

DIRECT_PAGES = {
    "Makers Electronics": "https://makerselectronics.com/product/hc-05-bluetooth-module-3-3v/",
    "Ampere Electronics": "https://ampere-electronics.com/product/hc-05-bluetooth-module-serial-ttl/",
    "RAM Electronics": "https://www.ram-e-shop.com/shop/kit-bluetooth-hc05-original-hc-05-original-chip-bluetooth-module-industrial-grade-module-8577",
}
PRICE_SELECTORS = {
    "Makers Electronics": ".product-price .woocommerce-Price-amount",
    "Ampere Electronics": "p.price .woocommerce-Price-amount",
    "RAM Electronics": "#product_detail .oe_price",
}
CONFIGURATIONS = {
    "Makers Electronics": "3.3V",
    "Ampere Electronics": "Serial TTL",
    "RAM Electronics": "Industrial Grade",
}

def parse_direct_offer(html: str, url: str, captured_at: datetime) -> Product:
    supplier = next((name for name, expected in DIRECT_PAGES.items() if expected == url), None)
    if supplier is None: raise ValueError("Direct product URL was not reviewed")
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one("h1")
    price_node = soup.select_one(PRICE_SELECTORS[supplier])
    if not title or not price_node: raise ValueError("Product title or price missing")
    name = title.get_text(" ", strip=True)
    if "HC-05" not in name: raise ValueError("Expected HC-05 model missing")
    if CONFIGURATIONS[supplier] not in name: raise ValueError("Expected configuration missing from title")
    price_text = price_node.get_text(" ", strip=True).replace("\xa0", " ")
    pattern = r"([\d,]+(?:\.\d{2})?)\s*EGP" if supplier != "Ampere Electronics" else r"([\d.]+,\d{2})\s*EGP"
    match = re.fullmatch(pattern, price_text)
    if not match: raise ValueError("Unexpected price or currency format")
    amount = Decimal(match.group(1).replace(",", "") if supplier != "Ampere Electronics" else match.group(1).replace(".", "").replace(",", "."))
    # Structured data is a cross-check, never a source of extra facts.
    if supplier != "RAM Electronics":
        jsonld = [p for p in extract_jsonld(html, url, captured_at) if "HC-05" in p.name]
        if len(jsonld) != 1 or jsonld[0].price != amount or jsonld[0].currency != "EGP":
            raise ValueError("Visible offer and JSON-LD disagree")
    stock_node = soup.select_one(".availability.stock") if supplier == "Makers Electronics" else soup.select_one("p.stock") if supplier == "Ampere Electronics" else None
    stock_text = stock_node.get_text(" ", strip=True) if stock_node else ""
    availability = "in_stock" if (supplier == "Makers Electronics" and "In Stock" in stock_text) or (supplier == "Ampere Electronics" and re.search(r"\d+ in stock", stock_text, re.I)) else None
    digest = hashlib.sha256(html.encode()).hexdigest()
    evidence = [Evidence(field="name",value=name,excerpt=name,source_url=url,captured_at=captured_at,method="direct_visible_html",content_sha256=digest),
                Evidence(field="model",value="HC-05",excerpt=name,source_url=url,captured_at=captured_at,method="direct_visible_html",content_sha256=digest),
                Evidence(field="configuration",value=CONFIGURATIONS[supplier],excerpt=name,source_url=url,captured_at=captured_at,method="direct_visible_html",content_sha256=digest),
                Evidence(field="price",value=str(amount),excerpt=f"{name} | {price_text}",source_url=url,captured_at=captured_at,method="direct_visible_html",content_sha256=digest),
                Evidence(field="currency",value="EGP",excerpt=price_text,source_url=url,captured_at=captured_at,method="direct_visible_html",content_sha256=digest)]
    if availability:
        evidence.append(Evidence(field="availability",value="in_stock",excerpt=stock_text,source_url=url,captured_at=captured_at,method="direct_visible_html",content_sha256=digest))
    return Product(id=hashlib.sha256(url.encode()).hexdigest()[:16],name=name,supplier=supplier,source_url=url,supplier_url=url,captured_at=captured_at,capture_mode="live_direct_supplier",verification_status="supplier_page_observed",model="HC-05",category="wireless serial modules",price=amount,currency="EGP",availability=availability,raw_specs={"model":"HC-05","configuration":CONFIGURATIONS[supplier]},evidence=evidence)
