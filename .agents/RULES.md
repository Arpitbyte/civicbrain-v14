# CivicBrain v14 — Operational Rules & Architecture Ground Truth

This document contains the persistent, non-negotiable hard rules, administrative domain model, file skeleton, bootstrap mechanism, and phase roadmap for CivicBrain v14. Every agent prompt, phase implementation, and review must adhere to these directives without exception.

---

## 1. The 17 Hard Rules

1. **No fabrication:** Never invent datasets, APIs, statistics, government integrations, model performance numbers, or legal conclusions. Write `UNKNOWN / NEEDS VERIFICATION` (or `NEEDS LEGAL VERIFICATION`) and stop rather than guess. All unbenchmarked performance claims and unvalidated statistical cutoffs must be labeled as provisional defaults, not settled facts.
2. **No operational data fabrication:** Synthetic/demo data lives strictly under `demo_namespace`, visibly labeled, and is never joined into production analytics or the Priority Engine. A stub external integration (DIGIT/CPGRAMS) returns clearly-labeled mock data or raises "not configured" — never a fabricated realistic response.
3. **Strict conceptual separation:** Keep `Severity ≠ Risk ≠ Exposure ≠ Criticality ≠ Urgency ≠ Priority ≠ Confidence` separate everywhere — in database schemas, API contracts, domain logic, and documentation.
4. **Deterministic over LLM:** Never use an LLM where a deterministic algorithm, database operation, geospatial function, or conventional ML/statistics fits better — especially deduplication, scoring, and routing. LLMs (Reasoning Trace, Civic Assistant) may only explain or converse — never compute a score, never alter case state.
5. **RLS is the real authorization boundary & Scoped Grants:** Row-Level Security in PostgreSQL is the true perimeter, tested via the client SDK using real per-role JWTs, never tested via the SQL editor or a service-role bypass connection. In addition (per Supabase's May 30, 2026 default where tables are not auto-exposed), every migration creating a table must include explicit per-role `GRANT` statements scoped strictly to necessary operations (never blanket `GRANT ALL`).
6. **Interoperate before building:** Before writing citizen-facing intake or tracking features, verify whether a DIGIT/UPYOG or CPGRAMS adapter is the honest answer instead of rebuilding a from-scratch feature.
7. **Language work is not optional polish:** NLP and CV acceptance criteria must include a romanized-script (Hinglish/transliterated) test case specifically, not just native-script datasets.
8. **No blocking on unavailable legal/partner approvals:** Build the legally-safe default and stub external integrations behind clean interfaces with sandbox data. Document governance requirements (Aadhaar sign-off, DPDP exemptions, STQC) as design considerations that do not block progress.
9. **Self-bootstrapping only (The Bootstrap Principle):** No feature may assume a pre-existing government asset registry, census/socioeconomic data, or IoT sensor hardware. All baselines derive from CivicBrain's own accumulated, verified data via Bühlmann credibility blending, starting from a neutral prior.
10. **Zero recurring cost:** Every infrastructure piece runs on free tiers (Supabase Free: Postgres+PostGIS+Auth+Storage+RLS; Render Free: FastAPI web service + Celery worker; Upstash Redis Free: broker). Never silently add paid services.
11. **Backend/API only:** No frontend or UI code until explicitly authorized. Every phase produces an API Surface (endpoints, response schemas, OpenAPI documentation, CORS) rather than built UI.
12. **Scope lock:** Only create or modify files explicitly listed for the current active phase. Anything else must be flagged in replies, not modified.
13. **Mandatory phase documentation:** After completing any phase, write or append `/docs/phase-log/phase-{N}.md` detailing what was built, key decisions, spec deviations, and open TODOs as a committed repository file.
14. **One persistent rules file:** This file (`.agents/RULES.md`) is the single ground truth. Future prompts reference this file instead of re-attaching the master specification document.
15. **One phase at a time:** Full phase specification must be reviewed and approved before writing any implementation code. Do not jump ahead or merge phases.
16. **Research before reinventing:** Base architecture and algorithmic choices on proven research standards (e.g., AHP, Fellegi-Sunter, Bühlmann credibility, Laplace differential privacy) and cite why they were selected.
17. **Query the graph, don't re-read the codebase:** Graphify is installed and active with git hooks. Query the knowledge graph (`graphify query`, `graphify path`, `graphify explain`, `graphify affected`) rather than grepping or re-reading whole files across sessions.

---

## 2. The Bootstrap Principle (Self-Calibrating Intelligence)

CivicBrain assumes zero pre-existing government data, census statistics, or IoT hardware. All intelligence is built from data generated through platform usage using **Bühlmann credibility theory**:

$$\text{estimate} = Z \times (\text{observed ward/asset data}) + (1 - Z) \times (\text{city-wide collective average})$$
$$Z = \frac{n}{n + K}$$

Where:
- $n$ is the count of verified data points accumulated by CivicBrain for that specific entity.
- $K$ is a tunable variance constant.
- When $n = 0$, $Z = 0$, falling back safely to the collective average with **Low Confidence**.
- As $n \to \infty$, $Z \to 1$, trusting local observed history with **High Confidence**.

Confidence is always exposed transparently to operators and citizens alongside priority scores and inspection recommendations.

---

## 3. Directory & File Skeleton

```
civicbrain/
  api/                 # FastAPI routers per module, versioned (/v1/...)
    v1/
  domain/              # Pure business logic, no framework dependencies
    identity/          # RBAC, tenant models, user accounts, Corporator scope
    intake/            # Intake reports, observations, incident clustering
    gis/               # PostGIS queries, GeoJSON generation, spatial joins
    cases/             # Case state machine, ERP workflows, SLA tracking
    priority/          # AHP scoring, Equity Compensator v2, Reasoning Trace validator
    notifications/     # Multi-channel notification routing
  workers/             # Celery async tasks (NLP, CV, priority, alerts)
  infra/               # DB sessions, Supabase client, storage, redis, external adapters
  schemas/             # Pydantic request/response schemas (strict typing)
  tests/               # Unit, integration, property-based, RLS client tests
docs/
  phase-log/           # Phase audit logs (phase-0.md, phase-1.md, ...)
.agents/
  RULES.md             # This persistent rules file
  rules/graphify.md    # Graphify rule integration
  workflows/graphify.md
graphify-out/          # Codebase knowledge graph (graph.json, graph.html, GRAPH_REPORT.md)
.graphifyignore        # Exclusions for knowledge graph
integrations/          # DIGIT/UPYOG and CPGRAMS stub adapters
```

---

## 4. Phase Roadmap (Summary)

- **Phase 0 — Foundations:** Scaffolding, CI/CD, Postgres/PostGIS connection, health checks, empty RLS-enabled schema (`organization` table with `ulb_type`), Phase 0 docs.
- **Phase 1 — Identity & RBAC:** Supabase Auth JWT claims, multi-tenant ULB hierarchy (`organization`, `zone`, `ward`), roles (Admin, Dispatcher, Inspector, Field Worker, Corporator), RLS client tests.
- **Phase 2 — Domain Core:** `intake_report` → `observation` → `incident` split supporting multi-issue photos across departments; `intake_report.status` tracks least-advanced child incident status while observations display individually (§A7); Fellegi-Sunter / Splink deduplication foundation.
- **Phase 3 — Citizen Intake:** Multi-channel ingestion (PWA, WhatsApp, Missed-Call/IVR, CSC), accessibility-first voice/contrast flows, provenance stamping, citizen report integrity layer.
- **Phase 4 — GIS Core:** PostGIS spatial queries, direct GeoJSON serving to MapLibre GL JS, spatial clustering, zero-cost architecture without self-hosted tile servers.
- **Phase 5 — NLP Pipeline:** IndicBERT, IndicXlit transliteration, IndicWav2Vec IVR processing, romanized Hinglish test evaluations, Emotion-Severity Decoupling.
- **Phase 6 — Computer Vision:** YOLO-World-v2 zero-shot detection for Indian civic categories, Living Taxonomy governance with HDBSCAN (approving category requires severity rubric defaulting to Bühlmann-blended baseline; distinct from static AHP sub-score weights), mandatory face/license-plate redaction.
- **Phase 7 — Priority Engine:** AHP pairwise weights with Consistency Ratio checking (weights compare Severity/Risk/Exposure/Criticality/Urgency against each other), self-bootstrapped Equity Compensator v2, Reasoning Trace deterministic validator, property-based tests, Causal Root-Cause Linking, Monsoon Surge Protocol.
- **Phase 8 — Dispatch & ERP:** Full state machine (`Reported` to `Confirmed`), SLA timers, department handoffs, Command Deck APIs.
- **Phase 9 — Field Companion:** Karmi Sahayak APIs, offline sync state lattice conflict resolution, post-resolution satisfaction loop, auto-escalation on dissatisfaction.
- **Phase 10 — Analytics & ETA:** Ward Report Card, Corporator Digest, Service-Time / ETA prediction engine accounting for spatial and departmental workload queueing.
- **Post-10 Addenda:** Proactive Inspection Engine (decay curves self-calibrated via Bühlmann credibility), Cross-Domain Signal Correlation (spatial leading indicators across departments).
- **Phase 11 — Transparency Board:** Jan Sunwai Ledger, differential privacy on public exports (suppress below absolute floor n < 5; calibrated Laplace noise only above floor), Nagar Pragati feed, read-only Civic Assistant.
- **Phase 12 — Hardening:** Full security, DPDP compliance audit, load tests, red-team penetration checks.

---

## 5. Specific Invariant Rules (v14 Re-derivations)

1. **Living Taxonomy Category Governance (§A11):** Approving a new category into the taxonomy requires defining its severity rubric, defaulting to a Bühlmann-blended city-wide baseline until refined. This is entirely separate from the AHP weights in §A12 — AHP weights compare Severity, Risk, Exposure, Criticality, and Urgency against each other and are **never** re-run when a category is added.
2. **Differential Privacy Floor & Laplace Calibration (§A23):** On public aggregate exports, counts below an absolute floor ($n < 5$) must be suppressed entirely rather than adding noise. Calibrated statistical noise (Laplace mechanism) is applied **only above that floor** ($n \ge 5$).
3. **Multi-Issue Single Report State Aggregation (§A7):** For an `intake_report` containing multiple CV/NLP observations split across department-scoped child incidents, `intake_report.status` is strictly defined as the **least-advanced status** among its child incidents (e.g., if one child incident is `Resolved` and another is `InProgress`, the parent report status remains `InProgress`). Furthermore, Nagrik Setu must present the status of each child `observation` individually so citizens have complete visibility.
4. **Mandatory Explicit Per-Role Table Grants (Supabase Post-May 2026 Default):** Because "Automatically expose new tables" is disabled in PostgREST/Supabase, every future migration that creates a table must include explicit per-role `GRANT` statements (not just `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`) for every role that needs to access it. Grants must be **strictly scoped to only the operations that role actually needs** (e.g. `anon` gets `SELECT` only where citizen-facing public queries are intended; `authenticated` and `service_role` get only what their specific domain workflows require) — **never a blanket `GRANT ALL`**. RLS policies filter rows only after table-level privilege is granted; without explicit grants, PostgREST denies all access unconditionally. This is a standing rule across all phases starting now.
5. **Literal Unedited Evidence in Reports (No Reconstruction):** Any evidence included in a report to the user — test execution output, CI results, file listings, schema dumps, query results — must be the literal, unedited output of the command that produced it, pasted directly. Never reconstruct, reformat into a summary table, or recall from memory what a command's output "would have shown." If the raw output is not already saved, re-run the command and paste what it actually returns. Whenever unsure whether something about to be reported was directly observed or reconstructed, treat that uncertainty itself as a mandatory requirement to re-verify before writing it down.


