"""API v1 router registry."""

from fastapi import APIRouter

from civicbrain.api.v1.auth import router as auth_router
from civicbrain.api.v1.causal import router as causal_router
from civicbrain.api.v1.gis import router as gis_router
from civicbrain.api.v1.health import router as health_router
from civicbrain.api.v1.hierarchy import router as hierarchy_router
from civicbrain.api.v1.incidents import router as incidents_router
from civicbrain.api.v1.intake import router as intake_router
from civicbrain.api.v1.nlp import router as nlp_router
from civicbrain.api.v1.prioritization import router as prioritization_router
from civicbrain.api.v1.taxonomy import router as taxonomy_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router, prefix="", tags=["Health & Diagnostics"])
api_v1_router.include_router(auth_router, prefix="", tags=["Authentication & Identity"])
api_v1_router.include_router(hierarchy_router, prefix="", tags=["Hierarchy & Administration"])
api_v1_router.include_router(intake_router, prefix="", tags=["Intake"])
api_v1_router.include_router(incidents_router, prefix="", tags=["Incidents"])
api_v1_router.include_router(taxonomy_router, prefix="", tags=["Taxonomy & Governance"])
api_v1_router.include_router(gis_router, prefix="/gis", tags=["GIS & Spatial Analysis"])
api_v1_router.include_router(nlp_router, prefix="/nlp", tags=["NLP & Multilingual Pipeline"])
api_v1_router.include_router(
    prioritization_router, prefix="/prioritization", tags=["Prioritization & Equity Engine"]
)
api_v1_router.include_router(
    causal_router, prefix="/causal", tags=["Causal Root-Cause Linking & Centrality"]
)
