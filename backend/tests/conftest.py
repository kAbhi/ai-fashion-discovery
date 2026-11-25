import os
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

# Ensure the repository root (parent of backend/) is on sys.path so tests
# can import from data.seed (sample catalogue data lives outside backend/).
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Tests never touch the developer's main database. Override with TEST_DATABASE_URL.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery_test",
)
os.environ["ENVIRONMENT"] = "test"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from app.core.config import get_settings  # noqa: E402
from app.db.base import Base  # noqa: E402
from app.db.session import get_db, get_engine  # noqa: E402
from app.main import create_app  # noqa: E402

get_settings.cache_clear()

_TEST_SESSION_MAKER: sessionmaker[Session] | None = None


@pytest.fixture(autouse=True)
def _ensure_test_schema():
    """Ensure the test database schema is up to date before each test."""
    global _TEST_SESSION_MAKER
    engine = get_engine()
    Base.metadata.create_all(engine)
    _TEST_SESSION_MAKER = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    yield


@pytest.fixture
def db_session() -> Iterator[Session]:
    """Provide a transaction-scoped session that rolls back after each test."""
    if _TEST_SESSION_MAKER is None:
        pytest.skip("Database not available")
    session = _TEST_SESSION_MAKER()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    """TestClient that uses the same db_session for dependency injection."""

    def override_get_db() -> Iterator[Session]:
        try:
            yield db_session
        finally:
            pass  # Session is managed by the db_session fixture

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def database_available() -> bool:
    try:
        with get_engine().connect():
            return True
    except Exception:
        return False
