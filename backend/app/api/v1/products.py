"""Product catalogue REST endpoints.

Route handlers are thin: all database access is in the repository layer and
all business logic is in the service layer.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.integrations.product_provider import get_product_provider
from app.repositories.product_repository import ProductRepository
from app.schemas.pagination import PageParams
from app.schemas.product import (
    MerchantListingSummary,
    ProductDetailOut,
    ProductFilters,
    ProductListItemOut,
    PaginatedProductOut,
    SimilarProductOut,
)
from app.services.catalogue_service import CatalogueService

router = APIRouter(tags=["products"])


def get_repository(db: Annotated[Session, Depends(get_db)]) -> ProductRepository:
    return ProductRepository(db)


def get_service(
    repo: Annotated[ProductRepository, Depends(get_repository)],
) -> CatalogueService:
    return CatalogueService(repo)


def get_provider(
    repo: Annotated[ProductRepository, Depends(get_repository)],
):
    return get_product_provider(repo)


@router.get(
    "/products",
    response_model=PaginatedProductOut,
    summary="List products with optional filtering and pagination",
)
def list_products(
    service: Annotated[CatalogueService, Depends(get_service)],
    # Filters
    category: Optional[str] = Query(default=None),
    subcategory: Optional[str] = Query(default=None),
    brand: Optional[str] = Query(default=None),
    gender: Optional[str] = Query(default=None),
    occasion: Optional[str] = Query(default=None),
    style: Optional[str] = Query(default=None),
    colour: Optional[str] = Query(default=None),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    q: Optional[str] = Query(default=None),
    # Pagination
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=1, le=100),
) -> PaginatedProductOut:
    filters = ProductFilters(
        category=category,
        subcategory=subcategory,
        brand=brand,
        gender=gender,
        occasion=occasion,
        style=style,
        colour=colour,
        min_price=min_price,
        max_price=max_price,
        q=q,
    )
    page_params = PageParams(page=page, page_size=page_size)
    return service.list_products(filters=filters, page_params=page_params)


@router.get(
    "/products/{product_id}",
    response_model=ProductDetailOut,
    summary="Get a single product with variants and merchant listings",
)
def get_product(
    product_id: str,
    service: Annotated[CatalogueService, Depends(get_service)],
) -> ProductDetailOut:
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get(
    "/products/{product_id}/similar",
    response_model=list[SimilarProductOut],
    summary="Get products similar to the given product",
)
def get_similar_products(
    product_id: str,
    service: Annotated[CatalogueService, Depends(get_service)],
    limit: int = Query(default=6, ge=1, le=24),
) -> list[SimilarProductOut]:
    # Verify the product exists before returning similar items.
    if service.get_product(product_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return service.get_similar_products(product_id=product_id, limit=limit)


@router.get(
    "/merchant-listings",
    response_model=list[MerchantListingSummary],
    summary="Get merchant listings for a product",
)
def get_merchant_listings(
    product_id: Annotated[str, Query(description="Product ID")],
    service: Annotated[CatalogueService, Depends(get_service)],
) -> list[MerchantListingSummary]:
    listings = service.get_merchant_listings(product_id=product_id)
    return [
        MerchantListingSummary(
            id=l.id,
            product_id=l.product_id,
            merchant=l.merchant,
            current_price=l.current_price,
            currency=l.currency,
            availability=l.availability,
        )
        for l in listings
    ]
