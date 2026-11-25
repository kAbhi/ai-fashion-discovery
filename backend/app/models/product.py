"""Product catalogue ORM models.

All identifiers are UUIDs generated server-side (Python-side default) so no
PostgreSQL extensions such as pgcrypto are required.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func, Index
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    subcategory: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, index=True
    )
    gender_audience: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, index=True
    )
    style_tags: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String(30)), nullable=True
    )
    occasion_tags: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String(30)), nullable=True
    )
    image_references: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String(500)), nullable=True
    )
    # Set to 1 for development seed data; never represents verified live
    # retailer inventory.
    is_sample_data: Mapped[bool] = mapped_column(
        nullable=False, default=1, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    merchant_listings: Mapped[list["MerchantListing"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    interactions: Mapped[list["ProductInteraction"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    size: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    colour: Mapped[Optional[str]] = mapped_column(String(40), nullable=True, index=True)
    variant_attributes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    product: Mapped["Product"] = relationship(back_populates="variants")


class MerchantListing(Base):
    __tablename__ = "merchant_listings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    merchant: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    current_price: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, index=True
    )
    original_price: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    availability: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True, index=True
    )
    # Set to 1 for development seed data; never represents verified live
    # retailer inventory.
    is_sample_data: Mapped[bool] = mapped_column(
        nullable=False, default=1, index=True
    )
    purchase_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    product: Mapped["Product"] = relationship(back_populates="merchant_listings")


Index(
    "ix_products_category_brand",
    Product.category,
    Product.brand,
)
Index(
    "ix_products_occasion_tags_gin",
    Product.occasion_tags,
    postgresql_using="gin",
)
Index(
    "ix_products_style_tags_gin",
    Product.style_tags,
    postgresql_using="gin",
)
