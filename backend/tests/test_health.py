from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.main import create_app
from tests.conftest import database_available


@pytest.mark.db
@pytest.mark.skipif(not database_available(), reason="PostgreSQL test database not reachable")
def test_health_ok_with_real_database(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "test", "database": "ok"}


class _BrokenSession:
    def execute(self, *_args: object, **_kwargs: object) -> None:
        raise OperationalError("SELECT 1", {}, Exception("connection refused"))


def test_health_reports_degraded_when_database_unavailable() -> None:
    app = create_app()

    def broken_db() -> Iterator[Session]:
        yield _BrokenSession()  # type: ignore[misc]

    app.dependency_overrides[get_db] = broken_db
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body == {"status": "degraded", "environment": "test", "database": "unavailable"}
    # No internal error details leak to the client.
    assert "connection refused" not in response.text


def test_cors_allows_configured_origin_only(client: TestClient) -> None:
    allowed = client.options(
        "/health",
        headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
    )
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:3000"

    denied = client.options(
        "/health",
        headers={"Origin": "https://evil.example.com", "Access-Control-Request-Method": "GET"},
    )
    assert "access-control-allow-origin" not in denied.headers


def test_cors_origin_regex_allows_matching_preview_origins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CORS_ORIGIN_REGEX", r"https://fashion-discovery-[a-z0-9-]+\.vercel\.app")
    get_settings.cache_clear()
    try:
        with TestClient(create_app()) as client:
            preview = "https://fashion-discovery-git-feature-abc.vercel.app"
            ok = client.options(
                "/health", headers={"Origin": preview, "Access-Control-Request-Method": "GET"}
            )
            assert ok.headers.get("access-control-allow-origin") == preview

            other = client.options(
                "/health",
                headers={
                    "Origin": "https://attacker.vercel.app",
                    "Access-Control-Request-Method": "GET",
                },
            )
            assert "access-control-allow-origin" not in other.headers
    finally:
        monkeypatch.delenv("CORS_ORIGIN_REGEX")
        get_settings.cache_clear()
