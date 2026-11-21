from __future__ import annotations
import hashlib, ipaddress, json, os, re, socket
from datetime import datetime, timezone
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
from .models import Evidence, Product

class SourceBlocked(ValueError): pass

def validate_public_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise SourceBlocked("Only public HTTPS URLs without credentials are allowed")
    host = parsed.hostname.lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith((".local", ".internal")):
        raise SourceBlocked("Local host blocked")
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise SourceBlocked("Host cannot be resolved") from exc
    for row in addresses:
        address = ipaddress.ip_address(row[4][0])
        if not address.is_global:
            raise SourceBlocked("Non-public address blocked")
    return url

class TavilySearch:
    def __init__(self, max_calls: int = 2):
        self.key = os.getenv("TAVILY_API_KEY")
        self.max_calls = max_calls
        self.calls = 0
        self.events: list[dict] = []

    def search(self, query: str, max_results: int = 5) -> list[dict]:
        if not self.key: raise RuntimeError("TAVILY_API_KEY missing; live search blocked")
        if self.calls >= self.max_calls: raise RuntimeError("Tavily call budget exhausted")
        self.calls += 1
        when = datetime.now(timezone.utc).isoformat()
        try:
            response = httpx.post("https://api.tavily.com/search", headers={"Authorization": f"Bearer {self.key}"}, json={"query": query[:300], "search_depth": "basic", "max_results": min(max_results, 5), "include_answer": False, "include_raw_content": False}, timeout=20)
            response.raise_for_status()
            results = [{"url": validate_public_url(r["url"]), "title": r.get("title", ""), "source": "tavily", "retrieved_at": when} for r in response.json().get("results", [])]
            self.events.append({"tool": "tavily", "at": when, "status": "ok", "count": len(results)})
            return results
        except Exception as exc:
            self.events.append({"tool": "tavily", "at": when, "status": "error", "error": type(exc).__name__})
            raise

def fetch_permitted(url: str, approved_domains: set[str]) -> tuple[str, datetime, str]:
    url = validate_public_url(url)
    host = urlparse(url).hostname.lower()
    if host not in approved_domains: raise SourceBlocked("Source domain requires documented permission review")
    with httpx.Client(follow_redirects=False, timeout=15, headers={"User-Agent": "ProcurePilotAI/0.1 research contact: repository README"}) as client:
        response = client.get(url)
        if response.is_redirect: raise SourceBlocked("Redirects require separate public URL and permission validation")
        response.raise_for_status()
        if len(response.content) > 2_000_000: raise SourceBlocked("Page exceeds size limit")
        if "text/html" not in response.headers.get("content-type", ""): raise SourceBlocked("Expected HTML")
        return response.text, datetime.now(timezone.utc), hashlib.sha256(response.content).hexdigest()

def extract_jsonld(html: str, url: str, captured_at: datetime, capture_mode: str = "live") -> list[Product]:
    """Extract only literal JSON-LD Product fields; unknown claims stay unknown."""
    soup = BeautifulSoup(html, "html.parser")
    found = []
    digest = hashlib.sha256(html.encode()).hexdigest()
    def nodes(obj):
        if isinstance(obj, list):
            for x in obj: yield from nodes(x)
        elif isinstance(obj, dict):
            if obj.get("@type") == "Product" or "Product" in obj.get("@type", []): yield obj
            for x in obj.get("@graph", []): yield from nodes(x)
    for script in soup.select('script[type="application/ld+json"]'):
        try: data = json.loads(script.string or script.get_text())
        except (ValueError, TypeError): continue
        for item in nodes(data):
            offers = item.get("offers", {})
            if isinstance(offers, list): offers = offers[0] if offers else {}
            if not isinstance(offers, dict): offers = {}
            name = str(item.get("name", "")).strip()
            if not name: continue
            brand = item.get("brand")
            if isinstance(brand, dict): brand = brand.get("name")
            seller = offers.get("seller", {})
            if isinstance(seller, dict): seller = seller.get("name")
            supplier = str(seller or urlparse(url).hostname)
            raw_price = offers.get("price")
            try: price = str(raw_price).replace(",", "") if raw_price is not None else None
            except Exception: price = None
            currency = offers.get("priceCurrency")
            evidence = []
            for field, value in [("name", name), ("price", price), ("currency", currency)]:
                if value is not None:
                    evidence.append(Evidence(field=field, value=str(value), excerpt=json.dumps(item, ensure_ascii=False)[:5000], source_url=url, captured_at=captured_at, method="jsonld", content_sha256=digest))
            found.append(Product(id=hashlib.sha256((url + name + str(item.get("sku", ""))).encode()).hexdigest()[:16], name=name, brand=str(brand) if brand else None, model=str(item.get("model")) if item.get("model") else None, supplier=supplier, source_url=url, captured_at=captured_at, capture_mode=capture_mode, price=price, currency=currency, availability="in_stock" if str(offers.get("availability", "")).endswith("InStock") else None, evidence=evidence))
    return found

class ScrapeGraphExtractor:
    """Optional local HTML extraction; model output must pass literal evidence checks."""
    def __init__(self, model: str = "ollama/qwen2.5:1.5b-instruct"):
        self.model = model

    def extract(self, html: str) -> dict:
        from scrapegraphai.graphs import SmartScraperGraph
        soup=BeautifulSoup(html,"html.parser")
        catalog_section=soup.select_one('section[aria-labelledby="offers-heading"]')
        source=f"<html><body>{catalog_section}</body></html>" if catalog_section else html
        prompt=("Extract name, supplier, price and currency from current offers in the first visible offer list only. Exclude stale offers in details. Return JSON." if catalog_section else "Extract product title, brand, model, price, currency, specifications, warranty, availability and seller. Return only fields literally present in the HTML.")
        graph = SmartScraperGraph(prompt=prompt, source=source, config={"llm": {"model": self.model, "base_url": "http://localhost:11434", "model_tokens": 8192, "format": "json", "temperature": 0}, "verbose": False, "headless": True})
        result = graph.run()
        if not isinstance(result, dict): raise ValueError("ScrapeGraph returned no structured object")
        if catalog_section:
            from .catalog import CATALOG_URL, extract_catalog_offers
            expected=extract_catalog_offers(html,CATALOG_URL,datetime.now(timezone.utc))
            allowed={(p.name,p.supplier,f"EGP {p.price}",p.currency) for p in expected}
            candidates=result.get("content",[])
            if not isinstance(candidates,list): candidates=[]
            accepted=[x for x in candidates if isinstance(x,dict) and (x.get("name"),x.get("supplier"),x.get("price"),x.get("currency")) in allowed]
            return {"content":accepted,"rejected_count":len(candidates)-len(accepted),"reference_offer_count":len(expected)}
        visible = soup.get_text(" ", strip=True).lower()
        return {k: v for k, v in result.items() if isinstance(v, (str, int, float)) and str(v).lower() in visible}
