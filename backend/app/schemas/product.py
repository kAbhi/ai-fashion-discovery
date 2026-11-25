"""Pydantic schemas for the product catalogue APIs."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductVariantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    size: Optional[str] = None
    colour: Optional[str] = None
    variant_attributes: Optional[dict] = None
    created_at: datetime


class MerchantListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    merchant: str
    current_price: float
    original_price: Optional[float] = None
    currency: str = "INR"
    availability: Optional[str] = None
    purchase_url: Optional[str] = None
    last_updated: datetime


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    brand: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    gender_audience: Optional[str] = None
    style_tags: Optional[List[str]] = None
    occasion_tags: Optional[List[str]] = None
    image_references: Optional[List[str]] = None
    variants: List[ProductVariantOut] = []
    merchant_listings: List[MerchantListingOut] = []
    created_at: datetime
    updated_at: datetime


class ProductListItemOut(BaseModel):
    """Flattened product representation for list endpoints (excludes variants/merchant details)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    brand: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    gender_audience: Optional[str] = None
    style_tags: Optional[List[str]] = None
    occasion_tags: Optional[List[str]] = None
    image_references: Optional[List[str]] = None
    min_price: Optional[float] = None
    currency: str = "INR"
    created_at: datetime


class PaginatedProductOut(BaseModel):
    items: List[ProductListItemOut]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProductFilters(BaseModel):
    """Query parameters for filtering and searching products."""

    category: Optional[str] = Field(
        default=None, description="Exact category match (e.g. ethnic_wear)"
    )
    subcategory: Optional[str] = Field(default=None)
    brand: Optional[str] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    occasion: Optional[str] = Field(
        default=None, description="Match products tagged with this occasion"
    )
    style: Optional[str] = Field(
        default=None, description="Match products tagged with this style"
    )
    colour: Optional[str] = Field(
        default=None, description="Match variants with this colour"
    )
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    q: Optional[str] = Field(
        default=None, description="Free-text search on name/brand/description"
    )


class ProductDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    brand: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    gender_audience: Optional[str] = None
    style_tags: Optional[List[str]] = None
    occasion_tags: Optional[List[str]] = None
    image_references: Optional[List[str]] = None
    variants: List[ProductVariantOut] = []
    merchant_listings: List[MerchantListingOut] = []
    created_at: datetime
    updated_at: datetime


class SimilarProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    brand: str
    category: str
    image_references: Optional[List[str]] = None
    min_price: Optional[float] = None
    currency: str = "INR"
    reason: Optional[str] = None


class MerchantListingSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    merchant: str
    current_price: float
    currency: str = "INR"
    availability: Optional[str] = None