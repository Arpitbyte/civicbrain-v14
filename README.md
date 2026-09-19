# CivicBrain v14

Deterministic, glass-box civic triage and dispatch system built for Indian Urban Local Bodies (ULBs).

## Overview
CivicBrain sits on top of existing civic infrastructure (CPGRAMS, DIGIT/UPYOG) to produce an itemized, appealable, equity-corrected priority ranking across open civic cases city-wide. It operates on the **Bootstrap Principle** via Bühlmann credibility theory, requiring zero day-one government registries, census data, or IoT sensors.

## Core Features
- **Deterministic Priority Engine:** Severity, Risk, Exposure, Criticality, Urgency, and Confidence kept strictly separate; AHP-weighted scoring.
- **Equity Compensator v2:** Self-calibrated expected issue rates per ward via Bühlmann credibility blending ($Z = \frac{n}{n + K}$).
- **Row-Level Security (RLS):** True authorization boundary enforced in PostgreSQL, verified via client SDK with per-role JWTs.
- **Zero Recurring Cost:** Architected for Supabase Free, Render Free, and Upstash Redis Free.
- **Backend / API Surface:** Modular FastAPI monolith with OpenAPI documentation.

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

## Running Tests
```bash
pytest -v
```
