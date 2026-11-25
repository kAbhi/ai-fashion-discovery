"""Migration tests: verify Alembic can bring the schema to head from scratch."""

import subprocess
import sys

import pytest
from sqlalchemy import inspect, text

from app.db.base import Base
from app.db.session import get_engine


@pytest.mark.db
def test_all_model_tables_exist(db_session):
    """All tables defined in SQLAlchemy models exist in the database."""
    inspector = inspect(get_engine())
    table_names = set(inspector.get_table_names())
    expected = {
        "products",
        "product_variants",
        "merchant_listings",
        "shopping_sessions",
        "product_interactions",
        "user_preferences",
        "wishlist_items",
        "product_comparisons",
    }
    missing = expected - table_names
    assert not missing, f"Missing tables: {missing}"


@pytest.mark.db
def test_alembic_version_table_exists(db_session):
    """The alembic_version table exists (migrations have been run)."""
    inspector = inspect(get_engine())
    assert "alembic_version" in inspector.get_table_names()


@pytest.mark.db
def test_product_has_required_columns(db_session):
    """Products table has the columns expected by the catalogue API."""
    inspector = inspect(get_engine())
    columns = {col["name"] for col in inspector.get_columns("products")}
    required = {
        "id", "name", "brand", "category", "subcategory", "gender_audience",
        "style_tags", "occasion_tags", "image_references", "is_sample_data",
        "created_at", "updated_at",
    }
    assert required <= columns, f"Missing columns: {required - columns}"


def test_alembic_upgrade_head_runs():
    """`alembic upgrade head` succeeds against the configured database."""
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
        cwd=str(__import__("pathlib").Path(__file__).resolve().parents[1]),
    )
    assert result.returncode == 0, result.stderr
