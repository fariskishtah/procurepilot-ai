from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator

class Status(StrEnum):
    ELIGIBLE = "eligible"
    REJECTED = "rejected"
    NEEDS_VERIFICATION = "needs_verification"

class Request(BaseModel):
    company: str = "NileTech Operations"
    industry: str = "Technology and operations (fictional demo company)"
    category: str = "business laptops"
    quantity: int = Field(default=10, ge=1, le=10000)
    budget: Decimal = Field(default=Decimal("300000"), gt=0)
    currency: str = "EGP"
    country: str = "Egypt"
    min_ram_gb: int | None = Field(default=16, ge=1)
    min_storage_gb: int | None = Field(default=512, ge=1)
    min_warranty_months: int | None = Field(default=12, ge=1)
    required_terms: list[str] = Field(default_factory=lambda: ["SSD"])
    excluded_brands: list[str] = Field(default_factory=list)
    preferred_brands: list[str] = Field(default_factory=list)
    weights: dict[str, int] = Field(default_factory=lambda: {"price": 35, "specifications": 35, "warranty": 15, "availability": 10, "evidence": 5})

    @field_validator("currency")
    @classmethod
    def currency_code(cls, value: str) -> str:
        value = value.upper().strip()
        if len(value) != 3 or not value.isalpha():
            raise ValueError("Use an ISO 4217 three-letter currency code")
        return value

    @model_validator(mode="after")
    def valid_weights(self):
        if set(self.weights) != {"price", "specifications", "warranty", "availability", "evidence"} or any(v < 0 for v in self.weights.values()) or sum(self.weights.values()) != 100:
            raise ValueError("Scoring weights must be nonnegative and total 100")
        return self

class Evidence(BaseModel):
    field: str
    value: str
    excerpt: str
    source_url: HttpUrl
    captured_at: datetime
    method: str
    content_sha256: str | None = None

class Product(BaseModel):
    id: str
    name: str
    supplier: str
    source_url: HttpUrl
    supplier_url: HttpUrl | None = None
    captured_at: datetime
    capture_mode: str
    verification_status: str = "direct_source"
    source_checked_text: str | None = None
    brand: str | None = None
    model: str | None = None
    category: str | None = None
    price: Decimal | None = Field(default=None, ge=0)
    currency: str | None = None
    ram_gb: int | None = None
    storage_gb: int | None = None
    processor: str | None = None
    display: str | None = None
    warranty_months: int | None = None
    availability: str | None = None
    shipping: Decimal | None = Field(default=None, ge=0)
    tax: Decimal | None = Field(default=None, ge=0)
    tax_included: bool | None = None
    raw_specs: dict[str, str] = Field(default_factory=dict)
    evidence: list[Evidence] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)

class Assessment(BaseModel):
    product_id: str
    status: Status
    reasons: list[str]
    known_total: Decimal | None = None
    total_is_complete: bool = False
    score: Decimal | None = None
    rank: int | None = None
    comparison_rank: int | None = None

class RunResult(BaseModel):
    run_id: str
    request: Request
    products: list[Product]
    assessments: list[Assessment]
    recommendation_id: str | None = None
    recommendation_status: str
    report_path: str | None = None
    crew_completed: bool = False
    task_trace: list[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
