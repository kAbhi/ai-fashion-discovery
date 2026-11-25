"""Service layer for the product catalogue.

Coordinates between the repository and the API, translating ORM models into
Pydantic response schemas. Keeps business logic out of route handlers.
"""

from typing import Optional, Sequence

from app.repositories.product_repository import ProductRepository
from app.schemas.pagination import PageParams
from app.schemas.product import (
    MerchantListingOut,
    ProductDetailOut,
    ProductFilters,
    ProductListItemOut,
    PaginatedProductOut,
    SimilarProductOut,
)


class CatalogueService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(
        self,
        *,
        filters: ProductFilters,
        page_params: PageParams,
    ) -> PaginatedProductOut:
        items, total = self.repository.list(
            filters=filters, page=page_params.page, page_size=page_params.page_size
        )
        return PaginatedProductOut(
            items=[self._to_list_item(item) for item in items],
            total=total,
            page=page_params.page,
            page_size=page_params.page_size,
            total_pages=(total + page_params.page_size - 1) // page_params.page_size
            if total
            else 0,
        )

    def get_product(self, product_id: str) -> Optional[ProductDetailOut]:
        product = self.repository.get(product_id)
        if product is None:
            return None
        return ProductDetailOut.model_validate(product)

    def get_merchant_listings(
        self, *, product_id: str
    ) -> Sequence[MerchantListingOut]:
        listings = self.repository.list_merchant_listings(product_id=product_id)
        return [MerchantListingOut.model_validate(item) for item in listings]

    def get_similar_products(
        self, *, product_id: str, limit: int = 6
    ) -> Sequence[SimilarProductOut]:
        products = self.repository.find_similar(product_id=product_id, limit=limit)
        return [
            SimilarProductOut(
                id=p.id,
                name=p.name,
                brand=p.brand,
                category=p.category,
                image_references=p.image_references,
                min_price=self._min_price(p),
                currency="INR",
                reason=None,
            )
            for p in products
        ]

    def _to_list_item(self, product) -> ProductListItemOut:
        return ProductListItemOut(
            id=product.id,
            name=product.name,
            brand=product.brand,
            description=product.description,
            category=product.category,
            subcategory=product.subcategory,
            gender_audience=product.gender_audience,
            style_tags=product.style_tags,
            occasion_tags=product.occasion_tags,
            image_references=product.image_references,
            min_price=self._min_price(product),
            currency="INR",
            created_at=product.created_at,
        )

    @staticmethod
    def _min_price(product) -> Optional[float]:
        listings = product.merchant_listings or []
        if not listings:
            return None
        return min(l.current_price for l in listings)
