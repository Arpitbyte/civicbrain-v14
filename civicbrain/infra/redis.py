"""Upstash Redis connection and rate limiting client."""

import logging
from typing import Any, cast

import redis.asyncio as aioredis

from civicbrain.infra.config import settings

logger = logging.getLogger(__name__)

_redis_client: Any = None


def get_redis_client() -> aioredis.Redis:
    """Returns singleton async Redis client connected to UPSTASH_REDIS_URL."""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.UPSTASH_REDIS_URL,
            decode_responses=True,
            socket_timeout=5.0,
            socket_connect_timeout=5.0,
        )
    return cast(aioredis.Redis, _redis_client)


def set_redis_client(client: Any) -> None:
    """Overrides redis client (used for testing or dependency injection)."""
    global _redis_client
    _redis_client = client
