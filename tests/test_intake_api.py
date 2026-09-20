"""Integration tests for citizen intake and operational incidents APIs."""

import uuid

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

from civicbrain.infra.redis import set_redis_client
from civicbrain.main import app


@pytest.mark.asyncio
async def test_track_anonymous_report_not_found():
    """Verify tracking endpoint returns 404 for nonexistent token."""
    set_redis_client(fakeredis.aioredis.FakeRedis())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/v1/intake/reports/track?token=nonexistent_token_1234567890")
        assert res.status_code == 404


@pytest.mark.asyncio
async def test_track_anonymous_report_rate_limit():
    """Verify Redis-backed IP rate limiting on anonymous tracking token endpoint."""
    set_redis_client(fakeredis.aioredis.FakeRedis())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Make 12 rapid calls to exceed rate limit (limit is 10)
        statuses = []
        for _ in range(12):
            res = await client.get("/v1/intake/reports/track?token=dummy_token_1234567890123")
            statuses.append(res.status_code)

        # First 10 requests should pass through to token check (returning 404 for dummy token)
        assert statuses[:10] == [404] * 10
        # 11th and 12th requests must be rejected by Redis rate limiter with 429 Too Many Requests
        assert statuses[10] == 429
        assert statuses[11] == 429


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


@pytest.mark.asyncio
async def test_taxonomy_categories_listing_empty():
    """Verify /v1/taxonomy/categories returns empty list for org with no categories."""
    random_org_id = uuid.uuid4()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(f"/v1/taxonomy/categories?organization_id={random_org_id}")
        assert res.status_code == 200
        assert res.json() == []
