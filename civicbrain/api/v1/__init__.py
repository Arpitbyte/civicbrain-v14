"""API v1 router registry."""

from fastapi import APIRouter

from civicbrain.api.v1.auth import router as auth_router
from civicbrain.api.v1.health import router as health_router
from civicbrain.api.v1.hierarchy import router as hierarchy_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, prefix="", tags=["Health & Diagnostics"])
api_v1_router.include_router(auth_router, prefix="", tags=["Authentication & Identity"])
api_v1_router.include_router(hierarchy_router, prefix="", tags=["Hierarchy & Administration"])
