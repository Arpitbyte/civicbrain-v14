# FRONTEND_CONTEXT.md — CivicBrain Frontend Source of Truth

> This is the compact product/backend reference the frontend team works from.
> Full backend detail lives in `PROJECT_REFERENCE_FOR_FRONTEND.md` — read that only
> when this file doesn't answer the question. Do not re-derive product facts already
> captured here.

## 1. What CivicBrain is

A **civic prioritization and dispatch intelligence system**, not a grievance ticketing
tool and not an AI chatbot wrapper. It sits on top of existing municipal infrastructure
(CPGRAMS/DIGIT) and turns multi-channel citizen complaints into an itemized, appealable,
equity-corrected priority ranking.

**Bootstrap Principle**: assumes zero day-one asset registries, zero census data, zero
IoT sensors. Every score is derived transparently from the platform's own accumulated
history via Bühlmann credibility (`Z = n / (n + K)`), blending city-wide priors into
ward-level reality as data volume grows. **The UI must never claim more certainty than
the data supports.**

## 2. The 7 workspaces (dual-named, distinct cohorts)

| Workspace | Vernacular | Users | Register |
|---|---|---|---|
| Citizen Portal | Nagrik Setu | Citizens | Warm, accessible, multilingual |
| Command Deck | — | Dispatchers, Ops Chiefs | Dense, operational, precise |
| Ops Board | — | Dept Supervisors/JEs | Departmental queue mgmt |
| City Pulse | — | Zonal Supervisors, Analysts | Spatial, analytical |
| Field Companion | Karmi Sahayak | Field workers | Mobile, outdoor, offline-first |
| Control Room | — | Commissioners, Admins | Structured, administrative |
| Transparency Board | Jan Sunwai Ledger / Nagar Pragati | Corporators, Public, Media | Open, evidentiary, public |

## 3. Entity model (condensed — 25 tables, see reference doc §4 for full ERD)

```
intake_report (citizen submission, tracking token)
  └─ observation (1 atomic defect, 1 dept, CV/NLP extracted)
       └─ incident (deduplicated case, 11-state lifecycle, priority score)
            ├─ work_order (dispatch task → field worker)
            ├─ incident_dedup_link (Fellegi-Sunter probabilistic linkage)
            ├─ incident_causal_link (upstream root cause → downstream symptom)
            ├─ dispatch_conflict_review (offline sync collision, needs adjudication)
            └─ jan_sunwai_ledger_entry (immutable public audit trail)

ward ── ward_equity_credibility (Z factor) ── ward_resolution_stat ── ward_report_card_snapshot
```

**Score formula (must be user-visible, itemized, never opaque):**
```
priority_score = raw_priority_score × (1 + equity_boost)
raw_priority_score = S·w_s + R·w_r + E·w_e + C·w_c + U·w_u   (AHP, 5 criteria)
equity_boost = f(ward vulnerability, Bühlmann credibility Z)
```
Severity/Risk/Exposure/Criticality/Urgency definitions: see reference doc §2.2. Every
score-bearing UI must show its confidence (`Z`) and let the user expand the breakdown.

## 4. The 11-state incident lifecycle

```
reported → triaged → verified → prioritized → assigned → in_progress → resolved → confirmed
                ↘ rejected ↗(appeal)→ reopened → prioritized
                                  resolved ↘(dispute)→ appealed
```
`work_order`: `created → dispatched → accepted → in_progress → completed` (+ `cancelled`).

**Least-advanced-child rule (§7.2, non-negotiable UI rule):** a citizen's intake report
status = the least-advanced status among its child incidents. A report with a resolved
Roads issue and an in-progress Electrical issue shows **in_progress**, never "Resolved."
Every observation gets its own progress indicator — never collapse to one bar.

## 5. Roles (6 staff roles + citizen, RLS-enforced)

`citizen` → Nagrik Setu + public Transparency Board only.
`field_worker` → Karmi Sahayak, own assigned work orders only.
`department_staff` → Ops Board, own department city-wide.
`dispatcher` → Command Deck, city-wide.
`zonal_supervisor` → City Pulse, zone-wide.
`corporator` → Transparency Board / ward digest, own ward only, read-only on ops data.
`admin` → Control Room + all boards, org-wide.

## 6. API surface — grouped by workspace

Full 46-path/50-op list is in the reference doc §5. Frontend teams should generate a
typed client from `/v1/openapi.json` rather than hand-writing fetch calls (see
`UI_ARCHITECTURE.md` §API client). Key shape to remember: most staff endpoints are
scoped by department/zone/ward via RLS — the frontend does not need to hide UI by role
beyond routing, but should still gate navigation to avoid dead-end 403 screens.

## 7. Hard constraints — do not violate

1. **No fake AI confidence.** CV pipeline is honest cold-start: observations are
   "Citizen Declared" or "Pending Automated Triage" — never "AI Detected: X (98% conf)."
2. **No fake data / decorative charts.** Every chart/number must trace to a real
   endpoint. Empty states are real states, not hidden with placeholder content.
3. **Do not build screens for unbuilt backend features**: Proactive Inspection Engine,
   Cross-Domain Signal Correlation are specified-but-unbuilt — do not design for them yet.
4. **Confidence and evidence are first-class UI**, never an afterthought or tooltip.
5. **Photos are evidence**, shown large with GPS/timestamp/redaction badges, not
   thumbnail attachments. Work order completion = side-by-side before/after.
6. Zero existing frontend code — this is a greenfield build against a live, stable API.

## 8. Status of this documentation set

- `FRONTEND_CONTEXT.md` — this file. Product/backend truth. ✅ established.
- `DESIGN.md` — design system (tokens, type, color, motion, workspace personalities). ✅ established.
- `UI_ARCHITECTURE.md` — tech stack, repo structure, state/data/offline architecture. ✅ established.
- `SCREEN_SPECS.md` — complete sitemap, shared component architecture, and full
  per-screen design (layout/composition/imagery/motion/states/data mapping) for all
  30 screens across 7 workspaces. ✅ established, v2.
- `ANTIGRAVITY_PROMPTS.md` — every paste-ready Antigravity implementation prompt, in
  build order (foundation → shells → nav → primitives → 7 representative screens →
  remaining 22 screens → responsive/motion/a11y/polish passes). ✅ established.
- `IMPLEMENTATION_LOG.md` — running build history. Antigravity appends one dated entry
  per completed prompt (files touched, deviations, gaps, states implemented,
  acceptance-criteria self-check). This is what `AUDIT.md` gets run against. ⏳ template
  only — first entry lands once PROMPT 0 is complete.
- `AUDIT.md` — audit framework. ⏳ template only — no code exists yet to audit.

**Note**: all of the above live together in the project's frontend-context docs folder
(the user maintains this folder locally/in-repo) — reference them by filename in any
new prompt or session, they are not re-derived from scratch.

When any of these change, edit the file directly rather than restating its contents in
chat. Antigravity prompts should cite section headers from these docs, not reproduce them.
