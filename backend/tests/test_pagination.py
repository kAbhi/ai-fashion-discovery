"""Pagination tests for the catalogue API."""

from fastapi.testclient import TestClient


def _seed_many_products(db_session, count: int = 25):
    from app.models.product import MerchantListing, Product, ProductVariant

    for i in range(count):
        p = Product(
            name=f"Product {i:03d}",
            brand="BatchBrand",
            category="tops_shirts",
            gender_audience="unisex",
            is_sample_data=True,
        )
        db_session.add(p)
        db_session.flush()
        db_session.add(ProductVariant(product_id=p.id, size="M", colour="Blue"))
        db_session.add(
            MerchantListing(
                product_id=p.id,
                merchant="TestMerchant",
                current_price=1000.0 + i,
                currency="INR",
                availability="in_stock",
                is_sample_data=True,
            )
        )
    db_session.flush()


def test_default_page_size(client: TestClient, db_session):
    _seed_many_products(db_session, count=25)
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    body = response.json()
    assert body["page_size"] == 24
    assert body["total"] == 25
    assert len(body["items"]) == 24
    assert body["total_pages"] == 2


def test_second_page(client: TestClient, db_session):
    _seed_many_products(db_session, count=25)
    response = client.get("/api/v1/products", params={"page": 2, "page_size": 24})
    assert response.status_code == 200
    body = response.json()
    assert body["page"] == 2
    assert len(body["items"]) == 1  # 25 - 24 = 1 remaining


def test_custom_page_size(client: TestClient, db_session):
    _seed_many_products(db_session, count=10)
    response = client.get("/api/v1/products", params={"page_size": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["page_size"] == 5
    assert len(body["items"]) == 5
    assert body["total_pages"] == 2


def test_page_beyond_range(client: TestClient, db_session):
    _seed_many_products(db_session, count=5)
    response = client.get("/api/v1/products", params={"page": 5, "page_size": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total"] == 5


def test_pagination_with_filter(client: TestClient, db_session):
    _seed_many_products(db_session, count=10)
    response = client.get(
        "/api/v1/products", params={"brand": "BatchBrand", "page_size": 3}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 10
    assert len(body["items"]) == 3
    assert all(item["brand"] == "BatchBrand" for item in body["items"])
