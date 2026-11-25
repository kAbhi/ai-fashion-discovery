"""Database model tests for the product catalogue."""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select

from app.models.product import MerchantListing, Product, ProductVariant
from app.models.session import (
    ProductComparison,
    ProductInteraction,
    ShoppingSession,
    UserPreference,
    WishlistItem,
)


def test_product_creation(db_session):
    product = Product(
        name="Test Kurta",
        brand="TestBrand",
        description="A test kurta",
        category="ethnic_wear",
        subcategory="kurta",
        gender_audience="women",
        style_tags=["casual", "traditional"],
        occasion_tags=["casual", "office"],
        image_references=["https://example.com/img.jpg"],
        is_sample_data=True,
    )
    db_session.add(product)
    db_session.flush()

    assert product.id is not None
    assert isinstance(product.created_at, datetime)
    assert product.created_at.tzinfo is not None


def test_product_variant_and_merchant_listing(db_session):
    product = Product(
        name="Test Product",
        brand="TestBrand",
        category="sneakers",
        gender_audience="unisex",
        is_sample_data=True,
    )
    db_session.add(product)
    db_session.flush()

    variant = ProductVariant(
        product_id=product.id,
        size="9",
        colour="White",
        variant_attributes={"material": "canvas"},
    )
    listing = MerchantListing(
        product_id=product.id,
        merchant="TestMerchant",
        current_price=2999.0,
        currency="INR",
        availability="in_stock",
        is_sample_data=True,
    )
    db_session.add_all([variant, listing])
    db_session.flush()

    assert variant.id is not None
    assert listing.id is not None

    # Verify relationships loaded back
    stmt = select(Product).where(Product.id == product.id)
    fetched = db_session.execute(stmt).scalar_one()
    assert len(fetched.variants) == 1
    assert fetched.variants[0].size == "9"
    assert len(fetched.merchant_listings) == 1
    assert fetched.merchant_listings[0].merchant == "TestMerchant"


def test_shopping_session_and_interactions(db_session):
    session = ShoppingSession()
    db_session.add(session)
    db_session.flush()

    product = Product(
        name="Interaction Product",
        brand="Brand",
        category="dresses",
        is_sample_data=True,
    )
    db_session.add(product)
    db_session.flush()

    interaction = ProductInteraction(
        session_id=session.id,
        product_id=product.id,
        interaction_type="like",
    )
    db_session.add(interaction)
    db_session.flush()

    assert interaction.id is not None
    assert len(session.interactions) == 1
    assert session.interactions[0].interaction_type == "like"


def test_wishlist_and_preference(db_session):
    session = ShoppingSession()
    db_session.add(session)
    db_session.flush()

    product = Product(
        name="Wishlist Product",
        brand="Brand",
        category="accessories",
        is_sample_data=True,
    )
    db_session.add(product)
    db_session.flush()

    wishlist = WishlistItem(session_id=session.id, product_id=product.id)
    preference = UserPreference(
        session_id=session.id,
        preference_type="brand",
        preference_value="Biba",
    )
    db_session.add_all([wishlist, preference])
    db_session.flush()

    assert wishlist.id is not None
    assert preference.id is not None
    assert len(session.wishlist_items) == 1
    assert len(session.preferences) == 1


def test_product_comparison(db_session):
    session = ShoppingSession()
    db_session.add(session)
    db_session.flush()

    comparison = ProductComparison(
        session_id=session.id,
        product_ids=[uuid4(), uuid4()],
    )
    db_session.add(comparison)
    db_session.flush()

    assert comparison.id is not None
    assert len(comparison.product_ids) == 2


def test_unique_wishlist_per_session_product(db_session):
    session = ShoppingSession()
    db_session.add(session)
    db_session.flush()

    product = Product(
        name="Dup Product",
        brand="Brand",
        category="sneakers",
        is_sample_data=True,
    )
    db_session.add(product)
    db_session.flush()

    db_session.add_all(
        [
            WishlistItem(session_id=session.id, product_id=product.id),
            WishlistItem(session_id=session.id, product_id=product.id),
        ]
    )
    from sqlalchemy.exc import IntegrityError

    try:
        db_session.commit()
        assert False, "Expected IntegrityError for duplicate wishlist item"
    except IntegrityError:
        db_session.rollback()
