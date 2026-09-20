"""Authentication and user session endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from civicbrain.domain.identity.jwt import CurrentUserClaims, get_current_user_claims
from civicbrain.domain.identity.services import resolve_user_profile
from civicbrain.infra.database import get_db
from civicbrain.schemas.identity import AuthMeResponse

router = APIRouter(prefix="/auth", tags=["Authentication & Identity"])


@router.get(
    "/me",
    response_model=AuthMeResponse,
    summary="Get current authenticated user profile and scopes",
)
async def get_my_profile(
    claims: CurrentUserClaims = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> AuthMeResponse:
    """Returns the authenticated identity, role assignments, and jurisdictional scopes (tenant, department, zone, ward)."""
    try:
        profile = await resolve_user_profile(db, claims.user_id)
        # Augment with JWT claims if not present in DB
        if claims.org_id and not profile.organization_id:
            profile.organization_id = claims.org_id
        if claims.role and claims.role not in profile.roles:
            profile.roles.append(claims.role)
        if claims.department_ids and not profile.department_ids:
            profile.department_ids = claims.department_ids
        if claims.zone_ids and not profile.zone_ids:
            profile.zone_ids = claims.zone_ids
        if claims.ward_id and not profile.ward_id:
            profile.ward_id = claims.ward_id
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resolve user profile: {e}",
        ) from e
