"""Smoke and integration tests for health and readiness endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from civicbrain.infra.config import settings
from civicbrain.main import app


@pytest.mark.asyncio
async def test_health_endpoint_liveness():
    """Verify that /v1/health returns HTTP 200 and expected liveness schema."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == settings.VERSION
        assert data["environment"] == settings.ENVIRONMENT
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_ready_endpoint_schema():
    """Verify that /v1/ready returns valid readiness response format."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/v1/ready")
        # In mock or disconnected local environment, status may be 200 (if local db exists) or 503
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "database_connected" in data
        assert "redis_connected" in data
        assert "details" in data
        assert "timestamp" in data


@pytest.mark.asyncio
async def test_root_endpoint_metadata():
    """Verify that root endpoint provides documentation links."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == settings.PROJECT_NAME
        assert data["docs_url"] == "/v1/docs"
