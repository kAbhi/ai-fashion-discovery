"""Filtering tests for the catalogue API."""

from fastapi.testclient import TestClient


def _seed_filter_products(db_session):
    from app.models.product import MerchantListing, Product, ProductVariant

    products = [
        Product(
            name="Red Cotton Kurta",
            brand="Biba",
            category="ethnic_wear",
            gender_audience="women",
            style_tags=["traditional", "casual"],
            occasion_tags=["festive", "casual"],
            image_references=["https://example.com/red-kurta.jpg"],
            is_sample_data=True,
        ),
        Product(
            name="Blue Formal Shirt",
            brand="Peter England",
            category="tops_shirts",
            gender_audience="men",
            style_tags=["formal", "business"],
            occasion_tags=["office", "formal"],
            image_references=["https://example.com/blue-shirt.jpg"],
            is_sample_data=True,
        ),
        Product(
            name="Green Sneakers",
            brand="Nike",
            category="sneakers",
            gender_audience="unisex",
            style_tags=["sporty", "casual"],
            occasion_tags=["fitness", "travel"],
            image_references=["https://example.com/green-sneakers.jpg"],
            is_sample_data=True,
        ),
    ]
    for p in products:
        db_session.add(p)
        db_session.flush()
        db_session.add(ProductVariant(product_id=p.id, size="M", colour="Blue"))
        db_session.add(
            MerchantListing(
                product_id=p.id,
                merchant="TestMerchant",
                current_price=1999.0 if "Kurta" in p.name else 2999.0,
                currency="INR",
                availability="in_stock",
                is_sample_data=True,
            )
        )
    db_session.flush()
    return products


def test_filter_by_category(client: TestClient, db_session):
    _seed_filter_products(db_session)
    response = client.get("/api/v1/products", params={"category": "sneakers"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["category"] == "sneakers"


def test_filter_by_brand(client: TestClient, db_session):
    _seed_filter_products(db_session)
    response = client.get("/api/v1/products", params={"brand": "Biba"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["brand"] == "Biba"


def test_filter_by_occasion(client: TestClient, db_session):
    _seed_filter_products(db_session)
    response = client.get("/api/v1/products", params={"occasion": "office"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert "office" in body["items"][0]["occasion_tags"]


def test_filter_by_style(client: TestClient, db_session):
    _seed_filter_products(db_session)
    response = client.get("/api/v1/products", params={"style": "formal"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert "formal" in body["items"][0]["style_tags"]


def test_filter_by_multiple(client: TestClient, db_session):
    _seed_filter_products(db_session)
    response = client.get(
        "/api/v1/products",
        params={"category": "ethnic_wear", "brand": "Biba"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["name"] == "Red Cotton Kurta"


def test_filter_no_results(client: TestClient, db_session):
    _seed_filter_products(db_session)
    response = client.get("/api/v1/products", params={"category": "nonexistent"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []
