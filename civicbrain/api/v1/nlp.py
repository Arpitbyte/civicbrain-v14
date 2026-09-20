"""NLP Pipeline and Multilingual Ingestion REST Endpoints (§A11)."""

import logging

from fastapi import APIRouter, Depends, status

from civicbrain.domain.identity.jwt import (
    CurrentUserClaims,
    get_current_user_claims,
)
from civicbrain.domain.nlp.processor import (
    DeterministicIndicRuleProcessor,
    NLPProcessor,
)
from civicbrain.schemas.nlp import TextAnalysisRequest, TextAnalysisResponse

logger = logging.getLogger("civicbrain.nlp")

router = APIRouter(tags=["NLP & Multilingual Pipeline"])

# Singleton instance of CPU-efficient rule processor
_processor: NLPProcessor = DeterministicIndicRuleProcessor()


@router.post(
    "/analyze",
    response_model=TextAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze citizen grievance text (Authenticated)",
)
async def analyze_text(
    payload: TextAnalysisRequest,
    claims: CurrentUserClaims = Depends(get_current_user_claims),
) -> TextAnalysisResponse:
    """Analyze multilingual civic text.

    Authenticated-only endpoint (requires valid Supabase JWT).
    Decouples citizen emotional urgency from physical engineering severity (§A11).
    """
    result = _processor.process_text(
        text=payload.text,
        citizen_category=payload.citizen_category,
    )
    return TextAnalysisResponse.model_validate(result)
