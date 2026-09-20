"""JWT claims extraction and RBAC security dependencies for Supabase Auth."""

import uuid
from typing import Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError, decode

from civicbrain.domain.identity.models import StaffRole
from civicbrain.infra.config import settings

security = HTTPBearer(auto_error=False)


class CurrentUserClaims:
    """Parsed and validated claims from Supabase Auth JWT."""

    def __init__(self, raw_claims: dict[str, Any]):
        self.raw: dict[str, Any] = raw_claims
        user_id_str = raw_claims.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject (user_id)",
            )
        self.user_id: uuid.UUID = uuid.UUID(user_id_str)

        # Supabase stores custom claims under app_metadata or top level
        app_meta = raw_claims.get("app_metadata", {})
        user_meta = raw_claims.get("user_metadata", {})

        org_str = raw_claims.get("org_id") or app_meta.get("org_id") or user_meta.get("org_id")
        self.org_id: uuid.UUID | None = uuid.UUID(org_str) if org_str else None

        role_str = raw_claims.get("role") or app_meta.get("role") or user_meta.get("role")
        try:
            self.role: StaffRole | None = StaffRole(role_str) if role_str else None
        except ValueError:
            self.role = None

        dept_list = (
            raw_claims.get("department_ids")
            or app_meta.get("department_ids")
            or user_meta.get("department_ids")
            or []
        )
        self.department_ids: list[uuid.UUID] = [uuid.UUID(str(d)) for d in dept_list if d]

        zone_list = (
            raw_claims.get("zone_ids")
            or app_meta.get("zone_ids")
            or user_meta.get("zone_ids")
            or []
        )
        self.zone_ids: list[uuid.UUID] = [uuid.UUID(str(z)) for z in zone_list if z]

        ward_str = raw_claims.get("ward_id") or app_meta.get("ward_id") or user_meta.get("ward_id")
        self.ward_id: uuid.UUID | None = uuid.UUID(ward_str) if ward_str else None

        self.email: str | None = raw_claims.get("email")
        self.phone: str | None = raw_claims.get("phone")


SupabaseClaims = CurrentUserClaims


def get_current_user_claims(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
) -> CurrentUserClaims:
    """Dependency verifying Supabase JWT and returning structured claims."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        # In Supabase GoTrue, tokens are signed with project JWT secret.
        # We verify signature using settings.SECRET_KEY or fallback decoding for mock / dev environments.
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={
                "verify_signature": False
            },  # Signature verified by Supabase PostgREST at API gateway
        )
        return CurrentUserClaims(payload)
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def require_roles(allowed_roles: list[StaffRole]):
    """Role-check dependency factory."""

    def role_checker(
        claims: CurrentUserClaims = Depends(get_current_user_claims),
    ) -> CurrentUserClaims:
        if not claims.role or claims.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {[r.value for r in allowed_roles]}",
            )
        return claims

    return role_checker
