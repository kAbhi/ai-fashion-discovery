import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

# Tests never touch the developer's main database. Override with TEST_DATABASE_URL.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery_test",
)
os.environ["ENVIRONMENT"] = "test"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from app.core.config import get_settings  # noqa: E402
from app.db.session import get_engine  # noqa: E402
from app.main import create_app  # noqa: E402

get_settings.cache_clear()


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_app()) as test_client:
        yield test_client


def database_available() -> bool:
    try:
        with get_engine().connect():
            return True
    except Exception:
        return False
