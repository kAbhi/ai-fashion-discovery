"""Invalid request tests for the catalogue API."""

from uuid import uuid4

from fastapi.testclient import TestClient


def test_invalid_uuid_format(client: TestClient, db_session):
    response = client.get("/api/v1/products/not-a-uuid")
    assert response.status_code == 422


def test_negative_page(client: TestClient, db_session):
    response = client.get("/api/v1/products", params={"page": 0})
    assert response.status_code == 422


def test_page_size_above_max(client: TestClient, db_session):
    response = client.get("/api/v1/products", params={"page_size": 101})
    assert response.status_code == 422


def test_negative_price(client: TestClient, db_session):
    response = client.get("/api/v1/products", params={"min_price": -1})
    assert response.status_code == 422


def test_empty_database_returns_zero(client: TestClient, db_session):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_similar_products_invalid_uuid(client: TestClient, db_session):
    response = client.get("/api/v1/products/not-a-uuid/similar")
    assert response.status_code == 422


def test_merchant_listings_missing_product_id(client: TestClient, db_session):
    response = client.get("/api/v1/merchant-listings")
    assert response.status_code == 422


def test_merchant_listings_for_nonexistent_product(client: TestClient, db_session):
    response = client.get(
        "/api/v1/merchant-listings", params={"product_id": str(uuid4())}
    )
    assert response.status_code == 200
    assert response.json() == []
