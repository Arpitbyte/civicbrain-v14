"""Integration tests for citizen intake and operational incidents APIs."""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from civicbrain.main import app


@pytest.mark.asyncio
async def test_track_anonymous_report_not_found():
    """Verify tracking endpoint returns 404 for nonexistent token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/v1/intake/reports/track?token=nonexistent_token_1234567890")
        assert res.status_code == 404


@pytest.mark.asyncio
async def test_track_anonymous_report_rate_limit():
    """Verify IP rate limiting on anonymous tracking token endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Make 12 rapid calls to exceed rate limit (limit is 10)
        statuses = []
        for _ in range(12):
            res = await client.get("/v1/intake/reports/track?token=dummy_token_1234567890123")
            statuses.append(res.status_code)

        # At least one request should have hit 429 Too Many Requests
        assert 429 in statuses


@pytest.mark.asyncio
async def test_incidents_listing_nonexistent_org():
    """Verify /v1/incidents returns empty list for empty or non-existent org."""
    random_org_id = uuid.uuid4()
    from tests.test_hierarchy_api import create_test_token

    token = create_test_token(uuid.uuid4(), "admin", random_org_id)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(
            f"/v1/incidents?organization_id={random_org_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 200
        assert res.json() == []
