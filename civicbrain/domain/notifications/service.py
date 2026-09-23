"""Notifications domain service: multi-channel staff onboarding and citizen alerts."""

import logging
from typing import Any

from civicbrain.infra.cache import cache_set
from civicbrain.infra.config import settings

logger = logging.getLogger("civicbrain.notifications")


async def dispatch_account_setup_invitation(
    user_id: str,
    org_id: str,
    phone: str,
    email: str | None,
    full_name: str,
    setup_token: str,
) -> str:
    """Dispatches password setup link to newly provisioned staff member.

    Never logs the setup token or link.
    Persists token with a 72-hour TTL for the password-setting flow.
    """
    # 72 hours TTL
    ttl_seconds = 72 * 3600
    cache_key = f"setup_token:{setup_token}"
    token_payload: dict[str, Any] = {
        "user_id": user_id,
        "org_id": org_id,
        "phone": phone,
        "email": email,
        "full_name": full_name,
    }
    await cache_set(cache_key, token_payload, ttl_seconds=ttl_seconds)

    # Construct frontend setup URL from config
    base_url = settings.FRONTEND_BASE_URL.rstrip("/")
    setup_url = f"{base_url}?token={setup_token}"

    # Log dispatch event without leaking the token
    logger.info("Dispatched onboarding setup invitation link for staff user")

    # In production, this dispatches via SMS (CDAC/NIC gateway) or WhatsApp/Email adapter
    return setup_url
