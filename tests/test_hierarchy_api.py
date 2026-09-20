"""Integration tests for hierarchy, representative, and auth endpoints."""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from jwt import encode

from civicbrain.infra.config import settings
from civicbrain.main import app


def create_test_token(user_id: uuid.UUID, role: str, org_id: uuid.UUID | None = None) -> str:
    """Generate unsigned/signed HS256 JWT for API dependency testing."""
    payload = {
        "sub": str(user_id),
        "email": f"user_{str(user_id)[:8]}@civicbrain.org",
        "app_metadata": {
            "org_id": str(org_id) if org_id else None,
            "role": role,
        },
    }
    return encode(payload, settings.SECRET_KEY, algorithm="HS256")


@pytest.mark.asyncio
async def test_auth_me_unauthorized():
    """Verify /v1/auth/me returns 401 when no token is provided."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/v1/auth/me")
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_auth_me_with_token():
    """Verify /v1/auth/me decodes claims from authenticated token."""
    uid = uuid.uuid4()
    org_id = uuid.uuid4()
    token = create_test_token(uid, "dispatcher", org_id)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["user_id"] == str(uid)
        assert data["organization_id"] == str(org_id)
        assert "dispatcher" in data["roles"]


@pytest.mark.asyncio
async def test_org_hierarchy_not_found():
    """Verify /v1/orgs/{org_id}/hierarchy returns 404 for nonexistent organization."""
    random_org_id = uuid.uuid4()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(f"/v1/orgs/{random_org_id}/hierarchy")
        assert res.status_code == 404
