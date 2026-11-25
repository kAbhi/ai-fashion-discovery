"""Shopping session, interaction, preference, wishlist and comparison models.

All identifiers are UUIDs generated server-side (Python-side default).
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func, Index
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ShoppingSession(Base):
    __tablename__ = "shopping_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
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

    interactions: Mapped[list["ProductInteraction"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    preferences: Mapped[list["UserPreference"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    comparisons: Mapped[list["ProductComparison"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class ProductInteraction(Base):
    __tablename__ = "product_interactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shopping_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # view | like | dislike | save | compare
    interaction_type: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session: Mapped["ShoppingSession"] = relationship(back_populates="interactions")
    product: Mapped["Product"] = relationship(back_populates="interactions")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shopping_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # style | colour | brand | category | price_max | ...
    preference_type: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True
    )
    preference_value: Mapped[str] = mapped_column(String(100), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    session: Mapped["ShoppingSession"] = relationship(back_populates="preferences")


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shopping_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session: Mapped["ShoppingSession"] = relationship(back_populates="wishlist_items")
    product: Mapped["Product"] = relationship(back_populates="wishlist_items")


class ProductComparison(Base):
    __tablename__ = "product_comparisons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("shopping_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # UUIDs of products being compared (MVP: 2-4 products).
    product_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=False
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

    session: Mapped["ShoppingSession"] = relationship(back_populates="comparisons")


Index(
    "ix_product_interactions_session_type",
    ProductInteraction.session_id,
    ProductInteraction.interaction_type,
)
Index(
    "ix_user_preferences_session_type",
    UserPreference.session_id,
    UserPreference.preference_type,
)
Index(
    "ix_wishlist_items_session_product",
    WishlistItem.session_id,
    WishlistItem.product_id,
    unique=True,
)
