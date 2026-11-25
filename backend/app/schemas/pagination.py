"""Generic pagination schemas used across catalogue and discovery endpoints."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageParams(BaseModel):
    """Query parameters for paginated list endpoints."""

    page: int = Field(default=1, ge=1, description="1-based page number")
    page_size: int = Field(
        default=24, ge=1, le=100, description="Items per page (max 100)"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated envelope."""

    items: List[T]
    total: int = Field(description="Total number of items matching the filters")
    page: int = Field(description="Current -based page number")
    page_size: int = Field(description="Items per page")
    total_pages: int = Field(description="Total number of pages")

    @classmethod
    def create(
        cls,
        items: List[T],
        *,
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        total_pages = (total + page_size - 1) // page_size if total else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
