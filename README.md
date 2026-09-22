# CivicBrain v14

Deterministic, glass-box civic triage and dispatch system built for Indian Urban Local Bodies (ULBs).

## Overview
CivicBrain sits on top of existing civic infrastructure (CPGRAMS, DIGIT/UPYOG) to produce an itemized, appealable, equity-corrected priority ranking across open civic cases city-wide. It operates on the **Bootstrap Principle** via Bühlmann credibility theory, requiring zero day-one government registries, census data, or IoT sensors.

## Core Features
- **Deterministic Priority Engine:** Severity, Risk, Exposure, Criticality, Urgency, and Confidence kept strictly separate; AHP-weighted scoring.
- **Equity Compensator v2:** Self-calibrated expected issue rates per ward via Bühlmann credibility blending ($Z = \frac{n}{n + K}$).
- **Row-Level Security (RLS):** True authorization boundary enforced in PostgreSQL, verified via client SDK with per-role JWTs across 24 tables.
- **Zero Recurring Cost:** Architected for Supabase Free, Render Free, and Upstash Redis Free.
- **Production Hardening:** ASGI security headers middleware (CSP, nosniff, DENY, HSTS), Redis sliding-window rate limiting, log-level PII scrubbing, sanitized 500 error handling, and 100% foreign key index coverage.
- **Backend / API Surface:** Modular FastAPI monolith with OpenAPI documentation.

## Phase Architecture

| Phase | Subsystem | Documentation |
|---|---|---|
| **Phase 0** | Foundations, Environment & Tooling | [Phase 0 Log](docs/phase-log/phase-0.md) |
| **Phase 1** | Identity, Multi-Tenant Hierarchy & RBAC | [Phase 1 Log](docs/phase-log/phase-1.md) |
| **Phase 2** | Domain Core, Incident Lifecycle & Dedup | [Phase 2 Log](docs/phase-log/phase-2.md) |
| **Phase 3** | Vision Ingestion, Living Taxonomy & Photo Splitting | [Phase 3 Spec](docs/specs/phase-3.md) / [Log](docs/phase-log/phase-3.md) |
| **Phase 4** | GIS Core & Spatial Analysis Pipeline | [Phase 4 Spec](docs/specs/phase-4.md) / [Log](docs/phase-log/phase-4.md) |
| **Phase 5** | NLP Pipeline, Multilingual & Emotion Decoupling | [Phase 5 Spec](docs/specs/phase-5.md) / [Log](docs/phase-log/phase-5.md) |
| **Phase 6** | AHP Prioritization & Bühlmann Equity Compensator | [Phase 6 Spec](docs/specs/phase-6.md) / [Log](docs/phase-log/phase-6.md) |
| **Phase 7** | Causal Root-Cause Linking & Cycle Prevention | [Phase 7 Spec](docs/specs/phase-7.md) / [Log](docs/phase-log/phase-7.md) |
| **Phase 8** | Evidence-Gated Dispatch & Verifier Consensus | [Phase 8 Spec](docs/specs/phase-8.md) / [Log](docs/phase-log/phase-8.md) |
| **Phase 9** | Field Companion (Karmi Sahayak) Offline Sync | [Phase 9 Spec](docs/specs/phase-9.md) / [Log](docs/phase-log/phase-9.md) |
| **Phase 10** | Analytics, Ward Report Card & Service ETA | [Phase 10 Spec](docs/specs/phase-10.md) / [Log](docs/phase-log/phase-10.md) |
| **Phase 11** | Citizen Transparency Board & Jan Sunwai Ledger | [Phase 11 Spec](docs/specs/phase-11.md) / [Log](docs/phase-log/phase-11.md) |
| **Phase 12** | Red-Team Audit, RLS Matrix & Compliance Scanner | [Phase 12 Spec](docs/specs/phase-12.md) / [Log](docs/phase-log/phase-12.md) |
| **Phase 13** | Security Headers, Redis Caching, Rate Limiting & Indexing | [Phase 13 Spec](docs/specs/phase-13.md) / [Log](docs/phase-log/phase-13.md) |

## Getting Started
```bash
# Clone the repository
git clone <repo-url>
cd civicbrain

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env

# Run local development server
uvicorn civicbrain.main:app --reload --port 8000
```

## Running Tests & Quality Gates
```bash
# Full test suite (107 passed tests)
pytest -v

# Code quality & type checks
ruff check .
ruff format --check .
mypy civicbrain

# Security & dependency audits
bandit -r civicbrain -ll
pip-audit .
```
