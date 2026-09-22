# Phase 13: Security & Performance Hardening — Technical Specification

**Version:** CivicBrain v14.13.0  
**Phase:** 13  
**Status:** APPROVED & IMPLEMENTED  

---

## 1. Executive Summary & Scope

Phase 13 establishes the production-grade application security hardening, defensive middleware, dependency integrity verification, and database query performance optimization across the entire CivicBrain v14 architecture:

1. **Defensive ASGI Security Middleware:**
   - Injects mandatory security response headers on all endpoints: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.
2. **CORS Allowlist Validation:**
   - Enforces an explicit origin allowlist via Pydantic validator, permanently forbidding wildcards (`*`) to eliminate CSRF / credential exposure vulnerabilities.
3. **Global Exception Sanitization:**
   - Intercepts all unhandled exceptions globally, emitting generic JSON (`INTERNAL_SERVER_ERROR`, HTTP 500) while logging full diagnostic traces internally, preventing SQL syntax, table name, or internal stack trace leakage.
4. **Photo Upload Memory Ceiling:**
   - Streams photo uploads in 1MB chunks with a strict 10MB memory ceiling (`MAX_PHOTO_UPLOAD_BYTES`), rejecting oversized payloads immediately with `HTTP_413_CONTENT_TOO_LARGE` to protect free-tier memory budgets.
5. **Generalized Upstash Redis Rate Limiting:**
   - Replaces mock rate limiters with an IP-based sliding/fixed-window counter across public intake, photo uploads, tracking lookups, and citizen feedback endpoints, operating with fail-open resilience.
6. **Log-Level PII Scrubbing Filter:**
   - Attaches an automated regex filter to the root logger and handlers to redact Aadhaar numbers, 10-digit Indian phone numbers, emails, and JWT Bearer tokens before writing to disk or stdout.
7. **Database Foreign Key Indexing (Migration 0014):**
   - Applies supporting B-tree indexes on all unindexed foreign key and timestamp columns identified during a live Postgres catalog audit, achieving 100% (59/59) index coverage on foreign keys.
8. **Upstash Redis Hot Read Caching:**
   - Caches rarely-changing public reads (`/taxonomy/categories`, `/prioritization/ahp/matrix/active`, `/analytics/wards/{id}/report-card`) with automated cache invalidation upon administrative mutation.
9. **Automated Static Security & Vulnerability Gates:**
   - Integrates `bandit` (static code analysis) and `pip-audit` (dependency CVE scanner) into both developer requirements and CI workflows, asserting 0 vulnerabilities and 0 security issues.

---

## 2. Invariant Rules & Architectural Constraints

1. **Zero Secret Leakage Invariant:**
   - Log statements, HTTP response payloads, and exception messages must never reveal Aadhaar, phone numbers, auth tokens, database credentials, or internal schema details.
2. **Zero Wildcard CORS Invariant:**
   - CORS origin configuration must strictly reject `*` when initialized or updated.
3. **Fail-Open Resilience for Ephemeral Cache Invariant:**
   - Unavailability or network partitions to Redis must fail open, logging warnings without causing denial-of-service on municipal emergency reporting.
4. **100% Foreign Key Index Coverage Invariant:**
   - Every foreign key constraint in PostgreSQL must have a corresponding index to prevent table locks and slow sequential scans on parent deletions/updates.
5. **Deterministic Scanners in CI:**
   - Every push to `main` must pass Ruff, Mypy, Bandit (`bandit -r civicbrain -ll`), and Pip-Audit (`pip-audit .`) across Python 3.11 and 3.12.
