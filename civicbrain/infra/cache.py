"""Upstash Redis caching layer for hot, rarely-changing public reads."""

import json
import logging
from typing import Any

from civicbrain.infra.redis import get_redis_client

logger = logging.getLogger(__name__)


async def cache_get(key: str) -> Any | None:
    """Retrieves JSON-deserialized value from Redis cache. Fails open on connection error."""
    try:
        redis_client = get_redis_client()
        raw = await redis_client.get(key)
        if raw is not None:
            return json.loads(raw)
    except Exception as exc:
        logger.debug("Cache get error for key '%s': %s", key, exc)
    return None


async def cache_set(key: str, value: Any, ttl_seconds: int = 180) -> None:
    """Stores JSON-serialized value into Redis cache with specified TTL. Fails open on error."""
    try:
        redis_client = get_redis_client()
        raw = json.dumps(value, default=str)
        await redis_client.set(key, raw, ex=ttl_seconds)
    except Exception as exc:
        logger.debug("Cache set error for key '%s': %s", key, exc)


async def cache_delete(key: str) -> None:
    """Deletes cached key upon invalidation. Fails open on error."""
    try:
        redis_client = get_redis_client()
        await redis_client.delete(key)
    except Exception as exc:
        logger.debug("Cache delete error for key '%s': %s", key, exc)
