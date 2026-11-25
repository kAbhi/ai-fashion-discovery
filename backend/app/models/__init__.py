"""ORM models. Import every model module here so Alembic autogenerate can discover it."""

from app.models import product  # noqa: F401  (registers Product, ProductVariant, MerchantListing)
from app.models import session  # noqa: F401  (registers session/interaction models)

__all__ = ["product", "session"]
