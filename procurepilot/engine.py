from __future__ import annotations
from decimal import Decimal
from .models import Request, Product, Assessment, Status

REQUIRED_EVIDENCE = {"price": "price", "ram_gb": "ram_gb", "storage_gb": "storage_gb", "warranty_months": "warranty_months"}

def has_evidence(product: Product, field: str) -> bool:
    return any(e.field == field and e.value and e.excerpt and e.value.lower() in e.excerpt.lower() for e in product.evidence)

def assess(product: Product, request: Request) -> Assessment:
    rejected, unknown = [], []
    if product.brand and product.brand.lower() in {x.lower() for x in request.excluded_brands}:
        rejected.append("Excluded brand")
    for field, minimum, label in [("ram_gb", request.min_ram_gb, "RAM"), ("storage_gb", request.min_storage_gb, "storage"), ("warranty_months", request.min_warranty_months, "warranty")]:
        if minimum is None: continue
        value = getattr(product, field)
        if value is None or not has_evidence(product, field): unknown.append(f"{label} requires source verification")
        elif value < minimum: rejected.append(f"{label} below minimum {minimum}")
    if request.required_terms:
        haystack = " ".join([product.name, *product.raw_specs.values()]).lower()
        for term in request.required_terms:
            if term.lower() not in haystack: unknown.append(f"Required term {term} not evidenced")
    if product.price is None or not has_evidence(product, "price"):
        unknown.append("Price requires source verification")
    if product.currency != request.currency: unknown.append("Currency is missing or differs from request")
    known_total = None
    complete = False
    if product.price is not None and product.currency == request.currency and has_evidence(product, "price"):
        known_total = product.price * request.quantity
        if product.shipping is not None: known_total += product.shipping
        if product.tax is not None and not product.tax_included: known_total += product.tax
        complete = product.shipping is not None and (product.tax is not None or product.tax_included is True)
        if known_total > request.budget: rejected.append("Known cost exceeds budget")
        if not complete: unknown.append("Shipping or tax is unknown")
    if product.conflicts: unknown.append("Conflicting source claims")
    if product.availability != "in_stock": unknown.append("Availability not confirmed")
    if rejected: status = Status.REJECTED
    elif unknown: status = Status.NEEDS_VERIFICATION
    else: status = Status.ELIGIBLE
    return Assessment(product_id=product.id, status=status, reasons=rejected + unknown, known_total=known_total, total_is_complete=complete)

def rank(products: list[Product], request: Request) -> list[Assessment]:
    assessments = [assess(p, request) for p in products]
    eligible = [(p, a) for p, a in zip(products, assessments) if a.status == Status.ELIGIBLE]
    if not eligible: return assessments
    prices = [p.price for p, _ in eligible]
    low, high = min(prices), max(prices)
    for p, a in eligible:
        price_score = Decimal(100) if high == low else (high - p.price) / (high - low) * 100
        spec_score = min(Decimal(100), Decimal(p.ram_gb or 0) / Decimal(request.min_ram_gb or 16) * 50 + Decimal(p.storage_gb or 0) / Decimal(request.min_storage_gb or 512) * 50)
        warranty_score = min(Decimal(100), Decimal(p.warranty_months or 0) / Decimal(max(request.min_warranty_months or 12, 1)) * 100)
        availability_score = Decimal(100) if p.availability == "in_stock" else Decimal(0)
        evidence_score = Decimal(min(100, len({e.field for e in p.evidence}) * 20))
        values = {"price": price_score, "specifications": spec_score, "warranty": warranty_score, "availability": availability_score, "evidence": evidence_score}
        a.score = sum(values[k] * Decimal(request.weights[k]) / 100 for k in values).quantize(Decimal("0.01"))
    for index, (_, a) in enumerate(sorted(eligible, key=lambda pair: (-pair[1].score, pair[0].price, pair[0].id)), 1): a.rank = index
    return assessments
