"""Logging infrastructure and automated PII redaction filter."""

import logging
import re

# Regex patterns for sensitive citizen PII and authentication tokens
AADHAAR_PATTERN = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
PHONE_PATTERN = re.compile(r"(?:\+91[-\s]?|0)?[6-9]\d{9}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
BEARER_TOKEN_PATTERN = re.compile(
    r"(Bearer\s+)[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+(?:\.[A-Za-z0-9\-_.+/=]*)?",
    re.IGNORECASE,
)
API_KEY_PATTERN = re.compile(r"\b(?:sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z-_]{35})\b")


def scrub_log_message(message: str) -> str:
    """Replaces sensitive citizen PII and credentials with redact labels."""
    if not isinstance(message, str):
        message = str(message)
    message = BEARER_TOKEN_PATTERN.sub(r"\1[REDACTED_TOKEN]", message)
    message = API_KEY_PATTERN.sub("[REDACTED_KEY]", message)
    message = AADHAAR_PATTERN.sub("[REDACTED_AADHAAR]", message)
    message = PHONE_PATTERN.sub("[REDACTED_PHONE]", message)
    message = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", message)
    return message


class PIIScrubbingFilter(logging.Filter):
    """Logging filter that scrubs sensitive citizen PII and credentials from all log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.msg and isinstance(record.msg, str):
            record.msg = scrub_log_message(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: (scrub_log_message(v) if isinstance(v, str) else v)
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    scrub_log_message(v) if isinstance(v, str) else v for v in record.args
                )
        return True
