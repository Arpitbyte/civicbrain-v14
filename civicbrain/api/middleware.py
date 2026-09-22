"""Security and hardening ASGI middleware."""

from starlette.types import ASGIApp, Receive, Scope, Send


class SecurityHeadersMiddleware:
    """Injects standard defensive security headers into all HTTP responses.

    Enforces:
    - Content-Security-Policy (CSP): Restricts script, object, and frame injection.
    - X-Content-Type-Options: nosniff (Blocks MIME-type sniffing).
    - X-Frame-Options: DENY (Prevents clickjacking).
    - Referrer-Policy: strict-origin-when-cross-origin (Protects sensitive URLs).
    - Strict-Transport-Security (HSTS): 1-year preload HSTS.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_security_headers(message: dict) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend(
                    [
                        (b"x-content-type-options", b"nosniff"),
                        (b"x-frame-options", b"DENY"),
                        (b"referrer-policy", b"strict-origin-when-cross-origin"),
                        (
                            b"strict-transport-security",
                            b"max-age=31536000; includeSubDomains; preload",
                        ),
                        (
                            b"content-security-policy",
                            (
                                b"default-src 'self'; "
                                b"img-src 'self' data: https:; "
                                b"script-src 'self'; "
                                b"style-src 'self' 'unsafe-inline'; "
                                b"object-src 'none'; "
                                b"frame-ancestors 'none';"
                            ),
                        ),
                    ]
                )
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_security_headers)
