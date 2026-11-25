import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import check_database, get_db
from app.schemas.health import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    """Liveness + database connectivity check (used by Render health checks)."""
    try:
        check_database(db)
    except SQLAlchemyError:
        # Log the detail server-side only; never leak connection info to clients.
        logger.exception("Database health check failed")
    else:
        return HealthResponse(status="ok", environment=settings.environment, database="ok")

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(
        status="degraded", environment=settings.environment, database="unavailable"
    )
