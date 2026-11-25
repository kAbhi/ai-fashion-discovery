from fastapi import APIRouter

# Versioned business endpoints (search, products, ...) are registered here from Phase 1.
api_router = APIRouter(prefix="/api/v1")
