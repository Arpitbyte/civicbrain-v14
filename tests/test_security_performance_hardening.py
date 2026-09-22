"""Comprehensive verification tests for Security and Performance Hardening pass."""

import io
import logging
import uuid

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

from civicbrain.infra.cache import cache_delete, cache_get, cache_set
from civicbrain.infra.config import Settings
from civicbrain.infra.logging import PIIScrubbingFilter, scrub_log_message
from civicbrain.infra.redis import set_redis_client
from civicbrain.main import app


@pytest.mark.asyncio
async def test_security_headers_middleware():
    """1. Verify standard defensive security headers injected on all HTTP responses."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/")
        assert res.status_code == 200
        headers = res.headers
        assert headers.get("x-content-type-options") == "nosniff"
        assert headers.get("x-frame-options") == "DENY"
        assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
        assert "max-age=31536000" in headers.get("strict-transport-security", "")
        assert "default-src 'self'" in headers.get("content-security-policy", "")
        assert "frame-ancestors 'none'" in headers.get("content-security-policy", "")


@pytest.mark.asyncio
async def test_cors_explicit_allowlist_forbids_wildcard():
    """2. Verify CORS allows only explicit origins and forbids wildcard '*'."""
    # Explicit allowed origin
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"

    # Unauthorized origin
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.options(
            "/",
            headers={
                "Origin": "https://evil-hacker.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert res.headers.get("access-control-allow-origin") != "https://evil-hacker.com"

    # Pydantic Settings forbids wildcard '*'
    with pytest.raises(ValueError, match="Wildcard '\\*' origin is forbidden"):
        Settings(CORS_ORIGINS="http://localhost:3000,*")


@pytest.mark.asyncio
async def test_global_exception_handler_sanitization():
    """3. Verify unhandled exceptions return generic message without leaking trace or SQL."""

    # Add temporary route raising an internal exception with simulated DB trace
    @app.get("/test-unhandled-error-simulation", include_in_schema=False)
    async def error_simulation_route():
        raise RuntimeError("CRITICAL_DB_SYNTAX: SELECT * FROM secret_table WHERE pass='1234'")

    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False), base_url="http://test"
    ) as client:
        res = await client.get("/test-unhandled-error-simulation")
        assert res.status_code == 500
        data = res.json()
        assert data["error_code"] == "INTERNAL_SERVER_ERROR"
        assert "internal server error occurred" in data["detail"].lower()
        # Ensure zero leakage of query text or internal identifiers
        assert "secret_table" not in res.text
        assert "1234" not in res.text
        assert "Traceback" not in res.text


@pytest.mark.asyncio
async def test_photo_upload_size_limit_413():
    """4. Verify photo uploads exceeding 10MB are rejected with 413 Payload Too Large."""
    set_redis_client(fakeredis.aioredis.FakeRedis())
    from tests.test_hierarchy_api import create_test_token

    org_id = uuid.uuid4()
    token = create_test_token(uuid.uuid4(), "admin", org_id)

    # Generate mock 11MB file payload in memory
    oversized_bytes = b"X" * (11 * 1024 * 1024)
    file_payload = ("test_large.jpg", io.BytesIO(oversized_bytes), "image/jpeg")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post(
            "/v1/intake/reports/photo",
            data={
                "organization_id": str(org_id),
                "latitude": "12.9716",
                "longitude": "77.5946",
                "channel": "pwa",
            },
            files={"image": file_payload},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 413
        assert "exceeds maximum allowed size" in res.json()["detail"]


@pytest.mark.asyncio
async def test_generalized_rate_limiter_intake_reports():
    """5. Verify generalized IP rate limiter protects POST /v1/intake/reports."""
    set_redis_client(fakeredis.aioredis.FakeRedis())
    from tests.test_hierarchy_api import create_test_token

    org_id = uuid.uuid4()
    token = create_test_token(uuid.uuid4(), "admin", org_id)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        statuses = []
        payload = {
            "organization_id": str(org_id),
            "latitude": 12.9716,
            "longitude": 77.5946,
            "channel": "pwa",
            "observations": [],
        }
        # Limit is 20 requests per minute
        for _ in range(22):
            res = await client.post(
                "/v1/intake/reports",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            statuses.append(res.status_code)

        # First 20 pass through (returning 404 since dummy org doesn't exist)
        assert statuses[:20] == [404] * 20
        # 21st and 22nd rejected with 429
        assert statuses[20] == 429
        assert statuses[21] == 429


def test_log_level_pii_scrubbing():
    """7. Verify log-level filter scrubs Aadhaar, phone numbers, emails, and JWTs."""
    raw_text = (
        "Citizen 9876543210 filed grievance with Aadhaar 1234 5678 9012 and email citizen@gov.in. "
        "Token: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.do_not_leak"
    )
    scrubbed = scrub_log_message(raw_text)

    assert "9876543210" not in scrubbed
    assert "[REDACTED_PHONE]" in scrubbed
    assert "1234 5678 9012" not in scrubbed
    assert "[REDACTED_AADHAAR]" in scrubbed
    assert "citizen@gov.in" not in scrubbed
    assert "[REDACTED_EMAIL]" in scrubbed
    assert "eyJhbGciOiJIUzI1NiJ9" not in scrubbed
    assert "[REDACTED_TOKEN]" in scrubbed

    # Test PIIScrubbingFilter in actual LogRecord
    flt = PIIScrubbingFilter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Contact phone is 9123456780",
        args=(),
        exc_info=None,
    )
    flt.filter(record)
    assert "9123456780" not in record.msg
    assert "[REDACTED_PHONE]" in record.msg


@pytest.mark.asyncio
async def test_redis_caching_layer():
    """8. Verify Upstash Redis caching for hot public reads."""
    fake = fakeredis.aioredis.FakeRedis()
    set_redis_client(fake)

    key = "cache:test_key"
    val = {"status": "ok", "items": [1, 2, 3]}

    # Cache miss
    assert await cache_get(key) is None

    # Cache set
    await cache_set(key, val, ttl_seconds=60)

    # Cache hit
    cached = await cache_get(key)
    assert cached == val

    # Cache delete
    await cache_delete(key)
    assert await cache_get(key) is None
