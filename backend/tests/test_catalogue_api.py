"""Catalogue API tests."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.schemas.product import ProductFilters
from app.repositories.product_repository import ProductRepository


def _seed_test_db(db_session):
    """Seed the test database with a minimal set of products for API tests."""
    from app.models.product import MerchantListing, Product, ProductVariant

    products = [
        Product(
            name="Test Cotton Kurta",
            brand="TestBrand",
            description="A comfortable cotton kurta",
            category="ethnic_wear",
            subcategory="kurta",
            gender_audience="women",
            style_tags=["casual", "traditional"],
            occasion_tags=["casual", "office"],
            image_references=["https://example.com/kurta.jpg"],
            is_sample_data=True,
        ),
        Product(
            name="Test Running Sneakers",
            brand="SportBrand",
            description="Lightweight running shoes",
            category="sneakers",
            subcategory="running",
            gender_audience="unisex",
            style_tags=["sporty", "casual"],
            occasion_tags=["travel", "fitness"],
            image_references=["https://example.com/sneakers.jpg"],
            is_sample_data=True,
        ),
        Product(
            name="Test Formal Suit",
            brand="FormalBrand",
            description="Business suit for office",
            category="occasion_wear",
            subcategory="suit",
            gender_audience="men",
            style_tags=["formal", "business"],
            occasion_tags=["office", "wedding"],
            image_references=["https://example.com/suit.jpg"],
            is_sample_data=True,
        ),
    ]
    for p in products:
        db_session.add(p)
        db_session.flush()
        db_session.add(
            ProductVariant(
                product_id=p.id, size="M", colour="Blue",
                variant_attributes={"material": "cotton"},
            )
        )
        db_session.add(
            MerchantListing(
                product_id=p.id,
                merchant="TestMerchant",
                current_price=1999.0,
                currency="INR",
                availability="in_stock",
                is_sample_data=True,
            )
        )
    db_session.flush()
    return products


def test_list_products(client: TestClient, db_session):
    products = _seed_test_db(db_session)
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "total" in body
    assert "page" in body
    assert "page_size" in body
    assert "total_pages" in body
    assert body["total"] == len(products)
    assert len(body["items"]) == len(products)
    for item in body["items"]:
        assert "id" in item
        assert "name" in item
        assert "brand" in item
        assert "category" in item


def test_get_product_detail(client: TestClient, db_session):
    products = _seed_test_db(db_session)
    product_id = str(products[0].id)
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == product_id
    assert body["name"] == "Test Cotton Kurta"
    assert body["brand"] == "TestBrand"
    assert "variants" in body
    assert "merchant_listings" in body


def test_get_product_not_found(client: TestClient, db_session):
    response = client.get(f"/api/v1/products/{uuid4()}")
    assert response.status_code == 404


def test_get_similar_products(client: TestClient, db_session):
    products = _seed_test_db(db_session)
    product_id = str(products[0].id)
    response = client.get(f"/api/v1/products/{product_id}/similar")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    ids = {item["id"] for item in body}
    assert str(product_id) not in ids


def test_get_similar_products_not_found(client: TestClient, db_session):
    response = client.get(f"/api/v1/products/{uuid4()}/similar")
    assert response.status_code == 404


def test_get_merchant_listings(client: TestClient, db_session):
    products = _seed_test_db(db_session)
    product_id = str(products[0].id)
    response = client.get(
        "/api/v1/merchant-listings", params={"product_id": product_id}
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["merchant"] == "TestMerchant"
    assert body[0]["current_price"] == 1999.0
    assert body[0]["currency"] == "INR"


def test_repository_direct_query(db_session):
    """Verify the repository layer works independently of the API."""
    repo = ProductRepository(db_session)
    products, total = repo.list(filters=ProductFilters(), page=1, page_size=10)
    assert total >= 0
    assert isinstance(products, list)
