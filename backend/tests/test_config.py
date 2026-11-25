import pytest

from app.core.config import Settings


@pytest.mark.parametrize(
    "raw",
    [
        "postgres://u:p@h:5432/db",
        "postgresql://u:p@h:5432/db",
        "postgresql+psycopg://u:p@h:5432/db",
    ],
)
def test_database_url_is_normalised_to_psycopg(raw: str) -> None:
    settings = Settings(database_url=raw)
    assert settings.database_url == "postgresql+psycopg://u:p@h:5432/db"


def test_cors_origins_parsed_from_comma_separated_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000, https://app.vercel.app")
    settings = Settings(database_url="postgresql://u:p@h/db")
    assert settings.cors_origins == ["http://localhost:3000", "https://app.vercel.app"]
