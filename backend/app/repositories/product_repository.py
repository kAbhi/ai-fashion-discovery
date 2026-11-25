"""Repository layer for product catalogue queries.

All database access for products lives here. API route handlers never
contain SQLAlchemy queries.
"""

from typing import Optional, Sequence

from sqlalchemy import or_, select, func
from sqlalchemy.orm import Session, joinedload

from app.models.product import MerchantListing, Product, ProductVariant
from app.schemas.product import ProductFilters


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, product_id: str) -> Optional[Product]:
        """Return a product by ID with variants and merchant listings loaded."""
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                joinedload(Product.variants),
                joinedload(Product.merchant_listings),
            )
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def list(
        self,
        *,
        filters: ProductFilters,
        page: int,
        page_size: int,
    ) -> tuple[Sequence[Product], int]:
        """Return a paginated, filtered list of products and the total count."""
        stmt = select(Product).where(Product.is_sample_data.is_(True))

        # Category / subcategory / brand / gender are exact matches.
        if filters.category:
            stmt = stmt.where(Product.category == filters.category)
        if filters.subcategory:
            stmt = stmt.where(Product.subcategory == filters.subcategory)
        if filters.brand:
            stmt = stmt.where(Product.brand.ilike(filters.brand))
        if filters.gender:
            stmt = stmt.where(Product.gender_audience == filters.gender)

        # Occasion / style are array contains matches.
        if filters.occasion:
            stmt = stmt.where(Product.occasion_tags.contains([filters.occasion]))
        if filters.style:
            stmt = stmt.where(Product.style_tags.contains([filters.style]))

        # Free-text search across name, brand and description.
        if filters.q:
            search = f"%{filters.q}%"
            stmt = stmt.where(
                or_(
                    Product.name.ilike(search),
                    Product.brand.ilike(search),
                    Product.description.ilike(search),
                )
            )

        # Count total before applying pagination.
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.execute(count_stmt).scalar_one()

        # Apply pagination + ordering.
        offset = (page - 1) * page_size
        stmt = (
            stmt.order_by(Product.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        items = self.session.execute(stmt).scalars().all()
        return items, total

    def list_merchant_listings(
        self, *, product_id: str
    ) -> Sequence[MerchantListing]:
        """Return merchant listings for a product."""
        stmt = (
            select(MerchantListing)
            .where(MerchantListing.product_id == product_id)
            .order_by(MerchantListing.current_price.asc())
        )
        return self.session.execute(stmt).scalars().all()

    def find_similar(
        self, *, product_id: str, limit: int = 6
    ) -> Sequence[Product]:
        """Return products sharing category or tags with the given product."""
        product = self.get(product_id)
        if product is None:
            return []

        conditions = [
            Product.id != product_id,
            Product.is_sample_data.is_(True),
        ]
        if product.category:
            conditions.append(Product.category == product.category)
        if product.brand:
            conditions.append(Product.brand == product.brand)

        stmt = (
            select(Product)
            .where(*conditions)
            .order_by(Product.created_at.desc())
            .limit(limit)
        )
        return self.session.execute(stmt).scalars().all()

    def get_variant(self, variant_id: str) -> Optional[ProductVariant]:
        stmt = select(ProductVariant).where(ProductVariant.id == variant_id)
        return self.session.execute(stmt).scalar_one_or_none()
