"""Generalized IP-based rate limiting via Upstash Redis."""

import logging

from fastapi import HTTPException, Request, status

from civicbrain.infra.redis import get_redis_client

logger = logging.getLogger(__name__)


class RateLimiter:
    """FastAPI dependency for sliding/fixed-window IP rate limiting via Upstash Redis."""

    def __init__(
        self,
        max_requests: int = 20,
        window_seconds: int = 60,
        prefix: str = "general",
    ) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.prefix = prefix

    async def __call__(self, request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown_client"
        key = f"rate_limit:{self.prefix}:{client_ip}"

        redis_client = get_redis_client()
        try:
            current = await redis_client.incr(key)
            if current == 1:
                await redis_client.expire(key, self.window_seconds)

            if current > self.max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=(
                        f"Rate limit exceeded: maximum {self.max_requests} requests "
                        f"per {self.window_seconds}s. Please retry later."
                    ),
                )
        except HTTPException:
            raise
        except Exception as exc:
            logger.warning(
                "Redis rate limiter error on prefix '%s' for IP %s: %s. Failing open.",
                self.prefix,
                client_ip,
                exc,
            )
            # Fail-open: do not block critical civic requests if Redis cache is temporarily unreachable
            return
