"""Product provider abstraction.

Defines the interface for product catalogue providers. Future retailer
integrations (Flipkart Affiliate API, Amazon Creators API, etc.) implement
this interface. A sample database-backed provider is provided for development
and works independently of any external API availability.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductFilters


class ProductProvider(ABC):
    """Abstract product catalogue provider."""

    @abstractmethod
    def list_products(
        self,
        *,
        filters: ProductFilters,
        page: int,
        page_size: int,
    ) -> tuple[List[Product], int]:
        """Return a paginated, filtered list of products and the total count."""
        raise NotImplementedError

    @abstractmethod
    def get_product(self, product_id: str) -> Optional[Product]:
        """Return a single product by ID, or None if not found."""
        raise NotImplementedError

    @abstractmethod
    def find_similar(
        self, *, product_id: str, limit: int = 6
    ) -> List[Product]:
        """Return products similar to the given product."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name (for logging/metrics)."""
        raise NotImplementedError


class SampleCatalogueProvider(ProductProvider):
    """Development provider backed by the local PostgreSQL sample catalogue.

    This provider is independent of external retailer APIs. All data is
    clearly identified as sample/development data and must never be
    represented as verified live retailer inventory.
    """

    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    @property
    def name(self) -> str:
        return "sample_catalogue"

    def list_products(
        self,
        *,
        filters: ProductFilters,
        page: int,
        page_size: int,
    ) -> tuple[List[Product], int]:
        items, total = self._repository.list(
            filters=filters, page=page, page_size=page_size
        )
        return items, total

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._repository.get(product_id)

    def find_similar(
        self, *, product_id: str, limit: int = 6
    ) -> List[Product]:
        return list(self._repository.find_similar(product_id=product_id, limit=limit))


def get_product_provider(repository: ProductRepository) -> ProductProvider:
    """Factory returning the active product provider.

    Currently returns the sample catalogue provider. Future phases can select
    between providers based on configuration without changing service code.
    """
    return SampleCatalogueProvider(repository)
