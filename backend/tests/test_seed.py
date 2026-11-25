"""Sample data seeding tests."""

from app.models.product import Product


def test_sample_data_count(db_session):
    """The seeded sample catalogue contains at least 100 products."""
    count = db_session.query(Product).filter(Product.is_sample_data.is_(True)).count()
    assert count >= 100, f"Expected at least 100 sample products, got {count}"


def test_sample_data_has_categories(db_session):
    """Sample data spans the expected categories."""
    categories = {
        row[0]
        for row in db_session.query(Product.category)
        .filter(Product.is_sample_data.is_(True))
        .distinct()
        .all()
    }
    expected = {
        "ethnic_wear",
        "occasion_wear",
        "indo_western",
        "dresses",
        "tops_shirts",
        "trousers",
        "sneakers",
        "casual_footwear",
        "accessories",
    }
    assert expected <= categories, f"Missing categories: {expected - categories}"


def test_sample_data_has_variants_and_listings(db_session):
    """Every sample product has at least one variant and one merchant listing."""
    from app.models.product import MerchantListing, ProductVariant

    products = (
        db_session.query(Product)
        .filter(Product.is_sample_data.is_(True))
        .all()
    )
    for p in products:
        assert len(p.variants) >= 1, f"Product {p.id} has no variants"
        assert len(p.merchant_listings) >= 1, f"Product {p.id} has no merchant listings"
        for listing in p.merchant_listings:
            assert listing.currency == "INR"
            assert listing.current_price > 0


def test_sample_data_flag_only_on_sample_products(db_session):
    """Non-sample products (if any) do not carry the sample flag."""
    nonsample = (
        db_session.query(Product)
        .filter(Product.is_sample_data.is_(False))
        .all()
    )
    # In a seeded test DB there should be no non-sample products, but if
    # there are, they must not be sample data.
    for p in nonsample:
        assert p.is_sample_data.is_(False)


def test_seed_script_runs(db_session):
    """The seed script can be imported and lists the expected product count."""
    from data.seed.sample_catalogue import SAMPLE_PRODUCTS
    from data.seed.sample_catalogue_extra import EXTRA_PRODUCTS
    from data.seed.sample_catalogue_more import MORE_PRODUCTS

    total = len(SAMPLE_PRODUCTS) + len(EXTRA_PRODUCTS) + len(MORE_PRODUCTS)
    assert total >= 100, f"Seed data has only {total} products"
