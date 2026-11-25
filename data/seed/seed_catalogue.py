"""Seed the development database with the sample product catalogue.

Usage:
    cd backend
    source .venv/bin/activate
    export DATABASE_URL=postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery
    python -m data.seed.seed_catalogue

All data is clearly identified as development/sample data.
"""

import sys
from pathlib import Path

# Allow running from backend/ as a module or as a script.
BACKEND_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import select

from app.core.config import get_settings
from app.db.session import get_sessionmaker
from app.models.product import MerchantListing, Product, ProductVariant
from data.seed.sample_catalogue import SAMPLE_PRODUCTS
from data.seed.sample_catalogue_extra import EXTRA_PRODUCTS
from data.seed.sample_catalogue_more import MORE_PRODUCTS

ALL_PRODUCTS = SAMPLE_PRODUCTS + EXTRA_PRODUCTS + MORE_PRODUCTS


def seed(clear_first: bool = True) -> None:
    settings = get_settings()
    session_factory = get_sessionmaker()
    session = session_factory()
    try:
        if clear_first:
            # Delete in dependency order.
            session.execute(select(MerchantListing)).scalars().all()
            for row in session.execute(select(MerchantListing)).scalars():
                session.delete(row)
            for row in session.execute(select(ProductVariant)).scalars():
                session.delete(row)
            session.execute(select(Product)).scalars().all()
            for row in session.execute(select(Product)).scalars():
                session.delete(row)
            session.commit()
            print("Cleared existing sample products.")

        count = 0
        for data in ALL_PRODUCTS:
            product = Product(
                name=data["name"],
                brand=data["brand"],
                description=data.get("description"),
                category=data["category"],
                subcategory=data.get("subcategory"),
                gender_audience=data.get("gender_audience"),
                style_tags=data.get("style_tags"),
                occasion_tags=data.get("occasion_tags"),
                image_references=data.get("image_references"),
            )
            session.add(product)
            session.flush()  # assign product.id before variants/listings

            for v in data.get("variants", []):
                session.add(
                    ProductVariant(
                        product_id=product.id,
                        size=v.get("size"),
                        colour=v.get("colour"),
                        variant_attributes=v.get("attributes"),
                    )
                )

            for m in data.get("merchant_listings", []):
                session.add(
                    MerchantListing(
                        product_id=product.id,
                        merchant=m["merchant"],
                        current_price=m["current_price"],
                        original_price=m.get("original_price"),
                        currency=m.get("currency", "INR"),
                        availability=m.get("availability"),
                    )
                )
            count += 1

        session.commit()
        print(f"Seeded {count} sample products into {settings.database_url.split('@')[-1]}")
    finally:
        session.close()


if __name__ == "__main__":
    clear = "--no-clear" not in sys.argv
    seed(clear_first=clear)
